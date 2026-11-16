import json, math, os, sys

ROOT = sys.argv[1]
REVIEW = {"status": "published", "technicallyValidated": False, "reviewer": "SewCraft editorial (sample)", "updated": "2026-11-14", "note": "Sample pattern; dimensions are internally consistent but not yet test-sewn."}

def T(name, **args): return {"type": "template", "name": name, "args": args}
def L(m): return {"type": "layout", "materialId": m}
def G(label="Finished!"): return {"type": "gallery", "index": 0, "label": label}
def M(label, value, unit="len"): return {"label": label, "value": value, "unit": unit}

def step(id, stage, title, text, visual, expert=None, beginner=None, meas=None, pieces=None, tech=None, tips=None, warn=None, timer=None):
    s = {"id": id, "stage": stage, "title": title, "text": text, "visual": visual}
    if expert: s["expert"] = expert
    if beginner: s["beginner"] = beginner
    if meas: s["measurements"] = meas
    if pieces: s["pieces"] = pieces
    if tech: s["techniques"] = tech
    if tips: s["tips"] = tips
    if warn: s["warnings"] = warn
    if timer: s["timerMin"] = timer
    return s

def fabric(id, name, swatch, why, rec, width, mode="folded", widths=None, weight=None, minw=None, alts=None, kind="fabric", required=True):
    m = {"id": id, "name": name, "kind": kind, "required": required, "recommended": rec, "why": why, "swatch": swatch,
         "layout": {"mode": mode, "defaultWidth": width, "widths": widths or [width]}}
    if weight: m["weight"] = weight
    if minw: m["minWidthCm"] = minw
    if alts: m["alternatives"] = alts
    return m

def notion(id, name, qty, why, swatch="#E8E0D2", alts=None, required=True):
    m = {"id": id, "name": name, "kind": "notion", "required": required, "quantity": qty, "why": why, "swatch": swatch}
    if alts: m["alternatives"] = alts
    return m

def piece(id, name, mat, qty, w, h, color, sa="sa", grain="lengthwise", fold=False, markings=None, notes=None):
    p = {"id": id, "name": name, "materialId": mat, "quantity": qty, "width": w, "height": h, "seamAllowance": sa, "grain": grain, "color": color}
    if fold: p["onFold"] = True
    if markings: p["markings"] = markings
    if notes: p["notes"] = notes
    return p

def ell(cx, cy, rx, ry, n=28):
    return [[round(cx + rx * math.cos(2 * math.pi * i / n), 1), round(cy + ry * math.sin(2 * math.pi * i / n), 1)] for i in range(n)]

def scene(*els): return {"els": list(els)}

def project(**kw):
    kw.setdefault("review", REVIEW)
    return kw

P = []

# ---------------------------------------------------------------- 1 scrunchie
P.append(project(
    id="scrunchie", title="Fabric Scrunchie", category="accessories", difficulty="beginner",
    summary="A soft, gathered hair tie — the perfect 30-minute scrap buster.",
    description="One strip of fabric and a short length of elastic. Sew a tube, thread the elastic, close the ring. You can sew it entirely by hand, and it's a great first project for using up leftover fabric.",
    tags=["accessories", "gifts", "beginner", "quick", "scraps", "upcycling", "hand-sewing"],
    minutes=[25, 40], costUSD=[1, 4], machineRequired=False, popularity=91, featured=True,
    constants={"sa": 1},
    finished={"label": "Finished scrunchie (approx.)", "dims": [{"label": "Tube width", "value": 4}, {"label": "Elastic loop", "value": 18.5}]},
    tools=["machine?", "hand-needle", "scissors", "pins", "safety-pin", "iron"],
    materials=[
        fabric("main", "Lightweight woven fabric", "#C98AA0", "Becomes the gathered tube.", ["Cotton lawn", "Rayon", "Satin", "Quilting cotton"], 112, "single", [50, 112, 140], weight="Light", alts=["A scrap at least 10 × 50 cm", "An old silk scarf"]),
        notion("elastic", "6 mm flat elastic", "20 cm", "Gives the stretch.", "#F1ECE4", ["Hair elastic, cut open"]),
        "thread"],
    pieces=[piece("tube", "Scrunchie strip", "main", 1, 10, 50, "#C98AA0", grain="any")],
    steps=[
        step("sc1", "prep", "Press your fabric", "Press the fabric smooth. Lightweight fabrics like lawn, rayon or satin gather softly; quilting cotton gives a fuller, puffier scrunchie.", T("press", tones=["main"], label="press flat"), tech=["pressing"]),
        step("sc2", "cut", "Cut the strip", "Cut one strip 10 × 50 cm. The direction doesn't matter much for a scrunchie, so place it wherever it fits your scrap.", L("main"), pieces=["tube"], warn=["Cut away from your body and keep fingers clear of the blades."]),
        step("sc3", "sew", "Sew the tube", "Fold the strip in half lengthwise, right sides together. Sew the long edge with a 1 cm seam, leaving both short ends open. Turn right side out with a safety pin.", T("tube", tone="main", label="sew the long edge, turn right side out"),
             beginner="By hand, use a small backstitch (about 3 mm stitches) — it's as strong as machine stitching. Attach a safety pin to one end and work it through the tube to turn it.",
             meas=[M("Seam allowance", "sa")], pieces=["tube"], tech=["seam-allowance", "backstitching"]),
        step("sc4", "assemble", "Thread the elastic", "Cut 20 cm of elastic. Pin a safety pin to one end and feed it through the tube. Pin the trailing end to the tube so it can't slip inside.", T("cord", tone="main", label="elastic through the tube"), meas=[M("Elastic length", 20)], pieces=["tube"], tech=["elastic-waistband"]),
        step("sc5", "assemble", "Join the elastic", "Check the elastic isn't twisted. Overlap the ends by 1.5 cm and zigzag back and forth several times, or hand-stitch firmly through both layers.", T("elastic", overlap=1.5), meas=[M("Overlap", 1.5)], tech=["zigzag-stitch"]),
        step("sc6", "finish", "Close the ring", "Fold 1 cm of one tube end to the inside. Tuck the other raw end into it by 1 cm and slip-stitch all the way round to join the tube into a ring.", T("close", tone="main", method="hand"), pieces=["tube"], tech=["ladder-stitch"],
             tips=["Spread the gathers away from the join before you stitch so it's easier to reach."]),
        step("sc7", "finish", "Shake out the gathers", "Spread the fabric evenly round the elastic. Make a few more — they make lovely small gifts.", G("Ready to wear")),
    ],
    gallery=[{"label": "Scrunchie", "scene": scene(
        {"k": "poly", "pts": ell(200, 150, 120, 100), "tone": "main"},
        {"k": "poly", "pts": ell(200, 150, 42, 34), "tone": "#FBF7F0"},
        *[{"k": "fold", "from": [round(200 + 50 * math.cos(a), 1), round(150 + 40 * math.sin(a), 1)], "to": [round(200 + 110 * math.cos(a), 1), round(150 + 92 * math.sin(a), 1)]} for a in [i * math.pi / 5 for i in range(10)]])}],
    related=["infinity-scarf", "headband", "zip-pouch"],
))

# ---------------------------------------------------------------- 2 napkins
P.append(project(
    id="cloth-napkins", title="Mitred Cloth Napkins (set of 4)", category="home", difficulty="beginner",
    summary="Everyday linen napkins with crisp mitred corners.",
    description="Napkins are the best way to master a perfect hem. Mitred corners lie flat and look professional, and once you've made four you'll never fear corners again. Choose your size; the hem allowance stays the same.",
    tags=["home", "gifts", "beginner", "table", "linen", "upcycling"],
    minutes=[75, 120], costUSD=[10, 25], machineRequired=True, popularity=72,
    constants={"hem": 2.5},
    params=[{"id": "N", "label": "Finished napkin size", "default": 45, "min": 35, "max": 55, "step": 5, "help": "35 cm cocktail · 45 cm everyday · 50+ cm dinner."}],
    sizes=[{"id": "cocktail", "label": "Cocktail 35", "values": {"N": 35}}, {"id": "everyday", "label": "Everyday 45", "values": {"N": 45}}, {"id": "dinner", "label": "Dinner 50", "values": {"N": 50}}],
    customNote="Each napkin is cut at the finished size plus 2 × 2.5 cm for a double-fold hem (1 cm + 1.5 cm). Hem allowance does not change with size.",
    finished={"label": "Finished napkin", "dims": [{"label": "Size (square)", "value": "N"}, {"label": "Hem width", "value": 1.5}]},
    tools=["machine", "rotary", "iron", "seam-gauge", "pins", "hand-needle?"],
    materials=[fabric("main", "Linen or cotton", "#B9A88E", "All four napkins.", ["Linen", "Cotton-linen", "Cotton poplin", "Chambray"], 140, "single", [112, 140, 150], weight="Light–medium", alts=["An old linen tablecloth or bedsheet"]), "thread"],
    pieces=[piece("napkin", "Napkin", "main", 4, "N + 2*hem", "N + 2*hem", "#B9A88E", sa="hem", markings=["Hem: press 1 cm, then 1.5 cm"])],
    steps=[
        step("n1", "prep", "Pre-wash and press", "Wash and dry the fabric — napkins get washed constantly and linen can shrink 5% or more. Press it flat.", T("press", tones=["main"]), tech=["prewash", "pressing"]),
        step("n2", "cut", "Cut four squares", "Cut four squares following the layout. Pull a thread or use a quilting ruler to keep them perfectly square — crooked napkins never press flat.", L("main"), pieces=["napkin"], tips=["Check squareness by measuring both diagonals; they must be equal."]),
        step("n3", "sew", "Press the hem folds", "On every edge, press 1 cm to the wrong side, then another 1.5 cm. Then unfold the second fold — you'll use the creases as guides for the mitre.", T("hem", tone="main", f1=1, f2=1.5, stitched=False),
             meas=[M("First fold", 1), M("Second fold", 1.5)], pieces=["napkin"], tech=["hemming", "pressing"], warn=["Keep fingertips clear of the iron when pressing narrow folds."]),
        step("n4", "sew", "Fold the mitred corners", "At each corner, fold the tip diagonally towards the centre so the fold passes exactly through the point where the inner creases cross. Press, trim the tip 7 mm beyond the fold, then refold both hems — the edges meet in a neat 45° line.", T("miter", tone="main"),
             beginner="Take it slowly on the first corner. The diagonal fold should line up with the creases on both sides; if it doesn't, unfold and adjust before you trim.", pieces=["napkin"], tech=["hemming"]),
        step("n5", "sew", "Stitch the hems", "Stitch close to the inner fold all the way round each napkin, from the wrong side, pivoting at each corner with the needle down.", T("topstitch", tone="main", dist=2.3), meas=[M("Stitch line from outer edge", 2.3), M("Stitch length", 2.5, "mm")], pieces=["napkin"], tech=["edgestitching"]),
        step("n6", "finish", "Close the mitres (optional)", "For the crispest corners, slip-stitch the diagonal mitre seams closed by hand so they never open in the wash.", T("hand", tone="main", stitch="ladder"), pieces=["napkin"], tech=["ladder-stitch"]),
        step("n7", "finish", "Final press", "Press all four napkins with steam. Fold them the same way and stack.", G("Set of four")),
    ],
    gallery=[{"label": "Stack", "scene": scene(
        {"k": "panel", "x": 110, "y": 70, "w": 200, "h": 180, "tone": "main"}, {"k": "panel", "x": 100, "y": 80, "w": 200, "h": 180, "tone": "main"}, {"k": "panel", "x": 90, "y": 90, "w": 200, "h": 180, "tone": "main"},
        {"k": "stitch", "pts": [[102, 102], [278, 102], [278, 258], [102, 258]], "closed": True})}],
    related=["table-runner", "envelope-cushion", "potholder"],
))

