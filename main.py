import numpy as np
import matplotlib.pyplot as plt
import os


current_directory = os.getcwd()
print("Répertoire de travail actuel :", current_directory)
# Charger les images
<<<<<<< HEAD
image_reference = plt.imread("./fichierImage/8.png")
image_to_compare = plt.imread('./fichierImage/2.png')
print('Chemin de l\'image de référence :', '1.png')
# Assurez-vous que l'image est au format BGR, vous pouvez la convertir en RGB si nécessaire
=======
image_reference = plt.imread("./fichierImage/1.png")

image_to_compare = plt.imread("./fichierImage/2.png")
>>>>>>> b5ca8089b387068d9de017642d13e850f5148a64

# Afficher l'image à l'aide de Matplotlib
plt.imshow(image_reference)
plt.axis('off')  # Désactive les axes
plt.show()

# À partir de ce point, vous pouvez ajouter la logique pour l'analyse, la comparaison et la validation des images comme vous l'avez décrit dans votre question initiale.
