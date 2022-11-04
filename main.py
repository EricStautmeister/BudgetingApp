import PySimpleGUI as sg

# Import various files for the GUI
from src import budgetwindow as budgetW
from src import expenses_income_window as expenses_income_W


# global variables
THEME: str = 'DarkAmber'
sg.theme(THEME)

LAYOUT: list[list[any]] = [[sg.Push(), sg.Text('Budgetti'), sg.Push()],
                           [sg.Button('Budgets'), sg.Button(
                               'Expenses and Income')]]


def create_main_window():
    return sg.Window('Budgetti', LAYOUT)


def main():
    # Define the window and theme
    window: any = create_main_window()
    while True:
        # read all actions and values from the window
        event, values = window.read()

        # if the user closes the window or clicks the "Exit" button, exit the program
        if event in ["Exit", sg.WIN_CLOSED]:
            break

        # if the user clicks the "Budgets" button, open the budget window
        if event == 'Budgets':
            budgetW.main()
        if event == 'Expenses and Income':
            expenses_income_W.main()

    window.close()
    del (window)


if __name__ == '__main__':
    # run the programm
    main()
