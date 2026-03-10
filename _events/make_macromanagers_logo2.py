"""
Generate assets/images/macromanagers-logo2.svg

Logo row (left → right, all centered at y=300):
  KRTK (PNG)  |  CEU (vector)  |  koren.dev (SVG inline)  |  coded thinking (SVG inline)  |  Bead (PNG)

Run from the repo root:
    python _events/make_macromanagers_logo2.py
"""
import base64, urllib.request, os, re

REPO   = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(REPO, "assets", "images")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_b64(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return base64.b64encode(urllib.request.urlopen(req).read()).decode()


def read_svg_parts(path, new_clip_id):
    """
    Parse a local SVG and return (defs_content, body_content)
    with all clip-path IDs renamed to `new_clip_id` to avoid conflicts.
    """
    with open(path) as f:
        src = f.read()
    # Rename any clip-path IDs
    old_id_m = re.search(r'id="(clip[^"]+)"', src)
    if old_id_m:
        old_id = old_id_m.group(1)
        src = src.replace(f'id="{old_id}"', f'id="{new_clip_id}"')
        src = src.replace(f'url(#{old_id})', f'url(#{new_clip_id})')
    # Extract <defs> inner content
    defs_m  = re.search(r'<defs>(.*?)</defs>', src, re.DOTALL)
    defs_inner = defs_m.group(1).strip() if defs_m else ""
    # Extract body (everything except the outer <svg> and <defs>)
    body = re.sub(r'<svg[^>]*>',           '', src,  count=1)
    body = re.sub(r'</svg>',               '', body)
    body = re.sub(r'<defs>.*?</defs>', '', body, flags=re.DOTALL)
    return defs_inner, body.strip()


# ---------------------------------------------------------------------------
# Fetch / load assets
# ---------------------------------------------------------------------------

print("Fetching KRTK logo…")
krtk_b64 = fetch_b64(
    "https://krtk.elte.hu/wp-content/uploads/2021/03/Group-491@2x-300x44.png")

print("Loading Bead logo…")
with open(os.path.join(ASSETS, "bead-zip.jpg"), "rb") as _f:
    bead_b64 = base64.b64encode(_f.read()).decode()
bead_mime = "image/jpeg"

print("Reading koren-dev.svg…")
kdev_defs, kdev_body = read_svg_parts(
    os.path.join(ASSETS, "koren-dev.svg"), "kdev_clip")

print("Reading koren-ct.svg…")
kct_defs, kct_body = read_svg_parts(
    os.path.join(ASSETS, "koren-ct.svg"), "kct_clip")


# ---------------------------------------------------------------------------
# CEU vector paths
# Extracted from https://macromanagers.eu/assets/images/logo.svg (clip1 group)
# Original bounding box: x=211.969..273.214, y=24.25..75.113  (w=61.245 h=50.863)
#   orig_cx = (211.969+273.214)/2 = 242.59
#   orig_cy = (24.25+75.113)/2    = 49.68
#
# Centered at (1027, 114), scale=0.75:
#   tx = 1027 - 242.59*0.75 = 845.06
#   ty =  114 -  49.68*0.75 =  76.74
# ---------------------------------------------------------------------------
# SVG is 1200×450 (= 16:6 ratio), matching the container exactly so object-cover
# does NOT crop horizontally. Badge covers 112px rendered = 112/s SVG px.
# At narrowest sm viewport (C=592): s=592/1200=0.493, badge=227px → x=260 clears it.
CEU_TRANSFORM = "translate(845.06 87.74) scale(0.75)"  # y-center=125 (cap center of MACROMANAGERS at y=144)

CEU_PATHS = """
    <path d="M235.217 44.7213C235.759 44.1081 236.609 43.8009 237.482 43.8009C238.073 43.8009 238.309 44.0372 241.66 45.7836L243.572 43.7772C242.32 41.6764 239.914 40.45 237.482 40.45C233.541 40.45 230.378 43.541 230.378 47.3408V51.1419C230.378 54.8698 233.541 58.0092 237.482 58.0092C239.914 58.0092 242.32 56.758 243.572 54.6583L241.66 52.652C238.309 54.422 238.073 54.6346 237.482 54.6346C236.609 54.6346 235.759 54.3511 235.217 53.7131C234.697 53.1471 234.697 52.8647 234.697 52.2503V46.1841C234.697 45.5945 234.697 45.2873 235.217 44.7213Z" fill="#1D1D40"/>
    <path d="M245.459 57.5607H257.449V54.1389H249.637V50.7406H256.057V47.3649H249.637V44.2739H257.449V40.8982H245.459V57.5607Z" fill="#1D1D40"/>
    <path d="M269.061 40.8982V51.1423C269.061 51.1559 269.063 51.1694 269.063 51.1829C269.063 51.1975 269.061 51.2098 269.061 51.2245V51.256H269.058C269.02 52.6637 267.869 53.7957 266.45 53.7957C265.007 53.7957 263.838 52.6266 263.838 51.1829C263.838 51.1423 263.843 51.103 263.844 51.0625V40.8982H259.691V51.471C259.691 54.9884 262.712 58.0097 266.441 58.0097C270.194 58.0097 273.214 54.9884 273.214 51.471V40.8982L269.061 40.8982Z" fill="#1D1D40"/>
    <path d="M236.955 24.25C235.915 24.25 234.537 24.3603 234.537 24.3603L236.955 31.1848L239.366 24.3637C239.366 24.3637 238.397 24.25 236.955 24.25Z" fill="#1D1D40"/>
    <path d="M247.583 26.387L246.683 32.9753L251.763 28.8051C251.763 28.8051 250.984 28.2177 249.733 27.4965C248.835 26.9766 247.583 26.387 247.583 26.387Z" fill="#1D1D40"/>
    <path d="M236.948 67.2913L234.537 74.1113C234.537 74.1113 235.504 74.2261 236.948 74.2261C237.985 74.2261 239.366 74.1147 239.366 74.1147L236.948 67.2913Z" fill="#1D1D40"/>
    <path d="M215.347 36.6597C214.827 37.5599 214.234 38.8089 214.234 38.8089L221.352 40.1277L216.651 34.6287C216.651 34.6287 216.068 35.4107 215.347 36.6597Z" fill="#00A9D5"/>
    <path d="M211.969 49.2521C211.969 50.2919 212.081 51.6703 212.081 51.6703L218.904 49.2521L212.083 46.8408C212.083 46.8408 211.969 47.8096 211.969 49.2521Z" fill="#1D1D40"/>
    <path d="M215.291 61.7012C215.811 62.6014 216.595 63.7402 216.595 63.7402L221.296 58.2344L214.184 59.5554C214.184 59.5554 214.57 60.4522 215.291 61.7012Z" fill="#1D1D40"/>
    <path d="M224.561 70.9468C225.461 71.4678 226.71 72.0596 226.71 72.0596L228.028 64.9414L222.53 69.6426C222.53 69.6426 223.312 70.2255 224.561 70.9468Z" fill="#1D1D40"/>
    <path d="M249.718 70.7358C250.618 70.216 251.757 69.4317 251.757 69.4317L246.251 64.7305L247.572 71.8431C247.572 71.8431 248.469 71.4571 249.718 70.7358Z" fill="#1D1D40"/>
    <path d="M224.735 27.3899C223.834 27.9098 222.696 28.6952 222.696 28.6952L228.203 33.3953L226.88 26.2827C226.88 26.2827 225.984 26.6686 224.735 27.3899Z" fill="#1D1D40"/>
"""

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
# Canvas: 1200 x 400  (16:6 aspect with object-cover; date badge ~112px left)
#
# object-cover math: scale≈0.6 at 640px container → crop ~67px + badge 112/0.6=187px
# → safe content start: x=260.  Right edge: x=1080 (120px white space).
# Usable zone: x=260..1080  (820px wide)
#
# TOP SECTION  (y=8..215, MACROMANAGERS cap-center y=114)
#   MACROMANAGERS title:  x=260  y=140  font-size=52  (ends ~x=700)
#   Vertical divider:     x=820  y=30   h=175
#   KRTK PNG (140x21):    x=827  y=103  (centered in zone 820..975, y-center=114)
#   Vertical divider:     x=975  y=30   h=175
#   CEU vector (scale=0.75, center 1027,114) — zone 975..1080
#     tx = 1027 - 242.59*0.75 = 845.06
#     ty =  114 -  49.68*0.75 =  76.74
#
# SEPARATOR  y=215  x=260  w=820
#
# BOTTOM ROW  (y=225..385) — 3 equal zones of 273px each (260..1080)
#   Zone 1: x=260..533   → Bead 100×100   cx=396  x=346  y=255
#   Zone 2: x=533..806   → coded thinking  scale=0.7 (106×70)  cx=669  x=616  y=270
#   Zone 3: x=806..1080  → koren.dev       scale=0.7 (164×70)  cx=943  x=861  y=270
#   Dividers at x=533, x=806  y=225  h=155
# ---------------------------------------------------------------------------

svg = f"""<svg width="1200" height="450" viewBox="0 0 1200 450" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {kdev_defs}
    {kct_defs}
  </defs>

  <!-- Background -->
  <rect width="1200" height="450" fill="white"/>
  <rect width="1200" height="8" fill="#1D1D40"/>
  <rect y="442" width="1200" height="8" fill="#1D1D40"/>

  <!-- MACROMANAGERS title -->
  <text x="260" y="144" font-family="Arial, Helvetica, sans-serif"
        font-size="52" font-weight="700" fill="#1D1D40" letter-spacing="3">MACROMANAGERS</text>

  <!-- Vertical dividers in top section -->
  <rect x="820" y="30" width="1" height="207" fill="#CBD5E1"/>
  <rect x="975" y="30" width="1" height="207" fill="#CBD5E1"/>

  <!-- KRTK logo (140x21, centered in zone 820..975, y-center=125) -->
  <image href="data:image/png;base64,{krtk_b64}"
         x="827" y="115" width="140" height="21"
         preserveAspectRatio="xMidYMid meet"/>

  <!-- CEU vector paths (scale=0.75, centered at 1027,125) -->
  <g transform="{CEU_TRANSFORM}">{CEU_PATHS}
  </g>

  <!-- Separator -->
  <rect x="260" y="242" width="820" height="1" fill="#E2E8F0"/>

  <!-- Bottom row dividers -->
  <rect x="533" y="252" width="1" height="170" fill="#CBD5E1"/>
  <rect x="806" y="252" width="1" height="170" fill="#CBD5E1"/>

  <!-- Zone 1: Bead (100×100, cx=396, x=346, y=297) -->
  <image href="data:image/jpeg;base64,{bead_b64}"
         x="346" y="297" width="100" height="100"
         preserveAspectRatio="xMidYMid meet"/>

  <!-- Zone 2: coded thinking (scale=0.7 → 106×70, cx=669, x=616, y=312) -->
  <g transform="translate(616 312) scale(0.7)">
    {kct_body}
  </g>

  <!-- Zone 3: koren.dev (scale=0.7 → 164×70, cx=943, x=861, y=312) -->
  <g transform="translate(861 312) scale(0.7)">
    {kdev_body}
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
out = os.path.join(ASSETS, "macromanagers-logo2.svg")
with open(out, "w") as f:
    f.write(svg)
print(f"Written {len(svg):,} chars  →  {out}")
