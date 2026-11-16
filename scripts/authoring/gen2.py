import json, os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *  # noqa

ROOT = sys.argv[1]
P = []
CIRCLE = "M {hw} 0 A {hw} {hw} 0 1 1 {hw} {h} A {hw} {hw} 0 1 1 {hw} 0 Z"

# ======================================================================== 1 Japanese knot bag
KNOT = "M 0 14 L 9 14 C 9 26 12 32 17 32 C 22 32 25 26 25 18 L 25 0 L 34 0 L 34 57 Q 34 62 29 62 L 5 62 Q 0 62 0 57 Z"
knot_scene = scale_path(KNOT, 4, 132, 26)
P.append(project(
    id="japanese-knot-bag", title="Japanese Knot Bag", category="bags", difficulty="beginner",
    summary="A small reversible-look wristlet: the long handle slips through the short one to close it.",
    description="The knot bag (sometimes called an azuma-style or knot wristlet) is a traditional Japanese shape: one long and one short handle. Thread the long handle through the short loop to close the bag, or carry it over your wrist. It's fully lined with every seam hidden, and it's a lovely introduction to sewing curves.",
    tags=["bags", "gifts", "beginner", "lined", "curves", "japanese", "wristlet"],
    minutes=[90, 150], costUSD=[6, 15], machineRequired=True, popularity=94, featured=True,
    constants={"sa": 1},
    finished={"label": "Finished bag (approx.)", "dims": [{"label": "Width", "value": 32}, {"label": "Body height", "value": 29}, {"label": "Long handle loop", "value": 58}, {"label": "Short handle loop", "value": 30}]},
    tools=["machine", "scissors", "pins", "iron", "point-turner?", "hand-needle", "safety-pin?"],
    materials=[
        fabric("main", "Outer fabric", "#3F6E8C", "Outside of the bag and handles.", ["Quilting cotton", "Linen", "Light canvas", "Japanese print cotton"], 112, "folded", [112, 140], weight="Light–medium", alts=["A furoshiki or vintage kimono cotton"]),
        fabric("lining", "Lining fabric", "#E3C48D", "Inside — it shows on the handle edges, so choose a contrast you like.", ["Quilting cotton", "Linen"], 112, "folded", [112, 140]),
        "thread"],
    pieces=[
        piece("outer", "Outer body", "main", 2, 34, 62, "#3F6E8C", markings=["Notch both outer side edges 32 cm below the long-handle top — side seams stop here"]),
        piece("liningp", "Lining body", "lining", 2, 34, 62, "#E3C48D", markings=["Notch both outer side edges 32 cm below the long-handle top", "Mark a 10 cm turning gap in the bottom of ONE piece"]),
    ],
    steps=[
        step("kb1", "prep", "Press your fabrics", "Pre-wash and press both fabrics. Cotton and linen with a little body make the handles hold their shape.", T("press", tones=["main", "lining"]), tech=["prewash", "pressing"]),
        step("kb2", "cut", "Print the pattern piece", "This bag has curves, so print the pattern piece at 100% scale (Print pattern), check the test square, and tape the pages together. One pattern piece is used four times.", {"type": "scene", "scene": scene(
            {"k": "path", "d": knot_scene, "tone": "#F5F1EA", "label": "pattern piece", "lx": 200, "ly": 200},
            {"k": "label", "x": 166, "y": 74, "text": "short", "anchor": "middle", "bold": True}, {"k": "label", "x": 248, "y": 18, "text": "long", "anchor": "middle", "bold": True},
            {"k": "dim", "from": [132, 290], "to": [268, 290], "value": 34})},
             beginner="Printing means the curves come out exactly as designed. The short and long handles must not be swapped — the label on the print shows which is which.", tech=["seam-allowance"]),
        step("kb3", "cut", "Cut the outer", "Fold the outer fabric right sides together and pin the pattern through both layers. Cutting through two layers gives you a mirrored pair — exactly what you need. Transfer the side notches.", L("main"), pieces=["outer"],
             warn=["Cut slowly round the curves with the tips of sharp scissors, keeping your other hand clear of the blades."]),
        step("kb4", "cut", "Cut the lining", "Cut a mirrored pair from the lining fabric the same way and transfer the notches.", L("lining"), pieces=["liningp"]),
        step("kb5", "sew", "Sew the outer sides and bottom", "Place the outer pieces right sides together. Sew from one notch, down the side, across the bottom and up to the other notch with a 1 cm seam. Backstitch at both notches. Clip into the seam allowance at the rounded corners.",
             {"type": "scene", "scene": scene(
                 {"k": "path", "d": knot_scene, "tone": "main", "side": "wrong", "label": "right sides together", "lx": 200, "ly": 210},
                 {"k": "stitch", "pts": [[136, 154], [136, 254], [142, 266], [254, 266], [260, 254], [260, 154]]},
                 {"k": "focus", "x": 136, "y": 154, "r": 10}, {"k": "focus", "x": 260, "y": 154, "r": 10},
                 {"k": "label", "x": 60, "y": 158, "text": "stop at notch", "bold": True})},
             meas=[M("Seam allowance", "sa"), M("Stop below long-handle top", 32)], pieces=["outer"], tech=["seam-allowance", "backstitching", "sewing-curves"]),
        step("kb6", "sew", "Sew the lining the same way", "Repeat with the lining, but leave a 10 cm gap in the middle of the bottom seam for turning.", {"type": "scene", "scene": scene(
                 {"k": "path", "d": knot_scene, "tone": "lining", "side": "wrong", "label": "lining", "lx": 200, "ly": 210},
                 {"k": "stitch", "pts": [[136, 154], [136, 254], [142, 266], [176, 266]]}, {"k": "stitch", "pts": [[220, 266], [254, 266], [260, 254], [260, 154]]},
                 {"k": "gap", "from": [176, 284], "to": [220, 284], "label": "10 cm gap"})},
             meas=[M("Turning gap", 10)], pieces=["liningp"], tech=["ladder-stitch"]),
        step("kb7", "assemble", "Nest outer inside lining", "Turn the outer bag right side out. Push it inside the lining (lining still wrong side out) so the right sides face each other. Match the side seams and line up every handle and curve. Pin all along the top edges.",
             T("layer", base="main", top="lining", label="outer inside lining — right sides together"), pieces=["outer", "liningp"], tech=["lining"]),
        step("kb8", "assemble", "Sew round the curves and handles", "Sew with a 1 cm seam along the inner scoop between the handles and along both long edges of every handle, stopping 3 cm before each handle end. Leave the four handle ends open — they are joined later. Backstitch at every stop.",
             {"type": "scene", "scene": scene(
                 {"k": "path", "d": knot_scene, "tone": "lining", "side": "wrong", "lx": 200, "ly": 210, "label": "lining (outer inside)"},
                 {"k": "stitch", "pts": [[168, 94], [168, 130], [178, 150], [200, 154], [222, 150], [232, 130], [232, 38]]},
                 {"k": "stitch", "pts": [[136, 94], [136, 154]]}, {"k": "stitch", "pts": [[264, 38], [264, 154]]},
                 {"k": "gap", "from": [132, 74], "to": [168, 74], "label": "end open"}, {"k": "gap", "from": [232, 18], "to": [268, 18], "label": "end open"})},
             beginner="Think of it as sewing round the whole top edge of a bag, except the four little handle ends, which stay open so the handles can be joined later. Go slowly around the curve, stopping with the needle down to pivot slightly as you go.",
             expert="Sew inner curve + both handle edges RST at 1 cm; stop 3 cm short of handle ends.",
             meas=[M("Seam allowance", "sa"), M("Stop before handle ends", 3)], pieces=["outer", "liningp"], tech=["sewing-curves", "backstitching"]),
        step("kb9", "assemble", "Clip the curves", "Clip into the seam allowance every 1.5 cm around the inner curve, close to but not through the stitching, so it lies smooth when turned.", T("clip", tone="lining"), meas=[M("Clip spacing", 1.5)], tech=["clipping-corners", "sewing-curves"]),
        step("kb10", "assemble", "Turn right side out", "Pull the whole bag through the gap in the lining. Push the handles out fully with a point turner or chopstick and push the lining down inside the bag. Press the curved edges so the seam sits right on the edge.", T("turn", tone="lining", label="pull through the lining gap"), tech=["pressing"]),
        step("kb11", "assemble", "Join the handle ends", "Take the two SHORT handle ends. Pull the lining layers out of the way and pin the two outer ends right sides together; sew across with 1 cm. Do the same for the two lining ends. Press open. Repeat with the two LONG handle ends. Tuck the remaining short gaps on each handle edge in line with the seams.",
             {"type": "scene", "scene": scene(
                 {"k": "panel", "x": 80, "y": 90, "w": 100, "h": 70, "tone": "main", "side": "wrong", "label": "outer ends RST"},
                 {"k": "panel", "x": 220, "y": 90, "w": 100, "h": 70, "tone": "lining", "side": "wrong", "label": "lining ends RST"},
                 {"k": "stitch", "pts": [[80, 102], [180, 102]]}, {"k": "stitch", "pts": [[220, 102], [320, 102]]},
                 {"k": "label", "x": 200, "y": 210, "text": "short to short · long to long", "anchor": "middle", "bold": True})},
             beginner="It's fiddly: the handle becomes a loop and the fabric twists a little. Keep the outer and lining layers separate while you sew each ring, and check nothing is twisted before sewing.",
             meas=[M("Seam allowance", "sa")], pieces=["outer", "liningp"], tech=["seam-allowance"]),
        step("kb12", "finish", "Close the openings", "Slip-stitch (ladder-stitch) the short open sections on each handle edge, then close the lining gap by machine or by hand.", T("close", tone="main", method="hand"), pieces=["liningp"], tech=["ladder-stitch"]),
        step("kb13", "finish", "Topstitch all edges", "Topstitch 5 mm from every edge — round the inner curve and both edges of each handle — to keep the lining from rolling out.", T("topstitch", tone="main", dist=0.5, all=False), meas=[M("Topstitch", 0.5)], pieces=["outer"], tech=["topstitching"]),
        step("kb14", "finish", "Tie the knot", "Slip the long handle through the short loop and carry it on your wrist. To open, slide the long handle back out.", G("Long handle through the short loop")),
    ],
    gallery=[{"label": "Knot bag", "scene": scene(
        {"k": "path", "d": scale_path(KNOT, 3.8, 135, 40), "tone": "main"},
        {"k": "stitch", "pts": [[168, 100], [169, 135], [180, 158], [200, 162], [220, 158], [228, 135], [229, 46]]},
        {"k": "cord", "pts": [[248, 44], [230, 30], [175, 70], [160, 110]], "color": "lining"})}],
    related=["classic-tote", "zip-pouch", "scrunchie"],
))

