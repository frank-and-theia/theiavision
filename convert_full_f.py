#!/usr/bin/env python3
from PIL import Image

img = Image.open('/tmp/visage_proche.jpg')
img = img.resize((64, 36))
img_gray = img.convert('L')

# Palette F - Gepeto (10 niveaux) : @ # * + = - : . ·
palette = ['@', '#', '*', '+', '=', '-', ':', '.', '·', ' ']

lines = []
for y in range(36):
    line = ""
    for x in range(64):
        gray = img_gray.getpixel((x, y))
        idx = int((gray / 255) * 9)  # 0-9 pour 10 niveaux
        idx = max(0, min(idx, 9))
        line += palette[idx]
    lines.append(line)

result = '\n'.join(lines)
print(result)

with open('/tmp/visage_full_palette_f.txt', 'w') as f:
    f.write(result)
