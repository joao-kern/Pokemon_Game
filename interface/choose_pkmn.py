import customtkinter as ctk
from CTkListbox import *

class ChoosePKMN(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#ef384c")

        # Atributos iniciais
        self.controller = controller

        self.list_box_type = CTkListbox(
            self, 
            self.controller.screen_height, self.controller.screen_width/4, 
            command=self.select_type, 
            text_color="#000000", 
            hover_color="#ef384c", 
            highlight_color="#ef384c", 
            justify="center", 
            border_width=0 , 
            font=ctk.CTkFont(family="PKMN RBYGSC", size=33, weight="bold"), 
            bg_color="#d6fffc", 
            fg_color="#d6fffc", )
        self.list_box_type.place(x=0, y=self.controller.screen_height * 0.15)

        self.background = ctk.CTkCanvas(
            self,
            width=(self.controller.screen_width * 3) / 4, 
            height=self.controller.screen_height, 
            bd=0, 
            highlightthickness=0)
        self.background.place(x=self.controller.screen_width / 4, y=0)
        
        self.background_image = self.controller.load_img("assets/background/background_pkmn.png", self.controller.screen_width * 3 // 2, self.controller.screen_height)

        self.background.create_image((self.controller.screen_width * 3) / 8, self.controller.screen_height / 2, image=self.background_image)

        for i, pkmn_type in enumerate(self.controller.pokedex.get_types()):
            self.list_box_type.insert(i, pkmn_type)

        self.title_text = ctk.CTkLabel(self, self.list_box_type.winfo_width(), self.controller.screen_height * 0.15, text="Tipos", font=("PKMN RBYGSC", 55, "bold"), fg_color="#d6fffc", bg_color="#d6fffc", text_color="#000000")
        self.title_text.place(x=0, y=0)

    def select_type(self, pkmn_type):
        self.pokemons = self.controller.pokedex.get_pokemons_by_type(pkmn_type)
        self.current_pkmn_index = 0
        self.display_pokemon(self.current_pkmn_index)

    def display_pokemon(self, index):
        self.background.delete("pkmn_info")

        self.pokemon = self.pokemons[index]
        self.pokemon_sprite = self.controller.load_image_pkmn(self.pokemon.get_sprite_front(), int(self.controller.screen_width * 0.25), int(self.controller.screen_width * 0.25))

        self.background.create_text(int(self.controller.screen_width * 0.20), int(self.controller.screen_height * 0.47), text=f"{self.pokemon.get_name()}", font=("PKMN RBYGSC", 22, "bold"), fill="#000000", anchor="w", tags="pkmn_info")
        self.background.create_text(int(self.controller.screen_width * 0.20), int(self.controller.screen_height * 0.52), text=f"HP: {self.pokemon.get_hp()}", font=("PKMN RBYGSC", 20, "bold"), fill="#000000", anchor="w", tags="pkmn_info")
        self.img_types = []
        for i, type_pkmn in enumerate(self.pokemon.get_type()):
            type_img = self.controller.load_img(f"assets/icon/pokemon_types/{type_pkmn}.png", int(0.03 * self.controller.screen_height), int(0.03 * self.controller.screen_height))
            self.img_types.append(type_img)
            self.type_pkmn = self.background.create_text(int(self.controller.screen_width * 0.20), int(self.controller.screen_height * (0.57 + (i * 0.03))), text=f"{type_pkmn}", font=("PKMN RBYGSC", 18, "bold"), fill="#000000", anchor="w", tags="pkmn_info")
            bbox = self.background.bbox(self.type_pkmn)
            self.background.create_image(bbox[2], int(self.controller.screen_height * (0.57 + (i * 0.03))), image=self.img_types[i], anchor="w", tags="pkmn_info")
        self.pokemon_img = self.background.create_image(int(self.controller.screen_width * 0.42), int(self.controller.screen_height * 0.50), image=self.pokemon_sprite, anchor="center", tags="pkmn_info")

        self.add_navigation_buttons()

    def add_navigation_buttons(self):

        if self.current_pkmn_index > 0:
            self.controller.create_rounded_button(
                self.background, int(self.controller.screen_width * 0.08), int(self.controller.screen_height * 0.45), int(self.controller.screen_width * 0.13), int(self.controller.screen_height * 0.53),
                "#ef384c", "#000000", self.show_previous_pkmn
            )
            text_id = self.background.create_text(int(self.controller.screen_width * 0.105), int(self.controller.screen_height * 0.47), text="<", font=("PKMN RBYGSC", int(self.controller.screen_width * 0.01851), "bold"), fill="#FFFFFF", tag="pkmn_info")
            self.background.tag_bind(text_id, "<Button-1>", lambda event: self.show_previous_pkmn())
            self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        if self.current_pkmn_index < len(self.pokemons) - 1:
            self.controller.create_rounded_button(
                self.background, int(self.controller.screen_width * 0.60), int(self.controller.screen_height * 0.45), int(self.controller.screen_width * 0.65), int(self.controller.screen_height * 0.53),
                "#ef384c", "#000000", self.show_next_pkmn
            )
            text_id = self.background.create_text(int(self.controller.screen_width * 0.625), int(self.controller.screen_height * 0.47), text=">", font=("PKMN RBYGSC", int(self.controller.screen_width * 0.01851), "bold"), fill="#FFFFFF", tag="pkmn_info")
            self.background.tag_bind(text_id, "<Button-1>", lambda event: self.show_next_pkmn())
            self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        self.controller.create_rounded_button(
            self.background, int(self.controller.screen_width * 0.26) , int(self.controller.screen_height * 0.74), int(self.controller.screen_width * 0.37), int(self.controller.screen_height * 0.81),
            "#ef384c", "#000000", self.controller.show_main_menu
        )
        text_id = self.background.create_text(int(self.controller.screen_width * 0.315), int(self.controller.screen_height * 0.775), text="Voltar", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.018), "bold"), fill="#FFFFFF", tag="pkmn_info")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_main_menu())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        self.controller.create_rounded_button(
            self.background, int(self.controller.screen_width * 0.47), int(self.controller.screen_height * 0.74), int(self.controller.screen_width * 0.58), int(self.controller.screen_height * 0.81),
            "#ef384c", "#000000", lambda pkmn=self.pokemon: self.select_pokemon(pkmn)
        )
        text_id = self.background.create_text(int(self.controller.screen_width * 0.525), int(self.controller.screen_height * 0.775), text="Escolher", font=("PKMN RBYGSC", int(self.controller.screen_height * 0.018), "bold"), fill="#FFFFFF", tag="pkmn_info")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.select_pokemon(self.pokemon))
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

    def show_previous_pkmn(self):
        if self.current_pkmn_index > 0:
            self.current_pkmn_index -= 1
            self.display_pokemon(self.current_pkmn_index)

    def show_next_pkmn(self):
        if self.current_pkmn_index < len(self.pokemons) - 1:
            self.current_pkmn_index += 1
            self.display_pokemon(self.current_pkmn_index)
    
    def select_pokemon(self, pokemon):
        """
        Confirmar a seleção do Pokemon
        """
        self.controller.pokemon_selected = pokemon
        self.controller.show_custom_message(f"{pokemon.get_name()} escolhido com sucesso!", self.controller.show_main_menu)
