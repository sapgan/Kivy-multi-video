__author__ = "Saptarshi Gan"
__copyright__ = "Copyright (C) 2014 Saptarshi Gan"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 2"
__version__ = "1.0"

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import RiseInTransition
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import os
from custom import VideoLayout,TopAction,CustomScreen


class VideoManagerApp(App):
    sm = ScreenManager()
    screens = {}

    def callback(self,button):
        text = button.text
        screen = self.screens[text]
        screen.manager.current = text

    def build(self):
        curdir = os.path.dirname(__file__)
        video_folder = 'videos'
        from main import SOURCE
        if SOURCE:
            dirname = SOURCE
        else:
            dirname = os.path.join(curdir,video_folder)
        dirs= [d for d in os.listdir(dirname) if os.path.isdir(dirname)]
        custom = CustomScreen(name='Main Page')
        g=GridLayout(cols=2,pos_hint={'top':0.8},size_hint=(1,0.8))
        custom.add_widget(g)
        self.sm.add_widget(custom)
        for d in dirs:
            ab = TopAction(dirs)
            name = d 
            thumb = d + '.png'
            b = Button(text=name)
            g.add_widget(b)
            custom_child = CustomScreen(name=name)
            self.screens[name] = custom_child
            self.sm.add_widget(custom_child)
            video_layout = VideoLayout(name,video_folder)
            full_layout = video_layout.body_layout()
            custom_child.add_widget(ab)
            custom_child.add_widget(full_layout)
            b.bind(on_release=self.callback)
        self.sm.transition = FallOutTransition()
        return self.sm