# ======================================================================== 2 bucket bag
P.append(project(
    id="bucket-bag", title="Drawstring Bucket Bag", category="bags", difficulty="intermediate",
    summary="A round-bottomed, lined bucket bag with eyelets, a drawstring and a shoulder strap.",
    description="A circular base and a tube body make a soft, roomy bucket. You'll learn to sew a curve to a straight edge evenly, install eyelets and make a drawstring channel between outer and lining.",
    tags=["bags", "lined", "curves", "drawstring", "eyelets"],
    minutes=[180, 270], costUSD=[18, 35], machineRequired=True, popularity=82, featured=True,
    constants={"sa": 1},
    params=[{"id": "D", "label": "Base diameter", "default": 20, "min": 16, "max": 26, "step": 1}, {"id": "H", "label": "Height", "default": 28, "min": 20, "max": 34, "step": 1}],
    sizes=[{"id": "s", "label": "Small", "values": {"D": 16, "H": 22}}, {"id": "m", "label": "Standard", "values": {"D": 20, "H": 28}}, {"id": "l", "label": "Large", "values": {"D": 24, "H": 32}}],
    customNote="The base is a circle of the finished diameter plus seam allowance; the body is exactly π × diameter around (plus seam allowances), so the two always match. Strap and eyelet position stay fixed.",
    finished={"label": "Finished bag", "dims": [{"label": "Base diameter", "value": "D"}, {"label": "Height", "value": "H"}, {"label": "Circumference", "value": "3.1416*D"}]},
    tools=["machine", "needle-90", "scissors", "ruler", "marker", "pins", "clips", "iron", "pressing-cloth", "safety-pin", "hand-needle?"],
    materials=[
        fabric("main", "Outer — canvas or denim", "#8E4A36", "Outside, base and strap.", ["Cotton canvas", "Denim", "Waxed canvas (no iron)"], 112, "single", [112, 140], weight="Medium–heavy"),
        fabric("lining", "Lining — cotton", "#E3C48D", "Inside.", ["Quilting cotton", "Poplin"], 112, "single", [112, 140]),
        fabric("intf", "Fusible fleece or heavy interfacing", "#ECE7DD", "Structure, especially the base.", ["Fusible fleece", "Fusible foam for the base"], 90, "single", [90], kind="interfacing"),
        notion("cord", "Cord, 5–6 mm", "{3.1416*D + 60} long", "The drawstring.", "#E8E0D2", ["Leather lace"]),
        notion("eyelets", "Eyelets (grommets), 10 mm inner", "2 + setting tool", "Where the drawstring exits.", "#B9C1C6", ["Two vertical buttonholes"]),
        "thread"],
    pieces=[
        piece("body", "Outer body", "main", 1, "3.1416*D + 2*sa", "H + 2*sa", "#8E4A36", markings=["Mark quarter points along the bottom edge"]),
        piece("base", "Outer base", "main", 1, "D + 2*sa", "D + 2*sa", "#6E3828", markings=["Mark quarter points on the edge"]),
        piece("strap", "Strap", "main", 1, 10, 110, "#A85E46", sa=0, grain="any"),
        piece("lbody", "Lining body", "lining", 1, "3.1416*D + 2*sa", "H + 2*sa", "#E3C48D"),
        piece("lbase", "Lining base", "lining", 1, "D + 2*sa", "D + 2*sa", "#C9A06A"),
        piece("ibody", "Interfacing body", "intf", 1, "3.1416*D", "H", "#CFC8BA", sa=0),
        piece("ibase", "Interfacing base", "intf", 1, "D", "D", "#CFC8BA", sa=0),
    ],
    steps=[
        step("bk1", "prep", "Press", "Press the outer and lining fabrics.", T("press", tones=["main", "lining"]), tech=["pressing"]),
        step("bk2", "cut", "Print the circle and cut the outer", "Print the base circle at 100%. Cut the outer body rectangle, the outer base circle and the strap.", L("main"), pieces=["body", "base", "strap"]),
        step("bk3", "cut", "Cut the lining", "Cut the lining body and lining base.", L("lining"), pieces=["lbody", "lbase"]),
        step("bk4", "cut", "Cut the interfacing", "Cut interfacing for the body and base without seam allowances.", L("intf"), pieces=["ibody", "ibase"]),
        step("bk5", "sew", "Fuse the interfacing", "Fuse the interfacing to the wrong side of the outer body and base, 1 cm in from the edges, using a pressing cloth.", T("press", tones=["main", "intf"], label="fuse with a pressing cloth"), pieces=["ibody", "ibase", "body", "base"], tech=["interfacing"], timer=1),
        step("bk6", "sew", "Make the strap", "Press the strap into a four-fold strap and edgestitch both long edges.", T("strap", tone="strap", width=2.5), pieces=["strap"], tech=["edgestitching"]),
        step("bk7", "sew", "Sew the body into a tube", "Fold the outer body right sides together, short edges matching, and sew with 1 cm. Press open. Repeat for the lining body, leaving a 12 cm gap in the middle of its seam.", T("sew", tone="main", sides="l", label="short edges together → tube"), meas=[M("Seam allowance", "sa"), M("Lining gap", 12)], pieces=["body", "lbody"], tech=["seam-allowance"]),
        step("bk8", "sew", "Staystitch and clip the tube bottom", "Staystitch 8 mm from the bottom edge of each tube, then clip into the allowance every 2 cm, stopping just short of the staystitching. This lets the straight edge spread round the curve.", T("edgestitch", tone="main", dist=8, label="staystitch, then clip every 2 cm"), meas=[M("Staystitch from edge", 0.8), M("Clip spacing", 2)], tech=["staystitching", "sewing-curves"]),
        step("bk9", "sew", "Sew in the base", "Mark quarter points on the base and the tube bottom (the seam is one quarter). Pin the base into the tube right sides together, matching the quarters, then pin generously between. Sew with the tube on top, 1 cm from the edge, easing as you go. Repeat for the lining.",
             {"type": "scene", "scene": scene({"k": "path", "d": "M 200 70 A 110 110 0 1 1 199.9 70 Z", "tone": "base", "side": "wrong", "label": "base", "lx": 200, "ly": 180}, {"k": "stitch", "pts": [[200, 82], [298, 180], [200, 278], [102, 180]], "closed": True}, {"k": "pin", "x": 200, "y": 72}, {"k": "pin", "x": 310, "y": 180, "angle": 0}, {"k": "pin", "x": 200, "y": 288}, {"k": "pin", "x": 90, "y": 180, "angle": 0}, {"k": "label", "x": 200, "y": 30, "text": "match the four quarter marks", "anchor": "middle", "bold": True})},
             beginner="A curve sewn to a straight edge is the trickiest part: go slowly, stop often with the needle down, and smooth only the next 3 cm in front of the foot. Puckers mean you need one more pin.",
             meas=[M("Seam allowance", "sa")], pieces=["base", "body", "lbase", "lbody"], tech=["sewing-curves"]),
        step("bk10", "sew", "Install the eyelets", "On the outer front, mark two eyelet positions 2.5 cm below the top edge, 3 cm either side of the centre. Cut the holes and set the eyelets following the kit instructions.", T("mark", tone="main", label="eyelets 2.5 cm down, 6 cm apart"), meas=[M("Below top edge", 2.5), M("Apart", 6)], pieces=["body"], tech=["eyelets"], warn=["Hammer eyelets on a hard surface with fingers well clear; wear eye protection."]),
        step("bk11", "assemble", "Baste the strap and join the top", "Baste the strap ends to the outer at both sides, raw ends at the top edge. Put the outer (right side out) into the lining (wrong side out) and sew round the top with 1 cm.", T("loops", base="main", strap="strap"), pieces=["strap", "body", "lbody"], tech=["attaching-straps", "lining"]),
        step("bk12", "assemble", "Turn and close", "Turn through the lining gap, close it, push the lining inside and press the top edge.", T("turn", tone="lining"), pieces=["lbody"], tech=["ladder-stitch"]),
        step("bk13", "finish", "Stitch the drawstring channel", "Topstitch round the top 1 cm from the edge, then again 4 cm from the edge, making a channel through which the eyelets open.", T("casing", tone="main", depth=3, insert="cord", gap=False), meas=[M("First line", 1), M("Second line", 4)], pieces=["body"], tech=["casing", "topstitching"]),
        step("bk14", "finish", "Thread the drawstring", "Thread the cord in through one eyelet, all round the channel and out of the other. Knot the ends.", T("cord", tone="main", label="in one eyelet, out the other"), meas=[M("Cord length", "3.1416*D + 60")], tech=["casing"]),
        step("bk15", "finish", "Pull it closed", "Pull the cord to gather the top.", G()),
    ],
    gallery=[{"label": "Bucket bag", "scene": scene(
        {"k": "poly", "pts": [[120, 100], [280, 100], [290, 270], [110, 270]], "tone": "main"},
        {"k": "poly", "pts": ell(200, 100, 80, 14), "tone": "lining"}, {"k": "stitch", "pts": [[118, 120], [282, 120]]},
        {"k": "cord", "pts": [[192, 116], [180, 150], [170, 170]], "color": "#E8E0D2"}, {"k": "cord", "pts": [[208, 116], [222, 150], [232, 168]], "color": "#E8E0D2"},
        {"k": "cord", "pts": [[122, 104], [140, 20], [260, 20], [278, 104]], "color": "strap"})}],
    related=["japanese-knot-bag", "drawstring-backpack"],
))

