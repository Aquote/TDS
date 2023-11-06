# -*- coding: utf-8 -*-
import cv2
import numpy as np

def compare_plate_sizes(w1, h1, w2, h2):
    if w2 < w1 and h2 < h1:
        return "plus petite que"
    elif w2 > w1 and h2 > h1:
        return "plus grande  que"
    else:
        return "de taille egale a"

def determine_plate_orientation(contours):
    angle = 0  # Angle par défaut

    if len(contours) > 4:
        # Si suffisamment de contours sont trouvés, calculez l'angle d'orientation
        rect = cv2.minAreaRect(contours[0])
        angle = rect[2]

    return angle

def process_image(image1, image2, filename1, filename2):
    
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

    # Créer des images vertes du même format que les images d'entrée
    image1_green = np.zeros_like(image1_filtree)
    image2_green = np.zeros_like(image2_filtree)

    # Remplacer les parties blanches par du vert dans les images vertes
    image1_green[:, :, 1] = 255  # Canal vert
    image2_green[:, :, 1] = 255  # Canal vert

    # Appliquer les masques pour marquer les parties blanches en vert
    image_marked1 = cv2.add(image1_filtree, image1_green, mask=binary_mask1)
    image_marked2 = cv2.add(image2_filtree, image2_green, mask=binary_mask2)

    # Identifier les contours dans les masques binaires
    contours1, _ = cv2.findContours(binary_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Reste du code inchangé...
    # Définir des valeurs par défaut si aucun contour n'est trouvé
    w1, h1 = 0, 0
    w2, h2 = 0, 0

    if len(contours1) > 0 and len(contours2) > 0:
        x1, y1, w1, h1 = cv2.boundingRect(contours1[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours2[0])

        # Comparer les dimensions des plaques
        size_comparison = compare_plate_sizes(w1, h1, w2, h2)
        print(f"La plaque est {size_comparison} la plaque de reference.")

        # Déterminer l'orientation des plaques
        orientation1 = determine_plate_orientation(contours1)
        orientation2 = determine_plate_orientation(contours2)

        print(f"Orientation de la plaque de reference : {orientation1} degres")
        print(f"Orientation de la deuxieme plaque : {orientation2} degres")

    # Redimensionner les images binaires pour les afficher en 600x500
    resized_image1 = cv2.resize(binary_mask1, (600, 500))
    resized_image2 = cv2.resize(binary_mask2, (600, 500))

    # Afficher l'image binaire avec le nom du fichier
    cv2.imshow(filename1, resized_image1)
    cv2.imshow(filename2, resized_image2)

    # Attendez une touche et fermez les fenêtres d'affichage
    cv2.waitKey(0)
    cv2.destroyAllWindows()
