import customtkinter as ctk
from interface.gui import GUI
from model.db import DB

def main():
    db = DB()
    root = ctk.CTk(fg_color="#f5f5dc")
    app = GUI(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()
    