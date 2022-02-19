from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder


from kivy.core.window import Window


Builder.load_file('client.kv')

class ClientUI(Widget):
    def test():
        pass



class Client(App):
    def build(self):
        client = ClientUI()
        Window.size = (800, 400)
        Window.minimum_width, Window.minimum_height = Window.size
        return client

def main():
    Client().run(); 

if __name__ == "__main__":
    main()