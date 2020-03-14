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
    logger.warn(yearsHtml)
    years = re.findall('<li(.*?)</li>', yearsHtml, re.DOTALL)
    years.reverse()

    for year in years:
        currentYear = re.findall('title=".*">(.*)</a>', year, re.DOTALL)[0]
        href = re.findall('href="(.*)" title', year, re.DOTALL)[0]
        label = re.findall('<a .*>(.*)</a>', year, re.DOTALL)[0]
        logger.warn(currentYear+'-'+href+'--'+label)
        addDirectoryItem(plugin.handle, plugin.url_for(show_year, label), ListItem(label), True)

    endOfDirectory(plugin.handle)

@plugin.route('/year/<year_id>')
def show_year(year_id):
    addDirectoryItem(plugin.handle, "", ListItem("Hello yearrrr %s!" % year_id))
    endOfDirectory(plugin.handle)


def run():
    plugin.run()