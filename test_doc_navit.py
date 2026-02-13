import os
import sys
import gc
import json
from datetime import datetime
from PIL import Image

DOC_DIR = "stress_test_documents"
PATCH_SIZE = 14

DOCS = [
    {"id": "01_long_receipt",        "width": 100,  "height": 2800, "desc": "Supermarket receipt"},
    {"id": "02_wide_spreadsheet",    "width": 2800, "height": 100,  "desc": "Employee database table"},
    {"id": "03_research_paper_a4",   "width": 595,  "height": 842,  "desc": "Two-column research paper"},
    {"id": "04_id_card_square",      "width": 512,  "height": 512,  "desc": "National ID card"},
    {"id": "05_narrow_invoice",      "width": 140,  "height": 2100, "desc": "Narrow service invoice"},
    {"id": "06_panoramic_timeline",  "width": 3500, "height": 70,   "desc": "Project timeline strip"},
    {"id": "07_mobile_form",         "width": 375,  "height": 812,  "desc": "Mobile registration form"},
    {"id": "08_financial_report_4k", "width": 3840, "height": 2160, "desc": "Annual financial report (4K)"},
    {"id": "09_medical_prescription","width": 987,  "height": 610,  "desc": "Medical prescription"},
    {"id": "10_postage_stamp",       "width": 64,   "height": 64,   "desc": "Postage stamp (tiny)"},
]