# ======================================================================== 3 laptop sleeve
P.append(project(
    id="laptop-sleeve", title="Padded Laptop Sleeve", category="bags", difficulty="beginner",
    summary="A snug, padded sleeve with a fold-over flap, made to your laptop's exact size.",
    description="Measure your laptop and the pattern sizes itself, with allowance for the padding. Fusible fleece makes it soft and protective; an elastic loop and button close the flap.",
    tags=["bags", "accessories", "gifts", "padded", "custom size"],
    minutes=[90, 140], costUSD=[10, 22], machineRequired=True, popularity=79,
    constants={"sa": 1, "ease": 2, "flap": 12},
    params=[{"id": "Lw", "label": "Laptop width", "default": 31, "min": 24, "max": 40, "step": 0.5}, {"id": "Lh", "label": "Laptop depth (front to back)", "default": 22, "min": 16, "max": 28, "step": 0.5}, {"id": "Ld", "label": "Laptop thickness", "default": 1.6, "min": 1, "max": 3, "step": 0.1}],
    sizes=[{"id": "13", "label": "13″ laptop", "values": {"Lw": 31, "Lh": 22, "Ld": 1.6}}, {"id": "14", "label": "14″", "values": {"Lw": 32.5, "Lh": 23, "Ld": 1.8}}, {"id": "15", "label": "15–16″", "values": {"Lw": 36, "Lh": 25, "Ld": 2}}],
    customNote="Width = laptop width + thickness + 2 cm padding ease + seam allowances. The length wraps front and back (2 × (depth + thickness + 1 cm)) plus a 12 cm flap. Measure the closed laptop at its largest point.",
    finished={"label": "Finished sleeve (inside)", "dims": [{"label": "Inside width", "value": "Lw + Ld + ease"}, {"label": "Inside depth", "value": "Lh + Ld + ease/2"}, {"label": "Flap", "value": "flap"}]},
    tools=["machine", "scissors", "ruler", "marker", "clips", "iron", "pressing-cloth", "hand-needle", "point-turner?"],
    materials=[
        fabric("main", "Outer fabric", "#5E6B57", "Outside.", ["Cotton canvas", "Waxed canvas", "Denim", "Wool felt"], 112, "single", [112, 140]),
        fabric("lining", "Lining fabric", "#E3C48D", "Inside — something smooth so the laptop slides in.", ["Quilting cotton", "Poplin"], 112, "single", [112, 140]),
        fabric("fleece", "Fusible fleece", "#ECE7DD", "Padding.", ["Fusible fleece", "Fusible foam (firmer)"], 90, "single", [90], kind="interfacing"),
        notion("elastic", "Round elastic cord", "12 cm", "Closure loop.", "#3A3530", ["Hair elastic", "Rouleau loop"]),
        notion("button", "Button, about 2.5 cm", "1", "Closure.", "#C9A06A"),
        "thread"],
    pieces=[
        piece("outer", "Outer", "main", 1, "Lw + Ld + ease + 2*sa", "2*(Lh + Ld + ease/2) + flap + 2*sa", "#5E6B57", markings=["Fold line at {Lh + Ld + ease/2 + sa} from the bottom", "Flap begins {2*(Lh + Ld + ease/2) + sa} from the bottom"]),
        piece("liningp", "Lining", "lining", 1, "Lw + Ld + ease + 2*sa", "2*(Lh + Ld + ease/2) + flap + 2*sa", "#E3C48D"),
        piece("fleecep", "Fleece", "fleece", 1, "Lw + Ld + ease", "2*(Lh + Ld + ease/2) + flap", "#CFC8BA", sa=0),
    ],
    steps=[
        step("ls1", "prep", "Measure your laptop", "Measure the closed laptop's width, depth and thickness at the widest points and enter them in Customise (or pick a size).", T("mark", tone="main", w="Lw", h="Lh", label="your laptop"), meas=[M("Width", "Lw"), M("Depth", "Lh"), M("Thickness", "Ld")]),
        step("ls2", "cut", "Cut the outer", "Cut one long outer rectangle.", L("main"), pieces=["outer"]),
        step("ls3", "cut", "Cut the lining", "Cut the lining the same size.", L("lining"), pieces=["liningp"]),
        step("ls4", "cut", "Cut the fleece", "Cut the fleece without seam allowance.", L("fleece"), pieces=["fleecep"]),
        step("ls5", "sew", "Fuse the fleece", "Fuse the fleece to the wrong side of the outer, 1 cm in from every edge, with a pressing cloth.", T("press", tones=["main", "fleece"], label="fuse the fleece"), pieces=["fleecep", "outer"], tech=["interfacing"], timer=1),
        step("ls6", "sew", "Mark the fold and flap", "On the wrong side of the outer and lining, mark the bottom fold line and the start of the flap.", T("fold", tone="main", label="bottom fold · flap above", dim="Lh + Ld + ease/2"), meas=[M("Bottom to fold", "Lh + Ld + ease/2 + sa")], pieces=["outer", "liningp"]),
        step("ls7", "sew", "Baste the elastic loop", "Fold the elastic cord in half and baste its ends to the centre of the flap's short edge on the outer's right side, loop pointing inwards.", T("loops", base="main", strap="#3A3530"), meas=[M("Loop length (folded)", 5)], pieces=["outer"]),
        step("ls8", "sew", "Sew the outer pocket", "Fold the outer at the bottom fold, right sides together. Sew both sides up to the flap line with 1 cm. Clip the allowance diagonally at the flap line on both sides.", T("sew", tone="main", sides="lr", label="sides up to the flap line"), meas=[M("Seam allowance", "sa")], pieces=["outer"], tech=["seam-allowance"]),
        step("ls9", "sew", "Sew the lining pocket", "Repeat with the lining, leaving a 12 cm gap in one side seam.", T("sew", tone="lining", sides="lr", gap="r", gapLabel="12 cm gap"), meas=[M("Gap", 12)], pieces=["liningp"]),
        step("ls10", "assemble", "Join round the opening and flap", "Turn the outer right side out and slide it into the lining (wrong side out) so right sides face. Match the side seams. Sew all the way round the front opening and up, across and down the flap with 1 cm, pivoting at the corners.", T("sew", tone="lining", sides="ltr", label="opening + flap, right sides together"), pieces=["outer", "liningp"], tech=["lining"]),
        step("ls11", "assemble", "Clip, turn and close", "Clip the flap corners, turn through the lining gap, close the gap and push the lining inside.", T("turn", tone="lining"), tech=["clipping-corners", "ladder-stitch"]),
        step("ls12", "finish", "Topstitch", "Press and topstitch round the opening and the flap, 5 mm from the edge.", T("topstitch", tone="main", dist=0.5), meas=[M("Topstitch", 0.5)], pieces=["outer"], tech=["topstitching"]),
        step("ls13", "finish", "Sew on the button", "Close the flap over the laptop and mark where the loop reaches. Sew the button on through the outer only, with a thread shank.", T("hand", tone="main", stitch="running"), tech=["buttonholes"]),
        step("ls14", "finish", "Slide your laptop in", "It should be snug but slide in easily.", G()),
    ],
    gallery=[{"label": "Sleeve", "scene": scene(
        {"k": "panel", "x": 70, "y": 80, "w": 260, "h": 180, "tone": "main", "rx": 6}, {"k": "poly", "pts": [[70, 80], [330, 80], [330, 140], [70, 140]], "tone": "main"},
        {"k": "stitch", "pts": [[78, 88], [322, 88], [322, 132], [78, 132]], "closed": True},
        {"k": "path", "d": "M 200 150 A 9 9 0 1 1 199.9 150 Z", "tone": "#C9A06A"}, {"k": "cord", "pts": [[200, 140], [190, 152], [200, 164], [210, 152], [200, 140]], "color": "#3A3530"})}],
    related=["zip-pouch", "crossbody-bag"],
))

