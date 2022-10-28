from sre_parse import CATEGORIES
import PySimpleGUI as sg

TIMEFRAMES = ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']
CATEGORIES = ['Food', 'Rent', 'Utilities',
              'Transportation', 'Entertainment', 'Other']

LAYOUT = [[sg.Text('Set Budget')],
          [sg.Text('Category'), sg.Combo(CATEGORIES, size=(20, 1)),
           sg.Text('Timeframe'), sg.Combo(TIMEFRAMES, size=(20, 1))],
          [sg.Text('Enter Budget Title:'), sg.InputText()],
          [sg.Button('Submit'), sg.Button('Cancel')]
          ]

window = sg.Window('Budgeting', LAYOUT)
sg.theme('DarkAmber')


def open_window():
    while True:
        event, values = window.read()
        if event in ["Exit", sg.WIN_CLOSED]:
            break
        # Output a message to the window
        print("Clear")

    window.close()


if __name__ == '__main__':
    open_window()
