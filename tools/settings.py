# -*- coding: utf-8 -*-

import xbmcaddon

def get(settingName):
    setting=xbmcaddon.Addon().getSetting(settingName)
    return setting

def isTracesEnable():
    return get('traces_enabled')

def isHtmlDebugEnable():
    return get('html_debug_enabled')