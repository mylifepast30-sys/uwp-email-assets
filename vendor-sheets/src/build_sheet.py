#!/usr/bin/env python3
"""Build the UWP -> Dendratec stair tread vendor price request sheet."""
import base64, pathlib

HERE = pathlib.Path(__file__).parent

def b64(p):
    return base64.b64encode((HERE / p).read_bytes()).decode()

UWP_LOGO = b64("uwp_logo.png")
DEN_LOGO = b64("dendratec_logo.png")

TEAL = "#104A4E"

# ---------------------------------------------------------------- profiles
# Side-view cross sections. Nose at left. viewBox 0 0 120 44 (thick treads)
def svg_bullnose(s=1.0):
    return """<svg viewBox="0 0 120 44" class="pf"><path d="M18 8 H112 V36 H18 A14 14 0 0 1 18 8 Z"
      fill="#EAF1F0" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/></svg>""" % TEAL

def svg_square():
    return """<svg viewBox="0 0 120 44" class="pf"><path d="M10 8 H112 V36 H10 Z"
      fill="#EAF1F0" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/></svg>""" % TEAL

def svg_eased():
    # 1/8" bevel top & bottom on the nose edge
    return """<svg viewBox="0 0 120 44" class="pf"><path d="M17 8 H112 V36 H17 L10 29 V15 Z"
      fill="#EAF1F0" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/></svg>""" % TEAL

def svg_retro_bull():
    # 1" nose, 5/8" body
    return """<svg viewBox="0 0 120 44" class="pf"><path d="M22 8 H46 V19 H112 V33 H46 V36 H22 A14 14 0 0 1 22 8 Z"
      fill="#EAF1F0" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/></svg>""" % TEAL

def svg_retro_sq():
    return """<svg viewBox="0 0 120 44" class="pf"><path d="M12 8 H46 V19 H112 V33 H46 V36 H12 Z"
      fill="#EAF1F0" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/></svg>""" % TEAL

def svg_mr():
    # plan view: reversible 45 deg mitered return
    return """<svg viewBox="0 0 120 44" class="pf"><path d="M8 8 H112 V36 H8 Z" fill="#EAF1F0"
      stroke="%s" stroke-width="2.4" stroke-linejoin="round"/>
      <path d="M8 20 L20 8 M112 20 L100 8" stroke="%s" stroke-width="2" fill="none" opacity=".55"/></svg>""" % (TEAL, TEAL)

