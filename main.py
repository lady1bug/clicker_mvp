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




class GameScreen(Screen):
   def go_menu(self):
       self.manager.current = "menu"




class SettingsScreen(Screen):
   def go_menu(self):
       self.manager.current = "menu"




# Головний застосунок
class ClickerApp(App):
   def build(self):
       sm = ScreenManager()
       sm.add_widget(MenuScreen(name="menu"))
       sm.add_widget(GameScreen(name="game"))
       sm.add_widget(SettingsScreen(name="settings"))
       return sm




app = ClickerApp()
app.run()
