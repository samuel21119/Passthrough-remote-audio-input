#!/usr/bin/env python3
#########################################################################
# > File Name: listen.py
# > Author: Samuel
# > Mail: enminghuang21119@gmail.com
# > Created Time: Fri Jul  1 15:25:15 2022
#########################################################################
from pynput import keyboard

class listen:
    def __init__(self, hotkey, callback):
        self.callback = callback
        self.hotkey = hotkey
    def start(self):
        hotkey = self.hotkey
        def on_activate_h():
            self.callback()
            # print(f'{hotkey} pressed')
            return
        self.listener = keyboard.GlobalHotKeys({hotkey: on_activate_h})
        self.listener.start()
    def stop(self):
        self.listener.stop()
