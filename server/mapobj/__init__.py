# -*- coding: utf-8 -*-

from . import mapobject

import pubglobalmanager

def Init():
	oMap = mapobject.CMap()
	oMap.Init()
	pubglobalmanager.SetGlobalManager("map", oMap)
	