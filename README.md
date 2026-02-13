# NaViT-Style Native Aspect Ratio Verification

A comprehensive evaluation proving that **GLM-OCR** and **Qwen2.5-VL-3B** implement NaViT-style native resolution processing for document OCR.

**Author:** Mohamed Amine Zinabi

---

## Results

| Model | Phase 1 (Documents) | Phase 2 (PDFs) | Total |
|-------|:---:|:---:|:---:|
| **GLM-OCR** | 10/10 ✅ | 28/28 ✅ | **38/38 (100%)** |
| **Qwen2.5-VL-3B** | 10/10 ✅ | 28/28 ✅ | **38/38 (100%)** |

---

## Environment Setup

All tests were run inside a **Python virtual environment** to isolate dependencies and ensure reproducibility.

### Prerequisites

- Python 3.10+
- Intel i5 vPro (or equivalent) with 8GB RAM minimum

### Creating the Virtual Environment

```bash
# Create the virtual environment
python -m venv glm_ocr_env

# Activate it
# Windows (PowerShell)
.\glm_ocr_env\Scripts\Activate.ps1
# Windows (CMD)
glm_ocr_env\Scripts\activate
# Linux/macOS
source glm_ocr_env/bin/activate

# Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install transformers pillow pymupdf
```

### Activating the Environment (for subsequent runs)

```powershell
# PowerShell
& ./glm_ocr_env/Scripts/Activate.ps1

# Verify
python --version
```

---

## Project Structure

```
glm_ocr_test/
├── README.md                        # This file
├── navit_verification_report.tex    # Full LaTeX report
├── Navit-Style Tests Report.pdf     # Compiled PDF report
│
├── generate_documents.py            # Phase 1: Realistic document image generator
├── test_doc_navit.py                # Phase 1: Document NaViT test (GLM + Qwen)
├── stress_test_documents/           # Phase 1: 10 PNG images + results JSON
│
├── generate_pdfs.py                 # Phase 2: Multi-page PDF generator
├── test_pdf_navit.py                # Phase 2: PDF page NaViT test (GLM + Qwen)
├── stress_test_pdfs/                # Phase 2: 7 PDFs (162 pages) + results JSON
│
└── glm_ocr_env/                     # Python virtual environment (not committed)
```

---

## Running the Tests

> **Important:** Always activate the virtual environment before running any test.

### Phase 1 — Realistic Document Images

```bash
# Generate the 10 test document images
python generate_documents.py

# Run NaViT verification (both models sequentially)
python test_doc_navit.py both

# Or run models individually (recommended for 8GB RAM)
python test_doc_navit.py glm
python test_doc_navit.py qwen
```

### Phase 2 — Multi-Page PDF Documents

```bash
# Generate the 7 test PDFs
python generate_pdfs.py

# Run NaViT verification on PDF pages
python test_pdf_navit.py
```

---

## Key Findings

- Both models use **`image_grid_thw`** to dynamically allocate visual tokens based on native image dimensions
- **Zero fixed-resize patterns** detected (no 256/576/1024 token counts)
- Aspect ratios tested: 1:1, 1.4:1, 1.6:1, 2.2:1, 15:1, 28:1, 50:1
- Resolutions tested: 64×64 (tiny) to 3840×2160 (4K)

### Recommendation

For CPU deployment on constrained hardware, **GLM-OCR** is the recommended choice:
- 🏆 SOTA accuracy: 94.62 on OmniDocBench V1.5
- ⚡ Lightweight: 0.9B parameters
- 📄 Apache 2.0 license
- 🔧 PyTorch + Hugging Face ecosystem
