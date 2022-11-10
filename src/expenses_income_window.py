import PySimpleGUI as sg

try:    
    import data_handler
    import budgetwindow
except Exception:
    import src.data_handler as data_handler
    import src.budgetwindow as budgetwindow


CATEGORIES = budgetwindow.CATEGORIES

# start code here
def create_window():
    layout = [
        [sg.Text("Expenses and Income")],
        [sg.Text("Income", size=(15, 1)), sg.InputText(key="income")],
        [sg.Text("Expenses", size=(15, 1)), sg.InputText(key="expenses")],
        [sg.Text("Categories", size=(15, 1)), sg.Combo(CATEGORIES)]]
    return sg.Window("Expenses and Income", layout, finalize=True)

def main():
    window = create_window()
    while True:
        event, values = window.read()
        if event in ["Cancel", sg.WIN_CLOSED]:
            break
        if event == "Submit":
            print(values["income"])
            print(values["expenses"])

    window.close()

if __name__ == '__main__':
    main()
