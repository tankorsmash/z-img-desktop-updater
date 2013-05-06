import requests, bs4, re

import os, wx

import scarjo_bg_changer, temp
def on_iconify(self, e):
    """
    Being minimized, hide self, which removes the program from the
    taskbar.
    """
    self.Hide()

app = wx.App(False)
frame = wx.Frame(None, -1, 'Simple Gui')
frame.Show()
frame.Bind(wx.EVT_LEFT_DCLICK, lambda e: scarjo_bg_changer.main(engine='bing'))
# temp.TaskBarIcon()
temp.ddTaskBarIcon('icon.ico', "tooltip", frame)
frame.Bind(wx.EVT_ICONIZE, lambda e: on_iconify(frame, e))
wx.StaticText(frame, label="Double click me to change background")
app.MainLoop()

# import ipdb
# ipdb.set_trace()

