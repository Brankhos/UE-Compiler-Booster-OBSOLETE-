import os
import time

import psutil as psutil
import win32api
import win32con
import win32process
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from win32com.client import GetObject, Dispatch

Builder.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/main.kv'))

priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                   win32process.BELOW_NORMAL_PRIORITY_CLASS,
                   win32process.NORMAL_PRIORITY_CLASS,
                   win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                   win32process.HIGH_PRIORITY_CLASS,
                   win32process.REALTIME_PRIORITY_CLASS]
green_to_red=[
    "#dee5e5",
    "#209c05",
    "#85e62c",
    "#ebff0a",
    "#f2ce02",
    "#ff0a0a"
]

class MyGrid(GridLayout):
    priority = ObjectProperty(None)
    compiler_type = ObjectProperty(None)

class MyGrid_E(GridLayout):
    txt = ObjectProperty(None)


class FirstWindow(Screen):


    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)
        #self.currents_scroll.bind(minimum_height=self.currents_scroll.setter('height'))
        self.chck_btn = False
        self.sleep_time = 5
        self.contin = True
        self.started_single = False
        self.shader_num = 1
        self.light_num = 1
        self.slider_shader.bind(value=self.adjust_shader)
        self.slider_light.bind(value=self.adjust_light)
        self.cont_check.bind(active=self.check_change)

        self.mygrid_pro.compiler_type.text = "None"
        self.mygrid_pro.priority.text = "None"
        out_widget = MyGrid_E()
        out_widget.txt.text = "None"
        self.currents_scroll.add_widget(out_widget)

    def reset(self):
        self.slider_light.value = 1
        self.slider_shader.value = 1

    def adjust_shader(self,aaa, value):
        self.shader_num = int(value)
        self.curr_shader.text = self.get_proi_name_for_scroll(value)
        aaa.value_track_color = green_to_red[int(value)]
        if value == 5 or self.light_num == 5:
            self.realtime_warning.text = "Bilgisayarı tamamen dondurabilir!"
        else:
            self.realtime_warning.text = ""

    def adjust_light(self, aaa, value):
        self.light_num = int(value)
        self.curr_light.text = self.get_proi_name_for_scroll(value)
        aaa.value_track_color = green_to_red[int(value)]

        if value == 5 or self.shader_num == 5:
            self.realtime_warning.text = "Bilgisayarı tamamen dondurabilir!"
        else:
            self.realtime_warning.text = ""

    def check_change(self,bx, value):
        if value:
            self.chck_btn = True
            print(self.chck_btn)
            self.sleep_time = 5
        else:
            self.chck_btn = False
            print(self.chck_btn)
            self.sleep_time = 5
        pass

    def stop(self, bx):
        self.cont_check.active = False
        self.single_button.disabled = True
        self.single_button.text = "Procressing"
        self.single_button.bind(on_press=self.start_single)

    def start_single(self,dt):
        self.started_single = True
        if self.chck_btn:
            self.single_button.text = "Stop"
            self.single_button.bind(on_press=self.stop)
        else:
            self.single_button.disabled = True
            self.single_button.text = "Procressing"
        self.start_single_cont("emp")

    def start_single_cont(self, dt):
        if self.contin or self.chck_btn:
            Clock.schedule_once(self.find_process)
            Clock.schedule_once(self.start_single_cont, self.sleep_time)
        else:
            self.contin = True
            self.started_single = False
            self.single_button.disabled = False
            self.single_button.text = "Start"

    @staticmethod
    def get_proi_name_for_scroll(proi_type):
        if 4 == proi_type:
            return "High"
        elif 0 == proi_type:
            return "Idle"
        elif 2 == proi_type:
            return "Normal"
        elif 5 == proi_type:
            return "Realtime"
        elif 3 == proi_type:
            return "Above Normal"
        elif 1 == proi_type:
            return "Below Normal"


    @staticmethod
    def get_proi_name(proi_type):
        if psutil.HIGH_PRIORITY_CLASS == proi_type:
            return "High"
        elif psutil.IDLE_PRIORITY_CLASS == proi_type:
            return "Idle"
        elif psutil.NORMAL_PRIORITY_CLASS == proi_type:
            return "Normal"
        elif psutil.REALTIME_PRIORITY_CLASS == proi_type:
            return "Realtime"
        elif psutil.ABOVE_NORMAL_PRIORITY_CLASS == proi_type:
            return "Above Normal"
        elif psutil.BELOW_NORMAL_PRIORITY_CLASS == proi_type:
            return "Below Normal"

    def find_process(self, dt):
        self.currents_scroll.clear_widgets()
        WMI = GetObject('winmgmts:')
        procs_sh = WMI.ExecQuery('select * from Win32_Process where Name="ShaderCompileWorker.exe"')
        #procs_sh = WMI.ExecQuery('select * from Win32_Process where Name="AnyDesk.exe"')
        if len(procs_sh) == 0:
            out_widget = MyGrid_E()
            out_widget.txt.text = "There is no ShaderComplier"
            self.currents_scroll.add_widget(out_widget)
        else:
            for k,proc in enumerate(procs_sh):
                    out_widget = MyGrid()
                    out_widget.compiler_type.text = f"{k+1}-Shader"
                    proc_i = psutil.Process(proc.ProcessId)
                    out_widget.priority.text = self.get_proi_name(proc_i.nice())
                    self.currents_scroll.add_widget(out_widget)
                    if self.started_single:
                        proc_i.nice(priorityclasses[self.shader_num])
                        out_widget.priority.text = self.get_proi_name(proc_i.nice())

        procs_l = WMI.ExecQuery('select * from Win32_Process where Name="UnrealLightmass.exe"')
        #procs_l = WMI.ExecQuery('select * from Win32_Process where Name="acrotray.exe"')
        if len(procs_l) == 0:
            out_widget = MyGrid_E()
            out_widget.txt.text = "There is no LightComplier"
            self.currents_scroll.add_widget(out_widget)
        else:
            for k,proc in enumerate(procs_l):
                    out_widget = MyGrid()
                    out_widget.compiler_type.text = f"{k+1}-Light"
                    proc_i = psutil.Process(proc.ProcessId)
                    out_widget.priority.text = self.get_proi_name(proc_i.nice())
                    self.currents_scroll.add_widget(out_widget)
                    if self.started_single:
                        proc_i.nice(priorityclasses[self.light_num])
                        out_widget.priority.text = self.get_proi_name(proc_i.nice())
        self.mygrid_pro.compiler_type.text = f"Num of Shader: {len(procs_sh)}"
        self.mygrid_pro.priority.text = f"Num of Light: {len(procs_l)}"

        self.contin = not (len(procs_sh) > 0 or len(procs_l) > 0)




class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'UE Complier Booster'

        self.sm = ScreenManager()
        self.fw = FirstWindow(name='firstwindow')

    def build(self):
        self.sm.add_widget(self.fw)
        return self.sm


if __name__ == "__main__":
    MainApp().run()