# ---------------------------------------------------------------- 3 pillowcase
P.append(project(
    id="pillowcase", title="Burrito-Method Pillowcase", category="home", difficulty="beginner",
    summary="A standard pillowcase with a contrast cuff and trim — every raw edge enclosed.",
    description="The 'burrito' roll hides the cuff seam completely, and French seams finish the sides, so the inside is as neat as the outside. Fits a standard 50 × 75 cm pillow.",
    tags=["home", "gifts", "beginner", "bedroom", "french seams"],
    minutes=[60, 90], costUSD=[12, 25], machineRequired=True, popularity=70,
    constants={"sa": 1},
    finished={"label": "Finished pillowcase", "dims": [{"label": "Width", "value": 52}, {"label": "Length", "value": 78}, {"label": "Cuff depth", "value": 22}]},
    tools=["machine", "rotary", "iron", "pins", "ruler"],
    materials=[
        fabric("main", "Body fabric", "#8FA3B8", "Main part of the case.", ["Quilting cotton", "Cotton percale", "Flannel"], 112, "single", [112, 140], minw=108),
        fabric("cuff", "Cuff fabric", "#E3C48D", "The wide band at the opening.", ["Quilting cotton"], 112, "single", [112, 140], minw=108),
        fabric("trim", "Accent trim fabric", "#B5727D", "Thin flat piping between body and cuff.", ["Quilting cotton"], 112, "single", [112, 140], minw=108),
        "thread"],
    pieces=[
        piece("body", "Body", "main", 1, 106, 58, "#8FA3B8", grain="any", notes="106 cm runs selvedge to selvedge."),
        piece("cuffp", "Cuff", "cuff", 1, 106, 46, "#E3C48D", grain="any"),
        piece("trimp", "Trim strip", "trim", 1, 106, 8, "#B5727D", grain="any"),
    ],
    steps=[
        step("pc1", "prep", "Pre-wash and press", "Pre-wash all three fabrics together so they shrink the same, then press.", T("press", tones=["main", "cuff"]), tech=["prewash"]),
        step("pc2", "cut", "Cut the body", "Cut the body 106 × 58 cm, with the 106 cm running across the fabric.", L("main"), pieces=["body"]),
        step("pc3", "cut", "Cut the cuff", "Cut the cuff 106 × 46 cm.", L("cuff"), pieces=["cuffp"]),
        step("pc4", "cut", "Cut the trim", "Cut the trim strip 106 × 8 cm.", L("trim"), pieces=["trimp"]),
        step("pc5", "sew", "Press the trim in half", "Fold the trim strip in half lengthwise, wrong sides together, and press.", T("fold", tone="trim", label="press in half lengthwise", dim=4), pieces=["trimp"], tech=["pressing"]),
        step("pc6", "assemble", "Roll the burrito", "Lay the cuff right side up. Along its top long edge, place the body right side up, then the folded trim, all raw edges together. Roll the body up towards the cuff edge, then bring the cuff's bottom edge up over the roll to meet the top edge. Pin all layers together — the body is wrapped inside the cuff like a burrito.",
             T("layer", base="cuff", top="main", label="cuff · body · trim — raw edges together"),
             beginner="It feels odd the first time. Check before pinning: the cuff's right side faces outwards and completely encloses the rolled-up body.", pieces=["cuffp", "body", "trimp"]),
        step("pc7", "assemble", "Sew the burrito seam", "Sew along the pinned edge through all layers with a 1 cm seam.", T("sew", tone="cuff", sides="t", label="sew through all layers"), meas=[M("Seam allowance", "sa")], pieces=["cuffp"], tech=["seam-allowance"]),
        step("pc8", "assemble", "Pull it through", "Reach into the tube and pull the body out. The cuff turns right side out with the seam fully enclosed. Press the cuff.", T("turn", tone="cuff", label="pull the body out through the cuff tube"), pieces=["body"]),
        step("pc9", "sew", "French seam — first pass", "Fold the case in half WRONG sides together, matching the cuff seams. Sew the side and bottom with a 0.5 cm seam. Trim the allowance to 3 mm and clip the corner.",
             T("sew", tone="main", sides="lb", label="WRONG sides together", sa=0.5), meas=[M("First seam", 0.5)], pieces=["body"], tech=["french-seam"]),
        step("pc10", "sew", "French seam — second pass", "Turn the case wrong side out, roll the seam exactly to the edge and press. Sew again 0.7 cm from the edge, enclosing the raw edges.", T("sew", tone="main", sides="lb", label="right sides together", sa=0.7), meas=[M("Second seam", 0.7)], pieces=["body"], tech=["french-seam"]),
        step("pc11", "finish", "Turn and press", "Turn right side out, push out the corners and give it a final press.", G()),
    ],
    gallery=[{"label": "Pillowcase", "scene": scene(
        {"k": "panel", "x": 40, "y": 80, "w": 230, "h": 150, "tone": "main", "rx": 6}, {"k": "panel", "x": 270, "y": 80, "w": 8, "h": 150, "tone": "trim"}, {"k": "panel", "x": 278, "y": 80, "w": 90, "h": 150, "tone": "cuff", "rx": 4})}],
    related=["envelope-cushion", "cloth-napkins"],
))

# ---------------------------------------------------------------- 4 gift bags
P.append(project(
    id="gift-bags", title="Drawstring Gift Bags", category="gifts", difficulty="beginner",
    summary="Reusable fabric gift wrap with a double drawstring — make any size.",
    description="Replace paper wrapping with bags that get used again and again. One folded rectangle, two side seams, a casing and a ribbon. Change the size for anything from jewellery to a bottle.",
    tags=["gifts", "beginner", "quick", "zero waste", "scraps"],
    minutes=[30, 45], costUSD=[2, 6], machineRequired=True, popularity=83,
    constants={"sa": 1, "cas": 2.5, "turn": 1},
    params=[{"id": "W", "label": "Finished width", "default": 20, "min": 10, "max": 35, "step": 1}, {"id": "H", "label": "Finished height", "default": 25, "min": 12, "max": 40, "step": 1}],
    sizes=[{"id": "small", "label": "Jewellery", "values": {"W": 12, "H": 15}}, {"id": "med", "label": "Book", "values": {"W": 20, "H": 25}}, {"id": "bottle", "label": "Bottle", "values": {"W": 18, "H": 38}}],
    customNote="The bag is one rectangle folded at the bottom: width + 2 seam allowances by 2 × (height + casing + turn-under). Casing depth stays 2.5 cm; ribbon length is 2 × width + 20 cm.",
    finished={"label": "Finished bag", "dims": [{"label": "Width", "value": "W"}, {"label": "Height", "value": "H"}]},
    tools=["machine", "scissors", "iron", "pins", "safety-pin"],
    materials=[fabric("main", "Cotton fabric", "#7F9473", "The bag.", ["Quilting cotton", "Linen", "Christmas prints"], 112, "single", [50, 112, 140], alts=["Scraps or an old shirt"]),
               notion("ribbon", "Ribbon or cord", "2 pieces, each {2*W + 20} long", "The drawstrings.", "#C0583A", ["Baker's twine", "Bias tape"]), "thread"],
    pieces=[piece("bag", "Bag", "main", 1, "W + 2*sa", "2*(H + cas + turn)", "#7F9473", markings=["Fold line across the middle = bag bottom", "Mark side-seam stop {cas + turn + 1} from each top edge"])],
    steps=[
        step("g1", "prep", "Press", "Press your fabric.", T("press", tones=["main"], label="press flat"), tech=["pressing"]),
        step("g2", "cut", "Cut one rectangle", "Cut a single rectangle — it folds in half to make the front, bottom and back.", L("main"), pieces=["bag"]),
        step("g3", "sew", "Sew the sides", "Fold the rectangle in half (the fold is the bottom), right sides together. Sew both sides with a 1 cm seam, starting at the fold and stopping at the mark below the top edge. Backstitch firmly at the stop.",
             T("sew", tone="main", sides="lr", label="fold = bottom · right sides together"), meas=[M("Seam allowance", "sa"), M("Stop below top edge", "cas + turn + 1")], pieces=["bag"], tech=["seam-allowance", "backstitching"]),
        step("g4", "sew", "Press open and secure the openings", "Press both seams open, including the unsewn sections at the top. Stitch round each little opening to hold the allowances flat.", T("edgestitch", tone="main", label="stitch round each side opening"), pieces=["bag"], tech=["pressing", "topstitching"]),
        step("g5", "sew", "Make the casing", "Press 1 cm to the wrong side all round the top, then another 2.5 cm. Stitch close to the lower fold, all the way round.", T("casing", tone="main", depth="cas", insert="none", gap=False), meas=[M("First fold", "turn"), M("Casing", "cas")], pieces=["bag"], tech=["casing"]),
        step("g6", "assemble", "Thread the ribbons", "Turn the bag right side out. Thread one ribbon in at the left opening, all the way round, and out the same side. Thread the second from the right. Knot each pair of ends.", T("cord", tone="main", label="one ribbon from each side"), meas=[M("Each ribbon", "2*W + 20")], tech=["casing"]),
        step("g7", "finish", "Fill and pull closed", "Pull both ribbons in opposite directions to close the bag.", G("Wrap it up")),
    ],
    gallery=[{"label": "Bag", "scene": scene(
        {"k": "poly", "pts": [[130, 80], [270, 80], [290, 270], [110, 270]], "tone": "main"}, {"k": "stitch", "pts": [[128, 100], [272, 100]]},
        {"k": "cord", "pts": [[200, 92], [180, 50], [160, 60]], "color": "#C0583A"}, {"k": "cord", "pts": [[200, 92], [222, 50], [244, 60]], "color": "#C0583A"})}],
    related=["drawstring-backpack", "scrunchie"],
))

# ---------------------------------------------------------------- 5 apron
P.append(project(
    id="apron", title="Classic Kitchen Apron", category="home", difficulty="beginner",
    summary="A full bib apron with a big front pocket and long waist ties.",
    description="Hemmed edges, straps and a patch pocket — skills that carry over into almost every other project. Sturdy cotton twill or canvas makes it last for years in the kitchen or workshop.",
    tags=["home", "clothing", "gifts", "beginner", "kitchen"],
    minutes=[120, 180], costUSD=[12, 25], machineRequired=True, popularity=78,
    constants={"sa": 1},
    finished={"label": "Finished apron", "dims": [{"label": "Width", "value": 65}, {"label": "Length", "value": 82}, {"label": "Ties (each)", "value": 82}]},
    tools=["machine", "needle-90", "scissors", "ruler", "marker", "pins", "iron", "seam-gauge?"],
    materials=[fabric("main", "Cotton twill or canvas", "#5E7C8A", "Body, ties and neck strap.", ["Cotton twill", "Light canvas", "Denim", "Linen"], 112, "single", [112, 140], weight="Medium"),
               fabric("pocket", "Pocket fabric", "#E3C48D", "Contrast pocket.", ["Quilting cotton", "Canvas"], 112, "single", [50, 112], alts=["Same as the body"]),
               "thread"],
    pieces=[piece("body", "Apron body", "main", 1, 70, 85, "#5E7C8A"), piece("ties", "Waist tie", "main", 2, 10, 85, "#46616D", sa=0),
            piece("neck", "Neck strap", "main", 1, 10, 62, "#46616D", sa=0), piece("pocketp", "Pocket", "pocket", 1, 32, 22, "#E3C48D")],
    steps=[
        step("ap1", "prep", "Pre-wash and press", "Pre-wash both fabrics and press.", T("press", tones=["main", "pocket"]), tech=["prewash"]),
        step("ap2", "cut", "Cut the body, ties and neck strap", "Cut the apron body, two waist ties and the neck strap with the long sides on the grain.", L("main"), pieces=["body", "ties", "neck"]),
        step("ap3", "cut", "Cut the pocket", "Cut the pocket from the contrast fabric.", L("pocket"), pieces=["pocketp"]),
        step("ap4", "sew", "Make the straps", "Press the neck strap and both ties into four-fold straps: in half lengthwise, open, edges to the centre, then in half again. On each tie, fold one short end in 1 cm before the final fold. Edgestitch both long edges.", T("strap", tone="ties", width=2.5),
             meas=[M("Finished strap width", 2.5)], pieces=["ties", "neck"], tech=["edgestitching", "pressing"]),
        step("ap5", "sew", "Hem the pocket", "Double-fold hem the top edge of the pocket (1 cm, then 2 cm) and stitch. Press the other three edges 1 cm to the wrong side.", T("hem", tone="pocket", f1=1, f2=2), meas=[M("First fold", 1), M("Second fold", 2)], pieces=["pocketp"], tech=["hemming"]),
        step("ap6", "sew", "Attach the pocket", "Centre the pocket on the apron body with its top 30 cm below the body's top edge. Edgestitch the sides and bottom, backstitching at the top corners. For two pockets, stitch a vertical line down the middle.", T("patch", base="main", patch="pocket", **{"from": 30}),
             meas=[M("Pocket top below apron top", 30)], pieces=["pocketp", "body"], tech=["edgestitching"]),
        step("ap7", "sew", "Hem the sides and bottom", "Double-fold hem both sides and the bottom of the body: press 1 cm, then 1.5 cm, and stitch close to the inner fold.", T("hem", tone="main", f1=1, f2=1.5), meas=[M("First fold", 1), M("Second fold", 1.5)], pieces=["body"], tech=["hemming"]),
        step("ap8", "assemble", "Hem the top and attach the neck strap", "Press the top edge 1 cm, then 2 cm. Tuck the neck strap ends under the second fold, 8 cm in from each side, check the strap isn't twisted, and stitch the hem. Flip the strap ends up and stitch across the hem again to lock them.", T("loops", base="main", strap="neck", dist=8),
             meas=[M("Strap ends from sides", 8)], pieces=["neck", "body"], tech=["attaching-straps"]),
        step("ap9", "assemble", "Attach the waist ties", "Tuck the raw end of a tie under each side hem, 30 cm below the top edge. Stitch a small box with an X through all layers.", T("edgestitch", tone="main", label="box-and-X over each tie end"), meas=[M("Tie position below top", 30)], pieces=["ties"], tech=["attaching-straps"]),
        step("ap10", "finish", "Press", "Give the apron a final press and trim threads.", G()),
    ],
    gallery=[{"label": "Apron", "scene": scene(
        {"k": "poly", "pts": [[150, 60], [250, 60], [250, 120], [300, 150], [300, 280], [100, 280], [100, 150], [150, 120]], "tone": "main"},
        {"k": "panel", "x": 150, "y": 175, "w": 100, "h": 60, "tone": "pocket"}, {"k": "cord", "pts": [[160, 62], [180, 20], [220, 20], [240, 62]], "color": "neck"},
        {"k": "cord", "pts": [[100, 152], [60, 170], [40, 220]], "color": "ties"}, {"k": "cord", "pts": [[300, 152], [340, 170], [360, 220]], "color": "ties"})}],
    related=["classic-tote", "potholder"],
))

