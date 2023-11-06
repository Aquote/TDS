# -*- coding: utf-8 -*-
import cv2
import numpy as np

def compare_plate_sizes(w1, h1, w2, h2):
    if w2 < w1 and h2 < h1:
        return "plus petite que"
    elif w2 > w1 and h2 > h1:
        return "plus grande que"
    else:
        return "de taille egale a"

def compare_plate_size(image1, image2, filename1, filename2):
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
    w1, h1 = 0, 0
    w2, h2 = 0, 0

    if len(contours1) > 0 and len(contours2) > 0:
        x1, y1, w1, h1 = cv2.boundingRect(contours1[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours2[0])

        # Comparer les dimensions des plaques
        size_comparison = compare_plate_sizes(w1, h1, w2, h2)
        print(f"La plaque est {size_comparison} la plaque de reference.")

    return w1, h1, w2, h2

# Charger vos images ici (image1 et image2)
# image1 = cv2.imread("nom_de_votre_image1.jpg")
# image2 = cv2.imread("nom_de_votre_image2.jpg")

# Remplacez "nom_de_votre_image1.jpg" et "nom_de_votre_image2.jpg" par les noms de vos fichiers d'images

# Appeler la fonction de comparaison
# w1, h1, w2, h2 = compare_plate_size(image1, image2, "nom_image1", "nom_image2")

# Afficher les résultats
# print(f"Comparaison de la taille des plaques :")
# print(f"Dimensions de {filename1}: Largeur = {w1}, Hauteur = {h1}")
# print(f"Dimensions de {filename2}: Largeur = {w2}, Hauteur = {h2}")
