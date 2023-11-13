import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
import json

def detect_defauts(image_path, screen=False):
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

            # Tri des centres des clusters
            sorted_cluster_centers = sorted(cluster_centers.tolist())

            # Trouver le coin supérieur gauche
            top_left_corner = min(points_noirs_array, key=lambda x: x[0] + x[1])

            # Calculer la distance entre chaque cluster et le coin supérieur gauche
            distances_to_top_left = [int(np.linalg.norm(np.array(center) - np.array(top_left_corner))) for center in sorted_cluster_centers]

            # Afficher les distances
            print("Distances entre chaque cluster et le coin supérieur gauche :", distances_to_top_left)

            # Afficher l'image avec les points rouges aux centres des clusters
            if screen:
                image_with_clusters = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                for center in cluster_centers:
                    x, y = center
                    cv2.circle(image_with_clusters, (x, y), 2, (0, 0, 255), -1)

                cv2.imshow("Image avec les points rouges aux centres des clusters", image_with_clusters)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            filename = os.path.basename(image_path)

            if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
                with open("data.json", "r") as json_file:
                    json_data = json.load(json_file)
                    json_data.setdefault(filename, {}).update({"centres_clusters": sorted_cluster_centers, "distances_to_top_left": distances_to_top_left})
            else:
                json_data = {}
                json_data = {filename: {"centres_clusters": sorted_cluster_centers, "distances_to_top_left": distances_to_top_left}}

            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file)
            return sorted_cluster_centers
        else:
            # Aucun contour détecté, ajouter "null" dans le fichier JSON
            filename = os.path.basename(image_path)

            if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
                with open("data.json", "r") as json_file:
                    json_data = json.load(json_file)
                    json_data.setdefault(filename, {}).update({"centres_clusters": "null", "distances_to_top_left": "null"})
            else:
                json_data = {}
                json_data.setdefault(filename, {}).update({"centres_clusters": "null", "distances_to_top_left": "null"})

            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file)
            return None

# Exemple d'utilisation avec l'affichage de l'image
image_path_example = "fichierImage/5.png"
centres_clusters = detect_defauts(image_path_example, screen=True)

if centres_clusters is not None:
    print("Coordonnées des centres des clusters (triés) :", centres_clusters)
else:
    print("Pas de contour détecté sur l'image ou pas assez de points noirs pour effectuer le regroupement.")
