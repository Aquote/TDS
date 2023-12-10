import json
from math import e
import os
import re
import tkinter as tk
from tkinter import IntVar, ttk, filedialog, messagebox
from turtle import width

from matplotlib.pylab import f
import plate_orientation
import plate_color
import plate_size
import holes
import contours

class ConformiteModule(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=8, sticky="S")
        self.create_widgets()

    def create_widgets(self):
        # Créer un cadre pour les widgets d'entrée et de sélection
        cadre_widgets = tk.Frame(self)
        cadre_widgets.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Ajouter les widgets dans le cadre
        self.label_orientation = tk.Label(cadre_widgets, text="Orientation (degrés, 0 à 90):")
        self.label_orientation.grid(row=0, column=0, pady=5, sticky="w")
        self.entry_orientation = tk.Entry(cadre_widgets)
        self.entry_orientation.insert(0, "0")
        self.entry_orientation.grid(row=0, column=1, pady=5)

        self.label_couleur = tk.Label(cadre_widgets, text="Couleur (peu importe):")
        self.label_couleur.grid(row=1, column=0, pady=5, sticky="w")
        self.couleur_options = ["Reference", "Peu Importe"]
        self.combo_couleur = ttk.Combobox(cadre_widgets, values=self.couleur_options, state='readonly')
        self.combo_couleur.set("Reference")
        self.combo_couleur.grid(row=1, column=1, pady=5)

        self.label_taille = tk.Label(cadre_widgets, text="Taille (0 à 10000):")
        self.label_taille.grid(row=2, column=0, pady=5, sticky="w")
        self.entry_taille = tk.Entry(cadre_widgets)
        self.entry_taille.insert(0, "0")
        self.entry_taille.grid(row=2, column=1, pady=5)

        self.label_defauts = tk.Label(cadre_widgets, text="Défauts (peu importe):")
        self.label_defauts.grid(row=3, column=0, pady=5, sticky="w")
        self.defauts_options = ["Reference", "Peu Importe"]
        self.combo_defauts = ttk.Combobox(cadre_widgets, values=self.defauts_options, state='readonly')
        self.combo_defauts.set("Reference")
        self.combo_defauts.grid(row=3, column=1, pady=5)

        self.bouton_sauvegarder = tk.Button(cadre_widgets, text="Sauvegarder", command=self.getData)
        self.bouton_sauvegarder.grid(row=4, column=0, pady=5, sticky="w")
    
    
    def getData(self):
        orientation = self.entry_orientation.get()
        couleur = self.combo_couleur.get()
        taille = self.entry_taille.get()
        defauts = self.combo_defauts.get()
        if orientation == "" or taille == "":
            messagebox.showerror("Erreur", "Veuillez entrer une valeur pour l'orientation et la taille.")
        else:
            try:
                orientation = int(orientation)
                taille = int(taille)
                if orientation < 0 or orientation > 90:
                    messagebox.showerror("Erreur", "L'orientation doit être comprise entre 0 et 90.")
                elif taille < 0 or taille > 10000:
                    messagebox.showerror("Erreur", "La taille doit être comprise entre 0 et 10000.")
                else:
                    data = {
                        "orientation": orientation,
                        "couleur": couleur,
                        "taille": taille,
                        "defauts": defauts
                    }
                    with open("tolerance.json", "w") as file:
                        json.dump(data, file)
                    print(orientation, couleur, taille, defauts)
            except ValueError:
                messagebox.showerror("Erreur", "L'orientation et la taille doivent être des nombres entiers.")

