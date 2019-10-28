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
Hosts               = [ ]
Httpd               = None
Ghost               = None
Tray                = None
Machine             = None

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

def WriteSettings ( ) :
  global Settings
  KEYs = Settings . keys ( )
  SS   = { }
  UserConf = Settings [ "Home" ]
  UserConf = f"{UserConf}/CpuProfiler/settings.json"
  for K in KEYs :
    if ( K not in [ "Home" , "Root" ] ) :
      SS [ K ] = Settings [ K ]
  TEXT = json . dumps ( SS )
  with open ( UserConf , "w" ) as settingsFile :
    settingsFile . write ( TEXT )
  return True

# HTTP Feeder
class PrivateFeederThreadedHTTPServer ( ThreadingMixIn , HTTPServer ) :
  pass

def StartRunning ( ) :
  CpuProfilerSettings [ "Running" ] = True
  threading . Thread ( target = CpuDaemonMain ) . start ( )
  Tray . Actions [ "Start" ] . setVisible ( False )
  Tray . Actions [ "Stop"  ] . setVisible ( True  )
  Tray . Actions [ "Exit"  ] . setVisible ( False )

def StopRunning ( ) :
  global Httpd
  Httpd . shutdown ( )
  CpuProfilerSettings [ "Running" ] = False
  Tray  . Actions [ "Start" ] . setVisible ( True  )
  Tray  . Actions [ "Stop"  ] . setVisible ( False )
  Tray  . Actions [ "Exit"  ] . setVisible ( True  )

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

