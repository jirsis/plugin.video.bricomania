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
    logger.warn("34567")
    #http = urllib2.urlopen(url_base)
    #html = http.read()
    #http.close()

    #yearsHtml = re.findall('<ul class="anio">(.*?)<ul class=', html, re.DOTALL)[0]
    #years = re.findall('<li(.*?)</li>', yearsHtml, re.DOTALL)
    years = ['2019', '2018', '2017', '2016', '2015', '1995']
    years.reverse()

    for year in years:
        addDirectoryItem(plugin.handle, plugin.url_for(show_category, year), ListItem("Category "+year), True)

    endOfDirectory(plugin.handle)


@plugin.route('/category/<category_id>')
def show_category(category_id):
    addDirectoryItem(
        plugin.handle, "", ListItem("Hello category %s!" % category_id))
    endOfDirectory(plugin.handle)

def run():
    plugin.run()