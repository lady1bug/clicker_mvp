from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy import platform
from kivy.properties import NumericProperty
from kivy.clock import Clock

# Розмір вікна (для ПК)
Window.size = (450, 900)




# Класи для екранів
class MenuScreen(Screen):
   def go_game(self):
       self.manager.current = "game"


   def go_settings(self):
       self.manager.current = "settings"


   def exit_app(self):
       App.get_running_app().stop()


class Fish(Image):
    hp =0
    fish_index = 0
    def new_fish(self, *args):
        app = App.get_running_app()
        # Беремо дані про поточну рибу
        fish_key = app.LEVELS[app.LEVEL][self.fish_index]
        self.source = app.FISHES[fish_key]['source']
        self.hp = app.FISHES[fish_key]['hp']
        self.opacity = 1

    def on_touch(self):
        if self.collide_point(*self.touch_pos) or self.opacity == 0:
            return False
        self.hp -= 1
        game_screen = App.get_running_app().root.root.get_screen('game')
        game_screen.score += 1
        if self.hp <= 0:
            self.opacity = 0
            app = App.get_running_app()
            if len(app.LEVELS[app.LEVEL]) > self.fish_index + 1:
                self.fish_index += 1
                Clock.schedule_once(self.new_fish, 1.2)
            else:
                Clock.schedule_once(game_screen.level_complete, 1.2)
                self.fish_index = 0
         return True



class GameScreen(Screen):
   def go_menu(self):
       self.manager.current = "menu"




class SettingsScreen(Screen):
   def go_menu(self):
       self.manager.current = "menu"




# Головний застосунок
class ClickerApp(App):
    LEVEL = 0
    FISHES = {
        'fish1': {'source': 'images/fish_01.png', 'hp': 10},
        'fish2': {'source': 'images/fish_02.png', 'hp': 20}
    }
    LEVELS = [['fish1', 'fish1', 'fish2']]
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm




app = ClickerApp()
app.run()
