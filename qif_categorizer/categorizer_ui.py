import os

os.environ['KIVY_NO_ARGS'] = 'T'

from kivymd.app import MDApp  # noqa: E402
from kivymd.uix.screen import Screen  # noqa: E402
from kivymd.uix.datatables import MDDataTable  # noqa: E402

from kivy.metrics import dp  # noqa: E402
from kivy.properties import ListProperty  # noqa: E402


class CategorizerUIApp(MDApp):
    transaction_list = ListProperty(None)

    def build(self):
        screen = Screen()
        txns = self.transaction_list  # noqa: F841

        # self.cols = 3

        table = MDDataTable(
            column_data=[
                ('Date', dp(30)),
                ('Payee', dp(60)),
                ('Amount', dp(30)),
            ]
        )

        screen.add_widget(table)
        return screen


if __name__ == '__main__':
    CategorizerUIApp().run()