# ======================================================================== 4 crossbody
P.append(project(
    id="crossbody-bag", title="Zip Crossbody Bag", category="bags", difficulty="intermediate",
    summary="A small lined zip bag with an adjustable webbing strap on D-rings.",
    description="Builds on the zip pouch: add D-ring tabs in the side seams and assemble an adjustable strap with a slider. Big enough for phone, keys and wallet.",
    tags=["bags", "zipper", "lined", "hardware", "adjustable strap"],
    minutes=[150, 210], costUSD=[15, 30], machineRequired=True, popularity=86, featured=True,
    constants={"sa": 1, "D": 4},
    finished={"label": "Finished bag", "dims": [{"label": "Width", "value": 24}, {"label": "Height", "value": 16}, {"label": "Depth", "value": "D"}, {"label": "Strap (max)", "value": 130}]},
    tools=["machine", "needle-90", "zip-foot", "scissors", "ruler", "marker", "clips", "iron", "pressing-cloth", "point-turner?"],
    materials=[
        fabric("main", "Outer fabric", "#B5727D", "Outside and tabs.", ["Light canvas", "Quilting cotton", "Faux leather (no iron)"], 112, "folded", [112, 140]),
        fabric("lining", "Lining fabric", "#7E98A8", "Inside.", ["Quilting cotton"], 112, "folded", [112, 140]),
        fabric("intf", "Medium fusible interfacing", "#ECE7DD", "Body.", ["Woven fusible interfacing", "Fusible fleece"], 90, "single", [90], kind="interfacing"),
        notion("zipper", "Coil zipper", "At least 32 cm", "Top opening.", "#2E3A40"),
        notion("webbing", "Webbing, 2.5 cm wide", "140 cm", "Strap.", "#3A3530", ["Cotton strap made from the outer fabric"]),
        notion("hardware", "2 D-rings + 1 strap slider, 2.5 cm", "1 set", "Adjustable strap hardware.", "#B9C1C6", ["Swivel clips instead of D-rings for a detachable strap"]),
        "thread"],
    pieces=[
        piece("outer", "Outer panel", "main", 2, "24 + D + 2*sa", "16 + D/2 + 2*sa", "#B5727D", markings=["Cut {D/2} squares from both bottom corners"]),
        piece("ringtab", "D-ring tab", "main", 2, 6, 8, "#93565F", sa=0, grain="any"),
        piece("ziptab", "Zip end tab", "main", 2, 5, 8, "#93565F", sa=0, grain="any"),
        piece("liningp", "Lining panel", "lining", 2, "24 + D + 2*sa", "16 + D/2 + 2*sa", "#7E98A8"),
        piece("intfp", "Interfacing", "intf", 2, "24 + D", "16 + D/2", "#CFC8BA", sa=0),
    ],
    steps=[
        step("cb1", "prep", "Press", "Press fabrics. If using faux leather, skip the iron and use clips instead of pins.", T("press", tones=["main", "lining"]), tech=["pressing"]),
        step("cb2", "cut", "Cut the outer pieces", "Cut two outer panels, two D-ring tabs and two zip end tabs.", L("main"), pieces=["outer", "ringtab", "ziptab"]),
        step("cb3", "cut", "Cut the lining", "Cut two lining panels.", L("lining"), pieces=["liningp"]),
        step("cb4", "cut", "Cut the interfacing", "Cut two interfacing panels without seam allowance.", L("intf"), pieces=["intfp"]),
        step("cb5", "sew", "Fuse and notch", "Fuse interfacing to the outer panels, then cut the corner squares from outer and lining panels.", T("notch", tone="main", value="D/2"), meas=[M("Corner square", "D/2")], pieces=["intfp", "outer", "liningp"], tech=["interfacing", "boxed-corners"]),
        step("cb6", "sew", "Make the D-ring tabs", "Press each D-ring tab into a four-fold strip and edgestitch. Slip a D-ring on and fold the tab in half; baste across close to the ring.", T("strap", tone="ringtab", width=1.5), pieces=["ringtab"], tech=["edgestitching", "adjustable-strap"]),
        step("cb7", "sew", "Zipper tabs and zipper", "Wrap the zip ends in the zip tabs (trimmed so the total span equals the panel width minus 2 cm), then sew the zipper between outer and lining on both sides with the sandwich method, and topstitch.", T("zip", tone="main", lining="lining"), meas=[M("Zip + tabs span", "24 + D")], pieces=["ziptab", "outer", "liningp"], tech=["zipper", "topstitching"]),
        step("cb8", "assemble", "Baste the D-ring tabs", "Open the zipper halfway. Baste a D-ring tab to each side edge of the FRONT outer panel, 2 cm below the zipper, ring pointing inwards.", T("loops", base="main", strap="ringtab"), meas=[M("Below zipper", 2)], pieces=["ringtab"]),
        step("cb9", "assemble", "Sew outer and lining", "Outer panels right sides together and lining panels right sides together. Sew sides and bottoms with 1 cm, leaving the corner squares open and an 8 cm gap in the lining bottom.", T("sew", tone="main", sides="lbr", gap="b", gapLabel="lining gap 8 cm", notch=True), pieces=["outer", "liningp"], warn=["Make sure the zipper is open."]),
        step("cb10", "assemble", "Box the corners and turn", "Box all four corners with 1 cm seams, turn through the lining gap, close the gap and shape.", T("box", tone="main", depth="D"), meas=[M("Boxing seam = depth", "D")], tech=["boxed-corners", "ladder-stitch"]),
        step("cb11", "finish", "Assemble the strap", "Thread one webbing end through the slider centre bar and stitch it down. Take the other end through a D-ring, back through the slider, then through the second D-ring; fold the end under and box-stitch with an X.",
             {"type": "scene", "scene": scene(
                 {"k": "cord", "pts": [[30, 150], [120, 150], [200, 140], [300, 150], [370, 150]], "color": "#3A3530"},
                 {"k": "path", "d": "M 40 135 L 40 165 A 15 15 0 0 0 40 135 Z", "tone": "#B9C1C6"}, {"k": "path", "d": "M 360 135 L 360 165 A 15 15 0 0 1 360 135 Z", "tone": "#B9C1C6"},
                 {"k": "panel", "x": 190, "y": 128, "w": 22, "h": 30, "tone": "#B9C1C6", "rx": 3}, {"k": "label", "x": 200, "y": 205, "text": "D-ring · slider · D-ring", "anchor": "middle", "bold": True})},
             tech=["adjustable-strap"], tips=["Melt or zigzag the cut webbing ends so they don't fray."]),
        step("cb12", "finish", "Ready to wear", "Clip on and adjust the length with the slider.", G()),
    ],
    gallery=[{"label": "Crossbody", "scene": scene(
        {"k": "panel", "x": 110, "y": 130, "w": 180, "h": 120, "tone": "main", "rx": 10}, {"k": "zip", "x": 110, "y": 126, "w": 180},
        {"k": "cord", "pts": [[112, 146], [90, 60], [200, 10], [310, 60], [288, 146]], "color": "#3A3530"})}],
    related=["zip-pouch", "laptop-sleeve", "weekender-duffel"],
))

# ======================================================================== 5 grocery bag
GROC = "M 0 0 L 9 0 C 9 12 13 18 20 18 C 27 18 31 12 31 0 L 40 0 L 40 60 L 0 60 Z"
P.append(project(
    id="grocery-bag", title="Foldable Grocery Bag", category="bags", difficulty="beginner",
    summary="A lightweight T-shirt-style shopping bag in ripstop, finished with French seams.",
    description="The classic reusable 'T-shirt' bag: handles are part of the pattern, every seam is enclosed and it folds up small enough for a pocket. A great way to practise French seams and narrow hems on curves.",
    tags=["bags", "gifts", "beginner", "zero waste", "french seams", "curves"],
    minutes=[60, 90], costUSD=[5, 12], machineRequired=True, popularity=75,
    constants={"sa": 1},
    finished={"label": "Finished bag", "dims": [{"label": "Width", "value": 38}, {"label": "Height incl. handles", "value": 58}]},
    tools=["machine", "scissors", "pins", "clips", "iron", "seam-gauge?"],
    materials=[fabric("main", "Ripstop nylon or light cotton", "#5E7C8A", "The whole bag.", ["Ripstop nylon", "Poplin", "Parachute fabric"], 140, "folded", [112, 140, 150], weight="Light", alts=["An old umbrella canopy (upcycled)"]), "thread"],
    pieces=[piece("body", "Bag body", "main", 2, 40, 60, "#5E7C8A")],
    steps=[
        step("gb1", "prep", "Press (cool iron)", "Press the fabric on a low, synthetic setting — nylon melts at cotton temperatures. Test on a scrap first.", T("press", tones=["main"], label="cool iron · test first"), warn=["Nylon melts — use a low iron setting and a pressing cloth."]),
        step("gb2", "cut", "Print the pattern and cut two", "Print the curved body pattern at 100%. Fold the fabric and cut two bodies at once.", L("main"), pieces=["body"]),
        step("gb3", "sew", "French seam: first pass", "Place the bodies WRONG sides together. Sew the sides and bottom with 0.5 cm, and the two short seams across the handle tops. Trim to 3 mm.", T("sew", tone="main", sides="lbr", sa=0.5, label="WRONG sides together"), meas=[M("First seam", 0.5)], pieces=["body"], tech=["french-seam"]),
        step("gb4", "sew", "French seam: second pass", "Turn wrong side out, press the seams flat on the edge, and sew again 0.7 cm in, enclosing the raw edges. Do the same at the handle tops.", T("sew", tone="main", sides="lbr", sa=0.7, label="right sides together"), meas=[M("Second seam", 0.7)], pieces=["body"], tech=["french-seam"]),
        step("gb5", "sew", "Hem the opening and handles", "Turn right side out. Press a narrow double hem (0.5 cm + 0.5 cm) round the scooped opening and along the outer edges of the handles, clipping lightly on the curves, and stitch.", T("hem", tone="main", f1=0.5, f2=0.5), meas=[M("Each fold", 0.5)], pieces=["body"], tech=["hemming", "sewing-curves"]),
        step("gb6", "finish", "Fold and pack", "Fold it in thirds lengthwise, roll it up and tie it with a scrap — or sew a small pocket to one side to stuff it into.", G()),
    ],
    gallery=[{"label": "Bag", "scene": scene({"k": "path", "d": scale_path(GROC, 4.4, 112, 18), "tone": "main"}, {"k": "stitch", "pts": [[154, 40], [158, 80], [200, 98], [244, 80], [248, 40]]})}],
    related=["classic-tote", "gift-bags"],
))
P[-1]["pieces"][0]["outline"] = GROC

# body outlines for knot bag
for pc in P[0]["pieces"]:
    pc["outline"] = KNOT
# circular bases for bucket bag
for pc in P[1]["pieces"]:
    if pc["id"] in ("base", "lbase", "ibase"): pc["outline"] = CIRCLE

