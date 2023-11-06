# -*- coding: utf-8 -*-
import cv2
import numpy as np

def determine_plate_orientation(contours):
    angle = 0  # Angle par défaut

    if len(contours) > 4:
        # Si suffisamment de contours sont trouvés, calculez l'angle d'orientation
        rect = cv2.minAreaRect(contours[0])
        angle = rect[2]

    return angle

def compare_plate_orientation(image1, image2, filename1, filename2):
    # Appliquer un filtre de lissage gaussien à l'image 1
    image1_filtree = cv2.GaussianBlur(image1, (5, 5), 0)

    # Appliquer un filtre de lissage gaussien à l'image 2
    image2_filtree = cv2.GaussianBlur(image2, (5, 5), 0)

    # Convertir les images en niveaux de gris
    image1_gray = cv2.cvtColor(image1_filtree, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2_filtree, cv2.COLOR_BGR2GRAY)

    # Appliquer le seuillage pour binariser les images et obtenir des masques des parties blanches
    _, binary_mask1 = cv2.threshold(image1_gray, 135, 255, cv2.THRESH_BINARY)
    _, binary_mask2 = cv2.threshold(image2_gray, 135, 255, cv2.THRESH_BINARY)

    # Identifier les contours dans les masques binaires
    contours1, _ = cv2.findContours(binary_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Définir des valeurs par défaut si aucun contour n'est trouvé
    angle1 = 0
    angle2 = 0

    if len(contours1) > 0 and len(contours2) > 0:
        # Déterminer l'orientation des plaques
        angle1 = determine_plate_orientation(contours1)
        angle2 = determine_plate_orientation(contours2)

        print(f"Orientation de {filename1}: {angle1} degrés")
        print(f"Orientation de {filename2}: {angle2} degrés")

    return angle1, angle2

# Charger vos images ici (image1 et image2)
# image1 = cv2.imread("nom_de_votre_image1.jpg")
# image2 = cv2.imread("nom_de_votre_image2.jpg")

# Remplacez "nom_de_votre_image1.jpg" et "nom_de_votre_image2.jpg" par les noms de vos fichiers d'images

# Appeler la fonction de comparaison
# angle_image1, angle_image2 = compare_plate_orientation(image1, image2, "nom_image1", "nom_image2")

# Afficher les résultats
# print(f"Comparaison d'orientation :")
# if angle_image1 < 45 or angle_image1 > 135:
#     print("Image 1 est en mode portrait")
# else:
#     print("Image 1 est en mode paysage")
# if angle_image2 < 45 or angle_image2 > 135:
#     print("Image 2 est en mode portrait")
# else:
#     print("Image 2 est en mode paysage")
