# gui_structure.py
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from skimage import io

class ImageComparatorGUI(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Image Comparator")
        self.geometry("1200x600")

        self.controller = controller
        if controller:
            self.controller.set_gui(self)  # Passer l'instance de GUI au contrôleur

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH)

        images_frame = tk.Frame(main_frame)
        images_frame.pack(side=tk.TOP, fill=tk.X)

        self.reference_name = tk.StringVar()
        reference_entry = tk.Entry(images_frame, textvariable=self.reference_name, state='readonly')
        reference_entry.pack(side=tk.LEFT, padx=10)

        add_reference_button = tk.Button(images_frame, text="Ajouter Référence", command=self.controller.add_reference_image)
        add_reference_button.pack(side=tk.LEFT, padx=10)

        remove_reference_button = tk.Button(images_frame, text="Supprimer Référence", command=self.controller.clear_reference_image)
        remove_reference_button.pack(side=tk.LEFT, padx=10)

        self.image_labels = {}
        self.reference_label = None

        self.treeview = ttk.Treeview(main_frame, columns=("Nom", "Orientation", "Taille", "Couleur", "Similarité"))
        self.treeview.heading("#1", text="Nom")
        self.treeview.heading("#2", text="Orientation")
        self.treeview.heading("#3", text="Taille")
        self.treeview.heading("#4", text="Couleur")
        self.treeview.heading("#5", text="Défauts")
        self.treeview.pack(expand=True, fill="both")

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(side=tk.BOTTOM, pady=10)

        add_button = tk.Button(buttons_frame, text="Ajouter Image", command=self.controller.add_image)
        add_button.pack(side=tk.LEFT, padx=10)

        compare_button = tk.Button(buttons_frame, text="Comparer", command=self.controller.compare_images)
        compare_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(buttons_frame, text="Effacer Image de Référence", command=self.controller.clear_reference_image)
        clear_button.pack(side=tk.LEFT, padx=10)

        # Checkboxes for comparison options
        self.checkbox_var_color = tk.BooleanVar()
        self.checkbox_var_size = tk.BooleanVar()
        self.checkbox_var_orientation = tk.BooleanVar()
        self.checkbox_var_defects = tk.BooleanVar()

        color_checkbox = tk.Checkbutton(buttons_frame, text="Orientation", variable=self.checkbox_var_color)
        size_checkbox = tk.Checkbutton(buttons_frame, text="Taille", variable=self.checkbox_var_size)
        orientation_checkbox = tk.Checkbutton(buttons_frame, text="Couleur", variable=self.checkbox_var_orientation)
        defects_checkbox = tk.Checkbutton(buttons_frame, text="Défauts", variable=self.checkbox_var_defects)

        color_checkbox.pack(side=tk.LEFT, padx=10)
        size_checkbox.pack(side=tk.LEFT, padx=10)
        orientation_checkbox.pack(side=tk.LEFT, padx=10)
        defects_checkbox.pack(side=tk.LEFT, padx=10)

    def set_controller(self, controller):
        self.controller = controller