# ======================================================================== 6 circle skirt
R = "(hip + 4)/6.2832"
RO = f"({R} + L - bw + nh)"
RI = f"({R} - sa)"
QUARTER = f"M {{sa + {RI}}} 0 L {{sa + {RO}}} 0 L {{sa + {RO}}} {{sa}} A {{{RO}}} {{{RO}}} 0 0 1 {{sa}} {{sa + {RO}}} L 0 {{sa + {RO}}} L 0 {{sa + {RI}}} L {{sa}} {{sa + {RI}}} A {{{RI}}} {{{RI}}} 0 0 0 {{sa + {RI}}} {{sa}} Z"
P.append(project(
    id="circle-skirt", title="Elastic-Waist Circle Skirt", category="clothing", difficulty="intermediate",
    summary="A full, twirly circle skirt drafted from your hip measurement, with a comfy elastic waistband.",
    description="Four quarter-circle panels, drafted with real geometry: the waist radius comes from your hip measurement so the skirt pulls on, and an elastic band gathers it gently to your waist. You'll learn staystitching, sewing bias edges and levelling a hem.",
    tags=["clothing", "skirt", "custom fit", "curves", "twirl"],
    minutes=[180, 270], costUSD=[20, 45], machineRequired=True, popularity=88, featured=True,
    constants={"sa": 1.5, "bw": 4, "nh": 1, "ew": 3},
    params=[{"id": "waist", "label": "Waist", "default": 72, "min": 56, "max": 110, "step": 1}, {"id": "hip", "label": "Hip", "default": 98, "min": 82, "max": 132, "step": 1, "help": "The waist opening is cut to fit over your hips."},
            {"id": "L", "label": "Skirt length", "default": 55, "min": 35, "max": 85, "step": 1, "help": "Waist to hem, including the 4 cm band."}],
    sizes=[{"id": "xs", "label": "XS", "values": {"waist": 62, "hip": 88, "L": 52}}, {"id": "s", "label": "S", "values": {"waist": 66, "hip": 92, "L": 54}}, {"id": "m", "label": "M", "values": {"waist": 72, "hip": 98, "L": 55}},
           {"id": "l", "label": "L", "values": {"waist": 80, "hip": 106, "L": 56}}, {"id": "xl", "label": "XL", "values": {"waist": 88, "hip": 114, "L": 57}}],
    customNote="Geometry, not scaling: waist radius r = (hip + 4 cm) ÷ 2π, so the waist edge is long enough to pull over your hips; the outer radius is r + length − band + hem. Each quarter is cut with 1.5 cm side seam allowances. The cutting layout packs each quarter's bounding square — nesting the quarters can save fabric on wide bolts.",
    finished={"label": "Finished skirt", "dims": [{"label": "Length", "value": "L"}, {"label": "Hem circumference", "value": f"6.2832*{RO} - 6.2832*nh"}, {"label": "Elastic", "value": "waist*0.9"}]},
    tools=["machine", "tape", "scissors", "ruler", "marker", "pins", "iron", "safety-pin", "seam-gauge?"],
    materials=[fabric("main", "Drapey woven fabric", "#C26A4E", "Skirt and waistband.", ["Rayon challis", "Cotton lawn", "Crepe", "Linen (light)"], 150, "single", [140, 150], weight="Light, drapey", minw=140),
               notion("elastic", "Woven elastic, 3 cm", "{waist*0.9 + 2}", "Waistband.", "#F1ECE4"), "thread"],
    pieces=[piece("quarter", "Quarter circle", "main", 4, f"sa + {RO}", f"sa + {RO}", "#C26A4E", sa="sa", markings=["Waist edge radius {(hip + 4)/6.2832 - sa}; outer radius {(hip + 4)/6.2832 + L - bw + nh}"]),
            piece("band", "Waistband", "main", 1, "hip + 4 + 2*sa", "2*bw + 2*sa", "#A85A40", grain="any")],
    steps=[
        step("cs1", "prep", "Measure waist, hip and length", "Measure your waist, the fullest part of your hips and the length from waist to hem. Enter them in Customise.", T("measure", lines="waist,hip"), meas=[M("Waist", "waist"), M("Hip", "hip"), M("Length", "L")]),
        step("cs2", "prep", "Pre-wash", "Pre-wash and press. Rayon can shrink and twist; wash it the way you'll wash the skirt.", T("press", tones=["main"]), tech=["prewash"]),
        step("cs3", "cut", "Print and cut four quarters + band", "Print the quarter-circle pattern (it's large — many pages). Cut four quarters with the straight edges on the grain as shown, plus the waistband.", L("main"), pieces=["quarter", "band"],
             beginner="If you'd rather not print, pin a tape measure at the corner and swing it like a compass to mark both curves: the inner radius and the outer radius are listed in the cutting table."),
        step("cs4", "sew", "Staystitch the waist edges", "Staystitch 1.2 cm from the curved waist edge of every quarter. The waist curve is partly on the bias and stretches easily.", T("edgestitch", tone="main", dist=12, label="staystitch the waist curve"), meas=[M("Staystitch from edge", 1.2)], pieces=["quarter"], tech=["staystitching"]),
        step("cs5", "sew", "Sew the four side seams", "Sew the quarters together along their straight edges with 1.5 cm seams, forming a full circle. Neaten and press open.", T("sew", tone="main", sides="l", sa=1.5, label="straight edges together"), meas=[M("Seam allowance", "sa")], pieces=["quarter"], tech=["seam-allowance", "finishing-edges"]),
        step("cs6", "sew", "Make the waistband", "Sew the band's short ends together into a loop, leaving a 4 cm gap in the seam for the elastic (backstitch either side). Press the band in half lengthwise, wrong sides together.", T("fold", tone="band", label="band loop pressed in half", dim="bw"), meas=[M("Finished band", "bw")], pieces=["band"], tech=["pressing"]),
        step("cs7", "assemble", "Attach the waistband", "Pin the band's raw edges to the skirt waist, right sides together, matching the band seam to a side seam. Sew with 1.5 cm, neaten and press up.", T("binding", tone="main", bind="band"), meas=[M("Seam allowance", "sa")], pieces=["band", "quarter"]),
        step("cs8", "assemble", "Insert the elastic", "Cut the elastic, thread it through the band via the gap, overlap the ends 2 cm and zigzag. Close the gap.", T("elastic", overlap=2), meas=[M("Elastic length", "waist*0.9 + 2")], tech=["elastic-waistband"]),
        step("cs9", "finish", "Hang overnight, then level the hem", "Hang the skirt for 24 hours — the bias sections drop and lengthen. Put it on (or on a dress form) and have a helper mark an even hem with a ruler from the floor. Trim along the marks.", T("measure", lines="hip"),
             beginner="Skipping this gives a wavy hem that's longer at the sides. It's the one step you can't rush.", tips=["Use a yardstick standing on the floor and pin at the same height all round."]),
        step("cs10", "finish", "Narrow hem", "Press a narrow double hem — 0.5 cm, then 0.5 cm — easing the fullness, and stitch.", T("hem", tone="main", f1=0.5, f2=0.5), meas=[M("Each fold", 0.5)], pieces=["quarter"], tech=["hemming", "sewing-curves"]),
        step("cs11", "finish", "Twirl", "Press lightly and enjoy the swish.", G()),
    ],
    gallery=[{"label": "Circle skirt", "scene": scene(
        {"k": "panel", "x": 160, "y": 40, "w": 80, "h": 22, "tone": "band", "rx": 4},
        {"k": "path", "d": "M 160 62 L 240 62 Q 340 160 370 260 Q 200 290 30 260 Q 60 160 160 62 Z", "tone": "main"},
        *[{"k": "fold", "from": [200 + dx * 0.25, 70], "to": [200 + dx, 268]} for dx in (-110, -40, 40, 110)])}],
    related=["elastic-skirt", "tiered-skirt", "wrap-skirt"],
))
P[-1]["pieces"][0]["outline"] = QUARTER

