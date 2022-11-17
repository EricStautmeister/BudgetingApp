import PySimpleGUI as sg

# Behandelt Importfehler
try:
    import data_handler
    import budgetwindow
except Exception:
    import src.data_handler as data_handler
    import src.budgetwindow as budgetwindow

# Importiert die Kategorien
CATEGORIES = budgetwindow.CATEGORIES
# Die API wird instanziiert um mit den Daten zu arbeiten
Data_Handler = data_handler.DataHandler()


def create_expense_view_window():
    """
    Das Fenster für die Ausgaben und Einnahmen wird definiert
    Es besteht aus zwei Listboxen, einer für die Ausgaben und einer für die Einnahmen

    :return: Das Fenster für die Ausgaben und Einnahmen
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
    Das Fenster für neue Ausgaben und Einnahmen wird definiert

    :return: Das Fenster für neue Ausgaben und Einahmen
    """

    # Setup
    Data_Handler.load_data()
    Data_Handler.format_data()
    keyList = Data_Handler.formatted_data["keyList"]
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
    """
    Es wird versucht, den Input in eine Floatzahl umzuwandeln.
    Wenn dies nicht möglich ist, wird 0 zurückgegeben. 

    :param input: Die input String
    :return: Die Eingabe als Float oder 0
    """
    try:
        return float(input)
    except ValueError:
        return 0


def new_expense_or_income():
    """
    Das Fenster für neue Ausgaben und Einnahmen wird geöffnet.
    Man kann die Werte eingeben und dann auf "Add" drücken.
    Dann werden die Daten and den DataHandler geschickt,
    der die Daten in das Datenobjekt hinzufügt.
    """
    window2 = create_new_expense_window()
    while True:
        event, values = window2.read()
        if event == "Add":
            # Die Werte werden aus den Eingabefeldern geholt
            # und in die richtigen Variablen gespeichert
            # Es wird dabei zwischen Ausgaben und Einnahmen unterschieden
            try:
                if values["mode"][0] == "Expense":
                    Data_Handler.add_expense(
                        values["BName"][0], values["EI_name"], handle_float(values["amount"]), values["description"])
                elif values["mode"][0] == "Income":
                    Data_Handler.add_income_element(
                        values["EI_name"], values["amount"])
                else:
                    raise TypeError(
                        "No mode selected when adding expense or income")
            except Exception as e:
                sg.popup(e)
            Data_Handler.save_data(None)
            break
        if event in ["Cancel", sg.WIN_CLOSED]:
            break

    window2.close()
    del (window2)


def main():
    """
    Das Ausgaben und Einnahmen Fenster wird geöffnet und die Daten werden geladen.
    Es werden die Ausgaben und Einnahmen in die Listboxen geschrieben,
    nachdem sie entsprechend formatiert wurden.

    TODO: Better formatting of expenses and income
    TODO: Income needs to be able to affect a budget
    TODO: Clicking on an income should open a window to view and edit it
    """

    # Setup
    window = create_expense_view_window()
    Data_Handler.load_data()
    Data_Handler.format_data()

    while True:
        expenses = Data_Handler.load_expenses()
        income = Data_Handler.load_income()

        # Die Ausgaben und Einnahmen werden formattiert mithilfe von List Comprehensions
        # Die Ausgaben und Einnahmen werden in die Listboxen geschrieben
        formatted_expenses = [
            f"{key}\n- {expense['amount']}\n- {expense['description']}\n\n" for key, expense in expenses.items() if key != 'type']
        formatted_income = [
            f"{key}\n- {income['amount']}\n\n" for key, income in income.items() if key != 'type']
        window["-expenses-"].update(formatted_expenses)
        window["-income-"].update(formatted_income)

        event, values = window.read()
        if event in ["Save and Exit", sg.WIN_CLOSED]:
            # Die Daten werden gespeichert und das Fenster geschlossen
            break
        if event == "New Expense or Income":
            # Das Fenster für neue Ausgaben und Einnahmen wird geöffnet
            new_expense_or_income()
        if values["-expenses-"]:
            # Funktioniert noch nicht (raise NotImplementedError)
            sg.popup(values["-expenses-"][0])

    # Cleanup
    Data_Handler.save_data(None)
    window.close()
    del (window)


if __name__ == '__main__':
    main()
