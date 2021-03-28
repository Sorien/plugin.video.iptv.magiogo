# -*- coding: utf-8 -*-

import xbmc

_lang = {}
_lang['en'] = {}
_lang['en']['playlist_created'] = 'M3U Playlist created'
_lang['en']['playlist_and_epg_created'] = 'M3U Playlist and EPG created'
_lang['en']['playlist_or_epg_not_created'] = 'M3U Playlist or EPG not created'
_lang['en']['live_tv'] = 'Live TV'
_lang['en']['archive'] = 'Archive'
_lang['en']['today'] = 'today'
_lang['en']['yesterday'] = 'yesterday'
_lang['en']['day_1'] = 'monday'
_lang['en']['day_2'] = 'tuesday'
_lang['en']['day_3'] = 'wednesday'
_lang['en']['day_4'] = 'thursday'
_lang['en']['day_5'] = 'friday'
_lang['en']['day_6'] = 'saturday'
_lang['en']['day_7'] = 'sunday'
_lang['en']['day_after'] = 'the day after'
_lang['en']['day_before'] = 'the day before'
_lang['en']['creating_playlist'] = 'Creating M3U Playlist'
_lang['en']['creating_epg'] = 'Creating EPG'
_lang['en']['configuring_addon'] = 'Configuring Addon'
_lang['en']['iptv_simple_not_installed'] = 'IPTV Simple Client add-on is not installed'
_lang['en']['iptv_simple_configure'] = 'Change configuration of IPTV Simple Client add-on according {}'

_lang['sk'] = {}
_lang['sk']['playlist_created'] = 'M3U Playlist bol vytvorený'
_lang['sk']['playlist_and_epg_created'] = 'M3U Playlist a EPG boli vytvorené'
_lang['sk']['playlist_or_epg_not_created'] = 'M3U Playlist alebo EPG sa nepodarilo vytvoriť'
_lang['sk']['live_tv'] = 'Živé vysielanie'
_lang['sk']['archive'] = 'Archív'
_lang['sk']['today'] = 'dnes'
_lang['sk']['yesterday'] = 'včera'
_lang['sk']['day_1'] = 'pondelok'
_lang['sk']['day_2'] = 'utorok'
_lang['sk']['day_3'] = 'streda'
_lang['sk']['day_4'] = 'štvrtok'
_lang['sk']['day_5'] = 'piatok'
_lang['sk']['day_6'] = 'sobota'
_lang['sk']['day_7'] = 'nedeľa'
_lang['sk']['day_after'] = 'nasledujúci deň'
_lang['sk']['day_before'] = 'predošlý deň'
_lang['sk']['creating_playlist'] = 'Vytváram M3U Playlist'
_lang['sk']['creating_epg'] = 'Vytváram EPG'
_lang['sk']['configuring_addon'] = 'Konfigurujem doplnok'
_lang['sk']['iptv_simple_not_installed'] = 'Doplnok IPTV Simple Client nie je nainštalovaný'
_lang['sk']['iptv_simple_configure'] = 'Upraviť konfiguráciu doplnku IPTV Simple Client podľa {}'

_lang['cs'] = {}
_lang['cs']['playlist_created'] = 'M3U Playlist byl vytvořený'
_lang['cs']['playlist_and_epg_created'] = 'M3U Playlist a EPG byli vytvořené'
_lang['cs']['playlist_or_epg_not_created'] = 'M3U Playlist nebo EPG se nepodařilo vytvořit'
_lang['cs']['live_tv'] = 'Živé vysílání'
_lang['cs']['archive'] = 'Archiv'
_lang['cs']['today'] = 'dnes'
_lang['cs']['yesterday'] = 'včera'
_lang['cs']['day_1'] = 'pondělí'
_lang['cs']['day_2'] = 'úterý'
_lang['cs']['day_3'] = 'středa'
_lang['cs']['day_4'] = 'čtvrtek'
_lang['cs']['day_5'] = 'pátek'
_lang['cs']['day_6'] = 'sobota'
_lang['cs']['day_7'] = 'neděle'
_lang['cs']['day_after'] = 'další den'
_lang['cs']['day_before'] = 'předchozí den'
_lang['cs']['creating_playlist'] = 'Vytvářím M3U Playlist'
_lang['cs']['creating_epg'] = 'Vytvářím EPG'
_lang['cs']['configuring_addon'] = 'Konfigurace doplňku'
_lang['cs']['iptv_simple_not_installed'] = 'Doplněk IPTV Simple Client není nainstalovaný'
_lang['cs']['iptv_simple_configure'] = 'Upravit konfiguraci doplňku IPTV Simple Client podle {}'

_code = xbmc.getLanguage(xbmc.ISO_639_1)


def _(key):
    # type: (str) -> str
    code = _code if _code in _lang else 'en'
    return _lang[code][key] if key in _lang[code] else 'Unknown Translation: [%s] %s' % (code, key)
