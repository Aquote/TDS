import cv2
import numpy as np


# Charger les deux images
image1 = cv2.imread("fichierImage/1.png")
image2 = cv2.imread("fichierImage/3.png")

# Assurez-vous que les images ont la même taille (redimensionnez ou recadrez si nécessaire)
if image1.shape != image2.shape:
    # Redimensionnez ou recadrez les images pour les mettre à la même taille
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

# Convertir les images en espace de couleur Lab (pour une meilleure représentation des couleurs)
image1_lab = cv2.cvtColor(image1, cv2.COLOR_BGR2Lab)
image2_lab = cv2.cvtColor(image2, cv2.COLOR_BGR2Lab)

# Calculer la différence de couleur moyenne entre les images
color_difference = np.mean(np.abs(image1_lab - image2_lab))

# Définir un seuil de différence
seuil = 10  # Vous pouvez ajuster ce seuil en fonction de votre application

# Comparer la différence de couleur à votre seuil
if color_difference > seuil:
    print("Les images sont différentes.")
else:
    print("Les images sont similaires.")