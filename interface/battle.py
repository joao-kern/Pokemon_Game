import customtkinter as ctk
from model.combat import Combat
from PIL import Image, ImageTk
from pymongo import MongoClient

class Battle(ctk.CTkFrame):
    def __init__(self, parent, controller, player_pókemon, opponent_pokemon, db):
        super().__init__(parent, fg_color="#f5f5dc")

        # Atributos iniciais
        self.combat = Combat(player_pókemon, opponent_pokemon)

        self.db = db

        self.controller = controller

        self.half_width = int(self.controller.screen_width / 2)
        self.half_height = int(self.controller.screen_height / 2)

        self.ended = False

        self.player_pokemon = player_pókemon
        self.opponent_pokemon = opponent_pokemon

        # Background
        self.background_battle_image = self.controller.load_img("assets/background/background_battle.png", self.controller.screen_width, self.controller.screen_height - int(self.controller.screen_height * 0.259))

        self.background = ctk.CTkCanvas(
            self, 
            width=self.controller.screen_width, 
            height=self.controller.screen_height, 
            bd=0, 
            highlightthickness=0)
        self.background.place(x=0, y=0)

        self.background.create_image(
            0, 0, 
            image=self.background_battle_image, 
            anchor="nw")

        # Tag Player
        self.player_tag_img = Image.open("assets/background/pkmn_tag.png")
        bbox = self.player_tag_img.getbbox()
        self.player_tag_img = self.player_tag_img.crop(bbox)
        self.player_tag_img = self.player_tag_img.resize((int(self.controller.screen_width * 0.2895), int(self.controller.screen_height * 0.1481)), resample=Image.Resampling.NEAREST)
        width_player_tag = self.player_tag_img.size[0]
        self.player_tag_img = self.player_tag_img.transpose(Image.FLIP_LEFT_RIGHT)
        self.player_tag_img = ImageTk.PhotoImage(self.player_tag_img)

        # Pokemon do Player
        self.player_pokemon_sprite = self.controller.load_image_pkmn(self.player_pokemon.get_sprite_back(), int(self.controller.screen_width * 0.2), int(self.controller.screen_width * 0.2))

        self.player_tag = self.background.create_image(
            int(self.controller.screen_width * 0.45), int(self.controller.screen_height * 0.5037), 
            image=self.player_tag_img, 
            anchor="nw")

        self.player_pokemon_shadow_img = self.controller.shadow(int(self.player_pokemon_sprite.width()))

        self.player_pokemon_shadow_coords = int(self.controller.screen_width * 0.35), int(self.controller.screen_height * 0.648)
        self.player_pokemon_shadow = self.background.create_image(
            self.player_pokemon_shadow_coords,
            anchor="s", 
            image=self.player_pokemon_shadow_img)
        
        self.player_pokemon_img_coords = int(self.controller.screen_width * 0.35), int(self.controller.screen_height * 0.648)
        self.player_pokemon_img = self.background.create_image(
            self.player_pokemon_img_coords,
            image=self.player_pokemon_sprite, 
            anchor="s")

        self.player_health_bar = ctk.CTkProgressBar(
            self.background, 
            width=width_player_tag * 0.8, 
            height=15, 
            corner_radius=5,
            progress_color="#17c521",
            fg_color="#FFFFFF",
            bg_color="#f0f0d0",
            border_width=4, 
            border_color="#0e0e18")
        self.player_health_bar_id = self.background.create_window(int(self.controller.screen_width * 0.485), int(self.controller.screen_height * 0.5737), window=self.player_health_bar, anchor="w")
        self.player_health_bar.set(1)

        self.player_name = self.background.create_text(
            int(self.controller.screen_width * 0.485), int(self.controller.screen_height * 0.5437), 
            anchor="w", 
            text=f"{self.player_pokemon.get_name()}", 
            font=("PKMN RBYGSC", 18, "bold"), 
            fill="#0e0e18")

        self.player_health = self.background.create_text(
            int(self.controller.screen_width * 0.485) ,int(self.controller.screen_height * 0.5987), 
            anchor="w",  
            text=f"{self.player_pokemon.get_hp():.2f}/{self.player_pokemon.get_hp_max()}", 
            font=("PKMN RBYGSC", 12, "bold"),
            fill="#0e0e18", )

        # Tag oponente
        self.opponent_tag_img = Image.open("assets/background/pkmn_tag.png")
        bbox = self.opponent_tag_img.getbbox()
        self.opponent_tag_img = self.opponent_tag_img.crop(bbox)
        width_opponent_tag = self.opponent_tag_img.size[0]
        self.opponent_tag_img = self.opponent_tag_img.resize((int(self.controller.screen_width * 0.2895), int(self.controller.screen_height * 0.1481)), resample=Image.Resampling.NEAREST)
        self.opponent_tag_img = ImageTk.PhotoImage(self.opponent_tag_img)

        # Pokemon oponente
        self.opponent_pokemon_sprite = self.controller.load_image_pkmn(self.opponent_pokemon.get_sprite_front(),int(self.controller.screen_width * 0.2), int(self.controller.screen_width * 0.2))

        self.opponent_tag = self.background.create_image(
            int(self.controller.screen_width * 0.20), int(self.controller.screen_height * 0.1388), 
            image=self.opponent_tag_img, 
            anchor="nw")

        self.opponent_pokemon_shadow_img = self.controller.shadow(int(self.opponent_pokemon_sprite.width()))

        self.opponent_pokemon_shadow_coords = int(self.controller.screen_width * 0.60), int(self.controller.screen_height * 0.37)
        self.opponent_pokemon_shadow = self.background.create_image(
            self.opponent_pokemon_shadow_coords,
            anchor="s", 
            image=self.opponent_pokemon_shadow_img)

        self.opponent_pokemon_img_coords = int(self.controller.screen_width * 0.60), int(self.controller.screen_height * 0.37)
        self.opponent_pokemon_img = self.background.create_image(
            self.opponent_pokemon_img_coords,
            image=self.opponent_pokemon_sprite,
            anchor="s")

        self.opponent_health_bar = ctk.CTkProgressBar(self.background, 
            width=width_opponent_tag * 0.8, 
            height=15, 
            corner_radius=5, 
            progress_color="#17c521",
            fg_color="#FFFFFF",
            bg_color="#f0f0d0", 
            border_width=4, 
            border_color="#0e0e18")
        self.opponent_health_bar_id = self.background.create_window(int(self.controller.screen_width * 0.215), int(self.controller.screen_height * 0.2088), window=self.opponent_health_bar, anchor="w")
        self.opponent_health_bar.set(1)

        self.opponent_name = self.background.create_text(int(self.controller.screen_width * 0.215), int(self.controller.screen_height * 0.1788), 
            anchor="w", 
            text=f"{self.opponent_pokemon.get_name()}", 
            font=("PKMN RBYGSC", 18, "bold"), 
            fill="#0e0e18")

        self.opponent_health = self.background.create_text(int(self.controller.screen_width * 0.215), int(self.controller.screen_height * 0.2338), 
            anchor="w", 
            text=f"{self.opponent_pokemon.get_hp():.2f}/{self.opponent_pokemon.get_hp_max()}", 
            font=("PKMN RBYGSC", 12, "bold"), 
            fill="#0e0e18")

        self.background.create_rectangle(
            0, int(self.controller.screen_height * 0.70), self.controller.screen_width, self.controller.screen_height,
            outline="#0e0e18", 
            fill="#f0f0d0", 
            width=8)

        # Cria os botões usando o canvas e funções do controller
        for i, move in enumerate(self.player_pokemon.get_moves()):

            # Botão Ataque 1
            if i == 0:
                button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.5), int(self.controller.screen_height * 0.71851), int(self.controller.screen_width * 0.7083), int(self.controller.screen_height * 0.8407), "#d6d6bb", "#0e0e18", lambda m=move: self.player_attack(m))
                text_id_name = self.background.create_text(
                    int(self.controller.screen_width * 0.60415), int(self.controller.screen_height * 0.74851),
                    text=f"{move['name'].upper()}",
                    font=("PKMN RBYGSC", 14, "bold"),
                    fill="#0e0e18"
                )
                text_id_type = self.background.create_text(
                    int(self.controller.screen_width * 0.55), int(self.controller.screen_height * 0.78851),
                    text=f"{move['type'].upper()}",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )
                text_id_power = self.background.create_text(
                    int(self.controller.screen_width * 0.65), int(self.controller.screen_height * 0.78851),
                    text=f"{move['damage']} POWER",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )

                bbox = self.background.bbox(text_id_type)

                self.type_img_0 = self.controller.load_img(f"assets/icon/pokemon_types/{move['type']}.png", int(0.03 * self.controller.screen_height), int(0.03 * self.controller.screen_height))
                img_id_type = self.background.create_image(
                    bbox[2], int(self.controller.screen_height * 0.78851), 
                    image=self.type_img_0, 
                    anchor="w", 
                    tags="pkmn_info")
            # Botão Ataque 2
            elif i == 1:
                button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.71875), int(self.controller.screen_height * 0.71851), int(self.controller.screen_width * 0.927), int(self.controller.screen_height * 0.8407), "#d6d6bb", "#0e0e18", lambda m=move: self.player_attack(m))
                text_id_name = self.background.create_text(
                    int(self.controller.screen_width * 0.822875), int(self.controller.screen_height * 0.74851),
                    text=f"{move['name'].upper()}",
                    font=("PKMN RBYGSC", 14, "bold"),
                    fill="#0e0e18"
                )
                text_id_type = self.background.create_text(
                    int(self.controller.screen_width * 0.76875), int(self.controller.screen_height * 0.78851),
                    text=f"{move['type'].upper()}",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )
                text_id_power = self.background.create_text(
                    int(self.controller.screen_width * 0.86875), int(self.controller.screen_height * 0.78851),
                    text=f"{move['damage']} POWER",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )

                bbox = self.background.bbox(text_id_type)

                self.type_img_1 = self.controller.load_img(f"assets/icon/pokemon_types/{move['type']}.png", int(0.03 * self.controller.screen_height), int(0.03 * self.controller.screen_height))
                img_id_type = self.background.create_image(
                    bbox[2], int(self.controller.screen_height * 0.78851), 
                    image=self.type_img_1, 
                    anchor="w",
                    tags="pkmn_info")

            # Botão Ataque 3
            elif i == 2:
                button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.5), int(self.controller.screen_height * 0.85925), int(self.controller.screen_width * 0.7083), int(self.controller.screen_height * 0.98148), "#d6d6bb", "#0e0e18", lambda m=move: self.player_attack(m))
                text_id_name = self.background.create_text(
                    int(self.controller.screen_width * 0.60415), int(self.controller.screen_height * 0.88925),
                    text=f"{move['name'].upper()}",
                    font=("PKMN RBYGSC", 14, "bold"),
                    fill="#0e0e18"
                )
                text_id_type = self.background.create_text(
                    int(self.controller.screen_width * 0.55), int(self.controller.screen_height * 0.92925),
                    text=f"{move['type'].upper()}",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )
                text_id_power = self.background.create_text(
                    int(self.controller.screen_width * 0.65), int(self.controller.screen_height * 0.92925),
                    text=f"{move['damage']} POWER",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )

                bbox = self.background.bbox(text_id_type)

                self.type_img_2 = self.controller.load_img(f"assets/icon/pokemon_types/{move['type']}.png", int(0.03 * self.controller.screen_height), int(0.03 * self.controller.screen_height))
                img_id_type = self.background.create_image(
                    bbox[2], int(self.controller.screen_height * 0.92925), 
                    image=self.type_img_2, 
                    anchor="w", 
                    tags="pkmn_info")

            # Botão Ataque 4
            elif i == 3:
                button_image = self.controller.create_rounded_button(self.background, int(self.controller.screen_width * 0.71875), int(self.controller.screen_height * 0.85925), int(self.controller.screen_width * 0.927), int(self.controller.screen_height * 0.98148), "#d6d6bb", "#0e0e18", lambda m=move: self.player_attack(m))
                text_id_name = self.background.create_text(
                    int(self.controller.screen_width * 0.822875), int(self.controller.screen_height * 0.88925),
                    text=f"{move['name'].upper()}",
                    font=("PKMN RBYGSC", 14, "bold"),
                    fill="#0e0e18"
                )
                text_id_type = self.background.create_text(
                    int(self.controller.screen_width * 0.76875), int(self.controller.screen_height * 0.92925),
                    text=f"{move['type'].upper()}",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )
                text_id_power = self.background.create_text(
                    int(self.controller.screen_width * 0.86875), int(self.controller.screen_height * 0.92925),
                    text=f"{move['damage']} POWER",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#0e0e18"
                )

                bbox = self.background.bbox(text_id_type)

                self.type_img_3 = self.controller.load_img(f"assets/icon/pokemon_types/{move['type']}.png", int(0.03 * self.controller.screen_height), int(0.03 * self.controller.screen_height))
                img_id_type = self.background.create_image(
                    bbox[2], int(self.controller.screen_height * 0.92925), 
                    image=self.type_img_3, 
                    anchor="w", 
                    tags="pkmn_info")

            # Associa as funções do botões ao texto
            self.background.tag_bind(text_id_name, "<Button-1>", lambda event, m=move: self.handle_click(event, m))
            self.background.tag_bind(text_id_name, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id_name, "<Leave>", lambda event: self.background.config(cursor=""))

            self.background.tag_bind(text_id_type, "<Button-1>", lambda event, m=move: self.handle_click(event, m))
            self.background.tag_bind(text_id_type, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id_type, "<Leave>", lambda event: self.background.config(cursor=""))

            self.background.tag_bind(text_id_power, "<Button-1>", lambda event, m=move: self.handle_click(event, m))
            self.background.tag_bind(text_id_power, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id_power, "<Leave>", lambda event: self.background.config(cursor=""))

            self.background.tag_bind(img_id_type, "<Button-1>", lambda event, m=move: self.handle_click(event, m))
            self.background.tag_bind(img_id_type, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(img_id_type, "<Leave>", lambda event: self.background.config(cursor=""))

            self.description_fight = self.background.create_text(
                int(self.controller.screen_width * 0.05), int(self.controller.screen_height * 0.85925),
                text="",
                font=("PKMN RBYGSC",28, "bold"),
                fill="#0e0e18",
                anchor="w"
            )

    def handle_click(self, event, move):
        self.player_attack(move)

    def show_endgame_message(self, result_text, canvas_width, canvas_height):
        """
        Mostra a mensagem de fim da batalha
        """

        self.background_message = ctk.CTkCanvas(
            self, 
            width=self.controller.screen_width, 
            height=self.controller.screen_height, 
            bd=0, 
            highlightthickness=0,
            )
        self.background_message.place(x=0, y=0)

        self.controller.create_translucent_rectangle(
            self.background_message,
            self.controller.screen_width,
            self.controller.screen_height,
        )

        self.background_message.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text=result_text,
            font=("PKMN RBYGSC", 60, "bold"),
            fill="#9b111e"
        )

        text_id = self.background_message.create_text(
            canvas_width // 2,
            canvas_height // 2 + 3,
            text=result_text,
            font=("PKMN RBYGSC", 60, "bold"),
            fill="#000000"
        )

    def player_attack(self, attack):
        """
        Realiza as funções necessárias para o ataque do Player
        """
        self.move_pkmn(1, self.player_pokemon_img, self.player_pokemon_img_coords, self.player_pokemon_shadow, self.player_pokemon_shadow_coords)
        self.attack(self.player_pokemon, attack, self.opponent_pokemon)
        self.calc_hp_bar(self.opponent_health_bar, self.opponent_pokemon)
        self.background.itemconfig(self.opponent_health,text=f"{self.opponent_pokemon.get_hp():.2f}/{self.opponent_pokemon.get_hp_max()}")
        self.background.itemconfig(self.description_fight, text=f"{self.player_pokemon.get_name()} usou {attack['name']}")
        self.after(800, self.player_reset)
        self.after(4000, self.end_battle)
        self.after(4000, self.opponent_attack)

    def player_reset(self):
        self.background.coords(self.player_pokemon_img, self.player_pokemon_img_coords)
        self.background.coords(self.player_pokemon_shadow, self.player_pokemon_shadow_coords)

    def opponent_attack(self):
        """
        Realiza as funções necessárias para o ataque do oponente
        """

        attack = self.combat.sort_attack()
        self.move_pkmn(-1, self.opponent_pokemon_img, self.opponent_pokemon_img_coords, self.opponent_pokemon_shadow, self.opponent_pokemon_shadow_coords)
        self.attack(self.opponent_pokemon, attack, self.player_pokemon)
        self.background.itemconfig(self.player_health, text=f"{self.player_pokemon.get_hp():.2f}/{self.player_pokemon.get_hp_max()}")
        self.background.itemconfig(self.description_fight, text=f"{self.opponent_pokemon.get_name()} usou {attack['name']}")
        self.calc_hp_bar(self.player_health_bar, self.player_pokemon)
        self.after(800, self.opponent_reset)
        self.after(4000, self.end_battle)

    def opponent_reset(self):
        self.background.coords(self.opponent_pokemon_img, self.opponent_pokemon_img_coords)
        self.background.coords(self.opponent_pokemon_shadow, self.opponent_pokemon_shadow_coords)

    def attack(self, attacker, attack, target):
        """
        Realiza o ataque do Pokemon
        """
        
        self.combat.attack(attacker, attack, target)

    def calc_hp_bar(self, health_bar, pokemon):
        """
        Faz o cálculo da barra de HP do Pokemon
        """

        health_percentage = pokemon.get_hp() / pokemon.get_hp_max()
        health_bar.set(max(0, health_percentage))

    def move_pkmn(self, direction, pkmn, pkmn_coords, shadow, shadow_coords):
        new_coords_img = (pkmn_coords[0] + 30 * direction, pkmn_coords[1] + 30 * -direction)
        new_coords_shadow = (shadow_coords[0] + 30 * direction, shadow_coords[1] + 30 * -direction)

        self.background.coords(pkmn, new_coords_img)
        self.background.coords(shadow, new_coords_shadow)

    def end_battle(self):
        """
        Analisa se a batalha terminou
        """
        if self.combat.get_winner() != None:
                self.player_pokemon.restore_hp()
                self.opponent_pokemon.restore_hp()
                if self.combat.get_winner() == self.player_pokemon and not self.ended:
                    self.ended = True
                    self.db.trainers.update_one(
                    {'_id': self.controller.user},
                    {
                        '$inc': {
                            'battles': 1,     
                            'victories': 1,     
                            'defeats': 0       
                        }
                    }
                )
                    self.show_endgame_message("VITÓRIA", self.controller.screen_width, self.controller.screen_height)
                    button_image = self.controller.create_rounded_button(self.background_message, int(self.controller.screen_width * 0.421), int(self.controller.screen_height * 0.7648), int(self.controller.screen_width * 0.5781), int(self.controller.screen_height * 0.8296), "#1e1e1e", "#9b111e", self.controller.show_main_menu)
                    text_button_id = self.background_message.create_text(
                    int(self.controller.screen_width * 0.49955), int(self.controller.screen_height * 0.79722),
                    text="Voltar",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#FFFFFF"
                )
                    self.background_message.tag_bind(text_button_id, "<Button-1>", lambda event: self.controller.show_main_menu)
                    self.background_message.tag_bind(text_button_id, "<Enter>", lambda event: self.background_message.config(cursor="hand2"))
                    self.background_message.tag_bind(text_button_id, "<Leave>", lambda event: self.background_message.config(cursor=""))
                    self.background_message.tag_raise(button_image)
                    self.background_message.tag_raise(text_button_id)
                    return True
                elif self.combat.get_winner() == self.opponent_pokemon and not self.ended:
                    self.ended = True
                    self.db.trainers.update_one(
                    {'_id': self.controller.user},
                    {
                        '$inc': {
                            'battles': 1,     
                            'victories': 0,     
                            'defeats': 1       
                        }
                    }
                )
                    self.show_endgame_message("DERROTA", self.controller.screen_width, self.controller.screen_height)
                    button_image = self.controller.create_rounded_button(self.background_message, int(self.controller.screen_width * 0.421), int(self.controller.screen_height * 0.7648), int(self.controller.screen_width * 0.5781), int(self.controller.screen_height * 0.8296), "#1e1e1e", "#9b111e", self.controller.show_main_menu)
                    text_button_id = self.background_message.create_text(
                    int(self.controller.screen_width * 0.49955), int(self.controller.screen_height * 0.79722),
                    text="Voltar",
                    font=("PKMN RBYGSC", 12, "bold"),
                    fill="#FFFFFF"
                )
                    self.background_message.tag_bind(text_button_id, "<Button-1>", lambda event: self.controller.show_main_menu)
                    self.background_message.tag_bind(text_button_id, "<Enter>", lambda event: self.background_message.config(cursor="hand2"))
                    self.background_message.tag_bind(text_button_id, "<Leave>", lambda event: self.background_message.config(cursor=""))
                    self.background_message.tag_raise(button_image)
                    self.background_message.tag_raise(text_button_id)
                    return True
                
        return False