# AutoKey — Automation Utility (Re:Zero Edition)

> ⚠️ **Warning:** This tool uses low-level keyboard hooks and overlays. Antivirus software may flag it as suspicious. This is expected behavior for automation utilities. Use at your own risk. Comply with the Terms of Service of any game or application you automate.

AutoKey is a Python + Tkinter application for automating simple actions in games and interfaces: auto-clicking, screen region monitoring, timing deviation graph, and quick links to PoE2 resources. The “Re:Zero Edition” theme and additional styles are included in the build.

---

## ✨ Features

- **Auto-click** with configurable interval (minutes, seconds, milliseconds).
- **Random timing spread (anti-bot)** — ±100 ms from the set interval for more natural behavior.
- **Two screen regions**: Region 1 (trigger) and Region 2 (stop).
- **Deviation graph overlay** (draggable with mouse) to visualize timing variance.
- **Quick links to PoE2 resources** (poe.ninja, Craft of Exile, poe2db.tw) — click the banner at the bottom of the Re:Zero theme to open a small window and enter a character name to get STATS and damage info.
- **Multilingual support**: Russian, English, German, Chinese, Japanese.
- **Themes**: Re:Zero Edition, Night, Light.
- **Embedded images via base64** — no external downloads on startup; previously loaded images aren’t re-downloaded unless the URL changes.
- **Config persistence**: language, theme, regions, thresholds, and keys are saved to `.autokey_config.json`.

---

## 📋 Requirements

### System

- **OS**: Windows (required due to low-level keyboard hooks).
- **Python version**: 3.9–3.12.
- **Privileges**: Administrator rights are required when running the app, because the `keyboard` library needs elevated permissions to intercept key presses.

### Dependencies

All dependencies are listed in `requirements.txt`:

```txt
keyboard>=0.13.5
Pillow>=9.0.0
numpy>=1.21.0
