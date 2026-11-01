#!/usr/bin/env python3
"""Genera le sezioni Elementor (Flexbox Container) della homepage LT3.
Output: build/sections/<slug>.json (compatto) + build/page-state.json
"""
import hashlib, json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sections")
os.makedirs(OUT, exist_ok=True)

SITE = "https://siti.propagandaadv.com/wp-content/uploads"
M = {  # media library
    "poster": (f"{SITE}/2026/10/lt3-hero-01-micro.webp", 195),
    "meso": (f"{SITE}/2026/11/lt3-hero-02-meso.webp", 196),
    "macro": (f"{SITE}/2026/11/lt3-hero-03-macro.webp", 197),
    "events": (f"{SITE}/2026/11/lt3-anima-events.webp", 198),
    "comm": (f"{SITE}/2026/11/lt3-anima-communication.webp", 199),
    "sci": (f"{SITE}/2026/11/lt3-anima-scientific.webp", 200),
    "video": (f"{SITE}/2026/11/lt3-hero-scrub.mp4", 201),
    "logo": (f"{SITE}/2026/11/lt3-logo.png", 203),
    "medu": (f"{SITE}/2026/11/member-of-meduspace.png", 204),
}

GREEN, DARK, MIST, WHITE, SAGE, SAGEHV, TEXT2 = (
    "#175632", "#0D2B19", "#F2F6F3", "#FFFFFF", "#A9C7B0", "#8FB39A", "#3E5A4A")
GID = {GREEN: "lt3green", DARK: "lt3dark", MIST: "lt3mist", WHITE: "lt3white",
       SAGE: "lt3sage", SAGEHV: "lt3sagehv", TEXT2: "lt3text2"}

_n = [0]


def rid():
    _n[0] += 1
    return hashlib.md5(f"lt3-{_n[0]}".encode()).hexdigest()[:7]


def px(v):
    return {"unit": "px", "size": v}


def sp(t, r=None, b=None, l=None):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def gap(v):
    return {"unit": "px", "size": v, "column": str(v), "row": str(v)}


def hexa(h, a):
    h = h.lstrip("#")
    return "rgba(%d,%d,%d,%s)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def W(wt, settings):
    return {"id": rid(), "elType": "widget", "widgetType": wt, "settings": settings, "elements": []}


def C(children, inner=True, **s):
    s.setdefault("content_width", "full")
    if "flex_gap" in s:
        s.setdefault("flex_gap_mobile", s["flex_gap"])
    return {"id": rid(), "elType": "container", "isInner": inner, "settings": s, "elements": children}


def col(color):
    return color, {"__globals__": {"_color": f"globals/colors?id={GID[color]}"}} if color in GID else {}


def typo(family="Outfit", weight="400", size=16, tab=None, mob=None, lh=None, ls=None, upper=False, prefix="typography_"):
    s = {prefix + "typography": "custom", prefix + "font_family": family, prefix + "font_weight": weight,
         prefix + "font_size": px(size)}
    if tab and tab != size:
        s[prefix + "font_size_tablet"] = px(tab)
    if mob and mob != size:
        s[prefix + "font_size_mobile"] = px(mob)
    if lh:
        s[prefix + "line_height"] = {"unit": "em", "size": lh}
    if ls is not None:
        s[prefix + "letter_spacing"] = px(ls)
    if upper:
        s[prefix + "text_transform"] = "uppercase"
    return s


def heading(text, size=48, tag="h2", color=DARK, weight="300", tab=None, mob=None, lh=1.08, ls=-1.2,
            upper=False, link=None, align=None, cls=None):
    s = {"title": text, "header_size": tag, "title_color": color,
         "__globals__": {"title_color": f"globals/colors?id={GID[color]}"}}
    s.update(typo("Outfit", weight, size, tab or max(size * 0.8, 14), mob or max(size * 0.62, 14), lh, ls, upper))
    if link:
        s["link"] = {"url": link, "is_external": "", "nofollow": ""}
    if align:
        s["align"] = align
        s["align_mobile"] = align
    if cls:
        s["_css_classes"] = cls
    return W("heading", s)


def label(text, color=GREEN, size=12, link=None, cls=None):
    return heading(text, size, "div", color, "600", size, size, 1.3, 2.5, True, link, None, cls)


