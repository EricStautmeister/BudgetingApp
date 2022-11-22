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

JSON_DATA_TEMPLATE: dict[str, dict[str, str | int]] = {
    "expenses": {"type": "e"},
    "income": {"type": "i"},
}

class DataHandler():
    def __init__(self):
        """
        Diese Funktion initialisiert die Klasse mit drei Variablen:
        rawdata: dict[str, dict[str, str | int]]
        filtered_data: dict[str, dict[str, str | int]]
        formatted_data: dict[str, list[str]]
        """
        self.rawdata = {}
        self.filtered_data = {}
        self.formatted_data = {}

    # FILE HANDLER METHODS
    def save_data(self, data: dict[str, dict[str, str | int]]) -> None:
        """
        Diese Funktion speichert die Daten in die Datei budget_data.json
        Dabei gibt es zwei Modi:

        1. Wenn keine neuen Daten kommen, wird die Datei einfach überschrieben
            mit den Daten, die sich in self.rawdata befinden.
        2. Wenn neue Daten kommen, werden diese mit den Daten in self.rawdata
            gemerged und dann gespeichert.

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
        """
        Diese Funktion lädt die Daten aus der Datei budget_data.json
        und speichert sie in self.rawdata

        :return: dict[str, dict[str, str | int]]: Alle Daten aus der Datei
        """
        try:
            with open("budget_data.json", "r") as f:
                loaded = json.load(f)
                loaded.update(self.rawdata)
                self.rawdata = loaded
                self.filtered_data = self.rawdata
            return self.rawdata
        except FileNotFoundError as e:
            with open("budget_data.json", "w") as f:
                json.dump(JSON_DATA_TEMPLATE, f)
            self.rawdata = JSON_DATA_TEMPLATE
            self.filtered_data = self.rawdata
            return self.rawdata

    def load_all_data(self) -> dict[str, dict[str, str | int]]:
        """
        Diese Funktion ist nicht in Gebrauch, 
        sie ist nur für das Konzept gedacht,  
        und könnte in Zukunft verwendet werden.

        :return: dict[str, dict[str, str | int]]: Alle Daten aus der Datei
        """
        with open("budget_data.json", "r") as f:
            return json.load(f)

    # DATA FORMATTER METHODS
    def format_data(self) -> list[str]:
        """
        Diese Funktion formatiert die Daten in eine Liste von Strings,
        die dann in der GUI angezeigt werden können.
        Es wird starker gebrauch von List Comprehensions gemacht.

        :return: list[str]: Liste von Strings, die die formatierten Daten enthalten
        """
        try:
            # eine Liste der Budget namen für die GUI
            keyList = [
                f"{key}" for key, value in self.filtered_data.items() if value["type"] == "b"]
            # eine Liste der Budgetdetails für die GUI
            formatted_meta = [f"Name: {key}\nCategory: {value['category']}\nTimeframe: {value['timeframe']}\nEntire Amount: {value['budget-amount']}\nCurrent Amount: {value['currently-left']}\n\n" for key,
                              value in self.filtered_data.items() if value['type'] == "b"]
            # eine Liste der Transaktionsnamen für die GUI
            formatted_meta.extend(
                [f"" for key, value in self.filtered_data.items() if value["type"] in ["i", "e"]])
            self.formatted_data = {"keyList": keyList,
                                   "formatted_meta": formatted_meta}
            return keyList
        except Exception as e:
            print(f"Error in Formatting: {e}")

    def filter_data(self, values) -> dict[str, dict[str, str | int]]:
        """
        Diese Funktion filtert die Daten nach den Kriterien, die der Benutzer
        in der GUI ausgewählt hat.

        :param values: dict[str, str]: Die Werte, die das Fenster zurückgibt
        :return: dict[str, dict[str, str | int]]: die gefilterten Daten
        """
        try:
            # die Daten werden für Einheitlichkeit in Grossbuchstaben umgewandelt
            category, timeframe = values["category"].upper(
            ), values["timeframe"].upper()
            filtered_dict = {}

            # wenn kein Filter ausgewählt wurde, wird nichts gefiltert
            if category in ["ALL", ""] and timeframe in ["ALL", ""]:
                self.filtered_data = self.rawdata
                return

            # es wird nach Kategorie und Zeitraum gefiltert
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
        """
        Diese Funktion gibt das aktuelle Datum zurück.
        Dies wird als Zeitstempel für die Transaktionen verwendet.

        :return: str: Das heutige Datum und die Zeit im Format dd/mm/yyyy, hh:mm:ss
        """
        return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # DATA MANIPULATION METHODS
    def reset_budgets(self, timeframe: str) -> None:
        """
        Diese Funktion setzt die Budgets zurück, die in einem bestimmten Zeitraum liegen.
        Sowohl das Expenses Objekt als auch die Transaktionen im Budget werden zurückgesetzt.

        :param timeframe: str: Der Zeitraum, für den die Budgets zurückgesetzt werden sollen
        :type timeframe: str
        """
        for _, budget in self.rawdata.items():
            if budget["type"] == "b":
                print(f"\n\n\n{budget}\n\n\n")
                if budget["timeframe"] == timeframe:
                    self.rawdata[budget]["currently-left"] = self.rawdata[budget]["budget-amount"]
                    self.rawdata[budget]["expenses"] = {}

    def reset_all_budgets(self) -> None:
        """
        Diese Funktion setzt alle Budget Werte zurück.
        Sowohl das Expenses Objekt als auch die Transaktionen im Budget werden zurückgesetzt.
        """
        for budget in self.rawdata:
            self.rawdata[budget]["currently-left"] = self.rawdata[budget]["budget-amount"]
            self.rawdata[budget]["expenses"] = {}

    def add_to_budget(self, budget_name: str, amount: int) -> None:
        """
        Diese Funktion fügt einen Betrag zu einem Budget hinzu.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :param budget_name: Der Name des Budgets zu dem der Betrag hinzugefügt werden soll
        :type budget_name: str
        :param amount: int: der Wert der hinzugefügt werden soll
        :type amount: int
        """
        self.rawdata[budget_name]["currently-left"] += amount

    def deduct_from_budget(self, budget_name: str, amount: int) -> None:
        """
        Diese Funktion zieht einen Betrag von einem Budget ab.

        :param budget_name: Der Name des Budgets von dem der Betrag abgezogen werden soll        
        :type budget_name: str
        :param amount: der Wert der abgezogen werden soll
        :type amount: int
        """
        self.rawdata[budget_name]["currently-left"] -= amount

    def remove_budget(self, budget_name: str) -> None:
        """
        Diese Funktion entfernt ein Budget aus den Daten.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :param budget_name: Der Name des Budgets, das entfernt werden soll
        :type budget_name: str
        """
        self.rawdata.pop(budget_name)

    def get_expenses_by_budget(self, budget_name: str) -> dict[str, dict[str, str | int]]:
        """
        Diese Funktion gibt die Ausgaben eines Budgets zurück.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :param budget_name: Der Name des Budgets, dessen Ausgaben zurückgegeben werden sollen
        :type budget_name: str
        :return: dict[str, dict[str, str | int]]: Die Ausgaben des Budgets
        """
        return self.rawdata[budget_name]["expenses"]

    def add_expense(self, budget_name: str, expense_name: str, amount: int, description: str) -> None:
        """
        Diese Funktion fügt eine Ausgabe hinzu.
        Die Ausgabe wird sowohl in das Budget hinzugefügt,
        als auch in die Transaktionen liste.
        Danach wird das Budget aktualisiert, indem der Betrag abgezogen wird.

        :param budget_name: Der Name des Budgets, zu dem die Ausgabe hinzugefügt werden soll
        :type budget_name: str
        :param expense_name: Der Name der Ausgabe
        :type expense_name: str
        :param amount: Der Betrag der Ausgabe
        :type amount: int
        :param description: Die Beschreibung der Ausgabe
        :type description: str
        """
        self.rawdata[budget_name]["expenses"][expense_name] = {
            "amount": amount, "description": description, "date": self.current_date_provider()}
        self.rawdata["expenses"].update({"type": "e", expense_name: {
            "amount": amount, "description": description, "related-budget": budget_name, "date": self.current_date_provider()}})
        self.deduct_from_budget(budget_name, amount)

    def remove_expense(self, budget_name: str, expense_name: str) -> None:
        """
        Diese Funktion entfernt eine Ausgabe aus einem Budget.
        Die Ausgabe wird sowohl aus dem Budget entfernt,
        als auch aus der Transaktionen liste.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :param budget_name: Der Name des Budgets, aus dem die Ausgabe entfernt werden soll
        :type budget_name: str
        :param expense_name: Der Name der Ausgabe
        :type expense_name: str
        """
        self.rawdata[budget_name]["expenses"].pop(expense_name)
        self.rawdata["expenses"].pop(expense_name)

    def update_expense(self, budget_name: str, expense_name: str, amount: int) -> None:
        """
        Diese Funktion aktualisiert eine Ausgabe.
        Die Ausgabe wird sowohl in dem Budget aktualisiert,
        als auch in der Transaktionen liste.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :param budget_name: Der Name des Budgets, in dem die Ausgabe aktualisiert werden soll
        :type budget_name: str
        :param expense_name: Der Name der Ausgabe
        :type expense_name: str
        :param amount: Der neue Betrag der Ausgabe
        :type amount: int
        """
        self.rawdata[budget_name]["expenses"][expense_name]["amount"] = amount
        self.rawdata["expenses"][expense_name]["amount"] = amount

    def read_all_expenses(self) -> dict[str, dict[str, str | int]]:
        """
        Diese Funktion gibt die Ausgaben Transaktionsliste zurück.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :return: dict[str, dict[str, str | int]]: Die Ausgaben Transaktionsliste
        """
        return self.rawdata["expenses"]

    def add_income_element(self, income_name: str, amount: int) -> None:
        """
        Diese Funktion fügt ein Einkommen hinzu.
        Das Einkommen wird in die Einkommen liste hinzugefügt.

        :param income_name: Der Name des Einkommens
        :type income_name: str
        :param amount: Der Betrag des Einkommens
        :type amount: int
        """
        self.rawdata["income"].update(
            {"type": "i", income_name: {"amount": amount}})

    def remove_income_element(self, income_name: str) -> None:
        """
        Diese Funktion entfernt ein Einkommen aus der Einkommen liste.

        Diese Funktion ist nicht in Gebrauch,
        sie ist nur für das Konzept gedacht,
        und könnte in Zukunft verwendet werden.

        :param income_name: Der Name des Einkommens
        :type income_name: str
        """
        self.rawdata["income"].pop(income_name)

    def load_expenses(self) -> dict[str, dict[str, str | int]]:
        """
        Es wird versucht, die Ausgaben Transaktionsliste zurückzugeben.
        Wenn dies nicht funktioniert, wird eine leere Ausgaben Transaktionsliste zurückgegeben.

        :return: dict[str, dict[str, str | int]]: Die Ausgaben Transaktionsliste
        """
        try:
            return self.rawdata["expenses"]
        except KeyError:
            self.rawdata["expenses"].update({"type": "e"})
            return self.rawdata["expenses"]

    def load_income(self) -> dict[str, dict[str, str | int]]:
        """
        Es wird versucht, die Einkommen liste zurückzugeben.
        Wenn dies nicht funktioniert, wird eine leere Einkommen liste zurückgegeben.

        :return: dict[str, dict[str, str | int]]: Die Einkommen liste
        """
        try:
            return self.rawdata["income"]
        except KeyError:
            self.rawdata["income"].update({"type": "i"})
            return self.rawdata["income"]
