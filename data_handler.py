import json


class DataHandler():
    def __init__(self):
        pass

    def save_data(self, data: dict[str, dict[str, str | int]]) -> None:
        """
        This function takes in a dictionary with a dictionary, 
        and updates the budget data file with the new data in json format.

        :param data: dict[str, dict[str, str | int]]
        :type data: dict[str, dict[str, str | int]]
        """
        try:
            # load current data
            loaded_json = json.load(f)
            # update current data with new data
            loaded_json.update(data)

            # dump updated data to data file
            with open("budget_data.json", "w") as f:
                json.dump(loaded_json, f)
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
    
    def format_data(self, data: dict[str, dict[str, str | int]]) -> list[str]:
        return [f"Name: {key}\nCategory: {value['category']}\nTimeframe: {value['timeframe']}\nAmount: {value['budget-amount']}\n\n" for key, value in data.items()]

    def filter_data(self, values, dict: dict):
        category, timeframe = values["category"].upper(
        ), values["timeframe"].upper()
        filtered_dict = {}
        if category == '' or category == 'ALL' and timeframe == '' or timeframe == 'ALL':
            filtered_dict = dict
        elif category in ['', 'ALL']:
            for key, value in dict.items():
                if value["timeframe"].upper() == timeframe:
                    filtered_dict[key] = value
        elif timeframe in ['', 'ALL']:
            for key, value in dict.items():
                if value["category"].upper() == category:
                    filtered_dict[key] = value
        else:
            for key, value in dict.items():
                if value["category"].upper() == category and value["timeframe"].upper() == timeframe:
                    filtered_dict[key] = value
        return filtered_dict