# ---------------------------------------------------------------- 6 table runner
P.append(project(
    id="table-runner", title="Reversible Table Runner", category="home", difficulty="beginner",
    summary="Two fabrics, one seam all round — a fast, reversible table update.",
    description="Sew a top and a back together, turn, topstitch. Choose a seasonal print on one side and a plain on the other. Set it to the exact length of your table.",
    tags=["home", "gifts", "beginner", "quick", "table", "reversible"],
    minutes=[45, 75], costUSD=[10, 25], machineRequired=True, popularity=64,
    constants={"sa": 1},
    params=[{"id": "L", "label": "Finished length", "default": 150, "min": 90, "max": 200, "step": 5, "help": "Table length plus about 15–20 cm overhang each end."}, {"id": "W", "label": "Finished width", "default": 35, "min": 28, "max": 45, "step": 1}],
    sizes=[{"id": "small", "label": "Small table", "values": {"L": 110, "W": 32}}, {"id": "std", "label": "Standard", "values": {"L": 150, "W": 35}}, {"id": "long", "label": "Long table", "values": {"L": 190, "W": 38}}],
    customNote="Top and back are cut at finished size plus a 1 cm seam allowance on every side. The length runs along the grain so the runner hangs straight.",
    finished={"label": "Finished runner", "dims": [{"label": "Length", "value": "L"}, {"label": "Width", "value": "W"}]},
    tools=["machine", "rotary", "iron", "pins", "point-turner?"],
    materials=[fabric("top", "Top fabric", "#C26A4E", "Main side.", ["Quilting cotton", "Linen", "Cotton canvas (light)"], 112, "single", [112, 140]),
               fabric("back", "Back fabric", "#9DB09A", "Reverse side.", ["Quilting cotton", "Linen"], 112, "single", [112, 140]), "thread"],
    pieces=[piece("topp", "Runner top", "top", 1, "W + 2*sa", "L + 2*sa", "#C26A4E"), piece("backp", "Runner back", "back", 1, "W + 2*sa", "L + 2*sa", "#9DB09A")],
    steps=[
        step("r1", "prep", "Pre-wash and press", "Pre-wash both fabrics so the runner doesn't pucker after its first wash, and press.", T("press", tones=["top", "back"]), tech=["prewash"]),
        step("r2", "cut", "Cut the top", "Cut the top rectangle with the length along the grain.", L("top"), pieces=["topp"]),
        step("r3", "cut", "Cut the back", "Cut the back the same size.", L("back"), pieces=["backp"]),
        step("r4", "assemble", "Layer and pin", "Lay the top right side up and the back right side down on it. Match all edges and pin every 15 cm.", T("layer", base="top", top="back", label="right sides together, edges matched"), pieces=["topp", "backp"], tech=["seam-allowance"]),
        step("r5", "sew", "Sew all round", "Sew all round with a 1 cm seam, pivoting at each corner, leaving a 15 cm gap in one long side. Backstitch either side of the gap.", T("sew", tone="back", sides="ltrb", gap="r", gapLabel="15 cm gap"), meas=[M("Seam allowance", "sa"), M("Gap", 15)], pieces=["topp", "backp"], tech=["seam-allowance", "backstitching"]),
        step("r6", "sew", "Clip the corners", "Clip each corner diagonally, close to — but not through — the stitching.", T("clip", tone="back"), tech=["clipping-corners"]),
        step("r7", "assemble", "Turn and press", "Turn right side out through the gap, push the corners out and press, tucking the gap's allowances in line with the seam.", T("turn", tone="back"), tech=["pressing"]),
        step("r8", "finish", "Topstitch", "Topstitch 5 mm from the edge all round. This closes the gap and keeps the runner flat.", T("topstitch", tone="top", dist=0.5), meas=[M("Topstitch from edge", 0.5), M("Stitch length", 3, "mm")], pieces=["topp"], tech=["topstitching"]),
        step("r9", "finish", "Final press", "Press both sides.", G()),
    ],
    gallery=[{"label": "Runner", "scene": scene({"k": "poly", "pts": [[40, 200], [300, 80], [370, 110], [110, 230]], "tone": "top"}, {"k": "poly", "pts": [[110, 230], [370, 110], [370, 116], [110, 236]], "tone": "back"})}],
    related=["cloth-napkins", "envelope-cushion"],
))

# ---------------------------------------------------------------- 7 potholder
P.append(project(
    id="potholder", title="Quilted Pot Holder", category="home", difficulty="intermediate",
    summary="A heat-resistant quilted pot holder with bound edges and a hanging loop.",
    description="A small, practical introduction to quilting and binding. Insulated batting protects your hands; a grid of quilting holds the layers together, and a double-fold binding finishes the edges.",
    tags=["home", "gifts", "kitchen", "quilting", "binding"],
    minutes=[60, 100], costUSD=[5, 12], machineRequired=True, popularity=67,
    constants={"sa": 1},
    finished={"label": "Finished pot holder", "dims": [{"label": "Size (square)", "value": 20}, {"label": "Binding", "value": 1}]},
    tools=["machine", "walking-foot?", "rotary", "iron", "clips", "hand-needle?"],
    materials=[
        fabric("main", "Front fabric (100% cotton)", "#C26A4E", "Front.", ["Quilting cotton"], 112, "single", [50, 112]),
        fabric("back", "Back fabric (100% cotton)", "#E3C48D", "Back.", ["Quilting cotton"], 112, "single", [50, 112]),
        fabric("batt", "Insulated batting", "#D7DCDF", "Heat protection — two layers.", ["Heat-resistant insulated batting", "100% cotton batting (two layers)"], 112, "single", [56, 112], kind="interfacing", alts=["Two layers of cotton batting + one layer of old cotton towel"]),
        fabric("bind", "Binding fabric (100% cotton)", "#5E7C8A", "Binding and loop.", ["Quilting cotton"], 112, "single", [112]),
        "thread"],
    pieces=[piece("front", "Front", "main", 1, 22, 22, "#C26A4E", sa=1), piece("backp", "Back", "back", 1, 22, 22, "#E3C48D", sa=1),
            piece("battp", "Batting", "batt", 2, 22, 22, "#B9C1C6", sa=1), piece("binding", "Binding strip", "bind", 1, 95, 6, "#5E7C8A", sa=0, grain="any"),
            piece("loop", "Hanging loop", "bind", 1, 6, 12, "#46616D", sa=0, grain="any")],
    steps=[
        step("h1", "prep", "Press the fabrics", "Press all cotton fabrics. Use only 100% cotton fabric and thread for anything that touches hot pans.", T("press", tones=["main", "back"]), warn=["Polyester fabric or thread can melt against hot cookware — use 100% cotton."]),
        step("h2", "cut", "Cut the front", "Cut the front square.", L("main"), pieces=["front"]),
        step("h3", "cut", "Cut the back", "Cut the back square.", L("back"), pieces=["backp"]),
        step("h4", "cut", "Cut the batting", "Cut two squares of insulated batting.", L("batt"), pieces=["battp"]),
        step("h5", "cut", "Cut the binding and loop", "Cut the binding strip and the hanging loop strip.", L("bind"), pieces=["binding", "loop"]),
        step("h6", "sew", "Stack and quilt", "Stack: back (right side down), both batting layers, front (right side up). Pin through all layers and quilt a 4 cm grid, starting from the centre and working outwards.", T("quilt", top="main", back="back", pattern="grid"),
             beginner="Quilting means stitching through all the layers so they act as one. A walking foot stops the top layer from creeping; otherwise sew slowly with plenty of pins.", meas=[M("Grid spacing", 4), M("Stitch length", 3, "mm")], pieces=["front", "backp", "battp"], tech=["quilting"]),
        step("h7", "sew", "Square up", "Trim all layers to an exact 20 × 20 cm square.", T("mark", tone="main", w=20, h=20, label="trim to 20 × 20"), meas=[M("Trimmed size", 20)], pieces=["front"]),
        step("h8", "sew", "Prepare binding and loop", "Press the binding strip in half lengthwise, wrong sides together. Press the loop strip into a four-fold strap and edgestitch it.", T("fold", tone="bind", label="binding pressed in half", dim=3), pieces=["binding", "loop"], tech=["binding", "pressing"]),
        step("h9", "assemble", "Sew on the binding", "Fold the loop in half and baste its ends to one corner on the back. Sew the binding's raw edges to the front edge with a 1 cm seam, mitring each corner and overlapping the ends 3 cm.", T("binding", tone="main", bind="bind", width=1), meas=[M("Binding seam", 1)], pieces=["binding", "loop"], tech=["binding"]),
        step("h10", "finish", "Finish the binding", "Wrap the binding to the back so its fold just covers the stitching. Slip-stitch by hand, or stitch in the ditch from the front.", T("hand", tone="bind", stitch="whip"), pieces=["binding"], tech=["binding", "ladder-stitch"]),
        step("h11", "finish", "Done", "Press lightly.", G()),
    ],
    gallery=[{"label": "Pot holder", "scene": scene(
        {"k": "panel", "x": 100, "y": 60, "w": 200, "h": 200, "tone": "bind", "rx": 6}, {"k": "panel", "x": 110, "y": 70, "w": 180, "h": 180, "tone": "main"},
        *[{"k": "stitch", "pts": [[110 + i * 36, 70], [110 + i * 36, 250]]} for i in range(1, 5)], *[{"k": "stitch", "pts": [[110, 70 + i * 36], [290, 70 + i * 36]]} for i in range(1, 5)],
        {"k": "cord", "pts": [[104, 64], [80, 40], [100, 30], [112, 58]], "color": "bind"})}],
    related=["apron", "baby-quilt"],
))

