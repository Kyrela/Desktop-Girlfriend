"""
Desktop Girlfriend
--

A simple and idle desktop companion representing the Friday Night Funkin's character 'Girlfriend'

Copyright (c) 2022 Kyrela
"""

import PySimpleGUI as sg
from psgtray import SystemTray

from gif import Gif

menu = ['Desktop Girlfriend', ['Show', 'Hide', '---', 'Size', ['Big', 'Normal', 'Small'], '---', 'Exit']]

img = Gif('assets/animated_girlfriend.gif')
img_data = img.to_bytes()

layout = [
    [sg.Image(data=img_data, enable_events=True, background_color='white', key='girlfriend',
              right_click_menu=menu, pad=0)], ]

# TODO: add default location based on taskbar location

window = sg.Window('Desktop Girlfriend', layout,
                   no_titlebar=True,
                   keep_on_top=True,
                   background_color='white',
                   transparent_color='white',
                   alpha_channel=1,
                   margins=(0, 0))

tray = SystemTray(menu, window=window, tooltip="Desktop Girlfriend", icon='assets/gf_icon.png')

while True:
    event, values = window.read(timeout=1)
    if event == tray.key:
        event = values[event]
    if event in (sg.WIN_CLOSED, 'Exit', 'Cancel', sg.WIN_CLOSE_ATTEMPTED_EVENT):
        break
    if event == 'Show':
        window.un_hide()
        window.bring_to_front()
    if event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
        if window._Hidden:
            window.un_hide()
            window.bring_to_front()
        else:
            window.hide()
    elif event == 'Hide':
        window.hide()
    # TODO: add size change
    elif event == 'Big':
        pass
    elif event == 'Normal':
        pass
    elif event == 'Small':
        pass

    window['girlfriend'].update_animation(img_data, time_between_frames=40)

window.close()
tray.close()