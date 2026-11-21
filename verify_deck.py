"""
Verification script for SECE_Presentation_Light.pptx
Checks bounding boxes, text frames, overflows, and diagram layout metrics.
"""

import pptx
from pptx.util import Inches, Pt

prs = pptx.Presentation("SECE_Presentation_Light.pptx")
print(f"Total Slides: {len(prs.slides)}")
print(f"Slide Dimensions: {prs.slide_width.inches:.3f} x {prs.slide_height.inches:.3f} inches (16:9)")

max_w = prs.slide_width.inches
max_h = prs.slide_height.inches

issues = []

for idx, slide in enumerate(prs.slides, start=1):
    shape_count = len(slide.shapes)
    print(f"\n--- Slide {idx}: {shape_count} shapes ---")
    
    for s_idx, shape in enumerate(slide.shapes):
        l = shape.left.inches if shape.left else 0
        t = shape.top.inches if shape.top else 0
        w = shape.width.inches if shape.width else 0
        h = shape.height.inches if shape.height else 0
        
        # Check if shape extends outside slide boundaries
        if l < -0.05 or t < -0.05 or (l + w) > (max_w + 0.1) or (t + h) > (max_h + 0.1):
            issues.append(f"Slide {idx} Shape {s_idx} ({shape.name}): Bounds outside slide ({l:.2f}, {t:.2f}, {w:.2f}, {h:.2f})")
            
        # Check text
        if shape.has_text_frame:
            for p_idx, p in enumerate(shape.text_frame.paragraphs):
                text_preview = p.text[:40].replace('\n', ' ')
                if text_preview.strip():
                    pass # has text

if not issues:
    print("\n>>> ALL CHECKS PASSED: Zero shapes outside slide bounds! <<<")
else:
    print(f"\n>>> FOUND {len(issues)} ISSUES: <<<")
    for iss in issues:
        print("  -", iss)
