import PySimpleGUI as sg

# Behandelt ein Importproblem
try:
    import data_handler
    # import expenses_income_window as expenses_income_W
except Exception:
    import src.data_handler as data_handler
    # import src.expenses_income_window as expenses_income_W

# Instanz der Klasse Data_Handler um mit den Daten zu arbeiten wird erstellt
Data_Handler = data_handler.DataHandler()

# die Kategorien und Zeitrahmen werden definiert
TIMEFRAMES: list[str] = ['All', 'Daily',
                         'Weekly', 'Monthly', 'Quarterly', 'Yearly']
CATEGORIES: list[str] = ['All', 'Food', 'Rent', 'Utilities',
                         'Transportation', 'Entertainment', 'Other']


def make_main_window(budget_choises: list[str]):
    """
    Das Budgetfenster wird definiert

    :param budget_choises: list[str] = []
    :return: Das Budgetfenster
    """
    MAIN_BUDGET_LAYOUT: list[list[any]] = [
        [sg.Text('Budgets', font=('Arial', 20)),
         sg.Button('Reset Budget Value'), sg.Push(), sg.Button('New Budget'), sg.Button('Delete Budget')],
        [sg.Text('', key="upper_bm_buffer")],
        [sg.Text('Timeframe:', size=(15, 1)), sg.Combo(
            TIMEFRAMES, size=(20, 8), readonly=True, key="timeframe"), sg.Text('Category:', size=(15, 1)), sg.Combo(
            CATEGORIES, size=(20, 8), readonly=True, key="category"), sg.Button('Apply Filters')],
        [sg.Listbox(budget_choises, size=(30, 20), key="-BUDGET_LIST-", enable_events=True),
         sg.Multiline('', key="-OUTPUT-", autoscroll=True,
                      size=(50, 10), font=('Arial', 12), enable_events=True)],
        [sg.Text('', key="lower_bm_buffer")],
        [sg.Push(), sg.Button('Exit')]
    ]
    return sg.Window('Budgeting', MAIN_BUDGET_LAYOUT, finalize=True)


def make_new_budget_window():
    """
    Das Fenster zum erstellen eines neuen Budgets wird definiert
    Darin kann der Titel, die Katgorie, der Zeitrahmen und der Budgetwert festgelegt werden
    :return: Ein Fenster zum erstellen eines neuen Budgets
    """

    NEW_BUDGET_LAYOUT: list[list[any]] = [[sg.Text('Set Budget')],
                                          [sg.Text('Category'), sg.Combo(CATEGORIES, size=(20, 1), key="category_new"),
                                           sg.Text('Timeframe'), sg.Combo(TIMEFRAMES, size=(20, 1), key="timeframe_new")],
                                          [sg.Text('Enter Budget Title:'),
                                           sg.InputText(key="budget_title_new")],
                                          [sg.Text('Enter Budget Amount:'),
                                           sg.InputText(key="budget_amount_new")],
                                          [sg.Button('Submit'),
                                           sg.Button('Cancel')]
                                          ]
    return sg.Window('New Budget', NEW_BUDGET_LAYOUT, )


def handle_float(input: str) -> float | None:
    """
    Die Eingabe wird in eine float gecastet und zur??ckgegeben,
    wenn das nicht m??glich ist wird None zur??ckgegeben

    :param input: str: Input der in eine float gecastet werden soll
    :return: float oder None
    """
    try:
        return float(input)
    except ValueError:
        return None


def new_budgets():
    """
    Das Fenster zum erstellen neuer Budgets wird ge??ffnet und gehandhabt. 
    """
    # Setup
    window2 = make_new_budget_window()

    while True:
        Data_Handler.load_data()
        event, values = window2.read()

        if event in ["Cancel", sg.WIN_CLOSED]:
            # Wenn das Fenster geschlossen wird, stoppt das Fenster
            break

        if event in ["Submit"]:
            # Wenn der Submit Button gedr??ckt wird, wird das Budget erstellt
            # Die Eingaben werden ??berpr??ft und das Budget erstellt und gespeichert
            # Dann wird das Fenster geschlossen
            budget_value = handle_float(values["budget_amount_new"])
            current_budget_data: dict[str, dict[str, str | int]] = {values["budget_title_new"]: {"type": "b", "category": values["category_new"], "timeframe": values["timeframe_new"],
                                                                                                 "budget-amount": budget_value, "currently-left": budget_value, "expenses": {}}}
            Data_Handler.save_data(current_budget_data)
            break

    window2.close()
    del (window2)


def make_update_window():
    """
    Das Fenster zum updaten der Budgets wird definiert
    :return: Ein Fenster zum updaten der Budgets
    """
    UPDATE_BUDGET_LAYOUT: list[list[any]] = [[sg.Text('Update Budget')],
                                             [sg.Text('Timeframe'), sg.Combo(
                                                 TIMEFRAMES, size=(20, 1), key="timeframe_update")],
                                             [sg.Button(
                                                 'Update selected Timeframe only')],
                                             [sg.Text("")],
                                             [sg.Button(
                                                 'UPDATE ALL TIMEFRAMES')],
                                             [sg.Button('Cancel')]
                                             ]
    return sg.Window('Update Budget', UPDATE_BUDGET_LAYOUT, )


