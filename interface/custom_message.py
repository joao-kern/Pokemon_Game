import customtkinter as ctk

class CustomMessage(ctk.CTkFrame):
    def __init__(self, parent, controller, message, next_frame):
        super().__init__(parent, fg_color="#f5f5dc")
        """
        Mensagem Customizada
        """
        
        # Atributos iniciais

        self.controller = controller

        self.half_width = int(self.controller.screen_width / 2)
        self.half_height = int(self.controller.screen_height / 2)

        # Background
        self.background = ctk.CTkCanvas(self, width=self.controller.screen_width, height=self.controller.screen_height, bd=0, highlightthickness=0)
        self.background.place(x=0, y=0)

        self.background.create_image(self.half_width, self.half_height, image=self.controller.background_image)

        # Mensagem
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.512), text=message, font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#000000", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.509), text=message, font=("PKMN RBYGSC", int(self.controller.screen_height * 0.035), "bold"), fill="#9b111e", width=int(self.controller.screen_width * 0.468), anchor="center", justify="center")

        # Botão Ok
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.429), int(self.controller.screen_height * 0.611), int(self.controller.screen_width * 0.57), int(self.controller.screen_height * 0.685), "#1e1e1e", "#9b111e", next_frame)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.648), text="Ok", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.025)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: next_frame())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))