import numpy as np
import cv2
import os

def analyze_images(image1, image2, filename1, filename2):
    # Convertir les images en niveaux de gris
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Appliquer le seuillage pour binariser les images et obtenir des masques des parties blanches
    _, binary_mask1 = cv2.threshold(image1_gray, 135, 255, cv2.THRESH_BINARY)
    _, binary_mask2 = cv2.threshold(image2_gray, 135, 255, cv2.THRESH_BINARY)

    # Créer des images vertes du même format que les images d'entrée
    image1_green = np.zeros_like(image1)
    image2_green = np.zeros_like(image2)

    # Remplacer les parties blanches par du vert dans les images vertes
    image1_green[:, :, 1] = 255  # Canal vert
    image2_green[:, :, 1] = 255  # Canal vert

    # Appliquer les masques pour marquer les parties blanches en vert
    image_marked1 = cv2.add(image1, image1_green, mask=binary_mask1)
    image_marked2 = cv2.add(image2, image2_green, mask=binary_mask2)

    # Identifier les contours dans les masques binaires
    contours1, _ = cv2.findContours(binary_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si des contours sont trouvés, calculez les dimensions du rectangle englobant
    if len(contours1) > 0 and len(contours2) > 0:
        # Le premier contour (contours[0]) est utilisé ici, vous pouvez boucler à travers les contours si nécessaire
        x1, y1, w1, h1 = cv2.boundingRect(contours1[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours2[0])

        # Résolution de l'image en pixels par centimètre (remplacez X par la valeur réelle)
        resolution_pixels_par_cm = 1

        # Conversion en centimètres
        largeur_cm1 = w1 / resolution_pixels_par_cm
        hauteur_cm1 = h1 / resolution_pixels_par_cm

        largeur_cm2 = w2 / resolution_pixels_par_cm
        hauteur_cm2 = h2 / resolution_pixels_par_cm

        print("Dimensions du rectangle englobant de l'image 1 (Largeur x Hauteur) en centimètres : {:.2f} cm x {:.2f} cm".format(largeur_cm1, hauteur_cm1))
        print("Dimensions du rectangle englobant de l'image 2 (Largeur x Hauteur) en centimètres : {:.2f} cm x {:.2f} cm".format(largeur_cm2, hauteur_cm2))

    # Redimensionner les images pour les afficher en 600x500
    resized_image1 = cv2.resize(image_marked1, (600, 500))
    resized_image2 = cv2.resize(image_marked2, (600, 500))

    # Vous pouvez retourner ou afficher les images redimensionnées si nécessaire
    return resized_image1, resized_image2

# Charger les images que vous souhaitez analyser
image1 = cv2.imread("./fichierImage/5.png")
image2 = cv2.imread("./fichierImage/6.png")

# Récupérer les noms de fichiers avec extension
filename1 = os.path.basename("./fichierImage/5.png")
filename2 = os.path.basename("./fichierImage/6.png")

# Appeler la fonction pour analyser les images
marked_image1, marked_image2 = analyze_images(image1, image2, filename1, filename2)

# Afficher les images marquées redimensionnées avec les noms de fenêtre basés sur les noms de fichiers d'origine
cv2.imshow(filename1 + " avec filtre", marked_image1)
cv2.imshow(filename2 + " avec filtre", marked_image2)

# Attendez une touche et fermez les fenêtres d'affichage
cv2.waitKey(0)
cv2.destroyAllWindows()
