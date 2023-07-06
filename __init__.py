import unrealsdk as unrealsdk
from unrealsdk import *
# from os import getcwd
# from Mods.Item_Randomizer import item_randomizer
# from Mods.Skill_Randomizer import skill_randomizer
# from Mods.SanitySaver import SanitySaver
# from Mods.Combat_Logger import combat_logger
def log_call(caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct):
    # unrealsdk.Log(f'{caller} used {function} with {params}')
    unrealsdk.Log(f'func called')
    return True

def logkey(caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct):
    key = tuple(['N'])
    if unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.WasInputKeyJustPressed(key):
        unrealsdk.Log(f'Key Pressed')
    return True


# unrealsdk.RunHook("/Game/PlayerCharacters/Beastmaster/_Shared/_Design/Character/BPChar_Beastmaster.BPChar_Beastmaster_C.GetPet", "keytest", logkey)
# unrealsdk.RemoveHook("/Game/PlayerCharacters/Beastmaster/_Shared/_Design/Character/BPChar_Beastmaster.BPChar_Beastmaster_C.GetPet", "keytest")

# unrealsdk.RunHook('/Script/OakGame.ZoneMapViewer.LoadMapForLevel', 'test', log_call)