def update_window(win):
    """
    Das Fenster zum updaten der Budgets wird ge??ffnet und gehandhabt.
    Darin kann der Zeitrahmen ausgew??hlt werden, der upgedatet werden soll
    Wird ein Zeitraum ausgew??hlt, werden alle Budgets mit diesem Zeitraum upgedatet
    Wird alle Zeitrahmen ausgew??hlt, werden alle Budgets upgedatet

    :param win: Das Budgetfenster
    """
    # Setup
    window2 = make_update_window()

    while True:
        Data_Handler.load_data()
        event, values = window2.read()

        if event in ["Cancel", sg.WIN_CLOSED]:
            # Wenn das Fenster geschlossen wird, stoppt das Fenster
            window2.close()
            del (window2)

        if event in ["Update selected Timeframe only"]:
            # Wenn der Update selected Timeframe only Button gedr??ckt wird,
            # werden alle Budgets mit dem ausgew??hlten Zeitraum upgedatet
            try:
                Data_Handler.reset_budgets(values["timeframe_update"])
                Data_Handler.save_data(None, mode=1)
                window2.close()
                del(window2)
                break
            except IndexError:
                sg.popup("Please select a timeframe")
                continue

        if event in ["RESET ALL BUDGETS"]:
            # Wenn der RESET ALL BUDGETS Button gedr??ckt wird,
            # werden alle Budgets upgedatet
            Data_Handler.reset_all_budgets()
            Data_Handler.save_data(None)
            window2.close()
            del(window2)
            break


def delete_budget():
    """
    Das Fenster zum l??schen eines Budgets wird ge??ffnet und gehandhabt.
    """
    # Setup
    layout = [[sg.Text('Delete Budget')],
              [sg.Text('Enter Budget Title:'),
               sg.DropDown(Data_Handler.formatted_data["keyList"], size=(20, 1), key="budget_title_delete")],
              [sg.Button('Submit'),
               sg.Button('Cancel')]
              ]
    window2 = sg.Window('Delete Budget', layout, )

    while True:
        Data_Handler.load_data()
        event, values = window2.read()

        def warning_popup():
            """
            Ein Popup wird ge??ffnet, wenn kein Budget ausgew??hlt ist
            """
            sg.popup("You have not picked a budget", title="Warning", keep_on_top=True)

        if event in ["Cancel", sg.WIN_CLOSED]:
            # Wenn das Fenster geschlossen wird, stoppt das Fenster
            break

        if event in ["Submit"]:
            # Wenn der Submit Button gedr??ckt wird, wird das Budget gel??scht
            # Wenn das Budget nicht existiert, wird eine Fehlermeldung angezeigt
            try:
                if values["budget_title_delete"] == "": 
                    warning_popup()
                    continue
                Data_Handler.delete_budget(values["budget_title_delete"])
                Data_Handler.save_data(None, mode=1)
                Data_Handler.format_data()
                break
            except KeyError:
                sg.popup("Budget does not exist")
                continue

    window2.close()
    del (window2)


def reload_budgets(window, values):
    # Wenn der Apply Filters Button gedr??ckt wird,
    # werden die Budgets gefiltert
    # Die Filter werden aus dem Fenster geholt
    # und an die Data_Handler Klasse weitergegeben
    # Die Budgets werden gefiltert, neu formatiert und angezeigt
    window["-OUTPUT-"].update("")
    Data_Handler.load_data()
    Data_Handler.filter_data(values)
    Data_Handler.format_data()
    window["-BUDGET_LIST-"].update(
        Data_Handler.formatted_data["keyList"])


def main():
    """
    Das Budgetfenster wird ge??ffnet und gehandhabt.
    Darin werden alle Budgets angezeigt und k??nnen 
    angeklickt werden um die Budgetdetails zu sehen

    TODO: Budgets k??nnen gel??scht werden
    TODO: Budgets k??nnen bearbeitet werden
    TODO: Budgets sollen resetted werden k??nnen
    """

    # Setup
    Data_Handler.load_data()
    keys = Data_Handler.format_data()
    window = make_main_window(keys)

    # Configs
    window["-OUTPUT-"].set_vscroll_position(0)
    window["-BUDGET_LIST-"].set_vscroll_position(0)

    while True:
        event, values = window.read()
        if values != None and values.get("-BUDGET_LIST-") != None:
            # Wenn ein Budget ausgew??hlt wird,
            # werden die Budgetdetails angezeigt
            # Die Budgetdetails werden aus der Data_Handler Klasse geholt
            # und in das Fenster geschrieben
            window["-OUTPUT-"].update("")
            Data_Handler.format_data()
            keyList = Data_Handler.formatted_data["keyList"]
            for i in range(len(keyList)):
                if len(values["-BUDGET_LIST-"]) == 0:
                    break
                if keyList[i] == values["-BUDGET_LIST-"][0]:
                    window["-OUTPUT-"].update(
                        Data_Handler.formatted_data["formatted_meta"][i])

        if event == "Apply Filters":
            # Wenn der Apply Filters Button gedr??ckt wird,
            # werden die Budgets gefiltert und wieder angezeigt
            reload_budgets(window, values)

        if event == "Reset Budget Value":
            # Wenn der Reset Budget Value Button gedr??ckt wird,
            # wird das Fenster zum updaten der Budgets ge??ffnet
            update_window(window)
            reload_budgets(window, values)

        if event in ["Exit", sg.WIN_CLOSED]:
            # Wenn das Fenster geschlossen wird, stoppt das Fenster
            break

        if event in ["New Budget"]:
            # Wenn der New Budget Button gedr??ckt wird,
            # wird das Fenster zum erstellen eines neuen Budgets ge??ffnet
            new_budgets()
            reload_budgets(window, values)

        if event in ["Delete Budget"]:
            # Wenn der Delete Budget Button gedr??ckt wird,
            # wird das Fenster zum l??schen eines Budgets ge??ffnet
            delete_budget()
            reload_budgets(window, values)


    # Cleanup
    window.close()
    Data_Handler.save_data(None)
    del (window)


if __name__ == '__main__':
    main()
