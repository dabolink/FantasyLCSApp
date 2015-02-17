from FantasyLCSAPI import *
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation


class LCSApp(App):

    def animate(self, instance):
        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(200, 100), t='out_bounce')
        animation &= Animation(size=(500, 500))
        animation += Animation(size=(100, 50))
        animation.start(instance)

    def build(self):
        layout = FloatLayout(size=(700, 700))
        button = Button(size_hint=(None, None), text='lelel', on_press=self.animate)
        layout.add_widget(button)
        return layout


if __name__ == "__main__":
    LCSApp().run()

