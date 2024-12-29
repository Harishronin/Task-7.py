""""
Name:Harishkumar
Program1:Use the url https://restcountries.com/v3.1/all with python

1.using oops concept for the following task
2.Using the class constructor for taking input the above mentioned url for the task
3.create a method that will fetch all json data from the url mentioned above
4.create a method that will display all the name of countires,curriencies and currency symbol
5.create a method that will display all those countires whose currency as dollar
6.create a method that will display all those countires whose currency as euros
Date:29-dec-2024
"""
import requests


class CountryData:
    def __init__(self, url):

        # Constructor
        self.url = url
        self.data = None

    def fetch_data(self):

        # Method to fetch JSON data from the given URL.

        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.data = response.json()
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def display_country_currency_info(self):

        # Method to display all countries, their currencies, and currency symbols.

        if not self.data:
            print("Data is not loaded. Please fetch data first.")
            return

        print("Countries, Currencies, and Symbols:")
        for country in self.data:
            name = country.get("name", {}).get("common", "Unknown")
            currencies = country.get("currencies", {})
            if currencies:
                for currency_code, currency_info in currencies.items():
                    print(f"Country: {name}, Currency: {currency_code}, Symbol: {currency_info.get('symbol', 'N/A')}")
            else:
                print(f"Country: {name}, Currency: N/A, Symbol: N/A")

    def countries_with_currency(self, currency_name):

        # Method to display all countries using the specified currency (e.g., Dollar or Euro).

        if not self.data:
            print("Data is not loaded. Please fetch data first.")
            return

        matching_countries = []
        for country in self.data:
            currencies = country.get("currencies", {})
            for currency_code, currency_info in currencies.items():
                if currency_name.lower() in currency_info.get("name", "").lower():
                    matching_countries.append(country.get("name", {}).get("common", "Unknown"))

        if matching_countries:
            print(f"Countries using {currency_name}:")
            print(", ".join(matching_countries))
        else:
            print(f"No countries found using {currency_name}.")

    def display_countries_with_dollar(self):

        # Method to display all countries whose currency is Dollar.

        self.countries_with_currency("dollar")

    def display_countries_with_euro(self):

        # Method to display all countries whose currency is Euro.

        self.countries_with_currency("euro")


# Main Program
if __name__ == "__main__":
    url = "https://restcountries.com/v3.1/all"
    country_data = CountryData(url)

    # Fetch data
    country_data.fetch_data()

    # Display country, currency, and symbol information
    country_data.display_country_currency_info()

    # Display countries using Dollar
    country_data.display_countries_with_dollar()

    # Display countries using Euro
    country_data.display_countries_with_euro()

""""
Name:Harishkumar

Program2:Visit the URL https://www.openbrewerydb.org/ write a python script and do the following.

1.List the names of all the breweries present in the state of alaska,maine and newyork.
2.What is the count of breweries in each of the states mentioned above
3.Count the number of breweries present in each of the state above mentioned
4.Count and list how many breweries have websites in the states of Alaska,aine and Newyork
Date:29-dec-2024
"""

import requests
from collections import defaultdict


class BreweryData:
    def __init__(self):
        """
        Constructor to initialize the base URL and list of states.
        """
        self.base_url = "https://api.openbrewerydb.org/breweries"
        self.states = ["alaska", "maine", "new_york"]

    def fetch_breweries_by_state(self, state):

        # Fetch all breweries for a given state.

        try:
            response = requests.get(f"{self.base_url}?by_state={state}&per_page=100")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"An error occurred while fetching data for state {state}: {e}")
            return []

    def list_breweries(self):

        # List the names of all breweries in the states of Alaska, Maine, and New York.

        breweries_by_state = {}
        for state in self.states:
            data = self.fetch_breweries_by_state(state)
            brewery_names = [brewery["name"] for brewery in data]
            breweries_by_state[state] = brewery_names
        return breweries_by_state

    def count_breweries_by_state(self):

        # Count the number of breweries in each state.

        counts = {}
        for state in self.states:
            data = self.fetch_breweries_by_state(state)
            counts[state] = len(data)
        return counts

    def count_brewery_types_by_city(self):

        # Count the number of types of breweries in individual cities of the states.

        brewery_types_by_city = defaultdict(lambda: defaultdict(int))
        for state in self.states:
            data = self.fetch_breweries_by_state(state)
            for brewery in data:
                city = brewery.get("city", "Unknown")
                brewery_type = brewery.get("brewery_type", "Unknown")
                brewery_types_by_city[state][city][brewery_type] += 1
        return brewery_types_by_city

    def count_breweries_with_websites(self):

        # Count and list the number of breweries with websites in the specified states.

        breweries_with_websites = defaultdict(list)
        for state in self.states:
            data = self.fetch_breweries_by_state(state)
            for brewery in data:
                if brewery.get("website_url"):
                    breweries_with_websites[state].append(brewery["name"])
        return {state: len(names) for state, names in breweries_with_websites.items()}


# Instantiate
if __name__ == "__main__":
    brewery_data = BreweryData()

    # 1. List names of all breweries in specified states
    breweries = brewery_data.list_breweries()
    print("Breweries in specified states:")
    for state, names in breweries.items():
        print(f"{state.title()}: {', '.join(names)}")

    # 2. Count breweries in each state
    counts = brewery_data.count_breweries_by_state()
    print("\nCount of breweries in each state:")
    for state, count in counts.items():
        print(f"{state.title()}: {count}")

    # 3. Count breweries with websites
    websites_count = brewery_data.count_breweries_with_websites()
    print("\nBreweries with websites:")
    for state, count in websites_count.items():
        print(f"{state.title()}: {count} breweries have websites")
