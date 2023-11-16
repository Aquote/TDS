import json
import os
import tkinter as tk
from tkinter import IntVar, ttk, filedialog, messagebox
import plate_orientation
import plate_color
import plate_size
import holes
import contours

class ConformiteModule(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=4, column=8, sticky="S")
        self.create_widgets()

    def create_widgets(self):
        self.label_orientation = tk.Label(self, text="Orientation (degrés, 0 à 90):")
        self.label_orientation.grid(row=0, column=0, pady=5, sticky="w")
        self.entry_orientation = tk.Entry(self)  
        self.entry_orientation.insert(0, "0")
        self.entry_orientation.grid(row=0, column=1, pady=5)

        self.label_couleur = tk.Label(self, text="Couleur (peu importe):")
        self.label_couleur.grid(row=1, column=0, pady=5, sticky="w")
        self.couleur_options = ["Référence", "Peu Importe"]
        self.combo_couleur = ttk.Combobox(self, values=self.couleur_options, state='readonly')
        self.combo_couleur.set("Référence")
        self.combo_couleur.grid(row=1, column=1, pady=5)

        self.label_taille = tk.Label(self, text="Taille (0 à 10000):")
        self.label_taille.grid(row=2, column=0, pady=5, sticky="w")
        self.entry_taille = tk.Entry(self)
        self.entry_taille.insert(0, "0")
        self.entry_taille.grid(row=2, column=1, pady=5)

        self.label_defauts = tk.Label(self, text="Défauts (peu importe):")
        self.label_defauts.grid(row=3, column=0, pady=5, sticky="w")
        self.defauts_options = ["Référence", "Peu Importe"]
        self.combo_defauts = ttk.Combobox(self, values=self.defauts_options, state='readonly')
        self.combo_defauts.set("Référence")
        self.combo_defauts.grid(row=3, column=1, pady=5)

        self.bouton_sauvegarder = tk.Button(self, text="Sauvegarder", command=self.getData)
        self.bouton_sauvegarder.grid(row=4, column=0, pady=5, sticky="w")
    
    def setData(self):

        data = {
        "orientation" :0,
        "couleur" : 'Référence',
        "taille" : 0,
        "defauts" : 'Référence'
        }
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
                    self.setData()
                    print(orientation, couleur, taille, defauts)
            except ValueError:
                messagebox.showerror("Erreur", "L'orientation et la taille doivent être des nombres entiers.")
class MaFenetre(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("É-plaqué")
        self.geometry("1200x600")
        self.creer_interface()
        self.conformite_module = ConformiteModule(self)

    def creer_interface(self):
        bouton_charger_ref = tk.Button(self, text="Charger référence", command=self.charger_reference)
        bouton_charger_ref.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        bouton_charger_img = tk.Button(self, text="Charger image", command=self.charger_image)
        bouton_charger_img.grid(row=0, column=1, padx=10, pady=10, sticky="Nw")

        self.checkbox_orientation_var = IntVar()
        self.checkbox_orientation = tk.Checkbutton(self, text="Orientation", onvalue=1, offvalue=0, variable=self.checkbox_orientation_var)
        self.checkbox_orientation.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.checkbox_orientation.select()

        self.checkbox_couleur_var = IntVar()
        self.checkbox_couleur = tk.Checkbutton(self, text="Couleur", onvalue=1, offvalue=0, variable=self.checkbox_couleur_var)
        self.checkbox_couleur.grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.checkbox_couleur.select()

        self.checkbox_taille_var = IntVar()
        self.checkbox_taille = tk.Checkbutton(self, text="Taille", onvalue=1, offvalue=0, variable=self.checkbox_taille_var)
        self.checkbox_taille.grid(row=0, column=5, padx=10, pady=10, sticky="e")
        self.checkbox_taille.select()

        self.checkbox_defauts_var = IntVar()
        self.checkbox_defauts = tk.Checkbutton(self, text="Défauts", onvalue=1, offvalue=0, variable=self.checkbox_defauts_var)
        self.checkbox_defauts.grid(row=0, column=6, padx=10, pady=10, sticky="e")
        self.checkbox_defauts.select()

        bouton_mesurer = tk.Button(self, text="Mesurer", command=self.mesure)
        bouton_mesurer.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        bouton_comparer = tk.Button(self, text="Comparer", command=self.comparer)
        bouton_mesurer.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.treeview = ttk.Treeview(self, columns=("Référence", "Nom", "Orientation", "Couleur", "Taille", "Défauts"), show="headings")
        self.treeview.heading("Référence", text="Référence", anchor="center")
        self.treeview.heading("Nom", text="Nom", anchor="center")
        self.treeview.heading("Orientation", text="Orientation", anchor="center")
        self.treeview.heading("Couleur", text="Couleur", anchor="center")
        self.treeview.heading("Taille", text="Taille", anchor="center")
        self.treeview.heading("Défauts", text="Défauts", anchor="center")
        self.treeview.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")

        for col, width in zip(("Référence", "Orientation", "Couleur", "Taille", "Défauts"), (200, 150, 100, 100, 150)):
            self.treeview.column(col, width=width, anchor="center")

        bande_images = tk.Frame(self)
        bande_images.grid(row=2, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.treeview.tag_configure("colored_row", background="#ADD8E6")

    def charger_reference(self):
        if len(self.treeview.get_children()) != 0:
            self.treeview.delete(*self.treeview.get_children())
        fichier_reference = filedialog.askopenfilename(initialdir="./fichierImage", title="Choisir une référence", filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg;*.gif")])
        if fichier_reference:
            nom_fichier = os.path.basename(fichier_reference)
            self.treeview.insert("", "end", values=("référence", nom_fichier, "", "", "", ""), tag ="colored_row")
            self.vider_json()

    def vider_json(self):
        json_data = {}
        with open("data.json", "w") as json_file:
            json.dump(json_data, json_file)

    def charger_image(self):
        items = self.treeview.get_children()
        reference_filename = None
        for item in items:
            values = self.treeview.item(item, 'values')
            if values and values[0] == "référence":
                reference_filename = values[1]
                break
        chemin = "./fichierImage"
        fichiers = [f for f in os.listdir(chemin) if os.path.isfile(os.path.join(chemin, f)) and f != reference_filename]
        for fichier in fichiers:
            self.treeview.insert("", "end", values=("", fichier, "", "", "", ""))

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
            if values and values[0] == "référence":
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

    
    
    def comparer(self):
        pass
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

if __name__ == "__main__":
    app = MaFenetre()
    app.mainloop()
