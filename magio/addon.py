import xbmc
import xbmcgui

from iptv.addon import IPTVAddon
from iptv.client import StreamNotResolvedException, UserNotDefinedException, UserInvalidException
from iptv.logger import log
from magio.magiogo import MagioGo, MagioGoException


class MagioGoAddon(IPTVAddon):

    def create_client(self):
        profile = xbmc.translatePath(self.getAddonInfo('profile'))
        return MagioGo(profile, self.getSetting('username'), self.getSetting('password'))

    def channels(self):
        return self.client.channels()

    def epg(self, channels, from_date, to_date):
        return self.client.epg(channels, from_date, to_date)

    def channel_stream_info(self, channel_id):
        return self._call(lambda: self.client.channel_stream_info(channel_id))

    def programme_stream_info(self, programme_id):
        return self._call(lambda: self.client.programme_stream_info(programme_id))

    def _select_device(self):
        devices = [d for d in self.client.devices() if not d.is_this]
        dialog = xbmcgui.Dialog()
        items = []
        for device in devices:
            items.append(device.name)
        d = dialog.select(self.getLocalizedString(30301), items)
        return devices[d] if d > -1 else ''

    def _call(self, fn):
        result = None
        try:
            result = fn()
        except MagioGoException as e:
            if e.id == 'DEVICE_MAX_LIMIT':
                if self.getSetting('reuse_last_device') == 'true':
                    device = min([d for d in self.client.devices() if not d.is_this])
                else:
                    device = self._select_device()

                if device != '':
                    log('disconnecting device: ' + device.id)
                    self.client.disconnect_device(device.id)
                    result = fn()
            else:
                xbmcgui.Dialog().ok(heading=self.getAddonInfo('name'), line1=e.text)
        except UserNotDefinedException:
            xbmcgui.Dialog().ok(heading=self.getAddonInfo('name'), line1=self.getLocalizedString(30501))
        except UserInvalidException:
            xbmcgui.Dialog().ok(heading=self.getAddonInfo('name'), line1=self.getLocalizedString(30502))
        except StreamNotResolvedException:
            xbmcgui.Dialog().ok(heading=self.getAddonInfo('name'), line1=self.getLocalizedString(30504))

        return result
