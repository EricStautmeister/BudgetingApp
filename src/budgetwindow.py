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
    MAIN_BUDGET_LAYOUT: list[list[any]] = [
        [sg.Text('Budgets', font=('Arial', 20))],
        [sg.Text('', key="upper_bm_buffer")],
        [sg.Text('Timeframe:', size=(15, 1)), sg.Combo(
            TIMEFRAMES, size=(20, 4), readonly=True, key="timeframe"), sg.Text('Category:', size=(15, 1)), sg.Combo(
            CATEGORIES, size=(20, 4), readonly=True, key="category"), sg.Button('Apply Filters')],
        [sg.Listbox(budget_choises, size=(100, 20), key="-BUDGET_LIST-", enable_events=True),
         sg.Multiline('', key="-OUTPUT-", autoscroll=True,
                      size=(50, 10), font=('Arial', 12), enable_events=True)],
        [sg.Text('', key="lower_bm_buffer")],
        [sg.Button('New Budget'), sg.Push(), sg.Button(
            "Expenses and Income"), sg.Button('Exit')]
    ]
    return sg.Window('Budgeting', MAIN_BUDGET_LAYOUT, finalize=True)


def make_new_budget_window():
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
    try:
        return float(input)
    except ValueError:
        return None


def open_window():
    window2 = make_new_budget_window()
    while True:
        event, values = window2.read()

        if event in ["Cancel", sg.WIN_CLOSED]:
            break

        if event in ["Submit"]:
            with open("budget_data.json", "r") as f:
                # create object for json dump from current data
                budget_value = handle_float(values["budget_amount_new"])
                current_budget_data: dict[str, dict[str, str | int]] = {values["budget_title_new"]: {"category": values["category_new"], "timeframe": values["timeframe_new"],
                                                                                                     "budget-amount": budget_value, "currently-left": budget_value, "expenses": {}}}
                Data_Handler.save_data(current_budget_data)
            break

    window2.close()
    del (window2)


def main():
    rawData = Data_Handler.load_data()
    budgetData = Data_Handler.format_data(
        Data_Handler.load_data())
    keyList, formatted_data_list = budgetData["keyList"], budgetData["formatted_data_list"]
    window = make_main_window(keyList)
    window["-OUTPUT-"].set_vscroll_position(0)
    window["-BUDGET_LIST-"].set_vscroll_position(0)

    while True:
        event, values = window.read()
        if values["-BUDGET_LIST-"]:
            window["-OUTPUT-"].update("")
            for i in range(len(keyList)):
                if values["-BUDGET_LIST-"][0] == keyList[i]:
                    window["-OUTPUT-"].print(formatted_data_list[i])
        if event == "Apply Filters":
            window["-OUTPUT-"].update("")
            filtered_key_list = Data_Handler.format_data(
                Data_Handler.filter_data(values, rawData))["keyList"]
            window["-BUDGET_LIST-"].update(filtered_key_list)
        if event in ["Exit", sg.WIN_CLOSED]:
            break
        if event in ["New Budget"]:
            open_window()
        if event in ["Expenses and Income"]:
            expenses_income_W.main()

    window.close()
    del (window)


if __name__ == '__main__':
    main()
