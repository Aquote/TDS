import os
import tkinter as tk
from tkinter import IntVar, ttk, filedialog

class MaFenetre(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ma Fenêtre")
        self.geometry("1200x600")
        self.creer_interface()

    def creer_interface(self):
        
        # Bouton Charger Référence
        bouton_charger_ref = tk.Button(self, text="Charger référence", command=self.charger_reference)
        bouton_charger_ref.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Bouton Charger Image
        bouton_charger_img = tk.Button(self, text="Charger image", command=self.charger_image)
        bouton_charger_img.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Bouton Comparer
        bouton_comparer = tk.Button(self, text="Comparer", command=lambda: self.comparer(
            checkbox_orientation.get(),
            checkbox_couleur.get(),
            checkbox_taille.get(),
            checkbox_defauts.get()
        ))
        bouton_comparer.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        onvalue=True
        offvalue=False
        
        global checkbox_orientation, checkbox_couleur, checkbox_taille, checkbox_defauts
        checkbox_orientation = IntVar()
        checkbox_couleur = IntVar()
        checkbox_taille = IntVar()
        checkbox_defauts = IntVar()
        
        checkbox_orientation = tk.Checkbutton(self, text="Orientation",onvalue=onvalue, offvalue=offvalue, variable=checkbox_orientation)
        checkbox_orientation.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        checkbox_orientation.select()

        checkbox_couleur = tk.Checkbutton(self, text="Couleur", onvalue=onvalue, offvalue=offvalue, variable=checkbox_couleur)
        checkbox_couleur.grid(row=0, column=4, padx=10, pady=10, sticky="e")

        checkbox_taille = tk.Checkbutton(self, text="Taille",onvalue=onvalue, offvalue=offvalue, variable=checkbox_taille)
        checkbox_taille.grid(row=0, column=5, padx=10, pady=10, sticky="e")

        checkbox_defauts = tk.Checkbutton(self, text="Défauts",onvalue=onvalue, offvalue=offvalue, variable=checkbox_defauts)
        checkbox_defauts.grid(row=0, column=6, padx=10, pady=10, sticky="e")


        self.treeview = ttk.Treeview(self, columns=("Référence","Nom" ,"Orientation", "Couleur", "Taille", "Défauts"), show="headings")
        self.treeview.heading("Référence", text="Référence", anchor="center")
        self.treeview.heading("Nom", text="Nom", anchor="center")
        self.treeview.heading("Orientation", text="Orientation", anchor="center")
        self.treeview.heading("Couleur", text="Couleur", anchor="center")
        self.treeview.heading("Taille", text="Taille", anchor="center")
        self.treeview.heading("Défauts", text="Défauts", anchor="center")
        self.treeview.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")


        for col, width in zip(("Référence", "Orientation", "Couleur", "Taille", "Défauts"), (200, 150, 100, 100, 150)):
            self.treeview.column(col, width=width, anchor="center")

        # Images en bande
        bande_images = tk.Frame(self)
        bande_images.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Ajuster la colonne 0 pour qu'elle prenne 100% de la largeur
        self.grid_columnconfigure(0, weight=1)
        #définir le tag
        self.treeview.tag_configure("colored_row", background="#ADD8E6")

    def charger_reference(self):
        # Effacer tous les éléments du Treeview s'il y en a
        if len(self.treeview.get_children()) != 0:
            self.treeview.delete(*self.treeview.get_children())
        # Ouvrir une boîte de dialogue pour choisir un fichier
        fichier_reference = filedialog.askopenfilename(initialdir="./fichierImage", title="Choisir une référence", filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg;*.gif")])

        # Ajouter le fichier de référence au Treeview avec une couleur spécifique
        if fichier_reference:
            nom_fichier = os.path.basename(fichier_reference)
            self.treeview.insert("", "end", values=("référence", nom_fichier, "", "", "", ""), tag ="colored_row")

    def charger_image(self):
            # Obtenez tous les éléments du Treeview
        items = self.treeview.get_children()

        # Parcourez les éléments et supprimez ceux qui n'ont pas "Référence" dans la colonne appropriée
        for item in items:
            values = self.treeview.item(item, 'values')
            if values and values[0] != "référence":
                self.treeview.delete(item)

        # Obtenez la liste des fichiers d'images dans le répertoire ./fichierImage
        chemin = "./fichierImage"
        fichiers = [f for f in os.listdir(chemin) if os.path.isfile(os.path.join(chemin, f))]

        # Ajoutez les fichiers d'images au Treeview
        for fichier in fichiers:
            self.treeview.insert("", "end", values=("", fichier, "", "", "", ""))
        
    def comparer(orientation,couleur,taille,defaut):
        pass
       
       
        # À vous de remplir cette partie avec la logique pour afficher les images en bande

if __name__ == "__main__":
    app = MaFenetre()
    app.mainloop()
