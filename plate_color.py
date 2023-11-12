import cv2
import numpy as np
import json
import os

def determine_plate_color(image_path, screen=False):
    """
    Détermine la couleur dominante d'une plaque d'immatriculation à partir d'une image.

    Paramètres :
    - image_path (str) : Chemin vers le fichier image.
    - screen (bool) : Si True, affiche l'image avec les masques blanc et brun.

    Renvoie :
    - str ou None : "Blanche" si la plaque est de couleur blanche (crème), "Brune" si la plaque est de couleur brune (carton), ou None si la détection est impossible.
    """
    image = cv2.imread(image_path)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Redimensionner l'image à 600x400 pixels
    image = cv2.resize(image, (600, 400))

    lower_white = np.array([200, 128, 128], dtype=np.uint8)
    upper_white = np.array([255, 143, 143], dtype=np.uint8)

    lower_brown = np.array([20, 128, 128], dtype=np.uint8)
    upper_brown = np.array([40, 143, 143], dtype=np.uint8)

    white_mask = cv2.inRange(lab_image, lower_white, upper_white)
    brown_mask = cv2.inRange(lab_image, lower_brown, upper_brown)

    white_pixel_count = cv2.countNonZero(white_mask)
    brown_pixel_count = cv2.countNonZero(brown_mask)

    if white_pixel_count > brown_pixel_count:
        plate_color = "Blanche"
    elif brown_pixel_count > white_pixel_count:
        plate_color = "Brune"
    else:
        plate_color = "Erreur"

    if screen:
        cv2.imshow("Image originale", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    filename = os.path.basename(image_path)

    if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
        with open("data.json", "r") as json_file:
            json_data = json.load(json_file)
    else:
        json_data = {}

    json_data.setdefault(filename, {}).update({"couleur": plate_color})

    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)

    return plate_color

# Exemple d'utilisation
image_path = "./fichierImage/6.png"
plate_color = determine_plate_color(image_path, screen=True)

if plate_color is not None:
    print(f"La plaque est de couleur : {plate_color}")
else:
    print("Impossible de déterminer la couleur de la plaque.")
