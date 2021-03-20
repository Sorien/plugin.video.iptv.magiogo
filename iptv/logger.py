try:
    import xbmc
    import xbmcaddon
    _addon_id = xbmcaddon.Addon().getAddonInfo('id')

    def log(msg):
        msg = "[%s] %s" % (_addon_id, msg)
        xbmc.log(msg, level=xbmc.LOGINFO)
except Exception:
    def log(msg):
        print(msg)