# ======================================================================== 7 wrap skirt
P.append(project(
    id="wrap-skirt", title="Gathered Wrap Skirt", category="clothing", difficulty="intermediate",
    summary="A soft gathered wrap skirt with long ties that wrap round and pass through a buttonhole.",
    description="One big rectangle gathered onto a long waistband with ties. Adjustable fit, no zipper, and it suits nearly every body. Introduces gathering and a buttonhole.",
    tags=["clothing", "skirt", "gathering", "adjustable", "summer"],
    minutes=[150, 220], costUSD=[15, 35], machineRequired=True, popularity=77,
    constants={"sa": 1.5, "hem": 3, "bw": 4},
    params=[{"id": "waist", "label": "Waist", "default": 72, "min": 56, "max": 100, "step": 1}, {"id": "hip", "label": "Hip", "default": 98, "min": 82, "max": 108, "step": 1, "help": "Up to 108 cm with 140 cm wide fabric."},
            {"id": "L", "label": "Skirt length", "default": 65, "min": 40, "max": 95, "step": 1}],
    sizes=[{"id": "s", "label": "S", "values": {"waist": 66, "hip": 92, "L": 63}}, {"id": "m", "label": "M", "values": {"waist": 72, "hip": 98, "L": 65}}, {"id": "l", "label": "L", "values": {"waist": 80, "hip": 106, "L": 66}}],
    customNote="The skirt panel is 1.25 × hip wide (it wraps a quarter past itself) and gathers into a band 1.5 × waist long, so the overlap sits flat at the front. Ties and hem allowances are fixed.",
    finished={"label": "Finished skirt", "dims": [{"label": "Length", "value": "L"}, {"label": "Width (flat)", "value": "hip*1.25"}, {"label": "Band", "value": "waist*1.5"}]},
    tools=["machine", "tape", "scissors", "ruler", "marker", "pins", "iron", "safety-pin", "seam-ripper"],
    materials=[fabric("main", "Light woven fabric", "#7F9473", "Skirt, band and ties.", ["Cotton lawn", "Rayon", "Double gauze", "Linen (light)"], 140, "single", [140, 150], weight="Light"), "thread"],
    pieces=[piece("panel", "Skirt panel", "main", 1, "hip*1.25 + 4", "L - bw + sa + hem", "#7F9473"),
            piece("band", "Waistband", "main", 1, "2*bw + 2*sa", "waist*1.5 + 2*sa", "#5F7354"),
            piece("ties", "Tie", "main", 2, 8, 80, "#5F7354", sa=0, grain="any")],
    steps=[
        step("ws1", "prep", "Measure", "Measure your waist and hip and choose the length; enter them in Customise.", T("measure", lines="waist,hip"), meas=[M("Waist", "waist"), M("Hip", "hip"), M("Length", "L")]),
        step("ws2", "prep", "Pre-wash", "Pre-wash and press.", T("press", tones=["main"]), tech=["prewash"]),
        step("ws3", "cut", "Cut the pieces", "Cut the panel across the full width, the waistband and two ties.", L("main"), pieces=["panel", "band", "ties"]),
        step("ws4", "sew", "Hem the side edges", "Double-fold hem both short side edges of the panel: 1 cm, then 1 cm.", T("hem", tone="main", f1=1, f2=1), meas=[M("Each fold", 1)], pieces=["panel"], tech=["hemming"]),
        step("ws5", "sew", "Gather the top edge", "Sew two rows of long basting stitches along the top edge (1 cm and 1.3 cm from the edge). Pull the bobbin threads until the top measures the band length minus 3 cm, and spread the gathers evenly.", T("gather", tone="main"), meas=[M("Gathered length", "waist*1.5 - 3")], pieces=["panel"], tech=["gathering"]),
        step("ws6", "assemble", "Attach the waistband", "Pin the band to the gathered edge right sides together, band extending 1.5 cm at each end. Sew with 1.5 cm. Press the band up, fold in half to the inside, fold the edge under and stitch in the ditch from the front.", T("binding", tone="main", bind="band", width="bw"), meas=[M("Seam allowance", "sa"), M("Finished band", "bw")], pieces=["band", "panel"]),
        step("ws7", "assemble", "Make and attach the ties", "Sew each tie into a tube, turn and press; fold one end in. Insert the raw end into each band end and topstitch across twice.", T("tube", tone="ties"), pieces=["ties"], tech=["edgestitching"]),
        step("ws8", "assemble", "Make the buttonhole", "Wrap the skirt on. Mark where the inner tie meets the band at your side, and sew a 2.5 cm vertical buttonhole there for the tie to pass through.", T("mark", tone="band", label="2.5 cm buttonhole at the side"), meas=[M("Buttonhole length", 2.5)], pieces=["band"], tech=["buttonholes"]),
        step("ws9", "finish", "Hem", "Try on to check the length. Press 1 cm then 2 cm at the hem and stitch.", T("hem", tone="main", f1=1, f2=2), meas=[M("First fold", 1), M("Second fold", 2)], pieces=["panel"], tech=["hemming"]),
        step("ws10", "finish", "Wrap and tie", "Wrap the inner tie through the buttonhole, round your back, and tie at the side.", G()),
    ],
    gallery=[{"label": "Wrap skirt", "scene": scene(
        {"k": "panel", "x": 140, "y": 50, "w": 120, "h": 18, "tone": "band", "rx": 3},
        {"k": "poly", "pts": [[140, 68], [260, 68], [310, 270], [90, 270]], "tone": "main"},
        {"k": "poly", "pts": [[210, 68], [260, 68], [310, 270], [250, 270]], "tone": "main"}, {"k": "fold", "from": [210, 68], "to": [250, 270]},
        {"k": "cord", "pts": [[262, 60], [300, 90], [292, 140]], "color": "ties"}, {"k": "cord", "pts": [[262, 60], [320, 80], [330, 130]], "color": "ties"})}],
    related=["circle-skirt", "elastic-skirt", "tiered-skirt"],
))

# ======================================================================== 8 boxy tee
BW = "(bust + ease)/4"
def tee_outline(nd):
    return (f"M 0 {{{nd}}} C {{nw*0.6}} {{{nd}}} {{nw}} {{{nd}*0.5}} {{nw}} 0 L {{hw}} 0 L {{hw}} {{ah + sa}} "
            f"L {{{BW} + sa + 4}} {{ah + sa}} Q {{{BW} + sa}} {{ah + sa}} {{{BW} + sa}} {{ah + sa + 4}} L {{{BW} + sa}} {{h}} L 0 {{h}} Z")
P.append(project(
    id="boxy-tee", title="Boxy Woven Tee", category="clothing", difficulty="intermediate",
    summary="A relaxed, cropped-sleeve top with grown-on sleeves and a bias-bound neckline.",
    description="Front and back are each one piece cut on the fold, with the short sleeves built in — no setting in sleeves. A drafted scoop neck is finished with bias binding. Sized from your bust measurement with generous ease.",
    tags=["clothing", "top", "custom fit", "curves", "summer", "bias binding"],
    minutes=[150, 240], costUSD=[15, 35], machineRequired=True, popularity=84, featured=True,
    constants={"sa": 1.5, "ease": 20, "sl": 12, "slh": 2, "ah": 22, "nw": 9, "ndf": 9, "ndb": 2.5, "hem": 2.5},
    params=[{"id": "bust", "label": "Bust / chest", "default": 92, "min": 78, "max": 124, "step": 1}, {"id": "L", "label": "Length (shoulder to hem)", "default": 60, "min": 48, "max": 75, "step": 1}],
    sizes=[{"id": "s", "label": "S", "values": {"bust": 86, "L": 58}}, {"id": "m", "label": "M", "values": {"bust": 92, "L": 60}}, {"id": "l", "label": "L", "values": {"bust": 102, "L": 62}}, {"id": "xl", "label": "XL", "values": {"bust": 112, "L": 64}}],
    customNote="Drafted: body width = (bust + 20 cm ease) ÷ 4 per half-panel; a 12 cm grown-on sleeve with a 22 cm armhole depth and a curved underarm. Neckline is 18 cm wide, 9 cm deep at the front and 2.5 cm at the back at every size; seam allowances 1.5 cm, hem 2.5 cm.",
    finished={"label": "Finished top", "dims": [{"label": "Chest", "value": "bust + ease"}, {"label": "Length", "value": "L"}, {"label": "Sleeve opening", "value": "2*ah"}]},
    tools=["machine", "tape", "scissors", "ruler", "marker", "pins", "iron", "seam-gauge?"],
    materials=[fabric("main", "Light–medium woven", "#D9A35F", "Body and binding.", ["Cotton lawn", "Linen", "Double gauze", "Chambray"], 140, "folded", [140, 150], weight="Light–medium", minw=140), "thread"],
    pieces=[piece("front", "Front", "main", 1, f"2*({BW} + sa + sl + slh)", "L + sa + hem", "#D9A35F", fold=True),
            piece("back", "Back", "main", 1, f"2*({BW} + sa + sl + slh)", "L + sa + hem", "#C08A4A", fold=True),
            piece("bias", "Bias binding strip", "main", 1, 4, 70, "#A8783D", sa=0, grain="any", notes="Cut on the bias (45°) so it curves smoothly round the neck.")],
    steps=[
        step("bt1", "prep", "Measure your bust", "Measure round the fullest part of your bust/chest and choose the length from the top of your shoulder. Enter them in Customise.", T("measure", lines="bust"), meas=[M("Bust", "bust"), M("Length", "L")]),
        step("bt2", "prep", "Pre-wash", "Pre-wash and press.", T("press", tones=["main"]), tech=["prewash"]),
        step("bt3", "cut", "Print and cut on the fold", "Print the front and back half-patterns. Fold the fabric selvedge to selvedge and place each pattern's fold edge exactly on the fold. Cut the bias strip at 45° from the remaining fabric.", L("main"), pieces=["front", "back", "bias"],
             beginner="The front neckline is deeper than the back — check the labels on the printed pieces before cutting."),
        step("bt4", "sew", "Staystitch the neckline", "Staystitch 1 cm from the neckline edges of front and back to stop the curves stretching.", T("edgestitch", tone="main", dist=10, label="staystitch the neck curves"), meas=[M("From edge", 1)], pieces=["front", "back"], tech=["staystitching"]),
        step("bt5", "sew", "Sew the shoulder seams", "Place front on back, right sides together. Sew the shoulder/sleeve-top seams with 1.5 cm, neaten and press towards the back.", T("sew", tone="main", sides="t", sa=1.5, label="shoulder + sleeve top"), meas=[M("Seam allowance", "sa")], pieces=["front", "back"], tech=["finishing-edges"]),
        step("bt6", "sew", "Bind the neckline", "Press the bias strip in half lengthwise. Sew its raw edges to the right side of the neckline with 1 cm, overlapping the ends at a shoulder. Trim, clip the curve, flip the binding to the inside and topstitch 7 mm from the edge.", T("binding", tone="main", bind="bias", width=1), meas=[M("Binding seam", 1), M("Topstitch", 0.7)], pieces=["bias"], tech=["binding", "sewing-curves"]),
        step("bt7", "sew", "Sew the side and underarm seams", "Right sides together, sew from the sleeve hem, round the curved underarm and down the side in one seam. Clip into the underarm curve, neaten and press.", T("sew", tone="main", sides="lb", sa=1.5, label="sleeve → underarm curve → side"), meas=[M("Seam allowance", "sa")], pieces=["front", "back"], tech=["sewing-curves", "clipping-corners"]),
        step("bt8", "finish", "Hem the sleeves", "Press 0.5 cm then 1.5 cm at the sleeve edges and stitch.", T("hem", tone="main", f1=0.5, f2=1.5), meas=[M("First fold", 0.5), M("Second fold", 1.5)], pieces=["front"], tech=["hemming"]),
        step("bt9", "finish", "Hem the body", "Press 1 cm then 1.5 cm at the hem and stitch.", T("hem", tone="main", f1=1, f2=1.5), meas=[M("First fold", 1), M("Second fold", 1.5)], pieces=["back"], tech=["hemming"]),
        step("bt10", "finish", "Press", "Give it a final press.", G()),
    ],
    gallery=[{"label": "Tee", "scene": scene(
        {"k": "path", "d": "M 165 40 Q 200 70 235 40 L 350 60 L 350 140 L 285 140 L 285 270 L 115 270 L 115 140 L 50 140 L 50 60 Z", "tone": "main"},
        {"k": "stitch", "pts": [[165, 46], [182, 58], [200, 62], [218, 58], [235, 46]]})}],
    related=["kimono-jacket", "tunic-dress"],
))
P[-1]["pieces"][0]["outline"] = tee_outline("ndf")
P[-1]["pieces"][1]["outline"] = tee_outline("ndb")

