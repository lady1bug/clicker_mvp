from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy import platform
from kivy.properties import NumericProperty
from kivy.clock import Clock

from kivy.animation import Animation
#from kivy.core.audio import SoundLoader


# Розмір вікна (для ПК)
Window.size = (450, 900)


class MenuScreen(Screen):
    def go_game(self):
        self.manager.current = "game"
        self.manager.transition.direction = "up"

    def go_settings(self):
        self.manager.current = "settings"

    def exit_app(self):
        App.get_running_app().stop()


class Fish(Image):
    hp = 0
    fish_index = 0
    #pop_sound = SoundLoader.load('sounds/pop.wav')
    def new_fish(self, *args):
        app = App.get_running_app()
        # 1. Дізнаємося, яка риба має з'явитися
        fish_key = app.LEVELS[app.LEVEL][self.fish_index]

        # 2. Оновлюємо картинку та здоров'я
        self.source = app.FISHES[fish_key]['source']
        self.hp = app.FISHES[fish_key]['hp']

        # 3. Робимо рибу видимою
        self.opacity = 1


    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos) or self.opacity < 1:
            return False
        #if self.pop_sound:
           # self.pop_sound.play()

        # --- АНІМАЦІЯ КЛІКУ ---
        # 1. Запам'ятовуємо поточний розмір та позицію
        w, h = self.size
        x, y = self.pos

        # 2. Створюємо швидку анімацію: збільшення (+) а потім повернення до норми
        # Ми трохи зсуваємо рибку (x - 10, y - 10), щоб вона розширювалася з центру
        pulse = Animation(size=(w + 20, h + 20), pos=(x - 10, y - 10), duration=0.05) + \
                Animation(size=(w, h), pos=(x, y), duration=0.05)
        pulse.start(self)
        # ----------------------

        self.hp -= 1
        game_screen = App.get_running_app().root.get_screen('game')
        game_screen.score += 1

        if self.hp <= 0:
            fade_out = Animation(opacity=0, duration=0.5)
            fade_out.start(self)

            if len(App.get_running_app().LEVELS[App.get_running_app().LEVEL]) > self.fish_index + 1:
                self.fish_index += 1
                Clock.schedule_once(self.new_fish, 0.6)
            else:
                Clock.schedule_once(game_screen.level_complete, 0.6)
                self.fish_index = 0

        return True


class GameScreen(Screen):
    score = NumericProperty(0)

    def on_pre_enter(self, *args):
        self.score = 0
        app = App.get_running_app()
        app.LEVEL = 0
        self.ids.fish.fish_index = 0
        self.ids.level_complete.opacity = 0


    def on_enter(self, *args):
        self.ids.fish.new_fish()


    def level_complete(self, *args):
        self.ids.level_complete.opacity = 1

    def go_home(self):
        self.manager.current = "menu"


class SettingsScreen(Screen):
    def go_menu(self):
        self.manager.current = "menu"


class ClickerApp(App):
    LEVEL = 0
    FISHES = {
        'fish1': {'source': 'images/fish_01.png', 'hp': 10},
        'fish2': {'source': 'images/fish_02.png', 'hp': 20}
    }
    LEVELS = [['fish1', 'fish1', 'fish2']]

    # music = None

    def build(self):
        #self.music = SoundLoader.load('sounds/background.mp3')

        #if self.music:
            #self.music.loop = True  # Робимо її нескінченною
            #self.music.volume = 0.5  # Гучність (від 0 до 1)
            #self.music.play()
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == '__main__':
    app = ClickerApp()
    app.run()