CpuProfilerSettings =                      { \
  "Hostname"        : "Cuisine"            , \
  "Path"            : "D:/Temp/CPU/Myself" , \
  "Root"            : ""                   , \
  "Lines"           : 900                  , \
  "Interval"        : 334                  , \
  "TimeZone"        : "Asia/Taipei"        , \
  "Decide"          : DecideRunning        , \
  "Port"            : 16319                , \
  "Running"         : True                 , \
}

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
    self . MyParent = parent
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
    # 設置除錯
    self          . debuggerMenu ( menu   )
    #
    menu          . addSeparator (        )
    # Start
    startAction   = menu . addAction ( Translations [ "Menu::Start" ] )
    if ( "Start" in Settings [ "Menu" ] ) :
      startAction   . setIcon ( QIcon ( ActualFile ( Settings [ "Menu" ] [ "Start" ] ) ) )
    startAction   . triggered . connect ( self . Start )
    self . Actions [ "Start" ] = startAction
    # Stop
    stopAction    = menu . addAction ( Translations [ "Menu::Stop" ] )
    if ( "Stop" in Settings [ "Menu" ] ) :
      stopAction    . setIcon ( QIcon ( ActualFile ( Settings [ "Menu" ] [ "Stop" ] ) ) )
    stopAction    . triggered . connect ( self . Stop )
    # stopAction    . setVisible ( False )
    self . Actions [ "Stop"  ] = stopAction
    # Exit
    exitAction    = menu . addAction ( Translations [ "Menu::Quit" ] )
    if ( "Quit" in Settings [ "Menu" ] ) :
      exitAction    . setIcon ( QIcon ( ActualFile ( Settings [ "Menu" ] [ "Quit" ] ) ) )
    exitAction    . triggered . connect ( self . Quit )
    self . Actions [ "Exit"  ] = exitAction
    #
    self . setContextMenu ( menu )

  def languageMenu ( self , menu ) :
    global Settings
    global Locales
    global Translations
    #
    LANG = Settings [ "Language" ]
    #
    langMenu  = menu      . addMenu ( Translations [ "Menu::Language" ] )
    langGroup = QActionGroup        ( langMenu                          )
    langGroup . setExclusive        ( True                              )
    langGroup . triggered . connect ( self . doLanguageTriggered        )
    #
    KEYs = Locales . keys ( )
    for K in KEYs :
      langAction = QAction   ( Locales [ K ]             ,
                               langMenu                  ,
                               checkable = True          ,
                               checked   = ( LANG == K ) )
      langAction . setData   ( K          )
      langMenu   . addAction ( langAction )
      langGroup  . addAction ( langAction )
    #
    self . Actions [ "Language"      ] = langMenu
    self . Actions [ "LanguageGroup" ] = langGroup
    return True

  def doLanguageTriggered ( self , action ) :
    global Settings
    global Locales
    global Translations
    Settings [ "Language" ] = action . data ( )
    Language     = Settings   [ "Language"            ]
    TRFILE       = f"locales/{Language}/translations.json"
    Translations = LoadJSON   ( ActualFile ( TRFILE ) )
    WriteSettings ( )
    # Configure Menu
    self . Menu = QMenu ( self . MyParent )
    self . PrepareMenu  ( self . Menu     )
    if ( CpuProfilerSettings [ "Running" ] ) :
      self . Actions [ "Start" ] . setVisible ( False )
      self . Actions [ "Stop"  ] . setVisible ( True  )
      self . Actions [ "Exit"  ] . setVisible ( False )
    else :
      self . Actions [ "Start" ] . setVisible ( True  )
      self . Actions [ "Stop"  ] . setVisible ( False )
      self . Actions [ "Exit"  ] . setVisible ( True  )
    return True

  def hostsMenu ( self , menu ) :
    global Settings
    global Hosts
    global Translations
    if ( len ( Hosts ) <= 0 ) :
      return False
    #
    hostMenu  = menu . addMenu      ( Translations [ "Menu::Machines" ] )
    hostGroup = QActionGroup        ( hostMenu                          )
    hostGroup . setEnabled          ( True                              )
    hostGroup . setExclusive        ( False                             )
    hostGroup . triggered . connect ( self . doHostTriggered            )
    #
    for H in Hosts :
      hostAction = QAction   ( H [ "Hostname" ] , hostMenu )
      hostMenu   . addAction ( hostAction )
      hostGroup  . addAction ( hostAction )
    #
    self . Actions [ "Machines"      ] = hostMenu
    self . Actions [ "MachinesGroup" ] = hostGroup
    return True

  def doHostTriggered           ( self , action    ) :
    global Settings
    global Hosts
    machineName = action . text (                  )
    Myself      = ActualFile    ( "CpuProfiler.py" )
    CMD         = f"start pythonw {Myself} --machine=\"{machineName}\""
    # CMD         = f"{Myself} --machine=\"{machineName}\""
    os . system                 ( CMD              )
    return True

  def debuggerMenu ( self , menu ) :
    global Settings
    global Hosts
    global Translations
    DBG           = Settings [ "Debug" ]
    debugMenu     = menu      . addMenu ( Translations [ "Menu::Debugger" ] )
    debugGroup    = QActionGroup ( debugMenu )
    debugGroup    . setExclusive(True)
    debugGroup    . triggered . connect ( self . doDebugTriggered )
    # NOTSET
    dbgAction     = QAction      ( "Nothing" , debugMenu , checkable= True , checked = ( "NOTSET" == DBG ) )
    debugMenu     . addAction    ( dbgAction )
    debugGroup    . addAction    ( dbgAction )
    # DEBUG
    dbgAction     = QAction      ( "Debug" , debugMenu , checkable= True , checked = ( "DEBUG" == DBG ) )
    debugMenu     . addAction    ( dbgAction )
    debugGroup    . addAction    ( dbgAction )
    # INFO
    dbgAction     = QAction      ( "Information" , debugMenu , checkable= True , checked = ( "INFO" == DBG ) )
    debugMenu     . addAction    ( dbgAction )
    debugGroup    . addAction    ( dbgAction )
    # WARNING
    dbgAction     = QAction      ( "Warning" , debugMenu , checkable= True , checked = ( "WARNING" == DBG ) )
    debugMenu     . addAction    ( dbgAction )
    debugGroup    . addAction    ( dbgAction )
    # ERROR
    dbgAction     = QAction      ( "Error" , debugMenu , checkable= True , checked = ( "ERROR" == DBG ) )
    debugMenu     . addAction    ( dbgAction )
    debugGroup    . addAction    ( dbgAction )
    # CRITICAL
    dbgAction     = QAction      ( "Critical" , debugMenu , checkable= True , checked = ( "CRITICAL" == DBG ) )
    debugMenu     . addAction    ( dbgAction )
    debugGroup    . addAction    ( dbgAction )
    #
    self . Actions [ "Debugger"      ] = debugMenu
    self . Actions [ "DebuggerGroup" ] = debugGroup
    return True

  def doDebugTriggered ( self , action ) :
    Logger = logging . getLogger ( )
    DMSG   = action . text ( )
    Logger . info ( f"Switch logging to {DMSG}" )
    if   ( "Nothing"     == DMSG ) :
      Logger . setLevel ( logging . NOTSET   )
      Settings [ "Debug" ] = "NOTSET"
    elif ( "Debug"       == DMSG ) :
      Logger . setLevel ( logging . DEBUG    )
      Settings [ "Debug" ] = "DEBUG"
    elif ( "Information" == DMSG ) :
      Logger . setLevel ( logging . INFO     )
      Settings [ "Debug" ] = "INFO"
    elif ( "Warning"     == DMSG ) :
      Logger . setLevel ( logging . WARNING  )
      Settings [ "Debug" ] = "WARNING"
    elif ( "Error"       == DMSG ) :
      Logger . setLevel ( logging . ERROR    )
      Settings [ "Debug" ] = "ERROR"
    elif ( "Critical"    == DMSG ) :
      Logger . setLevel ( logging . CRITICAL )
      Settings [ "Debug" ] = "CRITICAL"
    WriteSettings ( )
    return True

  def onTrayActivated ( self , reason ) :
    if ( reason == 3 ) :
      self . Menu . exec_ ( QCursor . pos ( ) )

  def Start ( self ) :
    StartRunning ( )

  def Stop ( self ) :
    StopRunning ( )

  def Quit ( self ) :
    self . hide ( )
    qApp . quit ( )

