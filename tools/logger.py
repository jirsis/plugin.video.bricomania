# -*- coding: utf-8 -*-

import xbmc
from tools import settings

def debug(msg):
    enabled = settings.isTracesEnable()
    if enabled:
        showDebugTrace(msg)

def debugHtml(msg):
    enabled = settings.isHtmlDebugEnable()
    if enabled:
        showDebugTrace(msg)

def showDebugTrace(msg):
    xbmc.log("BRICO-jarvis: "+str(msg))