import json
import os
import cv2
import numpy as np

def determine_plate_orientation(image_path):
    """
    Détermine l'angle d'orientation d'une plaque à partir d'une image.

    Parameters:
    - image_path (str): Chemin vers le fichier image.

    Returns:
    - float or None: L'angle d'orientation de la plaque en degrés, ou None si la détection est impossible.

    Processus :
    1. Convertit l'image en niveaux de gris.
    2. Applique une augmentation de contraste en utilisant l'égalisation d'histogramme.
    3. Utilise la détection de coins Shi-Tomasi pour trouver les coins significatifs.
    4. Sélectionne les coins les plus éloignés pour déterminer la diagonale de la plaque.
    5. Dessine une ligne entre les coins sélectionnés.
    6. Calcule l'angle d'orientation en degrés à partir de la ligne.
    """
    # Charger l'image
    image = cv2.imread(image_path)

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer une augmentation de contraste en utilisant l'égalisation d'histogramme
    equalized = cv2.equalizeHist(gray)

    # Appliquer la détection de coins Shi-Tomasi
    corners = cv2.goodFeaturesToTrack(equalized, maxCorners=100, qualityLevel=0.01, minDistance=10)

    # Convertir les coordonnées des coins en entiers
    corners = np.int0(corners)

    # Dessiner les coins sur l'image
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, 255, -1)

    # Calculer l'orientation de la plaque
    if len(corners) >= 4:
        # Sélectionner les coins les plus éloignés
        top_left = min(corners, key=lambda corner: corner[0][0] + corner[0][1])
        bottom_right = max(corners, key=lambda corner: corner[0][0] + corner[0][1])

        # Dessiner une ligne entre les coins sélectionnés
        cv2.line(image, (top_left[0][0], top_left[0][1]), (bottom_right[0][0], bottom_right[0][1]), (0, 255, 0), 2)

        # Calculer l'angle d'orientation
        angle = np.arctan2(bottom_right[0][1] - top_left[0][1], bottom_right[0][0] - top_left[0][0]) * 180 / np.pi
        angle = round(angle,3)

    # Obtenez le nom du fichier avec l'extension
    filename = os.path.basename(image_path)

    # Charger le contenu actuel du fichier JSON ou créer un dictionnaire vide si le fichier est vide
    if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
        with open("data.json", "r") as json_file:
            json_data = json.load(json_file)
    else:
        json_data = {}

    # Ajouter ou mettre à jour les informations spécifiques pour l'image actuelle
    json_data.setdefault(filename, {}).update({"orientation": angle})

    # Enregistrez le dictionnaire mis à jour dans le fichier JSON
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)

    return angle


image_path = "./fichierImage/8.png"
orientation_angle = determine_plate_orientation(image_path)

if orientation_angle is not None:
    print(f"L'angle d'orientation de la plaque est : {orientation_angle} degrés.")
else:
    print("Impossible de déterminer l'orientation de la plaque.")