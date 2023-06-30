import PySimpleGUI as sg
from datetime import datetime, date
from site_availability import SiteAvailability
from camp_site import CampSite
from wakasu import Wakasu

wakasu_camp_site = CampSite("若洲公園キャンプ場", "https://www.tptc.co.jp/park/03_09/reservation_info", "03-5569-6701")
wakasu = Wakasu(wakasu_camp_site)

def check_availability(site_available: SiteAvailability, check_date: date) -> bool:
    return site_available.check_availability(check_date)

# sg.theme_previewer()
sg.theme("DarkBlack1")

left_layout = [
    [sg.Text('selected date:'), sg.Input(key='-DATE-', enable_events=True, readonly=True)],
    [sg.CalendarButton(
        button_text='select date by calendar',
        key='calendar',
        format='%Y-%m-%d',
        target='-DATE-',
        close_when_date_chosen=False
    )]
]
right_layout = [
     [sg.Text('', key='-RESULT-', font=('Arial', 14))],
]

leftFrame = sg.Frame('select date', left_layout, size=(200, 100), vertical_alignment="top")
rightFrame = sg.Frame('result', right_layout, size=(400,300), vertical_alignment="top")

layout = [
    [
        leftFrame, rightFrame
    ],
    [
        sg.Exit()
    ]
]

window = sg.Window('CampsiteAvailabilityChecker', layout, resizable=True)
ret = window.find_element('-RESULT-')

while True:
    event, values = window.read()
    print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit'):
        print("Exit")
        break

    if event == '-DATE-':
        if(values['-DATE-'] == ""):
            continue
        input_date = datetime.strptime(values['-DATE-'], '%Y-%m-%d').date()

        if(check_availability(wakasu, input_date)):
            ret.update(text_color='green')
            ret.update(
                f"{input_date}\n{wakasu_camp_site.name} can reserve\n予約TEL: {wakasu_camp_site.tel}\n{wakasu_camp_site.url}"
            )
        else:
            ret.update(text_color='red')
            ret.update(
                f"{input_date}\n{wakasu_camp_site.name} can not reserve"
            )

window.close()