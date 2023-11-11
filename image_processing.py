import cv2

def resize_image(image, target_width, target_height):
    """Redimensionne l'image à la taille cible."""
    return cv2.resize(image, (target_width, target_height))

def increase_contrast(image):
    """Augmente le contraste de l'image en utilisant l'égalisation d'histogramme."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    contrasted = cv2.merge([equalized, equalized, equalized])
    return contrasted

def edge_detection(image):
    """Applique la détection de bord à l'image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges

def find_contours(image):
    """Trouve les contours dans l'image."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(image, contours):
    """Dessine les contours sur l'image."""
    drawn_image = image.copy()
    cv2.drawContours(drawn_image, contours, -1, (0, 255, 0), 2)
    return drawn_image

def compare_plate_size_percentage(w, h, ref_w, ref_h):
    """Compare les dimensions de la plaque par rapport à la plaque de référence."""
    percent_w = (w / ref_w) * 100
    percent_h = (h / ref_h) * 100
    return percent_w, percent_h

def compare_plate_size(w, h, ref_width, ref_height):
    """Compare les dimensions de la plaque par rapport à la plaque de référence."""
    plate_size_comparison = compare_plate_sizes(w, h, ref_width, ref_height)
    return plate_size_comparison

def compare_plate_sizes(w1, h1, w2, h2):
    """Compare les dimensions de deux plaques."""
    if w2 < w1 and h2 < h1:
        return "plus petite que"
    elif w2 > w1 and h2 > h1:
        return "plus grande que"
    else:
        return "de taille egale a"

# Charger vos images ici (image et ref_image)
image_path = "./fichierImage/1.png"
ref_image_path = "./fichierImage/2.png"

# Définir les dimensions de la plaque de référence (à titre d'exemple)
ref_width = 100
ref_height = 100

# Charger les images
image = cv2.imread(image_path)
ref_image = cv2.imread(ref_image_path)

# Appeler la fonction de comparaison pour l'image
w, h, drawn_image = compare_plate_size(image_path, ref_width, ref_height, "nom_image")
# Redimensionner les images
resized_image = resize_image(drawn_image, 600, 400)

# Afficher les résultats
print(f"Dimensions de l'image : Largeur = {w}, Hauteur = {h}")

# Appeler la fonction de comparaison pour l'image de référence
ref_w, ref_h, ref_drawn_image = compare_plate_size(ref_width, ref_height, ref_width, ref_height)

# Redimensionner les images
resized_ref_image = resize_image(ref_drawn_image, 600, 400)

# Afficher les résultats
print(f"Dimensions de l'image de référence : Largeur = {ref_w}, Hauteur = {ref_h}")

# Afficher l'image avec les contours dessinés
cv2.imshow("Contours Image", resized_image)
cv2.imshow("Contours Image de Référence", resized_ref_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
