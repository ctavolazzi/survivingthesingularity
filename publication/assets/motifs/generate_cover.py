"""Draw original cover artwork from authored vector geometry, without dependencies."""

from pathlib import Path
from math import sin, cos, pi
import xml.etree.ElementTree as ET

DEST = Path(__file__).resolve().parent
INK = "#202c28"
OLIVE = "#66764e"
shapes = []


def path(d, color=INK, width=1.65):
    shapes.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}"/>')


def circle(x, y, radius, width=1.65, color=INK, fill="none"):
    shapes.append(f'<circle cx="{x}" cy="{y}" r="{radius}" stroke="{color}" stroke-width="{width}" fill="{fill}"/>')


def wheat_head(x, y, angle=0, scale=1):
    """An original stylized awned head; the reference point is its lower end."""
    shapes.append(f'<g transform="translate({x} {y}) rotate({angle}) scale({scale})">')
    path("M0 7C1 -14 0 -42 0 -68", OLIVE, 1.55)
    for i in range(6):
        yy = -6 - i * 8.3
        reach = 13.5 - i * 0.65
        for side in (-1, 1):
            offset = 2.8 if side == 1 else 0
            tip_x = side * reach
            tip_y = yy - 13 + offset
            path(f"M0 {yy + offset}Q{side * 12} {yy - 1 + offset} {tip_x} {tip_y}Q{side * 2} {yy - 11 + offset} 0 {yy + offset}Z", OLIVE, 1.1)
            path(f"M{tip_x} {tip_y}L{side * (reach + 7)} {tip_y - 16}", OLIVE, 0.75)
            path(f"M{side * 2} {yy - 2 + offset}L{side * (reach - 3)} {tip_y + 2}", OLIVE, 0.6)
    path("M0 -68L-2 -82M1 -62L5 -78", OLIVE, 0.8)
    shapes.append("</g>")


# The ground is a field in section, not a pot or a display pedestal.
path("M34 266C68 258 95 264 120 260C146 255 158 264 180 260C211 255 245 262 272 259M301 261C317 261 328 265 338 265", OLIVE, 1.65)
path("M39 276C84 268 110 276 137 272M234 274C272 270 303 275 330 276", OLIVE, 0.8)
path("M40 302C74 297 88 297 105 295M236 291C264 286 297 289 326 293M368 297C395 303 418 306 442 306", OLIVE, 0.8)
path("M46 316C76 310 91 310 113 310M215 307C254 301 292 303 322 310M350 315C386 321 414 323 436 321", OLIVE, 0.65)

# Three crop stems have distinct silhouettes and heights. Curved blades remain
# mostly open, leaving the hand-worked feel of botanical pen illustration.
path("M155 262C149 224 163 181 166 139C169 114 164 107 162 97", OLIVE, 1.8)
path("M160 260C171 215 191 183 210 141C214 132 218 123 219 115", OLIVE, 1.6)
path("M153 261C136 224 119 200 115 169C113 158 113 148 109 142", OLIVE, 1.5)
wheat_head(162, 113, -13, 1.02)
wheat_head(217, 135, 13, 0.86)
wheat_head(110, 156, -22, 0.82)

path("M160 193C138 180 128 156 129 143C150 157 158 174 160 193Z", OLIVE, 1.2)
path("M159 190C145 176 136 160 132 151", OLIVE, 0.65)
path("M166 222C189 204 204 184 209 166C187 176 172 196 166 222Z", OLIVE, 1.2)
path("M170 216C188 197 199 181 204 175", OLIVE, 0.65)
path("M142 237C121 229 104 214 96 199C118 205 135 219 142 237Z", OLIVE, 1.1)
path("M137 232L103 205", OLIVE, 0.65)
path("M197 168C211 165 226 153 232 142C215 145 203 155 197 168Z", OLIVE, 1.1)

# Smaller plants establish a crop rather than a single emblematic stalk.
path("M65 262C67 246 73 232 80 222M69 246C57 243 52 237 51 230C65 233 68 238 69 246ZM74 234C84 235 91 229 93 221C83 222 77 226 74 234Z", OLIVE, 1.1)
path("M260 259C262 243 269 229 278 219M265 242C253 240 248 233 248 226C259 229 263 234 265 242ZM271 229C281 231 289 226 293 217C281 218 275 222 271 229Z", OLIVE, 1.1)
path("M224 262C225 252 230 241 235 234M228 248C216 246 214 241 213 236M231 240C240 241 245 237 248 232", OLIVE, 0.9)

