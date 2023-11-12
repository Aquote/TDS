# main.py
import gui_logique
import gui_structure

if __name__ == "__main__":
    gui = gui_structure.ImageComparatorGUI()
    controller = gui_logique.ImageComparatorController()
    gui.set_controller(controller)
    gui.mainloop()
