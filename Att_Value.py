import unrealsdk as unrealsdk
from unrealsdk import *


def GetPlayerController():
    PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
    #unrealsdk.Log(PC.Pawn)
    return PC

def Att_Value(att_name: str, player_bpchar: unrealsdk.UObject):
    """
    Returns the value of the attribute att_name for the player_bpchar.
    """
    attributes = unrealsdk.FindAll('GbxAttributeData')
    statics = unrealsdk.FindAll('GbxAttributeFunctionLibrary')[0]
    for att in attributes:
        if att_name == att.Name:
            att_obj = att
            break
    if att_obj is None:
        unrealsdk.Log(f'Attribute {att_name} not found!')
        return
    unrealsdk.Log(att_obj)
    unrealsdk.Log(statics)
    att_value = statics.GetValueOfAttribute(att_obj, player_bpchar, 0)
    return att_value


def main():
    att_obj_name = 'Att_RarityModifier_05_Legendary'
    PC = GetPlayerController()
    player_pawn = PC.Pawn
    out_value = Att_Value(att_obj_name, player_pawn)
    unrealsdk.Log(out_value)

main()
