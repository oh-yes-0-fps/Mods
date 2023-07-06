import unrealsdk as unrealsdk
from unrealsdk import *

def start(a=(),b=(),c=()):
    unrealsdk.SetConsoleLogLevel(8)
    unrealsdk.SetFileLogLevel(8)
    unrealsdk.LogAllCalls(True)

def stop(a=(),b=(),c=()):
    unrealsdk.SetConsoleLogLevel(4)
    unrealsdk.SetFileLogLevel(4)
    unrealsdk.LogAllCalls(False)

unrealsdk.RemoveConsoleCommand("start")
unrealsdk.RemoveConsoleCommand("stop")
unrealsdk.RegisterConsoleCommand("start", start)
unrealsdk.RegisterConsoleCommand("stop", stop)