# ---------------------------------------------------------------- 8 fabric basket
P.append(project(
    id="fabric-basket", title="Fabric Storage Basket", category="home", difficulty="intermediate",
    summary="A structured, lined basket with handle tabs — sized for any shelf.",
    description="Boxed corners plus stiff interfacing make a basket that stands up on its own. Make a set in different sizes for shelves, bathrooms or a craft room.",
    tags=["home", "gifts", "storage", "boxed corners", "lined"],
    minutes=[120, 180], costUSD=[10, 25], machineRequired=True, popularity=76, featured=True,
    constants={"sa": 1},
    params=[{"id": "W", "label": "Finished width", "default": 22, "min": 14, "max": 32, "step": 1}, {"id": "H", "label": "Finished height", "default": 18, "min": 12, "max": 26, "step": 1}, {"id": "D", "label": "Finished depth", "default": 16, "min": 8, "max": 22, "step": 1}],
    sizes=[{"id": "s", "label": "Small", "values": {"W": 16, "H": 14, "D": 12}}, {"id": "m", "label": "Medium", "values": {"W": 22, "H": 18, "D": 16}}, {"id": "l", "label": "Large", "values": {"W": 30, "H": 24, "D": 20}}],
    customNote="Side pieces are width + depth + 2 seam allowances across and height + half the depth + 2 seam allowances tall; corner squares are always half the depth. Interfacing is cut without seam allowances. Handle tabs stay the same size.",
    finished={"label": "Finished basket", "dims": [{"label": "Width", "value": "W"}, {"label": "Height", "value": "H"}, {"label": "Depth", "value": "D"}]},
    tools=["machine", "needle-90", "scissors", "ruler", "marker", "clips", "iron", "pressing-cloth", "point-turner?"],
    materials=[
        fabric("main", "Outer fabric", "#7F9473", "Outside and handle tabs.", ["Cotton canvas", "Linen", "Quilting cotton"], 112, "folded", [112, 140]),
        fabric("lining", "Lining fabric", "#E3C48D", "Inside.", ["Quilting cotton"], 112, "folded", [112, 140]),
        fabric("intf", "Heavy fusible interfacing or fusible foam", "#ECE7DD", "Makes the basket stand up.", ["Fusible foam stabiliser", "Heavyweight fusible interfacing", "Fusible fleece (softer)"], 90, "single", [50, 90], kind="interfacing"),
        "thread"],
    pieces=[piece("outer", "Outer side", "main", 2, "W + D + 2*sa", "H + D/2 + 2*sa", "#7F9473", markings=["Cut {D/2} squares from both bottom corners"]),
            piece("tab", "Handle tab", "main", 2, 10, 12, "#5F7354", sa=0, grain="any"),
            piece("liningp", "Lining side", "lining", 2, "W + D + 2*sa", "H + D/2 + 2*sa", "#E3C48D", markings=["Cut {D/2} squares from both bottom corners"]),
            piece("intfp", "Interfacing", "intf", 2, "W + D", "H + D/2", "#CFC8BA", sa=0, notes="Cut {D/2 - 1} squares from the bottom corners after fusing.")],
    steps=[
        step("fb1", "prep", "Press", "Press the outer and lining fabrics.", T("press", tones=["main", "lining"]), tech=["pressing"]),
        step("fb2", "cut", "Cut the outer pieces and tabs", "Cut two outer sides and two handle tabs.", L("main"), pieces=["outer", "tab"]),
        step("fb3", "cut", "Cut the lining", "Cut two lining sides.", L("lining"), pieces=["liningp"]),
        step("fb4", "cut", "Cut the interfacing", "Cut two interfacing pieces — smaller than the outer pieces so the seams aren't bulky.", L("intf"), pieces=["intfp"]),
        step("fb5", "sew", "Fuse the interfacing", "Centre the interfacing on the wrong side of each outer piece, 1 cm in from every edge, and fuse with a pressing cloth, 10–15 seconds per spot.", T("press", tones=["main", "intf"], label="fuse interfacing to the outer pieces"), meas=[M("Inset from edges", "sa")], pieces=["intfp", "outer"], tech=["interfacing"], timer=1, warn=["Hot iron and steam — use a pressing cloth."]),
        step("fb6", "sew", "Cut the corner squares", "Cut squares from both bottom corners of all four outer and lining pieces.", T("notch", tone="main", value="D/2"), meas=[M("Corner square", "D/2")], pieces=["outer", "liningp"], tech=["boxed-corners"]),
        step("fb7", "sew", "Make the handle tabs", "Press each tab into a four-fold strip and edgestitch both long edges. Fold in half into a loop.", T("strap", tone="tab", width=2.5), pieces=["tab"], tech=["edgestitching"]),
        step("fb8", "sew", "Sew the outer", "Place the outer pieces right sides together. Sew the sides and bottom with a 1 cm seam, leaving the corner squares open. Press seams open.", T("sew", tone="main", sides="lbr", notch=True), meas=[M("Seam allowance", "sa")], pieces=["outer"], tech=["seam-allowance"]),
        step("fb9", "sew", "Box the outer corners", "Match each side seam to the bottom seam, flatten and sew straight across with a 1 cm seam.", T("box", tone="main", depth="D"), meas=[M("Boxing seam = depth", "D")], pieces=["outer"], tech=["boxed-corners"]),
        step("fb10", "sew", "Sew and box the lining", "Repeat with the lining, leaving a 10 cm gap in the bottom seam.", T("sew", tone="lining", sides="lbr", gap="b", gapLabel="10 cm gap", notch=True), meas=[M("Gap", 10)], pieces=["liningp"], tech=["boxed-corners", "lining"]),
        step("fb11", "assemble", "Baste the tabs and join at the top", "Baste a tab loop to the centre of each outer side seam at the top, loop pointing down. Put the outer (right side out) inside the lining (wrong side out), match side seams and sew round the top with a 1 cm seam.", T("loops", base="main", strap="tab"), pieces=["tab", "outer", "liningp"], tech=["lining", "attaching-straps"]),
        step("fb12", "assemble", "Turn and close", "Turn through the lining gap, close the gap by edgestitching, and push the lining inside.", T("turn", tone="lining"), pieces=["liningp"], tech=["ladder-stitch"]),
        step("fb13", "finish", "Topstitch the rim", "Press the top edge and topstitch 5 mm from it.", T("topstitch", tone="main", dist=0.5, all=False), meas=[M("Topstitch", 0.5)], pieces=["outer"], tech=["topstitching"]),
        step("fb14", "finish", "Shape", "Push out the corners and shape the basket. Optionally fold the top down to show the lining.", G()),
    ],
    gallery=[{"label": "Basket", "scene": scene(
        {"k": "poly", "pts": [[90, 110], [290, 110], [320, 90], [320, 230], [290, 260], [90, 260]], "tone": "main"},
        {"k": "poly", "pts": [[90, 110], [120, 80], [320, 80], [290, 110]], "tone": "lining"}, {"k": "stitch", "pts": [[90, 120], [290, 120]]},
        {"k": "cord", "pts": [[95, 112], [72, 125], [92, 140]], "color": "tab"})}],
    related=["classic-tote", "zip-pouch"],
))

# ---------------------------------------------------------------- 9 crayon roll
P.append(project(
    id="crayon-roll", title="Crayon Roll", category="kids", difficulty="beginner",
    summary="A roll-up case with eight crayon slots and a ribbon tie.",
    description="Pocket channels, a turned-and-topstitched finish and a ribbon tie — quick to make and a favourite party gift. Sized for standard wax crayons.",
    tags=["kids", "gifts", "beginner", "quick", "scraps"],
    minutes=[45, 70], costUSD=[3, 8], machineRequired=True, popularity=74,
    constants={"sa": 1},
    finished={"label": "Finished roll (open)", "dims": [{"label": "Width", "value": 32}, {"label": "Height", "value": 20}, {"label": "Slot width", "value": 4}]},
    tools=["machine", "scissors", "ruler", "marker", "pins", "iron", "point-turner?"],
    materials=[fabric("main", "Outer fabric", "#5E7C8A", "Outside of the roll.", ["Quilting cotton", "Canvas"], 112, "single", [50, 112]),
               fabric("lining", "Lining & pocket fabric", "#E3C48D", "Inside and the crayon pocket.", ["Quilting cotton"], 112, "single", [50, 112]),
               notion("ribbon", "Ribbon, 1 cm wide", "60 cm", "Tie.", "#C0583A", ["Twill tape", "Elastic loop + button"]), "thread"],
    pieces=[piece("outerp", "Outer", "main", 1, 34, 22, "#5E7C8A"), piece("liningp", "Lining", "lining", 1, 34, 22, "#E3C48D"), piece("pocketp", "Pocket", "lining", 1, 34, 20, "#C9A06A", notes="Folded in half lengthwise to 10 cm.")],
    steps=[
        step("cr1", "prep", "Press", "Press your fabrics.", T("press", tones=["main", "lining"]), tech=["pressing"]),
        step("cr2", "cut", "Cut the outer", "Cut the outer rectangle.", L("main"), pieces=["outerp"]),
        step("cr3", "cut", "Cut the lining and pocket", "Cut the lining and the pocket from the lining fabric.", L("lining"), pieces=["liningp", "pocketp"]),
        step("cr4", "sew", "Fold the pocket", "Fold the pocket in half lengthwise, wrong sides together, and press. The fold is the pocket's top edge.", T("fold", tone="pocketp", label="fold in half, wrong sides together", dim=10), pieces=["pocketp"], tech=["pressing"]),
        step("cr5", "sew", "Sew the crayon channels", "Lay the pocket on the lining's right side with raw edges level at the bottom. Mark vertical lines 4 cm apart starting from 1 cm in, and stitch along each line through pocket and lining, backstitching at the top.", T("channels", tone="lining", pocket="pocketp", count=8, spacing=4),
             meas=[M("Channel spacing", 4), M("First line from side edge", 5)], pieces=["pocketp", "liningp"], tech=["backstitching"]),
        step("cr6", "assemble", "Baste the ribbon", "Fold the ribbon in half and baste the fold to the middle of the outer's right-hand short edge, ribbon lying across the fabric.", T("loops", base="main", strap="#C0583A"), pieces=["outerp"], tech=["attaching-straps"]),
        step("cr7", "assemble", "Sew outer to lining", "Place outer and lining right sides together. Sew all round with a 1 cm seam, keeping the ribbon tails inside, and leave a 7 cm gap along the top.", T("sew", tone="main", sides="ltrb", gap="t", gapLabel="7 cm gap"), meas=[M("Seam allowance", "sa")], pieces=["outerp", "liningp"]),
        step("cr8", "assemble", "Clip and turn", "Clip the corners, turn right side out, push out the corners and press.", T("turn", tone="main"), tech=["clipping-corners"]),
        step("cr9", "finish", "Topstitch", "Topstitch 3 mm from the edge all round, closing the gap.", T("topstitch", tone="main", dist=0.3), meas=[M("Topstitch", 0.3)], pieces=["outerp"], tech=["topstitching"]),
        step("cr10", "finish", "Fill with crayons", "Slide a crayon into each slot, roll up and tie.", G()),
    ],
    gallery=[{"label": "Open roll", "scene": scene(
        {"k": "panel", "x": 50, "y": 70, "w": 300, "h": 170, "tone": "lining"},
        *[{"k": "panel", "x": 62 + i * 36, "y": 90, "w": 14, "h": 90, "tone": c, "rx": 3} for i, c in enumerate(["#C0583A", "#D9A35F", "#7F9473", "#5E7C8A", "#B5727D", "#3A3530", "#E3C48D", "#8E4A36"])],
        {"k": "panel", "x": 50, "y": 150, "w": 300, "h": 90, "tone": "pocketp"}, *[{"k": "stitch", "pts": [[50 + i * 37.5, 150], [50 + i * 37.5, 240]]} for i in range(1, 8)],
        {"k": "cord", "pts": [[350, 150], [380, 140], [390, 170]], "color": "#C0583A"})}],
    related=["bean-bags", "burp-cloth"],
))

