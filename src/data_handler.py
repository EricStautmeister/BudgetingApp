import json
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# what does the above line do?
# it adds the current directory to the path so that the module can be imported

class DataHandler():
    def __init__(self):
        pass

    def save_data(self, data: dict[str, dict[str, str | int]]) -> None:
        """
        This function takes in a dictionary with a dictionary, 
        and updates the budget data file with the new data into json format.

        :param data: dict[str, dict[str, str | int]]
        :type data: dict[str, dict[str, str | int]]
        """
        try:
            with open("budget_data.json", "r") as f:
                current_budget_data = json.load(f)
                current_budget_data.update(data)
                with open("budget_data.json", "w") as f:
                    json.dump(current_budget_data, f)
        except Exception as e:
            # if no data exists, create new data file
            json.dump(data, f)

    def load_data(self) -> dict[str, dict[str, str | int]]:
        try:
            with open("budget_data.json", "r") as f:
                return json.load(f)
        except Exception as e:
            with open("budget_data.json", "w") as f:
                json.dump({}, f)
            return {}
    
    def load_all_data(self) -> dict[str, dict[str, str | int]]:
        with open("budget_data.json", "r") as f:
            return json.load(f)
    
    def format_data(self, data: dict[str, dict[str, str | int]]) -> list[str]:
        keyList = [f"{key}" for key in data]
        formated_data_list = [f"Name: {key}\nCategory: {value['category']}\nTimeframe: {value['timeframe']}\nAmount: {value['budget-amount']}\n\n" for key, value in data.items()]
        return {"keyList":keyList, "formatted_data_list":formated_data_list}

    def filter_data(self, values, dict: dict[str, dict[str, str | int]]):
        category, timeframe = values["category"].upper(
        ), values["timeframe"].upper()
        filtered_dict = {}        
        if category == "ALL" and timeframe == "ALL":
            return dict
        if category == "" and timeframe == "":
            return dict
        if category == "ALL" and timeframe == "":
            return dict
        if category == "" and timeframe == "ALL":
            return dict
        for key, value in dict.items():
            if category in ['', 'ALL'] and value["timeframe"].upper() == timeframe:
                filtered_dict[key] = value
            elif timeframe in ['', 'ALL'] and value["category"].upper() == category:
                filtered_dict[key] = value
            elif value["category"].upper() == category and value["timeframe"].upper() == timeframe:
                filtered_dict[key] = value
        return filtered_dict
