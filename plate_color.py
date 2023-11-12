import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
import json

def detect_defauts(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (600, 400))
    image_blur = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(image_blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_size = 20

    if contours:
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_size and 50 < cnt[0][0][0] < 550 and 50 < cnt[0][0][1] < 350]
        plaque_mask = np.zeros_like(image, dtype=np.uint8)
        cv2.drawContours(plaque_mask, filtered_contours, -1, 255, thickness=cv2.FILLED)
        points_noirs = []
        
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                if cv2.pointPolygonTest(np.concatenate(filtered_contours), (x, y), False) > 0:
                    if image[y, x] < 100:
                        points_noirs.append((x, y))
        
        points_noirs_array = np.array(points_noirs)
        num_clusters = 5

        if len(points_noirs_array) >= num_clusters:
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(points_noirs_array)
            cluster_centers = kmeans.cluster_centers_.astype(int)
            
            # Obtenez le nom du fichier avec l'extension
            filename = os.path.basename(image_path)

            # Charger le contenu actuel du fichier JSON ou créer un dictionnaire vide si le fichier est vide
            if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
                with open("data.json", "r") as json_file:
                    json_data = json.load(json_file)
            else:
                json_data = {}

            # Ajouter ou mettre à jour les informations spécifiques pour l'image actuelle
            json_data.setdefault(filename, {}).update({"centres_clusters": cluster_centers.tolist()})

            # Enregistrez le dictionnaire mis à jour dans le fichier JSON
            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file)

            return cluster_centers.tolist()

    return None

# Exemple d'utilisation :
image_path_example = "fichierImage/8.png"
centres_clusters = detect_defauts(image_path_example)

if centres_clusters is not None:
    print("Coordonnées des centres des clusters :", centres_clusters)
else:
    print("Pas de contour détecté sur l'image ou pas assez de points noirs pour effectuer le regroupement.")
