# AutoKey

**AutoKey** — automated key-press tool with screen region monitoring.  
Multi-language UI (RU, EN, DE, ZH, JA), three visual themes, Re:Zero-inspired design.

---

## Download


| Platform    | What to download | How to run                                         |
|-------------|------------------|----------------------------------------------------|
| **Windows** | `AutoKey.exe`    | Double-click                                       |
| **Linux**   | Source files     | `python3 setup_images.py` → `python3 autokey.py` |
| **macOS**   | Source files     | `python3 setup_images.py` → `python3 autokey.py` |


All files are on the [Releases](https://github.com/1bloodroot/autokey-app/releases) page.

---

## Windows

1. Download `AutoKey.exe` from [Releases](https://github.com/1bloodroot/autokey-app/releases).
2. Double-click to run.


If SmartScreen warns, click **More info → Run anyway**.

No installation, no Python, no dependencies — just run the `.exe`.

---

## Linux

### 1. Install system dependencies

```bash
sudo apt install python3-tk scrot  
pip3 install keyboard Pillow numpy  
2. Download source files  
Download these files from  and place them in the same folder:  
  
autokey.py  
embedded_images.py  
setup_images.py  
icon.ico  
3. Inline images  
bash  
python3 setup_images.py  
This embeds the images from embedded_images.py directly into autokey.py. A backup of the original autokey.py is saved as autokey.py.bak. After this step, embedded_images.py is no longer needed.  
  
4. Run  
bash  
python3 autokey.py  
Permissions  
The keyboard library requires access to input devices. If hotkeys don't register:  
  
bash  
sudo usermod -aG input 
```

 
