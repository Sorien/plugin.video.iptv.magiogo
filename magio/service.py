import os

from datetime import datetime, timedelta
from magio.addon import MagioGoAddon
from iptv.service import IPTVUpdateService


class MagioGoService(IPTVUpdateService):

    def create_addon(self):
        return MagioGoAddon()

    def fetch_channels(self):
        return self.addon.client.channels()

    def fetch_epg(self, channels):
        days = int(self.addon.getSetting('epg_days'))
        now = datetime.now()
        return self.addon.client.epg([c.id for c in channels], now - timedelta(days=days), now + timedelta(days=days))

    def playlist_path(self):
        if self.addon.getSetting('playlist_folder'):
            return os.path.join(self.addon.getSetting('playlist_folder'), self.addon.getSetting('playlist_file'))

    def epg_path(self):
        if self.addon.getSetting('epg_generate') == 'true' and self.addon.getSetting('epg_folder'):
            return os.path.join(self.addon.getSetting('epg_folder'), self.addon.getSetting('epg_file'))
