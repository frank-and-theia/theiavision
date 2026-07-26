#!/usr/bin/env python3
"""
TheiaVision - Convertisseur Image vers ASCII (Blocs d'opacité)
===============================================================

Ce script convertit une image en représentation ASCII utilisant des caractères
Unicode de blocs pour créer une "grille de pixels" lisible par Theia.

Caractères utilisés (du plus clair au plus foncé):
  " " = espace (vide)
  "░" = 25% opaque (U+2591)
  "▒" = 50% opaque (U+2592)  
  "▓" = 75% opaque (U+2593)
  "█" = 100% opaque (U+2588)

Avantage : Theia "voit" directement la densité sans décodage mental !
"""

import cv2
import numpy as np

def image_to_ascii(image_path, width=80, height=40):
    """
    Convertit une image en représentation ASCII avec blocs d'opacité.
    
    Args:
        image_path: Chemin vers l'image
        width: Largeur souhaitée (en caractères)
        height: Hauteur souhaitée (en lignes)
    
    Returns:
        String ASCII avec caractères de blocs
    """
    # 1. Charger l'image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image non trouvée: {image_path}")
    
    # 2. Convertir en noir et blanc (grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2b. Égaliser le contraste (améliore la délimitation des zones)
    # Technique suggérée par Gepeto : CLAHE ou equalizeHist
    gray = cv2.equalizeHist(gray)  # Égalisation d'histogramme simple
    # Alternative plus douce : CLAHE
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # gray = clahe.apply(gray)
    
    # 3. Redimensionner
    small = cv2.resize(gray, (width, height))
    
    # 4. Mapper vers des caractères selon luminosité (5 niveaux)
    chars = [" ", "░", "▒", "▓", "█"]
    
    # 5. Générer l'ASCII
    ascii_lines = []
    for row in small:
        line = ""
        for pixel in row:
            # pixel va de 0 (noir) à 255 (blanc)
            # On inverse pour que noir = █ et blanc = " "
            index = int((255 - pixel) / 255 * (len(chars) - 1))
            line += chars[index]
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)


def webcam_to_ascii(width=80, height=40):
    """
    Capture une frame de la webcam et la convertit en ASCII.
    
    Returns:
        String ASCII de la frame capturée
    """
    cap = cv2.VideoCapture(0)  # 0 = webcam par défaut
    
    if not cap.isOpened():
        raise RuntimeError("Impossible d'ouvrir la webcam")
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise RuntimeError("Impossible de capturer une image")
    
    # Sauvegarder temporairement et convertir
    temp_path = "/tmp/theiavision_frame.jpg"
    cv2.imwrite(temp_path, frame)
    
    return image_to_ascii(temp_path, width, height)


# === EXEMPLE D'UTILISATION ===
if __name__ == "__main__":
    # Test avec une image existante
    try:
        result = image_to_ascii("test_image.jpg", width=60, height=30)
        print(result)
    except FileNotFoundError:
        print("Place une image 'test_image.jpg' dans le dossier pour tester")
    
    # Ou test avec webcam (décommenter pour utiliser)
    # result = webcam_to_ascii(width=60, height=30)
    # print(result)


"""
AMÉLIORATIONS POSSIBLES:
=======================

1. Plus de niveaux de gris :
   chars = [" ", "·", ":", "░", "▒", "▓", "█"]  # 7 niveaux

2. Utiliser les demi-blocs pour doubler la résolution verticale :
   "▀" = demi-haut (U+2580)
   "▄" = demi-bas (U+2584)
   "█" = plein (U+2588)

3. Mode occupancy grid (pour navigation) :
   Remplacer par 0/1 selon seuil :
   if pixel < 128: "█" else: " "

4. Mode symbolique (pour compréhension) :
   Détecter les zones et étiqueter :
   "████████" → "[MUR]"
   "   ██   " → "[OBJET]"

5. Streaming temps réel :
   Boucle infinie avec intervalle (ex: 100ms = 10 FPS)
"""
