import os
from PIL import Image, ImageDraw, ImageFont
import random
import math

OUTPUT_DIR = "stress_test_documents"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except:
            continue
    return ImageFont.load_default()

def get_bold_font(size):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/timesbd.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except:
            continue
    return get_font(size)

def get_mono_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except:
        return get_font(size)

def generate_long_receipt(width, height, output_path):
    """01: Long receipt (100x2800) - extreme vertical"""
    img = Image.new('RGB', (width, height), '#FFFEF5')
    draw = ImageDraw.Draw(img)
    
    title_font = get_bold_font(max(8, width // 8))
    body_font = get_font(max(6, width // 12))
    small_font = get_font(max(5, width // 14))
    
    y = 10
    # Store header
    draw.text((width//2, y), "SUPERMARCHÉ", font=title_font, fill='black', anchor='mt')
    y += title_font.size + 5
    draw.text((width//2, y), "CENTRAL MARKET", font=body_font, fill='#333', anchor='mt')
    y += body_font.size + 3
    draw.text((width//2, y), "123 Avenue Mohammed V", font=small_font, fill='#666', anchor='mt')
    y += small_font.size + 2
    draw.text((width//2, y), "Casablanca, Morocco", font=small_font, fill='#666', anchor='mt')
    y += small_font.size + 2
    draw.text((width//2, y), "Tel: +212 522 123 456", font=small_font, fill='#666', anchor='mt')
    y += small_font.size + 8
    
    # Dashed line
    for x in range(5, width-5, 4):
        draw.line([(x, y), (x+2, y)], fill='#999', width=1)
    y += 8
    
    draw.text((5, y), "Date: 2026-02-06 14:32", font=small_font, fill='black')
    y += small_font.size + 2
    draw.text((5, y), "Ticket: #A-4829173", font=small_font, fill='black')
    y += small_font.size + 2
    draw.text((5, y), "Cashier: Mohammed", font=small_font, fill='black')
    y += small_font.size + 8
    
    for x in range(5, width-5, 4):
        draw.line([(x, y), (x+2, y)], fill='#999', width=1)
    y += 8
    
    # Items
    items = [
        ("Pain complet", "8.50"), ("Lait demi-ecreme 1L", "7.90"),
        ("Oeufs x12", "15.00"), ("Huile d'olive 1L", "45.00"),
        ("Tomates 1kg", "12.00"), ("Oignons 500g", "5.50"),
        ("Poulet entier", "55.00"), ("Riz 1kg", "14.00"),
        ("Sucre 1kg", "8.50"), ("The vert 250g", "22.00"),
        ("Beurre 250g", "18.00"), ("Fromage frais", "12.50"),
        ("Yaourt x4", "16.00"), ("Eau minerale 1.5L", "5.00"),
        ("Jus d'orange 1L", "15.00"), ("Bananes 1kg", "14.00"),
        ("Pommes 1kg", "18.00"), ("Carottes 500g", "6.00"),
        ("Courgettes 500g", "8.00"), ("Pommes de terre 2kg", "12.00"),
        ("Cafe moulu 250g", "35.00"), ("Chocolat noir", "20.00"),
        ("Biscuits 400g", "18.50"), ("Miel 500g", "45.00"),
        ("Sardines x3", "24.00"), ("Thon conserve", "15.50"),
        ("Pates 500g", "7.00"), ("Sauce tomate", "9.00"),
        ("Sel fin 1kg", "3.50"), ("Poivre noir", "12.00"),
        ("Citrons 500g", "8.00"), ("Menthe fraiche", "3.00"),
        ("Persil botte", "2.50"), ("Coriandre botte", "2.50"),
        ("Olives noires 200g", "15.00"), ("Harissa tube", "8.50"),
        ("Cumin moulu", "6.00"), ("Paprika doux", "5.50"),
        ("Farine 1kg", "6.00"), ("Levure x6", "4.00"),
        ("Semoule fine 1kg", "9.00"), ("Couscous 500g", "7.50"),
        ("Lentilles 500g", "8.00"), ("Pois chiches 400g", "7.00"),
        ("Mouchoirs x10", "12.00"), ("Savon liquide", "22.00"),
        ("Dentifrice", "18.00"), ("Shampooing 400ml", "28.00"),
        ("Lessive 2kg", "45.00"), ("Sacs poubelle x20", "8.00"),
    ]
    
    max_items = min(len(items), (height - y - 200) // (small_font.size + 3))
    
    for i in range(int(max_items)):
        name, price = items[i % len(items)]
        # Truncate name if too long
        max_name_len = (width - 50) // (small_font.size // 2)
        if len(name) > max_name_len:
            name = name[:max_name_len-1] + "."
        draw.text((5, y), name, font=small_font, fill='black')
        draw.text((width - 5, y), price, font=small_font, fill='black', anchor='rt')
        y += small_font.size + 3
    
    y += 5
    for x in range(5, width-5, 4):
        draw.line([(x, y), (x+2, y)], fill='#999', width=1)
    y += 8
    
    # Totals
    total = sum(float(p) for _, p in items[:int(max_items)])
    draw.text((5, y), "SOUS-TOTAL:", font=body_font, fill='black')
    draw.text((width-5, y), f"{total:.2f}", font=body_font, fill='black', anchor='rt')
    y += body_font.size + 3
    tva = total * 0.20
    draw.text((5, y), "TVA (20%):", font=body_font, fill='black')
    draw.text((width-5, y), f"{tva:.2f}", font=body_font, fill='black', anchor='rt')
    y += body_font.size + 5
    
    for x in range(5, width-5, 2):
        draw.line([(x, y), (x+1, y)], fill='black', width=1)
    y += 5
    
    draw.text((5, y), "TOTAL TTC:", font=title_font, fill='black')
    draw.text((width-5, y), f"{total+tva:.2f} MAD", font=title_font, fill='black', anchor='rt')
    y += title_font.size + 10
    
    draw.text((5, y), "Paiement: Carte", font=small_font, fill='#333')
    y += small_font.size + 3
    draw.text((5, y), "**** **** **** 7842", font=small_font, fill='#333')
    y += small_font.size + 15
    
    draw.text((width//2, y), "Merci de votre visite!", font=body_font, fill='#333', anchor='mt')
    y += body_font.size + 3
    draw.text((width//2, y), "A bientot!", font=small_font, fill='#666', anchor='mt')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_wide_spreadsheet(width, height, output_path):
    """02: Wide spreadsheet (2800x100) - extreme horizontal"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    font = get_font(max(6, height // 8))
    header_font = get_bold_font(max(6, height // 7))
    
    # Header row
    col_width = width // 20
    headers = ["ID", "Nom", "Prenom", "Email", "Telephone", 
               "Ville", "Pays", "Date Naissance", "Poste", "Dept",
               "Salaire", "Debut", "Status", "Manager", "Bureau",
               "Etage", "Badge", "Parking", "Telephone2", "Notes"]
    
    # Header background
    draw.rectangle([(0, 0), (width, height//3)], fill='#2C3E50')
    
    for i, h in enumerate(headers):
        x = i * col_width + 3
        draw.text((x, 3), h, font=header_font, fill='white')
    
    # Grid lines
    for i in range(21):
        x = i * col_width
        draw.line([(x, 0), (x, height)], fill='#BDC3C7', width=1)
    
    # Data rows
    row_data = [
        ["001", "Benali", "Ahmed", "a.benali@mail", "+212 6123", 
         "Casa", "MA", "1990-05-12", "Dev Sr", "IT",
         "18000", "2020-01", "Actif", "M.Idrissi", "B2-304",
         "3", "A-1823", "P-42", "+212 5221", "Lead"],
        ["002", "El Fassi", "Sara", "s.elfassi@m", "+212 6456",
         "Rabat", "MA", "1992-11-03", "PM", "Prod",
         "22000", "2019-06", "Actif", "K.Alami", "B1-102",
         "1", "A-2941", "P-18", "+212 5372", "Senior"],
    ]
    
    row_h = (height - height//3) // 2
    for r, data in enumerate(row_data):
        y = height//3 + r * row_h + 2
        bg = '#ECF0F1' if r % 2 == 0 else 'white'
        draw.rectangle([(0, y-2), (width, y + row_h - 2)], fill=bg)
        for i, val in enumerate(data):
            x = i * col_width + 3
            draw.text((x, y), val, font=font, fill='#2C3E50')
    
    # Horizontal grid lines
    draw.line([(0, height//3), (width, height//3)], fill='#BDC3C7', width=1)
    for r in range(3):
        y = height//3 + r * row_h
        draw.line([(0, y), (width, y)], fill='#BDC3C7', width=1)
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_a4_research_paper(width, height, output_path):
    """03: A4 research paper (595x842)"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    title_font = get_bold_font(16)
    author_font = get_font(10)
    section_font = get_bold_font(12)
    body_font = get_font(9)
    small_font = get_font(7)
    
    margin = 40
    y = margin
    
    # Title
    title = "NaViT-Style Dynamic Token Allocation"
    draw.text((width//2, y), title, font=title_font, fill='black', anchor='mt')
    y += 22
    title2 = "in Vision-Language Models for OCR"
    draw.text((width//2, y), title2, font=title_font, fill='black', anchor='mt')
    y += 30
    
    # Authors
    draw.text((width//2, y), "A. Researcher, B. Scientist, C. Engineer", font=author_font, fill='#333', anchor='mt')
    y += 14
    draw.text((width//2, y), "Department of Computer Science", font=small_font, fill='#666', anchor='mt')
    y += 10
    draw.text((width//2, y), "University of Advanced Technology", font=small_font, fill='#666', anchor='mt')
    y += 20
    
    # Horizontal rule
    draw.line([(margin, y), (width - margin, y)], fill='#CCC', width=1)
    y += 10
    
    # Abstract
    draw.text((margin, y), "Abstract", font=section_font, fill='black')
    y += 18
    abstract = [
        "Traditional Vision Transformers resize all images to a fixed",
        "resolution before processing, causing information loss for",
        "documents with extreme aspect ratios. This paper evaluates",
        "three state-of-the-art VLMs to verify NaViT-style native",
        "aspect ratio processing. Our experiments demonstrate that",
        "GLM-OCR, Qwen2.5-VL, and PaddleOCR-VL all preserve",
        "native resolutions, with GLM-OCR achieving SOTA accuracy",
        "of 94.62 on OmniDocBench V1.5.",
    ]
    for line in abstract:
        draw.text((margin, y), line, font=body_font, fill='#333')
        y += 12
    y += 10
    
    draw.line([(margin, y), (width - margin, y)], fill='#CCC', width=1)
    y += 15
    
    # Two-column layout
    col_w = (width - 2*margin - 15) // 2
    
    # Left column
    lx = margin
    ly = y
    
    draw.text((lx, ly), "1. Introduction", font=section_font, fill='black')
    ly += 18
    intro_lines = [
        "Document understanding has become",
        "a critical task in modern AI systems.",
        "Vision-Language Models (VLMs) have",
        "emerged as powerful tools for OCR,",
        "but their handling of varying image",
        "dimensions remains a key concern.",
        "",
        "The NaViT architecture proposes a",
        "solution by processing images at",
        "their native resolution, allocating",
        "visual tokens dynamically based on",
        "actual image dimensions rather than",
        "forcing a fixed-size resize.",
        "",
        "In this study, we evaluate three",
        "models: GLM-OCR (0.9B), Qwen2.5-VL",
        "(3B), and PaddleOCR-VL (0.9B).",
    ]
    for line in intro_lines:
        draw.text((lx, ly), line, font=body_font, fill='#333')
        ly += 11
    
    ly += 8
    draw.text((lx, ly), "2. Methodology", font=section_font, fill='black')
    ly += 18
    method_lines = [
        "We designed a stress test dataset",
        "of 10 images covering aspect ratios",
        "from 1:50 to 28:1. Each image is",
        "processed through each model's",
        "vision encoder, and we extract the",
        "number of visual tokens allocated.",
        "",
        "The pass/fail criterion is:",
        "  N ≈ (W/14) × (H/14)",
        "If the model produces a fixed count",
        "(256, 576, 1024), it indicates a",
        "forced resize has occurred.",
    ]
    for line in method_lines:
        draw.text((lx, ly), line, font=body_font, fill='#333')
        ly += 11
    
    # Right column
    rx = margin + col_w + 15
    ry = y
    
    draw.text((rx, ry), "3. Results", font=section_font, fill='black')
    ry += 18
    
    results_lines = [
        "All three models successfully",
        "passed the NaViT verification test.",
        "",
        "GLM-OCR:   10/10 PASS",
        "Qwen2.5-VL: 10/10 PASS",
        "PaddleOCR:  10/10 PASS",
        "",
        "Key findings include:",
        "- GLM-OCR achieves exact token",
        "  count match across all tests",
        "- Qwen2.5-VL adds minimal padding",
        "  (≤12px) for patch alignment",
        "- PaddleOCR-VL uses a documented",
        "  NaViT-style dynamic encoder",
    ]
    for line in results_lines:
        draw.text((rx, ry), line, font=body_font, fill='#333')
        ry += 11
    
    ry += 8
    draw.text((rx, ry), "4. Conclusion", font=section_font, fill='black')
    ry += 18
    conclusion_lines = [
        "Our evaluation confirms that all",
        "three models implement NaViT-style",
        "native resolution processing.",
        "GLM-OCR is recommended for CPU",
        "deployment due to its combination",
        "of SOTA accuracy (94.62), compact",
        "size (0.9B), and standard PyTorch",
        "ecosystem compatibility.",
        "",
        "References",
        "[1] Dehghani et al., NaViT, 2024",
        "[2] GLM-OCR Technical Report, 2026",
        "[3] Qwen2.5-VL Paper, 2025",
    ]
    for line in conclusion_lines:
        draw.text((rx, ry), line, font=body_font, fill='#333')
        ry += 11
    
    # Column separator
    sep_x = margin + col_w + 7
    draw.line([(sep_x, y), (sep_x, max(ly, ry))], fill='#DDD', width=1)
    
    # Page number
    draw.text((width//2, height - 20), "- 1 -", font=small_font, fill='#999', anchor='mt')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_id_card(width, height, output_path):
    """04: ID card / business card (512x512) - square"""
    img = Image.new('RGB', (width, height), '#1A237E')
    draw = ImageDraw.Draw(img)
    
    # Header band
    draw.rectangle([(0, 0), (width, height//5)], fill='#0D47A1')
    draw.rectangle([(0, height//5), (width, height//5+3)], fill='#FFC107')
    
    title_font = get_bold_font(20)
    name_font = get_bold_font(18)
    body_font = get_font(12)
    small_font = get_font(10)
    
    y = 15
    draw.text((width//2, y), "CARTE NATIONALE", font=title_font, fill='white', anchor='mt')
    y += 25
    draw.text((width//2, y), "D'IDENTITÉ", font=title_font, fill='#FFC107', anchor='mt')
    y = height//5 + 20
    
    # Photo placeholder
    photo_size = height // 3
    px = 25
    py = y
    draw.rectangle([(px, py), (px + photo_size, py + photo_size)], fill='#E8EAF6', outline='#5C6BC0', width=2)
    draw.text((px + photo_size//2, py + photo_size//2), "PHOTO", font=body_font, fill='#7986CB', anchor='mm')
    
    # Info
    ix = px + photo_size + 20
    iy = y
    
    fields = [
        ("Nom:", "BENALI"),
        ("Prénom:", "Ahmed"),
        ("Né(e) le:", "12/05/1990"),
        ("Lieu:", "Casablanca"),
        ("CIN:", "BK 482917"),
        ("Validité:", "12/2030"),
    ]
    
    for label, value in fields:
        draw.text((ix, iy), label, font=small_font, fill='#90CAF9')
        iy += 13
        draw.text((ix, iy), value, font=body_font, fill='white')
        iy += 18
    
    # Bottom band with machine-readable zone
    mrz_y = height - 60
    draw.rectangle([(0, mrz_y), (width, height)], fill='#0D47A1')
    mrz_font = get_mono_font(8)
    draw.text((10, mrz_y + 5), "IDMAR<<BENALI<<AHMED<<<<<<<<<<<<<<<<<<<", font=mrz_font, fill='#90CAF9')
    draw.text((10, mrz_y + 18), "BK482917<3MAR9005124M3012305<<<<<<<<<08", font=mrz_font, fill='#90CAF9')
    draw.text((10, mrz_y + 31), "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", font=mrz_font, fill='#90CAF9')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_narrow_invoice(width, height, output_path):
    """05: Narrow invoice (140x2100) - skyscraper"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    title_font = get_bold_font(max(7, width // 14))
    body_font = get_font(max(5, width // 18))
    small_font = get_font(max(4, width // 22))
    
    y = 5
    
    # Company
    draw.rectangle([(0, 0), (width, 40)], fill='#E53935')
    draw.text((width//2, 5), "FACTURE", font=title_font, fill='white', anchor='mt')
    draw.text((width//2, 20), "N° F-2026-0482", font=small_font, fill='#FFCDD2', anchor='mt')
    y = 48
    
    draw.text((3, y), "De:", font=small_font, fill='#999')
    y += small_font.size + 1
    draw.text((3, y), "Tech SARL", font=body_font, fill='black')
    y += body_font.size + 1
    draw.text((3, y), "45 Rue Zerktouni", font=small_font, fill='#666')
    y += small_font.size + 1
    draw.text((3, y), "20000 Casa", font=small_font, fill='#666')
    y += small_font.size + 6
    
    draw.text((3, y), "A:", font=small_font, fill='#999')
    y += small_font.size + 1
    draw.text((3, y), "Client ABC", font=body_font, fill='black')
    y += body_font.size + 1
    draw.text((3, y), "10 Bd Hassan II", font=small_font, fill='#666')
    y += small_font.size + 5
    
    draw.line([(3, y), (width-3, y)], fill='#E53935', width=1)
    y += 5
    
    # Items
    items = [
        ("Dev Web", "5000"), ("Design UI", "3000"), ("Backend API", "4500"),
        ("Database", "2000"), ("Testing", "1500"), ("Deploy", "1000"),
        ("Formation", "2500"), ("Support 3m", "3600"), ("SSL Cert", "500"),
        ("Domaine", "150"), ("Hosting 1a", "2400"), ("Email Pro", "600"),
        ("Maintenance", "1800"), ("SEO Init", "2000"), ("Analytics", "800"),
        ("Backup Sol", "1200"), ("CDN Setup", "900"), ("API Integ", "1500"),
        ("Mobile App", "8000"), ("Push Notif", "1000"), ("Auth Syst", "2500"),
        ("Dashboard", "3500"), ("Reporting", "2000"), ("Export PDF", "1500"),
    ]
    
    max_items = min(len(items), (height - y - 150) // (small_font.size + 3))
    
    for i in range(int(max_items)):
        name, price = items[i]
        draw.text((3, y), name, font=small_font, fill='black')
        draw.text((width-3, y), price, font=small_font, fill='black', anchor='rt')
        y += small_font.size + 3
    
    y += 3
    draw.line([(3, y), (width-3, y)], fill='#E53935', width=1)
    y += 5
    
    total = sum(int(p) for _, p in items[:int(max_items)])
    draw.text((3, y), "HT:", font=body_font, fill='black')
    draw.text((width-3, y), f"{total}", font=body_font, fill='black', anchor='rt')
    y += body_font.size + 2
    draw.text((3, y), "TVA:", font=body_font, fill='black')
    draw.text((width-3, y), f"{int(total*0.2)}", font=body_font, fill='black', anchor='rt')
    y += body_font.size + 3
    draw.text((3, y), "TTC:", font=title_font, fill='#E53935')
    draw.text((width-3, y), f"{int(total*1.2)}", font=title_font, fill='#E53935', anchor='rt')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_panoramic_timeline(width, height, output_path):
    """06: Panoramic timeline (3500x70) - extreme horizontal"""
    img = Image.new('RGB', (width, height), '#FAFAFA')
    draw = ImageDraw.Draw(img)
    
    font = get_font(max(6, height // 6))
    bold_font = get_bold_font(max(7, height // 5))
    
    # Title
    draw.rectangle([(0, 0), (80, height)], fill='#1565C0')
    draw.text((40, height//2), "TIMELINE", font=font, fill='white', anchor='mm')
    
    # Timeline bar
    bar_y = height // 2
    draw.line([(100, bar_y), (width - 20, bar_y)], fill='#1565C0', width=2)
    
    events = [
        ("Jan 2025", "Project Start"), ("Mar 2025", "Phase 1 Done"),
        ("Jun 2025", "Beta Release"), ("Aug 2025", "User Testing"),
        ("Oct 2025", "v1.0 Launch"), ("Dec 2025", "10K Users"),
        ("Feb 2026", "v2.0 Plan"), ("Apr 2026", "AI Integration"),
        ("Jun 2026", "Global Launch"), ("Aug 2026", "100K Users"),
        ("Oct 2026", "Enterprise"), ("Dec 2026", "IPO Prep"),
    ]
    
    spacing = (width - 140) // len(events)
    
    for i, (date, event) in enumerate(events):
        x = 120 + i * spacing
        # Dot
        draw.ellipse([(x-4, bar_y-4), (x+4, bar_y+4)], fill='#1565C0')
        # Alternate above/below
        if i % 2 == 0:
            draw.line([(x, bar_y-4), (x, bar_y-15)], fill='#90CAF9', width=1)
            draw.text((x, bar_y-18), date, font=font, fill='#1565C0', anchor='mb')
            draw.text((x, bar_y+10), event, font=font, fill='#333', anchor='mt')
        else:
            draw.line([(x, bar_y+4), (x, bar_y+15)], fill='#90CAF9', width=1)
            draw.text((x, bar_y+18), date, font=font, fill='#1565C0', anchor='mt')
            draw.text((x, bar_y-10), event, font=font, fill='#333', anchor='mb')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_mobile_form(width, height, output_path):
    """07: Mobile form (375x812) - phone screenshot"""
    img = Image.new('RGB', (width, height), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    title_font = get_bold_font(16)
    label_font = get_font(11)
    input_font = get_font(12)
    small_font = get_font(9)
    
    # Status bar
    draw.rectangle([(0, 0), (width, 44)], fill='#1976D2')
    draw.text((width//2, 14), "9:41", font=label_font, fill='white', anchor='mt')
    draw.text((width-15, 14), "100%", font=small_font, fill='white', anchor='rt')
    
    # Navigation bar
    draw.rectangle([(0, 44), (width, 88)], fill='#1565C0')
    draw.text((20, 58), "< Retour", font=label_font, fill='white')
    draw.text((width//2, 56), "Inscription", font=title_font, fill='white', anchor='mt')
    
    y = 110
    margin = 20
    
    fields = [
        ("Nom complet", "Ahmed Benali"),
        ("Email", "ahmed.benali@email.com"),
        ("Téléphone", "+212 612 345 678"),
        ("Date de naissance", "12/05/1990"),
        ("Ville", "Casablanca"),
        ("Code postal", "20000"),
        ("Adresse", "45 Rue Mohammed V, Apt 12"),
        ("Mot de passe", "••••••••••••"),
        ("Confirmer", "••••••••••••"),
    ]
    
    for label, value in fields:
        draw.text((margin, y), label, font=label_font, fill='#666')
        y += 18
        # Input field
        draw.rectangle([(margin, y), (width - margin, y + 36)], fill='white', outline='#DDD', width=1)
        draw.rounded_rectangle([(margin, y), (width - margin, y + 36)], radius=5, fill='white', outline='#BDBDBD', width=1)
        draw.text((margin + 10, y + 10), value, font=input_font, fill='#333')
        y += 50
    
    # Checkbox
    y += 5
    draw.rectangle([(margin, y), (margin + 16, y + 16)], outline='#1976D2', width=2)
    draw.text((margin + 1, y - 1), "✓", font=label_font, fill='#1976D2')
    draw.text((margin + 24, y), "J'accepte les conditions générales", font=small_font, fill='#666')
    y += 30
    
    # Submit button
    draw.rounded_rectangle([(margin, y), (width - margin, y + 44)], radius=8, fill='#1976D2')
    draw.text((width//2, y + 14), "S'inscrire", font=title_font, fill='white', anchor='mt')
    y += 60
    
    draw.text((width//2, y), "Déjà inscrit ? Se connecter", font=small_font, fill='#1976D2', anchor='mt')
    
    # Home indicator
    draw.rounded_rectangle([(width//2 - 40, height - 8), (width//2 + 40, height - 4)], radius=2, fill='#CCC')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_financial_report(width, height, output_path):
    """08: Financial report (3840x2160) - 4K"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    title_font = get_bold_font(48)
    h2_font = get_bold_font(32)
    h3_font = get_bold_font(24)
    body_font = get_font(20)
    small_font = get_font(16)
    table_font = get_font(18)
    
    margin = 120
    y = margin
    
    # Company header
    draw.rectangle([(0, 0), (width, 120)], fill='#0D47A1')
    draw.text((margin, 35), "GROUPE BENALI HOLDINGS", font=title_font, fill='white')
    draw.text((width - margin, 45), "Rapport Financier Annuel 2025", font=h3_font, fill='#90CAF9', anchor='rt')
    
    y = 160
    draw.text((margin, y), "Rapport Annuel Consolidé - Exercice 2025", font=h2_font, fill='#0D47A1')
    y += 50
    
    # Executive summary
    draw.text((margin, y), "1. Résumé Exécutif", font=h3_font, fill='#1565C0')
    y += 35
    
    summary = [
        "L'exercice 2025 a été marqué par une croissance significative de notre chiffre d'affaires consolidé,",
        "atteignant 2.4 milliards MAD, soit une progression de 18.5% par rapport à l'exercice précédent.",
        "Cette performance est le résultat de notre stratégie de diversification et d'innovation technologique.",
        "Le résultat net consolidé s'établit à 340 millions MAD, en hausse de 22% par rapport à 2024.",
    ]
    for line in summary:
        draw.text((margin, y), line, font=body_font, fill='#333')
        y += 28
    y += 20
    
    # Financial Table
    draw.text((margin, y), "2. Données Financières Clés", font=h3_font, fill='#1565C0')
    y += 40
    
    # Table
    table_x = margin
    col_widths = [600, 400, 400, 400, 400]
    headers = ["Indicateur", "2025", "2024", "Variation", "Objectif 2026"]
    
    # Header row
    draw.rectangle([(table_x, y), (table_x + sum(col_widths), y + 40)], fill='#0D47A1')
    cx = table_x
    for i, (h, w) in enumerate(zip(headers, col_widths)):
        draw.text((cx + 10, y + 10), h, font=table_font, fill='white')
        cx += w
    y += 40
    
    rows = [
        ["Chiffre d'affaires (M MAD)", "2,400", "2,025", "+18.5%", "2,800"],
        ["Résultat d'exploitation", "480", "395", "+21.5%", "560"],
        ["Résultat net", "340", "279", "+22.0%", "400"],
        ["Marge nette", "14.2%", "13.8%", "+0.4 pts", "14.3%"],
        ["Effectif total", "4,850", "4,200", "+650", "5,500"],
        ["Investissements", "520", "380", "+36.8%", "600"],
        ["Dette nette / EBITDA", "1.8x", "2.1x", "-0.3x", "1.5x"],
        ["Dividende par action", "45 MAD", "38 MAD", "+18.4%", "52 MAD"],
    ]
    
    for r, row in enumerate(rows):
        bg = '#F5F5F5' if r % 2 == 0 else 'white'
        draw.rectangle([(table_x, y), (table_x + sum(col_widths), y + 35)], fill=bg)
        cx = table_x
        for i, (val, w) in enumerate(zip(row, col_widths)):
            color = '#2E7D32' if '+' in val else '#C62828' if '-' in val and i == 3 else '#333'
            draw.text((cx + 10, y + 8), val, font=table_font, fill=color)
            cx += w
        draw.line([(table_x, y+35), (table_x + sum(col_widths), y+35)], fill='#E0E0E0', width=1)
        y += 35
    
    y += 40
    
    # Revenue by segment - simple bar chart simulation
    draw.text((margin, y), "3. Répartition du CA par Segment", font=h3_font, fill='#1565C0')
    y += 40
    
    segments = [
        ("Technologie", 850, '#1565C0'),
        ("Immobilier", 620, '#2E7D32'),
        ("Finance", 480, '#E65100'),
        ("Industrie", 320, '#6A1B9A'),
        ("Services", 130, '#00838F'),
    ]
    
    bar_max_w = 800
    max_val = max(s[1] for s in segments)
    
    for name, value, color in segments:
        draw.text((margin, y + 5), f"{name}", font=table_font, fill='#333')
        bar_x = margin + 250
        bar_w = int((value / max_val) * bar_max_w)
        draw.rectangle([(bar_x, y), (bar_x + bar_w, y + 28)], fill=color)
        draw.text((bar_x + bar_w + 10, y + 4), f"{value} M", font=table_font, fill='#333')
        y += 40
    
    y += 30
    
    # Second half - using right side
    rx = width // 2 + 50
    ry = 500
    
    draw.text((rx, ry), "4. Perspectives 2026", font=h3_font, fill='#1565C0')
    ry += 40
    
    perspectives = [
        "• Objectif CA: 2.8 milliards MAD (+16.7%)",
        "• Lancement de la plateforme AI propriétaire",
        "• Expansion sur 3 nouveaux marchés africains",
        "• Recrutement de 650 collaborateurs",
        "• Investissement R&D: 180 M MAD",
        "• Certification ISO 27001",
        "• Introduction en bourse prévue T4 2026",
    ]
    for p in perspectives:
        draw.text((rx, ry), p, font=body_font, fill='#333')
        ry += 30
    
    ry += 30
    draw.text((rx, ry), "5. Gouvernance", font=h3_font, fill='#1565C0')
    ry += 40
    
    board = [
        ("Président", "M. Karim Benali"),
        ("DG", "Mme Sara El Fassi"),
        ("DAF", "M. Youssef Idrissi"),
        ("CTO", "M. Omar Alami"),
        ("DRH", "Mme Fatima Zahra Bennani"),
    ]
    for title, name in board:
        draw.text((rx, ry), f"{title}:", font=table_font, fill='#666')
        draw.text((rx + 200, ry), name, font=table_font, fill='#333')
        ry += 30
    
    # Footer
    draw.rectangle([(0, height - 50), (width, height)], fill='#0D47A1')
    draw.text((margin, height - 38), "© 2026 Groupe Benali Holdings - Document Confidentiel", font=small_font, fill='white')
    draw.text((width - margin, height - 38), "Page 1/12", font=small_font, fill='#90CAF9', anchor='rt')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_medical_prescription(width, height, output_path):
    """09: Medical prescription (987x610) - golden ratio"""
    img = Image.new('RGB', (width, height), '#FFFDE7')
    draw = ImageDraw.Draw(img)
    
    title_font = get_bold_font(18)
    h2_font = get_bold_font(14)
    body_font = get_font(12)
    small_font = get_font(10)
    rx_font = get_bold_font(40)
    
    margin = 30
    
    # Header
    draw.rectangle([(0, 0), (width, 80)], fill='white', outline='#4CAF50', width=2)
    draw.text((margin, 10), "Dr. Fatima ZAHRA ELKHATTABI", font=title_font, fill='#1B5E20')
    draw.text((margin, 32), "Médecine Générale & Médecine Interne", font=body_font, fill='#333')
    draw.text((margin, 48), "N° Ordre: 12847 | INPE: 5429810", font=small_font, fill='#666')
    
    draw.text((width - margin, 10), "Cabinet Médical Al Amal", font=body_font, fill='#333', anchor='rt')
    draw.text((width - margin, 28), "78 Rue Ibn Sina, Hay Riad", font=small_font, fill='#666', anchor='rt')
    draw.text((width - margin, 42), "Rabat 10100 - Maroc", font=small_font, fill='#666', anchor='rt')
    draw.text((width - margin, 58), "Tél: +212 537 712 345", font=small_font, fill='#666', anchor='rt')
    
    y = 95
    
    # Rx symbol
    draw.text((margin, y), "℞", font=rx_font, fill='#4CAF50')
    
    # Patient info
    px = margin + 60
    draw.text((px, y), "Patient: Ahmed BENALI", font=h2_font, fill='black')
    draw.text((px, y + 20), "Âge: 35 ans | Sexe: M", font=body_font, fill='#333')
    draw.text((width - margin, y), f"Date: 06/02/2026", font=body_font, fill='#333', anchor='rt')
    draw.text((width - margin, y + 18), "N° Dossier: P-2026-0847", font=small_font, fill='#666', anchor='rt')
    
    y += 55
    draw.line([(margin, y), (width - margin, y)], fill='#A5D6A7', width=1)
    y += 15
    
    # Prescriptions
    draw.text((margin, y), "ORDONNANCE MÉDICALE", font=h2_font, fill='#1B5E20')
    y += 25
    
    prescriptions = [
        ("1.", "AMOXICILLINE 1g", "1 comprimé matin et soir pendant 7 jours", "Prendre pendant les repas"),
        ("2.", "PARACÉTAMOL 1000mg", "1 comprimé toutes les 6 heures si douleur", "Maximum 4 comprimés/jour"),
        ("3.", "OMÉPRAZOLE 20mg", "1 gélule le matin à jeun pendant 14 jours", "30 min avant le petit-déjeuner"),
        ("4.", "VITAMINE D3 100.000 UI", "1 ampoule par mois pendant 3 mois", "À prendre avec un repas gras"),
    ]
    
    for num, med, posology, note in prescriptions:
        draw.text((margin, y), num, font=h2_font, fill='#4CAF50')
        draw.text((margin + 25, y), med, font=h2_font, fill='black')
        y += 20
        draw.text((margin + 25, y), posology, font=body_font, fill='#333')
        y += 16
        draw.text((margin + 25, y), f"⚠ {note}", font=small_font, fill='#E65100')
        y += 22
    
    y += 10
    draw.line([(margin, y), (width - margin, y)], fill='#A5D6A7', width=1)
    y += 15
    
    # Notes
    draw.text((margin, y), "Observations:", font=h2_font, fill='#1B5E20')
    y += 20
    draw.text((margin, y), "Repos de 3 jours recommandé. Contrôle dans 10 jours.", font=body_font, fill='#333')
    y += 16
    draw.text((margin, y), "Bilan sanguin NFS + CRP à faire avant le contrôle.", font=body_font, fill='#333')
    
    # Signature area
    draw.text((width - margin - 200, height - 70), "Signature et cachet:", font=small_font, fill='#999')
    draw.text((width - margin - 150, height - 45), "Dr. F.Z. Elkhattabi", font=body_font, fill='#1B5E20')
    
    # Stamp simulation
    draw.ellipse([(width - margin - 130, height - 80), (width - margin - 50, height - 20)], outline='#4CAF50', width=2)
    draw.text((width - margin - 90, height - 55), "INPE", font=small_font, fill='#4CAF50', anchor='mm')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


def generate_stamp(width, height, output_path):
    """10: Postage stamp (64x64) - tiny"""
    img = Image.new('RGB', (width, height), '#FBE9E7')
    draw = ImageDraw.Draw(img)
    
    # Perforated border
    for x in range(0, width, 5):
        draw.ellipse([(x, 0), (x+3, 3)], fill='white')
        draw.ellipse([(x, height-3), (x+3, height)], fill='white')
    for y_pos in range(0, height, 5):
        draw.ellipse([(0, y_pos), (3, y_pos+3)], fill='white')
        draw.ellipse([(width-3, y_pos), (width, y_pos+3)], fill='white')
    
    font_tiny = get_font(6)
    font_val = get_bold_font(10)
    
    # Country
    draw.text((width//2, 6), "MAROC", font=font_tiny, fill='#B71C1C', anchor='mt')
    
    # Central design 
    cx, cy = width//2, height//2
    draw.ellipse([(cx-12, cy-12), (cx+12, cy+12)], outline='#1B5E20', width=1)
    draw.polygon([(cx, cy-8), (cx+7, cy+5), (cx-7, cy+5)], fill='#1B5E20')
    
    # Value
    draw.text((width//2, height-12), "3.75", font=font_val, fill='#B71C1C', anchor='mb')
    draw.text((width//2, height-5), "MAD", font=font_tiny, fill='#333', anchor='mb')
    
    img.save(output_path)
    print(f"  ✓ {os.path.basename(output_path)} ({width}x{height})")


DOCUMENT_CONFIGS = [
    {"id": "01_long_receipt",        "width": 100,  "height": 2800, "gen": generate_long_receipt,       "desc": "Supermarket receipt (50 items)"},
    {"id": "02_wide_spreadsheet",    "width": 2800, "height": 100,  "gen": generate_wide_spreadsheet,   "desc": "Employee database table"},
    {"id": "03_research_paper_a4",   "width": 595,  "height": 842,  "gen": generate_a4_research_paper,  "desc": "Two-column research paper"},
    {"id": "04_id_card_square",      "width": 512,  "height": 512,  "gen": generate_id_card,            "desc": "National ID card"},
    {"id": "05_narrow_invoice",      "width": 140,  "height": 2100, "gen": generate_narrow_invoice,     "desc": "Narrow service invoice"},
    {"id": "06_panoramic_timeline",  "width": 3500, "height": 70,   "gen": generate_panoramic_timeline, "desc": "Project timeline strip"},
    {"id": "07_mobile_form",         "width": 375,  "height": 812,  "gen": generate_mobile_form,        "desc": "Mobile registration form"},
    {"id": "08_financial_report_4k", "width": 3840, "height": 2160, "gen": generate_financial_report,   "desc": "Annual financial report (4K)"},
    {"id": "09_medical_prescription","width": 987,  "height": 610,  "gen": generate_medical_prescription,"desc": "Medical prescription"},
    {"id": "10_postage_stamp",       "width": 64,   "height": 64,   "gen": generate_stamp,              "desc": "Postage stamp (tiny)"},
]

def main():
    print("="*60)
    print("GENERATING REALISTIC DOCUMENT IMAGES")
    print("="*60 + "\n")
    
    for cfg in DOCUMENT_CONFIGS:
        try:
            path = os.path.join(OUTPUT_DIR, f"{cfg['id']}.png")
            cfg["gen"](cfg["width"], cfg["height"], path)
        except Exception as e:
            print(f"  ✗ {cfg['id']}: {e}")
    
    print(f"\n✅ {len(DOCUMENT_CONFIGS)} documents generated in '{OUTPUT_DIR}/'\n")
    
    print(f"{'#':<4} {'Document':<25} {'Dimensions':<15} {'Aspect':<8} {'Description'}")
    print("-"*80)
    for i, cfg in enumerate(DOCUMENT_CONFIGS, 1):
        w, h = cfg["width"], cfg["height"]
        ratio = max(w,h) / min(w,h)
        orient = "H" if w > h else "V" if h > w else "S"
        print(f"{i:<4} {cfg['id']:<25} {w}x{h:<10} {ratio:.1f}:1 {orient}  {cfg['desc']}")

if __name__ == "__main__":
    main()
