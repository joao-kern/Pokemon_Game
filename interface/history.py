import customtkinter as ctk

class History(ctk.CTkFrame):
    def __init__ (self, parent, controller, db):
        super().__init__(parent, fg_color="#f5f5dc")

        self.parent = parent

        self.db = db

        self.controller = controller

        trainer = self.db.trainers.find_one(
                    {'_id': self.controller.user},
                    {'_id': 0, 'battles': 1, 'victories': 1, 'defeats': 1}
        )

        self.battles = trainer['battles']
        self.victories = trainer['victories']
        self.defeats = trainer['defeats']

        self.half_width = int(self.controller.screen_width / 2)
        self.half_height = int(self.controller.screen_height / 2)

        # Background
        self.background = ctk.CTkCanvas(self, width=self.controller.screen_width, height=self.controller.screen_height, bd=0, highlightthickness=0)
        self.background.place(x=0, y=0)

        self.background.create_image(self.half_width, self.half_height, image=self.controller.background_image)

        # Título Histórico
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.28), text="Histórico", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0462), "bold"), fill="#000000")
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.277), text="Histórico", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0462), "bold"), fill="#9b111e")

        # Mensagem
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.419), text=f"Batalhas: {self.battles}", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#000000", width=int(self.controller.screen_height * 0.468), anchor="center", justify="center")
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.416), text=f"Batalhas: {self.battles}", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#FFFFFF", width=int(self.controller.screen_height * 0.468), anchor="center", justify="center")

        if self.battles == 0:

            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.512), text=f"Vitórias: 0", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#000000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.509), text=f"Vitórias: 0", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#00FF00", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")


            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.604), text=f"Derrotas: 0", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#000000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.601), text=f"Derrotas: 0", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#FF0000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
        else:
            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.512), text=f"Vitórias: {self.victories} ({(self.victories / self.battles) * 100:.2f}%)", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#000000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.509), text=f"Vitórias: {self.victories} ({(self.victories / self.battles) * 100:.2f}%)", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#00FF00", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")


            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.604), text=f"Derrotas: {self.defeats} ({(self.defeats / self.battles) * 100:.2f}%)", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#000000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
            self.background.create_text(self.half_width, int(self.controller.screen_height * 0.601), text=f"Derrotas: {self.defeats} ({(self.defeats / self.battles) * 100:.2f}%)", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#FF0000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
        # Botão Ok
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.429), int(self.controller.screen_height * 0.703), int(self.controller.screen_width * 0.57), int(self.controller.screen_height * 0.787), "#1e1e1e", "#9b111e", self.controller.show_main_menu)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.745), text="Ok", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0259)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_main_menu())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))