# ---------------------------------------------------------------- data
# (sku, size, species, profile-label)
FAMILIES = [
    dict(
        code="8070", name="ROUND BULLNOSE", art=svg_bullnose(),
        spec='1" full bullnose nosing &nbsp;·&nbsp; 1-1/32" thick &nbsp;·&nbsp; 11-1/2" depth',
        wrap=False,
        groups=[
            ("RED OAK", [
                ("8070RO42",  '1-1/32" × 11-1/2" × 42"',  "Red Oak", "Bullnose"),
                ("8070RO48",  '1-1/32" × 11-1/2" × 48"',  "Red Oak", "Bullnose"),
                ("8070RO60",  '1-1/32" × 11-1/2" × 60"',  "Red Oak", "Bullnose"),
                ("8070RO72",  '1-1/32" × 11-1/2" × 72"',  "Red Oak", "Bullnose"),
                ("8070RO84",  '1-1/32" × 11-1/2" × 84"',  "Red Oak", "Bullnose"),
                ("8070RO96",  '1-1/32" × 11-1/2" × 96"',  "Red Oak", "Bullnose"),
                ("8070RO48MR",'1-1/32" × 11-1/2" × 48"',  "Red Oak", "MR · 45° Rev."),
                ("8070RO60MR",'1-1/32" × 11-1/2" × 60"',  "Red Oak", "MR · 45° Rev."),
            ]),
            ("WHITE OAK", [
                ("8070WO42",  '1-1/32" × 11-1/2" × 42"',  "White Oak", "Bullnose"),
                ("8070WO48",  '1-1/32" × 11-1/2" × 48"',  "White Oak", "Bullnose"),
                ("8070WO60",  '1-1/32" × 11-1/2" × 60"',  "White Oak", "Bullnose"),
                ("8070WO48MR",'1-1/32" × 11-1/2" × 48"',  "White Oak", "MR · 45° Rev."),
                ("8070WO60MR",'1-1/32" × 11-1/2" × 60"',  "White Oak", "MR · 45° Rev."),
            ]),
            ("WIDE TREADS &amp; PLATFORM LANDINGS", [
                ("807020RO48", '1-1/32" × 20" × 48"', "Red Oak",   "Bullnose · Wide"),
                ("807030RO60", '1-1/32" × 30" × 60"', "Red Oak",   "Bullnose · Wide"),
                ("807030WO60", '1-1/32" × 30" × 60"', "White Oak", "Bullnose · Wide"),
                ("807048RO48", '1-1/32" × 48" × 48"', "Red Oak",   "Bullnose · Landing"),
                ("807048WO48", '1-1/32" × 48" × 48"', "White Oak", "Bullnose · Landing"),
            ]),
        ]),
    dict(
        code="8072", name="SQUARE EDGE", art=svg_square(),
        spec='Square nosing, eased 1/16" arris &nbsp;·&nbsp; 1-1/32" thick &nbsp;·&nbsp; 11-1/2" depth',
        wrap=False,
        groups=[
            ("RED OAK", [
                ("8072RO42",  '1-1/32" × 11-1/2" × 42"', "Red Oak", "Square"),
                ("8072RO48",  '1-1/32" × 11-1/2" × 48"', "Red Oak", "Square"),
                ("8072RO60",  '1-1/32" × 11-1/2" × 60"', "Red Oak", "Square"),
                ("8072RO48MR",'1-1/32" × 11-1/2" × 48"', "Red Oak", "MR · 45° Rev."),
                ("8072RO60MR",'1-1/32" × 11-1/2" × 60"', "Red Oak", "MR · 45° Rev."),
            ]),
            ("WHITE OAK", [
                ("8072WO42",  '1-1/32" × 11-1/2" × 42"', "White Oak", "Square"),
                ("8072WO48",  '1-1/32" × 11-1/2" × 48"', "White Oak", "Square"),
                ("8072WO60",  '1-1/32" × 11-1/2" × 60"', "White Oak", "Square"),
                ("8072WO48MR",'1-1/32" × 11-1/2" × 48"', "White Oak", "MR · 45° Rev."),
                ("8072WO60MR",'1-1/32" × 11-1/2" × 60"', "White Oak", "MR · 45° Rev."),
            ]),
            ("WIDE TREADS &amp; PLATFORM LANDINGS", [
                ("807220RO48",  '1-1/32" × 22" × 48"', "Red Oak",   "Square · Wide"),
                ("807230RO60",  '1-1/32" × 30" × 60"', "Red Oak",   "Square · Wide"),
                ("807230WO60",  '1-1/32" × 30" × 60"', "White Oak", "Square · Wide"),
                ("807248RO48",  '1-1/32" × 48" × 48"', "Red Oak",   "Square · Landing"),
                ("807248WO48",  '1-1/32" × 48" × 48"', "White Oak", "Square · Landing"),
            ]),
        ]),
    dict(
        code="8072 EE", name="EASED EDGE", art=svg_eased(),
        spec='1" eased edge, 1/8" bevel &nbsp;·&nbsp; 1-1/32" thick &nbsp;·&nbsp; 11-1/2" depth',
        wrap=False, isnew=True,
        groups=[
            ("RED OAK", [
                ("8072RO42EE",  '1-1/32" × 11-1/2" × 42"', "Red Oak", "Eased Edge"),
                ("8072RO48EE",  '1-1/32" × 11-1/2" × 48"', "Red Oak", "Eased Edge"),
                ("8072RO60EE",  '1-1/32" × 11-1/2" × 60"', "Red Oak", "Eased Edge"),
                ("8072RO48MREE",'1-1/32" × 11-1/2" × 48"', "Red Oak", "EE · MR 45° Rev."),
                ("8072RO60MREE",'1-1/32" × 11-1/2" × 60"', "Red Oak", "EE · MR 45° Rev."),
            ]),
            ("WHITE OAK", [
                ("8072WO42EE",  '1-1/32" × 11-1/2" × 42"', "White Oak", "Eased Edge"),
                ("8072WO48EE",  '1-1/32" × 11-1/2" × 48"', "White Oak", "Eased Edge"),
                ("8072WO60EE",  '1-1/32" × 11-1/2" × 60"', "White Oak", "Eased Edge"),
                ("8072WO48MREE",'1-1/32" × 11-1/2" × 48"', "White Oak", "EE · MR 45° Rev."),
                ("8072WO60MREE",'1-1/32" × 11-1/2" × 60"', "White Oak", "EE · MR 45° Rev."),
            ]),
            ("WIDE TREADS &amp; PLATFORM LANDINGS", [
                ("807230RO60EE", '1-1/32" × 30" × 60"', "Red Oak",   "EE · Wide"),
                ("807230WO60EE", '1-1/32" × 30" × 60"', "White Oak", "EE · Wide"),
                ("807248RO48EE", '1-1/32" × 48" × 48"', "Red Oak",   "EE · Landing"),
                ("807248WO48EE", '1-1/32" × 48" × 48"', "White Oak", "EE · Landing"),
            ]),
        ]),
    dict(
        code="8071", name="RETRO BULLNOSE", art=svg_retro_bull(),
        spec='1" bullnose nose &nbsp;·&nbsp; 5/8" body &nbsp;·&nbsp; 11-1/2" depth',
        wrap=True,
        groups=[
            ("RED OAK &amp; WHITE OAK", [
                ("8071RO42",   '1" × 5/8" × 11-1/2" × 42"', "Red Oak",   "Retro Bullnose"),
                ("8071RO48",   '1" × 5/8" × 11-1/2" × 48"', "Red Oak",   "Retro Bullnose"),
                ("8071WO42",   '1" × 5/8" × 11-1/2" × 42"', "White Oak", "Retro Bullnose"),
                ("8071WO48",   '1" × 5/8" × 11-1/2" × 48"', "White Oak", "Retro Bullnose"),
                ("807120RO48", '1" × 5/8" × 20" × 48"',     "Red Oak",   "Retro BN · Wide"),
            ]),
        ]),
    dict(
        code="8073", name="SQUARE RETRO-FIT", art=svg_retro_sq(),
        spec='1" square nose &nbsp;·&nbsp; 5/8" body &nbsp;·&nbsp; 11-1/2" depth',
        wrap=True,
        groups=[
            ("RED OAK &amp; WHITE OAK", [
                ("8073RO42",   '1" × 5/8" × 11-1/2" × 42"', "Red Oak",   "Square Retro-Fit"),
                ("8073RO48",   '1" × 5/8" × 11-1/2" × 48"', "Red Oak",   "Square Retro-Fit"),
                ("8073WO42",   '1" × 5/8" × 11-1/2" × 42"', "White Oak", "Square Retro-Fit"),
                ("8073WO48",   '1" × 5/8" × 11-1/2" × 48"', "White Oak", "Square Retro-Fit"),
                ("807348RO48", '1" × 5/8" × 48" × 48"',     "Red Oak",   "Sq. R-F · Landing"),
                ("807348WO48", '1" × 5/8" × 48" × 48"',     "White Oak", "Sq. R-F · Landing"),
            ]),
        ]),
]


