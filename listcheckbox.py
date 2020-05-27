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

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''


class Tabs(MDTabsBase, FloatLayout):
    pass


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''

class Containe(BoxLayout):
    pass



class Box(BoxLayout):
    pass


class MainScreen(Screen):

    def add_list_item(self):
        item = ListItemWithCheckbox(text='czop')
        self.ids.ann_marie.add_widget(item)
    
    def callback(self, instance):

        self.dialog = MDDialog(title="new:",
                type="custom",
                content_cls=Box(),
                buttons=[MDFlatButton(text='save', on_release=self.grabText), MDFlatButton(text='cancel', on_release=self.close)]
                )
        self.dialog.set_normal_height()
    
        if instance.icon == 'plus':
            self.dialog.open()
        elif instance.icon == 'minus':
            print('delete sellected')
        elif instance.icon == 'android':
            print('ok')

    def grabText(self, inst):
        for obj in self.dialog.content_cls.children:
            print(obj.text)
            print(inst)
            item = ListItemWithCheckbox(text=obj.text)
            print(tab_active_id)
            # self.ids.tab_active_id.add_widget(item)
        self.dialog.dismiss()
    
    def close(self,inst):
        self.dialog.dismiss()


class MainApp(MDApp):
    def add_list_item(self):
        item = ListItemWithCheckbox(text='czop')
        self.add_widget(item)
        # self.ids.ann_marie.add_widget(item)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        tab_active_id = tab_text
        print(tab_active_id)

    def build(self):
        return MainScreen()


   
MainApp().run()