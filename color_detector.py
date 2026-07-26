#!/usr/bin/env python3
"""
TheiaVision - Détecteur de couleurs simplifié
Map RGB vers caractères couleur
"""

from PIL import Image
import sys

def detect_color(r, g, b):
    """Détecte la couleur dominante d'un pixel."""
    # Seuils
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    # Noir/Blanc/Gris
    if max_val < 50:
        return 'K'  # Noir
    if min_val > 200:
        return 'W'  # Blanc
    if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
        return '.'  # Gris/Neutre
    
    # Couleurs
    if r > 150 and g > 150 and b < 100:
        return 'Y'  # Jaune !
    if r > 150 and g < 100 and b < 100:
        return 'R'  # Rouge
    if r < 100 and g > 150 and b < 100:
        return 'G'  # Vert
    if r < 100 and g < 100 and b > 150:
        return 'B'  # Bleu
    if r > 150 and g < 100 and b > 150:
        return 'M'  # Magenta
    if r < 100 and g > 150 and b > 150:
        return 'C'  # Cyan
    
    # Par défaut
    return '?'  # Incertain

def image_to_color(image_path, width=32, height=24):
    """Convertit une image en carte de couleurs."""
    img = Image.open(image_path)
    img = img.resize((width, height))
    
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            color = detect_color(r, g, b)
            line += color
        lines.append(line)
    
    return '\n'.join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 color_detector.py <image.jpg> [width] [height]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    h = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    
    print("Légende: Y=Jaune R=Rouge G=Vert B=Bleu W=Blanc K=Noir .=Gris M=Magenta C=Cyan")
    print("-" * 60)
    print(image_to_color(image_path, w, h))
