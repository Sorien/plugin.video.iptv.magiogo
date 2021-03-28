import os
import xbmcvfs

from datetime import datetime, timedelta
from iptv.iptvsimple import configure_iptvsimple
from magio.addon import MagioGoAddon
from iptv.service import IPTVUpdateService


class MagioGoService(IPTVUpdateService):

    def create_addon(self):
        return MagioGoAddon()

    def fetch_channels(self, progress):
        return self.addon.client.channels(progress)

    def fetch_epg(self, channels, progress):
        days = int(self.addon.getSetting('epg_days'))
        now = datetime.now()
        return self.addon.client.epg([c.id for c in channels], now - timedelta(days=days), now + timedelta(days=days), progress)

    def playlist_path(self):
        if self.addon.getSetting('playlist_folder'):
            return os.path.join(xbmcvfs.translatePath(self.addon.getSetting('playlist_folder')), self.addon.getSetting('playlist_file'))

    def epg_path(self):
        if self.addon.getSetting('epg_generate') == 'true' and self.addon.getSetting('epg_folder'):
            return os.path.join(xbmcvfs.translatePath(self.addon.getSetting('epg_folder')), self.addon.getSetting('epg_file'))

    def updated_after_settings_changed(self):
        configure_iptvsimple(self.playlist_path(), self.epg_path(), self.addon.getAddonInfo('name'))
