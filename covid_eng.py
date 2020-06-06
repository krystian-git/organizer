from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


import pandas as pd
import requests
import json

# getting currency rate from nbp's api
r = requests.get('http://api.nbp.pl/api/exchangerates/tables/A/')
jsonfile = r.text
currency = json.loads(jsonfile)
pln_euro_rate = currency[0]['rates'][7]['mid']

# getting official stats for covid-19 from ecdc website
list_covid = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv')
countries_grouped = list_covid.groupby('countriesAndTerritories')[['deaths','cases']]\
                    .sum().sort_values('deaths', ascending=False).head(20)
countries_list = countries_grouped.index.to_list()
countries_deaths = countries_grouped.deaths.to_list()
countries_cases = countries_grouped.cases.to_list()

# geting oil price from jonesoil / ballina
r = requests.post('https://jonesoil.ie/api/get_banded_oil_prices/product/1/quantity/1000',\
                          headers={"User-Agent":"Mozilla/5.0"})
oil = json.loads(r.text)
oil_price = oil['real_price']

class BoxContainer(BoxLayout):
    
    def feurolabel(self):
    # return euro rate to euroscreen's label
        self.ids.euro_pln.text = str(pln_euro_rate)
        self.ids.eurolabel.text = 'Euro stoi po:'

    def oilprice(self):
        self.ids.oil.text = 'Cheapest Heating Oil in Ballina '
        self.ids.oil_price.text = 'Jones Oil: ' + oil_price + '  for 1000l'

    def tables(self):
        table_container = self.ids.covids
        data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            rows_num = 15,
            sort = True,
            column_data=[
                ("Country", dp(60)),
                ("Deaths", dp(20)),
                ("Cases", dp(20)),
                ],
            row_data=[
                (country.replace('_', ' '), death, case)
                for country, death, case in zip(countries_list,  countries_deaths, countries_cases)
            ],
        )
        data_tables.bind(on_row_press=self.on_row_press)
        data_tables.bind(on_check_press=self.on_check_press)
        table_container.add_widget(data_tables)
        
    """ def on_start(self):
        self.data_tables.open() """
    def table_reset(self):
        table_container = self.ids.covids
        table_container.clear_widgets()
    
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)



class CovidEngApp(MDApp):
    
    def build(self):
        return BoxContainer()


CovidEngApp().run()
