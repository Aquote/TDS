import numpy as np
import cv2
import os

def compare_plate_sizes(w1, h1, w2, h2):
    if w1 < w2 and h1 < h2:
        return "plus petite"
    elif w1 > w2 and h1 > h2:
        return "plus grande"
    else:
        return "de taille égale"

def analyze_images(image1, image2, filename1, filename2):
    # Appliquer un filtre de lissage gaussien
    image_filtree = cv2.GaussianBlur(image1, (5, 5), 0)
    image_filtree2 = cv2.GaussianBlur(image2, (5, 5), 0)
    # Convertir les images en niveaux de gris
    image1_gray = cv2.cvtColor(image_filtree, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image_filtree, cv2.COLOR_BGR2GRAY)

    # Appliquer le seuillage pour binariser les images et obtenir des masques des parties blanches
    _, binary_mask1 = cv2.threshold(image1_gray, 135, 255, cv2.THRESH_BINARY)
    _, binary_mask2 = cv2.threshold(image2_gray, 135, 255, cv2.THRESH_BINARY)

    # Créer des images vertes du même format que les images d'entrée
    image1_green = np.zeros_like(image_filtree)
    image2_green = np.zeros_like(image_filtree2)

    # Remplacer les parties blanches par du vert dans les images vertes
    image1_green[:, :, 1] = 255  # Canal vert
    image2_green[:, :, 1] = 255  # Canal vert

    # Appliquer les masques pour marquer les parties blanches en vert
    image_marked1 = cv2.add(image_filtree, image1_green, mask=binary_mask1)
    image_marked2 = cv2.add(image_filtree2, image2_green, mask=binary_mask2)

    # Identifier les contours dans les masques binaires
    contours1, _ = cv2.findContours(binary_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Définir des valeurs par défaut si aucun contour n'est trouvé
    w1, h1 = 0, 0
    w2, h2 = 0, 0

    if len(contours1) > 0 and len(contours2) > 0:
        # Le premier contour (contours[0]) est utilisé ici, vous pouvez boucler à travers les contours si nécessaire
        x1, y1, w1, h1 = cv2.boundingRect(contours1[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours2[0])

        # Comparer les dimensions des plaques
        size_comparison = compare_plate_sizes(w1, h1, w2, h2)
        print(f"La seconde plaque est {size_comparison} que la plaque de base.")

    # Redimensionner les images pour les afficher en 600x500
    resized_image1 = cv2.resize(image_marked1, (600, 500))
    resized_image2 = cv2.resize(image_marked2, (600, 500))

    # Afficher les images marquées redimensionnées avec les noms de fenêtre basés sur les noms de fichiers d'origine
    cv2.imshow(filename1 + " avec filtre", resized_image1)
    cv2.imshow(filename2 + " avec filtre", resized_image2)

    # Attendre une touche et fermer les fenêtres d'affichage
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Charger les images que vous souhaitez analyser
image1 = cv2.imread("./fichierImage/5.png")
image2 = cv2.imread("./fichierImage/6.png")

# Récupérer les noms de fichiers avec extension
filename1 = os.path.basename("./fichierImage/5.png")
filename2 = os.path.basename("./fichierImage/6.png")

# Appeler la fonction pour analyser les images
analyze_images(image1, image2, filename1, filename2)
