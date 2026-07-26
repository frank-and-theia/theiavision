#!/usr/bin/env python3
"""
TheiaVision - Convertisseur ASCII v0.1
Transforme une image en grille de caractères pour IA text-based
"""

from PIL import Image
import sys

def image_to_ascii(image_path, output_width=64, output_height=36):
    """Convertit une image en ASCII art optimisé pour LLM."""
    
    # Caractères ASCII par densité croissante
    # De l'espace (vide) au bloc plein (plein)
    ASCII_CHARS = [' ', '░', '▒', '▓', '█']
    
    # Ouvrir l'image
    img = Image.open(image_path)
    
    # Convertir en RGB si nécessaire
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Redimensionner
    img = img.resize((output_width, output_height))
    
    # Convertir en niveaux de gris
    img_gray = img.convert('L')
    
    # Construire la grille ASCII
    ascii_lines = []
    for y in range(output_height):
        line = ""
        for x in range(output_width):
            # Valeur de gris (0-255)
            gray_value = img_gray.getpixel((x, y))
            
            # Mapper vers un caractère (0-255 → 0-4)
            char_index = int((gray_value / 255) * (len(ASCII_CHARS) - 1))
            char_index = max(0, min(char_index, len(ASCII_CHARS) - 1))
            
            line += ASCII_CHARS[char_index]
        ascii_lines.append(line)
    
    return '\n'.join(ascii_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ascii_converter.py <image.jpg> [width] [height]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 36
    
    result = image_to_ascii(image_path, width, height)
    print(result)
