"""Original vector ornaments for Surviving the Singularity.

Run with Python 3 from any directory. No third-party dependencies.
The drawings are authored geometry, not traced or generated from source images.
"""

from pathlib import Path
from xml.sax.saxutils import escape
import json
import xml.etree.ElementTree as ET

DEST = Path(__file__).resolve().parent
INK = "#202c28"
OLIVE = "#66764e"
STROKE = 4.2
DRAWINGS = []


def path(d, color=INK, width=STROKE):
    return f'<path d="{d}" stroke="{color}" stroke-width="{width}"/>'


def circle(x, y, r, color=INK, fill="none"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{color}" fill="{fill}"/>'


def ellipse(x, y, rx, ry, color=INK):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" stroke="{color}"/>'


def line(x1, y1, x2, y2, color=INK):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>'


def add(name, title, description, shapes):
    DRAWINGS.append((name, title, description, "\n".join(shapes)))


# Wheat is presented to an articulated, open gripper. Its fingers are open,
# giving the mechanical silhouette a receptive rather than crushing gesture.
add("01-grain-and-gripper", "Grain and an open gripper",
    "A curved ear of grain meets the open fingers of an articulated machine.", [
    path("M135 219C142 189 154 151 171 105C177 86 181 63 179 42", OLIVE),
    path("M178 62C164 61 155 53 154 40C170 41 178 49 178 62Z", OLIVE),
    path("M178 73C192 67 199 57 195 44C182 49 176 60 178 73Z", OLIVE),
    path("M174 91C159 90 149 82 148 68C163 70 173 79 174 91Z", OLIVE),
    path("M170 104C187 100 197 92 197 78C181 80 171 90 170 104Z", OLIVE),
    path("M163 123C148 120 138 111 139 97C154 102 163 111 163 123Z", OLIVE),
    path("M158 137C176 137 188 130 192 116C176 114 162 125 158 137Z", OLIVE),
    path("M179 42L180 31M154 40L145 32M195 44L207 35M148 68L135 59M197 78L211 69M139 97L128 85M192 116L205 109", OLIVE),
    path("M146 183C124 173 115 156 113 142C132 152 143 166 146 183Z", OLIVE),
    path("M148 175C166 170 180 157 188 143C166 148 152 162 148 175Z", OLIVE),
    path("M258 220H322M272 220V199L293 182"),
    circle(295, 168, 14),
    path("M287 155L243 115M305 157L255 105"),
    circle(242, 103, 13),
    path("M230 97L212 89L188 99L184 114M231 110L215 122L191 125L177 116"),
    path("M202 96L211 107L202 120"),
    path("M305 179L310 194V220"),
    circle(295, 168, 3, INK, INK),
    circle(242, 103, 3, INK, INK),
])


add("02-event-horizon", "An uncertain horizon",
    "Curved orbital lines pass around an open circular center; a speculative astronomical metaphor.", [
    circle(204, 128, 49),
    path("M61 150C81 104 143 64 219 54C278 47 321 58 339 83", OLIVE),
    path("M65 166C88 191 142 203 201 194C274 183 324 150 340 116", OLIVE),
    path("M68 151C106 140 130 132 157 122M252 134C281 126 314 112 336 93"),
    path("M71 169C100 157 129 147 158 138M250 116C279 107 307 94 329 79"),
    path("M123 212C99 189 105 134 139 88C170 47 205 29 231 35"),
    path("M175 223C205 228 252 192 280 145C303 105 307 73 294 48"),
    circle(321, 100, 4, OLIVE, OLIVE),
    circle(119, 177, 3, INK, INK),
])


add("03-centrifugal-governor", "A centrifugal governor",
    "Two weighted arms, a sliding collar and a spindle suggest regulation and feedback.", [
    path("M99 221H301M176 218V202H224V218"),
    path("M195 195V57M205 195V57"),
    path("M189 57H211M200 46V36"),
    circle(200, 77, 7),
    path("M193 81L140 142M207 81L260 142"),
    circle(134, 155, 16),
    circle(266, 155, 16),
    path("M147 165L186 192M253 165L214 192"),
    path("M186 184H214V198H186Z"),
    path("M214 190H272L293 179"),
    path("M103 84C126 60 150 49 169 45", OLIVE),
    path("M103 84L111 65M103 84L124 81", OLIVE),
    path("M231 45C252 50 277 62 297 84", OLIVE),
    path("M297 84L294 63M297 84L277 81", OLIVE),
    line(163, 229, 177, 229, OLIVE),
    line(190, 229, 210, 229, OLIVE),
    line(223, 229, 237, 229, OLIVE),
])


add("04-seed-and-root", "A seed becoming a plant",
    "A small seed opens into paired leaves and a branching root system across the ground line.", [
    path("M64 145C102 142 127 147 156 145M237 145C272 142 305 147 338 144"),
    path("M190 142C170 128 178 111 197 110C217 114 223 132 204 145", OLIVE),
    path("M198 128C201 104 197 81 203 52", OLIVE),
    path("M201 96C175 97 153 81 150 61C180 61 198 76 201 96Z", OLIVE),
    path("M202 76C226 81 246 66 253 43C227 43 208 53 202 76Z", OLIVE),
    path("M194 138C194 160 180 175 179 196C178 208 181 219 185 228"),
    path("M191 157C210 163 221 178 225 198C228 211 233 220 241 227"),
    path("M184 177C161 177 149 188 140 207M158 185L146 178M150 194L153 207"),
    path("M182 199C166 202 162 215 155 226M216 177C237 175 252 184 267 200"),
    path("M238 181L246 169M253 190L264 184M225 199L213 213"),
    circle(104, 173, 2.5, OLIVE, OLIVE),
    circle(296, 173, 2.5, OLIVE, OLIVE),
    line(91, 200, 104, 198, OLIVE),
    line(290, 221, 304, 223, OLIVE),
])


add("05-roof-and-joint", "A roof and its joint",
    "Open timber framing emphasizes the roof's supporting joints rather than a finished property.", [
    path("M72 157L200 49L328 157M85 166L200 69L315 166"),
    path("M99 154H301V170H99Z"),
    path("M117 171V222M132 171V222M268 171V222M283 171V222"),
    path("M193 76V150M207 76V150"),
    path("M132 197L166 171M132 183L146 171M268 197L234 171M268 183L254 171"),
    path("M189 155V169M211 155V169"),
    circle(124, 162, 3, INK, INK),
    circle(276, 162, 3, INK, INK),
    path("M94 225H301", OLIVE),
    path("M315 224C322 207 331 194 341 183", OLIVE),
    path("M329 204C316 201 312 192 313 183C324 187 329 195 329 204Z", OLIVE),
    path("M335 194C347 196 355 189 356 178C345 179 338 185 335 194Z", OLIVE),
])


add("06-shared-table", "A shared table",
    "An oval table holds distinct bowls and a small stem, with seats around its open perimeter.", [
    ellipse(200, 130, 112, 41),
    path("M88 130V143C90 165 146 184 200 184C254 184 310 165 312 143V130"),
    path("M120 164L109 219M134 171L126 219M266 171L274 219M280 164L291 219"),
    path("M139 80V61C139 52 166 48 168 58V79", OLIVE),
    path("M231 80V58C233 48 260 52 260 61V80", OLIVE),
    path("M57 140L57 109C57 97 73 94 79 102L79 119", OLIVE),
    path("M343 140V109C343 97 327 94 321 102V119", OLIVE),
    ellipse(146, 129, 20, 8),
    path("M127 131C130 151 162 151 166 131"),
    ellipse(250, 132, 20, 8),
    path("M231 134C233 154 266 154 269 134"),
    ellipse(195, 112, 16, 6),
    path("M181 114C184 128 205 130 210 114"),
    path("M203 151C212 140 215 126 218 109", OLIVE),
    path("M215 127C202 128 195 119 193 112M217 117C230 119 235 110 238 101", OLIVE),
])


add("07-pamphlet-and-thread", "A stitched pamphlet",
    "An open, hand-stitched pamphlet shows its folds and thread, without simulated writing.", [
    path("M73 67C113 62 159 73 200 96C241 73 287 62 327 67L319 190C281 187 243 194 202 217C159 194 121 187 81 190Z"),
    path("M200 97L202 216M73 77L63 82L72 203C119 198 158 207 201 228C244 207 282 198 328 203L337 82L327 77"),
    path("M101 83C131 84 154 91 178 102M100 173C128 173 152 179 179 191"),
    path("M222 103C249 91 273 84 302 83M224 191C251 179 275 173 302 173"),
    circle(200, 117, 3, OLIVE, OLIVE),
    circle(201, 147, 3, OLIVE, OLIVE),
    circle(201, 178, 3, OLIVE, OLIVE),
    path("M200 117C185 126 215 137 201 147C186 157 215 168 201 178C193 188 188 212 173 225C151 242 135 230 149 216C158 207 174 221 160 236", OLIVE),
    path("M249 142C262 132 278 119 287 102M264 128C251 126 248 118 250 111M277 114C287 116 297 110 300 102", OLIVE),
])


add("08-water-pump", "A pump and its water",
    "A hand-operated pump with a curved lever releases water above a small, open ripple.", [
    path("M162 220H267M176 217L181 194H243L250 217"),
    path("M190 192V113M231 192V112M186 112H235V97H186Z"),
    path("M196 96V72H216V94M198 72L280 45C289 42 294 49 292 55L213 86"),
    circle(209, 83, 5),
    path("M190 126H167C145 126 132 135 132 151V157H149V150C149 145 155 143 164 143H190"),
    path("M185 193H237M194 182H227"),
    path("M137 173C130 183 130 188 138 188C146 187 144 181 137 173Z", OLIVE),
    path("M133 207C106 207 94 213 110 218M148 210C168 215 155 226 125 226M112 205C77 212 87 231 137 232", OLIVE),
    path("M272 218C280 198 289 184 304 171", OLIVE),
    path("M284 196C273 192 268 183 270 174C283 179 286 189 284 196Z", OLIVE),
    path("M292 186C307 188 319 180 321 167C307 169 297 176 292 186Z", OLIVE),
])


add("09-repair-tools", "Repair tools and a loose washer",
    "An open-ended wrench, a screwdriver and a loose washer make a small working still life.", [
    path("M128 215C121 222 109 215 114 206L217 101C204 84 211 63 230 57L221 80L235 94L258 86C251 106 232 115 222 111L128 215Z"),
    path("M128 200L205 122"),
    circle(122, 209, 3),
    path("M146 52L161 56L170 73L159 85L142 76L137 62Z"),
    path("M164 79L248 170M155 89L238 178"),
    path("M248 165L273 185C283 195 285 212 277 220C268 229 253 225 244 215L225 190Z"),
    path("M243 187L266 211M252 179L276 203"),
    circle(309, 178, 18),
    circle(309, 178, 7),
    path("M68 168C83 152 90 136 90 117", OLIVE),
    path("M82 149C66 148 61 137 62 127C78 133 83 140 82 149Z", OLIVE),
    path("M89 131C103 132 115 123 118 112C103 113 93 120 89 131Z", OLIVE),
])


add("10-open-gate", "An open garden gate",
    "A garden gate opens toward a curved path; posts and living branches frame the entrance.", [
    path("M90 223V84L102 75L114 84V223M286 223V84L298 75L310 84V223"),
    path("M115 99L213 62V178L115 216M115 112L213 76M115 196L213 158"),
    path("M142 99V184M171 88V173M115 118L212 153"),
    circle(122, 109, 3),
    circle(122, 197, 3),
    path("M202 116V134"),
    path("M48 115H89M48 159H89M311 115H354M311 159H354"),
    path("M187 232C201 207 236 190 257 170C272 156 272 142 260 130", OLIVE),
    path("M233 232C245 214 267 195 278 176", OLIVE),
    path("M73 220C66 204 62 190 61 171M64 190C48 189 44 180 43 172M69 205C81 202 85 193 85 184", OLIVE),
    path("M324 220C331 204 335 190 336 171M333 190C348 187 352 180 353 171", OLIVE),
])


add("11-soil-profile", "Roots and a depth probe",
    "A root system and an unnumbered three-level probe cross an uneven soil section.", [
    path("M58 99C88 94 119 102 146 99M185 99C214 96 238 100 253 99M275 99C304 96 325 101 343 98"),
    path("M59 145C103 137 140 148 174 143M216 144C246 142 297 147 343 142", OLIVE),
    path("M60 193C95 188 131 196 164 192M229 193C269 188 307 196 343 192", OLIVE),
    path("M165 99C162 83 165 63 171 47", OLIVE),
    path("M165 75C146 75 134 64 131 49C151 51 163 60 165 75Z", OLIVE),
    path("M170 57C189 61 203 52 210 38C192 37 177 44 170 57Z", OLIVE),
    path("M165 99C160 124 161 145 177 166C189 182 187 205 181 226"),
    path("M161 122C145 127 130 139 123 157M147 131L135 119M132 145L116 144"),
    path("M166 148C192 146 209 158 221 177M195 150L200 134M212 164L229 161"),
    path("M181 172C158 177 148 191 145 208M158 187L145 183M153 195L161 211"),
    path("M186 199C203 205 212 216 215 230"),
    path("M258 57H275V76H258ZM264 77V224"),
    circle(264, 112, 5),
    circle(264, 159, 5),
    circle(264, 208, 5),
    path("M281 112H294M281 159H294M281 208H294"),
    circle(86, 122, 2.2, OLIVE, OLIVE),
    circle(321, 171, 2.2, OLIVE, OLIVE),
])


add("12-continuity-route", "A route and an alternative",
    "Two routes through contoured ground join the same endpoints; one has a visible break.", [
    path("M45 202C84 218 124 222 162 210C193 200 209 206 237 214C275 225 309 221 352 201", OLIVE),
    path("M49 225C92 237 142 235 177 223M257 231C294 234 326 228 354 213", OLIVE),
    path("M45 113C81 113 106 95 135 63C157 39 184 39 207 58M266 62C296 50 326 58 351 80", OLIVE),
    path("M53 87C86 84 98 67 121 43M281 39C312 35 337 43 354 53", OLIVE),
    circle(84, 176, 9),
    circle(320, 119, 9),
    path("M91 169C124 144 155 150 177 171M211 188C250 193 290 161 315 127"),
    path("M86 167C94 135 116 115 143 100C177 80 211 88 240 109C265 127 287 134 311 122"),
    circle(181, 176, 3, INK, INK),
    circle(203, 186, 3, INK, INK),
    path("M182 222C187 210 195 204 205 201", OLIVE),
    path("M192 210C179 208 176 200 178 192M198 205C210 209 219 201 222 192", OLIVE),
])


def render_svg(name, title, description, shapes, monochrome=False):
    if monochrome:
        shapes = shapes.replace(INK, "#000000").replace(OLIVE, "#000000")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)} Original publication ornament for Surviving the Singularity.</desc>
  <g fill="none" stroke="{('#000000' if monochrome else INK)}" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round">
{shapes}
  </g>