def CpuDaemonMain ( ) :
  global Ghost
  global CpuProfilerSettings
  global Settings
  global Tray
  Logger    = logging . getLogger (                         )
  Ghost     = Daemon              ( CpuProfilerSettings     )
  Path      = CpuProfilerSettings [ "Path"     ]
  Root      = CpuProfilerSettings [ "Root"     ]
  TZ        = CpuProfilerSettings [ "TimeZone" ]
  Username  = Settings            [ "Username" ]
  Password  = Settings            [ "Password" ]
  ConfigureCpu                    ( { "Daemon"   : Ghost       ,
                                      "Stop"     : StopRunning ,
                                      "Path"     : Path        ,
                                      "TimeZone" : TZ          ,
                                      "Root"     : Root        ,
                                      "Username" : Username    ,
                                      "Password" : Password    ,
                                      "Verify"   : False       ,
                                      } )
  # 啟動網路效能數據提供
  threading . Thread              ( target = RunCpuFeeder   ) . start ( )
  # 設定選單
  Tray      . Actions [ "Start" ] . setVisible ( False )
  Tray      . Actions [ "Stop"  ] . setVisible ( True  )
  Tray      . Actions [ "Exit"  ] . setVisible ( False )
  # 執行機器效能監視器
  Ghost     . run                 (                         )
  Logger    . debug               ( "Complete CPU Profiler" )

def ConfigureCpuProfiler ( ) :
  #
  global Settings
  global Locales
  global Translations
  global Hosts
  global Tray
  #
  Settings     = LoadJSON   ( ActualFile ( "settings.json"        ) )
  Locales      = LoadJSON   ( ActualFile ( "locales/locales.json" ) )
  Settings [ "Root" ] = os . path . dirname ( os . path . abspath (__file__) )
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
  CpuProfilerSettings [ "Root" ] = Settings [ "Root" ]
  # 讀取翻譯檔
  Language     = Settings   [ "Language"                            ]
  TRFILE       = f"locales/{Language}/translations.json"
  Translations = LoadJSON   ( ActualFile ( TRFILE                 ) )
  # 設定除錯機制
  isConsole   = False
  if ( Settings [ "Console" ] > 0 ) :
    isConsole = True
  ConfigureDebugger                ( {
    "Debug"   : Settings [ "Debug" ] ,
    "LOG"     : Settings [ "LOG"   ] ,
    "Console" : isConsole            ,
  } )
  return True

def CpuProfilerMain ( ) :
  #
  global Settings
  global Locales
  global Translations
  global Hosts
  global Tray
  #
  ConfigureCpuProfiler ( )
  # 啟動選單
  app      = QApplication    ( sys . argv                                   )
  trayMenu = CpuProfilerMenu ( QIcon ( ActualFile ( Settings [ "Icon" ] ) ) )
  trayMenu . show            (                                              )
  Tray     = trayMenu
  # 啟動機器效能監視器
  threading . Thread         ( target = CpuDaemonMain ) . start ( )
  sys      . exit            ( app . exec_ ( )                              )
  # 結束
  return True

def CpuProfilerView ( ) :
  #
  global Settings
  global Locales
  global Translations
  global Hosts
  global Tray
  #
  ConfigureCpuProfiler ( )
  #
  app      = QApplication               ( sys . argv      )
  # 設定資料
  settings =                            {                 }
  screen   = app    . primaryScreen     (                 )
  rect     = screen . availableGeometry (                 )
  size     = rect   . size              (                 )
  settings [ "Width"  ] = size . width  (                 )
  settings [ "Height" ] = size . height (                 )
  settings [ "Path"   ] = "D:/Temp/CPU/Cuisine"
  settings [ "URL"    ] = "http://192.168.0.98:16319"
  # 啟動CPU Chart
  w        = CpuChart                   ( settings        )
  w        . startup                    (                 )
  sys      . exit                       ( app . exec_ ( ) )
  return True

def SayCpuProfilerHelp ( ) :
  print ( "CpuProfiler.py -v (--help Help) -m MachineName (--machine=MachineName)" )
  return

def GetOptions ( argv ) :
  global Machine
  try :
    opts, args = getopt . getopt ( argv , "m:h" , [ "machine=" , "help" ] )
  except getopt . GetoptError :
    SayCpuProfilerHelp ( )
    sys . exit ( 2 )
  for opt , arg in opts :
    if opt in ( "-v" , "--help" ) :
      SayCpuProfilerHelp ( )
      sys . exit ( 0 )
    elif opt in ( "-m" , "--machine" ) :
      Machine = arg
  return True

if __name__ == '__main__':
  GetOptions        ( sys . argv [ 1: ] )
  if                ( None == Machine   ) :
    CpuProfilerMain (                   )
  else :
    CpuProfilerView (                   )
