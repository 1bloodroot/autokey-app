import os
import sys
import re

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    emb_path = os.path.join(script_dir, "embedded_images.py")
    autokey_path = os.path.join(script_dir, "autokey.py")

    if not os.path.exists(emb_path):
        print("Error: embedded_images.py not found.")
        sys.exit(1)
    if not os.path.exists(autokey_path):
        print("Error: autokey.py not found.")
        sys.exit(1)

    sys.path.insert(0, script_dir)
    try:
        import embedded_images
    except Exception as e:
        print(f"Error: cannot import embedded_images.py: {e}")
        sys.exit(1)

    bg = getattr(embedded_images, "BG_BASE64", None)
    icon = getattr(embedded_images, "ICON_BASE64", None)
    app_icon = getattr(embedded_images, "APP_ICON_BASE64", None)

    if not bg or not icon or not app_icon:
        print("Warning: one or more base64 variables are missing or empty.")

    with open(autokey_path, "r", encoding="utf-8") as f:
        src = f.read()

    old_block = re.compile(
        r'BG_BASE64\s*=\s*None\s*\n'
        r'ICON_BASE64\s*=\s*None\s*\n'
        r'APP_ICON_BASE64\s*=\s*None\s*\n'
        r'try:\s*\n'
        r'\s*from\s+embedded_images\s+import\s+BG_BASE64,\s*ICON_BASE64,\s*APP_ICON_BASE64\s*\n'
        r'except\s+ImportError:\s*\n'
        r'\s*pass\s*\n',
        re.MULTILINE
    )

    if not old_block.search(src):
        print("Error: could not find the import block in autokey.py.")
        sys.exit(1)

    def make_assignment(name, value):
        if value is None:
            return f"{name} = None"
        return f'{name} = """{value}"""'

    new_block = (
        make_assignment("BG_BASE64", bg) + "\n" +
        make_assignment("ICON_BASE64", icon) + "\n" +
        make_assignment("APP_ICON_BASE64", app_icon) + "\n"
    )

    new_src = old_block.sub(new_block, src)

    backup_path = autokey_path + ".bak"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"Backup saved: {backup_path}")

    with open(autokey_path, "w", encoding="utf-8") as f:
        f.write(new_src)
    print("Done: images from embedded_images.py are now inlined into autokey.py.")
    print("You can now run autokey.py without embedded_images.py.")

if __name__ == "__main__":
    main()
