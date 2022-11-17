import PySimpleGUI as sg
from src import budgetwindow as budgetW
from src import expenses_income_window as expenses_income_W
from src import data_handler


# global variables
THEME: str = 'DarkAmber'
sg.theme(THEME)


def create_main_window():
    """
    Erstellt das Hauptfenster
    :return: Das Hauptfenster
    """
    LAYOUT: list[list[any]] = [[sg.Push(), sg.Text('Budgetti'), sg.Push()],
                               [sg.Button('Budgets'), sg.Button(
                                   'Expenses and Income')]]

    return sg.Window('Budgetti', LAYOUT)


def main():
    """
    Hauptfenster
    Gibt zwei Buttons aus, die auf die jeweiligen Fenster verweisen.
    """
    window: any = create_main_window()
    while True:
        event, _ = window.read()
        # Handhabt das Schließen des Fensters
        if event in ["Exit", sg.WIN_CLOSED]:
            break

        # Handhabt den Button "Budgets"
        if event == 'Budgets':
            budgetW.main()

        # Handhabt den Button "Expenses and Income"
        if event == 'Expenses and Income':
            expenses_income_W.main()

    window.close()
    del (window)


if __name__ == '__main__':
    main()
