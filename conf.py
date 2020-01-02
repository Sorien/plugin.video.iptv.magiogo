import time

import xbmcaddon
import xbmcgui

dp = xbmcgui.DialogProgress()
dp.create("Copying files..." + xbmcaddon.Addon('plugin.iptv.magiogo').getSetting('username'))

for i in range(1, 100) :
    dp.update(i, "source\\file #%u" % i, "destination\\file #%u" % i)
    if dp.iscanceled():
        break
    time.sleep(1)