# ---------------------------------------------------------------- 10 burp cloth
P.append(project(
    id="burp-cloth", title="Baby Burp Cloth", category="kids", difficulty="beginner",
    summary="A soft, absorbent two-layer burp cloth — a classic baby-shower gift.",
    description="A printed cotton front and a thirsty terry or flannel back, turned and topstitched. Takes under an hour and uses fat quarters.",
    tags=["kids", "gifts", "beginner", "quick", "baby"],
    minutes=[30, 50], costUSD=[4, 10], machineRequired=True, popularity=69,
    constants={"sa": 1},
    finished={"label": "Finished cloth", "dims": [{"label": "Width", "value": 23}, {"label": "Length", "value": 48}]},
    tools=["machine", "scissors", "ruler", "pins", "iron", "point-turner?"],
    materials=[fabric("main", "Front — cotton print", "#B5727D", "Pretty side.", ["Quilting cotton", "Cotton flannel"], 112, "single", [50, 112]),
               fabric("back", "Back — terry or flannel", "#F0E6D8", "Absorbent side.", ["Cotton terry", "Bamboo terry", "Flannel", "Minky (less absorbent)"], 112, "single", [50, 112], alts=["An old cotton bath towel"]), "thread"],
    pieces=[piece("front", "Front", "main", 1, 25, 50, "#B5727D"), piece("backp", "Back", "back", 1, 25, 50, "#E6D8C4")],
    steps=[
        step("bc1", "prep", "Pre-wash both fabrics", "Pre-wash and dry both fabrics hot — flannel and terry can shrink a lot, and baby items get washed often.", T("press", tones=["main", "back"]), tech=["prewash"]),
        step("bc2", "cut", "Cut the front", "Cut the front rectangle.", L("main"), pieces=["front"]),
        step("bc3", "cut", "Cut the back", "Cut the back rectangle.", L("back"), pieces=["backp"]),
        step("bc4", "assemble", "Layer", "Place front and back right sides together and pin all round. Terry is slippery — use plenty of pins.", T("layer", base="main", top="back"), pieces=["front", "backp"]),
        step("bc5", "sew", "Sew all round", "Sew all round with a 1 cm seam, leaving an 8 cm gap on one long side.", T("sew", tone="back", sides="ltrb", gap="r", gapLabel="8 cm gap"), meas=[M("Seam allowance", "sa")], pieces=["front", "backp"], tech=["seam-allowance"]),
        step("bc6", "sew", "Clip and turn", "Clip the corners, turn right side out, push out the corners and press (gently on terry).", T("turn", tone="back"), tech=["clipping-corners"]),
        step("bc7", "finish", "Topstitch", "Topstitch 5 mm from the edge all round, closing the gap. Optionally add two lines down the middle to keep the layers together in the wash.", T("topstitch", tone="main", dist=0.5), meas=[M("Topstitch", 0.5)], pieces=["front"], tech=["topstitching"]),
        step("bc8", "finish", "Done", "Wash once before gifting so it's soft and absorbent.", G()),
    ],
    gallery=[{"label": "Burp cloth", "scene": scene({"k": "panel", "x": 130, "y": 30, "w": 140, "h": 240, "tone": "main", "rx": 6}, {"k": "stitch", "pts": [[140, 40], [260, 40], [260, 260], [140, 260]], "closed": True})}],
    related=["baby-quilt", "crayon-roll"],
))

# ---------------------------------------------------------------- 11 bean bags
P.append(project(
    id="bean-bags", title="Juggling Bean Bags (set of 4)", category="kids", difficulty="beginner",
    summary="Four little filled squares for juggling and throwing games — sew by hand or machine.",
    description="The best first project for kids learning to sew with an adult: tiny seams, instant results. Use felt or cotton scraps and fill with rice or plastic pellets.",
    tags=["kids", "gifts", "beginner", "hand-sewing", "scraps", "toys"],
    minutes=[45, 75], costUSD=[2, 6], machineRequired=False, popularity=62,
    constants={"sa": 1},
    finished={"label": "Each bean bag", "dims": [{"label": "Size (square)", "value": 10}]},
    tools=["hand-needle", "machine?", "scissors", "pins", "funnel?", "point-turner?"],
    materials=[fabric("main", "Sturdy cotton or felt scraps", "#D9A35F", "Bag fabric — tightly woven so filling can't escape.", ["Quilting cotton", "Wool felt", "Canvas"], 50, "single", [50, 112]),
               notion("filling", "Filling", "About 120 g per bag (480 g total)", "Weight.", "#E9DFC9", ["Plastic poly pellets (washable)", "Rice or dried lentils (not washable)"]), "thread"],
    pieces=[piece("square", "Bean bag square", "main", 8, 12, 12, "#D9A35F", grain="any")],
    steps=[
        step("bb1", "prep", "Choose and press fabrics", "Pick four pairs of fabrics — mismatched pairs look fun. Press them.", T("press", tones=["main"]), tech=["pressing"]),
        step("bb2", "cut", "Cut eight squares", "Cut eight 12 cm squares (two per bean bag).", L("main"), pieces=["square"], warn=["Children should only use scissors with adult supervision."]),
        step("bb3", "sew", "Sew around three and a half sides", "Place two squares right sides together. Sew all round with a 1 cm seam, leaving a 4 cm gap on one side. By hand, use a small backstitch so the filling can't escape.", T("sew", tone="main", sides="ltrb", gap="b", gapLabel="4 cm gap"),
             beginner="Backstitch by hand: bring the needle up, take a stitch backwards, then come up a stitch-length ahead. Keep stitches about 3 mm long.", meas=[M("Seam allowance", "sa"), M("Gap", 4)], pieces=["square"], tech=["backstitching", "seam-allowance"]),
        step("bb4", "sew", "Clip and turn", "Clip the corners, turn right side out and poke the corners out gently.", T("turn", tone="main"), tech=["clipping-corners"]),
        step("bb5", "assemble", "Fill", "Use a funnel to fill each bag about ¾ full — around 120 g. Leave room so it stays floppy for juggling.", T("fill", tone="main", label="about 120 g"), meas=[M("Filling per bag", 120, "deg")] if False else None,
             warn=["Small parts and fillings are a choking hazard — not for children under 3."]),
        step("bb6", "finish", "Close the gap", "Fold the gap's edges in and ladder-stitch it closed with small, firm stitches.", T("close", tone="main", method="hand"), pieces=["square"], tech=["ladder-stitch"]),
        step("bb7", "finish", "Play!", "Make all four and try a three-ball cascade.", G()),
    ],
    gallery=[{"label": "Set", "scene": scene(
        {"k": "panel", "x": 60, "y": 120, "w": 110, "h": 110, "tone": "main", "rx": 18}, {"k": "panel", "x": 150, "y": 70, "w": 110, "h": 110, "tone": "#7F9473", "rx": 18},
        {"k": "panel", "x": 240, "y": 130, "w": 110, "h": 110, "tone": "#C0583A", "rx": 18}, {"k": "panel", "x": 160, "y": 170, "w": 100, "h": 100, "tone": "#5E7C8A", "rx": 18})}],
    related=["crayon-roll", "scrunchie"],
))

# ---------------------------------------------------------------- 12 denim coasters
P.append(project(
    id="denim-coasters", title="Upcycled Denim Coasters", category="upcycling", difficulty="beginner",
    summary="Turn one leg of old jeans into a set of four sturdy coasters.",
    description="Old denim is thick, absorbent and already worn soft. One jeans leg, cut open, gives plenty of fabric for four coasters backed with a cheerful cotton.",
    tags=["upcycling", "home", "gifts", "beginner", "quick", "denim"],
    minutes=[40, 60], costUSD=[0, 3], machineRequired=True, popularity=71, featured=True,
    constants={"sa": 1},
    finished={"label": "Each coaster", "dims": [{"label": "Size (square)", "value": 10}]},
    tools=["machine", "needle-90", "scissors", "ruler", "marker", "pins", "iron", "point-turner?"],
    materials=[fabric("main", "Old jeans — one leg, opened flat", "#4F6A8C", "Coaster tops.", ["Denim"], 40, "single", [36, 40, 45], alts=["Denim scraps"], weight="Heavy"),
               fabric("back", "Cotton scraps", "#E3C48D", "Coaster backs.", ["Quilting cotton", "Canvas"], 50, "single", [50, 112]), "thread"],
    pieces=[piece("top", "Coaster top", "main", 4, 12, 12, "#4F6A8C", grain="any"), piece("bottom", "Coaster back", "back", 4, 12, 12, "#E3C48D", grain="any")],
    steps=[
        step("dc1", "cut", "Open up the jeans leg", "Cut one leg off the jeans just below the pocket. Cut along the inseam (not the thick outer seam) and open it flat. Press it.", T("mark", tone="main", label="cut along the inseam, open flat"), pieces=["top"], warn=["Denim is tough — use sharp scissors and cut slowly."]),
        step("dc2", "cut", "Cut the coaster tops", "Cut four 12 cm squares from the denim, avoiding worn holes and the thick seams.", L("main"), pieces=["top"]),
        step("dc3", "cut", "Cut the backs", "Cut four 12 cm squares from the cotton.", L("back"), pieces=["bottom"]),
        step("dc4", "sew", "Set up for denim", "Fit a 90/14 or denim needle and set a 3 mm stitch.", T("setup", tone="main", stitch=3, note="Denim needle 90/14"), meas=[M("Stitch length", 3, "mm")]),
        step("dc5", "assemble", "Sew top to back", "Place a denim and a cotton square right sides together. Sew all round with a 1 cm seam, leaving a 5 cm gap.", T("sew", tone="main", sides="ltrb", gap="b", gapLabel="5 cm gap"), meas=[M("Seam allowance", "sa")], pieces=["top", "bottom"]),
        step("dc6", "assemble", "Clip, turn and press", "Clip the corners close to the stitching, turn, push the corners out and press with steam.", T("turn", tone="main"), tech=["clipping-corners", "pressing"]),
        step("dc7", "finish", "Double topstitch", "Topstitch 3 mm and then 1 cm from the edge, closing the gap. Contrast thread looks great on denim.", T("topstitch", tone="main", dist=0.3), meas=[M("First line", 0.3), M("Second line", 1)], pieces=["top"], tech=["topstitching"]),
        step("dc8", "finish", "Stack and gift", "Make all four and tie the stack with twine.", G()),
    ],
    gallery=[{"label": "Coasters", "scene": scene(
        *[{"k": "panel", "x": 80 + i * 22, "y": 60 + i * 18, "w": 160, "h": 160, "tone": "main"} for i in range(4)],
        {"k": "stitch", "pts": [[152, 128], [298, 128], [298, 274], [152, 274]], "closed": True})}],
    related=["zip-pouch", "classic-tote"],
))

