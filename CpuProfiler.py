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
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
# Actions and CIOS
import CIOS
from CIOS .       StarDate import StarDate
from CIOS .       Debugger import ConfigureDebugger , ChangeDebuggerLevel
from CIOS . CPU . Profiler import Profiler
from CIOS . CPU . Daemon   import Daemon
from CIOS . CPU . Feeder   import CpuFeeder , ConfigureCpu
from CIOS . CPU . Analyzer import Analyzer
from CIOS . CPU . CpuChart import CpuChart

# Import PyQt5 interface
# Import PyQt5 interface
from PyQt5 import QtWidgets , QtGui , QtCore
from PyQt5.QtCore import QObject , pyqtSignal , QPointF , QTimer
from PyQt5.QtGui import QIcon , QCursor , QPen , QBrush , QColor
from PyQt5.QtGui import QPolygonF , QTransform
from PyQt5.QtWidgets import QApplication , QWidget , qApp , QAction , QActionGroup
from PyQt5.QtWidgets import QSystemTrayIcon , QMenu , QGraphicsView , QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem , QGraphicsPolygonItem

Settings            = { }
Locales             = { }
Translations        = { }
Hosts               = { }
Httpd               = None
Ghost               = None
Tray                = None
CpuProfilerSettings =                      { \
  "Hostname"        : "Cuisine"            , \
  "Path"            : "D:/Temp/CPU/Myself" , \
  "Lines"           : 900                  , \
  "Interval"        : 334                  , \
  "TimeZone"        : "Asia/Taipei"        , \
  "Decide"          : DecideRunning        , \
  "Port"            : 16319                , \
  "Running"         : True                 , \
}

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

# HTTP Feeder
class PrivateFeederThreadedHTTPServer ( ThreadingMixIn , HTTPServer ) :
  pass

def StopRunning ( ) :
  global Httpd
  Httpd . shutdown ( )
  CpuProfilerSettings [ "Running" ] = False

def DecideRunning ( ) :
  global CpuProfilerSettings
  return CpuProfilerSettings [ "Running" ]

def RunCpuFeeder ( ) :
  global Httpd
  global Ghost
  global CpuProfilerSettings
  Port  = CpuProfilerSettings [ "Port" ]
  Httpd = PrivateFeederThreadedHTTPServer ( ( '0.0.0.0' , Port ) , CpuFeeder )
  Httpd . serve_forever ( )

""" 系統選單 """
class CpuProfilerMenu ( QSystemTrayIcon ) :
  # emitShowUser = pyqtSignal ( bool , dict )
  def __init__(self , icon , parent = None ) :
    global Settings
    global Locales
    global Translations
    QSystemTrayIcon . __init__ ( self , icon , parent )
    self . setToolTip ( Translations [ "Menu::Title" ] )
    self . activated . connect ( self . onTrayActivated )
    self . Actions = { }
    # Configure Menu
    self . Menu = QMenu ( parent      )
    self . PrepareMenu  ( self . Menu )

  def PrepareMenu ( self , menu ) :
    global Settings
    global Locales
    global Translations
    # 主機
    self          . hostsMenu    ( menu   )
    # 設置語言
    self          . languageMenu ( menu   )
    #
    menu          . addSeparator (        )
    # Start
    startAction   = menu . addAction ( Translations [ "Menu::Start" ] )
    # startAction   . setIcon ( QIcon ( ActualFile ( Settings [ "Menu" ] [ "Quit" ] ) ) )
    startAction   . triggered . connect ( self . Start )
    self . Actions [ "Start" ] = startAction
    # Stop
    stopAction    = menu . addAction ( Translations [ "Menu::Stop" ] )
    # stopAction    . setIcon ( QIcon ( ActualFile ( Settings [ "Menu" ] [ "Quit" ] ) ) )
    stopAction    . triggered . connect ( self . Stop )
    # stopAction    . setVisible ( False )
    self . Actions [ "Stop"  ] = stopAction
    # Exit
    exitAction    = menu . addAction ( Translations [ "Menu::Quit" ] )
    exitAction    . setIcon ( QIcon ( ActualFile ( Settings [ "Menu" ] [ "Quit" ] ) ) )
    exitAction    . triggered . connect ( self . Quit )
    self . Actions [ "Exit"  ] = exitAction
    #
    self . setContextMenu ( menu )

  def languageMenu ( self , menu ) :
    return True

  def hostsMenu ( self , menu ) :
    return True

  def onTrayActivated ( self , reason ) :
    if ( reason == 3 ) :
      self . Menu . exec_ ( QCursor . pos ( ) )

  def Start ( self ) :
    threading . Thread ( target = CpuDaemonMain ) . start ( )

  def Stop ( self ) :
    StopRunning ( )

  def Quit ( self ) :
    self . hide ( )
    qApp . quit ( )

