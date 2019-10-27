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

include ($${PWD}/32x32/32x32.pri)
include ($${PWD}/64x64/64x64.pri)
include ($${PWD}/128x128/128x128.pri)
include ($${PWD}/others/others.pri)
include ($${PWD}/svg/svg.pri)
