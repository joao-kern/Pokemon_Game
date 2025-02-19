import customtkinter as ctk
import requests
from PIL import Image, ImageTk, ImageDraw
from model.pokedex import Pokedex
from io import BytesIO
from interface.start_menu import StartMenu
from interface.create_account import CreateAccount
from interface.login import Login
from interface.main_menu import MainMenu
from interface.choose_pkmn import ChoosePKMN
from interface.battle import Battle
from interface.history import History
from interface.custom_message import CustomMessage

class GUI:
    def __init__(self, root, db):

        # Atributo Root
        self.root = root

        self.db = db

        self.root.title("Pokemon Game")

        self.root.attributes('-fullscreen', True)

        ctk.set_appearance_mode("Dark")

        self.root.iconbitmap("assets/icon/pokeball.ico")

        self.root.geometry("960x540")

        # Tamanho tela
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Funções bind
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#79caf9")
        self.main_frame.pack(fill="both", expand=True)

        # Background
        self.background_image = Image.open("assets/background/background.png")
        self.background_image = self.background_image.resize((self.screen_width, self.screen_height), resample=Image.Resampling.BILINEAR)
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.background = ctk.CTkCanvas(self.main_frame, width=self.screen_width, height=self.screen_height, bd=0, highlightthickness=0)
        self.background.place(x=0, y=0)

        self.background.create_image(self.screen_width / 2, self.screen_height / 2, image=self.background_image)

        # Pokedex
        self.pokedex = Pokedex("assets/pokedex.json")

        self.pokemon_selected = None

        # Usuário
        self.user = None

        # Frames

        self.show_start_menu()

    def toggle_fullscreen(self, event=None):
        """
        Alterar Fullscreen
        """

        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)

    def exit_fullscreen(self, event=None):
        """
        Sair do Fullscreen
        """

        self.root.attributes('-fullscreen', False)

    def load_image_pkmn(self, url, width, height):
        """
        Carregar Sprite Pokemons
        """

        pill_img_data = requests.get(url).content
        pill_img = Image.open(BytesIO(pill_img_data))
        pill_img_resized = pill_img.resize((width, height), resample=Image.Resampling.BILINEAR)
        bbox = pill_img_resized.getbbox()
        pill_img_cropped = pill_img_resized.crop(bbox)

        img_tk = ImageTk.PhotoImage(pill_img_cropped)

        return img_tk
    
    def load_img(self, url, width, height):
        pill_img = Image.open(url)
        pill_img = pill_img.resize((width, height), resample=Image.Resampling.BILINEAR)
        img_tk = ImageTk.PhotoImage(pill_img)

        return img_tk

    def shadow(self, pokemon_width):
        """
        Criar Sombra Pokemon Estilo Pixelado
        """

        width, height = pokemon_width, 30
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.ellipse([(0, 0), (width, height)], fill=(0, 0, 0, 100))

        small_size = (width // 5, height // 5)
        pixelated_image = image.resize(small_size, Image.NEAREST)
        pixelated_image = pixelated_image.resize((width, height), Image.NEAREST)

        shadow = ImageTk.PhotoImage(pixelated_image)

        return shadow

    def create_translucent_rectangle(self, canvas, width, height):
        """
        Criar Retângulo Translucido
        """

        image = Image.new("RGBA", (width, height), (0, 0, 0, 128))
        draw = ImageDraw.Draw(image)
        draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 128))

        translucent_image = ImageTk.PhotoImage(image)

        self.translucent_image = translucent_image

        rect_id = canvas.create_image(0, 0, anchor="nw", image=translucent_image)

        return rect_id

    def create_rounded_button(self, canva, x1, y1, x2, y2, color, color_outline, command):
        """
        Criar Botão
        """

        width = int(x2 - x1)
        height = int(y2 - y1)

        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(5, 5), (width - 5, height - 5)],
            radius=10,
            fill=color,
            outline=color_outline,
            width=5
        )
        rounded_image = ImageTk.PhotoImage(image)
        button_image = canva.create_image(x1, y1, anchor="nw", image=rounded_image, tag="pkmn_info")

        if not hasattr(self, "_images"):
            self._images = []
        self._images.append(rounded_image)
        canva.tag_bind(button_image, "<Button-1>", lambda event, cmd=command: cmd())
        canva.tag_bind(button_image, "<Enter>", lambda event: canva.config(cursor="hand2"))
        canva.tag_bind(button_image, "<Leave>", lambda event: canva.config(cursor=""))

        return button_image

    def switch_frame(self, new_frame_class, *args, **kwargs):
        """
        Alterna para um novo frame. Cria o frame se ele ainda não existir.
        """

        # Destruir o frame atual
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Criar o novo frame
        self.current_frame = new_frame_class(self.main_frame, self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_custom_message(self, message, next_frame):
        self.switch_frame(CustomMessage, message, next_frame)

    def show_start_menu(self):
        self.switch_frame(StartMenu)

    def show_create_account(self):
        self.switch_frame(CreateAccount, self.db)

    def show_login(self):
        self.switch_frame(Login, self.db)
    
    def show_main_menu(self):
        self.switch_frame(MainMenu)

    def show_choose_pkmn(self):
        self.switch_frame(ChoosePKMN)

    def show_battle(self, pokemon_player, pokemon_opponent):
        self.switch_frame(Battle, pokemon_player, pokemon_opponent, self.db)

    def show_history(self):
        self.switch_frame(History, self.db)

    def finish_program(self):
        """
        Finalizar programa
        """

        self.main_frame.destroy()
        self.root.quit()


