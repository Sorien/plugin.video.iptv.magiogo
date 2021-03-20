# -*- coding: utf-8 -*-

try:
    from typing import List, Dict, Callable
except:
    pass

from io import open
from iptv.client import Channel, Programme

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)


def create_m3u(file_name, channels, url_callback):
    # type: (str, List[Channel], Callable[[Channel, bool], str]) -> None
    with open(file_name, 'w', encoding='utf8') as file:
        file.write('#EXTM3U\n')

        for c in channels:
            live_url = url_callback(c, False)
            if live_url:
                file.write('#EXTINF:-1')
                file.write(' tvg-id="%s"' % c.id)
                if c.logo:
                    file.write(' tvg-logo="%s"' % c.logo)

                catchup_url = url_callback(c, True)
                if catchup_url and c.archive_days > 0:
                    file.write(' catchup-days="%d" catchup-source="%s"' % (c.archive_days, catchup_url))

                file.write(',%s\n' % c.name)
                file.write('%s\n' % live_url)


def create_epg(file_name, epg):
    # type: (str, Dict[str, List[Programme]]) -> None
    with open(file_name, 'w', encoding='utf8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        file.write('<tv>\n')

        for channel_id in epg:
            file.write('<channel id="%s">\n' % channel_id)
            file.write('</channel>\n')

        for channel_id in epg:
            for p in epg[channel_id]:
                file.write('<programme channel="%s" start="%s" stop="%s">\n' % (
                    channel_id, p.start_time.strftime('%Y%m%d%H%M%S'), p.end_time.strftime('%Y%m%d%H%M%S')))
                if p.title:
                    file.write('<title>%s</title>\n' % html_escape(p.title))
                if p.description:
                    file.write('<desc>%s</desc>\n' % html_escape(p.description))
                if p.thumbnail:
                    file.write('<icon src="%s"/>\n' % html_escape(p.thumbnail))
                if p.genres:
                    file.write('<category>%s</category>\n' % html_escape(', '.join(p.genres)))
                if p.actors or p.directors or p.writers or p.producers:
                    file.write('<credits>\n')
                    for actor in p.actors:
                        file.write('<actor>%s</actor>\n' % html_escape(actor))
                    for director in p.directors:
                        file.write('<director>%s</director>\n' % html_escape(director))
                    for writer in p.writers:
                        file.write('<writer>%s</writer>\n' % html_escape(writer))
                    for producer in p.producers:
                        file.write('<producer>%s</producer>\n' % html_escape(producer))
                    file.write('</credits>\n')
                if p.seasonNo and p.episodeNo:
                    file.write('<episode-num system="xmltv_ns">%d.%d.</episode-num>\n' % (p.seasonNo - 1, p.episodeNo - 1))
                file.write('</programme>\n')
        file.write('</tv>\n')
