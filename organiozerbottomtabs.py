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
from kivymd.uix.bottomnavigation import MDBottomNavigationItem




    
   
class DialogTabsContainer(BoxLayout):
    


    def remove(self):
        print(OrganizerBottomTabsApp.tab_active_id, '_____________')
        tab = MainScreen.tabs_list[OrganizerBottomTabsApp.tab_active_id]
        print(tab)
        print(OrganizerBottomTabsApp.tab_active_id, '+++++++++++++++++++')
        MainScreen.items_dict.pop(OrganizerBottomTabsApp.tab_active_id)
        print(OrganizerBottomTabsApp.tab_active_id)
        del MainScreen.mdlists_dict[OrganizerBottomTabsApp.tab_active_id]
        print(OrganizerBottomTabsApp.tab_active_id)
        carous = self.children[1].children[0]
        print(carous.slides)
        
       
        self.remove_widget(tab)

        #self.clear_widgets()

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
        
    def on_long_touch(self, touch, *args):
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
        self.dialog.open()


    def close(self, instance):
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
                        
                        requests.patch(url=OrganizerBottomTabsApp.url, json=item_to_database)
                        #requests.delete(url=NewApp.url[:-5]+tab+'/'+self.selected_item_text+'.json')



        self.dialog.dismiss()

    
    
class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class NavigationDrawerIconButton(OneLineAvatarIconListItem):
    pass

            
class RightCheckBox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''

class AppContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
   

class BottomNavigationItem(MDBottomNavigationItem):
    
    def on_tab_release(self,*args):
        MainScreen.active_tab = self
        print(self)
        
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    active_tab = ''
        
    dialog = None
    tabs_list = {}
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
            self.tab = MDBottomNavigationItem(name=obj.text,text=obj.text)
            
            self.ids.panel.add_widget(self.tab)

        self.dialog.dismiss()
        a = {obj.text:{'_init':True}}
        data = json.dumps(a)
        tab_name_to_database = json.loads(data)
        print(tab_name_to_database)
        requests.patch(url=OrganizerBottomTabsApp.url, json=tab_name_to_database)
        sv = ScrollView()
        self.tab.add_widget(sv)
        self.tabs_list[obj.text] = self.tab
        self.items_dict[obj.text] = {'_init':True}
        tab_name = MDList()
        sv.add_widget(tab_name)
        print(tab_name)
        # add list name to list which we be referencing to add list_item
        self.mdlists_dict[obj.text] = tab_name
        OrganizerBottomTabsApp.tab_active_id = obj.text
        
    def popup_new_note(self):
        self.dialog = MDDialog(title='Add new note',
                                type='custom',
                                size_hint=(.9, None),
                                content_cls=DialogTabsContainer(),
                                buttons=[MDFlatButton(text='ADD', on_release=self.add_note),
                                MDFlatButton(text='CANCEL', on_release=self.close)]
                                )
        self.dialog.set_normal_height()
        self.dialog.open()
        
    def add_note(self,instance):
        print('_____________________',self.items_dict, '-------------------------')
       
        for obj in self.dialog.content_cls.children:
            self.item = ListItemWithCheckbox(text=obj.text)
            print(OrganizerBottomTabsApp.tab_active_id)
            self.mdlists_dict[OrganizerBottomTabsApp.tab_active_id].add_widget(self.item)
        self.dialog.dismiss()
                     
        self.items_dict[OrganizerBottomTabsApp.tab_active_id][obj.text] = True
        self.items_dict[OrganizerBottomTabsApp.tab_active_id]['_init'] = True
        data = json.dumps({OrganizerBottomTabsApp.tab_active_id:self.items_dict[OrganizerBottomTabsApp.tab_active_id]})
        item_to_database = json.loads(data)

        requests.patch(url=OrganizerBottomTabsApp.url, json=item_to_database)

            
    def delete_selected_notes(self, selected_notes):
        for item in selected_notes:
            for key, value in self.mdlists_dict.items():
                for child in value.children:
                    if item == child:
                        print('delte item: ',item)
                        value.remove_widget(child)
                        requests.delete(url=OrganizerBottomTabsApp.url[:-5]+key+'/'+item.text+'.json')
                        
                        self.items_dict[key].pop(item.text)
                self.remove_widget(item)
   
   

class OrganizerBottomTabsApp(MDApp):

    tab_active_id = ''
    items_dict_list = {}
    url = 'https://taskator12.firebaseio.com/.json'
    request = requests.get(url=url)
    database = request.json() 
   
    def build(self):
    
        self.theme_cls.primary_palette = "BlueGray"
        
    
        return MainScreen()

    def on_start(self):
        if self.database:
            for name_tab, item_name in self.database.items():
                #self.items_dict_list[name_tab] = {}
                self.items_dict_list = {}
                tab = BottomNavigationItem(name=name_tab, text=name_tab)
                self.root.ids.panel.add_widget(tab)
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
                self.tab_active_id = name_tab
        else:
            MainScreen.items_dict = {} 

        

    
        

    def remove_tab(self):

        print(MainScreen.mdlists_dict)
        print(MainScreen.items_dict)
        print(MainScreen.tabs_list)
        tab_id = MainScreen.active_tab
        print(tab_id)

        for key, tab in MainScreen.tabs_list.items():
            if key == tab_id.name:
                print(key, ' deleted')
                self.root.ids.panel.remove_widget(tab)
                break 

OrganizerBottomTabsApp().run()
