from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineIconListItem,OneLineAvatarListItem, OneLineAvatarIconListItem, OneLineRightIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, IconRightWidget
from kivymd.uix.behaviors import TouchBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import json
import requests
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.navigationdrawer import NavigationLayout
from kivy.properties import StringProperty, ObjectProperty
import pandas as pd
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from requests.exceptions import ConnectionError


def validate_input(string):
    text_after = string.strip()
    return text_after


class Tabs(FloatLayout, MDTabsBase):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

class DialogTabsContainer(BoxLayout):
    pass

class TabsContainer(MDTabs):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CheckboxLeftWidget(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class ListItemWithCheckbox(OneLineRightIconListItem, TouchBehavior):
    
    dialog = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_checkbox_active(checkbox, value):
        if value:
            MainScreen.selected_notes.append(checkbox)
            print(value)
        else:
            MainScreen.selected_notes.remove(checkbox)
        
    def on_triple_tap(self, touch, *args):
        if not self.dialog:
            self.dialog = MDDialog(title='edit note',
                            type='custom',
                            size_hint=(.9, None),
                            content_cls=DialogTabsContainer(),
                            buttons=[MDFlatButton(text='ADD', on_release=self.update_note),
                            MDFlatButton(text='CANCEL', on_release=self.close)]
                            )
        self.dialog.set_normal_height()
        for obj in self.dialog.content_cls.children:
            obj.text = self.text
            self.selected_item_text = obj.text
            print('ok')
        self.dialog.open()


    def close(self, instance):
        print('close')
        self.dialog.dismiss()

    def update_note(self, _instance):
        for obj in self.dialog.content_cls.children:
            print(obj)
            if validate_input(obj.text):
                new_text = validate_input(obj.text)
                self.text = new_text
                print(MainScreen.items_dict)
                for tab, parent in MainScreen.mdlists_dict.items():
                    for child in parent.children:
                        if child == self:
                            print(tab, parent, child)
                            MainScreen.items_dict[tab].pop(self.selected_item_text)
                            MainScreen.items_dict[tab][new_text] = True
                            MainScreen.items_dict[tab]['_init'] = True

                
                            print(self.selected_item_text)
                            print(MainScreen.items_dict)
                            data = json.dumps({tab:MainScreen.items_dict[tab]})
                            print(data)
                            item_to_database = json.loads(data)
                            print(item_to_database)
                            
                            requests.patch(url=MyApp.url, json=item_to_database)
            else:
                Snackbar(text="Note CAN NOT be empty").show()
                


        self.dialog.dismiss()


class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):"""
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
    """
pass
class NavigationDrawerIconButton(OneLineAvatarIconListItem):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()     

class AppContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
   

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    tabs = ObjectProperty(None)
    tab_active_id = ''
    dialog = None
    tabs_list = {}
    instance_tab_obj = None
    mdlists_dict = {}
    selected_notes = []
    items_dict = dict({})
    print(items_dict,'________________________________')
   


    def popup_new_tab(self):
        self.dialog = MDDialog(title='Add new Tab',
                                content_cls=DialogTabsContainer(),
                                type='custom',
                                size_hint=(.8, None),
                                buttons=[MDFlatButton(text='ADD', on_release=self.add_tab),
                                        MDFlatButton(text='CANCEL', on_release=self.close)]
                                )
        self.dialog.set_normal_height()
        self.dialog.open()
    
    def close(self, instance):
        self.dialog.dismiss()
    
    def callback_tab(self, instance):
        if instance.icon == 'tab-plus':
            self.popup_new_tab()
        elif instance.icon == 'tab-minus':
            self.remove_tab_popup()
        elif instance.icon == 'plus':
            self.popup_new_note()
        elif instance.icon ==  'minus':
            self.delete_selected_notes(self.selected_notes)
           
    def add_tab(self,instance):
        for key,value in self.ids:
            print(key,value)
        for obj in self.dialog.content_cls.children:
            if validate_input(obj.text):
                new_text = validate_input(obj.text)
                if new_text not in MainScreen.tabs_list:
                    self.tab = Tabs(text=new_text)
                    
                    self.tabs.add_widget(self.tab)

                    self.dialog.dismiss()
                    a = {new_text:{'_init':True}}
                    data = json.dumps(a)
                    tab_name_to_database = json.loads(data)
                    print(tab_name_to_database)
                    requests.patch(url=MyApp.url, json=tab_name_to_database)
                    sv = ScrollView()
                    self.tab.add_widget(sv)
                    self.tabs_list[new_text] = self.tab
                    self.items_dict[new_text] = {'_init':True}
                    tab_name = MDList()
                    sv.add_widget(tab_name)
                    print(tab_name)
                    # add list name to list which we be referencing to add list_item
                    self.mdlists_dict[new_text] = tab_name
                    self.tab_active_id = new_text
                else:
                    Snackbar(text="You already have that tab").show()
                    print('Already in')
                    self.dialog.dismiss()
            else:
                Snackbar(text="List name CAN NOT be empty").show()
        
    def popup_new_note(self):
        
        self.dialog = MDDialog(title=f'Add new note to {self.tab_active_id}',
                            type='custom',
                            size_hint=(.9, None),
                            content_cls=DialogTabsContainer(),
                            buttons=[MDFlatButton(text='ADD', on_release=self.add_note),
                            MDFlatButton(text='CANCEL', on_release=self.close)]
                            )
        self.dialog.set_normal_height()
        self.dialog.open()
        
    def add_note(self,instance):
       
        for obj in self.dialog.content_cls.children:
            if validate_input(obj.text):
                new_text = validate_input(obj.text)
                self.item = ListItemWithCheckbox(text=new_text)
                self.mdlists_dict[self.tab_active_id].add_widget(self.item)
            else:
                Snackbar(text="Note CAN NOT be empty").show()

        self.dialog.dismiss()
                     
        self.items_dict[self.tab_active_id][new_text] = True
        self.items_dict[self.tab_active_id]['_init'] = True
        data = json.dumps({self.tab_active_id:self.items_dict[self.tab_active_id]})
        item_to_database = json.loads(data)

        requests.patch(url=MyApp.url, json=item_to_database)

            
    def delete_selected_notes(self, selected_notes):
        for item in selected_notes:
            for key, value in self.mdlists_dict.items():
                for child in value.children:
                    if item == child:
                        print('delte item: ',item)
                        value.remove_widget(child)
                        requests.delete(url=MyApp.url[:-5]+key+'/'+item.text+'.json')
                        
                        self.items_dict[key].pop(item.text)
                self.remove_widget(item)
    def remove_tab_popup(self):
        self.dialog = MDDialog(title=f'Do You want to DELETE {self.tab_active_id}?',
                            type='custom',
                            size_hint=(.9, None),
                            buttons=[MDFlatButton(text='YES, DELETE IT', on_release=self.remove_tab),
                            MDFlatButton(text='NO, KEEP IT', on_release=self.close)]
                            )
        self.dialog.set_normal_height()
        self.dialog.open()
       
    def remove_tab(self, _instance):
        
        if MainScreen.tab_active_id != '@General' and MainScreen.tab_active_id in MainScreen.items_dict:
            tab = MainScreen.tabs_list[MainScreen.tab_active_id]
            del self.items_dict[MainScreen.tab_active_id]
            del self.mdlists_dict[MainScreen.tab_active_id]
            del self.tabs_list[MainScreen.tab_active_id]
            self.tabs.remove_widget(tab)
            requests.delete(url=MyApp.url[:-5]+MainScreen.tab_active_id+".json")
            self.tab_active_id = "@General"
        elif self.tab_active_id not in self.items_dict:
            Snackbar(text=f"There's no {self.tab_active_id} anymore").show()
        elif self.tab_active_id == '@General':
            Snackbar(text=f"You have no rights to delete {self.tab_active_id}").show()
        self.dialog.dismiss()
class MDJokeCard(MDCard):
    pass

class CaroseneScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    oil = ObjectProperty(None)
    joke_box = ObjectProperty(None)
    scroll_box = ObjectProperty(None)
    
    
    def on_enter(self):
        try:
            r = requests.post('https://jonesoil.ie/api/get_banded_oil_prices/product/1/quantity/1000',\
                            headers={"User-Agent":"Mozilla/5.0"})
            oil_p = json.loads(r.text)
            oil_price = oil_p['real_price']
            self.oil.text = f"Cheapest Carosene: Jones Oil: {oil_price}/1000L"
            # getting random joke
            for i in range(0,4):
                r = requests.get(url="https://icanhazdadjoke.com", headers={"Accept": "text/plain"})
                cardd = MDJokeCard()
                self.scroll_box.add_widget(cardd)

                joke_label = MDLabel(text=r.text,
                                    theme_text_color="Primary",
                                    size_hint=(1,None),
                                    text_size=self.size, 
                                    halign="center",
                                    valign="middle")
                                   
                                        
                print('ok')
                cardd.add_widget(joke_label)
        except ConnectionError as e:    # This is the correct syntax
            Snackbar(text='Check Your Internet').show()
            

class ContactUs(MDScreen):
    pass

class CovidsContainer(BoxLayout):


    def tables(self):
        try:
            list_covid = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv')
            countries_grouped = list_covid.groupby('countriesAndTerritories')[['deaths','cases']]\
                                .sum().sort_values('deaths', ascending=False).head(30)
            countries_list = countries_grouped.index.to_list()
            countries_deaths = countries_grouped.deaths.to_list()
            countries_cases = countries_grouped.cases.to_list()
            data_tables = MDDataTable(
                size_hint=(1, 1),
                #use_pagination=True,
                check=True,
                rows_num = 30,
                sort = True,
                column_data=[
                    ("Country", dp(38)),
                    ("Deaths", dp(12)),
                    ("Cases", dp(15)),
                    ],
                row_data=[
                    (country.replace('_', ' '), death, case)
                    for country, death, case in zip(countries_list,  countries_deaths, countries_cases)
                ],
            )
            data_tables.bind(on_row_press=self.on_row_press)
            data_tables.bind(on_check_press=self.on_check_press)
            self.add_widget(data_tables)
        except:
            Snackbar(text="Check Your Internet").show()
    """ def on_start(self):
        self.data_tables.open() """
    def table_reset(self):
        self.clear_widgets()
    
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)
class CovidScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
class JokeScreen(Screen):
    pass      
    

class MyApp(MDApp):

    database = None

    items_dict_list = {}
    url = 'https://taskator12.firebaseio.com/.json'
    try:
        request = requests.get(url=url)
        database = request.json()
    except:
        print('no connection')
    def build(self):
    
        self.theme_cls.primary_palette = "BlueGray"

        
    
    def on_start(self):
        if self.database:
            for name_tab, item_name in self.database.items():
                #self.items_dict_list[name_tab] = {}
                self.items_dict_list = {}
                tab = Tabs(text=name_tab)
                tabbb = TabsContainer()
                self.root.ids.tabs.add_widget(tab)
                sv = ScrollView()
                tab.add_widget(sv)
                MainScreen.tabs_list[name_tab] = tab
                tab_name = MDList()
                sv.add_widget(tab_name)
                MainScreen.mdlists_dict[name_tab] = tab_name
                
                if len(item_name.keys()) > 1:
                    for items in item_name.keys():
                        if items != '_init':
                            self.items_dict_list[items] = True
                            print(items)
                            item = ListItemWithCheckbox(text=items)
                            MainScreen.mdlists_dict[name_tab].add_widget(item)
                MainScreen.items_dict[name_tab] = self.items_dict_list
                print(MainScreen.items_dict)
        else:
            MainScreen.items_dict = {}
            Snackbar(text="You have NO internet").show()

        MainScreen.tab_active_id = '@General'
        

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        MainScreen.tab_active_id = tab_text
        MainScreen.instance_tab_obj = instance_tab
        print(MainScreen.tab_active_id)


MyApp().run()
