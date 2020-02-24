# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'


class Account(object):
    NAME = ""  # QQ acount
    PWD = ""  # QQ password


class TestInfo(object):
    PACKAGE = "com.special.warshiplegend.idle"  # test package name


### Engine Type
Unity = "unity"
UE4 = "ue4"


class Engine(object):
    Unity = "unity"
    UE4 = "ue4"


EngineType = Engine.Unity  # Type="unity" # unity or ue4
