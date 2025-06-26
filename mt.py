from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.graphics import Color, Rectangle
import json
import os
import shutil

Window.clearcolor = (1, 1, 1, 1)

BACKGROUND_IMAGE = 'coverimage.jpg'
ICON_IMAGE = 'mticon.png'
SESSION_FILE = 'session.json'
USER_FILE = 'users.json'
MEME_FOLDER = 'memes'

os.makedirs(MEME_FOLDER, exist_ok=True)

def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def save_session(username):
    with open(SESSION_FILE, 'w') as f:
        json.dump({'username': username}, f)

def load_session():
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f).get('username')
    except:
        return None

def clear_session():
    try:
        os.remove(SESSION_FILE)
    except:
        pass

class SplashScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = FloatLayout()
        layout.add_widget(Image(source=BACKGROUND_IMAGE, allow_stretch=True, keep_ratio=False, opacity=0.7))
        title = Label(text='[b]MEME TOWN (MT)[/b]', markup=True, font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.6})
        dev = Label(text='[i]Developer: Alimoo (MooBeats)[/i]', markup=True, font_size=28, color=(0, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(title)
        layout.add_widget(dev)
        self.add_widget(layout)
        from kivy.clock import Clock
        Clock.schedule_once(self.next_screen, 5)

    def next_screen(self, dt):
        remembered = load_session()
        if remembered:
            self.manager.current = 'home'
        else:
            self.manager.current = 'login'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remember = None
        self.build()

    def build(self):
        self.clear_widgets()
        layout = FloatLayout()
        layout.add_widget(Image(source=BACKGROUND_IMAGE, allow_stretch=True, keep_ratio=False, opacity=0.7))

        box = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.8, 0.6),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[20, 20])

        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)

        check_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=15)
        self.remember = CheckBox(size_hint=(None, None), size=(40, 40))

        checkbox_bg = BoxLayout(size_hint=(None, None), size=(40, 40), padding=2)
        checkbox_bg.add_widget(self.remember)

        with checkbox_bg.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=checkbox_bg.pos, size=checkbox_bg.size)

        checkbox_bg.bind(pos=self.update_checkbox_bg, size=self.update_checkbox_bg)

        label = Label(text='[b]Remember Me[/b]', markup=True, font_size=18, color=(0, 0, 0, 1))
        check_row.add_widget(checkbox_bg)
        check_row.add_widget(label)

        login_btn = Button(text='Login', on_press=self.login)
        register_btn = Button(text='Go to Register', on_press=partial(self.go_to_screen, 'register'))

        box.add_widget(self.username)
        box.add_widget(self.password)
        box.add_widget(check_row)
        box.add_widget(login_btn)
        box.add_widget(register_btn)

        layout.add_widget(box)
        self.add_widget(layout)

    def update_checkbox_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def go_to_screen(self, screen_name, *args):
        self.manager.current = screen_name

    def login(self, instance):
        users = load_users()
        uname = self.username.text.strip()
        pwd = self.password.text.strip()
        if uname in users and users[uname] == pwd:
            if self.remember.active:
                save_session(uname)
            self.manager.current = 'home'
        else:
            Popup(title='Error', content=Label(text='Invalid login'), size_hint=(0.6, 0.4)).open()

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=BACKGROUND_IMAGE, allow_stretch=True, keep_ratio=False, opacity=0.7))

        box = BoxLayout(orientation='vertical', size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=10)

        self.username = TextInput(hint_text='Choose Username', multiline=False)
        self.password = TextInput(hint_text='Choose Password', multiline=False, password=True)
        register_btn = Button(text='Register', on_press=self.register)
        login_btn = Button(text='Back to Login', on_press=partial(self.go_to_screen, 'login'))

        box.add_widget(self.username)
        box.add_widget(self.password)
        box.add_widget(register_btn)
        box.add_widget(login_btn)
        layout.add_widget(box)
        self.add_widget(layout)

    def go_to_screen(self, screen_name, *args):
        self.manager.current = screen_name

    def register(self, instance):
        users = load_users()
        uname = self.username.text.strip()
        pwd = self.password.text.strip()
        if uname and pwd:
            if uname in users:
                Popup(title='Error', content=Label(text='User already exists'), size_hint=(0.6, 0.4)).open()
            else:
                users[uname] = pwd
                save_users(users)
                Popup(title='Success', content=Label(text='Registered successfully'), size_hint=(0.6, 0.4)).open()
                self.manager.current = 'login'

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.clear_widgets()
        layout = FloatLayout()
        layout.add_widget(Image(source=BACKGROUND_IMAGE, allow_stretch=True, keep_ratio=False, opacity=0.7))

        upload_btn = Button(text='Upload Meme', size_hint=(0.4, 0.1), pos_hint={'x': 0.05, 'y': 0.01}, on_press=self.upload_meme)
        logout_btn = Button(text='Logout', size_hint=(0.3, 0.1), pos_hint={'right': 0.95, 'top': 0.98}, on_press=self.logout)

        layout.add_widget(upload_btn)
        layout.add_widget(logout_btn)

        self.feed = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.feed.bind(minimum_height=self.feed.setter('height'))

        scroll = ScrollView(size_hint=(1, 0.85), pos_hint={'x': 0, 'y': 0.1})
        scroll.add_widget(self.feed)
        layout.add_widget(scroll)

        self.add_widget(layout)
        self.load_memes()

    def logout(self, instance):
        clear_session()
        self.manager.current = 'login'

    def upload_meme(self, instance):
        chooser = FileChooserIconView()
        popup = Popup(title='Choose Meme (Image/Video)', content=chooser, size_hint=(0.9, 0.9))

        def select(*args):
            selection = chooser.selection
            if selection:
                filepath = selection[0]
                filename = os.path.basename(filepath)
                dest = os.path.join(MEME_FOLDER, filename)
                shutil.copy(filepath, dest)
                self.add_meme_widget(dest)
                popup.dismiss()

        chooser.bind(on_submit=lambda *x: select())
        popup.open()

    def load_memes(self):
        self.feed.clear_widgets()
        for filename in os.listdir(MEME_FOLDER):
            filepath = os.path.join(MEME_FOLDER, filename)
            self.add_meme_widget(filepath)

    def add_meme_widget(self, filepath):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=400)
        if filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            box.add_widget(Image(source=filepath))
        else:
            box.add_widget(Label(text='[Video] ' + os.path.basename(filepath)))
        reactions = BoxLayout(size_hint_y=None, height=50)
        for action in ['Like', 'Dislike', 'Comment', 'Share', 'Download', 'Repost']:
            reactions.add_widget(Button(text=action))
        box.add_widget(reactions)
        self.feed.add_widget(box)

class MTApp(App):
    def build(self):
        self.icon = ICON_IMAGE
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    MTApp().run()