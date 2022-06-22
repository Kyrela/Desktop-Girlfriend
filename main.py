import PySimpleGUI as sg
from psgtray import SystemTray

menu = ['GirlFriend Companion', ['Show', 'Hide', '---', 'Exit']]

layout = [
    [sg.Image(filename='assets/animated_girlfriend.gif', enable_events=True, background_color='white', key='girlfriend',
              right_click_menu=menu, pad=0)], ]

window = sg.Window('Girlfriend companion', layout,
                   no_titlebar=True,
                   keep_on_top=True,
                   background_color='white',
                   transparent_color='white',
                   alpha_channel=1,
                   margins=(0, 0))

tray = SystemTray(menu, window=window, tooltip="Girlfriend companion", icon='assets/gf_icon.png')

while True:
    event, values = window.read(timeout=1)
    if event == tray.key:
        event = values[event]
    if event in (sg.WIN_CLOSED, 'Exit', 'Cancel', sg.WIN_CLOSE_ATTEMPTED_EVENT):
        break
    if event in ('Show', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
        window.un_hide()
        window.bring_to_front()
    elif event == 'Hide':
        window.hide()

    window['girlfriend'].update_animation('assets/animated_girlfriend.gif', time_between_frames=40)

window.close()
tray.close()