def text(html, size=18, color=DARK, mob=None, width=None, weight="400", lh=1.6, cls=None):
    s = {"editor": html, "text_color": color, "__globals__": {"text_color": f"globals/colors?id={GID[color]}"}}
    s.update(typo("Outfit", weight, size, size, mob or max(size - 2, 14), lh))
    if width:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = {"unit": "px", "size": width}
    if cls:
        s["_css_classes"] = cls
    return W("text-editor", s)


def button(txt, link, bg=GREEN, fg=WHITE, border=None, size=14, hv_bg=None, hv_fg=None, pad=(16, 32), cls=None):
    s = {"text": txt, "link": {"url": link, "is_external": "", "nofollow": ""},
         "background_color": bg, "button_text_color": fg,
         "border_radius": {"unit": "px", "top": "999", "right": "999", "bottom": "999", "left": "999", "isLinked": True},
         "text_padding": sp(pad[0], pad[1]), "text_padding_mobile": sp(14, 24),
         "button_background_hover_color": hv_bg or SAGE, "hover_color": hv_fg or DARK}
    s.update(typo("Outfit", "600", size, size, size, 1.2, 0.6))
    if border:
        s.update({"border_border": "solid", "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}, "border_color": border})
    if cls:
        s["_css_classes"] = cls
    return W("button", s)


def link_button(txt, link, color=GREEN, size=13):
    s = {"text": txt, "link": {"url": link, "is_external": "", "nofollow": ""},
         "background_color": "rgba(0,0,0,0)", "button_text_color": color,
         "text_padding": sp(0, 0), "hover_color": SAGEHV}
    s.update(typo("Outfit", "600", size, size, size, 1.2, 2, True))
    s["border_border"] = "solid"
    s["border_width"] = {"unit": "px", "top": "0", "right": "0", "bottom": "1", "left": "0", "isLinked": False}
    s["border_color"] = color
    s["border_radius"] = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
    return W("button", s)


def image(key, alt, width=100, radius=2, link=None):
    url, mid = M[key]
    s = {"image": {"url": url, "id": mid, "alt": alt}, "image_size": "full",
         "width": {"unit": "%", "size": width},
         "image_border_radius": {"unit": "px", "top": str(radius), "right": str(radius), "bottom": str(radius), "left": str(radius), "isLinked": True}}
    if link:
        s["link_to"] = "custom"
        s["link"] = {"url": link, "is_external": "", "nofollow": ""}
    return W("image", s)


def marker(color=GREEN, size=12):
    return C([], content_width="full", width={"unit": "px", "size": size}, min_height={"unit": "px", "size": size},
             background_background="classic", background_color=color,
             flex_direction="row", flex_direction_mobile="row", padding=sp(0), padding_mobile=sp(0))


def root(css_id, children, bg=None, pad=(144, 32), pad_t=(104, 20), boxed=1280, direction="column", gp=64, **extra):
    s = {"css_id": css_id, "content_width": "full", "flex_direction": direction, "flex_direction_mobile": "column",
         "flex_direction_tablet": "column",
         "flex_gap": gap(gp), "flex_gap_mobile": gap(40),
         "padding": sp(pad[0], pad[1]), "padding_tablet": sp(112, 28), "padding_mobile": sp(pad_t[0] // 1.6, pad_t[1])}
    s["_element_id"] = css_id
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
        s["__globals__"] = {"background_color": f"globals/colors?id={GID[bg]}"}
    s.update(extra)
    return {"id": rid(), "elType": "container", "isInner": False, "settings": s, "elements": children}


def boxed(children, width=1280, direction="column", gp=48, align=None, justify=None, **extra):
    s = {"content_width": "boxed", "boxed_width": px(width), "flex_direction": direction,
         "flex_direction_mobile": "column", "flex_direction_tablet": "column" if direction == "row" else direction,
         "flex_gap": gap(gp), "flex_gap_mobile": gap(28), "padding": sp(0), "padding_mobile": sp(0),
         "width": {"unit": "%", "size": 100}}
    if align:
        s["flex_align_items"] = align
    if justify:
        s["flex_justify_content"] = justify
    s.update(extra)
    return {"id": rid(), "elType": "container", "isInner": True, "settings": s, "elements": children}


def write(slug, el):
    with open(os.path.join(OUT, slug + ".json"), "w") as f:
        json.dump(el, f, ensure_ascii=False, separators=(",", ":"))
    return el


# ------------------------------------------------------------------ HEADER
def header():
    nav = C([
        label("Events", WHITE, 12, "#sec-anime", "lt3-nav"),
        label("Communication", WHITE, 12, "#sec-anime", "lt3-nav"),
        label("Scientific", WHITE, 12, "#sec-anime", "lt3-nav"),
        label("Chi siamo", WHITE, 12, "#sec-metodo", "lt3-nav"),
        label("Contatti", WHITE, 12, "#sec-contatti", "lt3-nav"),
    ], flex_direction="row", flex_gap=gap(36), flex_align_items="center",
        hide_tablet="hidden-tablet", hide_mobile="hidden-mobile", padding=sp(0), padding_mobile=sp(0),
        flex_direction_mobile="row", flex_gap_mobile=gap(16))
    logo = image("logo", "LT3", 100, 0, "#sec-hero")
    logo["settings"]["width"] = {"unit": "px", "size": 44}
    logo["settings"]["_element_width"] = "initial"
    s = {"css_id": "sec-header", "_element_id": "sec-header", "css_classes": "lt3-header", "content_width": "full", "flex_direction": "row",
         "flex_direction_mobile": "row", "flex_direction_tablet": "row",
         "flex_justify_content": "space-between", "flex_align_items": "center",
         "flex_gap": gap(24), "flex_gap_mobile": gap(12),
         "padding": sp(18, 40), "padding_tablet": sp(16, 28), "padding_mobile": sp(12, 16),
         "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "-86", "left": "0", "isLinked": False},
         "margin_mobile": {"unit": "px", "top": "0", "right": "0", "bottom": "-72", "left": "0", "isLinked": False},
         "sticky": "top", "sticky_on": ["desktop", "tablet", "mobile"], "sticky_offset": 0,
         "z_index": 100}
    return write("sec-header", {"id": rid(), "elType": "container", "isInner": False, "settings": s,
                                "elements": [logo, nav, button("Parliamone", "#sec-contatti", GREEN, WHITE, SAGE, 13, SAGE, DARK, (12, 26))]})


# ------------------------------------------------------------------ HERO
HERO_JS = r"""
document.addEventListener('DOMContentLoaded',function(){
var root=document.getElementById('sec-hero');if(!root)return;
var hdr=document.querySelector('.lt3-header');
function hs(){if(!hdr)return;hdr.classList.toggle('is-solid',root.getBoundingClientRect().bottom<140)}
addEventListener('scroll',hs,{passive:true});addEventListener('resize',hs);hs();
if(matchMedia('(max-width:1024px),(prefers-reduced-motion:reduce)').matches)return;
var v=root.querySelector('.lt3-vid'),bar=root.querySelector('.lt3-load i'),media=root.querySelector('.lt3-media'),scrim=root.querySelector('.lt3-scrim'),hint=root.querySelector('.lt3-hint');
var caps=[].slice.call(root.querySelectorAll('.lt3-cap'));
var B=[[0,.30],[.33,.60],[.66,.86],[.90,1.01]],MP=[[0,0],[.30,5.4],[.62,12.2],[.88,15.125],[1,15.125]];
var tgt=0,cur=0,dur=0,seeking=false,ready=false,last=0,raf=0,shown=-2;
function clamp(x){return x<0?0:x>1?1:x}
function vt(p){for(var i=1;i<MP.length;i++){if(p<=MP[i][0]){var a=MP[i-1],b=MP[i];return a[1]+(b[1]-a[1])*((p-a[0])/(b[0]-a[0]))}}return MP[MP.length-1][1]}
function prog(){var h=root.offsetHeight-innerHeight*1.4;return h>0?clamp(-root.getBoundingClientRect().top/h):0}
function bands(p){var k=-1;for(var i=0;i<B.length;i++){if(p>=B[i][0]&&p<B[i][1]){k=i;break}}
if(k!==shown){shown=k;caps.forEach(function(c,i){c.classList.toggle('on',i===k)});scrim.style.opacity=k<0?0:(k===3?.75:1)}
hint.style.opacity=p<.02?1:0}
function frame(t){raf=0;var dt=Math.min(.1,((t-last)/1000)||.016);last=t;
tgt=prog();cur+=(tgt-cur)*(1-Math.exp(-dt*9));if(Math.abs(tgt-cur)<.0004)cur=tgt;
bands(tgt);
if(ready&&!seeking){var want=Math.min(vt(cur),dur-.02);if(Math.abs(v.currentTime-want)>.012){seeking=true;v.currentTime=want}}
if(Math.abs(tgt-cur)>.0004||seeking)raf=requestAnimationFrame(frame)}
function kick(){if(!raf){last=performance.now();raf=requestAnimationFrame(frame)}}
addEventListener('scroll',kick,{passive:true});addEventListener('resize',kick);
v.addEventListener('seeked',function(){seeking=false;kick()});
function done(){bar.parentNode.style.opacity=0}
var x=new XMLHttpRequest();x.open('GET','__VIDEO__');x.responseType='blob';
x.onprogress=function(e){if(e.lengthComputable)bar.style.width=(e.loaded/e.total*100)+'%'};
x.onload=function(){if(x.status<200||x.status>=300)return done();v.src=URL.createObjectURL(x.response);
v.addEventListener('loadedmetadata',function(){dur=v.duration;ready=true;media.classList.add('ok');done();kick()},{once:true});v.load()};
x.onerror=done;x.send();
bands(0);kick();
});
"""

HERO_CSS = """
#sec-hero .lt3-stage{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;align-self:flex-start;width:100%}
#sec-hero .lt3-stage>.elementor-widget-html,#sec-hero .lt3-stage>.elementor-widget-html .elementor-widget-container{position:absolute;inset:0;margin:0;z-index:0}
#sec-hero .lt3-media{position:absolute;inset:0;background:#0D2B19 url(__POSTER__) center/cover no-repeat}
#sec-hero .lt3-vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s}
#sec-hero .lt3-media.ok .lt3-vid{opacity:1}
#sec-hero .lt3-scrim{position:absolute;inset:0;opacity:0;transition:opacity .6s;background:linear-gradient(90deg,rgba(13,43,25,.86) 0%,rgba(13,43,25,.6) 34%,rgba(13,43,25,0) 66%),linear-gradient(0deg,rgba(13,43,25,.55) 0%,rgba(13,43,25,0) 40%)}
#sec-hero .lt3-load{position:absolute;left:0;right:0;bottom:0;height:2px;background:rgba(169,199,176,.25);transition:opacity .6s}
#sec-hero .lt3-load i{display:block;height:100%;width:0;background:#A9C7B0}
#sec-hero .lt3-hint{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);font:600 11px/1 Outfit,sans-serif;letter-spacing:.3em;color:#F2F6F3;transition:opacity .4s}
#sec-hero .lt3-cap{position:absolute;left:clamp(24px,6vw,96px);bottom:13vh;max-width:min(560px,40vw);opacity:0;transform:translateY(28px);transition:opacity .7s ease,transform .7s ease;pointer-events:none;z-index:2}
#sec-hero .lt3-cap.on{opacity:1;transform:none;pointer-events:auto}
#sec-hero .lt3-payoff{max-width:min(720px,52vw)}
.lt3-header{transition:background-color .3s,box-shadow .3s}
.lt3-header.is-solid{background-color:#F2F6F3!important;box-shadow:0 1px 0 rgba(23,86,50,.14)}
.lt3-header.is-solid .lt3-nav .elementor-heading-title,.lt3-header.is-solid .lt3-nav a{color:#0D2B19!important}
@media (max-width:1024px),(prefers-reduced-motion:reduce){
#sec-hero{min-height:0!important}
#sec-hero .lt3-stage{position:static;height:auto;overflow:visible;display:flex;flex-direction:column}
#sec-hero .lt3-stage>.elementor-widget-html{display:none}
#sec-hero .lt3-cap,#sec-hero .lt3-payoff{position:relative;left:auto;bottom:auto;max-width:none;width:100%;opacity:1;transform:none;pointer-events:auto;min-height:92svh;justify-content:flex-end;padding:120px 24px 56px;box-sizing:border-box;transition:none}
#sec-hero .lt3-cap-1{background:linear-gradient(180deg,rgba(13,43,25,.35),rgba(13,43,25,.9)),url(__POSTER__) center/cover}
#sec-hero .lt3-cap-2{background:linear-gradient(180deg,rgba(13,43,25,.35),rgba(13,43,25,.9)),url(__MESO__) center/cover}
#sec-hero .lt3-cap-3{background:linear-gradient(180deg,rgba(13,43,25,.35),rgba(13,43,25,.9)),url(__MACRO__) center/cover}
#sec-hero .lt3-payoff{background:#0D2B19;min-height:0;padding:72px 24px 88px}
}
"""


def hero():
    css = (HERO_CSS.replace("__POSTER__", M["poster"][0]).replace("__MESO__", M["meso"][0])
           .replace("__MACRO__", M["macro"][0]))
    js = HERO_JS.replace("__VIDEO__", M["video"][0])
    html = ("<style>" + css + "</style>"
            '<div class="lt3-media"><video class="lt3-vid" muted playsinline preload="auto" aria-hidden="true"></video>'
            '<div class="lt3-scrim"></div><div class="lt3-load" aria-hidden="true"><i></i></div>'
            '<div class="lt3-hint" aria-hidden="true">SCORRI</div></div><script>' + js + "</script>")
    media = W("html", {"html": html})

    def cap(n, lab, body):
        return C([label(lab, SAGE, 12), text(body, 19, WHITE, 17, None, "300", 1.55)],
                 css_classes=f"lt3-cap lt3-cap-{n}", flex_direction="column", flex_gap=gap(18),
                 flex_direction_mobile="column", padding=sp(0), padding_mobile=sp(0))

    caps = [
        cap(1, "01 — La cura nasce nel dettaglio",
            "<p>Ogni decisione terapeutica e ogni gesto clinico richiedono certezze. Non facciamo semplice divulgazione: costruiamo le basi per rendere quel singolo momento di cura più sicuro, efficace e aggiornato.</p>"),
        cap(2, "02 — La conoscenza diventa metodo",
            "<p>Dietro ogni competenza c'è un percorso strutturato. Con il nostro Comitato Scientifico progettiamo esperienze di apprendimento — residenziali, FAD e sul campo — che trasformano le più recenti evidenze della letteratura in protocolli applicabili sul lavoro.</p>"),
        cap(3, "03 — La garanzia istituzionale",
            "<p>Siamo il tassello che collega la pratica clinica al Sistema Sanitario Nazionale. Come Provider accreditato AGENAS, certifichiamo il valore legale dei crediti formativi e rendicontiamo direttamente a Co.Ge.A.P.S., garantendo la piena conformità professionale di chi ogni giorno si prende cura del Paese.</p>"),
    ]
    btns = C([button("Progettiamo il tuo prossimo evento", "#sec-contatti", WHITE, DARK, None, 14, SAGE, DARK),
              button("Scopri il metodo", "#sec-metodo", "rgba(0,0,0,0)", WHITE, SAGE, 14, SAGE, DARK)],
             flex_direction="row", flex_direction_mobile="column", flex_gap=gap(14), flex_wrap="wrap",
             flex_gap_mobile=gap(12), padding=sp(8, 0, 0, 0), padding_mobile=sp(8, 0, 0, 0))
    payoff = C([heading("Dal gesto del singolo alla salute di tutti: siamo il Provider ECM che certifica la qualità di chi cura.",
                        42, "h2", WHITE, "300", 30, 26, 1.12, -1.0), btns],
               css_classes="lt3-cap lt3-payoff", flex_direction="column", flex_gap=gap(28),
               flex_direction_mobile="column", padding=sp(0), padding_mobile=sp(0))
    stage = C([media] + caps + [payoff], css_classes="lt3-stage", flex_direction="column",
              flex_direction_mobile="column", padding=sp(0), padding_mobile=sp(0),
              min_height={"unit": "vh", "size": 100})
    el = {"id": rid(), "elType": "container", "isInner": False, "settings": {
        "css_id": "sec-hero", "_element_id": "sec-hero", "content_width": "full", "flex_direction": "column", "flex_direction_tablet": "column",
        "flex_direction_mobile": "column", "flex_gap": gap(0), "flex_gap_mobile": gap(0),
        "padding": sp(0), "padding_tablet": sp(0), "padding_mobile": sp(0),
        "min_height": {"unit": "vh", "size": 700}, "min_height_tablet": {"unit": "px", "size": 0}, "min_height_mobile": {"unit": "px", "size": 0},
        "background_background": "classic", "background_color": DARK,
        "__globals__": {"background_color": "globals/colors?id=lt3dark"}}, "elements": [stage]}
    return write("sec-hero", el)


# ------------------------------------------------------------------ ANIME
def anime():
    def card(n, name, key, alt, body, offset):
        top = C([marker(GREEN, 10), label(f"{n} — {name}", GREEN, 12)], flex_direction="row", flex_direction_mobile="row",
                flex_align_items="center", flex_gap=gap(12), padding=sp(0), padding_mobile=sp(0))
        return C([image(key, alt), top,
                  heading(name, 44, "h3", DARK, "300", 36, 34, 1.05, -1.0), text(body, 18, TEXT2, 16),
                  link_button("Parliamone", "#sec-contatti")],
                 flex_direction="column", flex_direction_mobile="column", flex_gap=gap(18), flex_gap_mobile=gap(16),
                 width={"unit": "%", "size": 31.5}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
                 padding=sp(offset, 0, 0, 0), padding_tablet=sp(0), padding_mobile=sp(0))
    head = C([label("Le tre anime di LT3", GREEN, 12),
              heading("Eventi, comunicazione, scienza. Un solo metodo.", 64, "h2", DARK, "300", 46, 36, 1.04, -1.8),
              text("<p>Ogni anima lavora da sola o insieme alle altre: è LT3 Global Care, dall'idea alla chiusura dell'evento.</p>", 18, TEXT2, 16, 640)],
             flex_direction="column", flex_direction_mobile="column", flex_gap=gap(18), padding=sp(0), padding_mobile=sp(0))
    row = C([card("01", "Events", "events", "Auditorium di un congresso visto dall'ultima fila",
                  "Progettiamo e realizziamo eventi, congressi e residenziali, dall'idea alla chiusura.", 0),
             card("02", "Communication", "comm", "Impaginati e bozze di comunicazione su un tavolo di lavoro",
                  "Comunicazione scientifica e di marca per il mondo Pharma.", 80),
             card("03", "Scientific", "sci", "Biblioteca scientifica con tavolo di lettura e lampada verde",
                  "ECM, Comitato Scientifico, FAD, accreditamento e rendicontazione.", 160)],
            flex_direction="row", flex_direction_tablet="column", flex_direction_mobile="column",
            flex_justify_content="space-between", flex_align_items="flex-start", flex_gap=gap(32),
            flex_gap_mobile=gap(56), padding=sp(0), padding_mobile=sp(0))
    return write("sec-anime", root("sec-anime", [boxed([head, row], 1280, "column", 72)], MIST))


# ------------------------------------------------------------------ METODO
def metodo():
    pillars = ["Provider accreditato AGENAS", "Comitato Scientifico indipendente",
               "Rendicontazione a Co.Ge.A.P.S.", "Conformità normativa"]
    pill_items = [C([marker(SAGE, 10), heading(p, 22, "h3", WHITE, "300", 20, 19, 1.2, -0.2)],
                    flex_direction="row", flex_direction_mobile="row", flex_align_items="center", flex_gap=gap(16),
                    padding=sp(18, 0), padding_mobile=sp(14, 0),
                    border_border="solid", border_width={"unit": "px", "top": "0", "right": "0", "bottom": "1", "left": "0", "isLinked": False},
                    border_color=hexa(SAGE, 0.28)) for p in pillars]
    left = C([label("Il metodo", SAGE, 12),
              heading("Marketing, Medical Affairs, Market Access: un solo partner per progettare, accreditare e rendicontare.",
                      46, "h2", WHITE, "300", 34, 30, 1.1, -1.2)],
             flex_direction="column", flex_direction_mobile="column", flex_gap=gap(22),
             width={"unit": "%", "size": 52}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
             padding=sp(0), padding_mobile=sp(0))
    right = C(pill_items, flex_direction="column", flex_direction_mobile="column", flex_gap=gap(0),
              width={"unit": "%", "size": 40}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
              padding=sp(0), padding_mobile=sp(0))
    top = C([left, right], flex_direction="row", flex_direction_tablet="column", flex_direction_mobile="column",
            flex_justify_content="space-between", flex_gap=gap(56), flex_gap_mobile=gap(36), padding=sp(0), padding_mobile=sp(0))

    def counter(n, suffix, title):
        s = {"starting_number": 0, "ending_number": n, "suffix": suffix, "duration": 1800,
             "thousand_separator": "yes", "thousand_separator_char": ".",
             "title": title, "number_color": SAGE, "title_color": WHITE,
             "title_typography_typography": "custom"}
        s.update(typo("Outfit", "300", 64, 52, 44, 1.0, -1.5, False, "typography_number_"))
        s.update(typo("Outfit", "400", 15, 15, 14, 1.4, 0, False, "typography_title_"))
        return C([W("counter", s)], flex_direction="column", flex_direction_mobile="column",
                 width={"unit": "%", "size": 23.5}, width_tablet={"unit": "%", "size": 48}, width_mobile={"unit": "%", "size": 100},
                 padding=sp(28, 0, 0, 0), padding_mobile=sp(20, 0, 0, 0),
                 border_border="solid", border_width={"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                 border_color=hexa(SAGE, 0.3))
    nums = C([counter(23, "", "anni di attività"), counter(330, "", "eventi l'anno (media degli ultimi 3 anni)"),
              counter(6668, "", "medici ai corsi ECM l'anno (media degli ultimi 3 anni)"),
              counter(11396, "", "partecipanti agli eventi nell'ultimo anno")],
             flex_direction="row", flex_direction_mobile="column", flex_wrap="wrap", flex_justify_content="space-between",
             flex_gap=gap(32), flex_gap_mobile=gap(24), padding=sp(0), padding_mobile=sp(0))

    def step(n, name):
        return C([label(n, SAGE, 12), heading(name, 26, "h3", WHITE, "300", 22, 22, 1.15, -0.4)],
                 flex_direction="column", flex_direction_mobile="column", flex_gap=gap(14),
                 width={"unit": "%", "size": 23.5}, width_tablet={"unit": "%", "size": 48}, width_mobile={"unit": "%", "size": 100},
                 padding=sp(24, 0, 0, 0), padding_mobile=sp(18, 0, 0, 0),
                 border_border="solid", border_width={"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                 border_color=hexa(SAGE, 0.3))
    steps = C([step("01", "Brief"), step("02", "Progetto scientifico"), step("03", "Evento o esperienza"),
               step("04", "Accreditamento e report")],
              flex_direction="row", flex_direction_mobile="column", flex_wrap="wrap", flex_justify_content="space-between",
              flex_gap=gap(32), flex_gap_mobile=gap(24), padding=sp(0), padding_mobile=sp(0))
    return write("sec-metodo", root("sec-metodo", [boxed([top, nums, steps], 1280, "column", 88)], DARK))


# ------------------------------------------------------------------ CONTATTI
def contatti():
    def fld(cid, ftype, lab, width="100", req=False, **kw):
        f = {"_id": rid() + "0"[:0], "custom_id": cid, "field_type": ftype, "field_label": lab, "width": width,
             "required": "true" if req else "", "placeholder": ""}
        f["_id"] = rid()
        f.update(kw)
        return f
    fields = [fld("nome", "text", "Nome", "50", True), fld("cognome", "text", "Cognome", "50", True),
              fld("azienda", "text", "Azienda", "50", True), fld("ruolo", "text", "Ruolo", "50", True),
              fld("email", "email", "Email aziendale", "50", True), fld("telefono", "tel", "Telefono (facoltativo)", "50"),
              fld("tipo", "select", "Tipo di progetto", "100", True, field_options="Evento\nComunicazione\nProgetto ECM\nAltro"),
              fld("messaggio", "textarea", "Messaggio", "100", False, rows=4),
              fld("privacy", "acceptance", "", "100", True, acceptance_text="Ho letto l'informativa privacy e acconsento al trattamento dei dati per essere ricontattato.")]
    form = {"form_name": "LT3 Contatti", "form_fields": fields, "button_text": "Invia la richiesta",
            "button_size": "md", "step_type": "none", "submit_actions": ["email"],
            "email_subject": "Nuova richiesta dalla homepage LT3", "email_from_name": "LT3 — sito",
            "success_message": "Grazie, abbiamo ricevuto la tua richiesta.",
            "show_labels": "yes", "label_color": DARK, "field_text_color": DARK, "field_background_color": WHITE,
            "field_border_color": hexa(GREEN, 0.28), "field_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "field_border_radius": {"unit": "px", "top": "2", "right": "2", "bottom": "2", "left": "2", "isLinked": True},
            "button_background_color": GREEN, "button_text_color": WHITE, "button_hover_background_color": DARK,
            "button_border_radius": {"unit": "px", "top": "999", "right": "999", "bottom": "999", "left": "999", "isLinked": True},
            "column_gap": px(16), "row_gap": px(18)}
    form.update(typo("Outfit", "400", 15, 15, 15, 1.4, 0, False, "field_typography_"))
    form.update(typo("Outfit", "600", 13, 13, 13, 1.4, 0.6, False, "button_typography_"))
    form.update(typo("Outfit", "600", 12, 12, 12, 1.4, 1.5, True, "label_typography_"))
    form_card = C([W("form", form)], flex_direction="column", flex_direction_mobile="column",
                  width={"unit": "%", "size": 55}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
                  background_background="classic", background_color=WHITE,
                  border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                  border_color=hexa(GREEN, 0.14), padding=sp(44), padding_mobile=sp(22))
    info = C([label("Contatti", GREEN, 12),
              heading("Raccontaci il tuo progetto.", 60, "h2", DARK, "300", 44, 36, 1.04, -1.6),
              C([marker(GREEN, 10), text("<p><strong>LT3 S.r.l.</strong><br>Via Regina, 61<br>22012 Cernobbio (CO)</p>", 18, DARK, 16)],
                flex_direction="row", flex_direction_mobile="row", flex_gap=gap(14), flex_align_items="flex-start", padding=sp(0), padding_mobile=sp(0)),
              C([marker(GREEN, 10), text('<p><a href="tel:+39031511626" style="color:inherit">+39 031 511626</a></p>', 18, DARK, 16)],
                flex_direction="row", flex_direction_mobile="row", flex_gap=gap(14), flex_align_items="flex-start", padding=sp(0), padding_mobile=sp(0))],
             flex_direction="column", flex_direction_mobile="column", flex_gap=gap(22),
             width={"unit": "%", "size": 36}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
             padding=sp(0), padding_mobile=sp(0))
    row = C([info, form_card], flex_direction="row", flex_direction_tablet="column", flex_direction_mobile="column",
            flex_justify_content="space-between", flex_align_items="flex-start", flex_gap=gap(56), flex_gap_mobile=gap(36),
            padding=sp(0), padding_mobile=sp(0))
    return write("sec-contatti", root("sec-contatti", [boxed([row], 1280)], MIST))


# ------------------------------------------------------------------ FOOTER
def footer():
    logo = image("logo", "LT3", 100, 0)
    logo["settings"]["width"] = {"unit": "px", "size": 150}
    logo["settings"]["_element_width"] = "initial"
    legal = C([text("<p><strong>LT3 S.r.l.</strong><br>Via Regina, 61 · 22012 Cernobbio (CO)<br>P.IVA 02236240137 · Tel. +39 031 511626</p>", 15, DARK, 14),
               text("<p>Società soggetta a direzione e coordinamento da parte di Meduspace S.p.A. Società Benefit.</p>", 14, TEXT2, 13)],
              flex_direction="column", flex_direction_mobile="column", flex_gap=gap(14),
              width={"unit": "%", "size": 44}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
              padding=sp(0), padding_mobile=sp(0))
    links = C([label("Privacy Policy", DARK, 12, "https://www.lt3.it/"), label("Cookie Policy", DARK, 12, "https://www.lt3.it/"),
               label("Contatti", DARK, 12, "#sec-contatti")],
              flex_direction="column", flex_direction_mobile="column", flex_gap=gap(14),
              width={"unit": "%", "size": 20}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100},
              padding=sp(0), padding_mobile=sp(0))
    top = C([logo, legal, links], flex_direction="row", flex_direction_tablet="column", flex_direction_mobile="column",
            flex_justify_content="space-between", flex_align_items="flex-start", flex_gap=gap(48), flex_gap_mobile=gap(32),
            padding=sp(0), padding_mobile=sp(0))
    medu = image("medu", "Member of Meduspace", 100, 0)
    medu["settings"]["width"] = {"unit": "px", "size": 420}
    medu["settings"]["width_mobile"] = {"unit": "%", "size": 100}
    medu["settings"]["_element_width"] = "initial"
    band = C([medu], flex_direction="row", flex_direction_mobile="column", flex_justify_content="center", flex_align_items="center",
             background_background="classic", background_color=WHITE, padding=sp(48, 32), padding_mobile=sp(36, 20),
             border_border="solid", border_width={"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
             border_color=hexa(GREEN, 0.14), width={"unit": "%", "size": 100})
    copy = text("<p>© 2026 LT3 S.r.l. Tutti i diritti riservati.</p>", 13, TEXT2, 12)
    main = root("sec-footer", [boxed([top, copy], 1280, "column", 48), band], MIST, pad=(96, 32), gp=72,
                border_border="solid", border_width={"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                border_color=hexa(GREEN, 0.14))
    main["settings"]["padding"] = sp(96, 32, 0, 32)
    main["settings"]["padding_mobile"] = sp(64, 20, 0, 20)
    main["settings"]["flex_gap"] = gap(72)
    return write("sec-footer", main)


if __name__ == "__main__":
    order = [header(), hero(), anime(), metodo(), contatti(), footer()]
    with open(os.path.join(os.path.dirname(OUT), "page-state.json"), "w") as f:
        json.dump({e["settings"]["css_id"]: e for e in order}, f, ensure_ascii=False)
    for e in order:
        p = os.path.join(OUT, e["settings"]["css_id"] + ".json")
        print(e["settings"]["css_id"], os.path.getsize(p), "bytes")
