import PySimpleGUI as sg
from src import budgetwindow as budgetW
from src import expenses_income_window as expenses_income_W
from src import data_handler


# global variables
sg.LOOK_AND_FEEL_TABLE['CustomTheme'] = {'BACKGROUND': '#FFFFFF',
                                            'TEXT': '#5B86E5',
                                            'INPUT': '#DDDDDD',
                                            'TEXT_INPUT': '#5B86E5',
                                            'SCROLL': '#99CC99',
                                            'BUTTON': ('#5B86E5', '#FFFFFF'),
                                            'PROGRESS': ('#D1826B', '#CC8019'),
                                            'BORDER': 1, 'SLIDER_DEPTH': 0,
                                            'PROGRESS_DEPTH': 0, }
font = ('Helvetica', 10, "bold")
THEME: str = 'CustomTheme'
sg.theme(THEME)
sg.set_options(font=font)
colors = ("white", sg.theme_background_color())


def create_main_window():
    """
    Das Hauptfenster wird definiert
    :return: Das Hauptfenster
    """
    LAYOUT: list[list[any]] = [[sg.Push(), sg.Text('Budgetti', font=("Helvetica", 12, "bold")), sg.Push()],
                               [sg.Button('Budgets', button_color=colors, image_filename="./Budgets.png", border_width=0),
                               sg.Button('Expenses\nand\nIncome', button_color=colors, image_filename="./EI.png", border_width=0)]]

    return sg.Window('Budgetti', LAYOUT)


def main():
    """
    Hauptfenster
    Gibt zwei Buttons aus, die auf die jeweiligen Fenster verweisen.
    """
    window: any = create_main_window()
    while True:
        event, _ = window.read()

        if event in ["Exit", sg.WIN_CLOSED]:
            # Fenster wird geschlossen
            break

        if event == 'Budgets':
            # Handhabt den Button "Budgets"
            # Öffnet das Fenster für die Budgets
            budgetW.main()

        if event == 'Expenses\nand\nIncome':
            # Handhabt den Button "Expenses and Income"
            # Öffnet das Fenster für die Ausgaben und Einnahmen
            expenses_income_W.main()

    # Cleanup
    window.close()
    del (window)


if __name__ == '__main__':
    main()