# ---------------------------------------------------------------- 13 infinity scarf
P.append(project(
    id="infinity-scarf", title="Infinity Scarf", category="clothing", difficulty="beginner",
    summary="A long, soft loop scarf from a single length of jersey or rayon.",
    description="One long seam and one joining seam. Jersey doesn't fray, so there are no edges to finish — the perfect first knit project.",
    tags=["clothing", "accessories", "gifts", "beginner", "knits", "quick"],
    minutes=[40, 60], costUSD=[8, 20], machineRequired=True, popularity=66,
    constants={"sa": 1},
    finished={"label": "Finished scarf", "dims": [{"label": "Loop length", "value": 148}, {"label": "Width (flat)", "value": 34}]},
    tools=["machine", "needle-ball", "scissors", "pins", "safety-pin?", "hand-needle"],
    materials=[fabric("main", "Jersey or rayon challis", "#8C6E9C", "The scarf.", ["Cotton jersey", "Viscose jersey", "Rayon challis", "Double gauze"], 140, "single", [140, 150], weight="Light, drapey", minw=140), "thread"],
    pieces=[piece("scarf", "Scarf", "main", 1, 70, 150, "#8C6E9C", notes="Width runs across the fabric; length along the grain.")],
    steps=[
        step("is1", "prep", "Set up for knits", "Fit a ballpoint (stretch) needle and choose a narrow zigzag (width 1, length 2.5) or your machine's stretch stitch, so the seam can stretch with the fabric.", T("setup", tone="main", stitch=2.5, note="Ballpoint needle · narrow zigzag"), meas=[M("Stitch length", 2.5, "mm")], tech=["zigzag-stitch"]),
        step("is2", "cut", "Cut the scarf", "Lay the fabric single-layer and cut one long rectangle — 70 cm across the width and 150 cm along the length.", L("main"), pieces=["scarf"]),
        step("is3", "sew", "Sew the long seam", "Fold the scarf in half lengthwise, right sides together. Sew the long edge with a 1 cm seam. Don't turn it yet.", T("tube", tone="main", label="sew the long edge — leave it inside out"), meas=[M("Seam allowance", "sa")], pieces=["scarf"], tech=["seam-allowance"]),
        step("is4", "assemble", "Join the ends", "Reach inside the tube and pull one end through until the two open ends meet, right sides together and long seams matched. Sew round the ends, leaving an 8 cm gap.", T("sew", tone="main", sides="t", gap="t", gapLabel="8 cm gap", label="ends right sides together"), meas=[M("Gap", 8)], pieces=["scarf"]),
        step("is5", "assemble", "Turn", "Pull the scarf right side out through the gap.", T("turn", tone="main")),
        step("is6", "finish", "Close the gap", "Ladder-stitch the gap closed by hand.", T("close", tone="main", method="hand"), pieces=["scarf"], tech=["ladder-stitch"]),
        step("is7", "finish", "Wear it", "Loop it twice round your neck.", G()),
    ],
    gallery=[{"label": "Scarf", "scene": scene({"k": "poly", "pts": ell(200, 140, 110, 120), "tone": "main"}, {"k": "poly", "pts": ell(200, 120, 55, 70), "tone": "#FBF7F0"}, {"k": "fold", "from": [140, 220], "to": [260, 230]})}],
    related=["scrunchie", "kimono-jacket", "headband"],
))

# ---------------------------------------------------------------- 14 headband
P.append(project(
    id="headband", title="Elastic-Back Headband", category="accessories", difficulty="beginner",
    summary="A comfy wide headband with a hidden elastic section at the back.",
    description="Two tubes and a short piece of elastic. The elastic sits in its own casing at the back, so the headband grips without pinching.",
    tags=["accessories", "gifts", "beginner", "quick", "scraps"],
    minutes=[35, 50], costUSD=[2, 6], machineRequired=True, popularity=58,
    constants={"sa": 1},
    finished={"label": "Finished headband", "dims": [{"label": "Band width", "value": 5}, {"label": "Relaxed circumference", "value": 50}]},
    tools=["machine", "scissors", "pins", "iron", "safety-pin"],
    materials=[fabric("main", "Cotton fabric", "#7F9473", "Band and casing.", ["Quilting cotton", "Cotton lawn", "Jersey"], 112, "single", [50, 112]),
               notion("elastic", "2 cm wide elastic", "14 cm", "Stretchy back.", "#F1ECE4"), "thread"],
    pieces=[piece("band", "Front band", "main", 1, 12, 42, "#7F9473"), piece("casing", "Elastic casing", "main", 1, 6, 22, "#5F7354")],
    steps=[
        step("hb1", "prep", "Press", "Press your fabric.", T("press", tones=["main"]), tech=["pressing"]),
        step("hb2", "cut", "Cut both pieces", "Cut the front band and the elastic casing.", L("main"), pieces=["band", "casing"]),
        step("hb3", "sew", "Sew the band tube", "Fold the band in half lengthwise, right sides together. Sew the long edge with a 1 cm seam and turn right side out. Press with the seam centred on the back.", T("tube", tone="main"), meas=[M("Seam allowance", "sa")], pieces=["band"], tech=["seam-allowance"]),
        step("hb4", "sew", "Sew the casing tube", "Repeat with the casing strip.", T("tube", tone="casing"), pieces=["casing"]),
        step("hb5", "assemble", "Thread the elastic", "Thread the elastic through the casing and stitch across each end to hold it, 5 mm from the edges. The casing gathers up.", T("cord", tone="casing", label="elastic through the casing"), meas=[M("Elastic length", 14)], pieces=["casing"], tech=["elastic-waistband"]),
        step("hb6", "assemble", "Join the ends", "Fold the band's raw ends 1 cm to the inside. Insert one end of the casing 2 cm into each end of the band and topstitch across twice.", T("close", tone="main", method="machine"), meas=[M("Overlap", 2)], pieces=["band", "casing"]),
        step("hb7", "finish", "Done", "Try it on.", G()),
    ],
    gallery=[{"label": "Headband", "scene": scene({"k": "poly", "pts": ell(200, 160, 130, 110), "tone": "main"}, {"k": "poly", "pts": ell(200, 175, 112, 98), "tone": "#FBF7F0"}, {"k": "panel", "x": 160, "y": 262, "w": 80, "h": 16, "tone": "casing", "rx": 6})}],
    related=["scrunchie", "infinity-scarf"],
))

# ---------------------------------------------------------------- 15 kimono jacket
P.append(project(
    id="kimono-jacket", title="Rectangle Kimono Jacket", category="clothing", difficulty="intermediate",
    summary="A breezy open-front kimono made entirely from rectangles, drafted from your bust measurement.",
    description="No curved pattern pieces: a back cut on the fold, two fronts, two sleeves and a long front band. Fit comes from your bust measurement plus generous ease, and you choose the length.",
    tags=["clothing", "custom fit", "summer", "rectangles"],
    minutes=[180, 270], costUSD=[20, 45], machineRequired=True, popularity=80, featured=True,
    constants={"sa": 1.5, "ease": 24, "hemA": 3, "band": 5},
    params=[{"id": "bust", "label": "Bust / chest", "default": 92, "min": 78, "max": 130, "step": 1, "help": "Around the fullest part, tape level."},
            {"id": "L", "label": "Jacket length", "default": 70, "min": 55, "max": 100, "step": 1, "help": "From the top of the shoulder to the hem."},
            {"id": "sleeve", "label": "Sleeve length", "default": 32, "min": 20, "max": 50, "step": 1, "help": "From the shoulder point down the arm."}],
    sizes=[{"id": "s", "label": "S", "values": {"bust": 86, "L": 68, "sleeve": 30}}, {"id": "m", "label": "M", "values": {"bust": 92, "L": 70, "sleeve": 32}},
           {"id": "l", "label": "L", "values": {"bust": 102, "L": 72, "sleeve": 33}}, {"id": "xl", "label": "XL", "values": {"bust": 112, "L": 74, "sleeve": 34}}],
    customNote="Drafted, not scaled: the body circumference is bust + 24 cm ease; the back takes half of that and each front a quarter minus the band. Sleeves are a fixed 46 cm around (roomy kimono sleeve) with your length. Seam allowance stays 1.5 cm and hems 3 cm at every size.",
    finished={"label": "Finished jacket", "dims": [{"label": "Body circumference", "value": "bust + ease"}, {"label": "Length", "value": "L"}, {"label": "Sleeve length", "value": "sleeve"}]},
    tools=["machine", "tape", "scissors", "ruler", "marker", "pins", "iron", "seam-gauge?"],
    materials=[fabric("main", "Drapey woven fabric", "#C98A6B", "Whole jacket.", ["Rayon challis", "Viscose crepe", "Cotton voile", "Linen (light)"], 140, "folded", [140, 150], weight="Light, drapey", minw=140), "thread"],
    pieces=[
        piece("back", "Back", "main", 1, "(bust + ease)/2 + 2*sa", "L + sa + hemA", "#C98A6B", fold=True),
        piece("front", "Front", "main", 2, "(bust + ease)/4 - band/2 + 2*sa", "L + sa + hemA", "#B07457"),
        piece("sleevep", "Sleeve", "main", 2, "46 + 2*sa", "sleeve + sa + hemA", "#D9A487"),
        piece("bandp", "Front band", "main", 2, "2*band + 2", "L + 18", "#8E5A43", sa=1, notes="Joined at the centre back neck."),
    ],
    steps=[
        step("k1", "prep", "Take your measurements", "Measure your bust (fullest point), the length from the top of your shoulder to where you want the hem, and your sleeve length from the shoulder point. Enter them in Customise — every piece updates.", T("measure", lines="bust"),
             meas=[M("Bust", "bust"), M("Jacket length", "L"), M("Sleeve length", "sleeve")]),
        step("k2", "prep", "Pre-wash", "Pre-wash and dry the fabric — rayon can shrink 5–8%, which matters for the length. Press.", T("press", tones=["main"]), tech=["prewash"]),
        step("k3", "cut", "Cut all pieces", "Fold the fabric selvedge to selvedge. Cut the back on the fold, then the fronts, sleeves and band pieces (two layers each).", L("main"), pieces=["back", "front", "sleevep", "bandp"],
             beginner="Drapey fabric shifts. Lay it on a large table, smooth it gently, and use pattern weights (tins work) instead of lots of pins."),
        step("k4", "sew", "Sew the shoulders", "Place the fronts on the back, right sides together, aligning the top edges at the outer sides. Sew the shoulder seams with 1.5 cm. Neaten and press towards the back.", T("sew", tone="main", sides="t", label="fronts on back · shoulders", sa=1.5), meas=[M("Seam allowance", "sa")], pieces=["front", "back"], tech=["seam-allowance", "finishing-edges"]),
        step("k5", "sew", "Attach the sleeves", "Open the body flat. Fold each sleeve in half to find the centre of its top edge, match it to the shoulder seam right sides together, pin and sew with 1.5 cm. Neaten and press towards the sleeve.", T("layer", base="main", top="sleevep", label="sleeve centre on shoulder seam"), meas=[M("Seam allowance", "sa")], pieces=["sleevep"], tech=["finishing-edges"]),
        step("k6", "sew", "Sew the underarm and side seams", "Fold the jacket right sides together at the shoulders. Sew from the sleeve hem, across the underarm and down the side in one seam. Clip into the underarm corner, neaten and press.", T("sew", tone="main", sides="lb", label="sleeve hem → underarm → side hem", sa=1.5), meas=[M("Seam allowance", "sa")], pieces=["front", "back", "sleevep"], tech=["clipping-corners"]),
        step("k7", "sew", "Hem sleeves and body", "Press 1 cm, then 2 cm, at the sleeve hems and the body hem. Stitch close to the inner fold.", T("hem", tone="main", f1=1, f2=2), meas=[M("First fold", 1), M("Second fold", 2)], pieces=["front", "back", "sleevep"], tech=["hemming"]),
        step("k8", "assemble", "Make the band", "Sew the two band pieces together at one short end — this seam sits at the centre back neck. Press the band in half lengthwise, wrong sides together. Fold each bottom end right sides together and sew across 1 cm, then turn.", T("fold", tone="bandp", label="band pressed in half lengthwise", dim="band"), meas=[M("Finished band width", "band")], pieces=["bandp"], tech=["pressing"]),
        step("k9", "assemble", "Attach the band", "Pin the band's raw edges to the right side of the front opening and back neck, band seam at centre back, finished ends level with the hem. Sew with 1 cm, neaten, press towards the band and topstitch 5 mm from the seam.", T("binding", tone="main", bind="bandp", width="band"), meas=[M("Band seam", 1), M("Topstitch", 0.5)], pieces=["bandp", "front", "back"], tech=["topstitching"]),
        step("k10", "finish", "Final press", "Press the whole jacket, especially the band.", G()),
    ],
    gallery=[{"label": "Front", "scene": scene(
        {"k": "poly", "pts": [[140, 40], [260, 40], [360, 60], [370, 140], [290, 140], [290, 270], [110, 270], [110, 140], [30, 140], [40, 60]], "tone": "main"},
        {"k": "poly", "pts": [[185, 40], [215, 40], [210, 270], [190, 270]], "tone": "bandp"})}],
    related=["elastic-skirt", "infinity-scarf"],
))

