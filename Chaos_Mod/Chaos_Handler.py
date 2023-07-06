
import unrealsdk as unrealsdk
from unrealsdk import *
#pyexec Chaos_Mod\Chaos_Handler.py

def test_modifier_func():
    from Mods.Chaos_Mod.modifiers.slippery import modifier
    test_modifier = modifier()
    unrealsdk.Log("Modifier name: " + test_modifier.name)
    unrealsdk.Log("Modifier description: " + test_modifier.description)
    test_modifier.activate()
    def deactivate(a=(),b=(),c=()):
        test_modifier.deactivate()
        unrealsdk.Log("Modifier deactivated")
    unrealsdk.RemoveConsoleCommand("deactivate")
    unrealsdk.RegisterConsoleCommand("deactivate", deactivate)

if __name__ == '__main__':
    test_modifier_func()
