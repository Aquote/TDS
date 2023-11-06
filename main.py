import cv2
import os
from image_processing import process_image

# Spécifiez les noms de fichiers que vous souhaitez comparer
fichier_image1 = "./fichierImage/5.png"
fichier_image2 = "./fichierImage/6.png"

# Extraire le nom de fichier sans extension et l'extension
nom_image1, extension1 = os.path.splitext(os.path.basename(fichier_image1))
nom_image2, extension2 = os.path.splitext(os.path.basename(fichier_image2))

# Chargez les images que vous souhaitez comparer
image1 = cv2.imread(fichier_image1)
image2 = cv2.imread(fichier_image2)

# Appeler la fonction de traitement d'image depuis image_processing.py
process_image(image1, image2, nom_image1 + extension1, nom_image2 +  extension2)
