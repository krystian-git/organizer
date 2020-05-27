from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox

Builder.load_string(
    """
<ListItemWithCheckbox@OneLineAvatarIconListItem>:
    MyAvatar:
        source: "data/logo/kivy-icon-128.png"
    MyCheckbox:


<Lists@BoxLayout>
    name: "lists"
    orientation: "vertical"

    MDToolbar:
        title:"List item with Checkbox"
        md_bg_color: app.theme_cls.primary_color
        elevation: 10

    ScrollView:

        MDList:
            id: scroll
"""
)


class MyCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class MyAvatar(ILeftBody, Image):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Kivymd Examples - MDList with Checkboxes"
        self.theme_cls.primary_palette = "Teal"
        super().__init__(**kwargs)

    def build(self):
        list = Factory.Lists()
        for i in range(30):
            list.ids.scroll.add_widget(Factory.ListItemWithCheckbox(text="Item %d" % i))
        self.root = list


if __name__ == "__main__":
    MainApp().run()