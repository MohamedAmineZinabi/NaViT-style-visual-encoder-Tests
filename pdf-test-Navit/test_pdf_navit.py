"""
NaViT Stress Test on Multi-Page PDF Documents
===============================================
Converts each page of each PDF to an image using PyMuPDF,
then runs NaViT token allocation verification on both
GLM-OCR and Qwen2.5-VL-3B.
"""

import os
import sys
import gc
import json
from datetime import datetime
from PIL import Image
import fitz  # PyMuPDF

PDF_DIR = "stress_test_pdfs"
PATCH_SIZE = 14
DPI = 150  # Render PDFs at 150 DPI for realistic OCR resolution


def pdf_to_images(pdf_path, dpi=DPI):
    """Convert a PDF to a list of PIL Images."""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append({
            "page": page_num + 1,
            "width": pix.width,
            "height": pix.height,
            "image": img,
        })
    doc.close()
    return images


def calc_expected(w, h, p=14):
    return (w // p) * (h // p)


def test_pages_glm(pages, pdf_name):
    """Test GLM-OCR on PDF pages."""
    from transformers import AutoImageProcessor
    
    ip = AutoImageProcessor.from_pretrained("zai-org/GLM-OCR", trust_remote_code=True)
    results = []
    
    for pg in pages:
        img = pg["image"]
        w, h = pg["width"], pg["height"]
        expected = calc_expected(w, h)
        
        result = {
            "page": pg["page"], "width": w, "height": h,
            "expected_tokens": expected,
            "actual_tokens": None, "grid": None,
            "padding": None, "status": "pending"
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
                result["padding"] = f"+{eff_w - w}w,+{eff_h - h}h"
            
            if result["actual_tokens"] is not None:
                act = result["actual_tokens"]
                if act in [256, 576, 1024] and expected not in [256, 576, 1024]:
                    result["status"] = "FAIL"
                elif abs(act - expected) / max(expected, 1) < 0.5:
                    result["status"] = "PASS"
                else:
                    result["status"] = "CHECK"
            else:
                result["status"] = "N/A"
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)[:80]
        
        results.append(result)
        del img
    
    del ip
    gc.collect()
    return results


def test_pages_qwen(pages, pdf_name):
    """Test Qwen2.5-VL on PDF pages."""
    from transformers import AutoProcessor
    
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct", trust_remote_code=True)
    results = []
    
    for pg in pages:
        img = pg["image"]
        w, h = pg["width"], pg["height"]
        expected = calc_expected(w, h)
        
        result = {
            "page": pg["page"], "width": w, "height": h,
            "expected_tokens": expected,
            "actual_tokens": None, "grid": None,
            "padding": None, "status": "pending"
        }
        
        try:
            messages = [{"role": "user", "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": "OCR this page"}
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
                result["padding"] = f"+{eff_w - w}w,+{eff_h - h}h"
            
            if result["actual_tokens"] is not None:
                act = result["actual_tokens"]
                if act in [256, 576, 1024] and expected not in [256, 576, 1024]:
                    result["status"] = "FAIL"
                elif abs(act - expected) / max(expected, 1) < 0.5:
                    result["status"] = "PASS"
                else:
                    result["status"] = "CHECK"
            else:
                result["status"] = "N/A"
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)[:80]
        
        results.append(result)
        del img
    
    del processor
    gc.collect()
    return results


def print_results(model_name, pdf_name, results):
    """Pretty-print results for a model."""
    passes = sum(1 for r in results if r["status"] == "PASS")
    checks = sum(1 for r in results if r["status"] == "CHECK")
    fails = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)
    
    icons = {"PASS":"✅","FAIL":"❌","CHECK":"⚠️","ERROR":"💥","N/A":"❓"}
    
    print(f"\n  {'Page':>4}  {'Dims':<14} {'Expected':>8} {'Actual':>8} {'Grid':>12} {'Pad':>14} {'St'}")
    print(f"  {'─'*4}  {'─'*14} {'─'*8} {'─'*8} {'─'*12} {'─'*14} {'─'*4}")
    
    for r in results:
        act = str(r.get("actual_tokens") or "N/A")
        grid = r.get("grid") or "-"
        pad = r.get("padding") or "-"
        icon = icons[r["status"]]
        print(f"  {r['page']:>4}  {r['width']}x{r['height']:<10} {r['expected_tokens']:>8,} {act:>8} {grid:>12} {pad:>14} {icon}")
    
    print(f"\n  Result: {passes} PASS / {checks} CHECK / {fails} FAIL / {total} total")
    return passes, total


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "both"
    # Optional: limit pages per PDF for speed
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print("="*70)
    print(f"NaViT MULTI-PAGE PDF STRESS TEST")
    print(f"Model: {model} | Max pages sampled per PDF: {max_pages}")
    print("="*70)
    
    # Find all PDFs
    pdfs = sorted([f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')])
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "multi_page_pdf",
        "dpi": DPI,
        "max_pages_per_pdf": max_pages,
        "pdfs": {}
    }
    
    total_pass = {"glm": 0, "qwen": 0}
    total_tested = {"glm": 0, "qwen": 0}
    
    for pdf_file in pdfs:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]
        
        print(f"\n{'='*70}")
        print(f"PDF: {pdf_file}")
        print(f"{'='*70}")
        
        # Convert pages to images
        print(f"  Converting PDF to images at {DPI} DPI...")
        all_pages = pdf_to_images(pdf_path, DPI)
        total_pages = len(all_pages)
        print(f"  ✓ {total_pages} pages extracted")
        
        # Sample pages: first, last, and evenly spaced
        if total_pages <= max_pages:
            sampled = all_pages
        else:
            indices = set([0, total_pages - 1])
            step = total_pages / (max_pages - 2) if max_pages > 2 else total_pages
            for i in range(max_pages - 2):
                indices.add(min(int(i * step), total_pages - 1))
            sampled = [all_pages[i] for i in sorted(indices)]
        
        print(f"  Testing {len(sampled)} of {total_pages} pages")
        
        # Report page dimensions found
        dims = set(f"{p['width']}x{p['height']}" for p in sampled)
        print(f"  Page dimensions: {', '.join(sorted(dims))}")
        
        pdf_result = {
            "total_pages": total_pages,
            "sampled_pages": len(sampled),
            "page_dimensions": list(dims),
        }
        
        if model in ["glm", "both"]:
            print(f"\n  ── GLM-OCR ──")
            glm_res = test_pages_glm(sampled, pdf_name)
            p, t = print_results("GLM-OCR", pdf_name, glm_res)
            total_pass["glm"] += p
            total_tested["glm"] += t
            pdf_result["glm"] = glm_res
            gc.collect()
        
        if model in ["qwen", "both"]:
            print(f"\n  ── Qwen2.5-VL ──")
            qwen_res = test_pages_qwen(sampled, pdf_name)
            p, t = print_results("Qwen2.5-VL", pdf_name, qwen_res)
            total_pass["qwen"] += p
            total_tested["qwen"] += t
            pdf_result["qwen"] = qwen_res
            gc.collect()
        
        all_results["pdfs"][pdf_name] = pdf_result
        
        # Free page images
        for pg in all_pages:
            del pg["image"]
        del all_pages
        gc.collect()
    
    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY — MULTI-PAGE PDF NaViT TEST")
    print("="*70)
    
    if model in ["glm", "both"]:
        print(f"\n  GLM-OCR:    {total_pass['glm']}/{total_tested['glm']} PASS across {len(pdfs)} PDFs")
    if model in ["qwen", "both"]:
        print(f"  Qwen2.5-VL: {total_pass['qwen']}/{total_tested['qwen']} PASS across {len(pdfs)} PDFs")
    
    print(f"\n{'='*70}")
    
    # Save results
    # Remove image objects before saving
    for pdf_name, pdf_data in all_results["pdfs"].items():
        for model_key in ["glm", "qwen"]:
            if model_key in pdf_data:
                for r in pdf_data[model_key]:
                    r.pop("image", None)
    
    out = os.path.join(PDF_DIR, "pdf_navit_results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📁 Results: {out}")


if __name__ == "__main__":
    main()
