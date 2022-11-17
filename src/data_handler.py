import datetime
import json
import sys
import os


"""
    Dieses Modul ist eine API um dem Budgetierungsprogramm 
    die Datenmanipulation weg zu abstrahieren.

    Es ist nicht für den Benutzer gedacht, sondern für die Entwickler.

    Sie ist dazu da, eine Abstraktionsschicht in den Rest der App zu bringen.
"""

# allow imports from outside the src folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# allow importing the src folder
sys.path.append(os.path.dirname(__file__))


class DataHandler():
    def __init__(self):
        self.rawdata = {}
        self.filtered_data = {}
        self.formatted_data = {}

    # FILE HANDLER METHODS
    def save_data(self, data: dict[str, dict[str, str | int]]) -> None:
        """
        This function takes in a dictionary with a dictionary, 
        and updates the budget data file with the new data into json format.

        :param data: dict[str, dict[str, str | int]]
        :type data: dict[str, dict[str, str | int]]
        """
        if data is None:
            self.load_data()
            with open("budget_data.json", "w") as f:
                json.dump(self.rawdata, f)
        else:
            try:
                self.load_data()
                self.rawdata.update(data)
                with open("budget_data.json", "w") as f:
                    json.dump(self.rawdata, f)
            except Exception as e:
                print(e)

    def load_data(self) -> dict[str, dict[str, str | int]]:
        try:
            with open("budget_data.json", "r") as f:
                loaded = json.load(f)
                loaded.update(self.rawdata)
                self.rawdata = loaded
                self.filtered_data = self.rawdata
            return self.rawdata
        except FileNotFoundError as e:
            with open("budget_data.json", "w") as f:
                json.dump({}, f)
            return {}

    def load_all_data(self) -> dict[str, dict[str, str | int]]:
        with open("budget_data.json", "r") as f:
            return json.load(f)

    # DATA FORMATTER METHODS
    def format_data(self) -> list[str]:
        try:
            keyList = [
                f"{key}" for key, value in self.filtered_data.items() if value["type"] == "b"]
            formatted_meta = [f"Name: {key}\nCategory: {value['category']}\nTimeframe: {value['timeframe']}\nEntire Amount: {value['budget-amount']}\nCurrent Amount: {value['currently-left']}\n\n" for key,
                              value in self.filtered_data.items() if value['type'] == "b"]
            formatted_meta.extend(
                [f"" for key, value in self.filtered_data.items() if value["type"] in ["i", "e"]])
            self.formatted_data = {"keyList": keyList,
                                   "formatted_meta": formatted_meta}
            return keyList
        except Exception as e:
            print(f"Error in Formatting: {e}")

    def filter_data(self, values) -> dict[str, dict[str, str | int]]:
        try:
            category, timeframe = values["category"].upper(
            ), values["timeframe"].upper()
            filtered_dict = {}
            if category in ["ALL", ""] and timeframe in ["ALL", ""]:
                self.filtered_data = self.rawdata
                return

            for key, value in self.rawdata.items():
                if value.get("timeframe") is None:
                    continue
                elif category in ['', 'ALL'] and value["timeframe"].upper() == timeframe:
                    filtered_dict[key] = value
                elif timeframe in ['', 'ALL'] and value["category"].upper() == category:
                    filtered_dict[key] = value
                elif value["category"].upper() == category and value["timeframe"].upper() == timeframe:
                    filtered_dict[key] = value
            self.filtered_data = filtered_dict
            return
        except Exception as e:
            print(e)

    # UTILITY METHODS
    def current_date_provider(self) -> str:
        return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # DATA MANIPULATION METHODS
    def reset_budgets(self, timeframe: str) -> None:
        # reset all budgets in a timeframe
        
        for _, budget in self.rawdata.items():
            if budget["type"] == "b":
                print(f"\n\n\n{budget}\n\n\n")
                if budget["timeframe"] == timeframe:
                    self.rawdata[budget]["currently-left"] = self.rawdata[budget]["budget-amount"]
                    self.rawdata[budget]["expenses"] = {}

    def reset_all_budgets(self) -> None:
        # reset all budgets
        for budget in self.rawdata:
            self.rawdata[budget]["currently-left"] = self.rawdata[budget]["budget-amount"]
            self.rawdata[budget]["expenses"] = {}

    def add_to_budget(self, budget_name: str, amount: int) -> None:
        # add to a budgets current value
        self.rawdata[budget_name]["currently-left"] += amount

    def deduct_from_budget(self, budget_name: str, amount: int) -> None:
        # deduct from a budgets current value
        self.rawdata[budget_name]["currently-left"] -= amount

    def remove_budget(self, budget_name: str) -> None:
        # delete a budget
        self.rawdata.pop(budget_name)

    def get_expenses_by_budget(self, budget_name: str) -> dict[str, dict[str, str | int]]:
        # returns a dictionary of expenses
        return self.rawdata[budget_name]["expenses"]

    def add_expense(self, budget_name: str, expense_name: str, amount: int, description: str) -> None:
        # add expense to budget and to expense list
        # update the budgets current value
        self.rawdata[budget_name]["expenses"][expense_name] = {
            "amount": amount, "description": description, "date": self.current_date_provider()}
        self.rawdata["expenses"].update({"type": "e", expense_name: {
            "amount": amount, "description": description, "related-budget": budget_name, "date": self.current_date_provider()}})
        self.deduct_from_budget(budget_name, amount)

    def remove_expense(self, budget_name: str, expense_name: str) -> None:
        # delete an expense
        self.rawdata[budget_name]["expenses"].pop(expense_name)
        self.rawdata["expenses"].pop(expense_name)

    def update_expense(self, budget_name: str, expense_name: str, amount: int) -> None:
        # update the budget amount
        self.rawdata[budget_name]["expenses"][expense_name]["amount"] = amount
        self.rawdata["expenses"][expense_name]["amount"] = amount

    def read_all_expenses(self) -> dict[str, dict[str, str | int]]:
        return self.rawdata["expenses"]

    def add_income_element(self, income_name: str, amount: int) -> None:
        self.rawdata["income"].update(
            {"type": "i", income_name: {"amount": amount}})

    def remove_income_element(self, income_name: str) -> None:
        self.rawdata["income"].pop(income_name)

    def load_expenses(self) -> dict[str, dict[str, str | int]]:
        try:
            return self.rawdata["expenses"]
        except KeyError:
            self.rawdata["expenses"].update({"type": "e"})
            return self.rawdata["expenses"]

    def load_income(self) -> dict[str, dict[str, str | int]]:
        try:
            return self.rawdata["income"]
        except KeyError:
            self.rawdata["income"].update({"type": "i"})
            return self.rawdata["income"]