def CpuDaemonMain ( ) :
  global Ghost
  global CpuProfilerSettings
  Logger    = logging . getLogger (                         )
  Ghost     = Daemon              ( CpuProfilerSettings     )
  Path      = CpuProfilerSettings [ "Path"     ]
  TZ        = CpuProfilerSettings [ "TimeZone" ]
  ConfigureCpu                    ( { "Daemon"   : Ghost       ,
                                      "Stop"     : StopRunning ,
                                      "Path"     : Path        ,
                                      "TimeZone" : TZ          ,
                                      "Username" : "foxman"    ,
                                      "Password" : "la0marina" ,
                                      "Verify"   : False       ,
                                      } )
  # 啟動網路效能數據提供
  threading . Thread              ( target = RunCpuFeeder   ) . start ( )
  # 執行機器效能監視器
  Ghost     . run                 (                         )
  Logger    . debug               ( "Complete CPU Profiler" )

def CpuProfilerMain ( ) :
  global Settings
  global Locales
  global Translations
  global Hosts
  Settings     = LoadJSON   ( ActualFile ( "settings.json"        ) )
  Locales      = LoadJSON   ( ActualFile ( "locales/locales.json" ) )
  Language     = Settings   [ "Language"                            ]
  TRFILE       = f"locales/{Language}/translations.json"
  Translations = LoadJSON   ( ActualFile ( TRFILE                 ) )
  if ( Settings [ "UserDirectory" ] > 0 ) :
    Settings [ "Home" ] = str ( Path . home ( ) )
  else :
    Settings [ "Home" ] = os . path . dirname ( os . path . abspath (__file__) )
  # 讀取私人設定
  UserConf = Settings [ "Home" ]
  UserConf = f"{UserConf}/CpuProfiler"
  if                         ( not os . path . isdir ( UserConf )         ) :
    os . mkdir               ( UserConf                                     )
  if                         (     os . path . isdir ( UserConf )         ) :
    Hosts  = LoadJSON        ( f"{UserConf}/hosts.json"                     )
    STS    = LoadJSON        ( f"{UserConf}/settings.json"                  )
    KEYs   = STS . keys      (                                              )
    for k in KEYs                                                           :
      Settings [ k ] = STS   [ k                                            ]
  # 設定除錯機制
  isConsole   = False
  if ( Settings [ "Console" ] > 0 ) :
    isConsole = True
  ConfigureDebugger                ( {
    "Debug"   : Settings [ "Debug" ] ,
    "LOG"     : Settings [ "LOG"   ] ,
    "Console" : isConsole            ,
  } )
  # 啟動選單
  app      = QApplication    ( sys . argv                                   )
  trayMenu = CpuProfilerMenu ( QIcon ( ActualFile ( Settings [ "Icon" ] ) ) )
  trayMenu . show            (                                              )
  Tray     = trayMenu
  # 啟動機器效能監視器
  threading . Thread         ( target = CpuDaemonMain ) . start ( )
  sys      . exit            ( app . exec_ ( )                              )
  # 結束

if __name__ == '__main__':
  CpuProfilerMain ( )