# Roots make the living support system as visible as the machine.
path("M156 263C153 277 159 290 150 307C147 312 145 318 146 325", OLIVE, 1.1)
path("M158 272C177 277 182 291 190 301C197 311 202 318 212 323", OLIVE, 0.85)
path("M153 280C139 282 126 289 120 303M134 287L127 278M125 296L115 298M158 294C170 299 178 312 178 323M175 307L186 311", OLIVE, 0.8)
path("M174 282C189 279 199 283 209 291M191 282L198 274M150 308C134 306 126 313 120 320M187 298L194 287M203 315L220 315", OLIVE, 0.7)
path("M66 264C68 279 60 287 56 292M65 276L78 285M261 262C257 276 264 283 268 291M259 274L249 282M263 281L278 286", OLIVE, 0.65)
for x, y, length in [(89,281,4),(104,313,5),(226,284,3),(281,306,4),(307,286,5),(75,307,3),(236,317,4)]:
    path(f"M{x} {y}l{length} -1.5", OLIVE, 0.7)

# The tending arm uses enclosed structural sections, pin joints, a cable and
# open compliant fingers. It is an imaginative tool, not a product drawing.
path("M337 270L349 258H424L438 270V277H337Z", INK, 1.8)
path("M337 270H438M350 277L346 281M425 277L429 281", INK, 0.95)
path("M365 258L373 239H405L415 258M373 239V229M405 240V229", INK, 1.8)
path("M375 246H405M372 251H410", INK, 0.75)
circle(392, 221, 21, 1.8)
circle(392, 221, 13, 0.8)
circle(392, 221, 5, 1.3)
path("M379 205L389 177M407 178L409 209", INK, 1.8)
path("M386 198L393 179M402 197L403 184", INK, 0.75)
circle(400, 156, 23, 1.8)
circle(400, 156, 15, 0.8)
circle(400, 156, 6, 1.3)
for a in (30,150,270):
    circle(round(400+18*cos(a*pi/180),2),round(156+18*sin(a*pi/180),2),1.15,0.75)
path("M378 149L295 107M295 125L378 166", INK, 1.8)
path("M365 148L300 118M370 159L304 132", INK, 0.75)
path("M310 113L301 130", INK, 0.95)
circle(280, 115, 17, 1.8)
circle(280, 115, 10, 0.8)
circle(280, 115, 3.7, 1.2)
path("M268 105L251 102L242 114L248 128L263 127", INK, 1.7)
path("M253 104L251 114L258 124", INK, 0.8)

# Receptive finger arcs surround empty space beside the grain. They do not
# cross, crush or clip the head. Rounded pads soften the machine's gesture.
path("M245 108L232 106L222 115L221 125L225 126L229 117L235 113L244 115", INK, 1.5)
path("M248 124L239 139L225 144L221 141L222 138L234 132L240 121", INK, 1.5)
circle(245,116,2.7,0.8)
path("M393 137C374 115 336 98 307 96C295 95 290 99 289 101", INK, 0.95)
path("M412 178C429 197 424 227 411 237", INK, 0.95)

# Engraving-like hatching is confined to the machine's planes, so the living
# shapes keep a lighter, more irregular rhythm.
for i in range(8):
    x = 343 + i * 11
    path(f"M{x} 273l3 -2", INK, 0.6)
for i in range(7):
    x = 312 + i * 8
    y = 133 + i * 3.5
    path(f"M{x} {y}l3 -5", INK, 0.6)
for x in (353,421):
    circle(x,266,1.8,0.8)

# Fine contextual field lines recede behind the main scene without adding a
# border or a picture-frame silhouette.
path("M33 246C52 242 69 241 87 241M32 235C51 232 68 231 82 231M292 244C310 247 323 252 333 259", OLIVE, 0.65)
path("M302 231C321 237 335 244 344 252M314 220C330 227 342 235 351 244", OLIVE, 0.65)

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="340" viewBox="0 0 480 340" role="img" aria-labelledby="title desc">
<title id="title">A harvest tended</title>
<desc id="desc">Three ripe grain stalks, young plants and branching roots share a cultivated plot with an articulated mechanical arm. Its open fingers reach gently toward the crop. Original conceptual cover artwork.</desc>
<g fill="none" stroke-linecap="round" stroke-linejoin="round">
''' + "\n".join(shapes) + "\n</g>\n</svg>\n"
ET.fromstring(svg)
(DEST / "cover-harvest.svg").write_text(svg)
(DEST / "monochrome" / "cover-harvest.svg").write_text(svg.replace(INK,"#000000").replace(OLIVE,"#000000"))
print("Wrote original 480 × 340 cover artwork and black-only variant.")
