from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.behaviors import TouchBehavior
from kivymd.theming import ThemableBehavior
import json
import requests
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.navigationdrawer import NavigationLayout

class Tabs(FloatLayout, MDTabsBase):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
   
class DialogTabsContainer(BoxLayout):
    pass

class TabsContainer(MDTabs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


       
    def remove_tab(self):
        
        if MainScreen.tab_active_id != '@General' and MainScreen.tab_active_id in MainScreen.items_dict:
            tab = MainScreen.tabs_list[MainScreen.tab_active_id]
            del MainScreen.items_dict[MainScreen.tab_active_id]
            del MainScreen.mdlists_dict[MainScreen.tab_active_id]
            del MainScreen.tabs_list[MainScreen.tab_active_id]
            self.remove_widget(tab)
            print(MainScreen.tabs_list)
        elif MainScreen.tab_active_id not in MainScreen.items_dict:
            Snackbar(text=f"There's no {MainScreen.tab_active_id} anymore").show()
        elif MainScreen.tab_active_id == '@General':
            Snackbar(text=f"You have no rights to delete {MainScreen.tab_active_id}").show()




class ListItemWithCheckbox(OneLineAvatarIconListItem, TouchBehavior):
    
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
            self.text = obj.text
            print(MainScreen.items_dict)
            for tab, parent in MainScreen.mdlists_dict.items():
                for child in parent.children:
                    if child == self:
                        print(tab, parent, child)
                        MainScreen.items_dict[tab].pop(self.selected_item_text)
                        MainScreen.items_dict[tab][obj.text] = True
                        MainScreen.items_dict[tab]['_init'] = True

            
                        print(self.selected_item_text)
                        print(MainScreen.items_dict)
                        data = json.dumps({tab:MainScreen.items_dict[tab]})
                        print(data)
                        item_to_database = json.loads(data)
                        print(item_to_database)
                        
                        requests.patch(url=NewApp.url, json=item_to_database)
                        #requests.delete(url=NewApp.url[:-5]+tab+'/'+self.selected_item_text+'.json')



        self.dialog.dismiss()


class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    """ def set_color_item(self, instance_item):
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

            
class RightCheckBox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''

class AppContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
   
class NavLayout(NavigationLayout):
    pass

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
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
        if instance.icon == 'android':
            self.popup_new_tab()
        elif instance.icon == 'plus':
            self.popup_new_note()
        elif instance.icon ==  'minus':
            self.delete_selected_notes(self.selected_notes)
           
    def add_tab(self,instance):
        for obj in self.dialog.content_cls.children:
            if obj.text not in MainScreen.tabs_list:
                self.tab = Tabs(text=obj.text)
            
                self.ids.tabs.add_widget(self.tab)

                self.dialog.dismiss()
                a = {obj.text:{'_init':True}}
                data = json.dumps(a)
                tab_name_to_database = json.loads(data)
                print(tab_name_to_database)
                requests.patch(url=NewApp.url, json=tab_name_to_database)
                sv = ScrollView()
                self.tab.add_widget(sv)
                self.tabs_list[obj.text] = self.tab
                self.items_dict[obj.text] = {'_init':True}
                tab_name = MDList()
                sv.add_widget(tab_name)
                print(tab_name)
                # add list name to list which we be referencing to add list_item
                self.mdlists_dict[obj.text] = tab_name
                self.tab_active_id = obj.text
            else:
                Snackbar(text="You already have that tab").show()
                print('Already in')
                self.dialog.dismiss()
        
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
            self.item = ListItemWithCheckbox(text=obj.text)
            self.mdlists_dict[self.tab_active_id].add_widget(self.item)
        self.dialog.dismiss()
                     
        self.items_dict[self.tab_active_id][obj.text] = True
        self.items_dict[self.tab_active_id]['_init'] = True
        data = json.dumps({self.tab_active_id:self.items_dict[self.tab_active_id]})
        item_to_database = json.loads(data)

        requests.patch(url=NewApp.url, json=item_to_database)

            
    def delete_selected_notes(self, selected_notes):
        for item in selected_notes:
            for key, value in self.mdlists_dict.items():
                for child in value.children:
                    if item == child:
                        print('delte item: ',item)
                        value.remove_widget(child)
                        requests.delete(url=NewApp.url[:-5]+key+'/'+item.text+'.json')
                        
                        self.items_dict[key].pop(item.text)
                self.remove_widget(item)
   
   

class DrawerApp(MDApp):

    items_dict_list = {}
    url = 'https://taskator12.firebaseio.com/.json'
    request = requests.get(url=url)
    database = request.json()
   
    def build(self):
    
        self.theme_cls.primary_palette = "BlueGray"

        

    def on_start(self):
        if self.database:
            for name_tab, item_name in self.database.items():
                #self.items_dict_list[name_tab] = {}
                self.items_dict_list = {}
                tab = Tabs(text=name_tab)
                tabbb = TabsContainer()
                tabbb.add_widget(tab)
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
        MainScreen.tab_active_id = '@General'


    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        MainScreen.tab_active_id = tab_text
        MainScreen.instance_tab_obj = instance_tab
        print(MainScreen.tab_active_id)
        print(instance_tab)
        print(instance_tab_label)
        print(instance_tabs)
        print(self)

    

    def on_carousel_index(self, carousel, index):
        print(self, carousel, index)

    
DrawerApp().run()
