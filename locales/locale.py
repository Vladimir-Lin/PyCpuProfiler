import os
import sys

pypath = os.path.dirname(os.path.abspath(__file__))
# pypath = os.path.abspath(os.path.join(pypath,".."))

twass = os.path.abspath(os.path.join(pypath,"zh-TW"))
cnass = os.path.abspath(os.path.join(pypath,"zh-CN"))

# 切換到簡體中文目錄
os . chdir ( cnass )
# 刪除所有檔案
cmds = "del *.json"
os.system ( cmds )
# 切換到選單目錄
os . chdir ( pypath )
# 複製繁體中文到簡體中文
cmds = "copy " + twass + "\\* " + cnass
os.system ( cmds )
# 切換到簡體中文目錄
os . chdir ( cnass )
os.system ( "TW2CN.exe --suffix json --all" )

print ( "Menu : Convert Traditional Chinese into Simplified Chinese" )
