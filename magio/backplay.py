# -*- coding: utf-8 -*-

import requests
import json
import xbmc
import xbmcgui
import datetime
import time
import random
import urllib.request, urllib.parse, urllib.error

#fix for datatetime.strptime returns None
class proxydt(datetime.datetime):
    @staticmethod
    def strptime(date_string, format):
        import time
        return datetime.datetime(*(time.strptime(date_string, format)[0:6]))

#Check first method stream and go to two method stream url
datetime.datetime = proxydt
channel = xbmc.getInfoLabel('ListItem.ChannelName').replace("HD", "").replace("FHD", "").replace("hd", "").replace(" ", "").replace("*", "").replace("Č", "C").replace("Ť", "T").replace("í", "i").replace(".", "").lower()
data = requests.get("https://1url.cz/Yz9TQ").json()
try:
    print((data[channel]))
except KeyError:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(xbmc.getInfoLabel('ListItem.ChannelName').replace("*", ""), "Stanica momentálne nepodporuje archív.")
    exit()

if data[channel]['check'] == channel:
    epgdatetime = datetime.datetime.strptime(xbmc.getInfoLabel('ListItem.Date'), "%d.%m.%Y %H:%M") + (datetime.timedelta(hours=-1))
    stream = data['server']['1'] + data[channel]['server'] + data[channel]['quality'] + data[channel]['catalog'] + epgdatetime.strftime("%Y%m%d") + "_" + data[channel]['channel'] + "_" + epgdatetime.strftime("%Y%m%d_%H%M%S") + data[channel]['url']
    try:
        code = urllib.request.urlopen(stream).getcode()
    except urllib.error.HTTPError as e:
        code = e.code
    if str(code).startswith('2') or str(code).startswith('3') :
        stream_url = stream
    else:
        epg_end = datetime.datetime.strptime(xbmc.getInfoLabel('ListItem.EndTime'), "%H:%M") + (datetime.timedelta(minutes=-2))
        epg_date = datetime.datetime.strptime(xbmc.getInfoLabel('ListItem.Date'), "%d.%m.%Y %H:%M")
        data_new = requests.get("https://1url.cz/Qz9Ti").json()
        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        headers_token = {'Origin': 'https://www.magiogo.sk', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.sk/', 'User-Agent': UA, 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site'}
        acestoken = requests.post("https://skgo.magio.tv/v2/auth/init?dsid=Netscape." + str(int(time.time())) + "." + str(random.random()) + "&deviceName=Web%20Browser&deviceType=OTT_WIN&osVersion=0.0.0&appVersion=0.0.0&language=SK", headers = headers_token).json()
        headers_url = {'Authorization': 'Bearer' + acestoken['token']['accessToken'], 'Origin': 'https://tvgo.t-mobile.cz', 'Pragma': 'no-cache', 'Referer': 'https://tvgo.t-mobile.cz/', 'User-Agent': UA, 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site'}
        epg_url = requests.get("https://skgo.magio.tv/v2/television/epg?filter=channel.id=in=(" + data_new[channel]['id'] + ");startTime=ge=" + epg_date.strftime("%Y-%m-%d") + "T" + epg_date.strftime("%H:%M:%S") + ".000;startTime=le=" + epg_date.strftime("%Y-%m-%d") + "T" + epg_end.strftime("%H:%M:%S") + ".000;&lang=SK", headers = headers_url).json()
        stream_url = (data_new[channel]['server'] + data_new[channel]['quality'] + data_new[channel]['catalog'] + data_new[channel]['channel'] + data_new[channel]['url'] + '?starttime=%s&stoptime=%s') % (epg_url['items'][0]['programs'][0]['startTimeUTC'], epg_url['items'][0]['programs'][0]['endTimeUTC'])
else:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('Kodi', "Chyba overenia na strane serveru. Kontaktujte prosím autora doplnku.")
    exit()

#Player Stream
namechannel = xbmc.getInfoLabel('ListItem.ChannelName').replace("*", "")
info = {
        'Title': namechannel + ": " + xbmc.getInfoLabel('Listitem.Title') + " (Archív)",
        'year': xbmc.getInfoLabel('ListItem.Year'),
        'genre': xbmc.getInfoLabel('ListItem.Genre'),
        'plot': xbmc.getInfoLabel('ListItem.Plot'),
        'media-type': 'tvshow',
    }
picture = {
    'thumb': xbmc.getInfoLabel('Listitem.Icon'),
    'icon': xbmc.getInfoLabel('Listitem.Icon'),
}
item = xbmcgui.ListItem()
item.setInfo('video', info)
item.setArt(picture)
xbmc.Player().play(stream_url, item)