# ======================================================================== 9 tunic dress
P.append(project(
    id="tunic-dress", title="Easy Rectangle Tunic Dress", category="clothing", difficulty="beginner",
    summary="A loose boat-neck dress from two rectangles, with a tie belt.",
    description="Possibly the simplest dress there is: two rectangles joined at the shoulders (leaving the neck open) and the sides (leaving the armholes open). Wear it loose or belted. Choose a fabric with drape.",
    tags=["clothing", "dress", "beginner", "rectangles", "summer"],
    minutes=[120, 180], costUSD=[15, 35], machineRequired=True, popularity=78,
    constants={"sa": 1.5, "ease": 30, "hem": 3, "nk": 26, "arm": 22},
    params=[{"id": "bust", "label": "Bust", "default": 92, "min": 78, "max": 126, "step": 1}, {"id": "L", "label": "Length (shoulder to hem)", "default": 95, "min": 70, "max": 120, "step": 1}],
    sizes=[{"id": "s", "label": "S", "values": {"bust": 86, "L": 92}}, {"id": "m", "label": "M", "values": {"bust": 92, "L": 95}}, {"id": "l", "label": "L", "values": {"bust": 102, "L": 97}}, {"id": "xl", "label": "XL", "values": {"bust": 112, "L": 99}}],
    customNote="Each panel is (bust + 30 cm ease) ÷ 2 wide plus seam allowances; the neck opening (26 cm) and armhole openings (22 cm) stay fixed so they fit any size.",
    finished={"label": "Finished dress", "dims": [{"label": "Circumference", "value": "bust + ease"}, {"label": "Length", "value": "L"}, {"label": "Neck opening", "value": "nk"}]},
    tools=["machine", "tape", "scissors", "ruler", "marker", "pins", "iron"],
    materials=[fabric("main", "Drapey woven", "#8C6E9C", "Dress and belt.", ["Rayon challis", "Linen", "Cotton voile", "Double gauze"], 140, "single", [140, 150], weight="Light–medium"), "thread"],
    pieces=[piece("panel", "Front / back panel", "main", 2, "(bust + ease)/2 + 2*sa", "L + sa + hem", "#8C6E9C"),
            piece("belt", "Belt", "main", 2, 8, 75, "#6F5680", sa=0, grain="any", notes="Joined end to end.")],
    steps=[
        step("td1", "prep", "Measure", "Measure your bust and the length from the top of your shoulder; enter them in Customise.", T("measure", lines="bust"), meas=[M("Bust", "bust"), M("Length", "L")]),
        step("td2", "prep", "Pre-wash", "Pre-wash and press.", T("press", tones=["main"]), tech=["prewash"]),
        step("td3", "cut", "Cut the panels and belt", "Cut two identical panels and two belt strips.", L("main"), pieces=["panel", "belt"]),
        step("td4", "sew", "Neaten the edges", "Zigzag or overlock the shoulder and side edges of both panels.", T("edgestitch", tone="main", dist=3, label="neaten shoulder & side edges"), pieces=["panel"], tech=["finishing-edges", "zigzag-stitch"]),
        step("td5", "sew", "Sew the shoulders, leaving the neck open", "Place the panels right sides together. Sew each shoulder from the outer edge inwards, stopping so the centre 26 cm stays open. Backstitch well.", T("sew", tone="main", sides="t", gap="t", gapLabel="26 cm neck opening", sa=1.5), meas=[M("Neck opening", "nk"), M("Seam allowance", "sa")], pieces=["panel"]),
        step("td6", "sew", "Finish the neckline", "Press the shoulder seams open and continue pressing the seam allowance under along the neck opening. Topstitch round the neck 1 cm from the edge.", T("topstitch", tone="main", dist=1, all=False), meas=[M("Topstitch", 1)], pieces=["panel"], tech=["topstitching"]),
        step("td7", "sew", "Sew the sides, leaving armholes", "Sew each side seam from the hem up, stopping 22 cm below the shoulder for the armhole. Press open, including the allowance along the armhole, and topstitch round each armhole.", T("sew", tone="main", sides="lr", sa=1.5, label="stop 22 cm below the shoulder"), meas=[M("Armhole opening", "arm")], pieces=["panel"], tech=["topstitching"]),
        step("td8", "finish", "Hem", "Try on, adjust the length if needed, then press 1 cm and 2 cm and stitch the hem.", T("hem", tone="main", f1=1, f2=2), meas=[M("First fold", 1), M("Second fold", 2)], pieces=["panel"], tech=["hemming"]),
        step("td9", "finish", "Make the belt", "Join the belt strips end to end, fold into a tube, sew, turn and press; fold the ends in and edgestitch all round.", T("tube", tone="belt"), pieces=["belt"], tech=["edgestitching"]),
        step("td10", "finish", "Wear it", "Wear it loose or belted.", G()),
    ],
    gallery=[{"label": "Dress", "scene": scene(
        {"k": "poly", "pts": [[110, 30], [290, 30], [300, 280], [100, 280]], "tone": "main"}, {"k": "fold", "from": [165, 30], "to": [235, 30]},
        {"k": "panel", "x": 104, "y": 130, "w": 192, "h": 12, "tone": "belt", "rx": 4}, {"k": "cord", "pts": [[200, 140], [190, 190], [180, 210]], "color": "belt"})}],
    related=["boxy-tee", "kimono-jacket"],
))

