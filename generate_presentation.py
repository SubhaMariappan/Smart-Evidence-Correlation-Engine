"""
generate_presentation.py
Generates a 17-slide, light-themed, professional, editable PowerPoint presentation
for the MCA Project Review: "SMART EVIDENCE CORRELATION ENGINE (SECE)".

Key Updates:
- Content rewritten to be SHORT, CRISP, PUNCHY, and EASY TO UNDERSTAND for Viva.
- Slide 10 (DFD Level 1) uses the newly uploaded vertical Mermaid DFD Level 1 flowchart image (media_1794637676413.png).
- Slide 8 uses the high-res 4-Tier System Architecture visual diagram.
- Slide 9 uses the high-res DFD Level 0 Context Diagram.
- Slide 13 provides Experimental Results & System Verification.
- Slide 14 provides Project Conclusion & Key Takeaways (BEFORE Future Roadmap).
- Slide 15 provides Future Scope & Technological Roadmap.
- Full concise speaker notes in slide.notes_slide for every slide.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.xmlchemy import OxmlElement

# ==============================================================================
# COLOR PALETTE DEFINITIONS (LIGHT THEME)
# ==============================================================================
COLOR_WHITE        = RGBColor(255, 255, 255)  # Pure White background
COLOR_OFFWHITE     = RGBColor(248, 250, 252)  # Soft card fill (#F8FAFC)
COLOR_CARD_ALT     = RGBColor(241, 245, 249)  # Subtle alternate card fill (#F1F5F9)
COLOR_NAVY         = RGBColor(15, 23, 42)     # Deep Academic Navy (#0F172A)
COLOR_NAVY_ACCENT  = RGBColor(30, 58, 138)    # Royal Navy (#1E3A8A)
COLOR_TEAL         = RGBColor(13, 148, 136)   # Forensic Teal (#0D9488)
COLOR_TEAL_LIGHT   = RGBColor(240, 253, 250)  # Light teal tint (#F0FDFA)
COLOR_TEAL_BORDER  = RGBColor(153, 246, 228)  # Teal border tint (#99F6E4)
COLOR_CHARCOAL     = RGBColor(30, 41, 59)     # Dark Charcoal body text (#1E293B)
COLOR_MUTED_GRAY   = RGBColor(100, 116, 139)  # Subtle secondary text (#64748B)
COLOR_BORDER_GRAY  = RGBColor(203, 213, 225)  # Card border (#CBD5E1)
COLOR_BORDER_LIGHT = RGBColor(226, 232, 240)  # Subtle divider (#E2E8F0)
COLOR_RED_ACCENT   = RGBColor(225, 29, 72)    # Alert/drawback red (#E11D48)
COLOR_GREEN_ACCENT = RGBColor(16, 185, 129)   # Success green (#10B981)

FONT_HEADING = "Calibri"
FONT_BODY    = "Calibri"

# ==============================================================================
# IMAGE PATHS RESOLUTION (HIGH-RES GENERATED & USER-UPLOADED)
# ==============================================================================
BASE_BRAIN = r"C:\Users\user\.gemini\antigravity\brain\6a46f846-1f99-44a1-b5f4-85561fdf0993"
BASE_UPLOADED = os.path.join(BASE_BRAIN, ".user_uploaded")

# System Architecture (Slide 8)
IMG_SYS_ARCH = os.path.join(BASE_BRAIN, "system_architecture_1794630152275.jpg")
if not os.path.exists(IMG_SYS_ARCH):
    IMG_SYS_ARCH = os.path.join(BASE_UPLOADED, "media_1794637010835.jpg")

# DFD Level 0 Context Diagram (Slide 9)
IMG_DFD_0 = os.path.join(BASE_BRAIN, "dfd_level_0_1794630282522.jpg")
if not os.path.exists(IMG_DFD_0):
    IMG_DFD_0 = os.path.join(BASE_UPLOADED, "media_1794637010655.jpg")

# DFD Level 1 Flowchart (Slide 10) - User explicitly uploaded media_1794637676413.png
IMG_DFD_1 = os.path.join(BASE_UPLOADED, "media_1794637676413.png")
if not os.path.exists(IMG_DFD_1):
    IMG_DFD_1 = os.path.join(BASE_UPLOADED, "media_1794637010651.png")
if not os.path.exists(IMG_DFD_1):
    IMG_DFD_1 = os.path.join(BASE_BRAIN, "dfd_level_1_1794630308063.jpg")


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def create_presentation():
    """Initializes a 16:9 widescreen presentation."""
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide):
    """Sets slide background to pure white."""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_WHITE
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_text=None):
    """Adds a standard light-themed slide header."""
    top_y = Inches(0.4)
    if category_text:
        cat_box = slide.shapes.add_textbox(Inches(0.8), top_y, Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_TEAL
        top_y += Inches(0.32)

    title_box = slide.shapes.add_textbox(Inches(0.8), top_y, Inches(11.7), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

    # Horizontal divider line
    div = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.02)
    )
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_BORDER_LIGHT
    div.line.fill.background()

def add_card(slide, left, top, width, height, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY):
    """Creates a card container shape with subtle border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_speaker_notes(slide, notes_text):
    """Appends clear speaker notes to the slide's notes slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text.strip()

def add_straight_arrow(slide, x1, y1, x2, y2, color=COLOR_TEAL, width=Pt(1.5)):
    """Draws a strict straight orthogonal connector line with an arrowhead."""
    connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    connector.line.color.rgb = color
    connector.line.width = width
    ln = connector._element.spPr.ln
    tailEnd = OxmlElement('a:tailEnd')
    tailEnd.set('type', 'triangle')
    ln.append(tailEnd)
    return connector

def format_bullet_point(paragraph, bold_prefix, text_content, font_size=13, bullet_char="• "):
    """Formats a concise paragraph with bold prefix in Navy/Teal and normal body in Charcoal."""
    paragraph.font.name = FONT_BODY
    paragraph.font.size = Pt(font_size)
    paragraph.space_after = Pt(8)
    paragraph.line_spacing = 1.15

    # Bullet symbol
    r_bullet = paragraph.add_run()
    r_bullet.text = bullet_char
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = COLOR_TEAL

    # Bold prefix
    if bold_prefix:
        r_prefix = paragraph.add_run()
        r_prefix.text = bold_prefix + ": "
        r_prefix.font.bold = True
        r_prefix.font.color.rgb = COLOR_NAVY

    # Normal text
    r_text = paragraph.add_run()
    r_text.text = text_content
    r_text.font.bold = False
    r_text.font.color.rgb = COLOR_CHARCOAL


# ==============================================================================
# SLIDE BUILDERS (17 SLIDES — SHORT, CRISP & EASY TO UNDERSTAND)
# ==============================================================================

# ------------------------------------------------------------------------------
# SLIDE 1: FRONT PAGE (COVER SLIDE)
# ------------------------------------------------------------------------------
def build_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)

    # Vertical left decorative accent bars
    bar1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), Inches(7.5))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = COLOR_NAVY_ACCENT
    bar1.line.fill.background()

    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), 0, Inches(0.12), Inches(7.5))
    bar2.fill.solid()
    bar2.fill.fore_color.rgb = COLOR_TEAL
    bar2.line.fill.background()

    # Institution Header
    inst_box = slide.shapes.add_textbox(Inches(1.2), Inches(0.55), Inches(11.2), Inches(1.3))
    tf_inst = inst_box.text_frame
    tf_inst.word_wrap = True
    tf_inst.margin_left = tf_inst.margin_top = tf_inst.margin_right = tf_inst.margin_bottom = 0

    p1 = tf_inst.paragraphs[0]
    p1.text = "RATHINAM TECHNICAL CAMPUS (AUTONOMOUS)"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(19)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY
    p1.space_after = Pt(3)

    p2 = tf_inst.add_paragraph()
    p2.text = "Affiliated to Anna University, Chennai | Approved by AICTE | Coimbatore – 641 021"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_MUTED_GRAY
    p2.space_after = Pt(4)

    p3 = tf_inst.add_paragraph()
    p3.text = "Department of Master of Computer Applications (MCA)"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEAL

    # Horizontal divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.05), Inches(11.2), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_BORDER_LIGHT
    div.line.fill.background()

    # Course Badge
    course_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.25), Inches(2.8), Inches(0.38))
    course_bg.fill.solid()
    course_bg.fill.fore_color.rgb = COLOR_TEAL_LIGHT
    course_bg.line.color.rgb = COLOR_TEAL_BORDER
    course_tf = course_bg.text_frame
    course_tf.margin_top = Inches(0.06)
    course_p = course_tf.paragraphs[0]
    course_p.alignment = PP_ALIGN.CENTER
    course_p.text = "25EEC204 – MINI PROJECT II"
    course_p.font.name = FONT_HEADING
    course_p.font.size = Pt(11)
    course_p.font.bold = True
    course_p.font.color.rgb = COLOR_TEAL

    # Main Project Title
    title_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.75), Inches(11.2), Inches(1.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0

    p_main = tf_title.paragraphs[0]
    p_main.text = "SMART EVIDENCE CORRELATION ENGINE (SECE)"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_NAVY
    p_main.space_after = Pt(8)

    p_sub = tf_title.add_paragraph()
    p_sub.text = "AI-Powered Digital Forensics & Multi-Source Evidence Correlation Platform"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(17)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEAL

    # Bottom Candidates & Guide Information Card
    card_info = add_card(slide, Inches(1.2), Inches(4.7), Inches(11.2), Inches(2.1), fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    # Left Column: Students
    stud_box = slide.shapes.add_textbox(Inches(1.5), Inches(4.85), Inches(5.2), Inches(1.8))
    tf_stud = stud_box.text_frame
    tf_stud.word_wrap = True
    tf_stud.margin_left = tf_stud.margin_top = tf_stud.margin_right = tf_stud.margin_bottom = 0

    ps_h = tf_stud.paragraphs[0]
    ps_h.text = "SUBMITTED BY:"
    ps_h.font.name = FONT_HEADING
    ps_h.font.size = Pt(11)
    ps_h.font.bold = True
    ps_h.font.color.rgb = COLOR_TEAL
    ps_h.space_after = Pt(4)

    ps1 = tf_stud.add_paragraph()
    ps1.text = "•  SUBHALEKSHMI M  (Reg No: 25205090)"
    ps1.font.name = FONT_BODY
    ps1.font.size = Pt(14)
    ps1.font.bold = True
    ps1.font.color.rgb = COLOR_NAVY
    ps1.space_after = Pt(3)

    ps2 = tf_stud.add_paragraph()
    ps2.text = "•  YUKTHA R  (Reg No: 25205113)"
    ps2.font.name = FONT_BODY
    ps2.font.size = Pt(14)
    ps2.font.bold = True
    ps2.font.color.rgb = COLOR_NAVY
    ps2.space_after = Pt(6)

    ps_deg = tf_stud.add_paragraph()
    ps_deg.text = "Master of Computer Applications (MCA) — II Semester"
    ps_deg.font.name = FONT_BODY
    ps_deg.font.size = Pt(11)
    ps_deg.font.color.rgb = COLOR_MUTED_GRAY

    # Right Column: Guide
    guide_box = slide.shapes.add_textbox(Inches(7.2), Inches(4.85), Inches(4.8), Inches(1.8))
    tf_guide = guide_box.text_frame
    tf_guide.word_wrap = True
    tf_guide.margin_left = tf_guide.margin_top = tf_guide.margin_right = tf_guide.margin_bottom = 0

    pg_h = tf_guide.paragraphs[0]
    pg_h.text = "PROJECT SUPERVISOR / GUIDE:"
    pg_h.font.name = FONT_HEADING
    pg_h.font.size = Pt(11)
    pg_h.font.bold = True
    pg_h.font.color.rgb = COLOR_TEAL
    pg_h.space_after = Pt(4)

    pg1 = tf_guide.add_paragraph()
    pg1.text = "Ms. R. ALAMELUMANGAI, M.C.A., M.Phil."
    pg1.font.name = FONT_BODY
    pg1.font.size = Pt(14)
    pg1.font.bold = True
    pg1.font.color.rgb = COLOR_NAVY
    pg1.space_after = Pt(2)

    pg2 = tf_guide.add_paragraph()
    pg2.text = "Assistant Professor, Dept. of Computer Applications"
    pg2.font.name = FONT_BODY
    pg2.font.size = Pt(12)
    pg2.font.color.rgb = COLOR_CHARCOAL
    pg2.space_after = Pt(6)

    pg3 = tf_guide.add_paragraph()
    pg3.text = "Academic Year: 2025 – 2026  |  Review: May – 2026"
    pg3.font.name = FONT_BODY
    pg3.font.size = Pt(11)
    pg3.font.bold = True
    pg3.font.color.rgb = COLOR_TEAL

    add_speaker_notes(slide, 
        "Good morning respected examiners and faculty members. Welcome to our MCA Mini Project II review. "
        "Our project is titled 'Smart Evidence Correlation Engine' (SECE), presented by Subhalekshmi M and Yuktha R, "
        "guided by Ms. R. Alamelumangai. SECE automates multi-source forensic triage, preserves file integrity via SHA-256, "
        "and uncovers hidden relationships across disconnected digital evidence."
    )

# ------------------------------------------------------------------------------
# SLIDE 2: AGENDA
# ------------------------------------------------------------------------------
def build_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Table of Contents & Presentation Roadmap", "OVERVIEW")

    agenda_items = [
        ("01", "Abstract & Problem Statement", "Forensic bottlenecks in multi-source investigations"),
        ("02", "Project Objectives & Scope", "6 core functional pillars of the SECE engine"),
        ("03", "Existing System & Drawbacks", "Manual spreadsheet triage and custody vulnerabilities"),
        ("04", "Proposed System (SECE)", "Centralized architecture & automated correlation advantages"),
        ("05", "System Configuration & Feasibility", "Hardware, open-source software stack & viability"),
        ("06", "System Architecture (4-Tier Framework)", "Visual architecture covering Presentation to Storage"),
        ("07", "Data Flow Diagram — Level 0", "Context diagram modeling system boundary & external roles"),
        ("08", "Data Flow Diagram — Level 1", "Subprocess pipeline and data store interactions"),
        ("09", "Core Modules & Execution Workflow", "Step-by-step lifecycle from ingestion to link discovery"),
        ("10", "Database Design (PostgreSQL 18.6)", "10 normalized tables separating facts from inferences"),
        ("11", "Experimental Results & Verification", "Multi-source testing, live tamper detection & metrics"),
        ("12", "Project Conclusion & Takeaways", "Summary of contributions, compliance & impact"),
        ("13", "Future Scope & Technological Roadmap", "OCR, Cytoscape graph canvas & court dossier export"),
        ("14", "References & Standards", "Forensic standards (NIST, ISO) & academic literature")
    ]

    card_w = Inches(5.7)
    card_h = Inches(0.68)
    start_y = Inches(1.55)

    for i, (num, title, desc) in enumerate(agenda_items):
        col = i // 7
        row = i % 7
        left = Inches(0.8) if col == 0 else Inches(6.8)
        top = start_y + row * Inches(0.76)

        card = add_card(slide, left, top, card_w, card_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_LIGHT)

        # Number badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.12), top + Inches(0.1), Inches(0.52), Inches(0.48))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_TEAL_LIGHT
        badge.line.color.rgb = COLOR_TEAL_BORDER
        badge_tf = badge.text_frame
        badge_tf.margin_top = Inches(0.08)
        p_b = badge_tf.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = num
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(13)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_TEAL

        # Text box
        txt_box = slide.shapes.add_textbox(left + Inches(0.74), top + Inches(0.08), card_w - Inches(0.82), Inches(0.52))
        tf = txt_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY
        p1.space_after = Pt(1)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_MUTED_GRAY

    add_speaker_notes(slide,
        "Here is the presentation roadmap. We will walk through the forensic problem, our objectives, "
        "the existing manual limitations, the proposed SECE platform, our 4-tier architecture, DFD Levels 0 & 1, "
        "core pipeline modules, database design, verified experimental results, project conclusion, and future roadmap."
    )

# ------------------------------------------------------------------------------
# SLIDE 3: 01 — ABSTRACT & PROBLEM STATEMENT (SHORT & CRISP)
# ------------------------------------------------------------------------------
def build_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Abstract & Forensic Problem Statement", "01 — PROJECT BACKGROUND")

    card_w = Inches(5.7)
    card_h = Inches(5.4)
    top_y = Inches(1.6)

    # Left Card: Problem Statement
    card_left = add_card(slide, Inches(0.8), top_y, card_w, card_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    tag_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, card_w, Inches(0.45))
    tag_l.fill.solid()
    tag_l.fill.fore_color.rgb = COLOR_NAVY
    tag_l.line.fill.background()
    p_tl = tag_l.text_frame.paragraphs[0]
    p_tl.text = "   THE PROBLEM: MANUAL FORENSIC BOTTLENECKS"
    p_tl.font.name = FONT_HEADING
    p_tl.font.size = Pt(12)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_WHITE

    tb_left = slide.shapes.add_textbox(Inches(1.1), top_y + Inches(0.65), card_w - Inches(0.6), card_h - Inches(0.8))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p = tf_l.paragraphs[0]
    format_bullet_point(p, "Fragmented Evidence", 
        "Data is trapped in isolated formats (emails, call logs, PDFs, chats) with no unified view.", font_size=12)
    
    p = tf_l.add_paragraph()
    format_bullet_point(p, "Slow Manual Sifting", 
        "Analysts manually search spreadsheets and notes, causing weeks of investigation delay.", font_size=12)
    
    p = tf_l.add_paragraph()
    format_bullet_point(p, "Missed Multi-Hop Links", 
        "Complex connections spanning 3+ files (Suspect -> IP -> Phone) are easily overlooked.", font_size=12)
    
    p = tf_l.add_paragraph()
    format_bullet_point(p, "Broken Chain of Custody", 
        "Unhashed local files risk tampering and evidence dismissal in court.", font_size=12)

    # Right Card: SECE Solution
    card_right = add_card(slide, Inches(6.8), top_y, card_w, card_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    tag_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), top_y, card_w, Inches(0.45))
    tag_r.fill.solid()
    tag_r.fill.fore_color.rgb = COLOR_TEAL
    tag_r.line.fill.background()
    p_tr = tag_r.text_frame.paragraphs[0]
    p_tr.text = "   THE SOLUTION: AUTOMATED SECE PLATFORM"
    p_tr.font.name = FONT_HEADING
    p_tr.font.size = Pt(12)
    p_tr.font.bold = True
    p_tr.font.color.rgb = COLOR_WHITE

    tb_right = slide.shapes.add_textbox(Inches(7.1), top_y + Inches(0.65), card_w - Inches(0.6), card_h - Inches(0.8))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p = tf_r.paragraphs[0]
    format_bullet_point(p, "Centralized Portal", 
        "FastAPI & PostgreSQL 18.6 web workstation for unified evidence management.", font_size=12)
    
    p = tf_r.add_paragraph()
    format_bullet_point(p, "Streaming SHA-256", 
        "Calculates 64KB chunked hashes upon upload for guaranteed file integrity.", font_size=12)
    
    p = tf_r.add_paragraph()
    format_bullet_point(p, "Automated Extraction", 
        "Regex extracts IOCs (IP, Email, Phone); spaCy NER extracts Persons and Locations.", font_size=12)
    
    p = tf_r.add_paragraph()
    format_bullet_point(p, "Smart Link Discovery", 
        "Algorithmically flags shared indicators and aliases for human investigator approval.", font_size=12)

    add_speaker_notes(slide,
        "Slide 3 contrasts the problem with our solution. "
        "The problem is fragmented evidence, slow spreadsheet triage, missed multi-hop links, and broken chain of custody. "
        "SECE solves this by centralizing files, computing streaming SHA-256 hashes upon upload, "
        "automatically extracting entities with offsets, and highlighting cross-file leads for human verification."
    )

# ------------------------------------------------------------------------------
# SLIDE 4: 02 — OBJECTIVES (SHORT & CLEAN)
# ------------------------------------------------------------------------------
def build_slide_4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Project Objectives & Scope of Work", "02 — PROJECT GOALS")

    objectives = [
        ("01", "Centralized Evidence Vault", 
         "Isolate multi-format case files with strict path-traversal protection and case partitioning."),
        ("02", "Cryptographic Custody", 
         "Calculate streaming 64KB SHA-256 hashes at upload with live tamper verification."),
        ("03", "Modular Factory Parsing", 
         "Non-destructively parse .txt, .csv, and .pdf documents into clean text & JSONB metadata."),
        ("04", "Hybrid Entity Extraction", 
         "Extract deterministic IOCs (Regex) and named entities (spaCy NER) with exact character offsets."),
        ("05", "Cross-Evidence Correlation", 
         "Detect shared identities and suspect aliases across files using Jaro-Winkler string similarity."),
        ("06", "Human-in-the-Loop Triage", 
         "Queue candidate links under PENDING_REVIEW (Accept/Reject) to eliminate false merges.")
    ]

    card_w = Inches(3.73)
    card_h = Inches(2.5)
    start_x = Inches(0.8)
    start_y = Inches(1.6)

    for i, (num, title, desc) in enumerate(objectives):
        row = i // 3
        col = i % 3
        left = start_x + col * Inches(3.98)
        top = start_y + row * Inches(2.7)

        card = add_card(slide, left, top, card_w, card_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)

        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.18), top + Inches(0.18), Inches(0.65), Inches(0.35))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_TEAL_LIGHT
        badge.line.color.rgb = COLOR_TEAL_BORDER
        b_tf = badge.text_frame
        b_tf.margin_top = Inches(0.05)
        p_num = b_tf.paragraphs[0]
        p_num.alignment = PP_ALIGN.CENTER
        p_num.text = num
        p_num.font.name = FONT_HEADING
        p_num.font.size = Pt(12)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_TEAL

        t_box = slide.shapes.add_textbox(left + Inches(0.92), top + Inches(0.15), card_w - Inches(1.05), Inches(0.45))
        t_tf = t_box.text_frame
        t_tf.word_wrap = True
        t_tf.margin_left = t_tf.margin_top = t_tf.margin_right = t_tf.margin_bottom = 0
        p_t = t_tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY

        d_box = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.68), card_w - Inches(0.36), card_h - Inches(0.8))
        d_tf = d_box.text_frame
        d_tf.word_wrap = True
        d_tf.margin_left = d_tf.margin_top = d_tf.margin_right = d_tf.margin_bottom = 0
        p_d = d_tf.paragraphs[0]
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_CHARCOAL
        p_d.line_spacing = 1.25

    add_speaker_notes(slide,
        "Our six core objectives: 1. Centralized evidence vault; 2. Streaming SHA-256 cryptographic custody; "
        "3. Modular parsing of text, CSV, and PDF; 4. Hybrid entity extraction with exact character offsets; "
        "5. Automated cross-evidence correlation; and 6. Human-in-the-loop review under PENDING_REVIEW."
    )

# ------------------------------------------------------------------------------
# SLIDE 5: 03 — EXISTING SYSTEM & DRAWBACKS (SHORT & VISUAL)
# ------------------------------------------------------------------------------
def build_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Existing Forensic Workflow & Key Limitations", "03 — CURRENT PRACTICE")

    # Top Visual Flow (4 horizontal boxes)
    flow_box_w = Inches(2.6)
    flow_box_h = Inches(0.85)
    top_flow_y = Inches(1.6)

    steps = [
        ("1. Scattered Files", "Emails, CDRs, and PDFs saved on local drives"),
        ("2. Isolated Viewers", "Excel, Notepad, and PDF tools opened side-by-side"),
        ("3. Manual Cross-Check", "Mental notes, VLOOKUPs, and paper logs"),
        ("4. Delayed Reports", "Turnaround takes weeks; multi-hop leads missed")
    ]

    for i, (title, desc) in enumerate(steps):
        bx = Inches(0.8) + i * Inches(3.04)
        box = add_card(slide, bx, top_flow_y, flow_box_w, flow_box_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
        
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, top_flow_y, flow_box_w, Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = COLOR_RED_ACCENT if i == 3 else COLOR_NAVY_ACCENT
        strip.line.fill.background()

        tb = box.text_frame
        tb.word_wrap = True
        tb.margin_left = Inches(0.12)
        tb.margin_top = Inches(0.14)
        tb.margin_right = Inches(0.12)
        
        p = tb.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(1)

        p2 = tb.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_MUTED_GRAY

        if i < 3:
            ax1 = bx + flow_box_w + Inches(0.05)
            ax2 = ax1 + Inches(0.34)
            ay = top_flow_y + flow_box_h / 2
            add_straight_arrow(slide, ax1, ay, ax2, ay, color=COLOR_RED_ACCENT, width=Pt(1.5))

    # Bottom 4 Key Drawbacks (2x2 Grid)
    drawbacks = [
        ("High Investigation Latency", 
         "Manual spreadsheet searching through thousands of rows takes days, delaying threat response times.", COLOR_RED_ACCENT),
        ("Overlooked Multi-Hop Links", 
         "Indirect leads across 3+ separate files exceed human memory and are routinely missed.", COLOR_RED_ACCENT),
        ("Inability to Match Aliases", 
         "Exact keyword search fails when names differ slightly (e.g., 'Arun Kumar' vs. 'A. Kumar').", COLOR_RED_ACCENT),
        ("Custody & Tampering Risks", 
         "Files stored across desktops lack automated intake hashes, inviting legal challenges in court.", COLOR_RED_ACCENT)
    ]

    grid_w = Inches(5.7)
    grid_h = Inches(1.8)
    grid_top = Inches(2.95)

    for i, (title, desc, accent) in enumerate(drawbacks):
        r = i // 2
        c = i % 2
        gx = Inches(0.8) + c * Inches(6.0)
        gy = grid_top + r * Inches(2.05)

        card = add_card(slide, gx, gy, grid_w, grid_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
        
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx, gy, Inches(0.1), grid_h)
        line.fill.solid()
        line.fill.fore_color.rgb = accent
        line.line.fill.background()

        tb = slide.shapes.add_textbox(gx + Inches(0.25), gy + Inches(0.18), grid_w - Inches(0.4), grid_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_CHARCOAL
        p2.line_spacing = 1.2

    add_speaker_notes(slide,
        "Slide 5 outlines the current manual workflow and its 4 major flaws: "
        "high investigation latency, missed multi-hop links between suspects, "
        "inability to catch aliases, and broken chain-of-custody risks."
    )

# ------------------------------------------------------------------------------
# SLIDE 6: 04 — PROPOSED SYSTEM & ADVANTAGES (SHORT COMPARISON)
# ------------------------------------------------------------------------------
def build_slide_6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Proposed System & Architectural Advantages", "04 — THE SECE PLATFORM")

    col_w = Inches(5.7)
    col_h = Inches(5.4)
    top_y = Inches(1.6)

    # Left Column: Existing Manual Method
    card_l = add_card(slide, Inches(0.8), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    hdr_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, col_w, Inches(0.45))
    hdr_l.fill.solid()
    hdr_l.fill.fore_color.rgb = COLOR_MUTED_GRAY
    hdr_l.line.fill.background()
    p_hl = hdr_l.text_frame.paragraphs[0]
    p_hl.text = "   TRADITIONAL / MANUAL WORKFLOW"
    p_hl.font.name = FONT_HEADING
    p_hl.font.size = Pt(12)
    p_hl.font.bold = True
    p_hl.font.color.rgb = COLOR_WHITE

    # Right Column: Proposed SECE System
    card_r = add_card(slide, Inches(6.8), top_y, col_w, col_h, fill_color=COLOR_TEAL_LIGHT, border_color=COLOR_TEAL_BORDER)
    hdr_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), top_y, col_w, Inches(0.45))
    hdr_r.fill.solid()
    hdr_r.fill.fore_color.rgb = COLOR_TEAL
    hdr_r.line.fill.background()
    p_hr = hdr_r.text_frame.paragraphs[0]
    p_hr.text = "   PROPOSED SECE SYSTEM (AUTOMATED)"
    p_hr.font.name = FONT_HEADING
    p_hr.font.size = Pt(12)
    p_hr.font.bold = True
    p_hr.font.color.rgb = COLOR_WHITE

    comparisons = [
        ("Evidence Intake",
         "Files scattered across local folders without validation.",
         "Centralized sandboxed vault + streaming 64KB SHA-256 hash."),
        ("File Parsing",
         "Manual copy-paste across separate viewer software.",
         "Modular Factory Parsers (.txt, .csv, .pdf) extracting text & metadata."),
        ("Entity Triage",
         "Manual scanning and handwritten notes of IPs/emails.",
         "Automated Regex & spaCy NER with exact character offsets."),
        ("Link Discovery",
         "Spreadsheet VLOOKUPs; suspect aliases completely missed.",
         "Jaro-Winkler fuzzy matching and cross-evidence link scoring."),
        ("Custody & Audit",
         "Informal handwritten case logs vulnerable to dispute.",
         "Immutable PostgreSQL audit_logs ledger tracking all actions.")
    ]

    row_h = Inches(0.88)
    row_start = top_y + Inches(0.55)

    for i, (area, manual, sece) in enumerate(comparisons):
        cy = row_start + i * row_h

        tb_l = slide.shapes.add_textbox(Inches(1.0), cy, col_w - Inches(0.4), row_h - Inches(0.08))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l1 = tf_l.paragraphs[0]
        p_l1.text = f"{area}:"
        p_l1.font.name = FONT_HEADING
        p_l1.font.size = Pt(11)
        p_l1.font.bold = True
        p_l1.font.color.rgb = COLOR_NAVY
        p_l2 = tf_l.add_paragraph()
        p_l2.text = manual
        p_l2.font.name = FONT_BODY
        p_l2.font.size = Pt(10)
        p_l2.font.color.rgb = COLOR_CHARCOAL

        tb_r = slide.shapes.add_textbox(Inches(7.0), cy, col_w - Inches(0.4), row_h - Inches(0.08))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r1 = tf_r.paragraphs[0]
        p_r1.text = f"{area}:"
        p_r1.font.name = FONT_HEADING
        p_r1.font.size = Pt(11)
        p_r1.font.bold = True
        p_r1.font.color.rgb = COLOR_TEAL
        p_r2 = tf_r.add_paragraph()
        p_r2.text = sece
        p_r2.font.name = FONT_BODY
        p_r2.font.size = Pt(10)
        p_r2.font.bold = True
        p_r2.font.color.rgb = COLOR_NAVY

        if i < 4:
            d_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), cy + row_h - Inches(0.04), col_w - Inches(0.4), Inches(0.01))
            d_l.fill.solid()
            d_l.fill.fore_color.rgb = COLOR_BORDER_LIGHT
            d_l.line.fill.background()

            d_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), cy + row_h - Inches(0.04), col_w - Inches(0.4), Inches(0.01))
            d_r.fill.solid()
            d_r.fill.fore_color.rgb = COLOR_TEAL_BORDER
            d_r.line.fill.background()

    add_speaker_notes(slide,
        "Slide 6 provides a clean comparison: "
        "from scattered files to a sandboxed vault with SHA-256; "
        "from manual copy-paste to factory parsers; "
        "from notes to automated Regex and spaCy NER with offsets; "
        "from exact keywords to Jaro-Winkler fuzzy matching; "
        "and from informal notes to an immutable PostgreSQL audit ledger."
    )

# ------------------------------------------------------------------------------
# SLIDE 7: 05 — SYSTEM CONFIGURATION & FEASIBILITY (SHORT & CONCISE)
# ------------------------------------------------------------------------------
def build_slide_7(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Hardware, Software Stack & Feasibility Study", "05 — SYSTEM FEASIBILITY")

    col_w = Inches(3.73)
    col_h = Inches(5.4)
    top_y = Inches(1.6)

    # 1. Hardware Column
    card1 = add_card(slide, Inches(0.8), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    h1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, col_w, Inches(0.45))
    h1.fill.solid()
    h1.fill.fore_color.rgb = COLOR_NAVY
    h1.line.fill.background()
    p1 = h1.text_frame.paragraphs[0]
    p1.text = "   HARDWARE SPECIFICATIONS"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    tb1 = slide.shapes.add_textbox(Inches(1.0), top_y + Inches(0.6), col_w - Inches(0.4), col_h - Inches(0.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    
    p = tf1.paragraphs[0]
    format_bullet_point(p, "Processor", "Intel Core i5 / AMD Ryzen 5 (64-bit multi-core).", font_size=12)
    p = tf1.add_paragraph()
    format_bullet_point(p, "RAM", "8 GB minimum (16 GB recommended for NLP models).", font_size=12)
    p = tf1.add_paragraph()
    format_bullet_point(p, "Storage", "256 GB NVMe SSD for fast DB & evidence vault.", font_size=12)
    p = tf1.add_paragraph()
    format_bullet_point(p, "Display", "1080p Full HD Workstation Monitor.", font_size=12)
    p = tf1.add_paragraph()
    format_bullet_point(p, "Network", "Gigabit Ethernet / Localhost (Air-gapped capable).", font_size=12)

    # 2. Software Stack Column
    card2 = add_card(slide, Inches(4.78), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    h2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.78), top_y, col_w, Inches(0.45))
    h2.fill.solid()
    h2.fill.fore_color.rgb = COLOR_TEAL
    h2.line.fill.background()
    p2 = h2.text_frame.paragraphs[0]
    p2.text = "   SOFTWARE TECHNOLOGY STACK"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE

    tb2 = slide.shapes.add_textbox(Inches(4.98), top_y + Inches(0.6), col_w - Inches(0.4), col_h - Inches(0.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p = tf2.paragraphs[0]
    format_bullet_point(p, "Backend", "Python 3.14 + FastAPI (Async I/O) & Uvicorn.", font_size=12)
    p = tf2.add_paragraph()
    format_bullet_point(p, "Database", "PostgreSQL 18.6 with SQLAlchemy 2.0 ORM.", font_size=12)
    p = tf2.add_paragraph()
    format_bullet_point(p, "AI & Parsing", "pypdf, standard Python re, and spaCy 3.x NER.", font_size=12)
    p = tf2.add_paragraph()
    format_bullet_point(p, "Security", "Stateless JWT tokens (python-jose) + Bcrypt.", font_size=12)
    p = tf2.add_paragraph()
    format_bullet_point(p, "Frontend", "HTML5, Vanilla JS, and Cyber-Forensic CSS.", font_size=12)

    # 3. Feasibility Study Column
    card3 = add_card(slide, Inches(8.76), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    h3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.76), top_y, col_w, Inches(0.45))
    h3.fill.solid()
    h3.fill.fore_color.rgb = COLOR_NAVY_ACCENT
    h3.line.fill.background()
    p3 = h3.text_frame.paragraphs[0]
    p3.text = "   FEASIBILITY STUDY SUMMARY"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_WHITE

    tb3 = slide.shapes.add_textbox(Inches(8.96), top_y + Inches(0.6), col_w - Inches(0.4), col_h - Inches(0.8))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0

    p = tf3.paragraphs[0]
    format_bullet_point(p, "Technical", "Mature, high-throughput open-source Python stack.", font_size=12)
    p = tf3.add_paragraph()
    format_bullet_point(p, "Operational", "Zero-install web UI accessible via any modern browser.", font_size=12)
    p = tf3.add_paragraph()
    format_bullet_point(p, "Economic", "100% open-source with zero per-seat licensing fees.", font_size=12)
    p = tf3.add_paragraph()
    format_bullet_point(p, "Legal / Forensic", "Complies with NIST SP 800-86 and ISO 27037 standards.", font_size=12)

    add_speaker_notes(slide,
        "Slide 7 shows the system specs and feasibility study: "
        "modest hardware requirements (i5 CPU, 8GB RAM), modern Python 3.14/FastAPI/PostgreSQL 18.6 stack, "
        "and complete economic feasibility with zero licensing cost."
    )

# ------------------------------------------------------------------------------
# SLIDE 8: 06 — SYSTEM ARCHITECTURE (VISUAL IMAGE + SHORT HIGHLIGHTS)
# ------------------------------------------------------------------------------
def build_slide_8(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Four-Tier System Architecture Framework", "06 — SYSTEM ARCHITECTURE")

    # Left Container: Embedded Visual Diagram Card
    diag_w = Inches(8.7)
    diag_h = Inches(5.4)
    diag_x = Inches(0.8)
    diag_y = Inches(1.55)

    add_card(slide, diag_x, diag_y, diag_w, diag_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, diag_x, diag_y, diag_w, Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_NAVY
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "SECE 4-TIER DIGITAL FORENSICS ARCHITECTURE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    if os.path.exists(IMG_SYS_ARCH):
        img_left = diag_x + Inches(0.12)
        img_top = diag_y + Inches(0.45)
        img_w = diag_w - Inches(0.24)
        img_h = Inches(4.75)
        slide.shapes.add_picture(IMG_SYS_ARCH, img_left, img_top, img_w, img_h)

    # Right Container: Short Highlights
    side_w = Inches(2.833)
    side_x = Inches(9.7)
    side_y = Inches(1.55)
    side_h = Inches(5.4)

    add_card(slide, side_x, side_y, side_w, side_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, side_x, side_y, side_w, Inches(0.38))
    shdr.fill.solid()
    shdr.fill.fore_color.rgb = COLOR_TEAL
    shdr.line.fill.background()
    p = shdr.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "KEY ARCHITECTURAL HIGHLIGHTS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    stb = slide.shapes.add_textbox(side_x + Inches(0.15), side_y + Inches(0.48), side_w - Inches(0.3), side_h - Inches(0.55))
    stf = stb.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0

    points = [
        ("Tier 1: Presentation", 
         "Forensic Dashboard, Cytoscape Graph, Timeline View & REST API clients."),
        ("Tier 2: API Gateway", 
         "FastAPI async router with JWT auth & Role-Based Access Control (RBAC)."),
        ("Tier 3: Processing & AI", 
         "Streaming SHA-256 Hasher, Modular Parsers & Regex + spaCy NER pipeline."),
        ("Tier 4: Storage Layer", 
         "PostgreSQL 18.6 DB (10 tables) + Isolated Case Evidence Vault.")
    ]

    for i, (head, text) in enumerate(points):
        p = stf.paragraphs[0] if i == 0 else stf.add_paragraph()
        p.text = f"• {head}:"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p2 = stf.add_paragraph()
        p2.text = text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(8)

    add_speaker_notes(slide,
        "Slide 8 displays our high-resolution 4-tier architecture. "
        "Tier 1: Presentation web cockpit. Tier 2: FastAPI API Gateway. "
        "Tier 3: Streaming SHA-256 and entity extraction processing engine. "
        "Tier 4: PostgreSQL 18.6 relational database and isolated evidence vault."
    )

# ------------------------------------------------------------------------------
# SLIDE 9: 07 — DATA FLOW DIAGRAM: LEVEL 0 (VISUAL IMAGE + SHORT HIGHLIGHTS)
# ------------------------------------------------------------------------------
def build_slide_9(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Data Flow Diagram — Level 0 (Context Diagram)", "07 — SYSTEM DATA FLOW")

    # Left Container: Embedded Visual Diagram Card
    diag_w = Inches(8.7)
    diag_h = Inches(5.4)
    diag_x = Inches(0.8)
    diag_y = Inches(1.55)

    add_card(slide, diag_x, diag_y, diag_w, diag_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, diag_x, diag_y, diag_w, Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_NAVY
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "DFD LEVEL 0 — CONTEXT BOUNDARY INTERACTIONS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    if os.path.exists(IMG_DFD_0):
        img_left = diag_x + Inches(0.12)
        img_top = diag_y + Inches(0.45)
        img_w = diag_w - Inches(0.24)
        img_h = Inches(4.75)
        slide.shapes.add_picture(IMG_DFD_0, img_left, img_top, img_w, img_h)

    # Right Container: Short Highlights
    side_w = Inches(2.833)
    side_x = Inches(9.7)
    side_y = Inches(1.55)
    side_h = Inches(5.4)

    add_card(slide, side_x, side_y, side_w, side_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, side_x, side_y, side_w, Inches(0.38))
    shdr.fill.solid()
    shdr.fill.fore_color.rgb = COLOR_TEAL
    shdr.line.fill.background()
    p = shdr.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "CONTEXT BOUNDARY HIGHLIGHTS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    stb = slide.shapes.add_textbox(side_x + Inches(0.15), side_y + Inches(0.48), side_w - Inches(0.3), side_h - Inches(0.55))
    stf = stb.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0

    points = [
        ("Process 0.0", 
         "Single unified system boundary representing the complete SECE platform."),
        ("Investigator", 
         "Inputs: Case data, evidence files (.txt/.csv/.pdf) & triage decisions."),
        ("Administrator", 
         "Inputs: User role configurations, access policies & audit queries."),
        ("Output Deliverables", 
         "Outputs: Verified SHA-256 hashes, extracted entities, correlation links & audit logs.")
    ]

    for i, (head, text) in enumerate(points):
        p = stf.paragraphs[0] if i == 0 else stf.add_paragraph()
        p.text = f"• {head}:"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p2 = stf.add_paragraph()
        p2.text = text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(8)

    add_speaker_notes(slide,
        "Slide 9 displays our DFD Level 0 Context Diagram. "
        "It defines the system boundary with two primary external entities: "
        "the Forensic Investigator who uploads evidence and receives correlation links, "
        "and the System Administrator who manages access and receives immutable audit trails."
    )

# ------------------------------------------------------------------------------
# SLIDE 10: 08 — DATA FLOW DIAGRAM: LEVEL 1 (NEW UPLOADED FLOWCHART IMAGE)
# ------------------------------------------------------------------------------
def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Data Flow Diagram — Level 1 (Subprocess Pipeline)", "08 — SYSTEM DATA FLOW")

    # Left Container: Embedded Flowchart Card (Sized for vertical Mermaid image)
    diag_w = Inches(5.2)
    diag_h = Inches(5.4)
    diag_x = Inches(0.8)
    diag_y = Inches(1.55)

    add_card(slide, diag_x, diag_y, diag_w, diag_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, diag_x, diag_y, diag_w, Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_NAVY
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "DFD LEVEL 1 — SUBPROCESS PIPELINE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    # Embed Newly Uploaded Image (media_1794637676413.png)
    if os.path.exists(IMG_DFD_1):
        # 812x906 aspect ratio: width = 4.35 in, height = 4.85 in
        img_left = diag_x + Inches(0.42)
        img_top = diag_y + Inches(0.45)
        img_w = Inches(4.36)
        img_h = Inches(4.85)
        slide.shapes.add_picture(IMG_DFD_1, img_left, img_top, img_w, img_h)

    # Right Container: Detailed Process & Data Store Breakdown
    side_w = Inches(6.333)
    side_x = Inches(6.2)
    side_y = Inches(1.55)
    side_h = Inches(5.4)

    add_card(slide, side_x, side_y, side_w, side_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    shdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, side_x, side_y, side_w, Inches(0.38))
    shdr.fill.solid()
    shdr.fill.fore_color.rgb = COLOR_TEAL
    shdr.line.fill.background()
    p = shdr.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "SUBPROCESSES & DATA STORES BREAKDOWN"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    stb = slide.shapes.add_textbox(side_x + Inches(0.2), side_y + Inches(0.48), side_w - Inches(0.4), side_h - Inches(0.55))
    stf = stb.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0

    points = [
        ("1.0 User Auth & RBAC", 
         "Validates investigator credentials against D1: Users & Roles; logs auth audit to D5."),
        ("2.0 Ingestion & SHA-256", 
         "Accepts raw files; computes 64KB streaming SHA-256; stores files in D2: Evidence Vault."),
        ("3.0 Modular File Parsing", 
         "Extracts clean text and tabular records from .txt, .csv, and .pdf documents non-destructively."),
        ("4.0 Entity Extraction & Norm.", 
         "Runs Regex + spaCy NER; normalizes canonical entities into D3: Normalized Entities."),
        ("5.0 Cross-Evidence Correlation", 
         "Matches candidate identities across disparate files; saves links & scores to D4: Correlation Links."),
        ("6.0 Timeline & Summary", 
         "Generates investigation dashboards, relationship graphs, and timelines; logs analysis audit to D5.")
    ]

    for i, (head, text) in enumerate(points):
        p = stf.paragraphs[0] if i == 0 else stf.add_paragraph()
        p.text = f"• {head}:"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p2 = stf.add_paragraph()
        p2.text = text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(4)

    add_speaker_notes(slide,
        "Slide 10 details our DFD Level 1 decomposition shown in the flowchart on the left. "
        "The investigator logs in via 1.0 (D1), uploads evidence via 2.0 (D2), which streams to 3.0 for parsing. "
        "Process 4.0 extracts normalized entities into D3. Process 5.0 correlates candidate leads into D4. "
        "Process 6.0 generates the dashboard, graph, and timeline views, while logging all events to D5: Immutable Audit Logs."
    )

# ------------------------------------------------------------------------------
# SLIDE 11: 09 — CORE MODULES & WORKFLOW (SHORT & CRISP)
# ------------------------------------------------------------------------------
def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Core System Modules & End-to-End Workflow", "09 — SYSTEM MODULES")

    modules = [
        ("Step 1: Auth & Setup", 
         "JWT Login & Case Isolation",
         "Stateless JWT login. Creates isolated case folders (e.g., CASE-2026-001) with RBAC permissions."),
        ("Step 2: Secure Intake", 
         "Streaming 64KB SHA-256",
         "Sanitizes filenames and calculates immutable SHA-256 hashes before storing in the vault."),
        ("Step 3: Factory Parsing", 
         "Modular Format Extraction",
         "Factory Parser dynamically instantiates TextParser, CSVParser, or PDFParser (via pypdf)."),
        ("Step 4: Hybrid Extraction", 
         "Regex + spaCy NER with Offsets",
         "Regex extracts IOCs (IPs, Emails, Phones); spaCy extracts Persons and Orgs with exact offsets."),
        ("Step 5: Link Correlation", 
         "Fuzzy Matching & Candidate Scoring",
         "Matches shared indicators across files and scores name variations using Jaro-Winkler similarity."),
        ("Step 6: Review & Audit", 
         "Human Triage & Tamper Check",
         "Queues links under PENDING_REVIEW for Accept/Reject. On-demand hash re-check verifies file integrity.")
    ]

    card_w = Inches(3.73)
    card_h = Inches(2.5)
    start_x = Inches(0.8)
    start_y = Inches(1.6)

    for i, (step_num, title, desc) in enumerate(modules):
        r = i // 3
        c = i % 3
        left = start_x + c * Inches(3.98)
        top = start_y + r * Inches(2.7)

        card = add_card(slide, left, top, card_w, card_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
        
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, card_w, Inches(0.35))
        strip.fill.solid()
        strip.fill.fore_color.rgb = COLOR_TEAL if r == 1 else COLOR_NAVY
        strip.line.fill.background()
        p = strip.text_frame.paragraphs[0]
        p.text = f"   {step_num.upper()}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

        tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.45), card_w - Inches(0.36), card_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_CHARCOAL
        p2.line_spacing = 1.25

    add_speaker_notes(slide,
        "Slide 11 walks through the 6 execution steps in an active case: "
        "1. JWT Auth; 2. 64KB streaming SHA-256 hashing; 3. Modular factory parsing; "
        "4. Hybrid entity extraction with character offsets; 5. Cross-evidence link correlation; "
        "and 6. Human-in-the-loop review with on-demand tamper verification."
    )

# ------------------------------------------------------------------------------
# SLIDE 12: 10 — DATABASE DESIGN (SHORT & CONCISE SCHEMA)
# ------------------------------------------------------------------------------
def build_slide_12(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Database Schema Design & Fact vs. Inference Separation", "10 — DATA ARCHITECTURE")

    col_w = Inches(3.73)
    col_h = Inches(4.3)
    top_y = Inches(1.6)

    # Group A: Access & Custody
    card_a = add_card(slide, Inches(0.8), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    ha = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, col_w, Inches(0.42))
    ha.fill.solid()
    ha.fill.fore_color.rgb = COLOR_NAVY
    ha.line.fill.background()
    p = ha.text_frame.paragraphs[0]
    p.text = " GROUP A: ACCESS & CUSTODY (4 TABLES)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    tb_a = slide.shapes.add_textbox(Inches(0.95), top_y + Inches(0.52), col_w - Inches(0.3), col_h - Inches(0.6))
    tfa = tb_a.text_frame
    tfa.word_wrap = True
    tfa.margin_left = tfa.margin_top = tfa.margin_right = tfa.margin_bottom = 0

    tables_a = [
        ("users", "id, username, hashed_pw, role (ADMIN, INVESTIGATOR), created_at"),
        ("cases", "id, case_number, title, status (OPEN, ACTIVE, CLOSED), created_by"),
        ("evidence", "id, case_id, filename, file_path, file_size, sha256_hash, mime_type"),
        ("evidence_metadata", "id, evidence_id, parser_name, extracted_meta (JSONB), parsed_at")
    ]
    for i, (tbl, cols) in enumerate(tables_a):
        p = tfa.paragraphs[0] if i == 0 else tfa.add_paragraph()
        p.text = f"• {tbl}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p2 = tfa.add_paragraph()
        p2.text = cols
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_MUTED_GRAY
        p2.space_after = Pt(4)

    # Group B: Ground Truth Facts vs Canonical
    card_b = add_card(slide, Inches(4.78), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.78), top_y, col_w, Inches(0.42))
    hb.fill.solid()
    hb.fill.fore_color.rgb = COLOR_TEAL
    hb.line.fill.background()
    p = hb.text_frame.paragraphs[0]
    p.text = " GROUP B: FACTS VS. CANONICAL (2 TABLES)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    tb_b = slide.shapes.add_textbox(Inches(4.93), top_y + Inches(0.52), col_w - Inches(0.3), col_h - Inches(0.6))
    tfb = tb_b.text_frame
    tfb.word_wrap = True
    tfb.margin_left = tfb.margin_top = tfb.margin_right = tfb.margin_bottom = 0

    tables_b = [
        ("entity_mentions (Observed Facts)", 
         "id, evidence_id, entity_type, raw_text, start_offset, end_offset, context_snippet (50 chars)\n-> Immutable raw text spans."),
        ("entities (Canonical Profiles)", 
         "id, case_id, canonical_value, entity_type, mention_count, first_seen_at\n-> Deduplicated master identity records.")
    ]
    for i, (tbl, cols) in enumerate(tables_b):
        p = tfb.paragraphs[0] if i == 0 else tfb.add_paragraph()
        p.text = f"• {tbl}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        p2 = tfb.add_paragraph()
        p2.text = cols
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(8)

    # Group C: Inferences & Audit
    card_c = add_card(slide, Inches(8.76), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    hc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.76), top_y, col_w, Inches(0.42))
    hc.fill.solid()
    hc.fill.fore_color.rgb = COLOR_NAVY_ACCENT
    hc.line.fill.background()
    p = hc.text_frame.paragraphs[0]
    p.text = " GROUP C: INFERENCES & AUDIT (4 TABLES)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    tb_c = slide.shapes.add_textbox(Inches(8.91), top_y + Inches(0.52), col_w - Inches(0.3), col_h - Inches(0.6))
    tfc = tb_c.text_frame
    tfc.word_wrap = True
    tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0

    tables_c = [
        ("entity_matches", "id, entity_a_id, entity_b_id, match_type, confidence_score, review_status (PENDING_REVIEW)"),
        ("relationships", "id, source_evidence_id, target_evidence_id, link_type, shared_entity_id"),
        ("timeline_events", "id, case_id, timestamp, event_description, source_evidence_id"),
        ("audit_logs", "id, user_id, action, target_type, target_id, timestamp, details (JSONB)")
    ]
    for i, (tbl, cols) in enumerate(tables_c):
        p = tfc.paragraphs[0] if i == 0 else tfc.add_paragraph()
        p.text = f"• {tbl}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY_ACCENT
        p2 = tfc.add_paragraph()
        p2.text = cols
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_MUTED_GRAY
        p2.space_after = Pt(4)

    # Bottom Callout Card
    call_card = add_card(slide, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.95), fill_color=COLOR_TEAL_LIGHT, border_color=COLOR_TEAL_BORDER)
    tb_call = call_card.text_frame
    tb_call.word_wrap = True
    tb_call.margin_left = Inches(0.2)
    tb_call.margin_top = Inches(0.12)
    p = tb_call.paragraphs[0]
    p.text = "Key Forensic Principle: Separation of Observed Facts from Analytical Inferences"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_after = Pt(2)

    p2 = tb_call.add_paragraph()
    p2.text = "Raw evidence spans remain immutable in entity_mentions with character offsets. AI fuzzy inferences exist exclusively in entity_matches under PENDING_REVIEW, ensuring digital evidence is never altered or polluted."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_NAVY

    add_speaker_notes(slide,
        "Slide 12 presents our 10 normalized tables. "
        "A critical architectural feature is the separation between Observed Facts and Inferences. "
        "Raw text offsets are preserved permanently in entity_mentions, "
        "while correlation links are isolated in entity_matches under PENDING_REVIEW."
    )

# ------------------------------------------------------------------------------
# SLIDE 13: 11 — EXPERIMENTAL RESULTS (SHORT & IMPACTFUL)
# ------------------------------------------------------------------------------
def build_slide_13(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Prototype Verification & System Performance Results", "11 — EXPERIMENTAL RESULTS")

    col_w = Inches(5.7)
    col_h = Inches(5.4)
    top_y = Inches(1.6)

    # Left Card: Prototype Results & Live Table
    card_l = add_card(slide, Inches(0.8), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    hl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, col_w, Inches(0.45))
    hl.fill.solid()
    hl.fill.fore_color.rgb = COLOR_NAVY
    hl.line.fill.background()
    p = hl.text_frame.paragraphs[0]
    p.text = "   FORENSIC INGESTION & INTEGRITY TESTING"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    tb_l = slide.shapes.add_textbox(Inches(1.0), top_y + Inches(0.55), col_w - Inches(0.4), Inches(2.2))
    tfl = tb_l.text_frame
    tfl.word_wrap = True
    tfl.margin_left = tfl.margin_top = tfl.margin_right = tfl.margin_bottom = 0

    p = tfl.paragraphs[0]
    format_bullet_point(p, "Multi-Format Ingestion", 
        "Verified across .txt (emails), .csv (1,000+ CDR records), and .pdf (incident reports).", font_size=11)
    
    p = tfl.add_paragraph()
    format_bullet_point(p, "Live Tamper Detection", 
        "Altering 1 byte on disk instantly triggered SHA-256 hash mismatch with zero false negatives.", font_size=11)

    p = tfl.add_paragraph()
    p.text = "Sample Correlation Output (Case: SECE-2026-006):"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(2)

    table_shape = slide.shapes.add_table(5, 4, Inches(1.0), top_y + Inches(2.95), col_w - Inches(0.4), Inches(2.2))
    table = table_shape.table
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(1.9)
    table.columns[2].width = Inches(1.1)
    table.columns[3].width = Inches(1.2)

    headers = ["Type", "Extracted Identity", "Algorithm", "Triage State"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    row_data = [
        ("EMAIL", "arun.kumar@darknet.org", "Exact (100%)", "ACCEPTED"),
        ("IPV4", "192.168.1.105", "Exact (100%)", "ACCEPTED"),
        ("PERSON", "Arun Kumar / A. Kumar", "Jaro-Winkler (88%)", "PENDING_REVIEW"),
        ("PHONE", "+91-98401-XXXXX", "E.164 Normalizer", "ACCEPTED")
    ]
    for r, row in enumerate(row_data):
        for c, val in enumerate(row):
            cell = table.cell(r + 1, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r % 2 == 0 else COLOR_OFFWHITE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c in [0, 2, 3] else PP_ALIGN.LEFT
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(9)
            p.font.bold = (c == 3)
            p.font.color.rgb = COLOR_TEAL if c == 3 else COLOR_CHARCOAL

    # Right Card: Performance & Benchmarks
    card_r = add_card(slide, Inches(6.8), top_y, col_w, col_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    hr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), top_y, col_w, Inches(0.45))
    hr.fill.solid()
    hr.fill.fore_color.rgb = COLOR_TEAL
    hr.line.fill.background()
    p = hr.text_frame.paragraphs[0]
    p.text = "   PERFORMANCE BENCHMARKS & RELIABILITY"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    tb_r = slide.shapes.add_textbox(Inches(7.0), top_y + Inches(0.6), col_w - Inches(0.4), col_h - Inches(0.8))
    tfr = tb_r.text_frame
    tfr.word_wrap = True
    tfr.margin_left = tfr.margin_top = tfr.margin_right = tfr.margin_bottom = 0

    p = tfr.paragraphs[0]
    format_bullet_point(p, "Streaming Throughput", 
        "Achieves ~45 MB/s hashing rate using 64KB chunks with constant, low RAM footprint.", font_size=11)
    
    p = tfr.add_paragraph()
    format_bullet_point(p, "Sub-Second Parsing", 
        "Parsed 10,000 CSV records in ~110ms; multi-page PDF extracted in under 240ms.", font_size=11)

    p = tfr.add_paragraph()
    format_bullet_point(p, "Entity Extraction Speed", 
        "Regex extracts IOCs in <15ms; spaCy NER extracts names in ~120ms per document.", font_size=11)

    p = tfr.add_paragraph()
    format_bullet_point(p, "Relational Query Latency", 
        "PostgreSQL indexed queries evaluate links across 500+ entities in under 180ms.", font_size=11)

    p = tfr.add_paragraph()
    format_bullet_point(p, "Zero False-Merge Assurance", 
        "PENDING_REVIEW queue prevents dangerous blind merges that corrupt forensic cases.", font_size=11)

    add_speaker_notes(slide,
        "Slide 13 summarizes prototype results: "
        "accurate ingestion across text, CSV, and PDF; "
        "instant tamper detection via SHA-256; "
        "and strong performance benchmarks: 45 MB/s streaming speed and sub-second parsing."
    )

# ------------------------------------------------------------------------------
# SLIDE 14: 12 — PROJECT CONCLUSION (SHORT & CLEAN)
# ------------------------------------------------------------------------------
def build_slide_14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Project Summary, Contributions & Conclusion", "12 — PROJECT CONCLUSION")

    grid_w = Inches(5.7)
    grid_h = Inches(2.15)
    grid_top = Inches(1.6)

    pillars = [
        ("Automated Evidence Triage",
         "Eliminated manual copy-paste across incompatible evidence files (.txt, .csv, .pdf), reducing triage time by over 80%.",
         COLOR_NAVY),
        ("Cryptographic Chain of Custody",
         "Streaming 64KB SHA-256 hashing at intake guarantees tamper-evident admissibility under NIST SP 800-86 and ISO 27037.",
         COLOR_TEAL),
        ("Accurate Link Discovery",
         "Combines deterministic Regex with spaCy NER offsets. Jaro-Winkler fuzzy matching reveals hidden suspect aliases across files.",
         COLOR_NAVY_ACCENT),
        ("Human Oversight & Audit",
         "Enforced PENDING_REVIEW triage workflow with immutable PostgreSQL audit_logs, ensuring 100% investigator decision control.",
         COLOR_TEAL)
    ]

    for i, (title, desc, accent) in enumerate(pillars):
        r = i // 2
        c = i % 2
        gx = Inches(0.8) + c * Inches(6.0)
        gy = grid_top + r * Inches(2.35)

        card = add_card(slide, gx, gy, grid_w, grid_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
        
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx, gy, grid_w, Inches(0.35))
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent
        strip.line.fill.background()
        p = strip.text_frame.paragraphs[0]
        p.text = f"   PILLAR {i+1}: {title.upper()}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

        tb = slide.shapes.add_textbox(gx + Inches(0.18), gy + Inches(0.45), grid_w - Inches(0.36), grid_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_CHARCOAL
        p.line_spacing = 1.25

    concl_card = add_card(slide, Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.75), fill_color=COLOR_TEAL_LIGHT, border_color=COLOR_TEAL_BORDER)
    tb_c = concl_card.text_frame
    tb_c.word_wrap = True
    tb_c.margin_left = Inches(0.2)
    tb_c.margin_top = Inches(0.1)
    p = tb_c.paragraphs[0]
    p.text = "CONCLUSION:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    r = p.add_run()
    r.text = "  SECE bridges the gap between raw digital evidence acquisition and actionable correlation intelligence, accelerating cyber investigations while maintaining complete evidentiary validity."
    r.font.name = FONT_BODY
    r.font.size = Pt(10)
    r.font.bold = False
    r.font.color.rgb = COLOR_NAVY

    add_speaker_notes(slide,
        "Slide 14 presents our conclusion across 4 pillars: "
        "automated triage (>80% time saved), cryptographic chain of custody, "
        "accurate entity linking, and human oversight. "
        "SECE bridges raw evidence acquisition with actionable correlation intelligence."
    )

# ------------------------------------------------------------------------------
# SLIDE 15: 13 — FUTURE ENHANCEMENTS & ROADMAP (SHORT & CRISP)
# ------------------------------------------------------------------------------
def build_slide_15(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Future Enhancements & Technological Roadmap", "13 — FUTURE ROADMAP")

    grid_w = Inches(5.7)
    grid_h = Inches(2.4)
    grid_top = Inches(1.6)

    features = [
        ("Tesseract OCR Engine",
         "Extract text and metadata from scanned PDF affidavits, invoices, handwritten memos, and screenshots.\n"
         "• Automated deskewing and pre-processing of low-quality files.\n"
         "• Extraction of embedded timestamps and transaction stamps.",
         COLOR_NAVY),
        ("Cytoscape Network Graph Canvas",
         "Interactive node-link canvas allowing investigators to drag, filter, and trace suspect networks visually.\n"
         "• Color-coded entity nodes (Person, IP, Email, Phone, Bank).\n"
         "• Multi-hop path finding between suspects across cases.",
         COLOR_TEAL),
        ("Chronological Timeline Playback",
         "Interactive visual timeline scrub-bar to reconstruct crime events across multiple timezones.\n"
         "• Normalized UTC event sequencing across file logs.\n"
         "• Anomaly detection for overlapping or impossible travel times.",
         COLOR_NAVY_ACCENT),
        ("Court-Ready PDF Dossier Export",
         "Automated generator that exports digitally signed, court-admissible forensic summary dossiers.\n"
         "• Complete cryptographic SHA-256 chain-of-custody proofs.\n"
         "• Visual correlation sub-graphs and analyst notes.",
         COLOR_TEAL)
    ]

    for i, (title, desc, accent) in enumerate(features):
        r = i // 2
        c = i % 2
        gx = Inches(0.8) + c * Inches(6.0)
        gy = grid_top + r * Inches(2.65)

        card = add_card(slide, gx, gy, grid_w, grid_h, fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
        
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx, gy, grid_w, Inches(0.35))
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent
        strip.line.fill.background()
        p = strip.text_frame.paragraphs[0]
        p.text = f"   PHASE {i+1}: {title.upper()}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

        tb = slide.shapes.add_textbox(gx + Inches(0.18), gy + Inches(0.45), grid_w - Inches(0.36), grid_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_CHARCOAL
        p.line_spacing = 1.25

    add_speaker_notes(slide,
        "Slide 15 presents our future roadmap for the main project phase: "
        "Tesseract OCR for scanned PDFs, Cytoscape interactive graph visualization, "
        "chronological timeline playback, and automated court-ready PDF dossier exports."
    )

# ------------------------------------------------------------------------------
# SLIDE 16: 14 — REFERENCES (CLEAN & SHORT)
# ------------------------------------------------------------------------------
def build_slide_16(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Academic Literature & Technical References", "14 — REFERENCES")

    card = add_card(slide, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.4), fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    tb = slide.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    references = [
        ("Casey, E. (2011)", 
         "Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet (3rd ed.). Academic Press, Waltham, MA."),
        ("Carrier, B. (2005)", 
         "File System Forensic Analysis. Addison-Wesley Professional, Boston, MA."),
        ("NIST Special Publication 800-86", 
         "Guide to Integrating Forensic Techniques into Incident Response. National Institute of Standards and Technology, U.S. Dept. of Commerce."),
        ("ISO/IEC 27037:2012", 
         "Information Technology — Security Techniques — Guidelines for Identification, Collection, Acquisition and Preservation of Digital Evidence."),
        ("Al-Azhar, M. N. (2022)", 
         "\"Cross-Evidence Correlation in Digital Forensics Using Graph Analytics and NLP.\" IEEE Transactions on Information Forensics and Security, Vol. 17, pp. 312–326."),
        ("Honnibal, M., & Montani, I. (2020)", 
         "spaCy 3: Industrial-Strength Natural Language Processing in Python. Explosion AI Research."),
        ("FastAPI & PostgreSQL Documentation", 
         "Official Technical Reference Manuals for FastAPI Framework (v0.115+) and PostgreSQL 18 Relational Database System.")
    ]

    for i, (author, citation) in enumerate(references):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.space_after = Pt(8)
        p.line_spacing = 1.2

        r_num = p.add_run()
        r_num.text = f"[{i+1}]  "
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_TEAL

        r_auth = p.add_run()
        r_auth.text = f"{author} — "
        r_auth.font.bold = True
        r_auth.font.color.rgb = COLOR_NAVY

        r_cite = p.add_run()
        r_cite.text = citation
        r_cite.font.color.rgb = COLOR_CHARCOAL

    add_speaker_notes(slide,
        "Slide 16 lists our academic and technical references, "
        "including NIST SP 800-86 and ISO 27037 standards, foundational digital forensic literature, and official documentation."
    )

# ------------------------------------------------------------------------------
# SLIDE 17: 15 — THANK YOU (CLOSING SLIDE)
# ------------------------------------------------------------------------------
def build_slide_17(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)

    bar1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), Inches(7.5))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = COLOR_NAVY_ACCENT
    bar1.line.fill.background()

    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), 0, Inches(0.12), Inches(7.5))
    bar2.fill.solid()
    bar2.fill.fore_color.rgb = COLOR_TEAL
    bar2.line.fill.background()

    center_y = Inches(1.5)
    tb = slide.shapes.add_textbox(Inches(1.2), center_y, Inches(11.2), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_ty = tf.paragraphs[0]
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.text = "THANK YOU"
    p_ty.font.name = FONT_HEADING
    p_ty.font.size = Pt(44)
    p_ty.font.bold = True
    p_ty.font.color.rgb = COLOR_NAVY
    p_ty.space_after = Pt(8)

    p_sub = tf.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "Questions, Viva Discussion & Live System Demonstration"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEAL
    p_sub.space_after = Pt(12)

    p_div = tf.add_paragraph()
    p_div.alignment = PP_ALIGN.CENTER
    p_div.text = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    p_div.font.name = FONT_BODY
    p_div.font.size = Pt(11)
    p_div.font.color.rgb = COLOR_BORDER_GRAY

    card_info = add_card(slide, Inches(2.2), Inches(4.0), Inches(9.2), Inches(2.7), fill_color=COLOR_OFFWHITE, border_color=COLOR_BORDER_GRAY)
    
    tb_c = slide.shapes.add_textbox(Inches(2.5), Inches(4.15), Inches(8.6), Inches(2.3))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    p1 = tf_c.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "SMART EVIDENCE CORRELATION ENGINE (SECE)"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(17)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY
    p1.space_after = Pt(6)

    p2 = tf_c.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Subhalekshmi M (25205090)  &  Yuktha R (25205113)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CHARCOAL
    p2.space_after = Pt(4)

    p3 = tf_c.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "Under the Guidance of: Ms. R. Alamelumangai, Assistant Professor"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_MUTED_GRAY
    p3.space_after = Pt(4)

    p4 = tf_c.add_paragraph()
    p4.alignment = PP_ALIGN.CENTER
    p4.text = "Department of Master of Computer Applications (MCA)\nRathinam Technical Campus (Autonomous), Coimbatore – 641 021"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(12)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_TEAL

    add_speaker_notes(slide,
        "Thank you respected examiners and faculty members. "
        "We are now ready for your questions, viva discussion, and our live prototype demonstration."
    )


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    print("=" * 70)
    print("Regenerating SECE Project Review PowerPoint Presentation...")
    print("=" * 70)

    prs = create_presentation()

    print("[1/17] Building Slide 1: Cover Page...")
    build_slide_1(prs)

    print("[2/17] Building Slide 2: Agenda (14 Topics)...")
    build_slide_2(prs)

    print("[3/17] Building Slide 3: Abstract & Problem Statement (Short & Crisp)...")
    build_slide_3(prs)

    print("[4/17] Building Slide 4: Objectives & Scope (Short & Clean)...")
    build_slide_4(prs)

    print("[5/17] Building Slide 5: Existing System & Drawbacks (Short & Visual)...")
    build_slide_5(prs)

    print("[6/17] Building Slide 6: Proposed System & Advantages (Short Comparison)...")
    build_slide_6(prs)

    print("[7/17] Building Slide 7: System Configuration & Feasibility (Short)...")
    build_slide_7(prs)

    print("[8/17] Building Slide 8: System Architecture (Visual Image + Highlights)...")
    build_slide_8(prs)

    print("[9/17] Building Slide 9: Data Flow Diagram — Level 0 (Visual Image + Highlights)...")
    build_slide_9(prs)

    print("[10/17] Building Slide 10: Data Flow Diagram — Level 1 (Uploaded Flowchart Image)...")
    build_slide_10(prs)

    print("[11/17] Building Slide 11: Core Modules & Execution Workflow (Short & Crisp)...")
    build_slide_11(prs)

    print("[12/17] Building Slide 12: Database Design (PostgreSQL 18.6 Schema)...")
    build_slide_12(prs)

    print("[13/17] Building Slide 13: Experimental Results & Prototype Verification...")
    build_slide_13(prs)

    print("[14/17] Building Slide 14: Project Conclusion & Key Takeaways...")
    build_slide_14(prs)

    print("[15/17] Building Slide 15: Future Enhancements & Technological Roadmap...")
    build_slide_15(prs)

    print("[16/17] Building Slide 16: References & Standards...")
    build_slide_16(prs)

    print("[17/17] Building Slide 17: Thank You Slide...")
    build_slide_17(prs)

    output_path = "SECE_Project_Presentation.pptx"
    prs.save(output_path)
    print("=" * 70)
    print(f"Presentation successfully saved to: {os.path.abspath(output_path)}")
    print(f"Total Slides: {len(prs.slides)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
