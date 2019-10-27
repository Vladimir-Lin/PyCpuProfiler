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






def CpuProfilerMain ( ) :
  print ( "Start" )
  pass

if __name__ == '__main__':
  CpuProfilerMain ( )
