#!/usr/bin/env python3
"""Build the Nederman ducting field labeling guide PDF."""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "nederman-ducting-labeling-guide.pdf")

INK = colors.HexColor("#1a1a1a")
ACCENT = colors.HexColor("#0b5394")
RULE = colors.HexColor("#c9c9c9")
BAND = colors.HexColor("#eef3f8")
WARN = colors.HexColor("#b45309")

styles = getSampleStyleSheet()


def S(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=base, **kw)


BODY = S("body", fontName="Helvetica", fontSize=10, leading=14,
         textColor=INK, spaceAfter=6, alignment=TA_LEFT)
H1 = S("h1", fontName="Helvetica-Bold", fontSize=15, leading=18,
       textColor=ACCENT, spaceBefore=14, spaceAfter=7)
H2 = S("h2", fontName="Helvetica-Bold", fontSize=11, leading=14,
       textColor=INK, spaceBefore=9, spaceAfter=4)
TITLE = S("title", fontName="Helvetica-Bold", fontSize=22, leading=25,
          textColor=INK, spaceAfter=3)
SUB = S("sub", fontName="Helvetica", fontSize=11, leading=14,
        textColor=colors.HexColor("#555555"), spaceAfter=2)
MONO = S("mono", fontName="Courier-Bold", fontSize=11, leading=15,
         textColor=ACCENT, spaceAfter=4)
SMALL = S("small", fontName="Helvetica", fontSize=8.5, leading=11.5,
          textColor=colors.HexColor("#555555"))
CELL = S("cell", fontName="Helvetica", fontSize=9, leading=12, textColor=INK)
CELLB = S("cellb", parent=CELL, fontName="Helvetica-Bold")
CELLM = S("cellm", parent=CELL, fontName="Courier-Bold", textColor=ACCENT)


def bullets(items, style=BODY, bullet="•"):
    return ListFlowable(
        [ListItem(Paragraph(t, style), leftIndent=14, value=bullet)
         for t in items],
        bulletType="bullet", start=bullet, leftIndent=12,
        bulletFontSize=9, spaceBefore=1, spaceAfter=6,
    )


def numbered(items, style=BODY):
    return ListFlowable(
        [ListItem(Paragraph(t, style), leftIndent=16) for t in items],
        bulletType="1", leftIndent=14, bulletFontName="Helvetica-Bold",
        spaceBefore=1, spaceAfter=6,
    )


def grid(data, widths, header=True, align_left_first=True):
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), BAND)]
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, body, color=WARN):
    inner = [[Paragraph("<b>%s</b>" % title, CELLB), ],
             [Paragraph(body, CELL)]]
    t = Table(inner, colWidths=[6.6 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fdf6ec")),
        ("BOX", (0, 0), (-1, -1), 0.8, color),
        ("LINEBEFORE", (0, 0), (0, -1), 3, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, -1), 0),
    ]))
    return t


class Checkbox(Flowable):
    """Empty tick box — Helvetica has no U+2610 glyph, so draw it."""

    def __init__(self, size=9):
        Flowable.__init__(self)
        self.width = self.height = size

    def draw(self):
        self.canv.setStrokeColor(colors.HexColor("#8a8a8a"))
        self.canv.setLineWidth(0.8)
        self.canv.rect(0, 0, self.width, self.height, stroke=1, fill=0)


class Rule(Flowable):
    def __init__(self, width=6.9 * inch, thickness=0.7, color=RULE, space=6):
        Flowable.__init__(self)
        self.width, self.thickness, self.color, self.space = width, thickness, color, space
        self.height = space

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space / 2.0, self.width, self.space / 2.0)


