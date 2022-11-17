import PySimpleGUI as sg

try:
    import data_handler
    import expenses_income_window as expenses_income_W
except Exception:
    import src.data_handler as data_handler
    import src.expenses_income_window as expenses_income_W


Data_Handler = data_handler.DataHandler()

TIMEFRAMES: list[str] = ['All', 'Daily',
                         'Weekly', 'Monthly', 'Quarterly', 'Yearly']
CATEGORIES: list[str] = ['All', 'Food', 'Rent', 'Utilities',
                         'Transportation', 'Entertainment', 'Other']


def make_main_window(budget_choises):
    # das fenster mit den budget namen und daten wird erstellt
    MAIN_BUDGET_LAYOUT: list[list[any]] = [
        [sg.Text('Budgets', font=('Arial', 20)),
         sg.Button('Reset Budget Value')],
        [sg.Text('', key="upper_bm_buffer")],
        [sg.Text('Timeframe:', size=(15, 1)), sg.Combo(
            TIMEFRAMES, size=(20, 4), readonly=True, key="timeframe"), sg.Text('Category:', size=(15, 1)), sg.Combo(
            CATEGORIES, size=(20, 4), readonly=True, key="category"), sg.Button('Apply Filters')],
        [sg.Listbox(budget_choises, size=(30, 20), key="-BUDGET_LIST-", enable_events=True),
         sg.Multiline('', key="-OUTPUT-", autoscroll=True,
                      size=(50, 10), font=('Arial', 12), enable_events=True)],
        [sg.Text('', key="lower_bm_buffer")],
        [sg.Button('New Budget'), sg.Push(), sg.Button('Exit')]
    ]
    return sg.Window('Budgeting', MAIN_BUDGET_LAYOUT, finalize=True)


def make_new_budget_window():
    # das neue budget fenster wird erstellt
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


def handle_float(input):
    # um input fehler zu vermeiden, wird der input in eine float gecasted
    try:
        return float(input)
    except ValueError:
        return None


def open_window():
    window2 = make_new_budget_window()
    while True:
        Data_Handler.load_data()
        event, values = window2.read()

        if event in ["Cancel", sg.WIN_CLOSED]:
            break

        if event in ["Submit"]:
            # create object for json dump from current data
            budget_value = handle_float(values["budget_amount_new"])
            current_budget_data: dict[str, dict[str, str | int]] = {values["budget_title_new"]: {"type": "b", "category": values["category_new"], "timeframe": values["timeframe_new"],
                                                                                                 "budget-amount": budget_value, "currently-left": budget_value, "expenses": {}}}
            Data_Handler.save_data(current_budget_data)
            break

    window2.close()
    del (window2)


def make_update_window():
    # das update budget fenster wird erstellt
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
    # das update fenster wird geöffnet
    window2 = make_update_window()
    while True:
        Data_Handler.load_data()
        event, values = window2.read()

        if event in ["Cancel", sg.WIN_CLOSED]:
            window2.close()
            del (window2)

        if event in ["Update selected Timeframe only"]:
            # reset all budgets in selected timeframe
            try:
                Data_Handler.reset_budgets(values["timeframe_update"][0])
                Data_Handler.save_data(None)
                window2.close()
                del (window2)
                win.close()
                del (win)

                break
            except IndexError:
                sg.popup("Please select a timeframe")
                continue

        if event in ["RESET ALL BUDGETS"]:
            # reset all budgets
            Data_Handler.reset_all_budgets()
            Data_Handler.save_data(None)
            window2.close()
            del (window2)
            win.close()
            del (win)
            break


def main():
    Data_Handler.load_data()
    keys = Data_Handler.format_data()

    # Setup
    window = make_main_window(keys)

    # Configs
    window["-OUTPUT-"].set_vscroll_position(0)
    window["-BUDGET_LIST-"].set_vscroll_position(0)

    while True:
        event, values = window.read()
        if values != None and values.get("-BUDGET_LIST-") != None:
            window["-OUTPUT-"].update("")
            Data_Handler.format_data()
            keyList = Data_Handler.formatted_data["keyList"]
            for i in range(len(keyList)):
                if len(values["-BUDGET_LIST-"]) == 0:
                    break
                if keyList[i] == values["-BUDGET_LIST-"][0]:
                    print(Data_Handler.formatted_data)
                    window["-OUTPUT-"].update(
                        Data_Handler.formatted_data["formatted_meta"][i])

        if event == "Apply Filters":
            # alle daten werden gefiltert, dann werden die keys in eine liste geschrieben
            # und die daten in die Infoliste  geschrieben
            window["-OUTPUT-"].update("")
            Data_Handler.load_data()
            Data_Handler.filter_data(values)
            Data_Handler.format_data()
            window["-BUDGET_LIST-"].update(
                Data_Handler.formatted_data["keyList"])

        if event == "Reset Budget Value":
            update_window(window)
        if event in ["Exit", sg.WIN_CLOSED]:
            # das programm wird beendet
            break
        if event in ["New Budget"]:
            # das neue budget fenster wird geöffnet
            open_window()
        # if event in ["Expenses and Income"]:
            # das expenses and income fenster wird geöffnet
            # expenses_income_W.main()

    # schließt das fenster und speichert die daten ab
    window.close()
    Data_Handler.save_data(None)
    del (window)


if __name__ == '__main__':
    main()
