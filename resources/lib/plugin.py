# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon

import xbmc
import urllib2
import re
import urllib
import urlparse

from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

domain_base = 'https://www.hogarmania.com'
url_base = domain_base + '/tv/programas/bricomania/'


@plugin.route('/')
def index():
    logger.warn(url_base)
    http = urllib2.urlopen(url_base)
    html = http.read()
    http.close()

    yearsHtml = re.findall('<ul class="anio">(.*?)<ul class=', html, re.DOTALL)[0]
    #logger.warn(yearsHtml)
    years = re.findall('<li(.*?)</li>', yearsHtml, re.DOTALL)
    years.reverse()

    logger.warn('******2020-/tv/programas/bricomania/index.html?202001--2020')
    for year in years:
        href = re.findall('href="(.*)" title', year, re.DOTALL)[0]
        year_month = re.findall('\?(.*)', href, re.DOTALL)[0]
        label = re.findall('<a .*>(.*)</a>', year, re.DOTALL)[0]
        addDirectoryItem(plugin.handle, plugin.url_for(show_year, year_month), ListItem(label), True)

    endOfDirectory(plugin.handle)

@plugin.route('/year/<year_month_id>')
def show_year(year_month_id):
    logger.warn(year_month_id)

    http = urllib2.urlopen('{url}index.html?{year_month_id}'.format(url=url_base, year_month_id=year_month_id))
    html = http.read()
    http.close()

    monthsHtml = re.findall('<ul class="mes {year}" style="display: none;">(.*?)</ul>'.format(year=year_month_id[:-2]), html, re.DOTALL)[0]
    months = re.findall('<li(.*?)</li>', monthsHtml, re.DOTALL)
    months.reverse()

    for month in months:
        label = re.findall('href=.*>(.*)</a>', month, re.DOTALL)[0]
        href = re.findall('href="(.*)"', month, re.DOTALL)[0]
        year_month = re.findall('\?(.*)', href, re.DOTALL)[0]
        addDirectoryItem(plugin.handle, plugin.url_for(show_month, year_month), ListItem(label), True)

    endOfDirectory(plugin.handle)


@plugin.route('/month/<year_month_id>')
def show_month(year_month_id):
    #logger.warn(year_month_id)

    http = urllib2.urlopen('{url}index.html?{year_month_id}'.format(url=url_base, year_month_id=year_month_id))
    html = http.read()
    http.close()

    weeksHtml = re.findall('<li class="pagina-tv">.*<ul>(.*?)</ul>', html, re.DOTALL)[0]
    weeks = re.findall('<li>(.*?)</li>', weeksHtml, re.DOTALL)
    #weeks.reverse()
    
    for week in weeks:
        #logger.warn(week)
        date = re.findall('fecha">(.*)</h3>', week, re.DOTALL)[0]
        href = re.findall('href="(.*)" title', week, re.DOTALL)[0]
        label = re.findall('title="(.*)">.*<span', week, re.DOTALL)[0] + ' [' + date + ']'
        thumbnail = re.findall('img src="(.*)" alt', week, re.DOTALL)[0]
        
        youtubeId = href.replace('https://m.youtube.com/watch?v=', '')
        addDirectoryItem(plugin.handle, plugin.url_for(play_youtube, youtubeId), ListItem(label))    
        
        
    endOfDirectory(plugin.handle)

@plugin.route('/youtube/<youtube_id>')
def play_youtube(youtube_id):
    logger.warn(youtube_id)
    #youtubePath='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid={youtube_id}'
    youtubePath='plugin://plugin.video.youtube/play/?video_id={video}'.format(video=youtube_id)
    xbmc.executebuiltin('PlayMedia({youtubePath})'.format(youtubePath=youtubePath))


def run():
    plugin.run()