def render_family(f):
    rows = []
    badge = ""
    if f.get("isnew"):
        badge = '<span class="badge-new">NEW</span>'
    if f.get("wrap"):
        badge += '<span class="badge-wrap">WRAP REQ\'D</span>'
    rows.append(f'''
    <tr class="fam"><td colspan="7">
      <div class="famrow">
        <div class="famart">{f["art"]}</div>
        <div class="famtxt">
          <div class="famname"><b>{f["code"]}</b><span class="famsep"></span>{f["name"]}{badge}</div>
          <div class="famspec">{f["spec"]}</div>
        </div>
      </div>
    </td></tr>''')
    for gname, items in f["groups"]:
        rows.append(f'<tr class="grp"><td colspan="7">{gname}</td></tr>')
        for sku, size, sp, prof in items:
            mark = '<span class="wmark">▣</span>' if f.get("wrap") else ""
            rows.append(f'''
      <tr>
        <td class="c-qty"></td>
        <td class="c-sku">{sku}{mark}</td>
        <td class="c-size">{size}</td>
        <td class="c-sp">{sp}</td>
        <td class="c-prof">{prof}</td>
        <td class="c-stock"></td>
        <td class="c-price"><span class="dol">$</span></td>
      </tr>''')
    return "".join(rows)


def table(families, cont=False):
    head = f'''
  <table class="items">
    <colgroup>
      <col style="width:60px"><col style="width:102px"><col>
      <col style="width:66px"><col style="width:100px">
      <col style="width:62px"><col style="width:80px">
    </colgroup>
    <thead>
      <tr class="hd">
        <th class="c-qty"><small>ANDY · UWP</small>QTY (EA)</th>
        <th class="c-sku">SKU</th>
        <th class="c-size">SIZE &nbsp;(THK × DEPTH × LENGTH)</th>
        <th class="c-sp">SPECIES</th>
        <th class="c-prof">PROFILE</th>
        <th class="c-stock"><small>DENDRATEC</small>IN STOCK</th>
        <th class="c-price"><small>&nbsp;</small>UNIT $/EA</th>
      </tr>
    </thead>
    <tbody>{"".join(render_family(f) for f in families)}</tbody>
  </table>'''
    return head


def page_head_compact(label):
    return f'''
  <header class="ph ph-c">
    <div class="ph-l">
      <img class="logo" src="data:image/png;base64,{UWP_LOGO}" alt="Unique Wood Products">
      <div class="ph-ctitle">STAIR TREADS<span>Vendor Price Request &nbsp;·&nbsp; Unfinished</span></div>
    </div>
    <div class="ph-cr">
      <span class="ph-cont">{label}</span>
      <img class="denlogo" src="data:image/png;base64,{DEN_LOGO}" alt="Dendratec">
    </div>
  </header>'''


