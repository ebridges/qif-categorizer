from kivy.app import App
from kivy.lang import Builder
from textwrap import dedent


class MyApp(App):
    def action(self, instance, value):

        word_list = ['hello', 'hi', 'man', 'girl']

        self.root.suggestion_text = ''

        val = value[value.rfind(' ') + 1 :]  # noqa E203

        if not val:
            return
        try:
            word = [word for word in word_list if word.startswith(val)][0][
                len(val) :  # noqa E203
            ]
            if not word:
                return
            self.root.suggestion_text = word
        except IndexError:
            print('Index Error.')

    def build(self):
        text_input = Builder.load_string(
            dedent(
                '''
            TextInput
        '''
            )
        )
        text_input.bind(text=self.action)
        return text_input


if __name__ == '__main__':
    MyApp().run()
