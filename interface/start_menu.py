import customtkinter as ctk

class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#f5f5dc")

        # Atributos iniciais
        self.controller = controller

        self.half_width = int(self.controller.screen_width / 2)
        self.half_height = int(self.controller.screen_height / 2)

       # Background
        self.background = ctk.CTkCanvas(self, width=self.controller.screen_width, height=self.controller.screen_width, bd=0, highlightthickness=0)
        self.background.place(x=0, y=0)

        self.background.create_image(self.half_width, self.half_height, image=self.controller.background_image)

        # Título Pokemon Game
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.28), text="Pokemon Game", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0462), "bold"), fill="#000000")
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.277), text="Pokemon Game", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0462), "bold"), fill="#9b111e")

        # Botão Criar Conta
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.388), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.462), "#1e1e1e", "#9b111e", self.controller.show_create_account)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.425), text="Criar Conta", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0222)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_create_account())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        # Botão Login
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.481), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.555), "#1e1e1e", "#9b111e", self.controller.show_login)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.518), text="Login", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0222)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_login())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
        
        # Botão Finalizar Programa
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.574), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.648), "#1e1e1e", "#9b111e", self.controller.finish_program)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.611), text="Finalizar Programa", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0222)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.finish_program())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
