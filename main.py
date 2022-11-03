import PySimpleGUI as sg

# Import various files for the GUI
from src import mainwindow as mainW
from src import budgetwindow as budgetW
from src import expenseswindow as expensesW
from src import incomewindow as incomeW

# global variables
THEME: str = 'DarkAmber'
sg.theme(THEME)

def create_main_window():
    return sg.Window('Budgetti', mainW.LAYOUT)

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
        if event == 'Set Income':
            print('Income')
        if event == 'Set Expenses':
            print('Expenses')

    # Finish up by removing from the screen
    window.close()


if __name__ == '__main__':
    # run the programm
    main()
