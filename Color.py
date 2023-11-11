import cv2
import numpy as np
import json
import os

def determine_plate_color(image_path):
    """
    Détermine la couleur d'une plaque à partir d'une image.

    Parameters:
    - image_path (str): Chemin vers le fichier image.

    Returns:
    - str or None: "Blanche" si la plaque est de couleur blanche (crème), "Brune" si la plaque est de couleur brune (carton), ou None si la détection est impossible.
    """
    # Charger l'image
    image = cv2.imread(image_path)

    # Convertir l'image en espace colorimétrique LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Définir les seuils pour la couleur blanche (crème) en LAB
    lower_white = np.array([200, 128, 128], dtype=np.uint8)
    upper_white = np.array([255, 143, 143], dtype=np.uint8)

    # Définir les seuils pour la couleur brune (carton) en LAB
    lower_brown = np.array([20, 128, 128], dtype=np.uint8)
    upper_brown = np.array([40, 143, 143], dtype=np.uint8)

    # Appliquer le seuillage pour détecter la couleur blanche
    white_mask = cv2.inRange(lab_image, lower_white, upper_white)

    # Appliquer le seuillage pour détecter la couleur brune
    brown_mask = cv2.inRange(lab_image, lower_brown, upper_brown)

    # Compter le nombre de pixels blancs et bruns
    white_pixel_count = cv2.countNonZero(white_mask)
    brown_pixel_count = cv2.countNonZero(brown_mask)

    
    # Déterminer la couleur dominante en fonction du nombre de pixels
    if white_pixel_count > brown_pixel_count:
        plate_color= "Blanche"
    elif brown_pixel_count > white_pixel_count:
        plate_color= "Brune"
    else:
        plate_color= "Erreur"
    
    # Obtenez le nom du fichier avec l'extension
    filename = os.path.basename(image_path)

    # Charger le contenu actuel du fichier JSON ou créer un dictionnaire vide si le fichier est vide
    if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
        with open("data.json", "r") as json_file:
            json_data = json.load(json_file)
    else:
        json_data = {}

    # Ajouter ou mettre à jour les informations spécifiques pour l'image actuelle
    json_data.setdefault(filename, {}).update({"couleur": plate_color})

    # Enregistrez le dictionnaire mis à jour dans le fichier JSON
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)

    return plate_color
    
    
    

# Exemple d'utilisation
image_path = "./fichierImage/6.png"
plate_color = determine_plate_color(image_path)

if plate_color is not None:
    print(f"La plaque est de couleur : {plate_color}")
else:
    print("Impossible de déterminer la couleur de la plaque.")

