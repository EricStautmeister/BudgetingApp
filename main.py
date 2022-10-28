import PySimpleGUI as sg
from src import mainwindow as mainW
from src import budgetwindow as budgetW
from src import expenseswindow as expensesW
from src import incomewindow as incomeW

# TODO: Income Expenses
#TODO: Budgeting
#TODO: Categories (Food, Rent, etc)
#TODO: Timeframe (Daily, Weekly, Monthly, Yearly)


window = sg.Window('Budgetti', mainW.LAYOUT)
sg.theme('DarkAmber')

def main():
    while True:
        event, values = window.read()
        if event in ["Exit", sg.WIN_CLOSED]:
            break
        if event == 'Set Budget':
            budgetW.open_window()
        if event == 'Set Income':
            print('Income Set')
        if event == 'Set Expenses':
            print('Expenses Set')

        # Output a message to the window
        print("Clear")

    # Finish up by removing from the screen
    window.close()

if __name__ == '__main__':
    main()
