from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList


class MainScreen(Screen):
    pass


class TabsContainer(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    tab_active_id = ''
    dialog = None
    tabs_list = []
    mdlists_dict = {}
    selected_notes = []
    
    def popup_new_tab(self, text):
        self.dialog = MDDialog(title='Add new Tab',
                                content_cls=DialogTabsContainer(),
                                type='custom',
                                size_hint=(.8, None),
                                buttons=[MDFlatButton(text='ADD', on_release=Tabs.add_tab),
                                        MDFlatButton(text='CANCEL', on_release=self.close)]
                                )
        self.dialog.set_normal_height()

        self.dialog.open()
    
    def close(self, instance):
        self.dialog.dismiss()
    
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.tab_active_id = tab_text
        for child in self.mdlists_dict[self.tab_active_id].children:
            print(child)

    def callback_tab(self, instance):
        if instance.icon == 'android':
            self.popup_new_tab('')
        elif instance.icon == 'plus':
            self.popup_new_note('')
        elif instance.icon ==  'minus':
            self.delete_selected_notes(self.selected_notes)

    """ def add_tab(self,instance):
        for obj in self.dialog.content_cls.children:
            self.tab = Tabs(obj.text) 
            self.ids.tabs.add_widget(self.tab)
        self.dialog.dismiss()
        sv = ScrollView()
        self.tab.add_widget(sv)
        self.tabs_list.append(obj.text)
        tab_name = MDList()
        sv.add_widget(tab_name)
        print(obj.text)
        print(tab_name) """
    """self.mdlists_dict[obj.text] = tab_name
        print(self.mdlists_dict) """

        # add list name to list which we be referencing to add list_item
        

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_checkbox_active(checkbox, value):
    # Adding/removing selected/unselected Objects to/from list for further process
        if value:
            MainScreen.selected_notes.append(checkbox)
            print(checkbox, 'added to list')
        else:
            MainScreen.selected_notes.remove(checkbox)
            print(checkbox, 'removed from list')

    def on_touch_item(instance, text):
        # called from .kv on touch list item - Making item editable
        
        MainScreen.popup_new_note(instance,text)


class Tabs(FloatLayout, MDTabsBase):
    # content for tabs
    
    def __init__(self, tab_name):
        super().__init__()
        self.name = tab_name
    

    def add_tab(self):
        for obj in self.dialog.content_cls.children:
            self.tab = Tabs(obj.text) 
            self.ids.tabs.add_widget(self.tab)
        self.dialog.dismiss()
        sv = ScrollView()
        self.tab.add_widget(sv)
        self.tabs_list.append(obj.text)
        tab_name = MDList()
        sv.add_widget(tab_name)
        print(obj.text)
        print(tab_name)

        self.mdlists_dict[obj.text] = tab_name
        print(self.mdlists_dict)
    """ def add_tab(self):
        md_tabs = MDTabs()
        md_tabs.add_widget(self(text=self.name))
        sv = ScrollView()
        self.add_widget(sv)
        tab_name = MDList()
        sv.add_widget(tab_name) """
         


class DialogTabsContainer(BoxLayout):
    pass


class RightCheckBox(IRightBodyTouch, MDCheckbox):
    # Custom right container.
    pass

class OrganizerApp(MDApp):
    

    
    def build(self):
        return MainScreen()


OrganizerApp().run()