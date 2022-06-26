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
screen_size = sg.Window.get_screen_size()
gf_size = img.size

sizes = {
    'Big': (gf_size[0] * (height := screen_size[1] // 3) // gf_size[1], height),
    'Normal': (gf_size[0] * (height := screen_size[1] // 5) // gf_size[1], height),
    'Small': (gf_size[0] * (height := screen_size[1] // 7) // gf_size[1], height)
}
img_data = img.copy().resize(sizes['Normal']).to_bytes()

layout = [
    [sg.Image(data=img_data, enable_events=True, background_color='white', key='girlfriend',
              right_click_menu=menu, pad=0)], ]

# TODO: add default location based on taskbar location
# FIXME: gf isn't always above the taskbar
# TODO: add a snd gf with hair cropped and allow to switch between them
# TODO: hide gf when entering fullscreen
# TODO: save configuration on exit (size, position, mode)

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
    elif event in ('Big', 'Normal', 'Small'):
        img_data = img.copy().resize(sizes[event]).to_bytes()

    window['girlfriend'].update_animation(img_data, time_between_frames=40)

window.close()
tray.close()