class Schematic(Flowable):
    """Branch schematic redrawn from Karl's sketch: 32 trunk, 24 main, 16 lateral."""

    def __init__(self, width=6.9 * inch, height=2.45 * inch):
        Flowable.__init__(self)
        self.width, self.height = width, height

    def _duct(self, c, x1, y1, x2, y2, w, label, tag, dia_note, off=2.4):
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        dx, dy = -math.sin(ang) * w / 2.0, math.cos(ang) * w / 2.0
        p = c.beginPath()
        p.moveTo(x1 + dx, y1 + dy)
        p.lineTo(x2 + dx, y2 + dy)
        p.lineTo(x2 - dx, y2 - dy)
        p.lineTo(x1 - dx, y1 - dy)
        p.close()
        c.setFillColor(colors.HexColor("#dce7f2"))
        c.setStrokeColor(ACCENT)
        c.setLineWidth(1.1)
        c.drawPath(p, stroke=1, fill=1)
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        c.setFillColor(ACCENT)
        c.setFont("Courier-Bold", 10)
        c.drawCentredString(mx, my - 3.5, label)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(mx + dx * off, my + dy * off + 8, tag)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawCentredString(mx + dx * off, my + dy * off - 2, dia_note)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        y = H * 0.42
        x_fan, x_join, x_end = 0.55 * inch, 3.3 * inch, 5.9 * inch

        # trunk A (largest, to collector) and main B (continues to pickups)
        self._duct(c, x_fan, y, x_join, y, 26, "Ø32", "A", "flanged")
        self._duct(c, x_join, y, x_end, y, 20, "Ø24", "B", "clamp")
        # lateral C at 45 deg
        self._duct(c, x_join, y, x_join + 1.55 * inch, y + 1.35 * inch, 15,
                   "Ø16", "C", "clamp", off=3.4)

        # airflow arrows
        ay = y - 0.82 * inch
        c.setStrokeColor(colors.HexColor("#7a7a7a"))
        c.setFillColor(colors.HexColor("#7a7a7a"))
        c.setLineWidth(0.9)
        for x0 in (x_end - 0.15 * inch, x_end - 1.15 * inch):
            c.line(x0, ay, x0 - 0.45 * inch, ay)
            p = c.beginPath()
            p.moveTo(x0 - 0.45 * inch, ay)
            p.lineTo(x0 - 0.33 * inch, ay + 0.04 * inch)
            p.lineTo(x0 - 0.33 * inch, ay - 0.04 * inch)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        c.setFont("Helvetica-Oblique", 8.5)
        c.drawRightString(x_end - 1.75 * inch, ay - 3, "airflow to filter / blower")

        # end callouts
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.05 * inch, y + 0.34 * inch, "TO FILTER + BLOWER")
        c.drawRightString(W - 0.02 * inch, y + 0.28 * inch, "to next pickup")
        c.drawString(x_join + 1.72 * inch, y + 1.18 * inch, "hood / machine drop")

        # flange break marker
        c.setStrokeColor(WARN)
        c.setDash(2, 2)
        c.setLineWidth(1)
        c.line(x_join, y - 0.35 * inch, x_join, y + 0.35 * inch)
        c.setDash()
        c.setFillColor(WARN)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x_join - 0.15 * inch, y - 0.48 * inch,
                            "flange break: above 25 = flanged")


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(0.8 * inch, LETTER[1] - 0.62 * inch, LETTER[0] - 0.8 * inch,
                LETTER[1] - 0.62 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(0.8 * inch, LETTER[1] - 0.55 * inch,
                      "Nederman Ducting — Field Labeling Guide")
    canvas.drawRightString(LETTER[0] - 0.8 * inch, LETTER[1] - 0.55 * inch,
                           "UWP — Air Pollution Control")
    canvas.line(0.8 * inch, 0.72 * inch, LETTER[0] - 0.8 * inch, 0.72 * inch)
    canvas.drawString(0.8 * inch, 0.55 * inch, "Rev A")
    canvas.drawCentredString(LETTER[0] / 2.0, 0.55 * inch,
                             "Label it in the shop — not on the lift.")
    canvas.drawRightString(LETTER[0] - 0.8 * inch, 0.55 * inch,
                           "Page %d" % doc.page)
    canvas.restoreState()


story = []
A = story.append

# ---------------------------------------------------------------- cover block
A(Paragraph("Nederman Ducting", SUB))
A(Paragraph("Field Labeling Guide", TITLE))
A(Paragraph("How to mark, key and sequence duct before it leaves the shop", SUB))
A(Spacer(1, 8))
A(Rule())
A(Spacer(1, 4))
A(Paragraph(
    "Per Karl's direction, every piece of Nederman duct gets labeled before it "
    "ships. This is the standard: what goes on the piece, how the runs are keyed, "
    "and how the numbers are sequenced so a crew can lay the whole system out on "
    "the floor and build it in order without a print in their hand.",
    BODY))
A(Spacer(1, 2))

# ------------------------------------------------------------------- the rules
A(Paragraph("1. The five rules", H1))
A(Paragraph(
    "Everything below comes out of these. If you remember nothing else, remember "
    "these five.", BODY))

rules = [
    ["R1", Paragraph("<b>Write the diameter on every piece.</b> No exceptions — "
                     "straights, elbows, reducers, laterals, blast gates, hoods. "
                     "A piece with no diameter on it is an unlabeled piece.", CELL)],
    ["R2", Paragraph("<b>Sequence small to large.</b> Numbering starts at the "
                     "smallest piece farthest from the fan and counts up toward the "
                     "trunk. The crew installs in that same order.", CELL)],
    ["R3", Paragraph("<b>Key the ducts.</b> Every run gets a letter off the drawing. "
                     "Main trunk is A. Laterals and Y-branches get their own letter, "
                     "not a share of the main's.", CELL)],
    ["R4", Paragraph("<b>Above 25 goes to flange.</b> Anything larger than 25 is "
                     "flanged construction, not quick-clamp. Mark the size on the "
                     "flange face so it stays readable once the piece is rigged and "
                     "the body is against the ceiling.", CELL)],
    ["R5", Paragraph("<b>Mark both ends.</b> One end is always the end you can't see "
                     "once it's up.", CELL)],
]
A(grid([[Paragraph("<b>%s</b>" % r[0], CELLB), r[1]] for r in rules],
       [0.4 * inch, 6.3 * inch], header=False))

A(callout(
    "Confirm the units before the first crate ships",
    "The sketch reads 32 / 24 / 16 and the rule reads “above 25.” That is "
    "consistent with the Nederman quick-connect break — clamp-together up to "
    "250&nbsp;mm, flanged at 280&nbsp;mm and above — and it is equally "
    "consistent with inches. This guide writes the bare number the way the sketch "
    "does, so it is correct either way. Pick one unit for the whole job, state it "
    "once on the drawing, and never mix the two on a label."))

# ---------------------------------------------------------------- label format
A(Paragraph("2. The label", H1))
A(Paragraph("Every piece carries the same four fields, in the same order:", BODY))
A(Spacer(1, 2))

fmt = Table([[Paragraph("SYSTEM", CELLB), Paragraph("RUN", CELLB),
              Paragraph("SEQ", CELLB), Paragraph("DIA", CELLB)],
             [Paragraph("DC1", CELLM), Paragraph("A", CELLM),
              Paragraph("03", CELLM), Paragraph("Ø32", CELLM)],
             [Paragraph("which collector /<br/>system it belongs to", SMALL),
              Paragraph("letter off the<br/>drawing", SMALL),
              Paragraph("build order,<br/>small → large", SMALL),
              Paragraph("outside diameter,<br/>always with Ø", SMALL)]],
            colWidths=[1.7 * inch, 1.6 * inch, 1.6 * inch, 1.8 * inch], hAlign="LEFT")
fmt.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, RULE),
    ("BACKGROUND", (0, 0), (-1, 0), BAND),
    ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f7fafd")),
    ("ALIGN", (0, 0), (-1, 1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
A(fmt)
A(Spacer(1, 6))
A(Paragraph("Written out on the piece:", H2))
A(Paragraph("DC1-A-03-Ø32", MONO))
A(Paragraph(
    "Add length in inches after the diameter when the piece is a cut straight and "
    "two lengths on the job could be confused — <font face='Courier-Bold'>"
    "DC1-A-03-Ø32-96</font>. Fittings don't need a length; they need their "
    "type instead (see §5).", BODY))

A(Paragraph("Assigning the letters", H2))
A(bullets([
    "<b>A is the trunk at the collector</b> — the biggest pipe, closest to the "
    "filter and blower. Letters walk outward from there: A, then B, then C.",
    "<b>A lateral or Y gets the next free letter</b>, not a sub-number of the main. "
    "A 16 branch dropping off the 24 main is run C, not B-2. When the crew is "
    "hunting a piece on a crowded floor, a letter is faster to find than a suffix.",
    "<b>The letter never changes size mid-run.</b> If the diameter steps, the run "
    "ends and a new letter starts at the reducer. That is what makes the label "
    "self-checking: two pieces with the same letter and different diameters means "
    "somebody mislabeled one of them.",
]))

# ------------------------------------------------------------------- example
A(KeepTogether([
    Paragraph("3. Worked example — Karl's sketch", H1),
    Paragraph(
        "This is the branch off the field sketch: a 32 trunk running to the filter "
        "and blower, a 24 main continuing out to the next pickup, and a 16 lateral "
        "dropping to a machine hood. Three sizes, three letters.", BODY),
    Spacer(1, 4),
    Schematic(),
    Spacer(1, 6),
]))

A(grid([
    [Paragraph("<b>Run</b>", CELLB), Paragraph("<b>Dia</b>", CELLB),
     Paragraph("<b>What it is</b>", CELLB), Paragraph("<b>Connection</b>", CELLB),
     Paragraph("<b>Label reads</b>", CELLB)],
    [Paragraph("A", CELL), Paragraph("32", CELL),
     Paragraph("Trunk — junction back to filter / blower", CELL),
     Paragraph("<b>Flanged</b> (>25)", CELL), Paragraph("DC1-A-03-Ø32", CELLM)],
    [Paragraph("B", CELL), Paragraph("24", CELL),
     Paragraph("Main — junction out to next pickup", CELL),
     Paragraph("Quick clamp", CELL), Paragraph("DC1-B-02-Ø24", CELLM)],
    [Paragraph("C", CELL), Paragraph("16", CELL),
     Paragraph("Lateral / Y — drop to machine hood", CELL),
     Paragraph("Quick clamp", CELL), Paragraph("DC1-C-01-Ø16", CELLM)],
], [0.55 * inch, 0.5 * inch, 2.5 * inch, 1.35 * inch, 1.8 * inch]))
A(Spacer(1, 6))
A(Paragraph(
    "Read the sequence numbers and the build order falls out of them: hang C first "
    "(01, the 16 at the hood), then B (02, the 24 main), then A (03, the 32 into the "
    "collector). Small to large, exactly as Karl called it — the crew works from "
    "the machines back to the fan, and the heavy flanged pipe goes up last, when the "
    "lift already has clear floor under it.", BODY))
A(Spacer(1, 2))
A(Paragraph(
    "The Y itself gets labeled too, on the body, with all three legs called out: "
    "<font face='Courier-Bold'>DC1-Y-Ø32xØ24xØ16</font>. Write the "
    "legs in the order trunk × main × branch so the fitter knows which port "
    "faces the fan before they wrestle it onto the strut.", BODY))

# ----------------------------------------------------------- where to mark
A(KeepTogether([Paragraph("4. Where and how to mark", H1), grid([
    [Paragraph("<b>Situation</b>", CELLB), Paragraph("<b>Where the mark goes</b>", CELLB)],
    [Paragraph("Straight duct, 25 and under (clamp)", CELL),
     Paragraph("Both ends, on the outside of the pipe, roughly 6″ back from "
               "each end so the clamp band doesn't cover it. Repeat the full label "
               "once at mid-length for anything over 8 feet.", CELL)],
    [Paragraph("Straight duct, above 25 (flanged)", CELL),
     Paragraph("<b>On the flange face</b>, per R4 — both flanges — plus "
               "once on the body. The flange stays visible from the floor after the "
               "piece is rigged; the body may not.", CELL)],
    [Paragraph("Elbows, reducers, laterals, Y", CELL),
     Paragraph("On the body, on the outside of the sweep where it will face down or "
               "out once installed. Never on the inside of a bend.", CELL)],
    [Paragraph("Blast gates, dampers", CELL),
     Paragraph("On the frame, next to the handle — not on the blade or the "
               "moving plate.", CELL)],
    [Paragraph("Hoods and machine drops", CELL),
     Paragraph("On the collar, plus the machine name or number the hood serves. "
               "This is the one label the plant's own maintenance crew will read "
               "for the next ten years.", CELL)],
], [2.0 * inch, 4.7 * inch])]))
A(Spacer(1, 4))
A(Paragraph("Marking method", H2))
A(bullets([
    "<b>Silver or white paint marker on galvanized and painted duct; black on "
    "stainless or bare bright.</b> Permanent marker fades off galv in a few weeks "
    "of shop light and disappears completely on an outdoor lay-down yard.",
    "<b>Print, don't script.</b> Caps, 2″ tall minimum on anything 16 and up. "
    "It has to be readable from the floor when the piece is on the ceiling.",
    "<b>Back the paint marker up with a tag on anything that ships loose</b> — "
    "wire-on weatherproof tag with the same label written on it. Paint gets scuffed "
    "off in transit; a tag survives.",
    "<b>Never label over a seam, weld, or the sealing face of a gasket.</b> Paint on "
    "a flange gasket face is a leak path.",
]))

# ------------------------------------------------------------ fittings & extras
A(Paragraph("5. Fittings — what else goes on the label", H1))
A(Paragraph(
    "Straights are identified by diameter and length. Fittings are identified by "
    "diameter and <i>type</i>, because two 24 elbows are not interchangeable if one "
    "is a 45 and one is a 90.", BODY))
A(Spacer(1, 2))
A(grid([
    [Paragraph("<b>Fitting</b>", CELLB), Paragraph("<b>Add to the label</b>", CELLB),
     Paragraph("<b>Example</b>", CELLB)],
    [Paragraph("Elbow", CELL), Paragraph("Angle and centerline radius", CELL),
     Paragraph("DC1-B-04-Ø24-90°-R1.5D", CELLM)],
    [Paragraph("Reducer", CELL), Paragraph("Both diameters, large first", CELL),
     Paragraph("DC1-A-05-RED-Ø32xØ24", CELLM)],
    [Paragraph("Lateral / Y", CELL), Paragraph("All legs: trunk × main × branch", CELL),
     Paragraph("DC1-Y-Ø32xØ24xØ16", CELLM)],
    [Paragraph("Blast gate", CELL), Paragraph("Diameter and the machine it isolates", CELL),
     Paragraph("DC1-C-BG-Ø16-SANDER 2", CELLM)],
    [Paragraph("Hood / drop", CELL), Paragraph("Collar diameter and machine", CELL),
     Paragraph("DC1-C-HD-Ø16-SANDER 2", CELLM)],
    [Paragraph("Flex hose", CELL), Paragraph("Diameter and cut length", CELL),
     Paragraph("DC1-C-FLX-Ø16-36", CELLM)],
], [1.15 * inch, 3.05 * inch, 2.5 * inch]))

# ------------------------------------------------------------ crates
A(KeepTogether([Paragraph("6. Crates, bundles and the pack list", H1), bullets([
    "<b>Crate by run, not by size.</b> One crate holds run C complete — duct, "
    "elbows, gate, hood, clamps, gaskets. The crew opens one box and hangs one "
    "branch. Sorting a crate of mixed 16s across four runs is where a day gets lost.",
    "<b>Stencil the crate with the system and the runs inside</b> — "
    "<font face='Courier-Bold'>DC1 / RUN C / PCS 01-07</font> — on two adjacent "
    "sides, so it reads however the forklift sets it down.",
    "<b>Pack list goes inside the crate and a copy in the shipping sleeve</b>, listing "
    "every label in the crate. That list is the receiving check and the punch list "
    "for anything short-shipped.",
    "<b>Load in reverse install order.</b> Highest sequence numbers go in the truck "
    "first so the smallest, first-installed pieces come off the truck first.",
])]))

# ------------------------------------------------------------ QC
A(Paragraph("7. Before it ships — QC check", H1))
check = [
    "Every piece has a diameter on it, both ends.",
    "Every piece above 25 is flanged, and the size is marked on the flange face.",
    "Run letters match the drawing exactly — no run letter reused, no size "
    "change inside a letter.",
    "Sequence numbers run small to large with no gaps and no duplicates.",
    "Fittings carry their type: angle, both reducer sizes, all three Y legs.",
    "Every hood and blast gate names its machine.",
    "Marks are paint, not permanent marker, and legible from twenty feet.",
    "Loose pieces carry a wire tag matching the painted label.",
    "Crates stencilled on two sides; pack list inside and in the sleeve.",
    "A marked-up copy of the drawing ships with the load, showing the same "
    "letters and numbers as the pieces.",
]
rows = [[Checkbox(), Paragraph(t, CELL)] for t in check]
A(grid(rows, [0.32 * inch, 6.38 * inch], header=False))

A(Spacer(1, 8))
A(Paragraph("8. The mistakes that cost a day", H1))
A(grid([
    [Paragraph("<b>Mistake</b>", CELLB), Paragraph("<b>What it costs</b>", CELLB)],
    [Paragraph("Labeling on the lift instead of in the shop", CELL),
     Paragraph("Two people and a lift tied up doing paperwork at height. Label on "
               "the bench where it takes seconds.", CELL)],
    [Paragraph("Marking one end only", CELL),
     Paragraph("The unmarked end goes up, and the next fitter has to guess or take "
               "a tape to it in the air.", CELL)],
    [Paragraph("Numbering large to small", CELL),
     Paragraph("Crew starts at the fan and works out. Every joint downstream then "
               "has to carry the weight of everything not yet hung.", CELL)],
    [Paragraph("Reusing a run letter after a size change", CELL),
     Paragraph("Two different pieces answer to the same label. Guaranteed wrong "
               "piece on the lift at least once.", CELL)],
    [Paragraph("Mixing units on one job", CELL),
     Paragraph("A “25” that means millimeters in the shop and inches in "
               "the field is a scrapped fitting.", CELL)],
    [Paragraph("Trusting the label and skipping the drawing", CELL),
     Paragraph("Labels tell you what a piece is, not where it goes. The marked-up "
               "drawing ships with the crate for a reason.", CELL)],
], [2.35 * inch, 4.35 * inch]))

# ------------------------------------------------------------------ bench card
A(Spacer(1, 14))
A(Paragraph("9. Bench card", H1))
A(Paragraph("Print this page, cut on the line, pin it over the layout bench.", BODY))
A(Spacer(1, 6))

CARDH = S("cardh", fontName="Helvetica-Bold", fontSize=13, leading=16,
          textColor=INK, spaceAfter=2)
CARDBIG = S("cardbig", fontName="Courier-Bold", fontSize=19, leading=23,
            textColor=ACCENT, spaceAfter=2)
CARDR = S("cardr", fontName="Helvetica", fontSize=9.5, leading=13.5,
          textColor=INK, spaceAfter=3)

card_left = [
    Paragraph("EVERY PIECE, EVERY TIME", CARDH),
    Spacer(1, 4),
    Paragraph("DC1-A-03-Ø32", CARDBIG),
    Paragraph("system &nbsp;–&nbsp; run &nbsp;–&nbsp; seq &nbsp;–&nbsp; diameter",
              SMALL),
    Spacer(1, 8),
    Paragraph("<b>Both ends.</b> Paint marker, caps, 2″ tall.", CARDR),
    Paragraph("<b>Above 25 → flanged.</b> Size goes on the flange face.", CARDR),
    Paragraph("<b>Fittings add their type:</b> 90°, RED-Ø32xØ24, "
              "Y-Ø32xØ24xØ16.", CARDR),
    Paragraph("<b>Gates and hoods add the machine name.</b>", CARDR),
]
card_right = [
    Paragraph("THE FIVE RULES", CARDH),
    Spacer(1, 4),
    Paragraph("1. &nbsp;Write the diameter on every piece.", CARDR),
    Paragraph("2. &nbsp;Sequence small to large — 01 is the far pickup, "
              "the last number is the trunk at the fan.", CARDR),
    Paragraph("3. &nbsp;Key every run with a letter. A = trunk. "
              "A lateral or Y gets its own letter.", CARDR),
    Paragraph("4. &nbsp;Above 25 goes to flange — mark the flange.", CARDR),
    Paragraph("5. &nbsp;Mark both ends.", CARDR),
    Spacer(1, 6),
    Paragraph("One letter = one diameter. If the size steps, "
              "the run letter steps with it.", SMALL),
]
cardtbl = Table([[card_left, card_right]],
                colWidths=[3.35 * inch, 3.35 * inch], hAlign="LEFT")
cardtbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOX", (0, 0), (-1, -1), 1.2, ACCENT),
    ("LINEAFTER", (0, 0), (0, 0), 0.6, RULE),
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbfcfe")),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
A(KeepTogether(cardtbl))

A(Spacer(1, 10))
A(Rule())
A(Paragraph(
    "Rev A — drafted from Karl's labeling direction and the field sketch "
    "(32 trunk / 24 main / 16 lateral). Confirm the unit convention and the exact "
    "flange break with Karl before the first crate ships, then this becomes the "
    "shop standard for all Nederman duct.", SMALL))


doc = BaseDocTemplate(
    OUT, pagesize=LETTER,
    leftMargin=0.8 * inch, rightMargin=0.8 * inch,
    topMargin=0.85 * inch, bottomMargin=0.9 * inch,
    title="Nederman Ducting - Field Labeling Guide",
    author="UWP - Air Pollution Control",
    subject="Duct labeling standard",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])
doc.build(story)
print("wrote", OUT)
