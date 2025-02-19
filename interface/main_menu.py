import customtkinter as ctk
from random import randint

class MainMenu(ctk.CTkFrame):
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

        # Escolher Pokemon
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.388), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.462), "#1e1e1e", "#9b111e", self.controller.show_choose_pkmn)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.425), text="Escolher Pokemon", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.022)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_choose_pkmn())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        # Batalhar
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.481), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.555), "#1e1e1e", "#9b111e", self.verify_pokemon)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.518), text="Batalhar", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.022)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.verify_pokemon())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
        
        # Histórico
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.574), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.648), "#1e1e1e", "#9b111e", self.trainer_history)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.611), text="Histórico", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.022)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.trainer_history())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        # Sair
        button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.377), int(self.controller.screen_height * 0.666), int(self.controller.screen_width * 0.622), int(self.controller.screen_height * 0.740), "#1e1e1e", "#9b111e", self.logout)
        text_id = self.background.create_text(self.half_width, int(self.controller.screen_height * 0.703), text="Sair", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.022)), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.logout())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))


    def verify_pokemon(self):
        """
        Verifica se um Pokemon foi selecionado
        """
        if self.controller.pokemon_selected == None:
            self.controller.show_custom_message("Nenhum Pokemon foi escolhido", self.controller.show_main_menu)
            return
        else:
            x = randint(1, 151)
            pokemon_opponent = self.controller.pokedex.get_pokemons()[x]
            self.controller.show_battle(self.controller.pokemon_selected, pokemon_opponent)

    def trainer_history(self):
        """
        Atualiza o frame para o Histórico
        """
        self.controller.show_history()

    def logout(self):
        self.controller.user = None
        self.controller.show_start_menu()