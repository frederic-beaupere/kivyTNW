from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest

Builder.load_string('''
<staButton@Button>:
    text_size: self.width, None
    halign: 'center'
    size_hint_x: 0.2
    background_color: (0.4, 0.4, 0.4, 1.0)
<queryTNW>:
    Button:
        text: "Settings"
        on_press: root.manager.current = "Settings"
        background_color: (0.4, 0.4, 0.4, 1.0)
        size_hint_x: 0.25
        size_hint_y: 0.4
    Label:
        text: "kivy Transport CH"
        text_size: self.width, None
        halign: 'center'
        color: .8,.9,0,1
        size_hint_y: 0.4
    staButton:
        text: "update Schuetzenhaus"
        on_release: root.lookup("Basel, Schuetzenhaus")
    Label:
        text: root.foundA
        text_size: self.width, None
        padding_x: 10
    staButton:
        text: "update Erasmusplatz"
        on_release: root.lookup("Erasmusplatz")
    Label:
        text: root.foundB
        text_size: self.width, None
        padding_x: 10
    staButton:
        text: "update Johanniterbruecke"
        on_release: root.lookup("Johanniterbruecke")
    Label:
        text: root.foundC
        text_size: self.width, None
        padding_x: 10
    staButton:
        text: "update Freilager"
        on_release: root.lookup("Freilager")
    Label:
        text: root.foundD
        text_size: self.width, None
        padding_x: 10
<SettingsScreen>:
    Label:
        text: "Set-Up your stations"
    staButton:
        text: "Back"
        on_release: root.manager.current = "queryTNW"
''')

stA = "Basel, Schuetzenhaus"
stB = "Erasmusplatz"
stC = "Johanniterbruecke"
stD = "Freilager"
limit = "&limit=6"
urlStation = "http://transport.opendata.ch/v1/stationboard?station="


class queryTNW(GridLayout, Screen):
    foundA = StringProperty("")
    foundB = StringProperty("")
    foundC = StringProperty("")
    foundD = StringProperty("")

    def __init__(self, **kwargs):
        super(queryTNW, self).__init__(**kwargs)
        self.cols = 2
        self.foundA = ""
        self.foundB = ""
        self.foundC = ""
        self.foundD = ""

    def req(*args):
        r = UrlRequest(urlStation + args[1] + limit)
        r.wait()
        jData = r.result
        stb = jData.get("stationboard")
        accuStr = []
        for i in range(len(stb)):
            tName = stb[i].get("name")
            tDest = stb[i].get("to")
            tDepTime = stb[i].get("stop").get("departure")
            displayStr = tName + ", "
            displayStr += tDepTime[11:16] + ", "
            displayStr += tDest
            if i < 7:
                accuStr += "\n" + displayStr
        return accuStr

    def lookup(self, *args):
        print(args)
        if args[0] == stA:
            self.foundA = ""
            for line in self.req(args[0]):
                self.foundA += line
        elif args[0] == stB:
            self.foundB = ""
            for line in self.req(args[0]):
                self.foundB += line
        elif args[0] == stC:
            self.foundC = ""
            for line in self.req(args[0]):
                self.foundC += line
        elif args[0] == stD:
            self.foundD = ""
            for line in self.req(args[0]):
                self.foundD += line


class SettingsScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(queryTNW(name="queryTNW"))
sm.add_widget(SettingsScreen(name="Settings"))

class kivyTNW(App):

    def build(self):
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    kivyTNW().run()