import cv2
import numpy as np

def detecter_contours(image_path, screen=False):
    """
    Détecte les contours et les défauts à l'intérieur des contours d'une plaque à partir d'une image.

    Paramètres:
    - image_path (str): Chemin vers le fichier image.
    - screen (bool): Si True, affiche l'image avec les contours des défauts.

    Retourne:
    - List[List[List[int]]] or None: Liste des contours des défauts, ou None si la détection est impossible.
    """
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Redimensionner l'image à 600x400 pixels
    image = cv2.resize(image, (600, 400))

    # Appliquer un filtre gaussien pour réduire le bruit
    image_blur = cv2.GaussianBlur(image, (5, 5), 0)

    # Utiliser la méthode de Canny pour détecter les contours
    edges = cv2.Canny(image_blur, 50, 150)

    # Trouver les contours dans l'image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Définir une taille minimale pour les contours (ajustez selon vos besoins)
    min_contour_size = 20

    # Si des contours sont détectés
    if contours:
        # Filtrer les contours en fonction de leur taille et position
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_size and 50 < cnt[0][0][0] < 550 and 50 < cnt[0][0][1] < 350]
        
        if screen:
            if len(filtered_contours) > 0:
                # Dessiner les contours sur une image vierge
                contours_image = np.zeros_like(image)
                cv2.drawContours(contours_image, filtered_contours, -1, 255, thickness=cv2.FILLED)  # Remplir les contours en blanc (255)
                
                # Trouver les contours à l'intérieur des contours de la plaque
                defects_contours = cv2.findContours(contours_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                
                # Si des contours de défauts sont détectés
                if defects_contours:
                    # Dessiner les contours des défauts en rouge sur l'image originale
                    image_with_defects = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                    cv2.drawContours(image_with_defects, defects_contours, -1, (0, 0, 255), 2)
                    
                    # Afficher l'image avec les contours des défauts
                    cv2.imshow("Contours de la plaque", image_with_defects)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            else:
                print("Pas de contour détecté sur l'image.")
        return defects_contours
    else:
        print("Pas de contour détecté sur l'image.")
        return None

# Exemple d'utilisation
image_path = "fichierImage/8.png"
defauts_contours = detecter_contours(image_path, screen=True)
