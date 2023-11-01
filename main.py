import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

current_directory = os.getcwd()
print("Répertoire de travail actuel :", current_directory)

# Charger l'image de référence
image_reference = cv2.imread("./fichierImage/5.png")

# Convertir l'image de référence en niveaux de gris
image_reference_gray = cv2.cvtColor(image_reference, cv2.COLOR_BGR2GRAY)

# Appliquer un seuillage pour binariser l'image et obtenir un masque des parties blanches
_, binary_mask = cv2.threshold(image_reference_gray, 150, 255, cv2.THRESH_BINARY)

# Créer une image verte du même format que l'image de référence
image_green = np.zeros_like(image_reference)

# Remplacer les parties blanches par du vert dans l'image verte
image_green[:, :, 1] = 255  # Canal vert

# Appliquer le masque pour marquer les parties blanches en vert
image_marked = cv2.add(image_reference, image_green, mask=binary_mask)

# Identifier les contours dans le masque binaire
contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Si des contours sont trouvés, calculez les dimensions du rectangle englobant
if len(contours) > 0:
    # Le premier contour (contours[0]) est utilisé ici, vous pouvez boucler à travers les contours si nécessaire
    x, y, w, h = cv2.boundingRect(contours[0])

    # Résolution de l'image en pixels par centimètre (remplacez X par la valeur réelle)
    resolution_pixels_par_cm = 1

    # Conversion en centimètres
    largeur_cm = w / resolution_pixels_par_cm
    hauteur_cm = h / resolution_pixels_par_cm

    print("Dimensions du rectangle englobant (Largeur x Hauteur) en centimètres : {:.2f} cm x {:.2f} cm".format(largeur_cm, hauteur_cm))

# Afficher l'image marquée en vert
plt.imshow(cv2.cvtColor(image_marked, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()