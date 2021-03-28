# -*- coding: utf-8 -*-

import sys
import time

import xbmcaddon
import xbmcgui
import xbmcplugin
import routing

try:
    from typing import List, Dict
except:
    pass

from datetime import datetime, timedelta
from iptv.lang import _
from iptv.client import StreamInfo, IPTVClient, Channel, Programme, WidevineDRM


class IPTVAddon(xbmcaddon.Addon):
    _handle = int(sys.argv[1]) if len(sys.argv) > 1 else -1

    def __init__(self):
        xbmcaddon.Addon.__init__(self)
        self.client = self.create_client()
        self._router = routing.Plugin()
        self.register_routes()

    def register_routes(self):
        self._router.route("/")(self.index_route)
        self._router.route("/play-channel/<channel_id>")(self.play_channel_route)
        self._router.route("/play-programme/<programme_id>")(self.play_programme_route)
        self._router.route("/play-programme-catchup/<channel_id>-<start>-<end>")(self.play_programme_by_time_route)
        self._router.route('/channels')(self.channels_route)
        self._router.route('/archive')(self.archive_route)
        self._router.route('/archive/<channel_id>-<channel_name>')(self.archive_days_route)
        self._router.route('/archive/<channel_id>-<channel_name>/<day>')(self.archive_programmes_route)

    def create_client(self):
        # type: () -> IPTVClient
        raise NotImplementedError("Should have implemented this")

    def run(self, args):
        self._router.run(args)

    def url_for(self, func, *args, **kwargs):
        return self._router.url_for(func, *args, **kwargs)

    def channels(self):
        # type: () -> List[Channel]
        return self.client.channels()

    def epg(self, channels, from_date, to_date):
        # type: (List[str],datetime,datetime) -> Dict[str, List[Programme]]
        return self.client.epg(channels, from_date, to_date)

    def channel_stream_info(self, channel_id):
        # type: (str) -> StreamInfo
        return self.client.channel_stream_info(channel_id)

    def programme_stream_info(self, programme_id):
        # type: (str) -> StreamInfo
        return self.client.programme_stream_info(programme_id)

    def _play(self, stream_info):
        # type: (StreamInfo) -> None
        if not stream_info:
            xbmcplugin.setResolvedUrl(self._handle, False, xbmcgui.ListItem())
            return

        if stream_info.manifest_type in ['mpd', 'hls', 'ism'] and isinstance(stream_info.drm, WidevineDRM):
            import inputstreamhelper
            is_helper = inputstreamhelper.Helper(stream_info.manifest_type, drm='com.widevine.alpha')
            if is_helper.check_inputstream():
                item = xbmcgui.ListItem(path=stream_info.url)
                item.setProperty('inputstream', is_helper.inputstream_addon)
                item.setProperty('inputstream.adaptive.manifest_type', stream_info.manifest_type)
                item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
                item.setProperty('inputstream.adaptive.license_key', stream_info.drm.licence_key.to_string())
                item.setProperty('inputstream.adaptive.license_flags', stream_info.drm.flags)
                if stream_info.drm.license_data:
                    item.setProperty('inputstream.adaptive.license_data', stream_info.drm.license_data)
                if stream_info.drm.server_certificate:
                    item.setProperty('inputstream.adaptive.server_certificate', stream_info.drm.server_certificate)
                if stream_info.max_bandwidth:
                    item.setProperty('inputstream.adaptive.max_bandwidth', stream_info.max_bandwidth)
                if stream_info.user_agent:
                    stream_info.headers.update({'User-Agent': stream_info.user_agent})
                if stream_info.headers:
                    item.setProperty('inputstream.adaptive.stream_headers', '&'.join(['%s=%s' % (k, v) for (k, v) in
                                                                                      list(stream_info.headers.items())]))
                if stream_info.drm.media_renewal_url:
                    item.setProperty('inputstream.adaptive.media_renewal_url', stream_info.drm.media_renewal_url)
                if stream_info.drm.media_renewal_time > 0:
                    item.setProperty('inputstream.adaptive.media_renewal_time', stream_info.drm.media_renewal_time)
                xbmcplugin.setResolvedUrl(self._handle, True, item)

        elif stream_info.manifest_type == 'mpd':
            item = xbmcgui.ListItem(path=stream_info.url)
            item.setProperty('inputstream', 'inputstream.adaptive')
            item.setProperty('inputstream.adaptive.manifest_type', stream_info.manifest_type)

            if stream_info.user_agent:
                stream_info.headers.update({'User-Agent': stream_info.user_agent})
            if stream_info.headers:
                item.setProperty('inputstream.adaptive.stream_headers', '&'.join(['%s=%s' % (k, v) for (k, v) in
                                                                                  list(stream_info.headers.items())]))
            xbmcplugin.setResolvedUrl(self._handle, True, item)

        elif stream_info.manifest_type == 'm3u':
            item = xbmcgui.ListItem(path=stream_info.url)
            item.setProperty('inputstream', 'inputstream.adaptive')
            item.setProperty('inputstream.adaptive.manifest_type', 'hls')

            if stream_info.user_agent:
                stream_info.headers.update({'User-Agent': stream_info.user_agent})
            if stream_info.headers:
                item.setProperty('inputstream.adaptive.stream_headers', '&'.join(['%s=%s' % (k, v) for (k, v) in
                                                                                  list(stream_info.headers.items())]))
            xbmcplugin.setResolvedUrl(self._handle, True, item)
            return
        else:
            xbmcplugin.setResolvedUrl(self._handle, False, xbmcgui.ListItem())

    def play_channel_route(self, channel_id):
        self._play(self.channel_stream_info(channel_id))

    def play_programme_route(self, programme_id):
        self._play(self.programme_stream_info(programme_id))

    def play_programme_by_time_route(self, channel_id, start, end):
        start = datetime.utcfromtimestamp(int(start))
        end = datetime.utcfromtimestamp(int(end))
        epg = self.epg([channel_id], start, end)
        for program in epg[channel_id]:
            if start <= program.start_time and program.end_time <= end:
                self.play_programme_route(program.id)

    def add_index_directory_items(self):
        xbmcplugin.addDirectoryItem(self._handle, self.url_for(self.channels_route), xbmcgui.ListItem(label=_('live_tv')), True)
        xbmcplugin.addDirectoryItem(self._handle, self.url_for(self.archive_route), xbmcgui.ListItem(label=_('archive')), True)

    def index_route(self):
        xbmcplugin.setPluginCategory(self._handle, '')
        xbmcplugin.setContent(self._handle, 'videos')

        self.add_index_directory_items()

        xbmcplugin.endOfDirectory(self._handle)

    def channels_route(self):
        channels = self.channels()
        xbmcplugin.setPluginCategory(self._handle, _('live_tv'))
        for channel in channels:
            list_item = xbmcgui.ListItem(label=channel.name)
            list_item.setInfo('video', {'title': channel.name})
            list_item.setArt({'thumb': channel.logo})
            list_item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(self._handle, self.url_for(self.play_channel_route, channel.id), list_item, False)
        xbmcplugin.endOfDirectory(self._handle)

    def archive_route(self):
        channels = self.channels()
        xbmcplugin.setPluginCategory(self._handle, _('archive'))
        for channel in channels:
            if channel.archive_days > 0:
                list_item = xbmcgui.ListItem(label=channel.name)
                list_item.setInfo('video', {'title': channel.name})
                list_item.setArt({'thumb': channel.logo})
                xbmcplugin.addDirectoryItem(self._handle, self.url_for(self.archive_days_route, channel.id, channel.name), list_item, True)
        xbmcplugin.endOfDirectory(self._handle)

    def archive_days_route(self, channel_id, channel_name):
        now = datetime.now()
        xbmcplugin.setPluginCategory(self._handle, 'Replay' + ' / ' + channel_name)
        for day in range(0, self.client.archive_days() + 1):
            d = now - timedelta(days=day)
            title = _('today') if day == 0 else _('yesterday') if day == 1 else d.strftime('%d. %m.')
            list_item = xbmcgui.ListItem(label=_('day_%d' % (d.weekday() + 1)) + ', ' + title)
            list_item.setArt({'icon': 'DefaultAddonPVRClient.png'})
            url = self.url_for(self.archive_programmes_route, channel_id, channel_name, d.strftime("%m-%d-%Y"))
            xbmcplugin.addDirectoryItem(self._handle, url, list_item, True)
        xbmcplugin.endOfDirectory(self._handle)

    @staticmethod
    def _strptime(date_string, format):
        # https://forum.kodi.tv/showthread.php?tid=112916 it's insane !!!
        try:
            return datetime.strptime(date_string, format)
        except TypeError:
            import time as ptime
            return datetime(*(ptime.strptime(date_string, format)[0:6]))

    def _utc2local(self, utc):
        # type: (datetime) -> datetime
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
        return utc + offset

    def archive_programmes_route(self, channel_id, channel_name, day):
        day = self._strptime(day, '%m-%d-%Y')
        next_day = day + timedelta(days=1)
        prev_day = day + timedelta(days=-1)

        epg = self.epg([channel_id], day, day)

        xbmcplugin.setPluginCategory(self._handle, _('archive') + ' / ' + channel_name)

        if day > datetime.today() - timedelta(days=self.client.archive_days()):
            list_item = xbmcgui.ListItem(label=_('day_before'))
            list_item.setArt({'icon': 'DefaultVideoPlaylists.png'})
            url = self.url_for(self.archive_programmes_route, channel_id, channel_name, prev_day.strftime("%m-%d-%Y"))
            xbmcplugin.addDirectoryItem(self._handle, url, list_item, True)

        if epg:
            for programme in epg[channel_id]:
                if programme.is_replyable:
                    title = self._utc2local(programme.start_time).strftime('%H:%M') + ' - ' + programme.title
                    list_item = xbmcgui.ListItem(label=title)

                    video_info = {
                        'title': programme.title,
                        'plot': programme.description,
                        'duration': programme.duration
                    }

                    if programme.episodeNo:
                        video_info['episode'] = programme.episodeNo

                    if programme.seasonNo:
                        video_info['season'] = programme.seasonNo

                    if programme.year:
                        video_info['year'] = programme.year

                    if programme.actors:
                        video_info['cast'] = programme.actors

                    if programme.directors:
                        video_info['director'] = programme.directors[0]

                    list_item.setInfo('video', video_info)

                    art_info = {}
                    if programme.thumbnail:
                        art_info = {'thumb': programme.thumbnail, 'icon': programme.thumbnail}

                    if programme.poster:
                        art_info['poster'] = programme.poster

                    list_item.setArt(art_info)

                    url = self.url_for(self.play_programme_route, programme.id)
                    list_item.setProperty('IsPlayable', 'true')
                    xbmcplugin.addDirectoryItem(self._handle, url, list_item, False)

        if day.date() < datetime.today().date():
            list_item = xbmcgui.ListItem(label=_('day_after'))
            list_item.setArt({'icon': 'DefaultVideoPlaylists.png'})
            url = self.url_for(self.archive_programmes_route, channel_id, channel_name, next_day.strftime("%m-%d-%Y"))
            xbmcplugin.addDirectoryItem(self._handle, url, list_item, True)

        xbmcplugin.endOfDirectory(self._handle)
