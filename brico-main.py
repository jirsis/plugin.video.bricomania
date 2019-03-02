# -*- coding: utf-8 -*-

from tools import logger

import re
import sys
import urllib2
import urllib
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc


__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
action = args.get('action', None)

domain_base = 'https://www.hogarmania.com'
url_base = domain_base + '/tv/programas/bricomania/'

plugin_url_base = sys.argv[0]

if action is None:
    logger.debug("main menu - list years")
    http = urllib2.urlopen(url_base)
    html = http.read()
    http.close()
    logger.debugHtml(html)
    yearsHtml = re.findall('<ul class="anio">(.*?)<ul class=', html, re.DOTALL)[0]
    logger.debugHtml(yearsHtml)
    years = re.findall('<li(.*?)</li>', yearsHtml, re.DOTALL)
    years.reverse()
    logger.debugHtml(years)
    
    for year in years:
        logger.debugHtml(year)
        currentYear = re.findall('title=".*">(.*)</a>', year, re.DOTALL)[0]
        href = re.findall('href="(.*)" title', year, re.DOTALL)[0]
        label = re.findall('<a .*>(.*)</a>', year, re.DOTALL)[0]
        
        query = {'action': 'year', 'url': domain_base + href, 'yearSelected': currentYear}
        logger.debug(query)
        
        url = plugin_url_base + '?'+urllib.urlencode(query)

        item = xbmcgui.ListItem(label=label, thumbnailImage='')
        item.setProperty('IsPlayable', str(False))
        xbmcplugin.addDirectoryItem(addon_handle, listitem=item, url=url, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif action[0] == 'year':
    yearSelected = args.get('yearSelected')[0]
    logger.debug('year menu [' + yearSelected + '] - list months')
    url = args.get('url', None)[0]
    http = urllib2.urlopen(url)
    html = http.read()
    http.close()
    logger.debugHtml(html)
    monthsHtml = re.findall('<ul class="mes '+yearSelected+'" style="display: none;">(.*?)</ul>', html, re.DOTALL)[0]
    logger.debugHtml(monthsHtml)
    months = re.findall('<li(.*?)</li>', monthsHtml, re.DOTALL)
    logger.debugHtml(months)
    
    for month in months:
        logger.debugHtml(month)
        label = re.findall('href=.*>(.*)</a>', month, re.DOTALL)[0]
        href = re.findall('href="(.*)"', month, re.DOTALL)[0]
        logger.debug(label + " -> " + href)

        query = {'action':'month', 'url': domain_base + href, 'year': yearSelected, 'month': label}
        logger.debug(query)

        url = plugin_url_base + '?' + urllib.urlencode(query)

        item = xbmcgui.ListItem(label=label, thumbnailImage='')
        item.setProperty('IsPlayable', str(False))
        xbmcplugin.addDirectoryItem(addon_handle, listitem=item, url=url, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif action[0] == 'month':
    yearSelected = args.get('year', None)[0]
    monthSelected = args.get('month', None)[0]
    logger.debug('month menu [' + monthSelected + '/' + yearSelected + '] - list programs')
    url = args.get('url', None)[0]
    http = urllib2.urlopen(url)
    html = http.read()
    http.close()
    logger.debugHtml(html)

    weeksHtml = re.findall('<li class="pagina-tv">.*<ul>(.*?)</ul>', html, re.DOTALL)[0]
    logger.debugHtml(weeksHtml)
    weeks = re.findall('<li>(.*?)</li>', weeksHtml, re.DOTALL)
    weeks.reverse()
    logger.debugHtml(weeks)

    for week in weeks:
        logger.debugHtml(week)
        date = re.findall('fecha">(.*)</h3>', week, re.DOTALL)[0]
        href = re.findall('href="(.*)" title', week, re.DOTALL)[0]
        label = re.findall('title="(.*)">.*<span', week, re.DOTALL)[0] + ' [' + date + ']'
        thumbnail = re.findall('img src="(.*)" alt', week, re.DOTALL)[0]
        logger.debug(label + " -> " + href + '[' + thumbnail + ']')
        
        query = {'action':'week', 'url': href, 'year': yearSelected, 'month': monthSelected, 'week': label, 'thumbnail': thumbnail}
        logger.debug(query)

        url = plugin_url_base + '?' + urllib.urlencode(query)

        item = xbmcgui.ListItem(label=label, thumbnailImage=domain_base + thumbnail)
        item.setProperty('IsPlayable', str(False))
        xbmcplugin.addDirectoryItem(addon_handle, listitem=item, url=url, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif action[0] == 'week':
    yearSelected = args.get('year', None)[0]
    monthSelected = args.get('month', None)[0]
    weekSelected = args.get('week', None)[0]
    thumbnail = args.get('thumbnail', None)[0]
    url = args.get('url', None)[0]

    logger.debug('week menu: ' + weekSelected + ' [' + monthSelected + '/' + yearSelected + '] - play program -> '+url)
    
    youtubeUrl = url

    youtubePath='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='
    youtubeId = youtubeUrl.replace('https://m.youtube.com/watch?v=', '')
    path = youtubePath + youtubeId

    logger.debug('YOUTUBE url: '+ youtubeUrl)
    logger.debug('YOUTUBE path: '+ path)
    xbmc.executebuiltin('PlayMedia('+path+')')

else:
    logger.debug("??")
    