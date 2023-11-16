import cv2
import numpy as np
import json
import os

def measure_contour_dimensions(image_path):
    """
    Mesure les dimensions totales des contours dans une image et enregistre le résultat dans un fichier JSON.

    Paramètres :
        image_path (str) : Le chemin de l'image à traiter.

    Renvoie :
        dict : Un dictionnaire contenant les dimensions totales (longueur et largeur) des contours.
    """
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.dilate(closing, kernel, iterations=2)
    contour_image = cv2.absdiff(dilated, closing)
    _, thresh = cv2.threshold(contour_image, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_length = 0
    total_width = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        total_length += w
        total_width += h

    dimensions_data = {
        "longueur_totale": total_length,
        "largeur_totale": total_width
    }

    filename = os.path.basename(image_path)

    if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
        with open("data.json", "r") as json_file:
            json_data = json.load(json_file)
    else:
        json_data = {}

    # Mettez à jour le dictionnaire avec les nouvelles données sans écraser les anciennes
    json_data[filename] = {**json_data.get(filename, {}), **dimensions_data}

    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)

    return dimensions_data

"""
# Exemple d'utilisation
image_path = "./fichierImage/1.png"
result = measure_contour_dimensions(image_path)
print("Dimensions mesurées :", result)
"""