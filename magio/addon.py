import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

from iptv.addon import IPTVAddon
from iptv.client import StreamNotResolvedException, UserNotDefinedException, UserInvalidException, NetConnectionError
from magio.magiogo import MagioGo, MagioGoException, MagioQuality


class MagioGoAddon(IPTVAddon):

    def create_client(self):
        profile = xbmcvfs.translatePath(self.getAddonInfo('profile'))
        return MagioGo(profile, self.getSetting('username'), self.getSetting('password'), MagioQuality.get(int(self.getSetting('quality'))))

    def register_routes(self):
        IPTVAddon.register_routes(self)
        self._router.route('/recordings')(self.recordings_route)
        self._router.route('/recording/play/<recording_id>/')(self.play_recording_route)
        self._router.route('/recording/delete/<recording_id>')(self.delete_recording_route)

    def add_index_directory_items(self):
        IPTVAddon.add_index_directory_items(self)
        xbmcplugin.addDirectoryItem(self._handle, self.url_for(self.recordings_route),
                                    xbmcgui.ListItem(self.getLocalizedString(30000)), True)

    def channels(self):
        return self._call(lambda: self.client.channels())

    def epg(self, channels, from_date, to_date):
        return self._call(lambda: self.client.epg(channels, from_date, to_date))

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
                    device = self.client.devices()[0]
                else:
                    device = self._select_device()

                if device != '':
                    self.client.disconnect_device(device.id)
                    result = fn()
            else:
                xbmcgui.Dialog().ok(self.getAddonInfo('name'), e.text)
        except UserNotDefinedException:
            xbmcgui.Dialog().ok(self.getAddonInfo('name'), self.getLocalizedString(30501))
        except UserInvalidException:
            xbmcgui.Dialog().ok(self.getAddonInfo('name'), self.getLocalizedString(30502))
        except StreamNotResolvedException:
            xbmcgui.Dialog().ok(self.getAddonInfo('name'), self.getLocalizedString(30504))
        except NetConnectionError:
            xbmcgui.Dialog().ok(self.getAddonInfo('name'), self.getLocalizedString(30503))

        return result

    def recordings_route(self):
        xbmcplugin.setPluginCategory(self._handle, self.getLocalizedString(30000))
        for rec in self._call(lambda: self.client.recordings()):
            item = xbmcgui.ListItem(rec.programme.title)
            item.setInfo('video', {
                'title': rec.programme.title,
                'plot': rec.programme.description,
                'duration': rec.programme.duration
            })
            if rec.programme.thumbnail:
                item.setArt({'thumb': rec.programme.thumbnail, 'icon': rec.programme.thumbnail})
            item.setProperty('IsPlayable', 'true')
            item.addContextMenuItems([(self.getLocalizedString(30001),
                                       'RunPlugin(%s)' % self.url_for(self.delete_recording_route, rec.id))])
            xbmcplugin.addDirectoryItem(self._handle, self.url_for(self.play_recording_route, rec.id), item, False)
        xbmcplugin.endOfDirectory(self._handle)

    def delete_recording_route(self, recording_id):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(self.getAddonInfo('name'), self.getLocalizedString(30002)):
            self._call(lambda: self.client.delete_recording(recording_id))
            xbmc.executebuiltin("Container.Refresh")

    def play_recording_route(self, recording_id):
        self._play(self._call(lambda: self.client.recording_stream_info(recording_id)))
