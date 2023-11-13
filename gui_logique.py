# gui_logique.py
import os
from PIL import Image, ImageTk
from skimage import io, metrics
import tkinter as tk
from tkinter import filedialog, ttk
from gui_structure import ImageComparatorGUI

class ImageComparatorController:
    def __init__(self):
        self.gui = None  # L'instance de GUI sera définie ultérieurement
        self.base_image = None
        self.other_images = []
        self.last_clicked_image = None
        self.comparison_results = {}

    def set_gui(self, gui):
        self.gui = gui  # Définir l'instance de GUI

    def add_reference_image(self):
        reference_file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if reference_file:
            if self.base_image:
                self.clear_reference_image()

            self.base_image = io.imread(reference_file)
            reference_filename = os.path.basename(reference_file)
            self.gui.reference_name.set(reference_filename)

            if not self.gui.reference_label:
                self.display_image(self.base_image, is_reference=True)

            self.gui.treeview.delete(*self.gui.treeview.get_children())
            reference_filename = self.gui.reference_name.get()
            self.gui.treeview.insert("", "end", text="Référence", values=(reference_filename, "", "", "", ""))
            self.display_image(self.base_image, True)

    def clear_reference_image(self):
        self.base_image = None
        self.gui.reference_name.set("")
        if self.gui.reference_label:
            self.gui.reference_label.configure(borderwidth=0, highlightbackground=None)
        self.gui.reference_label = None

        if self.gui.treeview.exists("Référence"):
            self.gui.treeview.delete("Référence")

    def display_image(self, image, is_reference=False):
        image_pil = Image.fromarray(image)
        image_pil.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image_pil)

        label = tk.Label(self.gui, image=photo, wraplength=200)
        label.image = photo

        if is_reference:
            if not self.gui.reference_label:
                label.configure(highlightbackground="blue")
                self.gui.reference_label = label
                label.pack(side=tk.LEFT, padx=10)
        else:
            self.gui.image_labels[label] = image
            label.bind("<Button-1>", self.image_clicked)
            label.pack(side=tk.LEFT, padx=10)

    def image_clicked(self, event):
        self.last_clicked_image = event.widget

    def compare_images(self):
        if self.base_image is not None:
            self.comparison_results = {}
            for label, image in self.gui.image_labels.items():
                similarity_score = self.calculate_similarity(self.base_image, image)
                image_id = self.get_image_id(label)
                self.comparison_results[image_id] = similarity_score
                self.update_table_with_comparison_result(image_id, similarity_score)

    def calculate_similarity(self, image1, image2):
        color = self.gui.checkbox_var_color.get()
        size = self.gui.checkbox_var_size.get()
        orientation = self.gui.checkbox_var_orientation.get()
        defects = self.gui.checkbox_var_defects.get()

        selected_options = [color, size, orientation, defects]

        # Utilisez les options sélectionnées pour calculer le score de similarité
        similarity_score = sum(selected_options) / len(selected_options)

        return similarity_score

    def update_table_with_comparison_result(self, image_id, similarity_score):
        item_id = f"image_{image_id}"
        self.gui.treeview.item(item_id, values=("", "", "", "", similarity_score))

    def get_image_id(self, label):
        for id, lbl in self.gui.image_labels.items():
            if lbl == label:
                return id

    def remove_all_images(self):
        for label in self.gui.image_labels.keys():
            label.pack_forget()
        self.gui.image_labels = {}
        self.other_images = []

    def add_image(self):
        image_file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if image_file:
            image = io.imread(image_file)
            self.other_images.append(image)
            self.update_images()

            image_index = len(self.other_images) - 1
            image_filename = os.path.basename(image_file)
            self.gui.treeview.insert("", "end", f"image_{image_index}", values=(image_filename, "", "", "", ""))

    def update_images(self):
        pass
