import requests, bs4, re

import os, wx

import scarjo_bg_changer

app = wx.App(False)
frame = wx.Frame(None, -1, 'Simple Gui')
frame.Show()
frame.Bind(wx.EVT_LEFT_DCLICK, lambda e: scarjo_bg_changer.main(engine='bing'))
wx.StaticText(frame, label="Double click me to change background")
app.MainLoop()

# import ipdb
# ipdb.set_trace()

