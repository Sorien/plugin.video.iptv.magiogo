# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcaddon
from iptv.lang import _

IPTV_SIMPLE_ID = 'pvr.iptvsimple'


def configure_iptvsimple(m3u_file, xmltv_file, plugin_name):
    try:
        xbmc.executebuiltin('InstallAddon({})'.format(IPTV_SIMPLE_ID), True)
        xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IPTV_SIMPLE_ID))
        addon = xbmcaddon.Addon(IPTV_SIMPLE_ID)
    except:
        xbmcgui.Dialog().ok(plugin_name, _('iptv_simple_not_installed'))
        return

    if not ((m3u_file and (addon.getSetting('m3uPath') != m3u_file)) or
            (xmltv_file and (addon.getSetting('epgPath') != xmltv_file))):
        return

    if not xbmcgui.Dialog().yesno(plugin_name, _('iptv_simple_configure').format(plugin_name)):
        return

    xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":false}}}}'.format(IPTV_SIMPLE_ID))

    if m3u_file:
        addon.setSetting('m3uPathType', '0')
        addon.setSetting('m3uPath', m3u_file)
        addon.setSetting('startNum', '1')

    if xmltv_file:
        addon.setSetting('epgPath', xmltv_file)
        addon.setSetting('epgPathType', '0')
        addon.setSetting('epgTimeShift', '0')
        addon.setSetting('epgTSOverride', 'false')

    xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IPTV_SIMPLE_ID))
