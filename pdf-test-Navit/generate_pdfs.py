"""
Generate Multi-Page PDF Documents for NaViT Stress Testing
===========================================================
Creates PDFs with varying:
  - Number of pages (5 to 50+)
  - Page sizes (A4, A3, Letter, Legal, custom tall/wide)
  - Content types (text, tables, mixed)
  - Mixed page sizes within same PDF
"""

import os
from reportlab.lib.pagesizes import A4, A3, letter, legal, landscape
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import random
import math

OUTPUT_DIR = "stress_test_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# PDF Generators
# ============================================================

def draw_header(c, w, h, title, page_num, total_pages):
    """Draw a consistent header/footer on each page."""
    # Header bar
    c.setFillColor(HexColor('#1565C0'))
    c.rect(0, h - 40, w, 40, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(15, h - 28, title)
    c.setFont("Helvetica", 9)
    c.drawRightString(w - 15, h - 28, f"Page {page_num}/{total_pages}")
    
    # Footer
    c.setFillColor(HexColor('#ECEFF1'))
    c.rect(0, 0, w, 25, fill=1, stroke=0)
    c.setFillColor(HexColor('#78909C'))
    c.setFont("Helvetica", 7)
    c.drawString(15, 9, "NaViT Stress Test — Multi-Page PDF")
    c.drawRightString(w - 15, 9, f"Generated 2026-02-12")


def generate_financial_report_pdf(path):
    """PDF 1: 15-page A4 financial report with tables and text."""
    w, h = A4
    total = 15
    c = canvas.Canvas(path, pagesize=A4)
    
    for page in range(1, total + 1):
        draw_header(c, w, h, "RAPPORT FINANCIER ANNUEL 2025", page, total)
        y = h - 70
        
        if page == 1:
            # Cover page
            c.setFillColor(HexColor('#0D47A1'))
            c.rect(50, h//2 - 50, w - 100, 120, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 28)
            c.drawCentredString(w/2, h//2 + 30, "GROUPE BENALI")
            c.setFont("Helvetica", 18)
            c.drawCentredString(w/2, h//2, "Rapport Financier Annuel")
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(w/2, h//2 - 30, "Exercice 2025")
            
            c.setFillColor(HexColor('#333333'))
            c.setFont("Helvetica", 10)
            c.drawCentredString(w/2, 200, "Direction Financière — Casablanca, Maroc")
            c.drawCentredString(w/2, 185, "Date: Février 2026 | Confidentiel")
        
        elif page == 2:
            # Table of contents
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(HexColor('#1565C0'))
            c.drawString(50, y, "Table des Matières")
            y -= 30
            
            toc = [
                "1. Résumé Exécutif", "2. Faits Marquants 2025",
                "3. Compte de Résultat Consolidé", "4. Bilan Consolidé",
                "5. Flux de Trésorerie", "6. Analyse par Segment",
                "7. Indicateurs de Performance", "8. Évolution Trimestrielle",
                "9. Ressources Humaines", "10. Investissements",
                "11. Gestion des Risques", "12. Perspectives 2026",
                "13. Annexes Comptables",
            ]
            c.setFont("Helvetica", 11)
            c.setFillColor(black)
            for i, item in enumerate(toc):
                c.drawString(70, y, item)
                c.drawRightString(w - 70, y, f"......... {i + 3}")
                y -= 22
        
        elif page <= 5:
            # Text pages
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(HexColor('#1565C0'))
            sections = ["Résumé Exécutif", "Faits Marquants", "Performance Globale"]
            c.drawString(50, y, f"{page-2}. {sections[page-3]}")
            y -= 25
            
            c.setFont("Helvetica", 10)
            c.setFillColor(black)
            paragraphs = [
                "L'exercice 2025 a été marqué par une forte croissance de l'ensemble des indicateurs financiers du Groupe.",
                "Le chiffre d'affaires consolidé a atteint 2,4 milliards MAD, en progression de 18,5% par rapport à 2024.",
                "Le résultat net part du groupe s'est établi à 340 millions MAD, soit une hausse de 22% sur un an.",
                "Cette performance reflète la pertinence de notre stratégie de diversification et d'innovation technologique.",
                "Le ratio d'endettement net s'est amélioré à 1,8x l'EBITDA contre 2,1x en 2024.",
                "Les investissements ont augmenté de 36,8% pour atteindre 520 millions MAD dont 180M en R&D.",
                "L'effectif total du Groupe a progressé à 4 850 collaborateurs avec un taux de rétention de 92%.",
                "Le Conseil d'Administration propose un dividende de 45 MAD par action au titre de l'exercice 2025.",
            ]
            for p in paragraphs:
                lines = [p[i:i+85] for i in range(0, len(p), 85)]
                for line in lines:
                    c.drawString(50, y, line)
                    y -= 14
                y -= 8
        
        elif page <= 10:
            # Financial tables
            titles = ["Compte de Résultat", "Bilan Actif", "Bilan Passif", 
                      "Flux de Trésorerie", "Analyse par Segment"]
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(HexColor('#1565C0'))
            c.drawString(50, y, titles[page-6])
            y -= 25
            
            data = [["Indicateur", "2025", "2024", "Var %"]]
            items = [
                ("Chiffre d'affaires", "2 400", "2 025", "+18.5%"),
                ("Coût des ventes", "1 560", "1 357", "+14.9%"),
                ("Marge brute", "840", "668", "+25.7%"),
                ("Charges d'exploitation", "360", "273", "+31.9%"),
                ("Résultat d'exploitation", "480", "395", "+21.5%"),
                ("Résultat financier", "-40", "-45", "-11.1%"),
                ("Résultat avant impôt", "440", "350", "+25.7%"),
                ("Impôt sur les sociétés", "100", "71", "+40.8%"),
                ("Résultat net", "340", "279", "+21.9%"),
                ("Amortissements", "120", "98", "+22.4%"),
                ("EBITDA", "600", "493", "+21.7%"),
                ("Marge EBITDA", "25.0%", "24.3%", "+0.7 pts"),
            ]
            for item in items:
                data.append(list(item))
            
            t = Table(data, colWidths=[200, 100, 100, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1565C0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDBDBD')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F5F5F5')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            tw, th = t.wrapOn(c, w - 100, y)
            t.drawOn(c, 50, y - th)
        
        else:
            # Additional analysis pages
            sections = ["Indicateurs KPI", "Évolution Trimestrielle", 
                       "Ressources Humaines", "Investissements R&D", "Perspectives 2026"]
            idx = (page - 11) % len(sections)
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(HexColor('#1565C0'))
            c.drawString(50, y, sections[idx])
            y -= 25
            
            c.setFont("Helvetica", 10)
            c.setFillColor(black)
            for i in range(15):
                bullet = f"• Point d'analyse {i+1}: résultat de l'indicateur pour la période concernée"
                c.drawString(60, y, bullet)
                y -= 16
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (A4)")


def generate_mixed_sizes_pdf(path):
    """PDF 2: 10-page PDF with mixed page sizes (A4, A3, Letter, Legal)."""
    total = 10
    c = canvas.Canvas(path)
    
    sizes = [
        ("A4 Portrait", A4),
        ("A4 Landscape", landscape(A4)),
        ("A3 Portrait", A3),
        ("Letter", letter),
        ("Legal", legal),
        ("A4 Portrait", A4),
        ("A3 Landscape", landscape(A3)),
        ("Custom Tall", (300, 1200)),
        ("Custom Wide", (1200, 400)),
        ("A4 Portrait", A4),
    ]
    
    for page, (label, size) in enumerate(sizes, 1):
        w, h = size
        c.setPageSize(size)
        
        draw_header(c, w, h, f"MIXED SIZES — {label}", page, total)
        y = h - 80
        
        # Page size info box
        c.setFillColor(HexColor('#E3F2FD'))
        c.roundRect(50, y - 80, w - 100, 80, 10, fill=1, stroke=0)
        c.setFillColor(HexColor('#1565C0'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(70, y - 25, f"Page Size: {label}")
        c.setFont("Helvetica", 11)
        c.drawString(70, y - 45, f"Dimensions: {w:.0f} x {h:.0f} points ({w/72:.1f}\" x {h/72:.1f}\")")
        c.drawString(70, y - 65, f"Pixels at 150 DPI: {int(w*150/72)} x {int(h*150/72)}")
        
        y -= 120
        
        # Fill with content
        c.setFont("Helvetica", 9)
        c.setFillColor(black)
        line_count = int((y - 40) / 14)
        for i in range(min(line_count, 40)):
            c.drawString(50, y, f"Line {i+1}: Content for NaViT stress test on {label} page ({w:.0f}x{h:.0f}pt)")
            y -= 14
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (mixed sizes)")


def generate_long_contract_pdf(path):
    """PDF 3: 30-page contract document (A4)."""
    w, h = A4
    total = 30
    c = canvas.Canvas(path, pagesize=A4)
    
    articles = [
        "Objet du Contrat", "Durée et Renouvellement", "Prix et Modalités de Paiement",
        "Obligations du Prestataire", "Obligations du Client", "Propriété Intellectuelle",
        "Confidentialité", "Protection des Données", "Responsabilité et Garanties",
        "Force Majeure", "Résiliation", "Sous-Traitance",
        "Non-Sollicitation", "Assurances", "Conformité Réglementaire",
        "Audit et Contrôle", "Communication", "Transfert de Compétences",
        "Gouvernance du Contrat", "Pénalités et Bonus",
        "Modifications et Avenants", "Droit Applicable", "Juridiction Compétente",
        "Notifications", "Dispositions Générales", "Annexe A: SLA",
        "Annexe B: Livrables", "Annexe C: Équipe Projet",
        "Annexe D: Plan de Transition", "Signatures",
    ]
    
    for page in range(1, total + 1):
        draw_header(c, w, h, "CONTRAT DE PRESTATION DE SERVICES IT", page, total)
        y = h - 70
        
        if page == 1:
            c.setFont("Helvetica-Bold", 20)
            c.setFillColor(HexColor('#1565C0'))
            c.drawCentredString(w/2, y, "CONTRAT DE PRESTATION")
            y -= 25
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(w/2, y, "DE SERVICES INFORMATIQUES")
            y -= 40
            
            c.setFont("Helvetica", 11)
            c.setFillColor(black)
            parties = [
                "ENTRE LES SOUSSIGNÉS:",
                "",
                "TECH SOLUTIONS SARL, société à responsabilité limitée au capital de 5.000.000 MAD,",
                "immatriculée au RC sous le numéro 123456, dont le siège social est situé au",
                "45 Boulevard Zerktouni, 20000 Casablanca, Maroc,",
                "représentée par M. Ahmed BENALI, en sa qualité de Directeur Général,",
                "ci-après dénommée « le Prestataire »,",
                "",
                "D'UNE PART,",
                "",
                "ET:",
                "",
                "GROUPE INDUSTRIEL ABC SA, société anonyme au capital de 50.000.000 MAD,",
                "immatriculée au RC sous le numéro 789012, dont le siège social est situé au",
                "10 Avenue Hassan II, 10000 Rabat, Maroc,",
                "représentée par Mme Sara EL FASSI, en sa qualité de Directrice des Systèmes",
                "d'Information,",
                "ci-après dénommée « le Client »,",
                "",
                "D'AUTRE PART,",
                "",
                "Ci-après dénommées ensemble « les Parties » et individuellement « la Partie ».",
            ]
            for line in parties:
                c.drawString(50, y, line)
                y -= 15
        else:
            article_idx = min(page - 2, len(articles) - 1)
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(HexColor('#1565C0'))
            c.drawString(50, y, f"Article {page-1} — {articles[article_idx]}")
            y -= 25
            
            c.setFont("Helvetica", 10)
            c.setFillColor(black)
            
            clauses = [
                f"{page-1}.1 Le Prestataire s'engage à réaliser les prestations décrites dans le présent",
                f"article conformément aux spécifications techniques définies en Annexe A.",
                "",
                f"{page-1}.2 Les prestations seront exécutées selon le calendrier établi d'un commun",
                f"accord entre les Parties, tel que détaillé dans le planning prévisionnel.",
                "",
                f"{page-1}.3 Le Prestataire garantit que les livrables seront conformes aux standards",
                f"de qualité définis par les normes ISO 27001 et les bonnes pratiques du secteur.",
                "",
                f"{page-1}.4 En cas de non-conformité, le Client dispose d'un délai de quinze (15)",
                f"jours ouvrés pour formuler ses observations par écrit au Prestataire.",
                "",
                f"{page-1}.5 Le Prestataire s'engage à mettre en œuvre les corrections nécessaires",
                f"dans un délai de dix (10) jours ouvrés suivant la réception des observations.",
                "",
                f"{page-1}.6 Les Parties conviennent que toute modification du périmètre initial",
                f"fera l'objet d'un avenant signé par les deux Parties.",
                "",
                f"{page-1}.7 Le Prestataire s'engage à respecter l'ensemble des dispositions légales",
                f"et réglementaires applicables au Maroc, notamment la loi 09-08 relative à la",
                f"protection des personnes physiques à l'égard du traitement des données personnelles.",
                "",
                f"{page-1}.8 Sans préjudice des autres dispositions du présent contrat, le Prestataire",
                f"garantit la disponibilité d'une équipe dédiée composée au minimum de :",
                f"    a) Un chef de projet certifié PMP ou équivalent",
                f"    b) Deux développeurs seniors (5+ ans d'expérience)",
                f"    c) Un architecte solutions cloud",
                f"    d) Un ingénieur qualité et tests",
                "",
                f"{page-1}.9 Le présent article est soumis aux dispositions de l'article 230 du DOC",
                f"et aux dispositions de la loi 31-08 édictant des mesures de protection du consommateur.",
            ]
            
            for line in clauses:
                if y < 40:
                    break
                c.drawString(50, y, line)
                y -= 14
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (A4 contract)")


def generate_receipt_roll_pdf(path):
    """PDF 4: 20-page receipt roll with narrow pages."""
    page_w = 220  # ~80mm thermal receipt
    page_h = 800
    total = 20
    c = canvas.Canvas(path, pagesize=(page_w, page_h))
    
    for page in range(1, total + 1):
        c.setPageSize((page_w, page_h))
        
        # White background
        c.setFillColor(HexColor('#FFFEF5'))
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        
        y = page_h - 20
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(black)
        c.drawCentredString(page_w/2, y, "SUPERMARCHE CENTRAL")
        y -= 12
        c.setFont("Helvetica", 7)
        c.drawCentredString(page_w/2, y, f"Ticket #{page:04d} — Caisse {(page%5)+1}")
        y -= 10
        c.drawCentredString(page_w/2, y, "06/02/2026 14:32")
        y -= 15
        
        # Dashed line
        c.setDash(3, 2)
        c.setStrokeColor(HexColor('#999999'))
        c.line(10, y, page_w - 10, y)
        c.setDash()
        y -= 15
        
        items = [
            ("Pain complet", "8.50"), ("Lait 1L", "7.90"), ("Oeufs x12", "15.00"),
            ("Huile olive", "45.00"), ("Tomates 1kg", "12.00"), ("Poulet", "55.00"),
            ("Riz 1kg", "14.00"), ("Sucre 1kg", "8.50"), ("The vert", "22.00"),
            ("Beurre", "18.00"), ("Fromage", "12.50"), ("Yaourt x4", "16.00"),
            ("Eau 1.5L", "5.00"), ("Jus orange", "15.00"), ("Bananes", "14.00"),
            ("Cafe 250g", "35.00"), ("Chocolat", "20.00"), ("Biscuits", "18.50"),
            ("Miel 500g", "45.00"), ("Sardines", "24.00"),
        ]
        
        c.setFont("Helvetica", 7)
        total_amount = 0
        start = ((page-1) * 3) % len(items)
        for i in range(min(len(items), int((y - 80) / 10))):
            idx = (start + i) % len(items)
            name, price = items[idx]
            total_amount += float(price)
            c.drawString(10, y, name)
            c.drawRightString(page_w - 10, y, price)
            y -= 10
        
        y -= 5
        c.setDash(3, 2)
        c.line(10, y, page_w - 10, y)
        c.setDash()
        y -= 12
        
        c.setFont("Helvetica-Bold", 8)
        c.drawString(10, y, "TOTAL TTC:")
        c.drawRightString(page_w - 10, y, f"{total_amount*1.2:.2f} MAD")
        y -= 20
        
        c.setFont("Helvetica", 6)
        c.drawCentredString(page_w/2, y, "Merci de votre visite!")
        c.drawCentredString(page_w/2, 10, f"Page {page}/{total}")
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (narrow receipt)")


def generate_presentation_pdf(path):
    """PDF 5: 25-page landscape presentation slides."""
    w, h = landscape(A4)
    total = 25
    c = canvas.Canvas(path, pagesize=landscape(A4))
    
    slides = [
        ("TITRE: Transformation Digitale 2026", "cover"),
        ("Agenda", "text"), ("Contexte & Enjeux", "text"),
        ("Vision Stratégique", "text"), ("Diagnostic IT Actuel", "table"),
        ("Architecture Cible", "text"), ("Feuille de Route", "table"),
        ("Phase 1: Infrastructure Cloud", "text"), ("Phase 2: Data & IA", "text"),
        ("Phase 3: Applications Métier", "text"), ("Budget Prévisionnel", "table"),
        ("ROI Attendu", "table"), ("Risques & Mitigation", "table"),
        ("Équipe Projet", "text"), ("Gouvernance", "text"),
        ("KPIs & Tableau de Bord", "table"), ("Cas d'Usage IA", "text"),
        ("Architecture Microservices", "text"), ("Plan de Formation", "text"),
        ("Change Management", "text"), ("Timeline Détaillée", "table"),
        ("Quick Wins vs Long Terme", "text"), ("Benchmark Concurrentiel", "table"),
        ("Questions & Discussion", "text"), ("Contacts & Prochaines Étapes", "text"),
    ]
    
    bg_colors = ['#1565C0', '#0D47A1', '#283593', '#1A237E', '#004D40',
                 '#1B5E20', '#E65100', '#BF360C', '#4A148C', '#880E4F']
    
    for page, (title, stype) in enumerate(slides, 1):
        c.setPageSize(landscape(A4))
        bg = HexColor(bg_colors[(page-1) % len(bg_colors)])
        
        if stype == "cover" or page == 1:
            c.setFillColor(bg)
            c.rect(0, 0, w, h, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 32)
            c.drawCentredString(w/2, h/2 + 30, "TRANSFORMATION DIGITALE")
            c.setFont("Helvetica", 20)
            c.drawCentredString(w/2, h/2 - 10, "Plan Stratégique 2026-2028")
            c.setFont("Helvetica", 14)
            c.drawCentredString(w/2, h/2 - 50, "Groupe Benali Holdings — Direction des Systèmes d'Information")
            c.setFont("Helvetica", 10)
            c.drawCentredString(w/2, 40, f"Février 2026 | Confidentiel")
        else:
            # Slide layout
            c.setFillColor(white)
            c.rect(0, 0, w, h, fill=1, stroke=0)
            
            # Title bar
            c.setFillColor(bg)
            c.rect(0, h - 60, w, 60, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(30, h - 42, title)
            c.setFont("Helvetica", 9)
            c.drawRightString(w - 30, h - 42, f"{page}/{total}")
            
            y = h - 90
            
            if stype == "table":
                data = [["Élément", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "Total"]]
                rows = ["Infrastructure", "Licences", "Développement", "Formation",
                       "Consulting", "Support", "Contingence"]
                for row_name in rows:
                    vals = [f"{random.randint(50, 500)}K" for _ in range(4)]
                    total_val = sum(int(v[:-1]) for v in vals)
                    data.append([row_name] + vals + [f"{total_val}K"])
                
                t = Table(data, colWidths=[140, 100, 100, 100, 100, 100])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), bg),
                    ('TEXTCOLOR', (0, 0), (-1, 0), white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDBDBD')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F5F5F5')]),
                ]))
                tw, th = t.wrapOn(c, w - 60, y)
                t.drawOn(c, 30, y - th)
            else:
                c.setFont("Helvetica", 11)
                c.setFillColor(black)
                bullets = [
                    "Objectif: Moderniser l'infrastructure IT du Groupe",
                    "Migration vers le cloud (Azure/AWS) pour 80% des workloads",
                    "Mise en place d'une plateforme Data centralisée",
                    "Déploiement de solutions IA pour l'automatisation",
                    "Renforcement de la cybersécurité (Zero Trust)",
                    "Formation de 500 collaborateurs aux outils digitaux",
                    "ROI attendu: 25% de réduction des coûts IT en 3 ans",
                    "Création d'un Centre d'Excellence IA & Data",
                ]
                for bullet in bullets:
                    c.drawString(50, y, f"▸  {bullet}")
                    y -= 28
            
            # Bottom brand bar
            c.setFillColor(HexColor('#ECEFF1'))
            c.rect(0, 0, w, 25, fill=1, stroke=0)
            c.setFillColor(HexColor('#78909C'))
            c.setFont("Helvetica", 7)
            c.drawString(30, 9, "Groupe Benali Holdings — Transformation Digitale 2026")
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (landscape slides)")


def generate_technical_manual_pdf(path):
    """PDF 6: 50-page A4 technical manual with code and diagrams."""
    w, h = A4
    total = 50
    c = canvas.Canvas(path, pagesize=A4)
    
    chapters = [
        "Installation", "Configuration", "Architecture", "API Reference",
        "Authentication", "Database Schema", "REST Endpoints", "WebSocket API",
        "Error Handling", "Testing", "Deployment", "Monitoring",
        "Troubleshooting", "Performance Tuning", "Security Best Practices",
    ]
    
    for page in range(1, total + 1):
        draw_header(c, w, h, "MANUEL TECHNIQUE — API Platform v3.2", page, total)
        y = h - 70
        
        if page == 1:
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(HexColor('#1565C0'))
            c.drawCentredString(w/2, h/2 + 40, "API PLATFORM v3.2")
            c.setFont("Helvetica", 16)
            c.setFillColor(HexColor('#333333'))
            c.drawCentredString(w/2, h/2, "Manuel Technique & Documentation API")
            c.setFont("Helvetica", 11)
            c.drawCentredString(w/2, h/2 - 40, "Version 3.2.1 — Février 2026")
        else:
            ch_idx = ((page - 2) // 3) % len(chapters)
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(HexColor('#1565C0'))
            c.drawString(50, y, f"Chapitre {ch_idx+1}: {chapters[ch_idx]}")
            y -= 30
            
            # Alternate between code blocks and text
            if page % 3 == 0:
                # Code block
                c.setFillColor(HexColor('#263238'))
                c.roundRect(50, y - 200, w - 100, 200, 5, fill=1, stroke=0)
                c.setFillColor(HexColor('#80CBC4'))
                c.setFont("Courier", 8)
                
                code_lines = [
                    "from fastapi import FastAPI, HTTPException",
                    "from pydantic import BaseModel",
                    "import uvicorn",
                    "",
                    "app = FastAPI(title='API Platform', version='3.2')",
                    "",
                    "class Document(BaseModel):",
                    "    id: str",
                    "    title: str", 
                    "    content: str",
                    "    pages: int = 1",
                    "",
                    "@app.post('/api/v3/documents')",
                    "async def create_document(doc: Document):",
                    "    result = await db.documents.insert_one(",
                    "        doc.model_dump()",
                    "    )",
                    "    return {'id': str(result.inserted_id)}",
                    "",
                    "@app.get('/api/v3/documents/{doc_id}')",
                    "async def get_document(doc_id: str):",
                    "    doc = await db.documents.find_one({'id': doc_id})",
                    "    if not doc:",
                    "        raise HTTPException(404, 'Document not found')",
                    "    return Document(**doc)",
                ]
                
                code_y = y - 15
                for line in code_lines:
                    c.drawString(60, code_y, line)
                    code_y -= 10
                
                y -= 220
            
            # Text content
            c.setFont("Helvetica", 10)
            c.setFillColor(black)
            for i in range(int((y - 40) / 14)):
                c.drawString(50, y, f"Documentation technique pour le chapitre {chapters[ch_idx]} — Section {i+1}.")
                y -= 14
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (A4 technical manual)")


def generate_ledger_pdf(path):
    """PDF 7: 12-page A3 landscape accounting ledger."""
    w, h = landscape(A3)
    total = 12
    c = canvas.Canvas(path, pagesize=landscape(A3))
    
    months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
              "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    
    for page in range(1, total + 1):
        c.setPageSize(landscape(A3))
        draw_header(c, w, h, f"GRAND LIVRE COMPTABLE — {months[page-1]} 2025", page, total)
        y = h - 70
        
        # Large table
        data = [["Date", "N° Pièce", "Compte", "Libellé", "Débit", "Crédit", "Solde", "TVA", "Devise", "Réf"]]
        
        running_balance = 1000000
        for day in range(1, 29):
            debit = random.randint(1000, 50000) if random.random() > 0.4 else 0
            credit = random.randint(1000, 50000) if debit == 0 else 0
            running_balance += credit - debit
            account = random.choice(["6110", "6120", "6130", "7010", "7020", "4411", "5141"])
            data.append([
                f"{day:02d}/{page:02d}/25",
                f"PJ-{page:02d}{day:02d}",
                account,
                f"Opération {account} - {months[page-1][:3]}",
                f"{debit:,.0f}" if debit else "",
                f"{credit:,.0f}" if credit else "",
                f"{running_balance:,.0f}",
                f"{(debit or credit) * 0.2:,.0f}",
                "MAD",
                f"R-{page:02d}{day:02d}"
            ])
        
        t = Table(data, colWidths=[65, 70, 55, 180, 80, 80, 90, 70, 40, 65])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0D47A1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (4, 1), (7, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#BDBDBD')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F5F5F5')]),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        tw, th = t.wrapOn(c, w - 60, y)
        t.drawOn(c, 30, y - th)
        
        c.showPage()
    
    c.save()
    print(f"  ✓ {os.path.basename(path)} — {total} pages (A3 landscape ledger)")


# ============================================================
# Main
# ============================================================

PDF_CONFIGS = [
    {"id": "01_financial_report",   "gen": generate_financial_report_pdf,  "pages": 15, "desc": "A4 financial report with tables"},
    {"id": "02_mixed_sizes",        "gen": generate_mixed_sizes_pdf,       "pages": 10, "desc": "Mixed page sizes (A4/A3/Letter/Legal/Custom)"},
    {"id": "03_long_contract",      "gen": generate_long_contract_pdf,     "pages": 30, "desc": "A4 legal contract"},
    {"id": "04_receipt_roll",       "gen": generate_receipt_roll_pdf,      "pages": 20, "desc": "Narrow thermal receipt pages"},
    {"id": "05_presentation",       "gen": generate_presentation_pdf,      "pages": 25, "desc": "Landscape presentation slides"},
    {"id": "06_technical_manual",   "gen": generate_technical_manual_pdf,  "pages": 50, "desc": "A4 technical documentation"},
    {"id": "07_accounting_ledger",  "gen": generate_ledger_pdf,            "pages": 12, "desc": "A3 landscape accounting ledger"},
]

def main():
    print("="*60)
    print("GENERATING MULTI-PAGE PDF DOCUMENTS")
    print("="*60 + "\n")
    
    total_pages = 0
    for cfg in PDF_CONFIGS:
        path = os.path.join(OUTPUT_DIR, f"{cfg['id']}.pdf")
        try:
            cfg["gen"](path)
            total_pages += cfg["pages"]
        except Exception as e:
            print(f"  ✗ {cfg['id']}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ {len(PDF_CONFIGS)} PDFs generated ({total_pages} total pages)")
    print(f"\n{'#':<4} {'PDF':<25} {'Pages':>6} {'Description'}")
    print("-"*70)
    for i, cfg in enumerate(PDF_CONFIGS, 1):
        print(f"{i:<4} {cfg['id']:<25} {cfg['pages']:>6}  {cfg['desc']}")

if __name__ == "__main__":
    main()
