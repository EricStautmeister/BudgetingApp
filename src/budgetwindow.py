import PySimpleGUI as sg
import json
import random


TIMEFRAMES: list[str] = ['All', 'Daily',
                         'Weekly', 'Monthly', 'Quarterly', 'Yearly']
CATEGORIES: list[str] = ['All', 'Food', 'Rent', 'Utilities',
                         'Transportation', 'Entertainment', 'Other']


def make_main_window():
    MAIN_BUDGET_LAYOUT: list[list[any]] = [
        [sg.Text('Budgets', font=('Arial', 20))],
        [sg.Text('', key="upper_bm_buffer")],
        [sg.Text('Timeframe:', size=(15, 1)), sg.Combo(
            TIMEFRAMES, size=(20, 4), readonly=True, key="timeframe"), sg.Text('Category:', size=(15, 1)), sg.Combo(
            CATEGORIES, size=(20, 4), readonly=True, key="category"), sg.Button('Apply Filters')],
        [sg.Multiline('', key="-OUTPUT-", autoscroll=True, size=(50, 10))],
        [sg.Text('', key="lower_bm_buffer")],
        [sg.Button('New Budget'), sg.Button('Manage income'),
         sg.Button('New Expense'), sg.Button('Exit')]
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
    return sg.Window('New Budget', NEW_BUDGET_LAYOUT, finalize=True)


def open_window():
    window2 = make_new_budget_window()
    while True:
        event, values = window2.read()

        if event in ["Cancel", sg.WIN_CLOSED]:
            break

        if event in ["Submit"]:
            with open("budget_data.json", "r") as f:
                # create object for json dump from current data
                current_budget_data: dict[str, dict[str, str | int]] = {values["budget_title_new"]: {"category": values["category_new"], "timeframe": values["timeframe_new"],
                                                                                                     "budget-amount": int(values["budget_amount_new"])}}
                try:
                    # load current data
                    loaded_json = json.load(f)
                    # update current data with new data
                    loaded_json.update(current_budget_data)

                    # dump updated data to data file
                    with open("budget_data.json", "w") as f:
                        json.dump(loaded_json, f)
                except Exception as e:
                    # if no data exists, create new data file
                    json.dump(current_budget_data, f)
            break

    window2.close()
    del (window2)


def main():
    window = make_main_window()

    def data_formatter(data: dict[str, dict[str, str | int]]) -> list[str]:
        data_list: list[list[str | int]] = []
        for key, value in data.items():
            data_list.append(
                f"Name: {key}\nCategory: {value['category']}\nTimeframe: {value['timeframe']}\nAmount: {value['budget-amount']}\n\n")
        return data_list

    def data_filter(dict: dict):
        category, timeframe = values["category"].upper(
        ), values["timeframe"].upper()
        filtered_dict = {}
        if category == '' or category == 'ALL' and timeframe == '' or timeframe == 'ALL':
            filtered_dict = dict
        else:
            for key, val in dict.items():

                if val["category"].upper() == category or val["category"].upper == 'ALL' or val["category"].upper == '' and val["timeframe"].upper() == timeframe or val["timeframe"].upper() == 'ALL' or val["timeframe"].upper() == '':
                    filtered_dict[key] = val

        return filtered_dict

    try:
        with open("budget_data.json", "r") as f:
            budget_data: dict = json.load(f)
            print(budget_data)
    except Exception as e:
        with open("budget_data.json", "w") as f:
            json.dump({}, f)

    while True:
        event, values = window.read()

        if event == "Apply Filters":
            display_data = data_formatter(data_filter(budget_data))

            for i in range(len(display_data)):
                window["-OUTPUT-"].print(display_data[i])

        if event in ["Exit", sg.WIN_CLOSED]:
            break

        if event in ["New Budget"]:
            open_window()

    window.close()
    del (window)


if __name__ == '__main__':
    main()
