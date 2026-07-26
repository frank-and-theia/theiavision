#!/usr/bin/env python3
from PIL import Image

img = Image.open('/root/.openclaw/media/inbound/file_127---98e9bc40-dfe0-4b8b-b3e2-2fc9a71ce693.jpg')
img = img.resize((48, 36))  # Format portrait pour les roses
img_gray = img.convert('L')

# Palette F - Gepeto (10 niveaux)
palette = ['@', '#', '*', '+', '=', '-', ':', '.', '·', ' ']

lines = []
for y in range(36):
    line = ""
    for x in range(48):
        gray = img_gray.getpixel((x, y))
        idx = int((gray / 255) * 9)
        idx = max(0, min(idx, 9))
        line += palette[idx]
    lines.append(line)

result = '\n'.join(lines)
print(result)