# ---------------------------------------------------------------- 16 baby quilt
P.append(project(
    id="baby-quilt", title="Patchwork Baby Quilt", category="kids", difficulty="intermediate",
    summary="A 60 × 80 cm patchwork quilt of 48 squares, quilted and bound.",
    description="Your first quilt: simple squares, nested seams, a quilt sandwich and a machine-sewn binding. Two alternating prints make a classic checkerboard.",
    tags=["kids", "gifts", "baby", "quilting", "patchwork", "binding"],
    minutes=[480, 720], costUSD=[30, 60], machineRequired=True, popularity=85, featured=True,
    constants={"sa": 0.75},
    finished={"label": "Finished quilt", "dims": [{"label": "Width", "value": 60}, {"label": "Length", "value": 80}, {"label": "Square (finished)", "value": 10}]},
    tools=["machine", "walking-foot?", "rotary", "iron", "pins", "clips", "hand-needle?", "safety-pin"],
    materials=[
        fabric("printA", "Print A", "#E3C48D", "24 squares.", ["Quilting cotton"], 112, "single", [112]),
        fabric("printB", "Print B", "#7F9473", "24 squares.", ["Quilting cotton"], 112, "single", [112]),
        fabric("backing", "Backing", "#F0E6D8", "Back of the quilt.", ["Quilting cotton", "Cotton flannel"], 112, "single", [112, 140]),
        fabric("batt", "Cotton batting", "#F5F1EA", "Warmth.", ["100% cotton batting", "Bamboo-cotton batting"], 112, "single", [112, 228], kind="interfacing"),
        fabric("bind", "Binding fabric", "#C0583A", "Edge binding.", ["Quilting cotton"], 112, "single", [112]),
        "thread"],
    pieces=[
        piece("sqA", "Square A", "printA", 24, 11.5, 11.5, "#E3C48D", grain="any"), piece("sqB", "Square B", "printB", 24, 11.5, 11.5, "#7F9473", grain="any"),
        piece("backp", "Backing", "backing", 1, 70, 90, "#E6D8C4", sa=5, notes="5 cm larger than the top all round; trimmed after quilting."),
        piece("battp", "Batting", "batt", 1, 70, 90, "#E4E0D8", sa=5),
        piece("bindp", "Binding strip", "bind", 3, 110, 6.5, "#C0583A", sa=0.75, grain="any", notes="Cut across the width; join end to end."),
    ],
    steps=[
        step("q1", "prep", "Pre-wash and press", "Pre-wash all fabrics (baby quilts are washed often), then starch-press the prints so the squares cut accurately.", T("press", tones=["printA", "printB"]), tech=["prewash"]),
        step("q2", "cut", "Cut squares A", "Cut 24 squares of print A with a rotary cutter and ruler.", L("printA"), pieces=["sqA"], warn=["Rotary blades are extremely sharp — close the guard every time you put it down."]),
        step("q3", "cut", "Cut squares B", "Cut 24 squares of print B.", L("printB"), pieces=["sqB"]),
        step("q4", "cut", "Cut backing and batting", "Cut the backing and batting 5 cm larger than the quilt top on every side.", L("backing"), pieces=["backp"]),
        step("q5", "cut", "Cut the batting", "Cut the batting the same size as the backing.", L("batt"), pieces=["battp"]),
        step("q6", "cut", "Cut binding strips", "Cut three binding strips across the width of the fabric.", L("bind"), pieces=["bindp"]),
        step("q7", "sew", "Arrange the squares", "Lay out 8 rows of 6 squares in a checkerboard, alternating A and B. Photograph the layout so you can find your place.", T("patchwork", tones=["printA", "printB"], cols=6, rows=8, sewn=False), pieces=["sqA", "sqB"]),
        step("q8", "sew", "Sew the rows", "Sew the squares of each row together with a 0.75 cm seam. Press seams of odd rows to the left and even rows to the right.", T("patchwork", tones=["printA", "printB"], cols=6, rows=8, sewn=False),
             beginner="Alternating the pressing direction lets the seams 'nest' — they lock together when you join the rows, so the corners match.", meas=[M("Seam allowance", "sa")], pieces=["sqA", "sqB"], tech=["seam-allowance", "pressing"]),
        step("q9", "sew", "Join the rows", "Sew the rows together, nesting the seams and pinning at every intersection. Press the long seams in one direction.", T("patchwork", tones=["printA", "printB"], cols=6, rows=8, sewn=True), meas=[M("Seam allowance", "sa")], pieces=["sqA", "sqB"]),
        step("q10", "assemble", "Make the quilt sandwich", "Tape the backing to the floor wrong side up, smooth the batting on top, then the quilt top right side up. Pin every 10 cm with safety pins.", T("quilt", top="printA", back="backing", pattern="lines"), pieces=["backp", "battp"], tech=["quilting"]),
        step("q11", "assemble", "Quilt", "Quilt straight lines 5 mm either side of every seam ('stitch in the ditch' or just beside it), working from the centre out with a walking foot.", T("quilt", top="printB", back="backing", pattern="grid"), meas=[M("Stitch length", 3, "mm")], tech=["quilting"]),
        step("q12", "assemble", "Trim", "Trim the backing and batting level with the quilt top and square the corners.", T("mark", tone="printA", w=60, h=80, label="trim to the quilt top"), meas=[M("Trimmed size", 60), M("Length", 80)]),
        step("q13", "finish", "Prepare the binding", "Join the binding strips end to end with diagonal seams, trim, press open, then press the whole strip in half lengthwise.", T("fold", tone="bind", label="binding pressed in half", dim=3.25), pieces=["bindp"], tech=["binding"]),
        step("q14", "finish", "Attach and finish the binding", "Sew the binding to the front with a 0.75 cm seam, mitring the corners. Wrap it to the back and hand-stitch, or stitch in the ditch from the front.", T("binding", tone="printB", bind="bind", width=1), meas=[M("Binding seam", "sa")], pieces=["bindp"], tech=["binding", "ladder-stitch"]),
        step("q15", "finish", "Wash", "Wash and dry the quilt for that soft, crinkly look.", G()),
    ],
    gallery=[{"label": "Quilt", "scene": scene(
        {"k": "panel", "x": 84, "y": 14, "w": 232, "h": 272, "tone": "bind"},
        *[{"k": "panel", "x": 90 + c * 36.7, "y": 20 + r * 32.5, "w": 36.7, "h": 32.5, "tone": "printA" if (r + c) % 2 == 0 else "printB", "rx": 0} for r in range(8) for c in range(6)])}],
    related=["burp-cloth", "potholder"],
))

# ---------------------------------------------------------------- 17 duffel (advanced)
P.append(project(
    id="weekender-duffel", title="Weekender Duffel Bag", category="bags", difficulty="advanced",
    summary="A structured, lined weekend bag with a top zipper, end panels and webbing handles.",
    description="An advanced bag that combines everything: fusible fleece for structure, a zipper panel, webbing handles running under the bag, and end panels sewn in with pivoted corners. Allow a full weekend.",
    tags=["bags", "travel", "zipper", "lined", "advanced"],
    minutes=[600, 900], costUSD=[40, 80], machineRequired=True, popularity=73,
    constants={"sa": 1},
    params=[{"id": "Lb", "label": "Length", "default": 50, "min": 40, "max": 60, "step": 1}, {"id": "H", "label": "Height", "default": 28, "min": 24, "max": 34, "step": 1}, {"id": "D", "label": "Depth", "default": 22, "min": 18, "max": 26, "step": 1}],
    sizes=[{"id": "cabin", "label": "Cabin", "values": {"Lb": 45, "H": 26, "D": 20}}, {"id": "weekend", "label": "Weekend", "values": {"Lb": 50, "H": 28, "D": 22}}, {"id": "large", "label": "Large", "values": {"Lb": 58, "H": 32, "D": 25}}],
    customNote="The body wraps front, bottom and back (2 × height + depth). Two zipper panels make up the top depth. End panels are depth × height. All pieces carry 1 cm seam allowances; the zipper must be at least the bag length + 10 cm. Webbing length is recalculated.",
    finished={"label": "Finished bag", "dims": [{"label": "Length", "value": "Lb"}, {"label": "Height", "value": "H"}, {"label": "Depth", "value": "D"}]},
    tools=["machine", "needle-90", "zip-foot", "walking-foot?", "rotary", "ruler", "marker", "clips", "iron", "pressing-cloth", "hand-needle", "seam-ripper"],
    materials=[
        fabric("main", "Outer — heavy canvas", "#5E6B57", "Outside.", ["Waxed canvas", "Duck canvas", "Cordura"], 140, "single", [112, 140, 150], weight="Heavy, 340+ g/m²"),
        fabric("lining", "Lining — cotton twill", "#E3C48D", "Inside.", ["Cotton twill", "Quilting cotton"], 140, "single", [112, 140]),
        fabric("fleece", "Fusible fleece", "#ECE7DD", "Structure and padding.", ["Fusible fleece", "Fusible foam (stiffer)"], 112, "single", [90, 112], kind="interfacing"),
        notion("zipper", "Heavy zipper, #5 or #8", "1 zipper, at least {Lb + 10} long", "Top opening.", "#2E3A40", ["Two-way zipper"]),
        notion("webbing", "Cotton webbing, 3 cm", "2 pieces, each {2*H + D + 70} long", "Handles that run under the bag.", "#3A3530", ["Leather straps"]),
        "thread"],
    pieces=[
        piece("body", "Body (front–bottom–back)", "main", 1, "Lb + 2*sa", "2*H + D + 2*sa", "#5E6B57"),
        piece("ends", "End panel", "main", 2, "D + 2*sa", "H + 2*sa", "#4B5746"),
        piece("zippanel", "Zipper panel", "main", 2, "Lb + 2*sa", "D/2 + 1.5", "#6E7C66"),
        piece("lbody", "Lining body", "lining", 1, "Lb + 2*sa", "2*H + D + 2*sa", "#E3C48D"),
        piece("lends", "Lining end", "lining", 2, "D + 2*sa", "H + 2*sa", "#C9A06A"),
        piece("fbody", "Fleece body", "fleece", 1, "Lb", "2*H + D", "#CFC8BA", sa=0),
        piece("fends", "Fleece end", "fleece", 2, "D", "H", "#CFC8BA", sa=0),
    ],
    steps=[
        step("w1", "prep", "Press and plan", "Press the lining. Waxed canvas must not be ironed — finger-press it instead. Read all steps before cutting; this is a long project.", T("press", tones=["main", "lining"]), warn=["Never iron waxed canvas directly; the wax melts."]),
        step("w2", "cut", "Cut the outer", "Cut the body, two end panels and two zipper panels.", L("main"), pieces=["body", "ends", "zippanel"]),
        step("w3", "cut", "Cut the lining", "Cut the lining body and two lining ends.", L("lining"), pieces=["lbody", "lends"]),
        step("w4", "cut", "Cut the fleece", "Cut fleece for the body and ends, without seam allowances.", L("fleece"), pieces=["fbody", "fends"]),
        step("w5", "sew", "Fuse the fleece", "Fuse fleece to the wrong side of the outer body and end panels, 1 cm in from each edge, with a pressing cloth.", T("press", tones=["main", "fleece"], label="fuse fleece, pressing cloth on top"), pieces=["fbody", "fends", "body", "ends"], tech=["interfacing"], timer=2),
        step("w6", "sew", "Attach the webbing handles", "Mark two lines on the body, each a quarter of the length in from the ends. Pin a webbing loop along each line, running across the bottom and up both sides, handles left free above the body. Edgestitch both edges of the webbing and box-stitch with an X where the stitching stops at the top.",
             T("loops", base="main", strap="#3A3530", dist="Lb/4"), meas=[M("Webbing from body ends", "Lb/4"), M("Edgestitch", 3, "mm")], pieces=["body"], tech=["attaching-straps", "edgestitching"],
             tips=["Use a 100/16 needle and walk the wheel by hand over the webbing joins."]),
        step("w7", "sew", "Install the zipper", "Press 1 cm under on one long edge of each zipper panel. Place the folds 3 mm from the zipper teeth, one on each side, and topstitch with a zipper foot.", T("edgestitch", tone="main", dist=3, label="panel folds 3 mm from the teeth"), meas=[M("Fold to teeth", 3, "mm")], pieces=["zippanel"], tech=["zipper", "topstitching"]),
        step("w8", "assemble", "Make the main tube", "Sew the long raw edges of the zipper unit to the top edges of the body, right sides together, with 1 cm seams, forming a tube. Topstitch the seams 5 mm towards the body.", T("sew", tone="main", sides="tb", label="zipper unit + body → tube"), meas=[M("Seam allowance", "sa")], pieces=["zippanel", "body"]),
        step("w9", "assemble", "Sew in the end panels", "OPEN THE ZIPPER halfway. Mark the corners of each end panel 1 cm in. Clip the tube's seam allowance at the corresponding points. Sew each end panel into the tube right sides together, stopping with the needle down at each corner, pivoting and continuing.", T("sew", tone="main", sides="ltrb", label="end panel into the tube · pivot at corners"),
             beginner="Pivoting means stopping exactly at the corner mark with the needle down, lifting the foot, turning the work 90° and carrying on. Clipping the tube's allowance at the corners lets it turn the corner flat.", meas=[M("Seam allowance", "sa")], pieces=["ends", "body"], tech=["seam-allowance", "clipping-corners"], warn=["Open the zipper before sewing the second end, or you can't turn the bag."]),
        step("w10", "assemble", "Turn and shape", "Trim the corners, turn right side out through the zipper and push out the corners.", T("turn", tone="main", label="turn through the open zipper"), tech=["clipping-corners"]),
        step("w11", "assemble", "Sew the lining", "Sew the lining body to the lining ends the same way (pivoting at the corners). Leave the top open. Press 1 cm to the wrong side along both top edges.", T("sew", tone="lining", sides="lrb", label="lining body + ends, top left open"), pieces=["lbody", "lends"], tech=["lining"]),
        step("w12", "finish", "Hand-stitch the lining", "Drop the lining into the bag, wrong sides together. Pin the folded top edges to the zipper tape, just clear of the teeth, and slip-stitch by hand.", T("hand", tone="lining", stitch="ladder"), pieces=["lbody"], tech=["ladder-stitch"]),
        step("w13", "finish", "Pack your bag", "Run the zipper end to end, check the handles and you're ready to travel.", G()),
    ],
    gallery=[{"label": "Duffel", "scene": scene(
        {"k": "poly", "pts": [[60, 120], [300, 120], [340, 100], [340, 220], [300, 250], [60, 250]], "tone": "main"},
        {"k": "poly", "pts": [[60, 120], [100, 95], [340, 95], [300, 120]], "tone": "zippanel"}, {"k": "zip", "x": 90, "y": 108, "w": 220},
        {"k": "cord", "pts": [[120, 250], [120, 120], [150, 40], [210, 40], [240, 120], [240, 250]], "color": "#3A3530"},
        {"k": "poly", "pts": [[300, 120], [340, 100], [340, 220], [300, 250]], "tone": "ends"})}],
    related=["classic-tote", "zip-pouch", "fabric-basket"],
))

