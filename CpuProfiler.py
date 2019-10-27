# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import logging
import requests
import threading
import gettext
import json
import psutil
import mysql.connector
from mysql.connector import Error
from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
# Import Actions and CIOS
import Actions
import CIOS
from CIOS.StarDate import StarDate
# Import PyQt5 interface
from PyQt5 import QtWidgets , QtGui , QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon , QCursor
from PyQt5.QtWidgets import QApplication , QWidget , qApp , QSystemTrayIcon , QMenu , QAction , QActionGroup

Settings     = { }
Locales      = { }
Translations = { }

def ActualFile ( filename ) :
  return os . path . dirname ( os . path . abspath (__file__) ) + "/" + filename

def LoadJSON ( Filename ) :
  if ( not os . path . isfile ( Filename ) ) :
    return { }
  TEXT     = ""
  with open ( Filename , "rb" ) as cpuFile :
    TEXT   = cpuFile . read ( )
  if ( len ( TEXT ) <= 0 ) :
    return { }
  BODY = TEXT . decode ( "utf-8" )
  return json . loads ( BODY )

def CpuProfilerMain   (                                     ) :
  global Settings
  global Locales
  global Translations
  Settings     = LoadJSON   ( ActualFile ( "settings.json"        ) )
  Locales      = LoadJSON   ( ActualFile ( "locales/locales.json" ) )
  Language     = Settings   [ "Language"                            ]
  TRFILE       = f"locales/{Language}/translations.json"
  Translations = LoadJSON   ( ActualFile ( TRFILE                 ) )
  print ( Settings     )
  print ( Locales      )
  print ( Translations )

if __name__ == '__main__':
  CpuProfilerMain ( )
