#!/usr/bin/env python3
"""
TheiaVision - Convertisseur ASCII v0.3 (Demi-blocs Unicode)
Double la résolution verticale ! ▀ ▄ █
"""

from PIL import Image
import sys

def image_to_ascii_blocks(image_path, output_width=64, output_height=36):
    """Convertit une image en demi-blocs Unicode pour 2x résolution verticale."""
    
    # Demi-blocs Unicode : ▀ (haut), ▄ (bas), █ (plein), ' ' (vide)
    # Chaque caractère = 2 pixels verticaux
    BLOCKS = [' ', '▄', '▀', '█']
    
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Hauteur x2 car chaque caractère représente 2 pixels
    img = img.resize((output_width, output_height * 2))
    img_gray = img.convert('L')
    
    ascii_lines = []
    for y in range(0, output_height * 2, 2):
        line = ""
        for x in range(output_width):
            # Pixel du haut
            top = img_gray.getpixel((x, y))
            # Pixel du bas
            bottom = img_gray.getpixel((x, y + 1))
            
            # Seuil : > 128 = allumé
            top_on = 1 if top > 128 else 0
            bottom_on = 1 if bottom > 128 else 0
            
            # Index : 0=rien, 1=bas, 2=haut, 3=plein
            idx = (top_on * 2) + bottom_on
            line += BLOCKS[idx]
        ascii_lines.append(line)
    
    return '\n'.join(ascii_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ascii_converter_blocks.py <image.jpg> [width] [height]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 36
    
    result = image_to_ascii_blocks(image_path, width, height)
    print(result)
