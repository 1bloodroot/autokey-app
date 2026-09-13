import sys, io
if sys.stdout is None: sys.stdout = io.StringIO()
if sys.stderr is None: sys.stderr = io.StringIO()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading, time, os, webbrowser, random, math, json
import queue as _q
import numpy as np
from PIL import ImageGrab, ImageTk, Image, ImageDraw, ImageFont
import keyboard
import base64
import ctypes
import tempfile

# ═══ КАРТИНКИ (из embedded_images.py) ═══
BG_BASE64 = None
ICON_BASE64 = None
APP_ICON_BASE64 = None
try:
    from embedded_images import BG_BASE64, ICON_BASE64, APP_ICON_BASE64
except ImportError:
    pass

def _b64_to_image(b64_str):
    data = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(data))

def _set_app_icon(root):
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AutoKey.ReZero")
    except Exception:
        pass
    icon_path = None
    d = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(d, "icon.ico")
    if os.path.exists(p):
        icon_path = p
    if not icon_path:
        try:
            p = os.path.join(sys._MEIPASS, "icon.ico")
            if os.path.exists(p):
                icon_path = p
        except Exception:
            pass
    if not icon_path and APP_ICON_BASE64:
        try:
            data = base64.b64decode(APP_ICON_BASE64)
            tf = os.path.join(tempfile.gettempdir(), "autokey_icon.ico")
            with open(tf, "wb") as f:
                f.write(data)
            icon_path = tf
        except Exception:
            pass
    if icon_path:
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass

# ═══ КОНФИГ ═══
def _cfg_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.expanduser("~"), ".autokey_config.json")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ".autokey_config.json")

