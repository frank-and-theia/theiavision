#!/usr/bin/env python3
"""
Test de palettes pour TheiaVision
Compare différents jeux de caractères sur la même zone
"""

from PIL import Image

def extract_zone(image_path, x, y, w, h):
    """Extrait une zone de l'image."""
    img = Image.open(image_path)
    return img.crop((x, y, x+w, y+h))

def convert_with_palette(img, palette, levels):
    """Convertit avec une palette personnalisée."""
    if img.mode != 'L':
        img = img.convert('L')
    
    width, height = img.size
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            gray = img.getpixel((x, y))
            idx = int((gray / 255) * (levels - 1))
            idx = max(0, min(idx, levels - 1))
            line += palette[idx]
        lines.append(line)
    return '\n'.join(lines)

# Charger l'image et extraire zone visage (centre)
img = Image.open('/tmp/visage_proche.jpg')
w, h = img.size
# Zone centrale 24x18 (yeux + nez)
zone = img.crop((w//2 - 12, h//3, w//2 + 12, h//3 + 18))
zone_gray = zone.convert('L')

# Définir les palettes à tester
palettes = {
    "A-Actuel(5)": ("@80&=.", 5),
    "B-Gepeto(5)": ("@#*+.", 5),
    "C-Blocks(5)": ("█▓▒░ ", 5),  # Unicode blocks
    "D-Contrast(5)": ("#%xo.", 5),
    "E-Actuel(10)": ("@80&=+-.", 10),
    "F-Gepeto(10)": ("@#*+=-.", 10),
}

print("="*60)
print("TEST PALETTES THEIAVISION - Zone visage (24x18)")
print("="*60)

results = {}
for name, (palette, levels) in palettes.items():
    result = convert_with_palette(zone_gray, palette, levels)
    results[name] = result
    print(f"\n{name}:")
    print("-" * 40)
    print(result)
    print()

# Sauvegarder dans un fichier
with open('/tmp/palette_comparison.txt', 'w') as f:
    for name, result in results.items():
        f.write(f"\n{name}:\n")
        f.write("-" * 40 + "\n")
        f.write(result + "\n\n")

print("\n✅ Résultats sauvegardés dans /tmp/palette_comparison.txt")
