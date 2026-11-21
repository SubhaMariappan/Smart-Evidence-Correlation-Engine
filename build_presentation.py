"""
Build PowerPoint presentation for:
SMART EVIDENCE CORRELATION ENGINE (SECE)
MCA Mini Project II (25EEC204) - Rathinam Technical Campus
"""

import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml

# ---------------------------------------------------------
# CONSTANTS & PALETTE (LIGHT THEME)
# ---------------------------------------------------------
COLOR_BG_WHITE       = RGBColor(255, 255, 255) # Pure White (#FFFFFF)
COLOR_NAVY_DARK      = RGBColor(15, 23, 42)    # #0F172A Deep Navy
COLOR_NAVY_MID       = RGBColor(30, 41, 59)    # #1E293B
COLOR_TEAL           = RGBColor(13, 148, 136)  # #0D9488 Vibrant Teal
COLOR_TEAL_DARK      = RGBColor(15, 118, 110)  # #0F766E
COLOR_TEAL_LIGHT     = RGBColor(240, 253, 250) # #F0FDFA Soft Mint
COLOR_SLATE_TEXT     = RGBColor(51, 65, 85)    # #334155 Main text
COLOR_SLATE_MUTED    = RGBColor(100, 116, 139) # #64748B Secondary / Muted
COLOR_CARD_BG        = RGBColor(248, 250, 252) # #F8FAFC Ice Blue/Gray
COLOR_CARD_BORDER    = RGBColor(226, 232, 240) # #E2E8F0 Subtle Border
COLOR_AMBER_BG       = RGBColor(254, 243, 199) # #FEF3C7 Soft Amber
COLOR_AMBER_TXT      = RGBColor(180, 83, 9)    # #B45309 Amber Text
COLOR_GREEN_BG       = RGBColor(209, 250, 229) # #D1FAE5 Soft Green
COLOR_GREEN_TXT      = RGBColor(4, 120, 87)    # #047857 Green Text
COLOR_BLUE_BG        = RGBColor(239, 246, 255) # #EFF6FF Soft Blue
COLOR_BLUE_TXT       = RGBColor(29, 78, 216)   # #1D4ED8 Blue Text

FONT_MAIN = "Segoe UI"
FONT_CODE = "Consolas"

# ---------------------------------------------------------
# HELPER FUNCTIONS FOR DRAWING & TEXT
# ---------------------------------------------------------

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_blank_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_WHITE
    return slide

