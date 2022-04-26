import kivy

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from plyer import email, accelerometer
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from multiprocessing.dummy import Process

import uuid
# kivy.require('1.8.0')

# setup graphics
Config.set('graphics', 'resizable', 0)

# Graphics fix
Window.clearcolor = (0, 0, 0, 1.)


class ClientApp(App):

    def build(self):
        app = GUI()

        return app

    def on_start(self):
        from kivy import platform
        if platform == "android":
            self.start_service()
        Process(target=self.initiate_load_sequence).start()


class GUI(Widget):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.user_id = str(uuid.uuid1())
        uid_label = Label(text=self.user_id)

        enable_label = Label(text='')
        enable_label.x = Window.width/2-enable_label.width/2
        enable_label.y = Window.height/2

        self.add_widget(enable_label)
        self.add_widget(uid_label)

        # setup accelerometer
        try:
            accelerometer.enable()

        except:
            enable_label.text = 'cant enable accelerometer'

        # setup accelerometer labels
        self.label = Label(text='accelerometer:')
        self.label.y = Window.height*0.25
        self.label.x = Window.width*0.5
        self.add_widget(self.label)

        # setup timer to update accelerometer
        Clock.schedule_interval(self.check_accel, 1.0/60.0)

        # self.notify()
        # self.email()

    def check_accel(self, dt):
        # update label
        try:
            self.txt = str(round(accelerometer.acceleration[0], 4)) + ',' + str(round(accelerometer.acceleration[1], 4))\
                       + ',' + str(round(accelerometer.acceleration[2], 4))
            self.label.text = 'accelerometer: ' + self.txt

        except:
            self.label.text = 'cant read accelerometer'

    # def email(self):
    #     try:
    #         email.send(recipient='yarin1997udi@gmail.com', subject='Thanks!', text='Enjoyed your lesson')
    #     except:
    #         print('cant email')


if __name__ == '__main__':
    ClientApp().run()