# ======================================================================== 10 tiered skirt
P.append(project(
    id="tiered-skirt", title="Tiered Maxi Skirt", category="clothing", difficulty="intermediate",
    summary="A floaty three-tier skirt with an elastic waist — each tier 1.5 × fuller than the last.",
    description="Gathering is the whole technique here — and you'll do a lot of it. Three tiers of rectangles, each gathered onto the one above, give a swishy boho maxi skirt that fits with a simple elastic casing.",
    tags=["clothing", "skirt", "gathering", "maxi", "summer"],
    minutes=[210, 300], costUSD=[25, 50], machineRequired=True, popularity=76,
    constants={"sa": 1.5, "ew": 3, "hemA": 2, "fr": 1.5},
    params=[{"id": "waist", "label": "Waist", "default": 72, "min": 56, "max": 110, "step": 1}, {"id": "hip", "label": "Hip", "default": 98, "min": 82, "max": 132, "step": 1}, {"id": "L", "label": "Skirt length", "default": 85, "min": 60, "max": 100, "step": 1}],
    sizes=[{"id": "s", "label": "S", "values": {"waist": 66, "hip": 92, "L": 84}}, {"id": "m", "label": "M", "values": {"waist": 72, "hip": 98, "L": 85}}, {"id": "l", "label": "L", "values": {"waist": 80, "hip": 106, "L": 86}}, {"id": "xl", "label": "XL", "values": {"waist": 88, "hip": 114, "L": 87}}],
    customNote="Tier 1 is hip + 20 cm around (it must pull on); tier 2 is 1.5 × that and tier 3 is 1.5 × tier 2, split across 2, 3 and 4 panels. Tier heights are 30%, 33% and 37% of your length plus casing, seam and hem allowances.",
    finished={"label": "Finished skirt", "dims": [{"label": "Length", "value": "L"}, {"label": "Hem circumference", "value": "(hip + 20)*fr*fr"}, {"label": "Elastic", "value": "waist*0.9"}]},
    tools=["machine", "tape", "scissors", "rotary?", "ruler", "marker", "pins", "iron", "safety-pin"],
    materials=[fabric("main", "Light woven fabric", "#B5727D", "All tiers.", ["Cotton voile", "Rayon challis", "Double gauze", "Cotton lawn"], 140, "single", [140, 150], weight="Light"),
               notion("elastic", "Woven elastic, 3 cm", "{waist*0.9 + 2}", "Waist.", "#F1ECE4"), "thread"],
    pieces=[piece("t1", "Tier 1 (top)", "main", 2, "(hip + 20)/2 + 2*sa", "0.3*L + ew + 2 + sa", "#B5727D"),
            piece("t2", "Tier 2", "main", 3, "(hip + 20)*fr/3 + 2*sa", "0.33*L + 2*sa", "#A0606A"),
            piece("t3", "Tier 3 (hem)", "main", 4, "(hip + 20)*fr*fr/4 + 2*sa", "0.37*L + sa + hemA", "#8C4E59")],
    steps=[
        step("ts1", "prep", "Measure", "Measure waist and hip and choose the length; enter them in Customise.", T("measure", lines="waist,hip"), meas=[M("Waist", "waist"), M("Hip", "hip"), M("Length", "L")]),
        step("ts2", "prep", "Pre-wash", "Pre-wash and press.", T("press", tones=["main"]), tech=["prewash"]),
        step("ts3", "cut", "Cut all the tiers", "Cut the panels for all three tiers across the fabric. Label each pile — they look alike.", L("main"), pieces=["t1", "t2", "t3"], tips=["A rotary cutter and long ruler make these long straight cuts much faster."]),
        step("ts4", "sew", "Join each tier into a ring", "Sew the panels of each tier together at their short edges into three rings (French seams look lovely here). Press.", T("sew", tone="main", sides="lr", sa=1.5, label="panels → rings"), meas=[M("Seam allowance", "sa")], pieces=["t1", "t2", "t3"], tech=["french-seam"]),
        step("ts5", "sew", "Gather tier 2", "Sew two rows of long basting stitches along the top of tier 2. Divide both tier 2 and tier 1's bottom edge into quarters and mark.", T("gather", tone="t2"), pieces=["t2"], tech=["gathering"]),
        step("ts6", "assemble", "Attach tier 2 to tier 1", "Right sides together, pin tier 2 to tier 1 matching the quarter marks; pull up the gathers to fit, spread them evenly and sew with 1.5 cm. Neaten and press the seam up.", T("layer", base="t1", top="t2", label="match quarters, pull gathers to fit"), meas=[M("Seam allowance", "sa")], pieces=["t1", "t2"], tech=["gathering"]),
        step("ts7", "assemble", "Gather and attach tier 3", "Repeat: gather the top of tier 3 and sew it to the bottom of tier 2.", T("gather", tone="t3"), pieces=["t3", "t2"], tech=["gathering"]),
        step("ts8", "assemble", "Make the casing", "At the top of tier 1, press 1 cm, then 4 cm. Stitch close to the lower fold, leaving a 5 cm gap.", T("casing", tone="t1", depth="ew + 1", insert="elastic", gap=True), meas=[M("Casing depth", "ew + 1")], pieces=["t1"], tech=["casing"]),
        step("ts9", "assemble", "Insert the elastic", "Thread the elastic, overlap 2 cm and zigzag, then close the casing.", T("elastic", overlap=2), meas=[M("Elastic length", "waist*0.9 + 2")], tech=["elastic-waistband"]),
        step("ts10", "finish", "Hem", "Press 0.5 cm, then 1.5 cm, at the hem and stitch.", T("hem", tone="t3", f1=0.5, f2=1.5), meas=[M("First fold", 0.5), M("Second fold", 1.5)], pieces=["t3"], tech=["hemming"]),
        step("ts11", "finish", "Press", "Steam the tiers lightly — don't flatten the gathers.", G()),
    ],
    gallery=[{"label": "Tiered skirt", "scene": scene(
        {"k": "poly", "pts": [[160, 30], [240, 30], [250, 100], [150, 100]], "tone": "t1"},
        {"k": "poly", "pts": [[150, 100], [250, 100], [275, 180], [125, 180]], "tone": "t2"},
        {"k": "poly", "pts": [[125, 180], [275, 180], [315, 280], [85, 280]], "tone": "t3"},
        {"k": "stitch", "pts": [[160, 40], [240, 40]]})}],
    related=["elastic-skirt", "circle-skirt", "wrap-skirt"],
))

# ======================================================================== 11 kids cape
CAPE = "M {(w - 26)/2} 0 L {(w + 26)/2} 0 L {w} {h - 6} Q {hw} {h} 0 {h - 6} Z"
P.append(project(
    id="kids-cape", title="Kids' Hero Cape", category="kids", difficulty="beginner",
    summary="A lined dress-up cape with a breakaway hook-and-loop neck band.",
    description="A flared, curved-hem cape in any size from toddler to tween. It's lined so it swishes nicely, and the neck closes with hook-and-loop tape that pulls apart safely — never ties.",
    tags=["kids", "clothing", "gifts", "costume", "dress-up", "curves"],
    minutes=[75, 120], costUSD=[8, 18], machineRequired=True, popularity=80,
    constants={"sa": 1},
    params=[{"id": "L", "label": "Cape length", "default": 55, "min": 35, "max": 80, "step": 1, "help": "Back of neck to where the cape should end."}],
    sizes=[{"id": "2-4", "label": "Age 2–4", "values": {"L": 40}}, {"id": "5-7", "label": "Age 5–7", "values": {"L": 55}}, {"id": "8-10", "label": "Age 8–10", "values": {"L": 68}}],
    customNote="The cape flares from a fixed 26 cm neck edge to 1.2 × its length at the hem, with a gently curved hem. The neck band and closure stay the same at every size.",
    finished={"label": "Finished cape", "dims": [{"label": "Length", "value": "L"}, {"label": "Hem width", "value": "L*1.2"}]},
    tools=["machine", "scissors", "ruler", "marker", "pins", "iron", "point-turner?"],
    materials=[
        fabric("main", "Outer — satin or cotton", "#C0583A", "Outside.", ["Poly satin", "Quilting cotton", "Felt"], 112, "single", [112, 140]),
        fabric("lining", "Lining — contrast cotton", "#D9A35F", "Inside and neck band.", ["Quilting cotton"], 112, "single", [112, 140]),
        notion("velcro", "Hook-and-loop tape, 2.5 cm", "5 cm", "Breakaway closure.", "#E8E0D2"), "thread"],
    pieces=[piece("outer", "Cape outer", "main", 1, "L*1.2 + 2*sa", "L + 2*sa", "#C0583A"),
            piece("liningp", "Cape lining", "lining", 1, "L*1.2 + 2*sa", "L + 2*sa", "#D9A35F"),
            piece("band", "Neck band", "lining", 1, 60, 10, "#B88A4A", sa=0, grain="any", notes="Encloses the neck edge; the ends overlap with hook-and-loop.")],
    steps=[
        step("kc1", "prep", "Press", "Press both fabrics (satin on a low setting).", T("press", tones=["main", "lining"]), warn=["Satin is usually polyester — use a cool iron."]),
        step("kc2", "cut", "Print and cut the outer", "Print the cape pattern at 100% for your size and cut one outer.", L("main"), pieces=["outer"]),
        step("kc3", "cut", "Cut the lining and band", "Cut one lining and the neck band.", L("lining"), pieces=["liningp", "band"]),
        step("kc4", "sew", "Optional: add an emblem", "Appliqué a felt initial or star on the outer back with a zigzag stitch before assembling.", T("patch", base="main", patch="#D9A35F", label="emblem"), pieces=["outer"], tech=["zigzag-stitch"]),
        step("kc5", "sew", "Sew outer to lining", "Place outer and lining right sides together. Sew both sides and the curved hem with 1 cm, leaving the neck edge open.", T("sew", tone="main", sides="lbr", label="sides + curved hem, neck open"), meas=[M("Seam allowance", "sa")], pieces=["outer", "liningp"], tech=["sewing-curves"]),
        step("kc6", "sew", "Clip, turn and press", "Clip the hem curve and the corners, turn right side out through the neck and press.", T("turn", tone="main", label="turn through the neck edge"), tech=["clipping-corners", "sewing-curves"]),
        step("kc7", "sew", "Topstitch", "Topstitch 5 mm round the sides and hem.", T("topstitch", tone="main", dist=0.5), meas=[M("Topstitch", 0.5)], pieces=["outer"], tech=["topstitching"]),
        step("kc8", "assemble", "Bind the neck edge", "Press the band in half lengthwise and press the long edges in 1 cm. Centre the cape's neck edge inside the band (17 cm of band extends each side), pin and edgestitch the band closed along its whole length.", T("binding", tone="main", bind="band", width=2.5), meas=[M("Band extends each side", 17)], pieces=["band"], tech=["binding", "edgestitching"]),
        step("kc9", "finish", "Add the breakaway closure", "Sew the hook side of the tape to the inside of one band end and the loop side to the outside of the other. Stitch a box round each piece.", T("mark", tone="band", label="hook inside · loop outside"),
             warn=["Never replace the hook-and-loop with ties or cords: a closure that pulls apart is safer for children's play."]),
        step("kc10", "finish", "Up, up and away", "Fasten it on and let them fly.", G()),
    ],
    gallery=[{"label": "Cape", "scene": scene({"k": "path", "d": "M 165 30 L 235 30 L 350 250 Q 200 290 50 250 Z", "tone": "main"}, {"k": "panel", "x": 120, "y": 22, "w": 160, "h": 16, "tone": "band", "rx": 6})}],
    related=["bean-bags", "crayon-roll"],
))
P[-1]["pieces"][0]["outline"] = CAPE
P[-1]["pieces"][1]["outline"] = CAPE

ALTS = {
    "kb2": "The knot bag pattern piece: a rounded body with a short handle on the left and a long handle on the right, 34 cm wide.",
    "kb5": "Two outer pieces right sides together, stitched down both sides and across the bottom, stopping at the side notches.",
    "kb6": "The lining pieces stitched the same way with a 10 cm gap left in the bottom seam.",
    "kb8": "Stitching following the inner curve between the handles and both edges of each handle, with the handle ends left open.",
    "kb11": "Outer handle ends sewn right sides together beside lining handle ends sewn right sides together.",
    "bk9": "A circular base pinned into the bottom of the tube at four quarter marks and stitched round.",
    "cb11": "A webbing strap threaded through a D-ring, a slider in the middle, and a second D-ring.",
}
for p in P:
    for st in p["steps"]:
        if st["id"] in ALTS: st["alt"] = ALTS[st["id"]]

for i, p in enumerate(P, start=23):
    with open(os.path.join(ROOT, "projects", f"{i:02d}-{p['id']}.json"), "w") as f:
        json.dump(clean(p), f, indent=1, ensure_ascii=False)
print(len(P), "projects")