def _load_cfg():
    try:
        with open(_cfg_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _save_cfg(cfg):
    try:
        with open(_cfg_path(), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except:
        pass

# ═══ ПЕРЕВОДЫ ═══
_LANG = "RU"

LANGS = {
    "RU": {
        "header": "\u27e1  AUTOKEY  \u27e1",
        "settings": "\u2699  НАСТРОЙКИ",
        "settings_title": "Настройки",
        "language": "Язык",
        "theme": "Тема оформления",
        "interval": "Интервал между нажатиями",
        "antibot": "Антибот",
        "antibot_desc": "Разброс \u00b1100 мс от установленного интервала",
        "graph_hint": "График отклонения (внизу слева) можно перетащить мышью",
        "show_regions": "Показать выделенные области",
        "key_label": "Клавиша:",
        "startstop_label": "Старт/стоп:",
        "threshold": "Порог совпадения",
        "bg_image": "Фоновое изображение",
        "bg_label": "Фон:",
        "icon_button": "Иконка кнопки старт/стоп",
        "icon_label": "Иконка:",
        "from_file": "Из файла",
        "reset": "Сбросить",
        "not_selected": "Не выбрана — клик для выбора",
        "region1": "\u25c6 Область 1 \u2014 триггер",
        "region2": "\u25c6 Область 2 \u2014 стоп",
        "region1_banner": "\u25c6 Область 1 \u2014 триггер \u25c6",
        "region2_banner": "\u25c6 Область 2 \u2014 стоп \u25c6",
        "select_area": "Выделите область",
        "select_r1": "Выделите ОБЛАСТЬ 1 — триггер",
        "select_r2": "Выделите ОБЛАСТЬ 2 — стоп",
        "stopped": "Остановлено",
        "waiting": "Отслеживание активно: ожидание совпадения области 1",
        "pressing": "Нажатие активно — область 1 совпала",
        "paused": "Приостановлено: область 2 изменилась",
        "hint": "\u2699 — настройки  •  Зажмите клавишу показа — увидите прямоугольники",
        "footer": "\u2762  Return by Death  \u2762",
        "forbidden": "Запрещено",
        "win_key_err": "Клавиша Windows недоступна.",
        "warning": "Внимание",
        "select_r1_first": "Сначала выберите Область 1.",
        "enter_key": "Укажите клавишу.",
        "min": "мин", "sec": "сек", "ms": "мс",
        "theme_rezero": "Re:Zero Edition",
        "theme_night": "Ночь",
        "theme_light": "Светлая",
        "select_bg": "Выберите фон",
        "select_icon": "Выберите иконку",
    },
    "EN": {
        "header": "\u27e1  AUTOKEY  \u27e1",
        "settings": "\u2699  SETTINGS",
        "settings_title": "Settings",
        "language": "Language",
        "theme": "Theme",
        "interval": "Interval between presses",
        "antibot": "Anti-bot",
        "antibot_desc": "Spread \u00b1100 ms from set interval",
        "graph_hint": "Deviation graph (bottom left) can be dragged with mouse",
        "show_regions": "Show selected regions",
        "key_label": "Key:",
        "startstop_label": "Start/Stop:",
        "threshold": "Match threshold",
        "bg_image": "Background image",
        "bg_label": "Background:",
        "icon_button": "Start/Stop button icon",
        "icon_label": "Icon:",
        "from_file": "From file",
        "reset": "Reset",
        "not_selected": "Not selected — click to select",
        "region1": "\u25c6 Region 1 \u2014 trigger",
        "region2": "\u25c6 Region 2 \u2014 stop",
        "region1_banner": "\u25c6 Region 1 \u2014 trigger \u25c6",
        "region2_banner": "\u25c6 Region 2 \u2014 stop \u25c6",
        "select_area": "Select area",
        "select_r1": "Select REGION 1 — trigger",
        "select_r2": "Select REGION 2 — stop",
        "stopped": "Stopped",
        "waiting": "Monitoring: waiting for region 1 match",
        "pressing": "Pressing active — region 1 matched",
        "paused": "Paused: region 2 changed",
        "hint": "\u2699 — settings  •  Hold show key to see rectangles",
        "footer": "\u2762  Return by Death  \u2762",
        "forbidden": "Forbidden",
        "win_key_err": "Windows key is not available.",
        "warning": "Warning",
        "select_r1_first": "Select Region 1 first.",
        "enter_key": "Specify a key.",
        "min": "min", "sec": "sec", "ms": "ms",
        "theme_rezero": "Re:Zero Edition",
        "theme_night": "Night",
        "theme_light": "Light",
        "select_bg": "Select background",
        "select_icon": "Select icon",
    },
    "DE": {
        "header": "\u27e1  AUTOKEY  \u27e1",
        "settings": "\u2699  EINSTELLUNGEN",
        "settings_title": "Einstellungen",
        "language": "Sprache",
        "theme": "Design",
        "interval": "Intervall zwischen Tastendr\u00fccken",
        "antibot": "Anti-Bot",
        "antibot_desc": "Streuung \u00b1100 ms vom eingestellten Intervall",
        "graph_hint": "Abweichungsdiagramm (unten links) per Maus verschiebbar",
        "show_regions": "Ausgew\u00e4hlte Bereiche anzeigen",
        "key_label": "Taste:",
        "startstop_label": "Start/Stop:",
        "threshold": "\u00dcbereinstimmungsschwelle",
        "bg_image": "Hintergrundbild",
        "bg_label": "Hintergrund:",
        "icon_button": "Start/Stop-Schaltfl\u00e4chensymbol",
        "icon_label": "Symbol:",
        "from_file": "Aus Datei",
        "reset": "Zur\u00fccksetzen",
        "not_selected": "Nicht ausgew\u00e4hlt \u2014 Klick zum Ausw\u00e4hlen",
        "region1": "\u25c6 Bereich 1 \u2014 Ausl\u00f6ser",
        "region2": "\u25c6 Bereich 2 \u2014 Stopp",
        "region1_banner": "\u25c6 Bereich 1 \u2014 Ausl\u00f6ser \u25c6",
        "region2_banner": "\u25c6 Bereich 2 \u2014 Stopp \u25c6",
        "select_area": "Bereich ausw\u00e4hlen",
        "select_r1": "BEREICH 1 ausw\u00e4hlen \u2014 Ausl\u00f6ser",
        "select_r2": "BEREICH 2 ausw\u00e4hlen \u2014 Stopp",
        "stopped": "Gestoppt",
        "waiting": "\u00dcberwachung aktiv: Warten auf \u00dcbereinstimmung von Bereich 1",
        "pressing": "Tastendruck aktiv \u2014 Bereich 1 stimmt \u00fcberein",
        "paused": "Pausiert: Bereich 2 hat sich ge\u00e4ndert",
        "hint": "\u2699 \u2014 Einstellungen  \u2022  Anzeigetaste gedr\u00fcckt halten \u2014 Rechtecke werden angezeigt",
        "footer": "\u2762  Return by Death  \u2762",
        "forbidden": "Verboten",
        "win_key_err": "Windows-Taste ist nicht verf\u00fcgbar.",
        "warning": "Achtung",
        "select_r1_first": "Bitte zuerst Bereich 1 ausw\u00e4hlen.",
        "enter_key": "Bitte eine Taste angeben.",
        "min": "Min", "sec": "Sek", "ms": "ms",
        "theme_rezero": "Re:Zero Edition",
        "theme_night": "Nacht",
        "theme_light": "Hell",
        "select_bg": "Hintergrund ausw\u00e4hlen",
        "select_icon": "Symbol ausw\u00e4hlen",
    },
    "ZH": {
        "header": "\u27e1  AUTOKEY  \u27e1",
        "settings": "\u2699  \u8bbe\u7f6e",
        "settings_title": "\u8bbe\u7f6e",
        "language": "\u8bed\u8a00",
        "theme": "\u4e3b\u9898",
        "interval": "\u6309\u952e\u95f4\u9694",
        "antibot": "\u9632\u673a\u5668\u4eba",
        "antibot_desc": "\u5728\u8bbe\u5b9a\u95f4\u9694\u4e0a \u00b1100 \u6beb\u79d2\u7684\u968f\u673a\u504f\u79fb",
        "graph_hint": "\u504f\u5dee\u56fe\u8868\uff08\u5de6\u4e0b\u89d2\uff09\u53ef\u4ee5\u7528\u9f20\u6807\u62d6\u52a8",
        "show_regions": "\u663e\u793a\u9009\u5b9a\u533a\u57df",
        "key_label": "\u6309\u952e\uff1a",
        "startstop_label": "\u542f\u52a8/\u505c\u6b62\uff1a",
        "threshold": "\u5339\u914d\u9608\u503c",
        "bg_image": "\u80cc\u666f\u56fe\u7247",
        "bg_label": "\u80cc\u666f\uff1a",
        "icon_button": "\u542f\u52a8/\u505c\u6b62\u6309\u94ae\u56fe\u6807",
        "icon_label": "\u56fe\u6807\uff1a",
        "from_file": "\u4ece\u6587\u4ef6",
        "reset": "\u91cd\u7f6e",
        "not_selected": "\u672a\u9009\u62e9 \u2014 \u70b9\u51fb\u9009\u62e9",
        "region1": "\u25c6 \u533a\u57df 1 \u2014 \u89e6\u53d1\u5668",
        "region2": "\u25c6 \u533a\u57df 2 \u2014 \u505c\u6b62",
        "region1_banner": "\u25c6 \u533a\u57df 1 \u2014 \u89e6\u53d1\u5668 \u25c6",
        "region2_banner": "\u25c6 \u533a\u57df 2 \u2014 \u505c\u6b62 \u25c6",
        "select_area": "\u9009\u62e9\u533a\u57df",
        "select_r1": "\u9009\u62e9\u533a\u57df 1 \u2014 \u89e6\u53d1\u5668",
        "select_r2": "\u9009\u62e9\u533a\u57df 2 \u2014 \u505c\u6b62",
        "stopped": "\u5df2\u505c\u6b62",
        "waiting": "\u76d1\u63a7\u4e2d\uff1a\u7b49\u5f85\u533a\u57df 1 \u5339\u914d",
        "pressing": "\u6309\u952e\u4e2d \u2014 \u533a\u57df 1 \u5df2\u5339\u914d",
        "paused": "\u5df2\u6682\u505c\uff1a\u533a\u57df 2 \u5df2\u53d8\u5316",
        "hint": "\u2699 \u2014 \u8bbe\u7f6e  \u2022  \u6309\u4f4f\u663e\u793a\u952e\u53ef\u67e5\u770b\u77e9\u5f62\u6846",
        "footer": "\u2762  Return by Death  \u2762",
        "forbidden": "\u7981\u6b62",
        "win_key_err": "Windows \u952e\u4e0d\u53ef\u7528\u3002",
        "warning": "\u6ce8\u610f",
        "select_r1_first": "\u8bf7\u5148\u9009\u62e9\u533a\u57df 1\u3002",
        "enter_key": "\u8bf7\u6307\u5b9a\u6309\u952e\u3002",
        "min": "\u5206", "sec": "\u79d2", "ms": "\u6beb\u79d2",
        "theme_rezero": "Re:Zero Edition",
        "theme_night": "\u591c\u665a",
        "theme_light": "\u660e\u4eae",
        "select_bg": "\u9009\u62e9\u80cc\u666f",
        "select_icon": "\u9009\u62e9\u56fe\u6807",
    },
    "JA": {
        "header": "\u27e1  AUTOKEY  \u27e1",
        "settings": "\u2699  \u8a2d\u5b9a",
        "settings_title": "\u8a2d\u5b9a",
        "language": "\u8a00\u8a9e",
        "theme": "\u30c6\u30fc\u30de",
        "interval": "\u30ad\u30fc\u5165\u529b\u9593\u9694",
        "antibot": "\u30a2\u30f3\u30c1\u30dc\u30c3\u30c8",
        "antibot_desc": "\u8a2d\u5b9a\u9593\u9694\u304b\u3089 \u00b1100 \u30df\u30ea\u79d2\u306e\u30e9\u30f3\u30c0\u30e0\u504f\u5dee",
        "graph_hint": "\u504f\u5dee\u30b0\u30e9\u30d5\uff08\u5de6\u4e0b\uff09\u306f\u30de\u30a6\u30b9\u3067\u30c9\u30e9\u30c3\u30b0\u3067\u304d\u307e\u3059",
        "show_regions": "\u9078\u629e\u7bc4\u56f2\u3092\u8868\u793a",
        "key_label": "\u30ad\u30fc\uff1a",
        "startstop_label": "\u958b\u59cb/\u505c\u6b62\uff1a",
        "threshold": "\u4e00\u81f4\u3057\u304d\u3044\u5024",
        "bg_image": "\u80cc\u666f\u753b\u50cf",
        "bg_label": "\u80cc\u666f\uff1a",
        "icon_button": "\u958b\u59cb/\u505c\u6b62\u30dc\u30bf\u30f3\u30a2\u30a4\u30b3\u30f3",
        "icon_label": "\u30a2\u30a4\u30b3\u30f3\uff1a",
        "from_file": "\u30d5\u30a1\u30a4\u30eb\u304b\u3089",
        "reset": "\u30ea\u30bb\u30c3\u30c8",
        "not_selected": "\u672a\u9078\u629e \u2014 \u30af\u30ea\u30c3\u30af\u3057\u3066\u9078\u629e",
        "region1": "\u25c6 \u9818\u57df 1 \u2014 \u30c8\u30ea\u30ac\u30fc",
        "region2": "\u25c6 \u9818\u57df 2 \u2014 \u505c\u6b62",
        "region1_banner": "\u25c6 \u9818\u57df 1 \u2014 \u30c8\u30ea\u30ac\u30fc \u25c6",
        "region2_banner": "\u25c6 \u9818\u57df 2 \u2014 \u505c\u6b62 \u25c6",
        "select_area": "\u9818\u57df\u3092\u9078\u629e",
        "select_r1": "\u9818\u57df 1 \u3092\u9078\u629e \u2014 \u30c8\u30ea\u30ac\u30fc",
        "select_r2": "\u9818\u57df 2 \u3092\u9078\u629e \u2014 \u505c\u6b62",
        "stopped": "\u505c\u6b62\u4e2d",
        "waiting": "\u76e3\u8996\u4e2d\uff1a\u9818\u57df 1 \u306e\u4e00\u81f4\u3092\u5f85\u6a5f\u4e2d",
        "pressing": "\u30ad\u30fc\u5165\u529b\u4e2d \u2014 \u9818\u57df 1 \u304c\u4e00\u81f4",
        "paused": "\u4e00\u6642\u505c\u6b62\uff1a\u9818\u57df 2 \u304c\u5909\u66f4\u3055\u308c\u307e\u3057\u305f",
        "hint": "\u2699 \u2014 \u8a2d\u5b9a  \u2022  \u8868\u793a\u30ad\u30fc\u3092\u9577\u62bc\u3057\u3067\u56db\u89d2\u5f62\u304c\u8868\u793a\u3055\u308c\u307e\u3059",
        "footer": "\u2762  Return by Death  \u2762",
        "forbidden": "\u7981\u6b62",
        "win_key_err": "Windows \u30ad\u30fc\u306f\u4f7f\u7528\u3067\u304d\u307e\u305b\u3093\u3002",
        "warning": "\u6ce8\u610f",
        "select_r1_first": "\u307e\u305a\u9818\u57df 1 \u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "enter_key": "\u30ad\u30fc\u3092\u6307\u5b9a\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "min": "\u5206", "sec": "\u79d2", "ms": "\u30df\u30ea\u79d2",
        "theme_rezero": "Re:Zero Edition",
        "theme_night": "\u591c",
        "theme_light": "\u30e9\u30a4\u30c8",
        "select_bg": "\u80cc\u666f\u3092\u9078\u629e",
        "select_icon": "\u30a2\u30a4\u30b3\u30f3\u3092\u9078\u629e",
    },
}

def _t(key):
    return LANGS.get(_LANG, LANGS["RU"]).get(key, LANGS["RU"].get(key, key))

def _theme_name(theme_id):
    mapping = {"Re:Zero Edition": "theme_rezero", "\u041d\u043e\u0447\u044c": "theme_night", "\u0421\u0432\u0435\u0442\u043b\u0430\u044f": "theme_light"}
    return _t(mapping.get(theme_id, theme_id))

LANG_NAMES = [("RU","\u0420\u0443\u0441\u0441\u043a\u0438\u0439"),("EN","English"),("DE","Deutsch"),("ZH","\u4e2d\u6587"),("JA","\u65e5\u672c\u8a9e")]

_RU_EN = {
    '\u0439':'q','\u0446':'w','\u0443':'e','\u043a':'r','\u0435':'t','\u043d':'y','\u0433':'u','\u0448':'i','\u0449':'o','\u0437':'p','\u0445':'[','\u044a':']',
    '\u0444':'a','\u044b':'s','\u0432':'d','\u0430':'f','\u043f':'g','\u0440':'h','\u043e':'j','\u043b':'k','\u0434':'l','\u0436':';','\u044d':"'",
    '\u044f':'z','\u0447':'x','\u0441':'c','\u043c':'v','\u0438':'b','\u0442':'n','\u044c':'m','\u0431':',','\u044e':'.',
    '\u0451':'`','\u2116':'#',
}
def _norm_key(k):
    k = k.strip().lower()
    k = ''.join(_RU_EN.get(c, c) for c in k)
    try:
        n = keyboard.normalize_name(k)
        if n: return n
    except: pass
    return k
def _key_scancodes(k):
    try: return set(keyboard.key_to_scan_codes(k))
    except: return set()

def _rgb(c): return int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
def _font(sz):
    for p in ["C:/Windows/Fonts/segoeui.ttf","C:/Windows/Fonts/arial.ttf",
              "C:/Windows/Fonts/msyh.ttc","C:/Windows/Fonts/meiryo.ttc",
              "C:/Windows/Fonts/simsun.ttc","C:/Windows/Fonts/Deng.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()
def _rrect(img, r):
    w,h = img.size; s=2; m = Image.new("L",(w*s,h*s),0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,w*s-1,h*s-1], radius=r*s, fill=255)
    m = m.resize((w,h), Image.LANCZOS); r2 = img.convert("RGBA"); r2.putalpha(m); return r2

THEMES = {
    "Re:Zero Edition": dict(bg="#0d0b1e",fbg="#16122e",bd="#3a2f6a",acc="#6ba3d6",acc2="#c8a8e8",
        txt="#e8e8f0",dim="#8888aa",red="#e0506e",pink="#e870b0",gold="#d4af37",
        bb="#1e1838",ba="#2a2050",eb="#120e24",str3="#3a2f6a",sfg="#6ba3d6",
        soff="#666688",swait="#e0a040",son="#4ed098",sstop="#e0506e",
        hdr="#d4af37",sub="#c8a8e8",ftr="#8888aa",gr="#6ba3d6",
        tsb="#1a2e22",tob="#2e1a1a",
        baa=0.15,has_bg=True,has_banner=True,gen="rezero"),
    "\u041d\u043e\u0447\u044c": dict(bg="#080810",fbg="#0e0e1a",bd="#1c1c30",acc="#6080b0",acc2="#405080",
        txt="#b8c0d8",dim="#484860",red="#c04040",pink="#905090",gold="#807020",
        bb="#101020",ba="#181830",eb="#080814",str3="#1c1c30",sfg="#6080b0",
        soff="#484860",swait="#807020",son="#30a060",sstop="#c04040",
        hdr="#6080b0",sub="#405080",ftr="#484860",gr="#6080b0",
        tsb="#0c1c14",tob="#1c0c0c",
        baa=0.40,has_bg=True,has_banner=False,gen="night"),
    "\u0421\u0432\u0435\u0442\u043b\u0430\u044f": dict(bg="#fdf5f0",fbg="#faf0eb",bd="#e8d0c8",acc="#c08090",acc2="#d4a0b0",
        txt="#8a6070",dim="#b8a0a8",red="#e07080",pink="#d4a0b0",gold="#c4a070",
        bb="#f5ebe5",ba="#eedfd5",eb="#fff8f5",str3="#e8d0c8",sfg="#c08090",
        soff="#b8a0a8",swait="#c4a070",son="#80b090",sstop="#e07080",
        hdr="#c08090",sub="#d4a0b0",ftr="#b8a0a8",gr="#c08090",
        tsb="#f5e8e0",tob="#f0e0e0",
        baa=0.15,has_bg=True,has_banner=False,gen="light_rose"),
}

# \u041a\u042d\u0428 \u0411\u0410\u041d\u041d\u0415\u0420\u0410
_BANNER_CACHE = {}

def _gen_bg(w,h,gen):
    if gen=="light_rose":
        a=np.zeros((h,w,3),np.uint8)
        a[:,:,0]=253; a[:,:,1]=245; a[:,:,2]=240
        im=Image.fromarray(a); d=ImageDraw.Draw(im); r=random.Random(27)
        for _ in range(35):
            x,y=r.randint(0,w-1),r.randint(0,h-1); rad=r.randint(25,90)
            pr,pg,pb=r.randint(235,250),r.randint(205,225),r.randint(210,230)
            for rr in range(rad,0,-2):
                t=1-rr/rad; mix=t*0.12
                d.ellipse([x-rr,y-rr,x+rr,y+rr],fill=(
                    int(253*(1-mix)+pr*mix),int(245*(1-mix)+pg*mix),int(240*(1-mix)+pb*mix)))
        for _ in range(18):
            x,y=r.randint(15,w-15),r.randint(15,h-15); sz=r.randint(8,16)
            for ang in range(0,360,72):
                rd=math.radians(ang)
                px=x+int(sz*0.7*math.cos(rd)); py=y+int(sz*0.7*math.sin(rd))
                d.ellipse([px-sz//2,py-sz//2,px+sz//2,py+sz//2],fill=(248,218,228))
            d.ellipse([x-sz//3,y-sz//3,x+sz//3,y+sz//3],fill=(255,238,228))
        for _ in range(80):
            x,y=r.randint(0,w-1),r.randint(0,h-1)
            d.ellipse([x-1,y-1,x+2,y+2],fill=(240,210,220))
        return im
    a=np.zeros((h,w,3),np.uint8)
    for y in range(h):
        t=y/h; a[y,:,0]=6+int(t*4); a[y,:,1]=6+int(t*4); a[y,:,2]=14+int(t*8)
    im=Image.fromarray(a); d=ImageDraw.Draw(im); r=random.Random(99)
    for x in range(0,w,40): d.line([(x,0),(x,h)],fill=(14,14,26))
    for y in range(0,h,40): d.line([(0,y),(w,y)],fill=(14,14,26))
    for gx in range(0,w,40):
        for gy in range(0,h,40):
            if r.random()<0.15:
                for rr in range(5,0,-1): d.ellipse([gx-rr,gy-rr,gx+rr,gy+rr],fill=(50-rr*8,50-rr*8,70-rr*8))
                d.ellipse([gx-1,gy-1,gx+1,gy+1],fill=(60,60,100))
    return im

def _gen_banner(w,h):
    key = (w,h)
    if key in _BANNER_CACHE:
        return _BANNER_CACHE[key]
    im=Image.new("RGB",(w,h),(13,11,30)); d=ImageDraw.Draw(im); r=random.Random(7)
    for _ in range(50):
        x,y=r.randint(0,w-1),r.randint(0,h-1); br=r.randint(80,200)
        d.ellipse([x,y,x+1,y+1],fill=(br,br,min(255,br+20)))
    f=_font(max(14,h//3)); txt="Re:Zero \u2014 Starting Life in Another World"
    b=d.textbbox((0,0),txt,font=f)
    d.text(((w-(b[2]-b[0]))//2,(h-(b[3]-b[1]))//2),txt,font=f,fill=(220,220,250))
    _BANNER_CACHE[key] = im
    return im

def _gen_icon(s,gen):
    im=Image.new("RGBA",(s,s),(0,0,0,0)); d=ImageDraw.Draw(im); cx,cy,r=s//2,s//2,s//2-2
    if gen=="light_rose":
        for i in range(r,0,-1):
            t=1-i/r
            d.ellipse([cx-i,cy-i,cx+i,cy+i],fill=(250-int(t*15),220-int(t*30),230-int(t*20),255))
        for ang in range(0,360,45):
            rd=math.radians(ang); pr=int(r*0.45)
            px=cx+int(r*0.4*math.cos(rd)); py=cy+int(r*0.4*math.sin(rd))
            d.ellipse([px-pr,py-pr,px+pr,py+pr],fill=(255,235,240,230))
        for ang in range(22,382,45):
            rd=math.radians(ang); pr=int(r*0.3)
            px=cx+int(r*0.25*math.cos(rd)); py=cy+int(r*0.25*math.sin(rd))
            d.ellipse([px-pr,py-pr,px+pr,py+pr],fill=(255,220,230,240))
        cr=int(r*0.2)
        d.ellipse([cx-cr,cy-cr,cx+cr,cy+cr],fill=(255,200,180,255))
        d.ellipse([cx-cr+2,cy-cr+1,cx+cr-3,cy+cr-3],fill=(255,230,210,255))
        return im
    for i in range(r,0,-1):
        t=1-i/r; d.ellipse([cx-i,cy-i,cx+i,cy+i],fill=(16+int(t*20),28+int(t*30),56+int(t*70),255))
    mr=int(r*0.55); d.ellipse([cx-mr,cy-mr,cx+mr,cy+mr],fill=(170,185,220,255))
    d.ellipse([cx-mr+int(mr*0.35),cy-mr-int(mr*0.12),cx+mr+int(mr*0.35),cy+mr-int(mr*0.12)],fill=(30,40,80,255))
    rnd=random.Random(13)
    for _ in range(6):
        a0=rnd.uniform(0,math.pi*2); dist=rnd.uniform(r*0.65,r*0.88)
        sx=cx+int(dist*math.cos(a0)); sy=cy+int(dist*math.sin(a0))
        d.ellipse([sx-1,sy-1,sx+1,sy+1],fill=(200,210,240,220))
    return im

def _get_bg(w, h, t):
    if t["gen"] == "rezero" and BG_BASE64 is not None:
        try:
            im = _b64_to_image(BG_BASE64)
            if im.mode == "P": im = im.convert("RGB")
            return im.resize((w, h), Image.LANCZOS)
        except Exception:
            return Image.new("RGB", (w, h), tuple(_rgb(t["bg"])))
    if t["gen"] == "rezero" and BG_BASE64 is None:
        return Image.new("RGB", (w, h), tuple(_rgb(t["bg"])))
    return _gen_bg(w, h, t["gen"])

def _get_icon(sz, t):
    w, h = sz
    if t["gen"] == "rezero" and ICON_BASE64 is not None:
        try:
            im = _b64_to_image(ICON_BASE64)
            if im.mode == "P": im = im.convert("RGB")
            return im.resize((w, h), Image.LANCZOS)
        except Exception:
            pass
    if t["gen"] == "rezero" and ICON_BASE64 is None:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy, r = w//2, h//2, min(w, h)//2 - 2
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(100, 140, 200, 255))
        return im
    return _gen_icon(w, t["gen"])

# \u0413\u0420\u0410\u0424\u0418\u041a-\u041f\u041e\u041b\u041e\u0421\u041a\u0410
class GraphOverlay:
    W, H = 140, 24
    def __init__(s, parent, app):
        s.a = app; s._parent = parent; s._drag = False
        s._dx = s._dy = 0; s._dev_ms = 0; s._label = "\u2014"; s._interactive = False
        s._build()
    def _build(s):
        gx, gy = s.a.gpos
        s.root = tk.Toplevel(s._parent)
        s.root.overrideredirect(True); s.root.attributes("-topmost", True)
        s.root.geometry(f"{s.W}x{s.H}+{gx}+{gy}"); s.root.configure(bg="#3a3a3a")
        s.canvas = tk.Canvas(s.root, width=s.W, height=s.H, bg="#3a3a3a",
                             highlightthickness=1, highlightbackground="#555555")
        s.canvas.pack(fill=tk.BOTH, expand=1)
        s._draw(s._dev_ms, s._label); s._apply_mode()
    def _apply_mode(s):
        if s._interactive:
            s.canvas.bind("<ButtonPress-1>", s._on_press)
            s.canvas.bind("<B1-Motion>", s._on_drag)
            s.canvas.bind("<ButtonRelease-1>", s._on_release)
            s.root.configure(cursor="fleur")
        else:
            s.canvas.unbind("<ButtonPress-1>"); s.canvas.unbind("<B1-Motion>")
            s.canvas.unbind("<ButtonRelease-1>"); s.root.configure(cursor="arrow")
    def set_interactive(s, on):
        if s._interactive == on: return
        s._interactive = on; s._apply_mode()
    def _on_press(s, e):
        s._drag = True; s._dx = e.x_root - s.root.winfo_x(); s._dy = e.y_root - s.root.winfo_y()
    def _on_drag(s, e):
        if not s._drag: return
        sw = s.root.winfo_screenwidth(); sh = s.root.winfo_screenheight()
        nx = max(0, min(sw - s.W, e.x_root - s._dx)); ny = max(0, min(sh - s.H, e.y_root - s._dy))
        s.root.geometry(f"+{nx}+{ny}")
    def _on_release(s, e):
        s._drag = False; s.a.gpos = (s.root.winfo_x(), s.root.winfo_y())
    def _draw(s, dev_ms, label):
        if not hasattr(s, 'canvas') or s.canvas is None: return
        s.canvas.delete("all")
        bar_w = s.W - 20; bar_x = 10; bar_y = s.H - 7; bar_h = 4; mid = bar_x + bar_w // 2
        s.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h, fill="#2a2a2a", outline="#555555")
        s.canvas.create_line(mid, bar_y - 1, mid, bar_y + bar_h + 1, fill="#777777", width=1)
        max_dev = 100; ratio = max(-1.0, min(1.0, dev_ms / max_dev))
        bar_len = int(abs(ratio) * (bar_w // 2))
        if ratio >= 0: x1, x2 = mid, mid + bar_len
        else: x1, x2 = mid - bar_len, mid
        if bar_len > 0:
            s.canvas.create_rectangle(x1, bar_y, x2, bar_y + bar_h, fill="#aaaaaa", outline="")
        s.canvas.create_text(bar_x + bar_w // 2, 8, text=label, fill="#cccccc", font=("Segoe UI", 7, "bold"))
    def update_val(s, dev_ms):
        if dev_ms is None: s._dev_ms = 0; s._label = "\u2014"
        else:
            s._dev_ms = dev_ms; sign = "+" if dev_ms >= 0 else "\u2212"
            s._label = f"{sign}{abs(int(dev_ms))}{_t('ms')}"
        s._draw(s._dev_ms, s._label)
    def destroy(s):
        try: s.root.destroy()
        except: pass

# \u0412\u0418\u0414\u0416\u0415\u0422\u042b
class RegionOverlay:
    def __init__(s,parent,r1=None,r2=None,theme=None):
        s.root=tk.Toplevel(parent); s.root.attributes("-fullscreen",1,"-topmost",1); s.root.configure(bg="#000")
        try: s.root.attributes("-transparentcolor","#000")
        except: s.root.attributes("-alpha",0.3)
        cv=tk.Canvas(s.root,bg="#000",highlightthickness=0); cv.pack(fill=tk.BOTH,expand=1)
        t=theme or THEMES["Re:Zero Edition"]
        for r,c,l in [(r1,t["red"],_t("region1_banner")),(r2,t["pink"],_t("region2_banner"))]:
            if not r: continue
            x1,y1,x2,y2=r; cv.create_rectangle(x1,y1,x2,y2,outline=c,width=4,dash=(8,4))
            cv.create_text((x1+x2)//2,max(y1-16,16),text=l,fill=c,font=("Segoe UI",12,"bold"))
            for cx,cy in [(x1,y1),(x2,y1),(x1,y2),(x2,y2)]: cv.create_oval(cx-5,cy-5,cx+5,cy+5,fill=c,outline="white")
    def destroy(s):
        try: s.root.destroy()
        except: pass

class RegionSelector:
    def __init__(s,parent,cb,txt=None,t=None):
        t=t or THEMES["Re:Zero Edition"]; s.cb,s.sx,s.sy,s.rect=cb,0,0,None
        txt=txt or _t("select_area")
        s.root=tk.Toplevel(parent); s.root.attributes("-fullscreen",1,"-alpha",0.3,"-topmost",1)
        s.root.configure(bg=t["bg"]); s.root.protocol("WM_DELETE_WINDOW",s._c)
        s.cv=tk.Canvas(s.root,cursor="cross",bg=t["bg"],highlightthickness=0); s.cv.pack(fill=tk.BOTH,expand=1)
        s.cv.create_text(s.root.winfo_screenwidth()//2,30,text=txt,fill=t["acc"],font=("Segoe UI",16,"bold"))
        s.cv.bind("<ButtonPress-1>",s._p); s.cv.bind("<B1-Motion>",s._d); s.cv.bind("<ButtonRelease-1>",s._r)
        s.root.bind("<Escape>",s._c); s._acc=t["acc"]
    def _c(s,e=None): s.root.destroy()
    def _p(s,e):
        s.sx,s.sy=e.x,e.y
        if s.rect: s.cv.delete(s.rect)
        s.rect=s.cv.create_rectangle(s.sx,s.sy,s.sx,s.sy,outline=s._acc,width=2)
    def _d(s,e): s.cv.coords(s.rect,s.sx,s.sy,e.x,e.y)
    def _r(s,e):
        x1,y1=min(s.sx,e.x),min(s.sy,e.y); x2,y2=max(s.sx,e.x),max(s.sy,e.y)
        if x2-x1>5 and y2-y1>5: s.cb((x1,y1,x2,y2))
        s.root.destroy()

class ReButton(tk.Label):
    def __init__(s,p,txt,cmd,t,fg=None,font=None,bg=None,bg_key=None,fg_key=None,**kw):
        s._bg=bg or t["bb"]; s._ba=t["ba"]; s._fg=fg or t["txt"]; s._txt=txt; s._f=font or ("Segoe UI",10)
        s._tl=False; s._r=12; s._cb=bg is not None; s._bg_key=bg_key; s._fg_key=fg_key
        super().__init__(p,text=txt,bg=s._bg,fg=s._fg,font=s._f,cursor="hand2",padx=12,pady=6,highlightthickness=0,**kw)
        s.bind("<Button-1>",lambda e:cmd()); s.bind("<Enter>",s._en); s.bind("<Leave>",s._lv)
    def _en(s,e=None): s.config(image=s._th) if s._tl and hasattr(s,'_th') else s.config(bg=s._ba)
    def _lv(s,e=None): s.config(image=s._tn) if s._tl and hasattr(s,'_tn') else s.config(bg=s._bg)
    def set_tl(s,n,h): s._tl=1; s._tn,s._th=n,h; s.config(image=n,compound="center",text="",borderwidth=0,highlightthickness=0)
    def clear_tl(s):
        s._tl=0
        for a in ['_tn','_th']:
            if hasattr(s,a): delattr(s,a)
        s.config(image="",text=s._txt,bg=s._bg,fg=s._fg)
    def upd(s,t):
        if s._bg_key: s._bg=t[s._bg_key]; s._ba=t["ba"]
        elif not s._cb: s._bg,s._ba=t["bb"],t["ba"]
        else: s._ba=t["ba"]
        if s._fg_key: s._fg=t[s._fg_key]
        if not s._tl: s.config(bg=s._bg,fg=s._fg)

class ToggleButton(tk.Label):
    IS=56
    def __init__(s,p,t,cb,**kw):
        s.t=t; s.cb=cb; s.running=False; s._ic=s._ic_s=s._ic_p=None; s._bgp=s._ph=None; s._tl=False; s._r=18
        super().__init__(p,bg=t["tsb"],cursor="hand2",padx=12,pady=12,highlightthickness=2,highlightbackground=t["bd"],highlightcolor=t["acc"],**kw)
        s.bind("<Button-1>",lambda e:cb()); s.bind("<Enter>",lambda e:s._en()); s.bind("<Leave>",lambda e:s._lv())
        s._li()
    def _li(s):
        im=_get_icon((s.IS,s.IS),s.t)
        im=im.convert("RGB") if im.mode!="RGB" else im
        s._ic=im; s._ic_s=s._mk_s(im)
        if not s._tl:
            s._ic_p=ImageTk.PhotoImage(s._ic); s.config(image=s._ic_p,compound="center",text="")
    def _mk_s(s,im):
        r,g,b=im.split()
        return Image.merge("RGB",(r.point(lambda x:min(255,int(x*1.4))),g.point(lambda x:int(x*0.5)),b.point(lambda x:int(x*0.5))))
    def _gc(s): return s.t["tob"] if s.running else s.t["tsb"]
    def set_tl(s,bp): s._tl=1; s._bgp=bp; s._rd()
    def clear_tl(s):
        s._tl=0; s._bgp=None; s.config(image="",text="")
        if s._ic:
            s._ic_p=ImageTk.PhotoImage(s._ic_s if s.running else s._ic)
            s.config(image=s._ic_p,compound="center",text="",bg=s._gc(),highlightthickness=2)
    def _rd(s):
        if not s._tl or s._bgp is None: return
        s.update_idletasks()
        x=s.winfo_rootx()-s.master.winfo_toplevel().winfo_rootx()
        y=s.winfo_rooty()-s.master.winfo_toplevel().winfo_rooty()
        w,h=s.winfo_width(),s.winfo_height()
        if w<=1 or h<=1: return
        cr=s._bgp.crop((x,y,x+w,y+h)).convert("RGBA"); r,g,b=_rgb(s._gc())
        res=_rrect(Image.alpha_composite(cr,Image.new("RGBA",(w,h),(r,g,b,60))),s._r)
        bd=Image.new("RGBA",(w,h),(0,0,0,0)); ImageDraw.Draw(bd).rounded_rectangle([0,0,w-1,h-1],radius=s._r,outline=(255,255,255,20),width=1)
        res=Image.alpha_composite(res,bd); ic=s._ic_s if s.running else s._ic
        if ic:
            ir=_rrect(ic.convert("RGBA"),12); res.paste(ir,((w-ir.size[0])//2,(h-ir.size[1])//2),ir)
        s._ph=ImageTk.PhotoImage(res); s.config(image=s._ph,compound="center",text="",highlightthickness=0)
    def _en(s):
        if not s._tl: s.config(bg=s.t["ba"])
    def _lv(s):
        if not s._tl: s.config(bg=s._gc())
    def set_run(s,r):
        s.running=r
        if s._tl: s._rd()
        else:
            if s._ic is not None:
                s._ic_p=ImageTk.PhotoImage(s._ic_s if r else s._ic)
                s.config(image=s._ic_p,compound="center",text="",bg=s._gc())
    def set_file(s,p):
        try:
            im=Image.open(p).resize((s.IS,s.IS),Image.LANCZOS)
            im=im.convert("RGB") if im.mode=="P" else im
            s._ic=im; s._ic_s=s._mk_s(im)
            if s._tl: s._rd()
            else:
                s._ic_p=ImageTk.PhotoImage(s._ic); s.config(image=s._ic_p,compound="center")
            return True
        except: return False
    def upd(s,t):
        s.t=t; s.config(image="",text=""); s._ic=s._ic_s=s._ic_p=None
        if not s._tl:
            s.config(bg=s._gc(),highlightbackground=t["bd"],highlightcolor=t["acc"]); s._li()
        else:
            s.config(highlightbackground=t["bd"],highlightcolor=t["acc"]); s._li(); s._rd()

# \u041d\u0410\u0421\u0422\u0420\u041e\u0419\u041a\u0418
class Settings:
    def __init__(s,app):
        s.a=app
        s.root=tk.Toplevel(app.root); s.root.title(_t("settings_title")); s.root.geometry("540x860"); s.root.resizable(0,0)
        s.root.configure(bg=app.t["bg"]); s.root.protocol("WM_DELETE_WINDOW",s._cl); s.root.transient(app.root)
        s.t=app.t; s.st=ttk.Style(); s._b()
        if s.a.graph: s.a.graph.set_interactive(True)
    def _mf(s,p,title,tc=None):
        t=s.t; f=tk.Frame(p,bg=t["fbg"],highlightthickness=1,highlightbackground=t["bd"],bd=0)
        bar=tk.Frame(f,bg=t["fbg"],height=28); bar.pack(fill="x")
        tk.Label(bar,text=f"  \u2726 {title}",bg=t["fbg"],fg=tc or t["acc"],font=("Segoe UI",10,"bold"),anchor="w").pack(side="left",padx=4,pady=4)
        return f
    def _b(s):
        t,r=s.t,s.root
        tk.Label(r,text=_t("settings"),bg=t["bg"],fg=t["hdr"],font=("Segoe UI",16,"bold")).pack(pady=10)
        tk.Frame(r,bg=t["bd"],height=2).pack(fill="x",padx=20,pady=4)
        f=s._mf(r,_t("language")); f.pack(fill="x",padx=14,pady=4)
        rr=tk.Frame(f,bg=t["fbg"]); rr.pack(pady=6,padx=10,fill="x")
        for code,name in LANG_NAMES:
            lb=("\u2714 " if code==s.a.lang else "")+name
            b=tk.Label(rr,text=lb,bg=t["bb"],fg=t["txt"],font=("Segoe UI",9,"bold"),cursor="hand2",padx=10,pady=4,highlightthickness=1,highlightbackground=t["bd"])
            b.pack(side="left",padx=4); b.bind("<Button-1>",lambda e,c=code:s._sl(c))
            b.bind("<Enter>",lambda e,w=b:w.config(bg=t["ba"])); b.bind("<Leave>",lambda e,w=b:w.config(bg=t["bb"]))
        f=s._mf(r,_t("theme")); f.pack(fill="x",padx=14,pady=4)
        rr=tk.Frame(f,bg=t["fbg"]); rr.pack(pady=6,padx=10,fill="x")
        for n in THEMES:
            lb=("\u2714 " if n==s.a.ctn else "")+_theme_name(n)
            b=tk.Label(rr,text=lb,bg=t["bb"],fg=t["txt"],font=("Segoe UI",9,"bold"),cursor="hand2",padx=10,pady=4,highlightthickness=1,highlightbackground=t["bd"])
            b.pack(side="left",padx=4); b.bind("<Button-1>",lambda e,n=n:s._st(n))
            b.bind("<Enter>",lambda e,w=b:w.config(bg=t["ba"])); b.bind("<Leave>",lambda e,w=b:w.config(bg=t["bb"]))
        f=s._mf(r,_t("interval")); f.pack(fill="x",padx=14,pady=4)
        rr=tk.Frame(f,bg=t["fbg"]); rr.pack(pady=6,padx=10)
        mk=lambda to: tk.Spinbox(rr,from_=0,to=to,width=4,bg=t["eb"],fg=t["txt"],insertbackground=t["acc"],font=("Segoe UI",10),relief="flat",buttonbackground=t["bb"],highlightthickness=1,highlightbackground=t["bd"],selectbackground=t["ba"])
        for lb,to,attr in [(_t("min"),59,"sp_min"),(_t("sec"),59,"sp_sec"),(_t("ms"),999,"sp_ms")]:
            tk.Label(rr,text=lb,bg=t["fbg"],fg=t["txt"],font=("Segoe UI",9)).pack(side="left",padx=3)
            w=mk(to); w.pack(side="left",padx=3); setattr(s,attr,w)
        c=s.a.iv
        s.sp_min.delete(0,"end"); s.sp_min.insert(0,str(int(c//60)))
        s.sp_sec.delete(0,"end"); s.sp_sec.insert(0,str(int(c%60)))
        s.sp_ms.delete(0,"end"); s.sp_ms.insert(0,str(int((c-int(c))*1000)))
        f=s._mf(r,_t("antibot"),t["acc2"]); f.pack(fill="x",padx=14,pady=4)
        rr=tk.Frame(f,bg=t["fbg"]); rr.pack(pady=6,padx=10,fill="x")
        s.var_rnd=tk.BooleanVar(value=s.a.rnd)
        tk.Label(rr,text=_t("antibot_desc"),bg=t["fbg"],fg=t["dim"],font=("Segoe UI",9)).pack(side="left",padx=4)
        tk.Checkbutton(rr,variable=s.var_rnd,bg=t["fbg"],fg=t["txt"],
            activebackground=t["fbg"],activeforeground=t["acc2"],
            selectcolor=t["eb"],font=("Segoe UI",9),highlightthickness=0,bd=0,
            command=s._toggle_rnd).pack(side="left",padx=4)
        rr2=tk.Frame(f,bg=t["fbg"]); rr2.pack(pady=2,padx=10,fill="x")
        tk.Label(rr2,text=_t("graph_hint"),bg=t["fbg"],fg=t["dim"],font=("Segoe UI",8,"italic")).pack(side="left",padx=4)
        f=s._mf(r,_t("show_regions"),t["acc2"]); f.pack(fill="x",padx=14,pady=4)
        rr=tk.Frame(f,bg=t["fbg"]); rr.pack(pady=4,padx=10,fill="x")
        tk.Label(rr,text=_t("key_label"),bg=t["fbg"],fg=t["txt"],font=("Segoe UI",9)).pack(side="left",padx=4)
        s.e_show=tk.Entry(rr,width=14,bg=t["eb"],fg=t["txt"],insertbackground=t["acc2"],font=("Segoe UI",10),relief="flat",highlightthickness=1,highlightbackground=t["bd"])
        s.e_show.pack(side="left",padx=4); s.e_show.insert(0,s.a.sk)
        f=s._mf(r,_t("threshold")); f.pack(fill="x",padx=14,pady=4)
        rr=tk.Frame(f,bg=t["fbg"]); rr.pack(pady=6,padx=10,fill="x")
        try: s.st.configure("Themed.Horizontal.TScale",background=t["sfg"],troughcolor=t["str3"],darkcolor=t["str3"],lightcolor=t["str3"],bordercolor=t["bd"],focuscolor=t["sfg"])
        except: pass
        s.sv=tk.DoubleVar(value=s.a.th); s.sc=ttk.Scale(rr,from_=0.50,to=1.00,orient="horizontal",variable=s.sv,style="Themed.Horizontal.TScale",length=380)
        s.sc.pack(side="left",padx=4,fill="x",expand=1)
        s.lb_th=tk.Label(rr,text=f"{int(s.a.th*100)} %",bg=t["fbg"],fg=t["gold"],font=("Segoe UI",10,"bold")); s.lb_th.pack(side="left",padx=8)
        s.sc.config(command=lambda v:s.lb_th.config(text=f"{int(float(v)*100)} %"))
        f=s._mf(r,_t("bg_image"),t["acc2"]); f.pack(fill="x",padx=14,pady=4)
        r1=tk.Frame(f,bg=t["fbg"]); r1.pack(pady=3,padx=10,fill="x")
        tk.Label(r1,text=_t("bg_label"),bg=t["fbg"],fg=t["txt"],font=("Segoe UI",9)).pack(side="left",padx=4)
        ReButton(r1,_t("from_file"),s._bf,t).pack(side="left",padx=2)
        ReButton(r1,_t("reset"),s._br,t).pack(side="left",padx=2)
        f=s._mf(r,_t("icon_button"),t["acc2"]); f.pack(fill="x",padx=14,pady=4)
        r2=tk.Frame(f,bg=t["fbg"]); r2.pack(pady=3,padx=10,fill="x")
        tk.Label(r2,text=_t("icon_label"),bg=t["fbg"],fg=t["txt"],font=("Segoe UI",9)).pack(side="left",padx=4)
        ReButton(r2,_t("from_file"),s._if,t).pack(side="left",padx=2)
        ReButton(r2,_t("reset"),s._ir,t).pack(side="left",padx=2)
    def _sl(s, code):
        s._save()
        global _LANG
        _LANG = code; s.a.lang = code
        _save_cfg({"lang": code})
        s.a.sw=None; s.root.destroy(); s.a._at(); s.a._os()
    def _toggle_rnd(s):
        if s.var_rnd.get():
            s.a.rnd = True
            if not s.a.graph:
                s.a.graph = GraphOverlay(s.a.root, s.a); s.a.graph.set_interactive(True)
        else:
            s.a.rnd = False
            if s.a.graph: s.a.graph.destroy(); s.a.graph = None
    def _save(s):
        try: m,sc,ms=int(s.sp_min.get()),int(s.sp_sec.get()),int(s.sp_ms.get())
        except: m,sc,ms=0,1,0
        s.a.iv=max(m*60+sc+ms/1000.0,0.05)
        k=_norm_key(s.e_show.get())
        if k and k not in s.a.FK: s.a.sk=k; s.a._rh()
        s.a.th=float(s.sv.get()); s.a.rnd=s.var_rnd.get()
    def _st(s,n):
        s._save(); s.a._st(n); s.a.sw=None; s.root.destroy(); s.a._os()
    def _bf(s):
        p=filedialog.askopenfilename(title=_t("select_bg"),filetypes=[("Images","*.png *.jpg *.jpeg *.gif *.bmp *.webp")])
        if p: s.a._bgf(p)
    def _br(s): s.a._lb(); s.a._at()
    def _if(s):
        p=filedialog.askopenfilename(title=_t("select_icon"),filetypes=[("Images","*.png *.jpg *.jpeg *.gif *.bmp *.webp")])
        if p: s.a.tb.set_file(p)
    def _ir(s): s.a.tb._li()
    def _cl(s):
        s._save()
        if s.a.graph: s.a.graph.set_interactive(False)
        s.a.sw=None; s.root.destroy()

# \u041f\u0420\u0418\u041b\u041e\u0416\u0415\u041d\u0418\u0415
class App:
    FK={"windows","win","super","meta","left windows","right windows"}
    W=560
    LINKS=[("poe.ninja \u2014 Forbidden Rites","https://poe.ninja/poe2/builds/forbiddenrites"),
           ("Craft of Exile","https://www.craftofexile.com/?game=poe2"),
           ("poe2db.tw","https://poe2db.tw/ru/")]
    def __init__(s):
        global _LANG
        cfg=_load_cfg()
        s.lang=cfg.get("lang","RU")
        _LANG=s.lang
        s.root=tk.Tk()
        _set_app_icon(s.root)
        s.root.title("AutoKey")
        s.root.geometry(f"{s.W}x640"); s.root.resizable(0,0)
        s.ctn="Re:Zero Edition"; s.t=THEMES[s.ctn]
        s.r1=s.r2=s.ref1=s.ref2=None
        s.pk,s.tk,s.sk="f1","f10","f8"
        s.iv,s.th=1.0,0.85; s.running=s.pr=False; s.ev=threading.Event()
        s.rnd=False; s.gpos=(20,0); s.graph=None
        s.ov=None; s.bl=False; s._hk=None; s._t1=s._t2=False; s.sw=None
        s._tk_sc=set(); s._sk_sc=set()
        s._q=_q.Queue(); s.bp=s.bph=s.blbl=None; s.bi=s.bnlbl=None
        s._st_key="stopped"
        s._ui(); s._at(); s._rh()
        s.root.update_idletasks()
        sh = s.root.winfo_screenheight()
        s.gpos = (20, sh - GraphOverlay.H - 20)
        s.root.after(50, s._poll)
    def _ui(s):
        r,t=s.root,s.t
        s.blbl=tk.Label(r); s.blbl.place(x=0,y=0,relwidth=1,relheight=1); s.blbl.lower()
        top=tk.Frame(r,bg=t["bg"]); top.pack(fill="x",pady=(8,2))
        tf=tk.Frame(top,bg=t["bg"]); tf.pack(side="left",padx=14)
        s.lh=tk.Label(tf,text=_t("header"),bg=t["bg"],fg=t["hdr"],font=("Segoe UI",18,"bold")); s.lh.pack()
        s.ls=tk.Label(tf,text=_theme_name(s.ctn),bg=t["bg"],fg=t["sub"],font=("Segoe UI",9,"italic")); s.ls.pack()
        s.gr=tk.Label(top,text="\u2699",bg=t["bg"],fg=t["gr"],font=("Segoe UI",22),cursor="hand2"); s.gr.pack(side="right",padx=14)
        s.gr.bind("<Button-1>",lambda e:s._os()); s.gr.bind("<Enter>",lambda e:s.gr.config(fg=t["acc"])); s.gr.bind("<Leave>",lambda e:s.gr.config(fg=t["gr"]))
        tk.Frame(r,bg=t["bd"],height=2).pack(fill="x",padx=20,pady=4)
        s.lr1t=tk.Label(r,text=_t("region1"),bg=t["bg"],fg=t["red"],font=("Segoe UI",11,"bold"),cursor="hand2")
        s.lr1t.pack(pady=(6,1)); s.lr1t.bind("<Button-1>",lambda e:s._sr1())
        s.lr1=tk.Label(r,text=_t("not_selected"),bg=t["bg"],fg=t["dim"],font=("Segoe UI",9)); s.lr1.pack(pady=1)
        s.lr2t=tk.Label(r,text=_t("region2"),bg=t["bg"],fg=t["pink"],font=("Segoe UI",11,"bold"),cursor="hand2")
        s.lr2t.pack(pady=(6,1)); s.lr2t.bind("<Button-1>",lambda e:s._sr2())
        s.lr2=tk.Label(r,text=_t("not_selected"),bg=t["bg"],fg=t["dim"],font=("Segoe UI",9)); s.lr2.pack(pady=1)
        kr=tk.Frame(r,bg=t["bg"]); kr.pack(pady=6)
        s.lk=tk.Label(kr,text=_t("key_label"),bg=t["bg"],fg=t["txt"],font=("Segoe UI",9)); s.lk.pack(side="left",padx=4)
        s.ek=tk.Entry(kr,width=14,bg=t["eb"],fg=t["txt"],insertbackground=t["acc"],font=("Segoe UI",10),relief="flat",highlightthickness=1,highlightbackground=t["bd"])
        s.ek.pack(side="left",padx=4); s.ek.insert(0,"f1")
        s.bk=ReButton(kr,"\u2713",s._apk,t,fg=t["bg"],bg=t["acc"],bg_key="acc",fg_key="bg",font=("Segoe UI",13,"bold"))
        s.bk.pack(side="left",padx=4)
        tr=tk.Frame(r,bg=t["bg"]); tr.pack(pady=4)
        s.ltst=tk.Label(tr,text=_t("startstop_label"),bg=t["bg"],fg=t["txt"],font=("Segoe UI",9)); s.ltst.pack(side="left",padx=4)
        s.et=tk.Entry(tr,width=14,bg=t["eb"],fg=t["txt"],insertbackground=t["acc2"],font=("Segoe UI",10),relief="flat",highlightthickness=1,highlightbackground=t["bd"])
        s.et.pack(side="left",padx=4); s.et.insert(0,"f10")
        s.bt=ReButton(tr,"\u2713",s._atk,t,fg=t["bg"],bg=t["acc"],bg_key="acc",fg_key="bg",font=("Segoe UI",13,"bold"))
        s.bt.pack(side="left",padx=4)
        s.tb=ToggleButton(r,t,s._tg); s.tb.pack(anchor="center",pady=8)
        s.lst=tk.Label(r,text=_t("stopped"),bg=t["bg"],fg=t["soff"],font=("Segoe UI",12,"bold")); s.lst.pack(pady=4)
        s.lhi=tk.Label(r,text=_t("hint"),bg=t["bg"],fg=t["dim"],font=("Segoe UI",8),justify="center"); s.lhi.pack(pady=4)
        s.bf=tk.Frame(r,bg=t["bg"]); s.bf.pack(fill="x",padx=14,pady=2)
        s.bnlbl=tk.Label(s.bf,bg=t["bg"],cursor="hand2"); s.bnlbl.pack(pady=2); s.bnlbl.bind("<Button-1>",lambda e:s._bc())
        tk.Frame(r,bg=t["bd"],height=2).pack(fill="x",padx=20,pady=4)
        s.lft=tk.Label(r,text=_t("footer"),bg=t["bg"],fg=t["ftr"],font=("Segoe UI",8,"italic")); s.lft.pack(pady=2)
    def _lb(s):
        s.root.update_idletasks(); w,h=s.root.winfo_width(),s.root.winfo_height()
        w=s.W if w<10 else w; h=640 if h<10 else h
        im=_get_bg(w,h,s.t); im=im.convert("RGB") if im.mode!="RGB" else im; s.bp=im; s.bph=ImageTk.PhotoImage(im)
        s.blbl.config(image=s.bph); s.blbl.place(x=0,y=0,relwidth=1,relheight=1); s.blbl.lower()
    def _lbn(s):
        im=_gen_banner(s.W-28,70); s.bi=ImageTk.PhotoImage(im); s.bnlbl.config(image=s.bi)
    def _bc(s):
        if not s.t.get("has_banner"): return
        t=s.t; m=tk.Menu(s.root,tearoff=0,bg=t["fbg"],fg=t["txt"],activebackground=t["ba"],activeforeground=t["acc"],font=("Segoe UI",10))
        for lb,u in s.LINKS: m.add_command(label=lb,command=lambda u=u:webbrowser.open(u))
        m.tk_popup(s.bnlbl.winfo_rootx(),s.bnlbl.winfo_rooty()+s.bnlbl.winfo_height()); m.grab_release()
    def _bgf(s,p):
        try:
            s.root.update_idletasks(); w,h=s.root.winfo_width(),s.root.winfo_height()
            im=Image.open(p).resize((w,h),Image.LANCZOS); im=im.convert("RGB") if im.mode!="RGB" else im
            s.bp=im; s.bph=ImageTk.PhotoImage(im); s.blbl.config(image=s.bph); s.blbl.place(x=0,y=0,relwidth=1,relheight=1); s.blbl.lower()
            s._at()
        except: pass
    def _os(s):
        if s.sw:
            try: s.sw.root.lift(); return
            except: pass
        s.sw=Settings(s)
    def _st(s,n): s.ctn=n; s.t=THEMES[n]; s._at()
    def _at(s):
        t=s.t; s.root.config(bg=t["bg"]); s._lb()
        s.lh.config(text=_t("header"),bg=t["bg"],fg=t["hdr"])
        s.ls.config(text=_theme_name(s.ctn),bg=t["bg"],fg=t["sub"])
        s.gr.config(bg=t["bg"],fg=t["gr"])
        s.lr1t.config(text=_t("region1"),bg=t["bg"],fg=t["red"])
        s.lr2t.config(text=_t("region2"),bg=t["bg"],fg=t["pink"])
        if s.r1:
            x1,y1,x2,y2=s.r1
            s.lr1.config(text=f"{x1},{y1} \u2014 {x2},{y2}  {x2-x1}x{y2-y1}",bg=t["bg"],fg=t["red"])
        else:
            s.lr1.config(text=_t("not_selected"),bg=t["bg"],fg=t["dim"])
        if s.r2:
            x1,y1,x2,y2=s.r2
            s.lr2.config(text=f"{x1},{y1} \u2014 {x2},{y2}  {x2-x1}x{y2-y1}",bg=t["bg"],fg=t["pink"])
        else:
            s.lr2.config(text=_t("not_selected"),bg=t["bg"],fg=t["dim"])
        s.lk.config(text=_t("key_label"),bg=t["bg"],fg=t["txt"])
        s.ek.config(bg=t["eb"],fg=t["txt"],insertbackground=t["acc"],highlightbackground=t["bd"])
        s.ltst.config(text=_t("startstop_label"),bg=t["bg"],fg=t["txt"])
        s.et.config(bg=t["eb"],fg=t["txt"],insertbackground=t["acc2"],highlightbackground=t["bd"])
        for b in [s.bk,s.bt]: b.clear_tl(); b.upd(t)
        s.tb.clear_tl(); s.tb.upd(t)
        st_key=getattr(s,'_st_key','stopped')
        c=t["sstop"] if s.running and s.bl else (t["son"] if s.running and s.pr else (t["swait"] if s.running else t["soff"]))
        s.lst.config(text=_t(st_key),bg=t["bg"],fg=c)
        s.lhi.config(text=_t("hint"),bg=t["bg"],fg=t["dim"])
        s.lft.config(text=_t("footer"),bg=t["bg"],fg=t["ftr"])
        s.bf.config(bg=t["bg"])
        if t.get("has_banner"): s.bnlbl.pack(pady=2); s.bnlbl.config(bg=t["bg"],cursor="hand2"); s._lbn()
        else: s.bnlbl.pack_forget()
        s.root.update(); s.root.after(100,s._at2)
    def _at2(s):
        if not s.t.get("has_bg") or s.bp is None: return
        s.root.update_idletasks()
        def cb(x,y,w,h,c,a,r):
            if s.bp is None or w<=1: return None
            cr=s.bp.crop((x,y,x+w,y+h)).convert("RGBA"); r2,g,b=_rgb(c)
            return _rrect(Image.alpha_composite(cr,Image.new("RGBA",(w,h),(r2,g,b,int(255*a)))),r)
        s.tb.set_tl(s.bp)
        for b in [s.bk,s.bt]:
            if b._cb: continue
            b.update_idletasks()
            x=b.winfo_rootx()-s.root.winfo_rootx(); y=b.winfo_rooty()-s.root.winfo_rooty()
            w,h=b.winfo_width(),b.winfo_height()
            n=cb(x,y,w,h,s.t["bb"],s.t.get("baa",0.15),b._r); h2=cb(x,y,w,h,s.t["ba"],s.t.get("baa",0.15),b._r)
            if n and h2: b.set_tl(n,h2)
    @staticmethod
    def _g(r): x1,y1,x2,y2=r; return np.array(ImageGrab.grab(bbox=(x1,y1,x2,y2)))
    @staticmethod
    def _sim(ref,cur):
        if ref is None or cur is None or ref.shape!=cur.shape: return 0.0
        return 1.0-np.abs(ref.astype(np.int16)-cur.astype(np.int16)).mean()/255.0
    def _poll(s):
        try:
            while True:
                item = s._q.get_nowait()
                tag = item[0]
                if tag == 'toggle': s._tg()
                elif tag == 'show': s._sr()
                elif tag == 'hide': s._hr()
                elif tag == 'status': s.lst.config(text=_t(item[1]), fg=s.t.get(item[2], "#666688"))
                elif tag == 'graph':
                    if s.graph: s.graph.update_val(item[1])
        except _q.Empty: pass
        s.root.after(50, s._poll)
    def _st_(s, key, ck="soff"):
        s._st_key = key
        s._q.put(('status', key, ck))
    def _sr1(s):
        s.root.withdraw(); s.root.update(); time.sleep(0.2)
        def cb(c):
            s.r1=c; s.ref1=s._g(c); x1,y1,x2,y2=c
            s.lr1.config(text=f"{x1},{y1} \u2014 {x2},{y2}  {x2-x1}x{y2-y1}",fg=s.t["red"])
        sel=RegionSelector(s.root,cb,_t("select_r1"),s.t)
        s.root.wait_window(sel.root); s.root.deiconify()
    def _sr2(s):
        s.root.withdraw(); s.root.update(); time.sleep(0.2)
        def cb(c):
            s.r2=c; s.ref2=s._g(c); x1,y1,x2,y2=c
            s.lr2.config(text=f"{x1},{y1} \u2014 {x2},{y2}  {x2-x1}x{y2-y1}",fg=s.t["pink"])
        sel=RegionSelector(s.root,cb,_t("select_r2"),s.t)
        s.root.wait_window(sel.root); s.root.deiconify()
    def _rh(s):
        if s._hk:
            try: keyboard.unhook(s._hk)
            except: pass
        s._t1=s._t2=False
        s._tk_sc=_key_scancodes(s.tk); s._sk_sc=_key_scancodes(s.sk)
        try: s._hk=keyboard.hook(s._ok)
        except Exception as ex: print(f"Keyboard hook failed: {ex}"); s._hk=None
    def _ok(s,e):
        kn=e.name.lower() if e.name else ""
        sc=getattr(e,'scan_code',None)
        is_tg = (kn==s.tk) or (sc is not None and sc in s._tk_sc)
        is_sh = (kn==s.sk) or (sc is not None and sc in s._sk_sc)
        if is_tg:
            if e.event_type==keyboard.KEY_DOWN:
                if not s._t1: s._t1=True; s._q.put(('toggle',))
            else: s._t1=False
        elif is_sh:
            if e.event_type==keyboard.KEY_DOWN:
                if not s._t2: s._t2=True; s._q.put(('show',))
            else: s._t2
    def _ok(s,e):
        kn=e.name.lower() if e.name else ""
        sc=getattr(e,'scan_code',None)
        is_tg = (kn==s.tk) or (sc is not None and sc in s._tk_sc)
        is_sh = (kn==s.sk) or (sc is not None and sc in s._sk_sc)
        if is_tg:
            if e.event_type==keyboard.KEY_DOWN:
                if not s._t1: s._t1=True; s._q.put(('toggle',))
            else: s._t1=False
        elif is_sh:
            if e.event_type==keyboard.KEY_DOWN:
                if not s._t2: s._t2=True; s._q.put(('show',))
            else: s._t2=False; s._q.put(('hide',))
    def _apk(s):
        k=_norm_key(s.ek.get())
        if not k: return
        if k in s.FK: messagebox.showwarning(_t("warning"),_t("win_key_err")); return
        s.pk=k; s.ek.delete(0,"end"); s.ek.insert(0,k)
    def _atk(s):
        k=_norm_key(s.et.get())
        if not k: return
        if k in s.FK: messagebox.showwarning(_t("warning"),_t("win_key_err")); return
        s.tk=k; s.et.delete(0,"end"); s.et.insert(0,k); s._rh()
    def _sr(s):
        if s.ov or (s.r1 is None and s.r2 is None): return
        s.ov=RegionOverlay(s.root,s.r1,s.r2,s.t)
    def _hr(s):
        if s.ov: s.ov.destroy(); s.ov=None
    def _tg(s): s._stop() if s.running else s._start()
    def _start(s):
        if s.running: return
        if s.r1 is None: messagebox.showwarning(_t("warning"),_t("select_r1_first")); return
        k=_norm_key(s.ek.get())
        if not k: messagebox.showwarning(_t("warning"),_t("enter_key")); return
        if k in s.FK: messagebox.showwarning(_t("warning"),_t("win_key_err")); return
        s.pk=k; s.ek.delete(0,"end"); s.ek.insert(0,k)
        s.running=True; s.ev.clear(); s.tb.set_run(True)
        s._st_("waiting","swait")
        threading.Thread(target=s._lp,daemon=True).start()
    def _stop(s):
        if not s.running: return
        s.running=False; s.ev.set()
        if s.pr:
            try: keyboard.release(s.pk)
            except: pass
            s.pr=False
        s.tb.set_run(False); s._st_("stopped","soff")
    def _lp(s):
        while s.running and not s.ev.is_set():
            bl=False
            if s.r2 and s.ref2 is not None:
                if s._sim(s.ref2,s._g(s.r2))<s.th: bl=True
            s.bl=bl
            if bl:
                if s.pr:
                    s.pr=False
                    try: keyboard.release(s.pk)
                    except: pass
                s._st_("paused","sstop")
                if s.rnd and s.graph: s._q.put(('graph', None))
                s.ev.wait(0.15); continue
            if s._sim(s.ref1,s._g(s.r1))>=s.th:
                if not s.pr:
                    s.pr=True; s._st_("pressing","son")
                try:
                    keyboard.press(s.pk); time.sleep(0.05); keyboard.release(s.pk)
                except: pass
                wt=s.iv
                if s.rnd:
                    dev = random.uniform(-0.1, 0.1)
                    wt=max(0.05, s.iv+dev)
                    s._q.put(('graph', int(dev*1000)))
                s.ev.wait(wt)
            else:
                if s.pr:
                    s.pr=False
                    try: keyboard.release(s.pk)
                    except: pass
                s._st_("waiting","swait")
                if s.rnd and s.graph: s._q.put(('graph', None))
                s.ev.wait(0.1)
    def run(s):
        s.root.protocol("WM_DELETE_WINDOW",s._cl); s.root.mainloop()
    def _cl(s):
        s._stop(); s._hr()
        if s.graph: s.graph.destroy(); s.graph=None
        try: keyboard.unhook_all()
        except: pass
        s.root.destroy()

if __name__=="__main__":
    App().run()