# ---------------------------------------------------------------- community guides
C = []
C.append(dict(
    id="lavender-sachet", title="Lavender Sachets", author="Maya R.", category="gifts", difficulty="beginner",
    summary="Tiny scented pillows for drawers and wardrobes — hand-sewn in an evening.",
    description="I make a batch of these every winter from shirt offcuts. Fill with dried lavender (or rice + a few drops of essential oil). Shared from my sewing notebook!",
    tags=["gifts", "home", "beginner", "hand-sewing", "scraps", "upcycling"],
    minutes=[30, 45], costUSD=[2, 6], machineRequired=False, popularity=55,
    constants={"sa": 1},
    finished={"label": "Each sachet", "dims": [{"label": "Size", "value": 10}]},
    tools=["hand-needle", "scissors", "pins", "funnel?"],
    materials=[fabric("main", "Tightly woven cotton scraps", "#9C8AB4", "Sachet.", ["Quilting cotton", "Shirting", "Linen"], 50, "single", [50, 112]),
               notion("lav", "Dried lavender", "About 2 tablespoons per sachet", "Scent.", "#8C7BA8", ["Rice + essential oil"]), "thread"],
    pieces=[piece("sq", "Sachet square", "main", 2, 12, 12, "#9C8AB4", grain="any")],
    steps=[
        step("ls1", "cut", "Cut two squares", "Cut two 12 cm squares from a tightly woven fabric so the lavender doesn't poke through.", L("main"), pieces=["sq"]),
        step("ls2", "sew", "Backstitch three sides", "Right sides together, backstitch round three sides and 2 cm into the fourth, 1 cm from the edge.", T("sew", tone="main", sides="ltrb", gap="t", gapLabel="opening"), meas=[M("Seam allowance", "sa")], pieces=["sq"], tech=["backstitching"]),
        step("ls3", "sew", "Turn", "Clip the corners and turn right side out.", T("turn", tone="main"), tech=["clipping-corners"]),
        step("ls4", "assemble", "Fill", "Spoon in the lavender until it's about two-thirds full.", T("fill", tone="main", label="⅔ full")),
        step("ls5", "finish", "Close with ladder stitch", "Fold the edges in and ladder-stitch closed. I add a ribbon loop in the seam for hanging.", T("close", tone="main", method="hand"), pieces=["sq"], tech=["ladder-stitch"]),
    ],
    gallery=[{"label": "Sachet", "scene": scene({"k": "panel", "x": 120, "y": 70, "w": 160, "h": 160, "tone": "main", "rx": 22}, {"k": "cord", "pts": [[200, 72], [185, 30], [215, 30], [200, 72]], "color": "#C0583A"})}],
    review={"status": "published", "technicallyValidated": False, "updated": "2026-11-02"},
))
C.append(dict(
    id="pet-bandana", title="Reversible Pet Bandana", author="stitchwithsam", category="accessories", difficulty="beginner",
    summary="A two-sided triangle bandana that slips over your dog's collar.",
    description="My dog has one for every season! Sewn as a square, cut into triangles and turned; the top edge folds over to make a channel for the collar. Measure the collar and adjust the square.",
    tags=["accessories", "gifts", "pets", "reversible", "quick"],
    minutes=[30, 45], costUSD=[3, 8], machineRequired=True, popularity=60,
    constants={"sa": 1},
    params=[{"id": "S", "label": "Square size", "default": 40, "min": 25, "max": 60, "step": 5, "help": "About the collar length + 5 cm."}],
    sizes=[{"id": "s", "label": "Small dog", "values": {"S": 30}}, {"id": "m", "label": "Medium dog", "values": {"S": 40}}, {"id": "l", "label": "Large dog", "values": {"S": 55}}],
    customNote="Each side is a square cut diagonally; the long edge is about 1.4 × the square.",
    finished={"label": "Finished bandana", "dims": [{"label": "Long edge (approx.)", "value": "S*1.41 - 2"}]},
    tools=["machine", "scissors", "ruler", "pins", "iron"],
    materials=[fabric("main", "Side A cotton", "#C26A4E", "One side.", ["Quilting cotton"], 112, "single", [50, 112]),
               fabric("back", "Side B cotton", "#5E7C8A", "Other side.", ["Quilting cotton"], 112, "single", [50, 112]), "thread"],
    pieces=[piece("a", "Side A square", "main", 1, "S", "S", "#C26A4E", grain="any", markings=["Cut diagonally after sewing"]), piece("b", "Side B square", "back", 1, "S", "S", "#5E7C8A", grain="any")],
    steps=[
        step("pb1", "cut", "Cut side A", "Cut a square from side A fabric.", L("main"), pieces=["a"]),
        step("pb2", "cut", "Cut side B", "Cut the same size square from side B.", L("back"), pieces=["b"]),
        step("pb3", "sew", "Sew round the square", "Right sides together, sew all round with 1 cm, leaving a 6 cm gap in the middle of one side.", T("sew", tone="back", sides="ltrb", gap="t", gapLabel="6 cm gap"), meas=[M("Seam allowance", "sa")], pieces=["a", "b"]),
        step("pb4", "sew", "Turn, press and topstitch", "Clip the corners, turn, press, then topstitch 5 mm all round, closing the gap.", T("topstitch", tone="main", dist=0.5), pieces=["a"], tech=["topstitching", "clipping-corners"]),
        step("pb5", "finish", "Fold over the collar channel", "Fold the square into a triangle with side B showing on the top flap. Stitch a line 3 cm below the fold to make a channel for the collar.", T("fold", tone="main", label="fold into a triangle, stitch a collar channel"), meas=[M("Channel depth", 3)], pieces=["b"]),
        step("pb6", "finish", "Slide onto the collar", "Thread the collar through the channel.", G()),
    ],
    gallery=[{"label": "Bandana", "scene": scene({"k": "poly", "pts": [[60, 80], [340, 80], [200, 260]], "tone": "main"}, {"k": "panel", "x": 60, "y": 66, "w": 280, "h": 24, "tone": "back"})}],
    review={"status": "published", "technicallyValidated": False, "updated": "2026-11-09"},
))
C.append(dict(
    id="makeup-pads", title="Reusable Makeup Remover Pads", author="Ana K.", category="upcycling", difficulty="beginner",
    summary="Washable cotton pads from an old towel and flannel scraps.",
    description="Zero-waste swap I love. Terry on one side for scrubbing, soft flannel on the other. Sew a dozen and keep them in a jar by the sink.",
    tags=["upcycling", "home", "gifts", "zero waste", "quick"],
    minutes=[40, 60], costUSD=[0, 5], machineRequired=True, popularity=58,
    constants={"sa": 0.7},
    finished={"label": "Each pad", "dims": [{"label": "Size", "value": 8.6}]},
    tools=["machine", "scissors", "pins"],
    materials=[fabric("main", "Old cotton towel (terry)", "#E6D8C4", "Scrubby side.", ["Cotton terry", "Bamboo terry"], 50, "single", [50]),
               fabric("back", "Cotton flannel scraps", "#B5727D", "Soft side.", ["Flannel"], 50, "single", [50, 112]), "thread"],
    pieces=[piece("t", "Terry square", "main", 12, 10, 10, "#E6D8C4", grain="any"), piece("f", "Flannel square", "back", 12, 10, 10, "#B5727D", grain="any")],
    steps=[
        step("mp1", "cut", "Cut terry squares", "Cut 12 squares of terry from the towel, skipping the hemmed edges.", L("main"), pieces=["t"]),
        step("mp2", "cut", "Cut flannel squares", "Cut 12 flannel squares.", L("back"), pieces=["f"]),
        step("mp3", "sew", "Sew pairs", "Pair terry and flannel right sides together and sew round with 7 mm, leaving a 4 cm gap.", T("sew", tone="back", sides="ltrb", gap="b", gapLabel="4 cm gap", sa=0.7), meas=[M("Seam allowance", "sa")], pieces=["t", "f"]),
        step("mp4", "sew", "Turn and topstitch", "Clip, turn, and topstitch 3 mm round the edge, closing the gap.", T("topstitch", tone="back", dist=0.3), tech=["topstitching"]),
        step("mp5", "finish", "Use and wash", "Wash in a mesh bag with your towels.", G()),
    ],
    gallery=[{"label": "Pads", "scene": scene(*[{"k": "panel", "x": 90 + i * 30, "y": 90 + i * 20, "w": 130, "h": 130, "tone": "back" if i % 2 else "main", "rx": 10} for i in range(3)])}],
    review={"status": "published", "technicallyValidated": False, "updated": "2026-11-11"},
))

def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if v is not None}
    if isinstance(o, list): return [clean(v) for v in o]
    return o

for i, p in enumerate(P, start=6):
    with open(os.path.join(ROOT, "projects", f"{i:02d}-{p['id']}.json"), "w") as f:
        json.dump(clean(p), f, indent=1, ensure_ascii=False)
os.makedirs(os.path.join(ROOT, "community"), exist_ok=True)
for p in C:
    with open(os.path.join(ROOT, "community", f"{p['id']}.json"), "w") as f:
        json.dump(clean(p), f, indent=1, ensure_ascii=False)
print(len(P), "projects,", len(C), "community")
