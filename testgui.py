import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from skimage import io
from skimage.metrics import structural_similarity as ssim

class ImageComparatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Comparator")
        self.geometry("1200x600")

        self.base_image = None
        self.other_images = []
        self.last_clicked_image = None  # Nouvelle variable
        self.comparison_results = {}  # Dictionnaire pour stocker les résultats de comparaison

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH)

        images_frame = tk.Frame(main_frame)
        images_frame.pack(side=tk.TOP, fill=tk.X)

        self.reference_name = tk.StringVar()
        reference_entry = tk.Entry(images_frame, textvariable=self.reference_name, state='readonly')
        reference_entry.pack(side=tk.LEFT, padx=10)

        add_reference_button = tk.Button(images_frame, text="Ajouter Référence", command=self.add_reference_image)
        add_reference_button.pack(side=tk.LEFT, padx=10)

        remove_reference_button = tk.Button(images_frame, text="Supprimer Référence", command=self.remove_reference_image)
        remove_reference_button.pack(side=tk.LEFT, padx=10)

        self.image_labels = []
        self.reference_label = None

        # Créez un Treeview pour afficher les données
        self.treeview = ttk.Treeview(main_frame, columns=("Nom", "Orientation", "Taille", "Couleur", "Similarité"))
        self.treeview.heading("#1", text="Nom")
        self.treeview.heading("#2", text="Orientation")
        self.treeview.heading("#3", text="Taille")
        self.treeview.heading("#4", text="Couleur")
        self.treeview.heading("#5", text="Défauts")
        self.treeview.pack(expand=True, fill="both")

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(side=tk.BOTTOM, pady=10)

        add_button = tk.Button(buttons_frame, text="Ajouter Image", command=self.add_image)
        add_button.pack(side=tk.LEFT, padx=10)

        compare_button = tk.Button(buttons_frame, text="Comparer", command=self.compare_images)
        compare_button.pack(side=tk.LEFT, padx=10)

    def remove_image(self, clicked_label):
        # Supprimez l'image et l'étiquette associée
        image = self.image_labels.pop(clicked_label)
        clicked_label.pack_forget()
        # Assurez-vous que l'image est également supprimée de la liste des autres images
        if image in self.other_images:
            self.other_images.remove(image)
        # Effacez la sélection
        self.last_clicked_image = None

    def add_reference_image(self):
        reference_file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if reference_file:
            # Supprimez l'ancienne image de référence s'il y en a une
            if self.base_image:
                self.remove_reference_image()

            self.base_image = io.imread(reference_file)
            reference_filename = os.path.basename(reference_file)  # Extrait le nom du fichier
            self.reference_name.set(reference_filename)  # Utilise le nom du fichier dans le champ de référence

            # Vérifiez si l'image de référence a déjà été affichée, sinon, affichez-la
            if not self.reference_label:
                self.display_image(self.base_image, is_reference=True)

            # Mettez à jour le tableau avec le nom de l'image de référence
            self.treeview.delete(*self.treeview.get_children())  # Effacez toutes les entrées précédentes
            reference_filename = self.reference_name.get()
            self.treeview.insert("", "end", text="Référence", values=(reference_filename, "", "", "", ""))
    def display_image(self, image, is_reference=False):
            # Convertissez l'image NumPy en format d'image PIL pour affichage
            image_pil = Image.fromarray(image)
            image_pil.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image_pil)

            label = tk.Label(self, image=photo, wraplength=200)
            label.image = photo

            if is_reference:
                label.configure(highlightbackground="blue")
                self.reference_label = label
            else:
                self.image_labels[label] = image  # Stockez l'image dans le dictionnaire

            label.bind("<Button-1>", self.image_clicked)
            label.pack(side=tk.LEFT, padx=10)
            
    def image_clicked(self, event):
        clicked_label = event.widget
        if clicked_label in self.image_labels:
            # Supprimez l'image lorsqu'elle est cliquée
            self.remove_image(clicked_label)
            
    def compare_images(self):
        if self.base_image is not None:
            self.comparison_results = {}  # Réinitialisez les résultats de la comparaison
            for label, image in self.image_labels.items():
                # Comparez l'image avec l'image de référence
                similarity_score = self.calculate_similarity(self.base_image, image)

                # Stockez le résultat de la comparaison dans le dictionnaire
                image_id = self.get_image_id(label)
                self.comparison_results[image_id] = similarity_score

                # Mettez à jour le tableau avec le score de similarité
                self.update_table_with_comparison_result(image_id, similarity_score)
    
    def calculate_similarity(self, image1, image2):
        # Calculer le score de similarité entre les deux images
        return ssim(image1, image2, multichannel=True)

    def update_table_with_comparison_result(self, image_id, similarity_score):
        # Mettez à jour la ligne correspondant à l'image avec le score de similarité
        item_id = f"image_{image_id}"
        self.treeview.item(item_id, values=("", "", "", "", similarity_score))

    def get_image_id(self, label):
        # Obtenez l'identifiant de l'image à partir de son label
        for id, lbl in self.image_labels.items():
            if lbl == label:
                return id
            
            
    def remove_reference_image(self):
        self.base_image = None
        self.reference_name.set("")
        if self.reference_label:
            self.reference_label.configure(borderwidth=0, highlightbackground=None)
        self.reference_label = None

        # Supprimez la ligne de l'image de référence dans le tableau
        if self.treeview.exists("Référence"):
            self.treeview.delete("Référence")

    def add_image(self):
        image_file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if image_file:
            image = io.imread(image_file)
            self.other_images.append(image)
            self.update_images()
            print(f"Image ajoutée : {image_file}")

            # Obtenez l'index de la dernière image ajoutée
            image_index = len(self.other_images) - 1

            # Ajoutez l'image au tableau avec l'index comme identifiant
            image_filename = os.path.basename(image_file)
            self.treeview.insert("", "end", f"image_{image_index}", values=(image_filename, "", "", "", ""))

    def compare_images(self):
        if self.base_image is not None:
            self.comparison_results = {}  # Réinitialisez les résultats de la comparaison
            for image_id, image in enumerate(self.other_images):
                # Comparez l'image avec l'image de référence
                similarity_score = self.calculate_similarity(self.base_image, image)

                # Stockez le résultat de la comparaison dans le dictionnaire
                self.comparison_results[image_id] = similarity_score

                # Mettez à jour le tableau avec le score de similarité
                self.update_table_with_comparison_result(image_id, similarity_score)

    def calculate_similarity(self, image1, image2):
        # Calculer le score de similarité entre les deux images
        return ssim(image1, image2, multichannel=True)

    def update_table_with_comparison_result(self, image_id, similarity_score):
        # Mettez à jour la ligne correspondant à l'image avec le score de similarité
        item_id = f"image_{image_id}"
        self.treeview.item(item_id, values=("", "", "", "", similarity_score))

    def update_images(self):
        # Ne fait rien, car les images ne sont pas affichées
        pass
    def display_image(self, image, is_reference=False):
        # Cette fonction ne fait rien, car les images ne sont pas affichées
        pass
    def image_clicked(self, event):
        self.last_clicked_image = event.widget

if __name__ == "__main__":
    app = ImageComparatorApp()
    app.mainloop()
