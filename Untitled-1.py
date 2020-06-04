
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.app import Builder
from kivymd.app import MDApp

kv = '''

<CustomToolbar>:
    size_hint_y: None
    padding: dp(20), 0
    height: root.theme_cls.standard_increment
    padding: [root.theme_cls.horizontal_margins - dp(12), 0]
    opposite_colors: True
    md_bg_color: self.theme_cls.primary_color
    MDLabel:
        text: " My App"
        id: label_title
        font_style: 'H6'
        opposite_colors: root.opposite_colors
        theme_text_color: 'Custom'
        text_color: root.specific_text_color
        shorten: True
        shorten_from: 'right'
        padding: dp(8), 0

<Tab>:
    orientation: "vertical"
    cols: 1
    id: tabtabku
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        scroll_y: 0
        MDLabel:
            id: console
            height: self.texture_size[1]
            size_hint_y: None
            markup: True
    BoxLayout:
        height: "35dp"
        orientation: 'horizontal'
        size_hint: (1, None)
        pos_hint: {"center_x": .5}
        MDIconButton:
            icon: "close-box-outline"
            size_hint: None, None
            pos_hint: {"center_y": .5}
            on_release:
                app.remove(root)
        MDTextFieldRect:
            id: textsend
            multiline: False
            pos_hint: {"top": 1}
            hint_text: "Say something!"
            max_text_length: 245
            padding: [5, (self.height-self.line_height)/2]
            height: "35dp"
        MDRaisedButton:
            text: "Send"
            id: tombolsendtext
            on_release: app.remove(root)

<TabHome>:
    orientation: "vertical"
    MDTextField:
        id: room
    MDRaisedButton:
        text: "add"
        on_press:
            app.add(room.text)
    MDRaisedButton:
        text: "print"
        on_press:
            app.printku()
    MDLabel:

BoxLayout: 
    tabku: tabku.__self__
    orientation: "vertical"
    CustomToolbar:
        id: tulbar
    MDTabs:
        allow_stretch: False
        id: tabku
        TabHome:
            id: tabhome
            text: "Home"

'''
class Tab(BoxLayout, MDTabsBase):
    pass
class TabHome(BoxLayout, MDTabsBase):
    pass
class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout):
    pass
class MainApp(MDApp):
    mytab = ObjectProperty()
    mytab = []
    dialog = None
    tabroom = {}

    def build(self):
        return Builder.load_string(kv)

    def add(self, name):
        tab = Tab(text=name)
        if len(self.tabroom) == 0:
            print("nol",self.tabroom)
            self.tabroom[name] = 0
        else:
            print("ada",len(self.tabroom))
            self.tabroom[name] = len(self.tabroom)
        self.root.ids.tabku.add_widget(tab)
        self.mytab.append(tab)

    def remove(self, widget):
        self.root.ids.tabku.remove_widget(widget)
        self.mytab.remove(widget)

    def set(self, nametab):
        
        index = None
        for x in range(len(self.mytab)):
            if self.mytab[x].text == nametab:
                index = x
                break

    def printku(self):
        panel = self.root.ids.tabku
        #print(panel.tab_list)
        print(self.root.tabku)
        carousel = self.root.tabku.children[1].children[0]
        print(carousel.slides)
        # q = self.root.ids.tabku.ids.scrollview.children[0].children
        # print(self.tabroom["a"])
        # if "b" not in self.tabroom:
        #     print("tidak ada")

MainApp().run()