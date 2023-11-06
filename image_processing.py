import cv2

def compare_plate_sizes(w1, h1, w2, h2):
    if w2 < w1 and h2 < h1:
        return "plus petite"
    elif w2 > w1 and h2 > h1:
        return "plus grande"
    else:
        return "de taille égale"

def determine_plate_orientation(contours):
    angle = 0  # Angle par défaut

    if len(contours) > 4:
        # Si suffisamment de contours sont trouvés, calculez l'angle d'orientation
        rect = cv2.minAreaRect(contours[0])
        angle = rect[2]

    return angle

def process_image(image1, image2, filename1, filename2):
    # Convertir les images en niveaux de gris
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Appliquer le seuillage pour binariser les images et obtenir des masques des parties blanches
    _, binary_mask1 = cv2.threshold(image1_gray, 135, 255, cv2.THRESH_BINARY)
    _, binary_mask2 = cv2.threshold(image2_gray, 135, 255, cv2.THRESH_BINARY)

    # Identifier les contours dans les masques binaires
    contours1, _ = cv2.findContours(binary_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Définir des valeurs par défaut si aucun contour n'est trouvé
    w1, h1 = 0, 0
    w2, h2 = 0, 0

    if len(contours1) > 0 and len(contours2) > 0:
        x1, y1, w1, h1 = cv2.boundingRect(contours1[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours2[0])

        # Comparer les dimensions des plaques
        size_comparison = compare_plate_sizes(w1, h1, w2, h2)
        print(f"La plaque est {size_comparison} que la plaque de référence.")

        # Déterminer l'orientation des plaques
        orientation1 = determine_plate_orientation(contours1)
        orientation2 = determine_plate_orientation(contours2)

        print(f"Orientation de la plaque de référence : {orientation1} degrés")
        print(f"Orientation de la deuxième plaque : {orientation2} degrés")
        
    # Redimensionner les images pour les afficher en 600x500
    resized_image1 = cv2.resize(image1, (600, 500))
    resized_image2 = cv2.resize(image2, (600, 500))

    # Afficher l'image marquée avec le nom du fichier
    cv2.imshow(filename1, resized_image1)
    cv2.imshow(filename2, resized_image2)

    # Attendez une touche et fermez les fenêtres d'affichage
    cv2.waitKey(0)
    cv2.destroyAllWindows()