def page_head(n, total, sub=""):
    return f'''
  <header class="ph">
    <div class="ph-l">
      <img class="logo" src="data:image/png;base64,{UWP_LOGO}" alt="Unique Wood Products">
      <div class="ph-tag">Moulding&nbsp; ·&nbsp; Stair Parts&nbsp; ·&nbsp; Millwork</div>
    </div>
    <div class="ph-r">
      <div class="ph-kicker">Vendor Price Request</div>
      <h1>STAIR TREADS<span>UNFINISHED · RED &amp; WHITE OAK</span></h1>
      <div class="ph-meta">
        <span>PREPARED FOR</span>
        <img class="denlogo" src="data:image/png;base64,{DEN_LOGO}" alt="Dendratec">
      </div>
    </div>
  </header>'''


PARTIES = f'''
  <section class="parties">
    <div class="pt pt-uwp">
      <div class="pt-cap"><i></i>SHIP TO &nbsp;/&nbsp; BUYER — completed by UWP</div>
      <div class="pt-body">
        <div class="pt-name">UNIQUE WOOD PRODUCTS</div>
        <div class="pt-addr">9915 Tanner Road · Houston, TX 77041<br>
          Acct 130 · Branch HOU1 · T 713.462.5045 · F 713.462.5086</div>
        <div class="fills">
          <label>BUYER<em>Andy Tong</em></label>
          <label>ORDER DATE<em></em></label>
          <label>REQ'D SHIP DATE<em></em></label>
          <label>PO / REFERENCE<em></em></label>
        </div>
      </div>
    </div>
    <div class="pt pt-den">
      <div class="pt-cap"><i></i>SUPPLIER — completed by Dendratec</div>
      <div class="pt-body">
        <div class="pt-name">DENDRATEC TECHNOLOGIES</div>
        <div class="pt-addr">3551 St Charles Blvd, Suite 114<br>
          Kirkland, QC &nbsp;H9H 3C4 &nbsp;· &nbsp;Canada</div>
        <div class="fills">
          <label>CONTACT<em></em></label>
          <label>QUOTE DATE<em></em></label>
          <label>QUOTE VALID UNTIL<em></em></label>
          <label>MILL / ORIGIN<em></em></label>
        </div>
      </div>
    </div>
  </section>
  <div class="howto">
    <span class="ht-l">◀ &nbsp;<b>ANDY</b> enters quantity</span>
    <span class="ht-c">All pricing <b>UNFINISHED</b> and truckload. Quote every line or mark <b>N/A</b>. Freight terms on page 2.</span>
    <span class="ht-r"><b>DENDRATEC</b> enters stock on hand + unit price&nbsp; ▶</span>
  </div>'''


def profile_key():
    cells = []
    for f in FAMILIES:
        tag = '<b class="pk-new">NEW</b>' if f.get("isnew") else (
              '<b class="pk-wrap">&#9635;</b>' if f.get("wrap") else "")
        dim = f["spec"].split("&nbsp;·&nbsp;")[0]
        cells.append(
            '<div class="pk"><div class="pk-art">' + f["art"] + '</div>'
            '<div class="pk-code">' + f["code"] + tag + '</div>'
            '<div class="pk-name">' + f["name"] + '</div>'
            '<div class="pk-dim">' + dim + '</div></div>')
    return ('<section class="pkey"><div class="pk-cap">PROFILE KEY</div>'
            '<div class="pk-row">' + "".join(cells) + '</div></section>')


WRAP_NOTE = '''
  <section class="wrapnote">
    <div class="wn-icon">▣</div>
    <div class="wn-body">
      <div class="wn-h">8071 &amp; 8073 RETRO-FIT — PLASTIC WRAP REQUIRED, PRICED IN</div>
      <p>The 5/8" body on 8071 and 8073 cups in Houston humidity. Every 8071 and 8073 tread must ship
      <b>fully wrapped in plastic</b> — 4-side enclosure, min. 6 mil, with a continuous vapor sheet above and
      below each pallet layer. No exposed end grain, no partial wraps, no outdoor staging. End-coat all
      lengths 60" and over. UWP will reject at receiving for visible cupping, face checking, or MC variance.</p>
      <p class="wn-price"><b>Plastic wrap must be included in the unit price quoted on this sheet.</b>
      Do not quote it as a separate adder or leave it out to reach a target price — a price without wrap
      will not be accepted for these two profiles.</p>
    </div>
  </section>'''


