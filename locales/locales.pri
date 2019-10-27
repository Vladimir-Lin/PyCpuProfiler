SOURCES += $${PWD}/*.php
SOURCES += $${PWD}/*.js
SOURCES += $${PWD}/*.css
SOURCES += $${PWD}/*.html
SOURCES += $${PWD}/*.txt
SOURCES += $${PWD}/*.json
SOURCES += $${PWD}/*.py
SOURCES += $${PWD}/*.pl
SOURCES += $${PWD}/*.rb
SOURCES += $${PWD}/*.rs
SOURCES += $${PWD}/*.bat

include ($${PWD}/en/en.pri)
include ($${PWD}/zh-TW/zh-TW.pri)
include ($${PWD}/zh-CN/zh-CN.pri)
include ($${PWD}/zh-HK/zh-HK.pri)
include ($${PWD}/ja-JP/ja-JP.pri)
