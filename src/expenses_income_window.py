import PySimpleGUI as sg

try:
    import data_handler
    import budgetwindow
except Exception:
    import src.data_handler as data_handler
    import src.budgetwindow as budgetwindow


CATEGORIES = budgetwindow.CATEGORIES
Data_Handler = data_handler.DataHandler()


def create_expense_view_window():
    """
    Needed:
        - Add Expense and Income
            - Category
            - Amount
            - Date
            - Description
        - List of Expenses and Income
        - Total Expenses and Income

    """
    view_expenses = [
        [sg.Text("View Expenses and Income"), sg.Push(),
         sg.Button("New Expense or Income")],
        [sg.Text("Expenses"), sg.Push(), sg.Text("Income"), sg.Push()],
        [sg.Listbox([], size=(40, 10), key="-expenses-"),
         sg.Listbox([], size=(40, 10), key="-income-")],
        [sg.Push(), sg.Button("Save and Exit")]
    ]
    return sg.Window("Expenses and Income", view_expenses, finalize=True)


def create_new_expense_window():
    """
    Needed:
        - Add Expense and Income
            - Category
            - Amount
            - Date
            - Description
        - List of Expenses and Income
        - Total Expenses and Income

    """

    Data_Handler.load_data()
    Data_Handler.format_data()
    keyList = Data_Handler.formatted_data["keyList"]

    print(Data_Handler.formatted_data)

    MODES = ["Expense", "Income"]

    new_expense_layout = [
        [sg.Text("Add Expense or Income")],
        [sg.Text("Mode"), sg.Listbox(MODES, size=(20, 2), key="mode")],
        [sg.Text("Expense Title"), sg.InputText(key="EI_name")],
        [sg.Text("Budget"), sg.Listbox(keyList, size=(20, 2), key="BName")],
        [sg.Text("Amount"), sg.InputText(key="amount")],
        [sg.Text("Description"), sg.InputText(key="description")],
        [sg.Button("Add"), sg.Push(), sg.Button("Cancel")]
    ]
    return sg.Window("Expenses and Income", new_expense_layout, finalize=True)


def handle_float(input: str) -> float | int:
    # um input fehler zu vermeiden, wird der input in eine float gecasted
    try:
        return float(input)
    except ValueError:
        return 0


def new_expense_or_income():
    window2 = create_new_expense_window()
    while True:
        event, values = window2.read()
        if event == "Add":
            try:
                if values["mode"][0] == "Expense":
                    Data_Handler.add_expense(
                        values["BName"][0], values["EI_name"], handle_float(values["amount"]), values["description"])
                elif values["mode"][0] == "Income":
                    Data_Handler.add_income_element(
                        values["EI_name"], values["amount"])
                else:
                    raise TypeError("No mode selected when adding expense or income")
            except Exception as e:
                sg.popup(e)
            Data_Handler.save_data(None)
            break
        if event in ["Cancel", sg.WIN_CLOSED]:
            break
    
    window2.close()
    del (window2)


def main():
    window = create_expense_view_window()
    Data_Handler.load_data()
    Data_Handler.format_data()

    while True:
        expenses = Data_Handler.load_expenses()
        print(expenses)
        income = Data_Handler.load_income()
        formatted_expenses = [
            f"{key}\n- {expense['amount']}\n- {expense['description']}\n\n" for key, expense in expenses.items() if key != 'type']
        formatted_income = [
            f"{key}\n- {income['amount']}\n\n" for key, income in income.items() if key != 'type']
        window["-expenses-"].update(formatted_expenses)
        window["-income-"].update(formatted_income)

        event, values = window.read()
        if event in ["Save and Exit", sg.WIN_CLOSED]:
            break
        if event == "New Expense or Income":
            new_expense_or_income()
        if values["-expenses-"]:
            sg.popup(values["-expenses-"][0])

    Data_Handler.save_data(None)
    window.close()
    del (window)


if __name__ == '__main__':
    main()