NOTES = '''
  <section class="notes">
    <div class="nt">
      <h4>Abbreviations</h4>
      <p><b>EE</b> — Eased Edge, 1/8" bevel<br>
         <b>MR</b> — Miter Return, 45°, reversible left/right<br>
         <b>Wide</b> — extra-depth tread &nbsp;·&nbsp; <b>Landing</b> — platform tread<br>
         <b>&#9635;</b> — plastic wrap required (8071 / 8073)</p>
    </div>
    <div class="nt">
      <h4>Pricing basis</h4>
      <p>Truckload (FTL) volume, <b>unfinished</b> only, USD per each.<br>
         Price every line or mark <b>N/A</b>. Note substitutes where a size is unavailable.<br>
         <b>8071 / 8073 prices must include plastic wrap.</b><br>
         Lead time <b>3–5 weeks</b>, up to 6 when busy.</p>
    </div>
    <div class="nt">
      <h4>Ship to</h4>
      <p>Unique Wood Products · 9915 Tanner Road<br>
         Houston, TX 77041 &nbsp;·&nbsp; Attn: Andy Tong<br>
         Return completed sheet to <b>orders@uniquewoodproducts.com</b></p>
    </div>
  </section>'''


TERMS = '''
  <section class="terms">
    <div class="tm tm-den">
      <div class="tm-cap">FREIGHT &amp; LEAD TIME — Dendratec completes</div>
      <div class="tm-grid">
        <label>FULL TRUCKLOAD (FTL) RATE TO HOUSTON, TX 77041<em>$</em></label>
        <label>LEAD TIME THIS ORDER (WEEKS)<em></em></label>
        <label>TRANSIT DAYS TO HOUSTON<em></em></label>
        <label>FOB TERMS (ORIGIN / DESTINATION)<em></em></label>
        <label>PIECES PER BUNDLE<em></em></label>
        <label>PAYMENT TERMS OFFERED<em></em></label>
      </div>
      <div class="tm-confirm">
        <div class="tmc">
          <b>Plastic wrap for 8071 / 8073 included in the unit prices above?</b>
          <span class="yn">YES <i></i> &nbsp;&nbsp; NO <i></i></span>
        </div>
        <div class="tmc tmc-note">Standing lead time agreed with Dendratec: <b>3–5 weeks, up to 6 when
          busy.</b> Note above if this order runs longer.</div>
      </div>
    </div>
  </section>'''


SIGS = '''
  <section class="terms">
    <div class="sigs">
      <div class="sig">
        <div class="sig-line"></div>
        <div class="sig-cap">UWP AUTHORIZED SIGNATURE<span>Andy Tong · Unique Wood Products</span></div>
      </div>
      <div class="sig sig-d">
        <div class="sig-line"></div>
        <div class="sig-cap">DENDRATEC AUTHORIZED SIGNATURE<span>Name &amp; title · date</span></div>
      </div>
    </div>
  </section>'''


SPECS = '''
  <section class="specs">
    <h2>MILL SUPPLY SPECIFICATION</h2>
    <div class="spec-grid">
      <div class="sp">
        <h3>Species &amp; Grade</h3>
        <ul>
          <li>Red Oak <i>(Quercus rubra)</i> · White Oak <i>(Quercus alba)</i></li>
          <li>Select Grade or better per CS 89-40. Face and nosing clear, free of sapwood.</li>
          <li>Glued-up stock matched for color and grain. Max two streaks per tread, 6" max length.</li>
        </ul>
      </div>
      <div class="sp">
        <h3>Stave Construction</h3>
        <ul>
          <li>3 to 5 staves maximum per tread, color-matched and grain-blended.</li>
          <li>No visible contrast between adjacent staves. No heartwood-to-sapwood transitions on the face.</li>
          <li>Glue joints tight, flush and continuous. Face grain consistent across all staves.</li>
        </ul>
      </div>
      <div class="sp">
        <h3>Face, Nosing &amp; Defects</h3>
        <ul>
          <li>Face and nosing smooth — no mill marks, chipped grain, torn fiber or skip milling.</li>
          <li>Nosing consistent and sharp. No feathering or rollover at the profile edge.</li>
          <li>Knots: sound and tight, 3/4" max dia., 2 per piece. Checks: 1/4 length max, no through splits.
              Holes: spot-worm 1/16" max, 1 per lineal foot.</li>
        </ul>
      </div>
      <div class="sp">
        <h3>Moisture, Labeling &amp; Packaging</h3>
        <ul>
          <li>Kiln-dried to 6–8% EMC prior to machining.</li>
          <li>Each bundle labeled: species, grade, size, MC, mill name.</li>
          <li>Banded on pallets with edge protection, wrapped loads only. End-coat all lengths 60"+.</li>
          <li><b>8071 / 8073 — full plastic wrap required (see above).</b></li>
        </ul>
      </div>
    </div>
    <div class="exempt"><b>Technology exemption.</b> Suppliers using certified moisture-management technology
      (engineered stabilization, sealed surface systems, or proprietary equivalent) may request a wrap exemption
      with prior written UWP approval. Documentation required before shipment.</div>
  </section>'''