def add_header(slide, kicker, title, subtitle):
    """Standard slide header with category kicker, main title, and context subtitle."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(Inches(0.8)), int(Inches(0.42)), int(Inches(0.6)), int(Inches(0.04)))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_TEAL
    line.line.fill.background()

    kicker_box = slide.shapes.add_textbox(int(Inches(0.8)), int(Inches(0.50)), int(Inches(11.7)), int(Inches(0.28)))
    tf_k = kicker_box.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = FONT_MAIN
    p_k.font.size = Pt(9.5)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_TEAL

    title_box = slide.shapes.add_textbox(int(Inches(0.8)), int(Inches(0.74)), int(Inches(11.7)), int(Inches(0.45)))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_MAIN
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    sub_box = slide.shapes.add_textbox(int(Inches(0.8)), int(Inches(1.22)), int(Inches(11.7)), int(Inches(0.35)))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle
    p_s.font.name = FONT_MAIN
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = COLOR_SLATE_MUTED

def add_footer(slide, current_slide, total_slides=13):
    """Subtle bottom footer bar."""
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(Inches(0.8)), int(Inches(6.92)), int(Inches(11.733)), int(Inches(0.015)))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_CARD_BORDER
    div.line.fill.background()

    box_l = slide.shapes.add_textbox(int(Inches(0.8)), int(Inches(6.98)), int(Inches(8.0)), int(Inches(0.3)))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "SMART EVIDENCE CORRELATION ENGINE (SECE)  •  MCA MINI PROJECT II (25EEC204)"
    p_l.font.name = FONT_MAIN
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = COLOR_SLATE_MUTED

    box_r = slide.shapes.add_textbox(int(Inches(10.533)), int(Inches(6.98)), int(Inches(2.0)), int(Inches(0.3)))
    tf_r = box_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"{current_slide:02d} / {total_slides:02d}"
    p_r.font.name = FONT_MAIN
    p_r.font.size = Pt(8.5)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_TEAL

def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, border_width=1.0, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
    card = slide.shapes.add_shape(shape_type, int(left), int(top), int(width), int(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_arrow_head(connector):
    ln = connector.line._ln
    head = parse_xml('<a:headEnd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" type="triangle" w="med" len="med"/>')
    ln.append(head)

def draw_straight_arrow(slide, start_x, start_y, end_x, end_y, color=COLOR_TEAL, width=1.5):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, int(start_x), int(start_y), int(end_x), int(end_y))
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    add_arrow_head(conn)
    return conn

def draw_badge(slide, left, top, width, height, text, bg_color, text_color, font_size=9, bold=True):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, int(left), int(top), int(width), int(height))
    pill.fill.solid()
    pill.fill.fore_color.rgb = bg_color
    pill.line.fill.background()
    tf = pill.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text
    p.font.name = FONT_MAIN
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    return pill

# ---------------------------------------------------------
# SLIDE BUILDERS
# ---------------------------------------------------------

def build_slide_1(prs):
    """Slide 1: Front Page (Separate Cover Slide)"""
    slide = add_blank_slide(prs)

    # Decorative left accent bars
    bar1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, int(Inches(0.35)), int(Inches(7.5)))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = COLOR_NAVY_DARK
    bar1.line.fill.background()

    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(Inches(0.35)), 0, int(Inches(0.12)), int(Inches(7.5)))
    bar2.fill.solid()
    bar2.fill.fore_color.rgb = COLOR_TEAL
    bar2.line.fill.background()

    content_left = Inches(1.2)

    # Institutional Header
    inst_box = slide.shapes.add_textbox(int(content_left), int(Inches(0.6)), int(Inches(11.3)), int(Inches(0.9)))
    tf_inst = inst_box.text_frame
    tf_inst.word_wrap = True
    tf_inst.margin_left = tf_inst.margin_top = tf_inst.margin_right = tf_inst.margin_bottom = 0

    p0 = tf_inst.paragraphs[0]
    p0.text = "RATHINAM TECHNICAL CAMPUS (AUTONOMOUS)"
    p0.font.name = FONT_MAIN
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_NAVY_DARK

    p1 = tf_inst.add_paragraph()
    p1.text = "Department of Master of Computer Applications  |  Coimbatore – 641 021"
    p1.font.name = FONT_MAIN
    p1.font.size = Pt(11)
    p1.font.color.rgb = COLOR_SLATE_MUTED

    p2 = tf_inst.add_paragraph()
    p2.text = "Mini Project II Evaluation  •  Academic Session: May – 2026"
    p2.font.name = FONT_MAIN
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEAL

    # Thin divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(content_left), int(Inches(1.65)), int(Inches(11.3)), int(Inches(0.015)))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_CARD_BORDER
    div.line.fill.background()

    # Course Pill
    draw_badge(slide, content_left, Inches(1.95), Inches(3.2), Inches(0.32), "COURSE CODE: 25EEC204", COLOR_TEAL_LIGHT, COLOR_TEAL_DARK, font_size=10, bold=True)

    # Main Project Title
    title_box = slide.shapes.add_textbox(int(content_left), int(Inches(2.45)), int(Inches(11.3)), int(Inches(1.5)))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0

    pt0 = tf_title.paragraphs[0]
    pt0.text = "SMART EVIDENCE CORRELATION ENGINE (SECE)"
    pt0.font.name = FONT_MAIN
    pt0.font.size = Pt(28)
    pt0.font.bold = True
    pt0.font.color.rgb = COLOR_NAVY_DARK

    pt1 = tf_title.add_paragraph()
    pt1.text = "AI-Powered Digital Forensics & Multi-Source Evidence Correlation Platform"
    pt1.font.name = FONT_MAIN
    pt1.font.size = Pt(15)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_TEAL

    pt2 = tf_title.add_paragraph()
    pt2.text = "Streaming 64KB Forensic Integrity  •  Multi-Format Ingestion  •  Hybrid NLP Link Discovery"
    pt2.font.name = FONT_MAIN
    pt2.font.size = Pt(11)
    pt2.font.color.rgb = COLOR_SLATE_MUTED

    # Two Bottom Cards for Candidate & Guide Details
    card_w = Inches(5.5)
    card_h = Inches(2.5)
    top_pos = Inches(4.3)

    # Candidate Card
    create_card(slide, content_left, top_pos, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    strip1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(content_left), int(top_pos), int(card_w), int(Inches(0.06)))
    strip1.fill.solid()
    strip1.fill.fore_color.rgb = COLOR_NAVY_DARK
    strip1.line.fill.background()

    cand_box = slide.shapes.add_textbox(int(content_left + Inches(0.3)), int(top_pos + Inches(0.25)), int(card_w - Inches(0.6)), int(card_h - Inches(0.4)))
    tf_c = cand_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    pc0 = tf_c.paragraphs[0]
    pc0.text = "SUBMITTED BY (STUDENTS):"
    pc0.font.name = FONT_MAIN
    pc0.font.size = Pt(10)
    pc0.font.bold = True
    pc0.font.color.rgb = COLOR_TEAL

    pc1 = tf_c.add_paragraph()
    pc1.text = "1. SUBHALEKSHMI M"
    pc1.font.name = FONT_MAIN
    pc1.font.size = Pt(13)
    pc1.font.bold = True
    pc1.font.color.rgb = COLOR_NAVY_DARK

    pc1_sub = tf_c.add_paragraph()
    pc1_sub.text = "    Register Number: 25205090"
    pc1_sub.font.name = FONT_CODE
    pc1_sub.font.size = Pt(10.5)
    pc1_sub.font.color.rgb = COLOR_SLATE_TEXT

    pc2 = tf_c.add_paragraph()
    pc2.text = "2. YUKTHA R"
    pc2.font.name = FONT_MAIN
    pc2.font.size = Pt(13)
    pc2.font.bold = True
    pc2.font.color.rgb = COLOR_NAVY_DARK

    pc2_sub = tf_c.add_paragraph()
    pc2_sub.text = "    Register Number: 25205113"
    pc2_sub.font.name = FONT_CODE
    pc2_sub.font.size = Pt(10.5)
    pc2_sub.font.color.rgb = COLOR_SLATE_TEXT

    # Guide Card
    guide_left = content_left + card_w + Inches(0.3)
    create_card(slide, guide_left, top_pos, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    strip2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(guide_left), int(top_pos), int(card_w), int(Inches(0.06)))
    strip2.fill.solid()
    strip2.fill.fore_color.rgb = COLOR_TEAL
    strip2.line.fill.background()

    guide_box = slide.shapes.add_textbox(int(guide_left + Inches(0.3)), int(top_pos + Inches(0.25)), int(card_w - Inches(0.6)), int(card_h - Inches(0.4)))
    tf_g = guide_box.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = tf_g.margin_top = tf_g.margin_right = tf_g.margin_bottom = 0

    pg0 = tf_g.paragraphs[0]
    pg0.text = "PROJECT SUPERVISION:"
    pg0.font.name = FONT_MAIN
    pg0.font.size = Pt(10)
    pg0.font.bold = True
    pg0.font.color.rgb = COLOR_TEAL

    pg1 = tf_g.add_paragraph()
    pg1.text = "Ms. R. ALAMELUMANGAI"
    pg1.font.name = FONT_MAIN
    pg1.font.size = Pt(13)
    pg1.font.bold = True
    pg1.font.color.rgb = COLOR_NAVY_DARK

    pg1_sub = tf_g.add_paragraph()
    pg1_sub.text = "Assistant Professor, Dept. of Computer Applications"
    pg1_sub.font.name = FONT_MAIN
    pg1_sub.font.size = Pt(10.5)
    pg1_sub.font.color.rgb = COLOR_SLATE_TEXT

    pg2 = tf_g.add_paragraph()
    pg2.text = "Rathinam Technical Campus (Autonomous), Coimbatore"
    pg2.font.name = FONT_MAIN
    pg2.font.size = Pt(10)
    pg2.font.color.rgb = COLOR_SLATE_MUTED

    pg3 = tf_g.add_paragraph()
    pg3.text = "Degree: Master of Computer Applications (MCA)"
    pg3.font.name = FONT_MAIN
    pg3.font.size = Pt(10)
    pg3.font.bold = True
    pg3.font.color.rgb = COLOR_TEAL_DARK


def build_slide_2(prs):
    """Slide 2: Abstract & Overview"""
    slide = add_blank_slide(prs)
    add_header(slide, "Executive Summary", "Abstract & Project Overview",
               "A forensic triage engine unifying heterogeneous evidence files while maintaining strict chain-of-custody.")
    add_footer(slide, 2)

    card_w = Inches(5.7)
    card_h = Inches(2.35)
    row1_y = Inches(1.8)
    row2_y = Inches(4.35)
    col1_x = Inches(0.8)
    col2_x = Inches(6.833)

    cards_data = [
        (col1_x, row1_y, "01", "The Forensic Challenge", "DATA FRAGMENTATION",
         COLOR_NAVY_DARK, [
             ("Scattered Evidence:", "Cyber incidents produce massive, isolated files (emails, CDRs, PDFs)."),
             ("Tool Silos:", "Data sits in proprietary formats without cross-file querying."),
             ("Cognitive Overload:", "Manual cross-referencing causes critical links to be overlooked.")
         ]),
        (col2_x, row1_y, "02", "Our Solution (SECE)", "CENTRALIZED PLATFORM",
         COLOR_TEAL, [
             ("Unified Web Hub:", "Centralized platform to store, parse, and analyze multi-source files."),
             ("Factory Parsers:", "Extensible modular parsers for .txt, .csv, and .pdf formats."),
             ("Rapid Triage:", "Transforms unstructured dumps into structured, correlated intelligence.")
         ]),
        (col1_x, row2_y, "03", "Forensic Integrity", "STREAMING HASHING",
         COLOR_TEAL, [
             ("64KB SHA-256:", "Streaming cryptographic checksum locked immediately upon file upload."),
             ("Zero RAM Bloat:", "Constant low memory footprint even for gigabyte-sized evidence files."),
             ("Tamper Detection:", "Real-time disk re-verification catches any unauthorized byte alteration.")
         ]),
        (col2_x, row2_y, "04", "Smart Correlation", "HYBRID AI & NLP",
         COLOR_NAVY_DARK, [
             ("Deterministic Regex:", "Instantly extracts structured emails, IPv4 addresses, and phone numbers."),
             ("spaCy NER Engine:", "Identifies named individuals and suspects within narrative text."),
             ("Jaro-Winkler Matching:", "Surfaces hidden identity aliases with human-in-the-loop validation.")
         ]),
    ]

    for left, top, num, title, badge_text, accent_color, bullets in cards_data:
        create_card(slide, left, top, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(left), int(top), int(card_w), int(Inches(0.05)))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.fill.background()

        draw_badge(slide, left + Inches(0.25), top + Inches(0.18), Inches(1.8), Inches(0.24), badge_text, COLOR_TEAL_LIGHT, COLOR_TEAL_DARK, font_size=8, bold=True)

        num_box = slide.shapes.add_textbox(int(left + card_w - Inches(0.9)), int(top + Inches(0.12)), int(Inches(0.7)), int(Inches(0.35)))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.alignment = PP_ALIGN.RIGHT
        pn.text = num
        pn.font.name = FONT_MAIN
        pn.font.size = Pt(14)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_SLATE_MUTED

        tb = slide.shapes.add_textbox(int(left + Inches(0.25)), int(top + Inches(0.48)), int(card_w - Inches(0.5)), int(Inches(0.35)))
        tf_t = tb.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        pt = tf_t.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_MAIN
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY_DARK

        bb = slide.shapes.add_textbox(int(left + Inches(0.25)), int(top + Inches(0.85)), int(card_w - Inches(0.5)), int(card_h - Inches(0.95)))
        tf_b = bb.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

        for idx, (label, desc) in enumerate(bullets):
            p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            p.space_after = Pt(4)
            run1 = p.add_run()
            run1.text = "• " + label + " "
            run1.font.name = FONT_MAIN
            run1.font.size = Pt(10)
            run1.font.bold = True
            run1.font.color.rgb = COLOR_NAVY_DARK

            run2 = p.add_run()
            run2.text = desc
            run2.font.name = FONT_MAIN
            run2.font.size = Pt(9.5)
            run2.font.color.rgb = COLOR_SLATE_TEXT


def build_slide_3(prs):
    """Slide 3: Problem Statement & Objectives"""
    slide = add_blank_slide(prs)
    add_header(slide, "Research Motivation", "Problem Statement & Project Objectives",
               "Bridging critical gaps in current forensic investigations with automated intelligence.")
    add_footer(slide, 3)

    card_w = Inches(5.7)
    card_h = Inches(4.8)
    top_y = Inches(1.8)

    # Left Card: Problem Statement
    left_x = Inches(0.8)
    create_card(slide, left_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(left_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_l.fill.solid()
    bar_l.fill.fore_color.rgb = RGBColor(225, 29, 72)
    bar_l.line.fill.background()

    draw_badge(slide, left_x + Inches(0.3), top_y + Inches(0.2), Inches(2.2), Inches(0.26), "INVESTIGATIVE BOTTLENECK", RGBColor(255, 241, 242), RGBColor(225, 29, 72), font_size=8.5, bold=True)

    title_l = slide.shapes.add_textbox(int(left_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(Inches(0.4)))
    tf_tl = title_l.text_frame
    tf_tl.margin_left = tf_tl.margin_top = tf_tl.margin_right = tf_tl.margin_bottom = 0
    p_tl = tf_tl.paragraphs[0]
    p_tl.text = "Current Investigation Challenges"
    p_tl.font.name = FONT_MAIN
    p_tl.font.size = Pt(15)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_NAVY_DARK

    prob_items = [
        ("Isolated Evidence Silos", "Data resides in disconnected formats (Call logs, emails, PDFs, CSVs) across separate analyst workstations."),
        ("Manual Cross-Referencing", "Analysts spend days copying identifiers into spreadsheets; slow, fatiguing, and highly prone to human error."),
        ("Hidden Multi-Hop Links", "Indirect links across files (e.g. an email address in an invoice linking to a phone in a CDR) are easily missed."),
        ("Chain-of-Custody Hazards", "Manual handling and scattered file copies risk unintentional modification, jeopardizing legal courtroom admissibility.")
    ]

    p_y = top_y + Inches(1.05)
    for title, desc in prob_items:
        create_card(slide, left_x + Inches(0.3), p_y, card_w - Inches(0.6), Inches(0.8), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER, border_width=0.8)
        tb = slide.shapes.add_textbox(int(left_x + Inches(0.45)), int(p_y + Inches(0.1)), int(card_w - Inches(0.9)), int(Inches(0.6)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.text = "✕  " + title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(225, 29, 72)
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(9)
        p1.font.color.rgb = COLOR_SLATE_TEXT
        p_y += Inches(0.88)

    # Right Card: Key Objectives
    right_x = Inches(6.833)
    create_card(slide, right_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(right_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_r.fill.solid()
    bar_r.fill.fore_color.rgb = COLOR_TEAL
    bar_r.line.fill.background()

    draw_badge(slide, right_x + Inches(0.3), top_y + Inches(0.2), Inches(2.0), Inches(0.26), "PROPOSED SECE OBJECTIVES", COLOR_TEAL_LIGHT, COLOR_TEAL_DARK, font_size=8.5, bold=True)

    title_r = slide.shapes.add_textbox(int(right_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(Inches(0.4)))
    tf_tr = title_r.text_frame
    tf_tr.margin_left = tf_tr.margin_top = tf_tr.margin_right = tf_tr.margin_bottom = 0
    p_tr = tf_tr.paragraphs[0]
    p_tr.text = "Target Engineering Objectives"
    p_tr.font.name = FONT_MAIN
    p_tr.font.size = Pt(15)
    p_tr.font.bold = True
    p_tr.font.color.rgb = COLOR_NAVY_DARK

    obj_items = [
        ("Centralized Cryptographic Vault", "Safely store heterogeneous evidence files with streaming 64KB SHA-256 locking upon initial upload."),
        ("Automated Multi-Format Parsing", "Implement extensible factory parsers for .txt, .csv, and .pdf files to automatically extract text and metadata."),
        ("Hybrid AI Entity Extraction", "Harness deterministic Regex for emails, IPs, and phones, combined with spaCy NER for semantic person names."),
        ("Scored Cross-File Correlation", "Algorithmic matching (Exact + Jaro-Winkler) surfaces hidden links with human-in-the-loop review queues.")
    ]

    o_y = top_y + Inches(1.05)
    for title, desc in obj_items:
        create_card(slide, right_x + Inches(0.3), o_y, card_w - Inches(0.6), Inches(0.8), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER, border_width=0.8)
        tb = slide.shapes.add_textbox(int(right_x + Inches(0.45)), int(o_y + Inches(0.1)), int(card_w - Inches(0.9)), int(Inches(0.6)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.text = "✓  " + title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_TEAL
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(9)
        p1.font.color.rgb = COLOR_SLATE_TEXT
        o_y += Inches(0.88)


def build_slide_4(prs):
    """Slide 4: Existing System vs. Proposed System (SECE)"""
    slide = add_blank_slide(prs)
    add_header(slide, "Comparative Analysis", "Existing Forensic Workflow vs. Proposed System (SECE)",
               "Direct evaluation demonstrating significant improvements in efficiency, integrity, and link discovery.")
    add_footer(slide, 4)

    table_left = Inches(0.8)
    table_top = Inches(1.8)
    table_w = Inches(11.733)
    table_h = Inches(4.7)

    rows = 5
    cols = 4
    col_widths = [Inches(2.2), Inches(3.6), Inches(3.7), Inches(2.233)]

    table_shape = slide.shapes.add_table(rows, cols, int(table_left), int(table_top), int(table_w), int(table_h))
    table = table_shape.table

    for i, w in enumerate(col_widths):
        table.columns[i].width = int(w)

    headers = ["Forensic Dimension", "Existing System (Manual / Siloed)", "Proposed System (SECE Engine)", "Forensic Advantage"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_DARK
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.12)
        tf.margin_bottom = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_MAIN
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_BG_WHITE

    comparison_data = [
        ("Evidence Storage & Vaulting",
         "Scattered across local desktop folders, external drives, and disparate tools; high risk of misplacement.",
         "Centralized isolated Evidence Vault; strict case containers and role-based permissions.",
         "Single source of truth; zero misplaced evidence."),
        ("Chain-of-Custody & Integrity",
         "Manual or external checksum tools (md5sum); often skipped under time pressure.",
         "Automated 64KB streaming SHA-256 computed on upload; continuous re-hashing verification.",
         "Tamper-proof integrity guaranteed for court."),
        ("Entity Extraction & Analysis",
         "Manual spreadsheet searching, visual skimming, and repetitive copy-pasting.",
         "Automated hybrid extraction: Regex (Email, IP, Phone) + spaCy NER (Person names).",
         "10x faster triage; eliminates human fatigue."),
        ("Cross-File Link Discovery",
         "Blind manual merging or mental notes; non-obvious indirect leads completely missed.",
         "Algorithmic correlation engine (Exact & Jaro-Winkler) with non-destructive PENDING_REVIEW.",
         "High correlation recall with analyst oversight.")
    ]

    for row_idx, row_data in enumerate(comparison_data, start=1):
        bg_col = COLOR_CARD_BG if row_idx % 2 == 1 else COLOR_BG_WHITE

        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.15)
            tf.margin_right = Inches(0.15)
            tf.margin_top = Inches(0.12)
            tf.margin_bottom = Inches(0.12)
            p = tf.paragraphs[0]
            p.text = text
            p.font.name = FONT_MAIN

            if col_idx == 0:
                p.font.size = Pt(10.5)
                p.font.bold = True
                p.font.color.rgb = COLOR_NAVY_DARK
            elif col_idx == 1:
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_SLATE_TEXT
            elif col_idx == 2:
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_NAVY_DARK
                p.font.bold = True
            else:
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_TEAL_DARK
                p.font.bold = True


def build_slide_5(prs):
    """Slide 5: System Architecture Diagram (Dedicated Visual Slide)"""
    slide = add_blank_slide(prs)
    add_header(slide, "System Architecture", "SECE 4-Tier Modular System Architecture",
               "Clean horizontal tier decomposition ensuring loose coupling, high cohesion, and scalable forensics.")
    add_footer(slide, 5)

    base_x = Inches(0.8)
    base_w = Inches(11.733)

    # Tier 1: Presentation Layer
    t1_y = Inches(1.75)
    t1_h = Inches(0.9)
    create_card(slide, base_x, t1_y, base_w, t1_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    draw_badge(slide, base_x + Inches(0.15), t1_y + Inches(0.1), Inches(2.4), Inches(0.24), "TIER 1: PRESENTATION LAYER", COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=8, bold=True)

    t1_items = ["Case Manager", "Evidence Vault", "Entity Explorer", "Correlation Hub", "Audit Inspector"]
    sub_w = Inches(1.75)
    sub_h = Inches(0.4)
    start_sub_x = base_x + Inches(2.7)
    gap_x = Inches(0.1)
    for idx, item in enumerate(t1_items):
        cx = start_sub_x + idx * (sub_w + gap_x)
        create_card(slide, cx, t1_y + Inches(0.38), sub_w, sub_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
        tb = slide.shapes.add_textbox(int(cx), int(t1_y + Inches(0.38)), int(sub_w), int(sub_h))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = item
        p.font.name = FONT_MAIN
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY_DARK

    # Arrow 1: Tier 1 -> Tier 2
    a1_y = t1_y + t1_h
    arrow1 = draw_straight_arrow(slide, Inches(6.666), a1_y, Inches(6.666), a1_y + Inches(0.35), color=COLOR_TEAL, width=1.5)
    lbl1 = slide.shapes.add_textbox(int(Inches(3.5)), int(a1_y + Inches(0.05)), int(Inches(6.333)), int(Inches(0.25)))
    tf1 = lbl1.text_frame
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    p1 = tf1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "REST API (JSON Payload / Bearer JWT Authentication)"
    p1.font.name = FONT_CODE
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEAL_DARK

    # Tier 2: Application Layer
    t2_y = a1_y + Inches(0.35)
    t2_h = Inches(0.9)
    create_card(slide, base_x, t2_y, base_w, t2_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    draw_badge(slide, base_x + Inches(0.15), t2_y + Inches(0.1), Inches(2.4), Inches(0.24), "TIER 2: APPLICATION & ROUTING", COLOR_TEAL, COLOR_BG_WHITE, font_size=8, bold=True)
    t2_items = ["Auth Router (Bcrypt / JWT)", "Case Router (Isolation)", "Evidence Router (Uploads)", "Correlation Router (Triage)"]
    sub_w2 = Inches(2.15)
    start_sub2_x = base_x + Inches(2.7)
    gap_x2 = Inches(0.1)
    for idx, item in enumerate(t2_items):
        cx = start_sub2_x + idx * (sub_w2 + gap_x2)
        create_card(slide, cx, t2_y + Inches(0.38), sub_w2, sub_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
        tb = slide.shapes.add_textbox(int(cx), int(t2_y + Inches(0.38)), int(sub_w2), int(sub_h))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = item
        p.font.name = FONT_MAIN
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY_DARK

    # Arrow 2: Tier 2 -> Tier 3
    a2_y = t2_y + t2_h
    arrow2 = draw_straight_arrow(slide, Inches(6.666), a2_y, Inches(6.666), a2_y + Inches(0.35), color=COLOR_TEAL, width=1.5)
    lbl2 = slide.shapes.add_textbox(int(Inches(3.5)), int(a2_y + Inches(0.05)), int(Inches(6.333)), int(Inches(0.25)))
    tf2 = lbl2.text_frame
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Modular Asynchronous Service Invocations"
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEAL_DARK

    # Tier 3: Processing & AI Layer
    t3_y = a2_y + Inches(0.35)
    t3_h = Inches(1.0)
    create_card(slide, base_x, t3_y, base_w, t3_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    draw_badge(slide, base_x + Inches(0.15), t3_y + Inches(0.1), Inches(2.4), Inches(0.24), "TIER 3: FORENSIC AI & NLP", COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=8, bold=True)

    t3_steps = [
        ("SHA-256 Hasher", "Streaming 64KB Chunks"),
        ("Factory Parsers", ".txt / .csv / .pdf"),
        ("Hybrid Extractor", "Regex + spaCy NER"),
        ("Correlation Engine", "Jaro-Winkler Matching")
    ]
    step_w = Inches(1.95)
    step_gap = Inches(0.4)
    start_step_x = base_x + Inches(2.65)
    for idx, (title, sub) in enumerate(t3_steps):
        cx = start_step_x + idx * (step_w + step_gap)
        create_card(slide, cx, t3_y + Inches(0.22), step_w, Inches(0.68), bg_color=COLOR_BG_WHITE, border_color=COLOR_TEAL, border_width=1.0)
        tb = slide.shapes.add_textbox(int(cx), int(t3_y + Inches(0.26)), int(step_w), int(Inches(0.6)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        p0.text = title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.text = sub
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(8)
        p1.font.color.rgb = COLOR_SLATE_MUTED

        if idx < len(t3_steps) - 1:
            arr_x = cx + step_w
            draw_straight_arrow(slide, arr_x, t3_y + Inches(0.56), arr_x + step_gap, t3_y + Inches(0.56), color=COLOR_TEAL, width=1.5)

    # Arrow 3: Tier 3 -> Tier 4
    a3_y = t3_y + t3_h
    arrow3 = draw_straight_arrow(slide, Inches(6.666), a3_y, Inches(6.666), a3_y + Inches(0.35), color=COLOR_TEAL, width=1.5)
    lbl3 = slide.shapes.add_textbox(int(Inches(3.5)), int(a3_y + Inches(0.05)), int(Inches(6.333)), int(Inches(0.25)))
    tf3 = lbl3.text_frame
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
    p3 = tf3.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "SQLAlchemy 2.0 Async ORM  •  Direct Vault File IO"
    p3.font.name = FONT_CODE
    p3.font.size = Pt(8.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEAL_DARK

    # Tier 4: Persistence Layer
    t4_y = a3_y + Inches(0.35)
    t4_h = Inches(0.85)

    db_w = Inches(5.75)
    create_card(slide, base_x, t4_y, db_w, t4_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    draw_badge(slide, base_x + Inches(0.15), t4_y + Inches(0.1), Inches(2.2), Inches(0.22), "POSTGRESQL 18.6 RDBMS", COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=8, bold=True)
    tb_db = slide.shapes.add_textbox(int(base_x + Inches(0.2)), int(t4_y + Inches(0.38)), int(db_w - Inches(0.4)), int(Inches(0.4)))
    tf_db = tb_db.text_frame
    tf_db.word_wrap = True
    tf_db.margin_left = tf_db.margin_top = tf_db.margin_right = tf_db.margin_bottom = 0
    pdb = tf_db.paragraphs[0]
    pdb.text = "10 Normalized Tables: users, cases, evidence, metadata, entities, matches..."
    pdb.font.name = FONT_MAIN
    pdb.font.size = Pt(9)
    pdb.font.color.rgb = COLOR_SLATE_TEXT

    vault_x = base_x + db_w + Inches(0.233)
    create_card(slide, vault_x, t4_y, db_w, t4_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    draw_badge(slide, vault_x + Inches(0.15), t4_y + Inches(0.1), Inches(2.2), Inches(0.22), "ISOLATED EVIDENCE VAULT", COLOR_TEAL, COLOR_BG_WHITE, font_size=8, bold=True)
    tb_vt = slide.shapes.add_textbox(int(vault_x + Inches(0.2)), int(t4_y + Inches(0.38)), int(db_w - Inches(0.4)), int(Inches(0.4)))
    tf_vt = tb_vt.text_frame
    tf_vt.word_wrap = True
    tf_vt.margin_left = tf_vt.margin_top = tf_vt.margin_right = tf_vt.margin_bottom = 0
    pvt = tf_vt.paragraphs[0]
    pvt.text = "Immutable disk directory; SHA-256 locked storage with UUID keys and read-only flags."
    pvt.font.name = FONT_MAIN
    pvt.font.size = Pt(9)
    pvt.font.color.rgb = COLOR_SLATE_TEXT


def build_slide_6(prs):
    """Slide 6: Data Flow Diagram — Level 0 (Dedicated Context Diagram)"""
    slide = add_blank_slide(prs)
    add_header(slide, "System Data Flow", "Data Flow Diagram — Level 0 (Context Diagram)",
               "High-level system boundary illustrating external investigator roles and bi-directional forensic data exchanges.")
    add_footer(slide, 6)

    top_diagram = Inches(2.0)

    # 1. Left Actor: Investigator
    inv_x = Inches(0.8)
    inv_y = top_diagram + Inches(0.5)
    inv_w = Inches(2.4)
    inv_h = Inches(3.2)
    create_card(slide, inv_x, inv_y, inv_w, inv_h, bg_color=COLOR_CARD_BG, border_color=COLOR_NAVY_DARK, border_width=1.5)
    hbar_inv = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(inv_x), int(inv_y), int(inv_w), int(Inches(0.5)))
    hbar_inv.fill.solid()
    hbar_inv.fill.fore_color.rgb = COLOR_NAVY_DARK
    hbar_inv.line.fill.background()
    tb_hi = slide.shapes.add_textbox(int(inv_x), int(inv_y + Inches(0.1)), int(inv_w), int(Inches(0.3)))
    tf_hi = tb_hi.text_frame
    tf_hi.margin_left = tf_hi.margin_top = tf_hi.margin_right = tf_hi.margin_bottom = 0
    phi = tf_hi.paragraphs[0]
    phi.alignment = PP_ALIGN.CENTER
    phi.text = "INVESTIGATOR / ANALYST"
    phi.font.name = FONT_MAIN
    phi.font.size = Pt(10)
    phi.font.bold = True
    phi.font.color.rgb = COLOR_BG_WHITE

    tb_ibody = slide.shapes.add_textbox(int(inv_x + Inches(0.2)), int(inv_y + Inches(0.7)), int(inv_w - Inches(0.4)), int(inv_h - Inches(0.8)))
    tf_ib = tb_ibody.text_frame
    tf_ib.word_wrap = True
    tf_ib.margin_left = tf_ib.margin_top = tf_ib.margin_right = tf_ib.margin_bottom = 0
    pib = tf_ib.paragraphs[0]
    pib.text = "Primary User Role:"
    pib.font.name = FONT_MAIN
    pib.font.size = Pt(9.5)
    pib.font.bold = True
    pib.font.color.rgb = COLOR_NAVY_DARK
    pib_desc = tf_ib.add_paragraph()
    pib_desc.text = "• Creates Cases\n• Ingests Raw Evidence\n• Reviews Link Matches\n• Validates Entities"
    pib_desc.font.name = FONT_MAIN
    pib_desc.font.size = Pt(9)
    pib_desc.font.color.rgb = COLOR_SLATE_TEXT

    # 2. Center System Process: 0.0 SECE
    sys_x = Inches(5.3)
    sys_y = top_diagram + Inches(0.3)
    sys_w = Inches(2.733)
    sys_h = Inches(3.6)
    create_card(slide, sys_x, sys_y, sys_w, sys_h, bg_color=COLOR_TEAL_LIGHT, border_color=COLOR_TEAL, border_width=2.0)

    tb_sys = slide.shapes.add_textbox(int(sys_x + Inches(0.2)), int(sys_y + Inches(0.4)), int(sys_w - Inches(0.4)), int(Inches(2.8)))
    tf_sys = tb_sys.text_frame
    tf_sys.word_wrap = True
    tf_sys.margin_left = tf_sys.margin_top = tf_sys.margin_right = tf_sys.margin_bottom = 0

    ps0 = tf_sys.paragraphs[0]
    ps0.alignment = PP_ALIGN.CENTER
    ps0.text = "PROCESS 0.0"
    ps0.font.name = FONT_MAIN
    ps0.font.size = Pt(10)
    ps0.font.bold = True
    ps0.font.color.rgb = COLOR_TEAL_DARK

    ps1 = tf_sys.add_paragraph()
    ps1.alignment = PP_ALIGN.CENTER
    ps1.text = "SMART EVIDENCE\nCORRELATION ENGINE\n(SECE PLATFORM)"
    ps1.font.name = FONT_MAIN
    ps1.font.size = Pt(13)
    ps1.font.bold = True
    ps1.font.color.rgb = COLOR_NAVY_DARK

    ps2 = tf_sys.add_paragraph()
    ps2.alignment = PP_ALIGN.CENTER
    ps2.space_before = Pt(8)
    ps2.text = "• Streaming SHA-256 Vault\n• Factory Parsing Hub\n• Regex + spaCy NER\n• Cross-Evidence Matcher"
    ps2.font.name = FONT_MAIN
    ps2.font.size = Pt(9)
    ps2.font.color.rgb = COLOR_SLATE_TEXT

    # 3. Right Actor: Admin / Auditor
    adm_x = Inches(10.133)
    adm_y = top_diagram + Inches(0.5)
    adm_w = Inches(2.4)
    adm_h = Inches(3.2)
    create_card(slide, adm_x, adm_y, adm_w, adm_h, bg_color=COLOR_CARD_BG, border_color=COLOR_NAVY_DARK, border_width=1.5)
    hbar_adm = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(adm_x), int(adm_y), int(adm_w), int(Inches(0.5)))
    hbar_adm.fill.solid()
    hbar_adm.fill.fore_color.rgb = COLOR_NAVY_DARK
    hbar_adm.line.fill.background()
    tb_ha = slide.shapes.add_textbox(int(adm_x), int(adm_y + Inches(0.1)), int(adm_w), int(Inches(0.3)))
    tf_ha = tb_ha.text_frame
    tf_ha.margin_left = tf_ha.margin_top = tf_ha.margin_right = tf_ha.margin_bottom = 0
    pha = tf_ha.paragraphs[0]
    pha.alignment = PP_ALIGN.CENTER
    pha.text = "ADMIN / AUDITOR"
    pha.font.name = FONT_MAIN
    pha.font.size = Pt(10)
    pha.font.bold = True
    pha.font.color.rgb = COLOR_BG_WHITE

    tb_abody = slide.shapes.add_textbox(int(adm_x + Inches(0.2)), int(adm_y + Inches(0.7)), int(adm_w - Inches(0.4)), int(adm_h - Inches(0.8)))
    tf_ab = tb_abody.text_frame
    tf_ab.word_wrap = True
    tf_ab.margin_left = tf_ab.margin_top = tf_ab.margin_right = tf_ab.margin_bottom = 0
    pab = tf_ab.paragraphs[0]
    pab.text = "Supervisory Role:"
    pab.font.name = FONT_MAIN
    pab.font.size = Pt(9.5)
    pab.font.bold = True
    pab.font.color.rgb = COLOR_NAVY_DARK
    pab_desc = tf_ab.add_paragraph()
    pab_desc.text = "• Role & User Admin\n• Audit Log Inspection\n• Chain-of-Custody Review\n• System Health Monitoring"
    pab_desc.font.name = FONT_MAIN
    pab_desc.font.size = Pt(9)
    pab_desc.font.color.rgb = COLOR_SLATE_TEXT

    # Straight 90-degree connectors & label badges
    # Lane 1 (Top lane): Y = 3.1
    y_lane1 = top_diagram + Inches(1.1)
    draw_straight_arrow(slide, inv_x + inv_w, y_lane1, sys_x, y_lane1, color=COLOR_TEAL, width=2.0)
    lbl_box1 = create_card(slide, inv_x + inv_w + Inches(0.15), y_lane1 - Inches(0.38), Inches(1.8), Inches(0.32), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tf_l1 = lbl_box1.text_frame
    tf_l1.margin_left = tf_l1.margin_top = tf_l1.margin_right = tf_l1.margin_bottom = 0
    p_l1 = tf_l1.paragraphs[0]
    p_l1.alignment = PP_ALIGN.CENTER
    p_l1.text = "Upload Evidence & Case Info"
    p_l1.font.name = FONT_MAIN
    p_l1.font.size = Pt(8.5)
    p_l1.font.bold = True
    p_l1.font.color.rgb = COLOR_NAVY_DARK

    # Lane 2 (Bottom lane): Y = 4.7
    y_lane2 = top_diagram + Inches(2.7)
    draw_straight_arrow(slide, sys_x, y_lane2, inv_x + inv_w, y_lane2, color=COLOR_NAVY_DARK, width=2.0)
    lbl_box2 = create_card(slide, inv_x + inv_w + Inches(0.15), y_lane2 + Inches(0.08), Inches(1.8), Inches(0.32), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tf_l2 = lbl_box2.text_frame
    tf_l2.margin_left = tf_l2.margin_top = tf_l2.margin_right = tf_l2.margin_bottom = 0
    p_l2 = tf_l2.paragraphs[0]
    p_l2.alignment = PP_ALIGN.CENTER
    p_l2.text = "SHA-256, Entities, Matches"
    p_l2.font.name = FONT_MAIN
    p_l2.font.size = Pt(8.5)
    p_l2.font.bold = True
    p_l2.font.color.rgb = COLOR_TEAL_DARK

    # Right Lane Connectors
    draw_straight_arrow(slide, adm_x, y_lane2, sys_x + sys_w, y_lane2, color=COLOR_TEAL, width=2.0)
    lbl_box3 = create_card(slide, sys_x + sys_w + Inches(0.15), y_lane2 + Inches(0.08), Inches(1.8), Inches(0.32), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tf_l3 = lbl_box3.text_frame
    tf_l3.margin_left = tf_l3.margin_top = tf_l3.margin_right = tf_l3.margin_bottom = 0
    p_l3 = tf_l3.paragraphs[0]
    p_l3.alignment = PP_ALIGN.CENTER
    p_l3.text = "RBAC Roles & Audit Queries"
    p_l3.font.name = FONT_MAIN
    p_l3.font.size = Pt(8.5)
    p_l3.font.bold = True
    p_l3.font.color.rgb = COLOR_NAVY_DARK

    draw_straight_arrow(slide, sys_x + sys_w, y_lane1, adm_x, y_lane1, color=COLOR_NAVY_DARK, width=2.0)
    lbl_box4 = create_card(slide, sys_x + sys_w + Inches(0.15), y_lane1 - Inches(0.38), Inches(1.8), Inches(0.32), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tf_l4 = lbl_box4.text_frame
    tf_l4.margin_left = tf_l4.margin_top = tf_l4.margin_right = tf_l4.margin_bottom = 0
    p_l4 = tf_l4.paragraphs[0]
    p_l4.alignment = PP_ALIGN.CENTER
    p_l4.text = "Custody Logs & Audit Reports"
    p_l4.font.name = FONT_MAIN
    p_l4.font.size = Pt(8.5)
    p_l4.font.bold = True
    p_l4.font.color.rgb = COLOR_TEAL_DARK


def build_slide_7(prs):
    """Slide 7: Data Flow Diagram — Level 1 (Dedicated System Pipeline Diagram)"""
    slide = add_blank_slide(prs)
    add_header(slide, "System Data Flow", "Data Flow Diagram — Level 1 (Detailed Subsystems)",
               "Step-by-step forensic data flow showing the 5 core processes and 6 persistent data stores.")
    add_footer(slide, 7)

    proc_y = Inches(1.85)
    proc_w = Inches(1.9)
    proc_h = Inches(1.8)
    gap_p = Inches(0.55)
    start_x = Inches(0.8)

    processes = [
        ("1.0", "Evidence Ingestion\n& Hashing", "Locks 64KB SHA-256\nStores binary copy"),
        ("2.0", "Factory\nParsing", "Extracts raw text\nHandles .txt/.csv/.pdf"),
        ("3.0", "Hybrid Entity\nExtraction", "Deterministic Regex\nspaCy NER Models"),
        ("4.0", "Correlation &\nMatching", "Cross-file matches\nJaro-Winkler scores"),
        ("5.0", "Dashboard &\nAudit Trail", "PENDING_REVIEW UI\nAppend-only logs")
    ]

    for idx, (num, title, sub) in enumerate(processes):
        px = start_x + idx * (proc_w + gap_p)
        create_card(slide, px, proc_y, proc_w, proc_h, bg_color=COLOR_CARD_BG, border_color=COLOR_TEAL, border_width=1.5)

        draw_badge(slide, px + Inches(0.12), proc_y + Inches(0.12), Inches(0.6), Inches(0.25), num, COLOR_TEAL, COLOR_BG_WHITE, font_size=9, bold=True)

        tb = slide.shapes.add_textbox(int(px + Inches(0.1)), int(proc_y + Inches(0.45)), int(proc_w - Inches(0.2)), int(proc_h - Inches(0.5)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        p0.text = title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.space_before = Pt(4)
        p1.text = sub
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(8.5)
        p1.font.color.rgb = COLOR_SLATE_TEXT

        if idx < len(processes) - 1:
            arr_x = px + proc_w
            mid_y = proc_y + Inches(0.9)
            draw_straight_arrow(slide, arr_x, mid_y, arr_x + gap_p, mid_y, color=COLOR_NAVY_DARK, width=1.5)

    store_y = Inches(4.35)
    store_h = Inches(1.9)

    data_stores = [
        (Inches(0.8), "D1 & D2: Raw Vault & Evidence DB", "• [D1: Disk Vault] Raw binary stream\n• [D2: Evidence Table] SHA-256 hash, file size, timestamps, case_id", Inches(2.2)),
        (Inches(3.25), "D3: Metadata Store", "• [D3: Evidence Metadata]\nExtracted text content, page count, and parsing status in JSONB", Inches(2.2)),
        (Inches(5.7), "D4: Entity Mentions", "• [D4: Entities & Mentions]\nCanonical catalog + exact file offsets for IP, Email, Phone, Persons", Inches(2.2)),
        (Inches(8.15), "D5: Matches & Links", "• [D5: Matches & Rel]\nPairs marked PENDING_REVIEW with Jaro-Winkler similarity scores", Inches(2.2)),
        (Inches(10.6), "D6: Audit Logs", "• [D6: Audit Log Table]\nImmutable record of logins, uploads, extractions, and approvals", Inches(1.933))
    ]

    for sx, stitle, sdesc, sw in data_stores:
        create_card(slide, sx, store_y, sw, store_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER, border_width=1.0)
        sbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(sx), int(store_y), int(sw), int(Inches(0.32)))
        sbar.fill.solid()
        sbar.fill.fore_color.rgb = COLOR_NAVY_DARK
        sbar.line.fill.background()

        tb_sh = slide.shapes.add_textbox(int(sx), int(store_y + Inches(0.06)), int(sw), int(Inches(0.25)))
        tf_sh = tb_sh.text_frame
        tf_sh.margin_left = tf_sh.margin_top = tf_sh.margin_right = tf_sh.margin_bottom = 0
        psh = tf_sh.paragraphs[0]
        psh.alignment = PP_ALIGN.CENTER
        psh.text = stitle
        psh.font.name = FONT_MAIN
        psh.font.size = Pt(8.5)
        psh.font.bold = True
        psh.font.color.rgb = COLOR_BG_WHITE

        tb_sb = slide.shapes.add_textbox(int(sx + Inches(0.12)), int(store_y + Inches(0.42)), int(sw - Inches(0.24)), int(store_h - Inches(0.5)))
        tf_sb = tb_sb.text_frame
        tf_sb.word_wrap = True
        tf_sb.margin_left = tf_sb.margin_top = tf_sb.margin_right = tf_sb.margin_bottom = 0
        psb = tf_sb.paragraphs[0]
        psb.text = sdesc
        psb.font.name = FONT_MAIN
        psb.font.size = Pt(8.5)
        psb.font.color.rgb = COLOR_SLATE_TEXT

        px_center = int(sx + sw / 2)
        draw_straight_arrow(slide, px_center, proc_y + proc_h, px_center, store_y, color=COLOR_TEAL, width=1.5)


def build_slide_8(prs):
    """Slide 8: Core Modules & Database Design"""
    slide = add_blank_slide(prs)
    add_header(slide, "Implementation Details", "Core Implemented Modules & Database Schema",
               "Seven functional system modules backed by an enterprise 10-table normalized PostgreSQL 18.6 schema.")
    add_footer(slide, 8)

    card_w = Inches(5.7)
    card_h = Inches(4.8)
    top_y = Inches(1.8)

    # Left Column: 7 Modules
    left_x = Inches(0.8)
    create_card(slide, left_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_m = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(left_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_m.fill.solid()
    bar_m.fill.fore_color.rgb = COLOR_NAVY_DARK
    bar_m.line.fill.background()

    draw_badge(slide, left_x + Inches(0.3), top_y + Inches(0.18), Inches(2.2), Inches(0.25), "7 CORE SYSTEM MODULES", COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=8.5, bold=True)

    modules = [
        ("1. Auth & RBAC:", "Bcrypt password hashing, JWT bearer tokens, role enforcement."),
        ("2. Case Management:", "Case containers with strict isolation and status lifecycles."),
        ("3. Evidence Vault:", "Streaming 64KB SHA-256 hashing locks file integrity upon upload."),
        ("4. Factory Parsers:", "Extensible polymorphic parsers for .txt, .csv, and .pdf formats."),
        ("5. Hybrid Extractor:", "Deterministic Regex (Email, IP, Phone) + spaCy NER (Person)."),
        ("6. Correlation Engine:", "Exact matching + Jaro-Winkler similarity (score threshold)."),
        ("7. Audit Log Inspector:", "Immutable append-only record tracking all investigator actions.")
    ]

    tb_mod = slide.shapes.add_textbox(int(left_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(card_h - Inches(0.65)))
    tf_m = tb_mod.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0

    for idx, (m_title, m_desc) in enumerate(modules):
        p = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
        p.space_after = Pt(7)
        r0 = p.add_run()
        r0.text = m_title + " "
        r0.font.name = FONT_MAIN
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY_DARK
        r1 = p.add_run()
        r1.text = m_desc
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_SLATE_TEXT

    # Right Column: 10 PostgreSQL Tables
    right_x = Inches(6.833)
    create_card(slide, right_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_d = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(right_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_d.fill.solid()
    bar_d.fill.fore_color.rgb = COLOR_TEAL
    bar_d.line.fill.background()

    draw_badge(slide, right_x + Inches(0.3), top_y + Inches(0.18), Inches(2.4), Inches(0.25), "POSTGRESQL 18.6 SCHEMA (10 TABLES)", COLOR_TEAL, COLOR_BG_WHITE, font_size=8.5, bold=True)

    tb_sch = slide.shapes.add_textbox(int(right_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(card_h - Inches(0.65)))
    tf_s = tb_sch.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0

    p_grp1 = tf_s.paragraphs[0]
    p_grp1.text = "Custody & Case Management Tables:"
    p_grp1.font.name = FONT_MAIN
    p_grp1.font.size = Pt(10.5)
    p_grp1.font.bold = True
    p_grp1.font.color.rgb = COLOR_TEAL_DARK

    tables_custody = [
        ("users", "User profiles, roles (analyst/admin), hashed credentials."),
        ("cases", "Incident metadata, case numbers, open/closed status."),
        ("evidence", "File metadata, original name, mime type, SHA-256 hash."),
        ("evidence_metadata", "Extracted text content and schema metadata in JSONB."),
        ("audit_logs", "Append-only forensic event log with actor IDs & timestamps.")
    ]
    for tbl, desc in tables_custody:
        p = tf_s.add_paragraph()
        p.space_after = Pt(2)
        r0 = p.add_run()
        r0.text = f"• {tbl}: "
        r0.font.name = FONT_CODE
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY_DARK
        r1 = p.add_run()
        r1.text = desc
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SLATE_TEXT

    p_grp2 = tf_s.add_paragraph()
    p_grp2.space_before = Pt(8)
    p_grp2.text = "Intelligence & Correlation Tables:"
    p_grp2.font.name = FONT_MAIN
    p_grp2.font.size = Pt(10.5)
    p_grp2.font.bold = True
    p_grp2.font.color.rgb = COLOR_TEAL_DARK

    tables_intel = [
        ("entities", "Canonical deduplicated entities across all case files."),
        ("entity_mentions", "File-level occurrences with exact character offsets."),
        ("entity_matches", "Scored candidate links flagged as PENDING_REVIEW."),
        ("relationships", "Confirmed analyst-approved cross-file connections."),
        ("timeline_events", "Chronologically sequenced event logs across evidence.")
    ]
    for tbl, desc in tables_intel:
        p = tf_s.add_paragraph()
        p.space_after = Pt(2)
        r0 = p.add_run()
        r0.text = f"• {tbl}: "
        r0.font.name = FONT_CODE
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY_DARK
        r1 = p.add_run()
        r1.text = desc
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SLATE_TEXT


def build_slide_9(prs):
    """Slide 9: Technology Stack & System Requirements"""
    slide = add_blank_slide(prs)
    add_header(slide, "Technical Specifications", "Technology Stack & System Requirements",
               "Production-grade open-source stack selected for speed, stability, and forensic defensibility.")
    add_footer(slide, 9)

    card_w = Inches(5.7)
    card_h = Inches(4.8)
    top_y = Inches(1.8)

    # Left Card: Software Stack
    left_x = Inches(0.8)
    create_card(slide, left_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(left_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_s.fill.solid()
    bar_s.fill.fore_color.rgb = COLOR_NAVY_DARK
    bar_s.line.fill.background()

    draw_badge(slide, left_x + Inches(0.3), top_y + Inches(0.18), Inches(2.2), Inches(0.25), "SOFTWARE & AI STACK", COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=8.5, bold=True)

    tech_items = [
        ("Runtime Environment:", "Python 3.14 (Async I/O, modern typing, high performance)"),
        ("Backend Framework:", "FastAPI (High-speed ASGI, auto Swagger OpenAPI docs)"),
        ("Database Engine:", "PostgreSQL 18.6 (ACID transactions, JSONB indexing)"),
        ("Object-Relational Mapping:", "SQLAlchemy 2.0 (Modern declarative mapped models)"),
        ("NLP & NER Engine:", "spaCy (en_core_web_sm) + Custom Compiled Regex"),
        ("Parsers & File Processing:", "pypdf (PDF text & meta), csv/text standard libraries"),
        ("Authentication & Security:", "PyJWT (HS256/RS256 tokens) & Passlib (Bcrypt hashing)"),
        ("Frontend Workstation:", "HTML5, CSS3 Modern Dark/Light Theme, Vanilla ES6+ JS")
    ]

    tb_t = slide.shapes.add_textbox(int(left_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(card_h - Inches(0.65)))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0

    for idx, (label, val) in enumerate(tech_items):
        p = tf_t.paragraphs[0] if idx == 0 else tf_t.add_paragraph()
        p.space_after = Pt(5)
        r0 = p.add_run()
        r0.text = "• " + label + " "
        r0.font.name = FONT_MAIN
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY_DARK
        r1 = p.add_run()
        r1.text = val
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SLATE_TEXT

    # Right Card: Hardware & Deployment
    right_x = Inches(6.833)
    create_card(slide, right_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_h = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(right_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_h.fill.solid()
    bar_h.fill.fore_color.rgb = COLOR_TEAL
    bar_h.line.fill.background()

    draw_badge(slide, right_x + Inches(0.3), top_y + Inches(0.18), Inches(2.4), Inches(0.25), "HARDWARE & ENVIRONMENT", COLOR_TEAL, COLOR_BG_WHITE, font_size=8.5, bold=True)

    hw_items = [
        ("Processor (CPU):", "Intel Core i5 / AMD Ryzen 5 or higher (Multi-core for batch parsing)"),
        ("System Memory (RAM):", "8 GB minimum (16 GB recommended for concurrent spaCy models)"),
        ("Primary Storage:", "256 GB NVMe SSD (High random I/O for 64KB streaming hashing)"),
        ("Network Configuration:", "Gigabit Ethernet / Localhost (Zero external cloud dependencies)"),
        ("Operating System:", "Windows 11 / Linux (Ubuntu 22.04 LTS / Debian stable)"),
        ("Browser Compatibility:", "Google Chrome, Microsoft Edge, Mozilla Firefox (Modern ECMAScript)"),
        ("Security Isolation:", "Dedicated isolated local folder for raw binary disk vault")
    ]

    tb_h = slide.shapes.add_textbox(int(right_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(card_h - Inches(0.65)))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0

    for idx, (label, val) in enumerate(hw_items):
        p = tf_h.paragraphs[0] if idx == 0 else tf_h.add_paragraph()
        p.space_after = Pt(7)
        r0 = p.add_run()
        r0.text = "• " + label + " "
        r0.font.name = FONT_MAIN
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY_DARK
        r1 = p.add_run()
        r1.text = val
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SLATE_TEXT


def build_slide_10(prs):
    """Slide 10: Results & Functional Verification"""
    slide = add_blank_slide(prs)
    add_header(slide, "Experimental Evaluation", "Results & Functional Prototype Verification",
               "Empirical verification across synthetic cyber incident files confirms forensic accuracy and link discovery.")
    add_footer(slide, 10)

    top_y = Inches(1.8)
    card_w = Inches(3.75)
    card_h = Inches(1.1)
    gap_c = Inches(0.24)
    start_x = Inches(0.8)

    highlights = [
        ("Tamper Detection", "100% SUCCESS", "Any single byte alteration on disk immediately triggers a cryptographic hash mismatch flag.", COLOR_GREEN_TXT, COLOR_GREEN_BG),
        ("Entity Extraction", "HIGH PRECISION", "Deterministic regex achieved zero false positives on emails/IPs; spaCy NER tagged suspects.", COLOR_BLUE_TXT, COLOR_BLUE_BG),
        ("Analyst Triage", "HUMAN-IN-THE-LOOP", "Non-destructive PENDING_REVIEW queue prevents automatic erroneous entity merges.", COLOR_AMBER_TXT, COLOR_AMBER_BG)
    ]

    for idx, (title, stat, desc, text_c, bg_c) in enumerate(highlights):
        cx = start_x + idx * (card_w + gap_c)
        create_card(slide, cx, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

        draw_badge(slide, cx + Inches(0.15), top_y + Inches(0.12), Inches(1.4), Inches(0.22), title.upper(), COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=7.5, bold=True)
        draw_badge(slide, cx + card_w - Inches(1.45), top_y + Inches(0.12), Inches(1.3), Inches(0.22), stat, bg_c, text_c, font_size=8, bold=True)

        tb = slide.shapes.add_textbox(int(cx + Inches(0.15)), int(top_y + Inches(0.42)), int(card_w - Inches(0.3)), int(Inches(0.6)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_SLATE_TEXT

    tbl_top = Inches(3.1)
    tbl_w = Inches(11.733)
    tbl_h = Inches(3.6)

    rows = 5
    cols = 5
    col_widths = [Inches(1.8), Inches(3.2), Inches(2.6), Inches(1.8), Inches(2.333)]

    table_shape = slide.shapes.add_table(rows, cols, int(Inches(0.8)), int(tbl_top), int(tbl_w), int(tbl_h))
    table = table_shape.table

    for i, w in enumerate(col_widths):
        table.columns[i].width = int(w)

    headers = ["Entity Type", "Extracted Value / Match Pair", "Matching Logic", "Confidence", "Triage Status"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_DARK
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.1)
        tf.margin_bottom = Inches(0.1)
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_MAIN
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_BG_WHITE

    sample_results = [
        ("EMAIL", "arun.kumar@darknet.org", "Deterministic Regex Exact Match", "100%", "PENDING_REVIEW"),
        ("IPV4", "192.168.1.105", "Valid Octet Boundary Match", "100%", "PENDING_REVIEW"),
        ("PHONE", "+91 98765 43210", "E.164 Cleaned Digit Match", "100%", "PENDING_REVIEW"),
        ("PERSON", "Arun Kumar  ↔  A. Kumar", "spaCy NER + Jaro-Winkler", "88%", "PENDING_REVIEW")
    ]

    for row_idx, (etype, evalue, elogic, conf, status) in enumerate(sample_results, start=1):
        bg_col = COLOR_CARD_BG if row_idx % 2 == 1 else COLOR_BG_WHITE

        c0 = table.cell(row_idx, 0)
        c0.fill.solid(); c0.fill.fore_color.rgb = bg_col
        tf0 = c0.text_frame; tf0.word_wrap = True; tf0.margin_left = Inches(0.15); tf0.margin_top = Inches(0.12)
        p0 = tf0.paragraphs[0]; p0.text = etype; p0.font.name = FONT_MAIN; p0.font.size = Pt(10); p0.font.bold = True; p0.font.color.rgb = COLOR_NAVY_DARK

        c1 = table.cell(row_idx, 1)
        c1.fill.solid(); c1.fill.fore_color.rgb = bg_col
        tf1 = c1.text_frame; tf1.word_wrap = True; tf1.margin_left = Inches(0.15); tf1.margin_top = Inches(0.12)
        p1 = tf1.paragraphs[0]; p1.text = evalue; p1.font.name = FONT_CODE; p1.font.size = Pt(9.5); p1.font.color.rgb = COLOR_SLATE_TEXT

        c2 = table.cell(row_idx, 2)
        c2.fill.solid(); c2.fill.fore_color.rgb = bg_col
        tf2 = c2.text_frame; tf2.word_wrap = True; tf2.margin_left = Inches(0.15); tf2.margin_top = Inches(0.12)
        p2 = tf2.paragraphs[0]; p2.text = elogic; p2.font.name = FONT_MAIN; p2.font.size = Pt(9.5); p2.font.color.rgb = COLOR_SLATE_TEXT

        c3 = table.cell(row_idx, 3)
        c3.fill.solid(); c3.fill.fore_color.rgb = bg_col
        tf3 = c3.text_frame; tf3.word_wrap = True; tf3.margin_left = Inches(0.15); tf3.margin_top = Inches(0.12)
        p3 = tf3.paragraphs[0]; p3.text = conf; p3.font.name = FONT_MAIN; p3.font.size = Pt(10); p3.font.bold = True
        p3.font.color.rgb = COLOR_GREEN_TXT if conf == "100%" else COLOR_TEAL_DARK

        c4 = table.cell(row_idx, 4)
        c4.fill.solid(); c4.fill.fore_color.rgb = bg_col
        tf4 = c4.text_frame; tf4.word_wrap = True; tf4.margin_left = Inches(0.15); tf4.margin_top = Inches(0.12)
        p4 = tf4.paragraphs[0]; p4.text = status; p4.font.name = FONT_CODE; p4.font.size = Pt(9.5); p4.font.bold = True
        p4.font.color.rgb = COLOR_AMBER_TXT


def build_slide_11(prs):
    """Slide 11: Conclusion & Future Enhancements"""
    slide = add_blank_slide(prs)
    add_header(slide, "Summary & Roadmap", "Conclusion & Future Enhancements",
               "Delivered an automated forensic triage engine, with defined paths for scaling forensic capabilities.")
    add_footer(slide, 11)

    card_w = Inches(5.7)
    card_h = Inches(4.8)
    top_y = Inches(1.8)

    # Left Card: Conclusion
    left_x = Inches(0.8)
    create_card(slide, left_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(left_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_c.fill.solid()
    bar_c.fill.fore_color.rgb = COLOR_NAVY_DARK
    bar_c.line.fill.background()

    draw_badge(slide, left_x + Inches(0.3), top_y + Inches(0.2), Inches(2.2), Inches(0.26), "PROJECT CONCLUSION", COLOR_NAVY_DARK, COLOR_BG_WHITE, font_size=8.5, bold=True)

    title_c = slide.shapes.add_textbox(int(left_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(Inches(0.4)))
    tf_tc = title_c.text_frame
    tf_tc.margin_left = tf_tc.margin_top = tf_tc.margin_right = tf_tc.margin_bottom = 0
    p_tc = tf_tc.paragraphs[0]
    p_tc.text = "Implemented System Achievements"
    p_tc.font.name = FONT_MAIN
    p_tc.font.size = Pt(15)
    p_tc.font.bold = True
    p_tc.font.color.rgb = COLOR_NAVY_DARK

    concl_items = [
        ("End-to-End Triage Pipeline", "Successfully connects raw multi-format uploads (.txt, .csv, .pdf) directly to correlated entity intelligence."),
        ("Strict Chain of Custody", "Streaming 64KB SHA-256 cryptographic locking guarantees file integrity without memory exhaustion."),
        ("Hybrid AI Accuracy", "Blends deterministic regex speed for structured identifiers with spaCy NLP for unstructured person names."),
        ("Human-Centric Safety", "Non-destructive PENDING_REVIEW workflow leaves final confirmation under full investigator control.")
    ]

    c_y = top_y + Inches(1.05)
    for title, desc in concl_items:
        create_card(slide, left_x + Inches(0.3), c_y, card_w - Inches(0.6), Inches(0.8), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER, border_width=0.8)
        tb = slide.shapes.add_textbox(int(left_x + Inches(0.45)), int(c_y + Inches(0.1)), int(card_w - Inches(0.9)), int(Inches(0.6)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.text = "★  " + title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(9)
        p1.font.color.rgb = COLOR_SLATE_TEXT
        c_y += Inches(0.88)

    # Right Card: Future Enhancements
    right_x = Inches(6.833)
    create_card(slide, right_x, top_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_f = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(right_x), int(top_y), int(card_w), int(Inches(0.06)))
    bar_f.fill.solid()
    bar_f.fill.fore_color.rgb = COLOR_TEAL
    bar_f.line.fill.background()

    draw_badge(slide, right_x + Inches(0.3), top_y + Inches(0.2), Inches(2.2), Inches(0.26), "FUTURE ENHANCEMENTS", COLOR_TEAL, COLOR_BG_WHITE, font_size=8.5, bold=True)

    title_f = slide.shapes.add_textbox(int(right_x + Inches(0.3)), int(top_y + Inches(0.55)), int(card_w - Inches(0.6)), int(Inches(0.4)))
    tf_tf = title_f.text_frame
    tf_tf.margin_left = tf_tf.margin_top = tf_tf.margin_right = tf_tf.margin_bottom = 0
    p_tf = tf_tf.paragraphs[0]
    p_tf.text = "Planned Engineering Roadmap"
    p_tf.font.name = FONT_MAIN
    p_tf.font.size = Pt(15)
    p_tf.font.bold = True
    p_tf.font.color.rgb = COLOR_NAVY_DARK

    future_items = [
        ("Tesseract OCR Integration", "Extract text automatically from scanned paper documents, crime scene receipts, and PNG/JPEG evidence."),
        ("Interactive Cytoscape.js Graph", "Full interactive node-link network visualizer allowing analysts to pan, zoom, and cluster entity networks."),
        ("Chronological Timeline Slider", "Interactive event playback scrubbing across multi-source evidence timestamps to uncover timelines."),
        ("Court-Ready Dossier Export", "Automated one-click PDF generation bundling hashes, entity links, and audit logs for courtroom presentation.")
    ]

    f_y = top_y + Inches(1.05)
    for title, desc in future_items:
        create_card(slide, right_x + Inches(0.3), f_y, card_w - Inches(0.6), Inches(0.8), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER, border_width=0.8)
        tb = slide.shapes.add_textbox(int(right_x + Inches(0.45)), int(f_y + Inches(0.1)), int(card_w - Inches(0.9)), int(Inches(0.6)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.text = "➜  " + title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_TEAL
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(9)
        p1.font.color.rgb = COLOR_SLATE_TEXT
        f_y += Inches(0.88)


def build_slide_12(prs):
    """Slide 12: References"""
    slide = add_blank_slide(prs)
    add_header(slide, "Academic Foundation", "Key References & Forensic Standards",
               "Grounded in established digital forensics literature, international standards, and peer-reviewed research.")
    add_footer(slide, 12)

    top_y = Inches(1.8)
    card_w = Inches(11.733)
    card_h = Inches(1.05)
    gap_y = Inches(0.2)

    references = [
        ("1", "Casey, E. (2011)", "Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet", "3rd Edition, Academic Press. Standard textbook on chain-of-custody, digital triage, and evidentiary integrity standards."),
        ("2", "NIST SP 800-86 (2006)", "Guide to Integrating Forensic Techniques into Incident Response", "National Institute of Standards and Technology, U.S. Dept. of Commerce. Outlines forensic collection, preservation, and analysis methodologies."),
        ("3", "ISO/IEC 27037:2012", "Guidelines for Identification, Collection, Acquisition and Preservation of Digital Evidence", "International Organization for Standardization. Governs digital chain-of-custody, forensic integrity, and admissibility protocols."),
        ("4", "Al-Azhar, M. N. (2022)", "Cross-Evidence Correlation in Digital Forensics Using Graph Analytics and NLP Techniques", "IEEE Transactions on Information Forensics and Security, vol. 17, pp. 1120–1134. Methodological basis for hybrid regex and NER entity linking.")
    ]

    for idx, (num, author, title, pub) in enumerate(references):
        cy = top_y + idx * (card_h + gap_y)
        create_card(slide, Inches(0.8), cy, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

        draw_badge(slide, Inches(1.0), cy + Inches(0.3), Inches(0.45), Inches(0.45), num, COLOR_TEAL, COLOR_BG_WHITE, font_size=12, bold=True)

        tb = slide.shapes.add_textbox(int(Inches(1.65)), int(cy + Inches(0.15)), int(card_w - Inches(1.8)), int(card_h - Inches(0.25)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = author + " — "
        r0.font.name = FONT_MAIN
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY_DARK

        r1 = p0.add_run()
        r1.text = f'"{title}"'
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(10.5)
        r1.font.italic = True
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEAL_DARK

        p1 = tf.add_paragraph()
        p1.space_before = Pt(3)
        p1.text = pub
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(9)
        p1.font.color.rgb = COLOR_SLATE_TEXT


def build_slide_13(prs):
    """Slide 13: End Card / Thank You Slide (Separate Closing Slide)"""
    slide = add_blank_slide(prs)

    bar1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, int(Inches(0.35)), int(Inches(7.5)))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = COLOR_NAVY_DARK
    bar1.line.fill.background()

    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(Inches(0.35)), 0, int(Inches(0.12)), int(Inches(7.5)))
    bar2.fill.solid()
    bar2.fill.fore_color.rgb = COLOR_TEAL
    bar2.line.fill.background()

    content_left = Inches(1.2)

    inst_box = slide.shapes.add_textbox(int(content_left), int(Inches(0.8)), int(Inches(11.3)), int(Inches(0.5)))
    tf_inst = inst_box.text_frame
    tf_inst.word_wrap = True
    tf_inst.margin_left = tf_inst.margin_top = tf_inst.margin_right = tf_inst.margin_bottom = 0
    p0 = tf_inst.paragraphs[0]
    p0.text = "RATHINAM TECHNICAL CAMPUS (AUTONOMOUS)  •  DEPARTMENT OF MCA"
    p0.font.name = FONT_MAIN
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_TEAL

    ty_box = slide.shapes.add_textbox(int(content_left), int(Inches(1.6)), int(Inches(11.3)), int(Inches(2.2)))
    tf_ty = ty_box.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_top = tf_ty.margin_right = tf_ty.margin_bottom = 0

    pt0 = tf_ty.paragraphs[0]
    pt0.text = "THANK YOU"
    pt0.font.name = FONT_MAIN
    pt0.font.size = Pt(44)
    pt0.font.bold = True
    pt0.font.color.rgb = COLOR_NAVY_DARK

    pt1 = tf_ty.add_paragraph()
    pt1.space_before = Pt(8)
    pt1.text = "Questions & Live System Demonstration"
    pt1.font.name = FONT_MAIN
    pt1.font.size = Pt(18)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_TEAL

    pt2 = tf_ty.add_paragraph()
    pt2.space_before = Pt(6)
    pt2.text = "Open for viva questions, technical queries, and prototype demonstration."
    pt2.font.name = FONT_MAIN
    pt2.font.size = Pt(11.5)
    pt2.font.color.rgb = COLOR_SLATE_MUTED

    bottom_y = Inches(4.3)
    card_w = Inches(11.3)
    card_h = Inches(2.4)
    create_card(slide, content_left, bottom_y, card_w, card_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

    bar_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(content_left), int(bottom_y), int(card_w), int(Inches(0.06)))
    bar_strip.fill.solid()
    bar_strip.fill.fore_color.rgb = COLOR_TEAL
    bar_strip.line.fill.background()

    col1_w = Inches(4.0)
    tb_c1 = slide.shapes.add_textbox(int(content_left + Inches(0.4)), int(bottom_y + Inches(0.3)), int(col1_w), int(Inches(1.8)))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = tf_c1.margin_right = tf_c1.margin_bottom = 0
    p_c1_0 = tf_c1.paragraphs[0]
    p_c1_0.text = "PROJECT IDENTIFICATION"
    p_c1_0.font.name = FONT_MAIN
    p_c1_0.font.size = Pt(9.5)
    p_c1_0.font.bold = True
    p_c1_0.font.color.rgb = COLOR_TEAL

    p_c1_1 = tf_c1.add_paragraph()
    p_c1_1.text = "SMART EVIDENCE CORRELATION ENGINE"
    p_c1_1.font.name = FONT_MAIN
    p_c1_1.font.size = Pt(11.5)
    p_c1_1.font.bold = True
    p_c1_1.font.color.rgb = COLOR_NAVY_DARK

    p_c1_2 = tf_c1.add_paragraph()
    p_c1_2.text = "Course: 25EEC204 – Mini Project II\nMaster of Computer Applications (MCA)\nAcademic Year: May – 2026"
    p_c1_2.font.name = FONT_MAIN
    p_c1_2.font.size = Pt(9.5)
    p_c1_2.font.color.rgb = COLOR_SLATE_TEXT

    col2_x = content_left + Inches(4.7)
    col2_w = Inches(3.2)
    tb_c2 = slide.shapes.add_textbox(int(col2_x), int(bottom_y + Inches(0.3)), int(col2_w), int(Inches(1.8)))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = tf_c2.margin_right = tf_c2.margin_bottom = 0
    p_c2_0 = tf_c2.paragraphs[0]
    p_c2_0.text = "SUBMITTED BY"
    p_c2_0.font.name = FONT_MAIN
    p_c2_0.font.size = Pt(9.5)
    p_c2_0.font.bold = True
    p_c2_0.font.color.rgb = COLOR_TEAL

    p_c2_1 = tf_c2.add_paragraph()
    p_c2_1.text = "• Subhalekshmi M (25205090)\n• Yuktha R (25205113)"
    p_c2_1.font.name = FONT_MAIN
    p_c2_1.font.size = Pt(11)
    p_c2_1.font.bold = True
    p_c2_1.font.color.rgb = COLOR_NAVY_DARK

    p_c2_2 = tf_c2.add_paragraph()
    p_c2_2.text = "Dept. of Computer Applications\nRathinam Technical Campus"
    p_c2_2.font.name = FONT_MAIN
    p_c2_2.font.size = Pt(9.5)
    p_c2_2.font.color.rgb = COLOR_SLATE_TEXT

    col3_x = content_left + Inches(8.1)
    col3_w = Inches(2.8)
    tb_c3 = slide.shapes.add_textbox(int(col3_x), int(bottom_y + Inches(0.3)), int(col3_w), int(Inches(1.8)))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = tf_c3.margin_top = tf_c3.margin_right = tf_c3.margin_bottom = 0
    p_c3_0 = tf_c3.paragraphs[0]
    p_c3_0.text = "PROJECT GUIDE"
    p_c3_0.font.name = FONT_MAIN
    p_c3_0.font.size = Pt(9.5)
    p_c3_0.font.bold = True
    p_c3_0.font.color.rgb = COLOR_TEAL

    p_c3_1 = tf_c3.add_paragraph()
    p_c3_1.text = "Ms. R. Alamelumangai"
    p_c3_1.font.name = FONT_MAIN
    p_c3_1.font.size = Pt(11)
    p_c3_1.font.bold = True
    p_c3_1.font.color.rgb = COLOR_NAVY_DARK

    p_c3_2 = tf_c3.add_paragraph()
    p_c3_2.text = "Assistant Professor\nDepartment of MCA\nCoimbatore – 641 021"
    p_c3_2.font.name = FONT_MAIN
    p_c3_2.font.size = Pt(9.5)
    p_c3_2.font.color.rgb = COLOR_SLATE_TEXT


# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
def main():
    print("Initializing PowerPoint presentation generation for SECE...")
    prs = create_presentation()

    print("Building Slide 1: Front Page (Cover)...")
    build_slide_1(prs)

    print("Building Slide 2: Abstract & Overview...")
    build_slide_2(prs)

    print("Building Slide 3: Problem Statement & Objectives...")
    build_slide_3(prs)

    print("Building Slide 4: Existing System vs. Proposed System (SECE)...")
    build_slide_4(prs)

    print("Building Slide 5: System Architecture Diagram...")
    build_slide_5(prs)

    print("Building Slide 6: Data Flow Diagram - Level 0...")
    build_slide_6(prs)

    print("Building Slide 7: Data Flow Diagram - Level 1...")
    build_slide_7(prs)

    print("Building Slide 8: Core Modules & Database Design...")
    build_slide_8(prs)

    print("Building Slide 9: Technology Stack & System Requirements...")
    build_slide_9(prs)

    print("Building Slide 10: Results & Functional Verification...")
    build_slide_10(prs)

    print("Building Slide 11: Conclusion & Future Enhancements...")
    build_slide_11(prs)

    print("Building Slide 12: References...")
    build_slide_12(prs)

    print("Building Slide 13: End Card / Thank You Slide...")
    build_slide_13(prs)

    output_filename = "SECE_Presentation_Light.pptx"
    prs.save(output_filename)
    print("\n=======================================================")
    print("SUCCESS: Presentation successfully generated and saved:")
    print(f"Path: {os.path.abspath(output_filename)}")
    print(f"Total Slides: {len(prs.slides)}")
    print("=======================================================")

if __name__ == "__main__":
    main()