class MaFenetre(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("É-plaqué")
        self.geometry("1200x750")
        self.creer_interface()
        self.conformite_module = ConformiteModule(self)

        self.reference_image = None  # Pour stocker l'image de Reference
        self.current_selected_image_path = None
        self.label_image = None  # Initialisez à None pour pouvoir vérifier plus tard s'il faut créer ou mettre à jour l'image

        
    def creer_interface(self):
        # Cadre principal
        cadre_principal = tk.Frame(self)
        cadre_principal.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Cadre pour les boutons de chargement
        cadre_chargement = tk.Frame(cadre_principal)
        cadre_chargement.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        bouton_charger_ref = tk.Button(cadre_chargement, text="Charger Reference", command=self.charger_reference, width=15, height=2)
        bouton_charger_ref.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        bouton_charger_img = tk.Button(cadre_chargement, text="Charger image", command=self.charger_image, width=15, height=2)
        bouton_charger_img.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Cadre pour les boutons d'actions
        cadre_boutons_actions = tk.Frame(cadre_principal)
        cadre_boutons_actions.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        bouton_mesurer = tk.Button(cadre_boutons_actions, text="Mesurer", command=self.mesure, width=15, height=2)
        bouton_mesurer.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        bouton_comparer = tk.Button(cadre_boutons_actions, text="Comparer", command=self.comparer_tout, width=15, height=2)
        bouton_comparer.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Cadre pour les cases à cocher
        cadre_cases_a_cocher = tk.Frame(self)
        cadre_cases_a_cocher.grid(row=0, column=2, padx=10, pady=10, sticky="nw")

        self.checkbox_orientation_var = tk.IntVar()
        self.checkbox_orientation = tk.Checkbutton(cadre_cases_a_cocher, text="Orientation", onvalue=1, offvalue=0, variable=self.checkbox_orientation_var)
        self.checkbox_orientation.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.checkbox_orientation.select()

        self.checkbox_couleur_var = tk.IntVar()
        self.checkbox_couleur = tk.Checkbutton(cadre_cases_a_cocher, text="Couleur", onvalue=1, offvalue=0, variable=self.checkbox_couleur_var)
        self.checkbox_couleur.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.checkbox_couleur.select()

        self.checkbox_taille_var = tk.IntVar()
        self.checkbox_taille = tk.Checkbutton(cadre_cases_a_cocher, text="Taille", onvalue=1, offvalue=0, variable=self.checkbox_taille_var)
        self.checkbox_taille.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.checkbox_taille.select()

        self.checkbox_defauts_var = tk.IntVar()
        self.checkbox_defauts = tk.Checkbutton(cadre_cases_a_cocher, text="Défauts", onvalue=1, offvalue=0, variable=self.checkbox_defauts_var)
        self.checkbox_defauts.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.checkbox_defauts.select()

        # Cadre pour le Treeview
        cadre_treeview = tk.Frame(self)
        cadre_treeview.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.treeview = ttk.Treeview(cadre_treeview, columns=("Reference", "Nom", "Orientation", "Couleur", "Taille", "Défauts"), show="headings")
        self.treeview.heading("Reference", text="Reference", anchor="center")
        self.treeview.heading("Nom", text="Nom", anchor="center")
        self.treeview.heading("Orientation", text="Orientation", anchor="center")
        self.treeview.heading("Couleur", text="Couleur", anchor="center")
        self.treeview.heading("Taille", text="Taille", anchor="center")
        self.treeview.heading("Défauts", text="Défauts", anchor="center")
        self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for col, width in zip(("Reference", "Orientation", "Couleur", "Taille", "Défauts"), (100, 150, 100, 100, 150)):
            self.treeview.column(col, width=width, anchor="center")

        # Cadre pour les images
        bande_images = tk.Frame(self)
        bande_images.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Définition de la couleur de fond de la Reference
        self.grid_columnconfigure(0, weight=1)
        self.treeview.tag_configure("colored_row", background="#ADD8E6")
        self.treeview.tag_configure("red_row", background="#FBAA99")
        self.treeview.tag_configure("green_row", background="#77DD77")

    def charger_reference(self):
        if len(self.treeview.get_children()) != 0:
            self.treeview.delete(*self.treeview.get_children())
        fichier_reference = filedialog.askopenfilename(initialdir="./fichierImage", title="Choisir une Reference", filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg;*.gif")])
        if fichier_reference:
            nom_fichier = os.path.basename(fichier_reference)
            self.treeview.insert("", "end", values=("Reference", nom_fichier, "", "", "", ""), tag ="colored_row")
            self.vider_json()

            # Charger l'image de Reference et l'afficher dans l'interface
            self.reference_image = tk.PhotoImage(file=fichier_reference).subsample(20)
            self.label_reference = tk.Label(self, image=self.reference_image)
            self.label_reference.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def vider_json(self):
        json_data = {}
        with open("data.json", "w") as json_file:
            json.dump(json_data, json_file)

    def charger_image(self):
        items = self.treeview.get_children()
        reference_filename = None
        for item in items:
            values = self.treeview.item(item, 'values')
            if values and values[0] == "Reference":
                reference_filename = values[1]
                break
        chemin = "./fichierImage"
        fichiers = [f for f in os.listdir(chemin) if os.path.isfile(os.path.join(chemin, f)) and f != reference_filename]
        for fichier in fichiers:
            already_exists = False
            for item in items:
                values = self.treeview.item(item, 'values')
                if values and values[1] == fichier:
                    already_exists = True
                    break
            if not already_exists:
                self.treeview.insert("", "end", values=("", fichier, "", "", "", ""))
                self.current_selected_image_path = os.path.join("./fichierImage", fichier)  # Mettre à jour le chemin de l'image sélectionnée ici
        # Ajout d'un événement pour sélectionner une image dans le treeview
        self.treeview.bind("<<TreeviewSelect>>", self.selectionner_image)

    def selectionner_image(self, event):
        selected_item = self.treeview.selection()[0]  # Obtenir l'élément sélectionné dans le treeview
        values = self.treeview.item(selected_item, 'values')
        if values and values[0] != "Reference":  # Vérifier si l'élément sélectionné n'est pas la Reference
            image_filename = values[1]
            self.current_selected_image_path = os.path.join("./fichierImage", image_filename)
            self.afficher_image_reference()

    def mesure(self):
        orientation_bool = self.checkbox_orientation_var.get()
        couleur_bool = self.checkbox_couleur_var.get()
        taille_bool = self.checkbox_taille_var.get()
        defaut_bool = self.checkbox_defauts_var.get()
        print(orientation_bool, couleur_bool, taille_bool, defaut_bool)
        items = self.treeview.get_children()
        for item in items:
            values = self.treeview.item(item, 'values')
            if values:
                image_filename = values[1]
                image_path = os.path.join("./fichierImage", image_filename)
                results = {}
                if orientation_bool:
                    results["orientation"] = plate_orientation.determine_plate_orientation(image_path)
                if couleur_bool:
                    results["couleur"] = plate_color.determine_plate_color(image_path, False)
                if taille_bool:
                    results["dimensions"] = plate_size.measure_contour_dimensions(image_path)
                if defaut_bool:
                    results["defauts"] = holes.detect_defauts(image_path, False)
                self.maj_treeview(image_filename, results)
        reference_item = None
        for item in items:
            values = self.treeview.item(item, 'values')
            if values and values[0] == "Reference":
                reference_item = item
                break
        if reference_item:
            reference_filename = self.treeview.item(reference_item, 'values')[1]
            reference_path = os.path.join("./fichierImage", reference_filename)
            reference_results = {}
            if orientation_bool:
                reference_results["orientation"] = plate_orientation.determine_plate_orientation(reference_path)
            if couleur_bool:
                reference_results["couleur"] = plate_color.determine_plate_color(reference_path, False)
            if taille_bool:
                reference_results["dimensions"] = plate_size.measure_contour_dimensions(reference_path)
            if defaut_bool:
                reference_results["defauts"] = holes.detect_defauts(reference_path, False)
            self.maj_treeview(reference_filename, reference_results)

    def afficher_image_reference(self):
        if self.current_selected_image_path:
            if self.label_image:
                self.label_image.grid_forget()  # Dissocie l'image de la grille sans la détruire
                self.label_image = None  # Réinitialise la Reference à l'image

            new_photo = tk.PhotoImage(file=self.current_selected_image_path).subsample(20)
            self.label_image = tk.Label(self, image=new_photo)
            self.label_image.image = new_photo
            self.label_image.grid(row=3, column=1, padx=10, pady=10, sticky="w")


    def comparer_orientation(self,reference_item,value,tolerance):
        if value != '' or reference_item != '':
            lower_orientation = reference_item - tolerance
            upper_orientation = reference_item + tolerance
            if lower_orientation <= value <= upper_orientation:
                return True
            else:
                return False
        else:
            return True

    def comparer_couleur(self,reference_item,value,tolerance):
            if tolerance == "Reference":
                if value == reference_item:
                    return True
                else:
                    return False
            else:
                return True
               
            
    def comparer_taille(self,reference_item,values,tolerance):
        
        if values != '' or reference_item != '':
 
            widthref, heightref = map(int,reference_item.split(" x "))
            width, height = map(int,values.split(" x "))

            lower_taille_width= widthref - tolerance
            upper_taille_width = widthref+ tolerance

            lower_taille_height = heightref - tolerance
            upper_taille_height = heightref + tolerance

            if (lower_taille_width <= width <= upper_taille_width) and (lower_taille_height <= height <= upper_taille_height):
                return True
            else:
                return False
            
        else:
            return True

    def comparer_defauts(self,reference_item,values,tolerance):
        if tolerance == "Reference":
            if values == reference_item:
                return True
            else:
                return False
                    
        else:
            return True
                
    def comparer_tout(self):
        # Load tolerance data from "tolerance.json"
        with open("tolerance.json", "r") as file:
            tolerance = json.load(file)

        # Get the reference item
        reference_item = None
        items = self.treeview.get_children()
        for item in items:
            values = self.treeview.item(item, 'values')
            if values and values[0] == "Reference":
                reference_item = values
                break

        if not reference_item:
            messagebox.showerror("Erreur", "Veuillez charger une image de référence.")
            return

        for item in items:
            values = self.treeview.item(item, 'values')
            if not values or values[0] == "Reference":
                continue

            is_orientation_ok = self.comparer_orientation(reference_item[2], values[2], tolerance["orientation"])
            is_couleur_ok = self.comparer_couleur(reference_item[3], values[3], tolerance["couleur"])
            is_taille_ok = self.comparer_taille(reference_item[4], values[4], tolerance["taille"])
            is_defauts_ok = self.comparer_defauts(reference_item[5], values[5], tolerance["defauts"])

            if all([is_orientation_ok, is_couleur_ok, is_taille_ok, is_defauts_ok]):
                self.treeview.item(item, tags="green_row")
            else:
                self.treeview.item(item, tags="red_row")


    def maj_treeview(self, image_filename, results):
        item_id = None
        for item in self.treeview.get_children():
            values = self.treeview.item(item, 'values')
            if values and values[1] == image_filename:
                item_id = item
                break
        if item_id:
            if "orientation" in results:
                self.treeview.set(item_id, "Orientation", results["orientation"])
            if "couleur" in results:
                self.treeview.set(item_id, "Couleur", results["couleur"])
            if "dimensions" in results:
                taille_formattee = f"{results['dimensions']['longueur_totale']} x {results['dimensions']['largeur_totale']}"
                self.treeview.set(item_id, "Taille", taille_formattee)
            if "defauts" in results:
                self.treeview.set(item_id, "Défauts", "Oui" if results["defauts"] else "Non")

            # Mise à jour de self.current_selected_image_path
            self.current_selected_image_path = os.path.join("./fichierImage", image_filename)

            # Affichage de l'image référente
            self.afficher_image_reference()
    
if __name__ == "__main__":
    app = MaFenetre()
    app.mainloop()