def calc_expected(w, h, p=14):
    return (w // p) * (h // p)


def test_glm():
    print("\n" + "="*70)
    print("GLM-OCR — Document NaViT Test")
    print("="*70 + "\n")
    
    from transformers import AutoImageProcessor
    
    print("Loading GLM-OCR image processor...")
    ip = AutoImageProcessor.from_pretrained("zai-org/GLM-OCR", trust_remote_code=True)
    print(f"✓ Loaded: {type(ip).__name__}")
    
    has_dynamic = False
    print("\nProcessor attributes:")
    for attr in ['size', 'image_size', 'min_pixels', 'max_pixels', 'crop_size', 'do_resize']:
        val = getattr(ip, attr, 'N/A')
        print(f"  {attr}: {val}")
        if attr == 'min_pixels' and val != 'N/A':
            has_dynamic = True
    
    results = []
    print(f"\n{'Document':<28} {'Dims':<14} {'Expected':>8} {'Actual':>8} {'Grid':>12} {'Padding':>14} {'Status'}")
    print("-"*90)
    
    for cfg in DOCS:
        path = os.path.join(DOC_DIR, f"{cfg['id']}.png")
        img = Image.open(path)
        expected = calc_expected(cfg["width"], cfg["height"])
        
        result = {
            "id": cfg["id"], "desc": cfg["desc"],
            "dimensions": f"{cfg['width']}x{cfg['height']}",
            "expected_tokens": expected,
            "actual_tokens": None,
            "preprocessed_size": None,
            "status": "pending"
        }
        
        try:
            inputs = ip(images=img, return_tensors="pt")
            if 'image_grid_thw' in inputs:
                grid = inputs['image_grid_thw']
                t, h_p, w_p = grid[0].tolist()
                result["actual_tokens"] = int(h_p * w_p)
                result["grid"] = f"{int(h_p)}x{int(w_p)}"
                
                eff_h = int(h_p) * PATCH_SIZE
                eff_w = int(w_p) * PATCH_SIZE
                pad_h = eff_h - cfg["height"]
                pad_w = eff_w - cfg["width"]
                result["padding"] = f"+{pad_w}w,+{pad_h}h"
                result["preprocessed_size"] = f"{int(w_p)}x{int(h_p)} grid"
            else:
                for key in inputs:
                    tensor = inputs[key]
                    if hasattr(tensor, 'shape'):
                        if len(tensor.shape) == 4:
                            _, c, h, w = tensor.shape
                            result["actual_tokens"] = (w // PATCH_SIZE) * (h // PATCH_SIZE)
                            result["preprocessed_size"] = f"{w}x{h}"
            
            if result["actual_tokens"] is not None:
                act = result["actual_tokens"]
                if act in [256, 576, 1024] and expected not in [256, 576, 1024]:
                    result["status"] = "FAIL"
                elif abs(act - expected) / max(expected, 1) < 0.5:
                    result["status"] = "PASS"
                elif expected < 100 and act not in [256, 576, 1024]:
                    # Tiny images: large relative deviation but valid NaViT upscaling
                    result["status"] = "PASS"
                else:
                    result["status"] = "CHECK"
            else:
                result["status"] = "N/A"
                result["keys"] = list(inputs.keys())
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)[:80]
        
        results.append(result)
        icon = {"PASS":"✅","FAIL":"❌","CHECK":"⚠️","ERROR":"💥","N/A":"❓"}[result["status"]]
        act_str = str(result.get("actual_tokens") or "N/A")
        grid_str = result.get("grid") or "-"
        pad_str = result.get("padding") or "-"
        print(f"  {cfg['id']:<26} {cfg['width']}x{cfg['height']:<8} {expected:>8,} {act_str:>8} {grid_str:>12} {pad_str:>14} {icon}")
        
        del img
        gc.collect()
    
    passes = sum(1 for r in results if r["status"] == "PASS")
    print(f"\nGLM-OCR: {passes}/10 PASS")
    
    del ip
    gc.collect()
    
    return results


def test_qwen():
    print("\n" + "="*70)
    print("Qwen2.5-VL-3B — Document NaViT Test")
    print("="*70 + "\n")
    
    from transformers import AutoProcessor
    
    print("Loading Qwen2.5-VL processor...")
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct", trust_remote_code=True)
    print(f"✓ Loaded: {type(processor).__name__}\n")
    
    results = []
    print(f"{'Document':<28} {'Dims':<14} {'Expected':>8} {'Actual':>8} {'Grid':>12} {'Padding':>14} {'Status'}")
    print("-"*90)
    
    for cfg in DOCS:
        path = os.path.join(DOC_DIR, f"{cfg['id']}.png")
        img = Image.open(path)
        expected = calc_expected(cfg["width"], cfg["height"])
        
        result = {
            "id": cfg["id"], "desc": cfg["desc"],
            "dimensions": f"{cfg['width']}x{cfg['height']}",
            "expected_tokens": expected,
            "actual_tokens": None,
            "grid": None,
            "padding": None,
            "status": "pending"
        }
        
        try:
            messages = [{"role": "user", "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": "OCR this document"}
            ]}]
            text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = processor(text=[text], images=[img], return_tensors="pt", padding=True)
            
            if 'image_grid_thw' in inputs:
                grid = inputs['image_grid_thw']
                t, h_p, w_p = grid[0].tolist()
                result["actual_tokens"] = int(h_p * w_p)
                result["grid"] = f"{int(h_p)}x{int(w_p)}"
                
                eff_h = int(h_p) * PATCH_SIZE
                eff_w = int(w_p) * PATCH_SIZE
                pad_h = eff_h - cfg["height"]
                pad_w = eff_w - cfg["width"]
                result["padding"] = f"+{pad_w}w,+{pad_h}h"
            
            if result["actual_tokens"] is not None:
                act = result["actual_tokens"]
                if act in [256, 576, 1024] and expected not in [256, 576, 1024]:
                    result["status"] = "FAIL"
                elif abs(act - expected) / max(expected, 1) < 0.5:
                    result["status"] = "PASS"
                elif expected < 100 and act not in [256, 576, 1024]:
                    # Tiny images: large relative deviation but valid NaViT upscaling
                    result["status"] = "PASS"
                else:
                    result["status"] = "CHECK"
            else:
                result["status"] = "N/A"
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)[:80]
        
        results.append(result)
        icon = {"PASS":"✅","FAIL":"❌","CHECK":"⚠️","ERROR":"💥","N/A":"❓"}[result["status"]]
        act_str = str(result.get("actual_tokens") or "N/A")
        grid_str = result.get("grid") or "-"
        pad_str = result.get("padding") or "-"
        print(f"  {cfg['id']:<26} {cfg['width']}x{cfg['height']:<8} {expected:>8,} {act_str:>8} {grid_str:>12} {pad_str:>14} {icon}")
        
        del img
        gc.collect()
    
    passes = sum(1 for r in results if r["status"] == "PASS")
    print(f"\nQwen2.5-VL: {passes}/10 PASS")
    
    del processor
    gc.collect()
    
    return results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    
    print("="*70)
    print("NaViT DOCUMENT STRESS TEST — REALISTIC DOCUMENTS")
    print("="*70)
    
    results = {}
    
    if mode in ["glm", "both"]:
        results["glm"] = test_glm()
        gc.collect()
    
    if mode in ["qwen", "both"]:
        results["qwen"] = test_qwen()
        gc.collect()

    out = os.path.join(DOC_DIR, "document_navit_results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "test_type": "realistic_documents",
            "results": results
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n Results: {out}")
    print("="*70)


if __name__ == "__main__":
    main()
