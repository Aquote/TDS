import cv2
import numpy as np
import json
import os

def measure_contour_dimensions(image_path):
    """
    Mesure les dimensions totales des contours dans une image et enregistre le résultat dans un fichier JSON.

    Parameters:
        image_path (str): Le chemin de l'image à traiter.

    Returns:
        dict: Un dictionnaire contenant les dimensions totales (longueur et largeur) des contours.

    Steps:
         1. Charger l'image en couleur.
        2. Convertir l'image en niveaux de gris pour simplifier le traitement.
        3. Appliquer une opération de fermeture pour éliminer le bruit dans l'image.
        4. Appliquer une opération de dilatation pour rendre les contours plus visibles.
        5. Soustraire la dilatation de l'image fermée pour obtenir les contours.
        6. Seuiller l'image pour obtenir une image binaire avec des contours.
        7. Trouver les contours dans l'image binaire.
        8. Parcourir tous les contours trouvés.
        9. Mesurer les dimensions du rectangle englobant (bounding box) de chaque contour.
        10. Ajouter les dimensions au total pour obtenir les dimensions totales.
        11. Charger le contenu actuel du fichier JSON ou créer un dictionnaire vide si le fichier est vide.
        12. Ajouter ou mettre à jour les informations spécifiques pour l'image actuelle.
        13. Enregistrer le dictionnaire mis à jour dans le fichier JSON (data.json).
        14. Renvoyer le dictionnaire des dimensions totales.
    """
    # Charger l'image en couleur
    image = cv2.imread(image_path)

    # Convertir l'image en niveaux de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer une opération de fermeture pour éliminer le bruit
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    # Appliquer une opération de dilatation
    dilated = cv2.dilate(closing, kernel, iterations=2)

    # Soustraire la dilatation de l'image fermée pour obtenir les contours
    contour_image = cv2.absdiff(dilated, closing)

    # Seuiller l'image pour obtenir une image binaire
    _, thresh = cv2.threshold(contour_image, 30, 255, cv2.THRESH_BINARY)

    # Trouver les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialiser les variables pour stocker les dimensions totales
    total_length = 0
    total_width = 0

    # Parcourir tous les contours
    for contour in contours:
        # Mesurer les dimensions du contour
        x, y, w, h = cv2.boundingRect(contour)

        # Ajouter les dimensions au total
        total_length += w
        total_width += h

    # Créer un dictionnaire avec les dimensions totales
    dimensions_data = {
        "longueur_totale": total_length,
        "largeur_totale": total_width
    }

    # Obtenez le nom du fichier avec l'extension
    filename = os.path.basename(image_path)

    # Charger le contenu actuel du fichier JSON ou créer un dictionnaire vide si le fichier est vide
    if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
        with open("data.json", "r") as json_file:
            json_data += json.load(json_file)
    else:
        json_data = {}

    # Ajouter ou mettre à jour les informations spécifiques pour l'image actuelle
    json_data[filename] = dimensions_data

    # Enregistrez le dictionnaire mis à jour dans le fichier JSON
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)


    return dimensions_data


image_path = "./fichierImage/3.png"
result = measure_contour_dimensions(image_path)
print("Dimensions mesurées :", result)
