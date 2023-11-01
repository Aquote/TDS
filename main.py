import numpy as np
import matplotlib.pyplot as plt

# Charger les images
image_reference = plt.imread("./fichierImage/8.png")
image_to_compare = plt.imread('2.png')
print('Chemin de l\'image de référence :', '1.png')
# Assurez-vous que l'image est au format BGR, vous pouvez la convertir en RGB si nécessaire

# Afficher l'image à l'aide de Matplotlib
plt.imshow(image_reference)
plt.axis('off')  # Désactive les axes
plt.show()

# À partir de ce point, vous pouvez ajouter la logique pour l'analyse, la comparaison et la validation des images comme vous l'avez décrit dans votre question initiale.
