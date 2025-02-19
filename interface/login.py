import customtkinter as ctk

class Login(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, fg_color="#f5f5dc")

        # Atributos iniciais
        self.controller = controller

        self.db = db

        self.half_width = int(self.controller.screen_width / 2)
        self.half_height = int(self.controller.screen_height / 2)

        # Background
        self.background = ctk.CTkCanvas(self, width=self.controller.screen_width, height=self.controller.screen_width, bd=0, highlightthickness=0)
        self.background.place(x=0, y=0)

        self.background.create_image(self.half_width, self.half_height, image=self.controller.background_image)

        # Título Criar Conta
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.28), text="Login", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.037), "bold"), fill="#000000")
        self.background.create_text(self.half_width, int(self.controller.screen_height * 0.277), text="Login", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.037), "bold"), fill="#9b111e")

        # Username
        usarname_text = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.388), text="Nome de Treinador", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.025)), fill="#000000")
        self.username_entry = ctk.CTkEntry(self, font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0231)), bg_color="#79caf9", width=int(self.controller.screen_width * 0.234), height=int(self.controller.screen_height * 0.037))
        self.username_entry.place(anchor="center", x=self.half_width, y= int(self.controller.screen_height * 0.444))

        # Password
        password_text = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.5), text="Senha", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.025)), fill="#000000")
        self.password_entry = ctk.CTkEntry(self, font=("Arial", int(self.controller.screen_height * 0.0277), "bold"), show="*", bg_color="#79caf9", width=int(self.controller.screen_width * 0.234), height=int(self.controller.screen_height * 0.02))
        self.password_entry.place(anchor="center", x=self.half_width, y=int(self.controller.screen_height * 0.564))
        
        # Botão Entrar
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.505), int(self.controller.screen_height * 0.666), int(self.controller.screen_width * 0.625), int(self.controller.screen_height * 0.74), "#1e1e1e", "#9b111e", self.verify_account)
        text_id = self.background.create_text(int(self.controller.screen_width * 0.565), int(self.controller.screen_height * 0.7), text="Login", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0222)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.verify_account())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        # Botão Voltar
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.375), int(self.controller.screen_height * 0.666), int(self.controller.screen_width * 0.494), int(self.controller.screen_height * 0.74), "#1e1e1e", "#9b111e", self.controller.show_start_menu)
        text_id = self.background.create_text(int(self.controller.screen_width * 0.434), int(self.controller.screen_height * 0.7), text="Voltar", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.0222)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_start_menu())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

    def verify_account(self):
        """
        Verificações da Conta
        """

        password = self.password_entry.get()
        username = self.username_entry.get()

        if not username or not password:
            self.controller.show_custom_message("Campos obrigatórios não preenchidos", self.controller.show_login)
            return

        user = self.db.trainers.find_one({"username": username})

        if user:
            if user["password"] == password:
                self.controller.user = user['_id']
                self.controller.show_custom_message("Login realizado com sucesso", self.controller.show_main_menu)
                return

        self.controller.show_custom_message("Usuário ou senha incorretos", self.controller.show_login)
         