</svg>
'''


def main():
    mono = DEST / "monochrome"
    mono.mkdir(parents=True, exist_ok=True)
    items = []
    for name, title, description, shapes in DRAWINGS:
        for target, is_mono in [(DEST, False), (mono, True)]:
            svg = render_svg(name, title, description, shapes, is_mono)
            ET.fromstring(svg)
            (target / f"{name}.svg").write_text(svg, encoding="utf-8")
        items.append({"file": f"{name}.svg", "title": title, "description": description,
                      "monochrome": f"monochrome/{name}.svg"})
    (DEST / "manifest.json").write_text(json.dumps({
        "title": "Surviving the Singularity: original publication motifs",
        "viewBox": [0, 0, 400, 260], "colors": {"ink": INK, "olive": OLIVE},
        "stroke_svg_units": STROKE, "stroke_at_two_inches_pt": STROKE * 144 / 400,
        "authoring": "Original geometry authored for this publication; no tracing, external fonts or embedded assets.",
        "assets": items,
    }, indent=2) + "\n", encoding="utf-8")
    cards = "\n".join(f'<figure><img src="{a[0]}.svg"><figcaption>{escape(a[1])}</figcaption></figure>' for a in DRAWINGS)
    (DEST / "contact-sheet.html").write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>Original publication motifs</title>
<style>*{box-sizing:border-box}body{margin:0;padding:42px;background:#f5f3eb;color:#202c28;font:14px Georgia,serif}h1{font-size:25px;font-weight:normal;margin:0 0 8px}p{margin:0 0 26px;color:#66764e}main{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 20px}figure{margin:0;padding:14px 14px 20px;background:white;border-bottom:1px solid #deded3}img{display:block;width:100%;height:208px;object-fit:contain}figcaption{text-align:center;font-size:13px;letter-spacing:.03em}@media print{body{background:white}figure{break-inside:avoid}}</style>
<h1>Surviving the Singularity</h1><p>Original botanical and mechanical ornaments · vector masters · September 2026</p><main>'''+cards+'''</main></html>''', encoding="utf-8")
    print(f"Wrote {len(items)} original masters and {len(items)} monochrome variants to {DEST}")


if __name__ == "__main__":
    main()