CSS = """
@page { size: Letter; margin: 0; }
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font:400 10px/1.4 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:#111A1D;background:#8a8a8a}
.page{width:8.5in;height:11in;background:#fff;padding:.42in .45in .40in;display:flex;flex-direction:column;
      position:relative;overflow:hidden;page-break-after:always}
.page:last-child{page-break-after:auto}
.foot{position:absolute;left:.45in;right:.45in;bottom:.24in;display:flex;justify-content:space-between;
      align-items:center;border-top:1px solid #E3E8E7;padding-top:5px;font-size:7.2px;letter-spacing:.09em;
      color:#8B9998;text-transform:uppercase}
.foot b{color:#104A4E;font-weight:600}

/* ---------- header ---------- */
.ph{display:flex;justify-content:space-between;align-items:flex-start;
    border-bottom:2.5px solid #104A4E;padding-bottom:11px;margin-bottom:13px}
.ph-l{display:flex;flex-direction:column;gap:7px}
.logo{height:62px;width:auto;display:block}
.ph-tag{font-size:7.4px;letter-spacing:.15em;color:#5C6D6C;text-transform:uppercase;white-space:nowrap}
.ph-r{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.ph-kicker{font-size:8px;letter-spacing:.3em;text-transform:uppercase;color:#8A9A99}
.ph-r h1{font-size:25px;letter-spacing:.03em;font-weight:300;color:#104A4E;line-height:1;
         display:flex;flex-direction:column;align-items:flex-end;gap:5px}
.ph-r h1 span{font-size:8px;letter-spacing:.22em;font-weight:600;color:#111A1D}
.ph-meta{display:flex;align-items:center;gap:9px;margin-top:5px;padding-top:7px;
         border-top:1px solid #E3E8E7;width:100%;justify-content:flex-end}
.ph-meta span{font-size:7px;letter-spacing:.2em;color:#9AA8A7}
.denlogo{height:26px;width:auto;display:block}

/* compact header for continuation pages */
.ph-c{align-items:center;border-bottom-width:1.5px;padding-bottom:8px;margin-bottom:12px}
.ph-c .ph-l{flex-direction:row;align-items:center;gap:13px}
.ph-c .logo{height:38px}
.ph-ctitle{font-size:13px;letter-spacing:.11em;font-weight:600;color:#104A4E;line-height:1.25;
           border-left:1px solid #DCE3E2;padding-left:13px}
.ph-ctitle span{display:block;font-size:7.2px;letter-spacing:.15em;text-transform:uppercase;
                color:#8A9A99;font-weight:400;margin-top:2px}
.ph-cr{display:flex;align-items:center;gap:14px}
.ph-cont{font-size:7.2px;letter-spacing:.15em;text-transform:uppercase;color:#9AA8A7}
.ph-c .denlogo{height:19px}

/* ---------- parties ---------- */
.parties{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:0}
.pt{border:1px solid #DCE3E2;border-radius:3px;overflow:hidden}
.pt-cap{font-size:7.2px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;
        padding:5px 8px;display:flex;align-items:center;gap:6px}
.pt-cap i{width:6px;height:6px;border-radius:50%;display:block}
.pt-uwp .pt-cap{background:#EDF4F3;color:#104A4E}
.pt-uwp .pt-cap i{background:#104A4E}
.pt-den .pt-cap{background:#F4F1EC;color:#6B5B44}
.pt-den .pt-cap i{background:#8A7355}
.pt-body{padding:7px 8px 8px}
.pt-name{font-size:11px;font-weight:700;letter-spacing:.05em;color:#111A1D}
.pt-addr{font-size:8.2px;line-height:1.5;color:#5C6D6C;margin-top:2px}
.fills{margin-top:7px;display:grid;grid-template-columns:1fr 1fr;gap:5px 10px}
.fills label{font-size:6.6px;letter-spacing:.11em;color:#94A2A1;text-transform:uppercase;
             display:flex;flex-direction:column;gap:1px}
.fills em{font-style:normal;font-size:9px;color:#111A1D;font-weight:600;
          border-bottom:1px solid #C9D3D2;min-height:14px;padding-top:2px}

.howto{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:9px 0 9px;
       padding:5px 9px;background:#F7FAF9;border:1px solid #E3EBEA;border-radius:3px;
       font-size:7.6px;color:#5C6D6C}
.howto b{font-weight:700;letter-spacing:.06em}
.ht-l{color:#104A4E;white-space:nowrap}
.ht-r{color:#6B5B44;white-space:nowrap}
.ht-c{text-align:center;flex:1}

/* ---------- profile key ---------- */
.pkey{margin:0 0 3px}
.pk-cap{font-size:6.8px;letter-spacing:.24em;color:#9AA8A7;text-transform:uppercase;font-weight:600;
        margin-bottom:5px}
.pk-row{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
.pk{border:1px solid #E3EBEA;border-radius:3px;padding:7px 8px 8px;background:#FCFDFD}
.pk-art{margin-bottom:4px}
.pk svg.pf{width:60px;height:22px}
.pk-code{font-size:9.5px;font-weight:700;color:#104A4E;letter-spacing:.04em;
         display:flex;align-items:center;gap:5px}
.pk-new{background:#104A4E;color:#fff;font-size:5.6px;font-weight:700;letter-spacing:.12em;
        padding:1.5px 4px;border-radius:2px}
.pk-wrap{color:#B08A3E;font-size:8px}
.pk-name{font-size:6.6px;letter-spacing:.13em;text-transform:uppercase;color:#111A1D;font-weight:600;
         margin-top:2px}
.pk-dim{font-size:6.8px;color:#8B9998;margin-top:2px;line-height:1.35}

/* ---------- items ---------- */
.items{width:100%;border-collapse:collapse;table-layout:fixed}
.items th,.items td{vertical-align:middle}
tr.hd th{font-size:7px;letter-spacing:.11em;text-transform:uppercase;color:#fff;background:#104A4E;
         padding:5px 7px 6px;text-align:left;font-weight:600;vertical-align:bottom}
tr.hd th small{display:block;font-size:5.8px;letter-spacing:.18em;font-weight:700;
               opacity:.62;margin-bottom:2px}
tr.hd th.c-qty{background:#0C3A3D;text-align:center}
tr.hd th.c-stock{background:#5F4E3A;text-align:center;padding-right:0}
tr.hd th.c-price{background:#5F4E3A;text-align:center;padding-left:0}
tr.hd th.c-sp,tr.hd th.c-prof{text-align:left}

tr.fam td{padding:12px 0 5px}
.famrow{display:flex;align-items:center;gap:12px;border-bottom:1.5px solid #104A4E;padding-bottom:6px;
        margin-left:62px}
.famart{width:70px;flex:0 0 70px}
svg.pf{width:70px;height:26px;display:block}
.famtxt{flex:1}
.famname{font-size:11.5px;letter-spacing:.05em;color:#104A4E;display:flex;align-items:center;gap:0}
.famname b{font-weight:700}
.famsep{display:inline-block;width:16px;height:1px;background:#B7C6C5;margin:0 8px}
.famspec{font-size:7.8px;color:#7A8988;margin-top:1.5px;letter-spacing:.03em}
.badge-new{margin-left:9px;background:#104A4E;color:#fff;font-size:6.4px;font-weight:700;
           letter-spacing:.14em;padding:2px 6px;border-radius:2px}
.badge-wrap{margin-left:7px;background:#F3EAD9;color:#7A5B22;border:1px solid #E0CDA6;font-size:6.4px;
            font-weight:700;letter-spacing:.12em;padding:1.5px 6px;border-radius:2px}

tr.grp td{font-size:6.8px;letter-spacing:.17em;text-transform:uppercase;color:#94A2A1;
          padding:7px 0 3px 62px;font-weight:600}

.items tbody tr td{border-bottom:1px solid #EDF1F0;padding:0 7px;height:19px;font-size:8.6px}
.items tbody tr.fam td,.items tbody tr.grp td{border-bottom:none;height:auto;padding-right:0}
.items tbody tr.fam td{padding-left:0}
.c-sku{font-weight:700;letter-spacing:.02em;font-size:8.4px}
.c-size{color:#5C6D6C;font-variant-numeric:tabular-nums}
.c-sp{color:#5C6D6C}
.c-prof{color:#5C6D6C;font-size:8px}
td.c-qty{background:#F2F7F6;border-left:2px solid #104A4E;border-bottom:1px solid #DFE9E8}
td.c-stock{background:#FAF7F1;border-left:2px solid #8A7355;border-bottom:1px solid #EBE3D5;
           border-right:1px solid #E6DCC9}
td.c-price{background:#FAF7F1;border-right:2px solid #8A7355;border-bottom:1px solid #EBE3D5;
           text-align:left;color:#B3A48D;font-weight:600}
tr.fam td.c-qty,tr.grp td.c-qty{background:none;border-left:none}
.wmark{color:#B08A3E;font-size:7px;margin-left:5px;vertical-align:1px}

/* ---------- wrap note ---------- */
.wrapnote{display:flex;gap:11px;align-items:flex-start;margin-top:13px;padding:10px 12px;
          background:#FBF6EC;border:1px solid #E3D3B0;border-left:3px solid #B08A3E;border-radius:3px}
.wn-icon{font-size:15px;color:#B08A3E;line-height:1}
.wn-h{font-size:9px;font-weight:700;letter-spacing:.11em;color:#7A5B22;text-transform:uppercase}
.wn-body p{font-size:8.2px;line-height:1.55;color:#6B5B44;margin-top:3px}
.wn-body b{color:#5A4519}
.wn-price{margin-top:5px !important;padding-top:5px;border-top:1px solid #E3D3B0}

/* freight confirm */
.tm-confirm{border-top:1px solid #EDE7DC;padding:8px 9px 9px;display:grid;
            grid-template-columns:1fr 1fr;gap:14px;align-items:center}
.tmc{font-size:7.8px;color:#6B5B44;line-height:1.5}
.tmc b{color:#5A4519}
.yn{display:inline-flex;align-items:center;gap:4px;margin-left:8px;font-size:7.4px;
    letter-spacing:.1em;font-weight:700;color:#6B5B44}
.yn i{display:inline-block;width:11px;height:11px;border:1px solid #B9A483;background:#fff;
      border-radius:2px;vertical-align:-2px}
.tmc-note{color:#8B7B63}

/* ---------- notes ---------- */
.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:15px;padding-top:12px;
       border-top:1px solid #E3E8E7}
.nt h4{font-size:6.8px;letter-spacing:.2em;text-transform:uppercase;color:#104A4E;font-weight:700;
       margin-bottom:4px}
.nt p{font-size:7.6px;line-height:1.65;color:#6E7E7D}
.nt b{color:#111A1D;font-weight:700}

/* ---------- terms ---------- */
.terms{margin-top:12px}
.tm{border:1px solid #DCE3E2;border-radius:3px;overflow:hidden}
.tm-cap{font-size:7.2px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;
        padding:5px 9px;background:#F4F1EC;color:#6B5B44}
.tm-grid{padding:9px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px 14px}
.tm-grid label{font-size:6.6px;letter-spacing:.11em;color:#94A2A1;text-transform:uppercase;
               display:flex;flex-direction:column;gap:1px}
.tm-grid em{font-style:normal;font-size:9px;color:#B3A48D;font-weight:600;
            border-bottom:1px solid #C9D3D2;min-height:17px;padding-top:2px}
.sigs{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:22px}
.sig-line{border-bottom:1px solid #6E7E7D;height:20px}
.sig-cap{font-size:6.8px;letter-spacing:.13em;text-transform:uppercase;color:#5C6D6C;font-weight:700;
         margin-top:4px;display:flex;flex-direction:column;gap:1px}
.sig-cap span{font-weight:400;letter-spacing:.04em;color:#9AA8A7;text-transform:none;font-size:7.4px}
.sig-d .sig-cap{color:#6B5B44}

/* ---------- specs ---------- */
.specs{margin-top:15px}
.specs h2{font-size:9px;letter-spacing:.22em;color:#104A4E;font-weight:700;text-transform:uppercase;
          border-bottom:1.5px solid #104A4E;padding-bottom:5px;margin-bottom:10px}
.spec-grid{display:grid;grid-template-columns:1fr 1fr;gap:11px 18px}
.sp h3{font-size:8.4px;letter-spacing:.09em;text-transform:uppercase;color:#111A1D;font-weight:700;
       margin-bottom:4px}
.sp ul{list-style:none;display:flex;flex-direction:column;gap:3px}
.sp li{font-size:8px;line-height:1.5;color:#5C6D6C;padding-left:9px;position:relative}
.sp li:before{content:"";position:absolute;left:0;top:5.5px;width:3px;height:3px;border-radius:50%;
              background:#B7C6C5}
.sp i{font-style:italic;color:#8B9998}
.exempt{margin-top:11px;padding:8px 10px;background:#F7FAF9;border:1px solid #E3EBEA;border-radius:3px;
        font-size:7.8px;line-height:1.55;color:#5C6D6C}
.exempt b{color:#104A4E}
"""


