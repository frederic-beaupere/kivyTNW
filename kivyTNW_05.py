from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest

Builder.load_string('''
<queryTNW>:
    Button:
        text: "update Blaesiring"
        on_press: root.lookup("Blaesiring")
    Label:
        text: root.foundA
    Button:
        text: "update Erasmusplatz"
        on_press: root.lookup("Erasmusplatz")
    Label:
        text: root.foundB
    Button:
        text: "update Johanniterbruecke"
        on_press: root.lookup("Johanniterbruecke")
    Label:
        text: root.foundC
    Button:
        text: "update Freilager"
        on_press: root.lookup("Freilager")
    Label:
        text: root.foundD
''')

stA = "Blaesiring"
stB = "Erasmusplatz"
stC = "Johanniterbruecke"
stD = "Freilager"
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
        r = UrlRequest(urlStation + args[1])
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
        if args[0] == "Blaesiring":
            self.foundA = ""
            for line in self.req(stA):
                self.foundA += line
        elif args[0] == "Erasmusplatz":
            self.foundB = ""
            for line in self.req(stB):
                self.foundB += line
        elif args[0] == "Johanniterbruecke":
            self.foundC = ""
            for line in self.req(stC):
                self.foundC += line
        elif args[0] == "Freilager":
            self.foundD = ""
            for line in self.req(stD):
                self.foundD += line


sm = ScreenManager()
sm.add_widget(queryTNW(name="queryTNW"))


class kivyTNW(App):

    def build(self):
        return sm


if __name__ == "__main__":
    kivyTNW().run()