def foot(n, total):
    return (f'<div class="foot"><span><b>Unique Wood Products</b> &nbsp;·&nbsp; '
            f'Vendor Price Request &nbsp;·&nbsp; Stair Treads &nbsp;·&nbsp; Dendratec</span>'
            f'<span>uniquewoodproducts.com &nbsp;·&nbsp; Page {n} of {total}</span></div>')


TOTAL = 3

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>UWP · Dendratec — Stair Tread Vendor Price Request</title>
<style>{CSS}</style></head><body>

<div class="page">
  {page_head(1, TOTAL)}
  {PARTIES}
  {profile_key()}
  {table([FAMILIES[0]])}
  {NOTES}
  {foot(1, TOTAL)}
</div>

<div class="page">
  {page_head_compact("Price schedule &nbsp;·&nbsp; continued")}
  {table([FAMILIES[1], FAMILIES[2]])}
  {TERMS}
  {foot(2, TOTAL)}
</div>

<div class="page">
  {page_head_compact("Retro-fit treads &nbsp;·&nbsp; specification &amp; signatures")}
  {table([FAMILIES[3], FAMILIES[4]])}
  {WRAP_NOTE}
  {SPECS}
  {SIGS}
  {foot(3, TOTAL)}
</div>

</body></html>"""

out = HERE / "UWP_Dendratec_Stair_Tread_Quote_Request.html"
out.write_text(html)
print("wrote", out)
