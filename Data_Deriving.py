from typing import Any, Optional, Tuple
import sys
import unrealsdk as unrealsdk
from unrealsdk import *

def logtype(obj: Any) -> str:
    """logs the type of the object"""
    unrealsdk.Log(type(obj))
    return type(obj)

import timeit
def logtimetaken(func) -> None:
    """logs the time taken to run a function"""
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        end = timeit.default_timer()
        unrealsdk.Log(f'    {func.__name__} took {end - start} seconds')
    return wrapper

def GetPlayerController() -> unrealsdk.UObject:
    """Returns the player controller"""
    PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
    return PC

def GetObject(cls_name: str, obj_path: str) -> unrealsdk.UObject:
    """
    For some reason FindObject takes forever to run so i use this
    \nslow function to get an object by name, can also be unsafe.
    """
    Objects = unrealsdk.FindAll(cls_name)
    obj_pkg = obj_path.split('.')[0]
    obj_name = obj_path.split('.')[1]
    for obj in Objects:
        if obj_name == obj.Name and obj_pkg in str(obj.Outer):
            return obj
    unrealsdk.Log(f'{obj_name} not found!')
    return

def Get_cls_instance(cls_name: str) -> unrealsdk.UObject:
    """Returns the default object of the class"""
    return unrealsdk.FindAll(cls_name)[0]

def GetHeldWeapon() -> unrealsdk.UObject:
    """Returns the weapon the player is holding."""
    return GetPlayerController().Pawn.GetActiveWeapon(0)

def modifier_type_resolver(default=1.0,preadd=0.0,pos_scale=0.0, neg_scale=0.0,simple_scale=1.0, postadd=0.0) -> float:
    """
    Takes up to 6 arguments and returns a float value of the calculated value of the modifier.
    """
    return (default + preadd) * ((1 + pos_scale)/(1 - neg_scale)) * (simple_scale) + postadd

def GetWorld() -> unrealsdk.UObject:
    return unrealsdk.GetEngine().GameViewport.World

def GetCurrentLevelName() -> str:
    Static = Get_cls_instance('GbxGameplayStatics')
    return Static.GetCurrentLevelName(GetWorld(), False)

def GetMayhemLevel() -> int:
    Static = Get_cls_instance('MayhemModeFunctionLibrary')
    return Static.GetMayhemLevel(GetWorld())

#somewhat redundant having all 3 but why not
def GetGame() -> str:
    """Returns \'Wonderlands\' or \'Borderlands3\' depending on the game."""
    return sys.executable.split('\\')[-1].replace('.exe','')

def wonderlands() -> bool:
    """Returns True if sdk is running in Wonderlands."""
    if GetGame() == 'Wonderlands':
        return True
    return False

def borderlands3() -> bool:
    """Returns True if sdk is running in Borderlands 3."""
    if GetGame() == 'Borderlands3':
        return True
    return False

#uses native datatable function to get value from datatable
def GetDatatableValue(datatable: unrealsdk.UObject, row: str, column: Optional[str], pawn=GetPlayerController().Pawn) -> float:
    """
    Gets value from a data table entry.
    """
    static = Get_cls_instance('GbxDataTableFunctionLibrary')
    handle = (datatable,row,column)
    out = static.GetDataTableValueFromHandle(handle,pawn,0.0)[0]
    return out

#uses native blueprint function to get value from attribute
def GetAttValue(att_obj: unrealsdk.UObject, pawn=GetPlayerController().Pawn) -> float:
    """
    Returns the value of the attribute att_name for the player_bpchar.
    """
    statics = Get_cls_instance('GbxAttributeFunctionLibrary')
    att_value = statics.GetValueOfAttribute(att_obj, pawn, 0)
    return att_value

#native function wasn't working for me so I made my own
def Query_Statuseffect(SE_name: str, return_bool=False, pawn=GetPlayerController().Pawn) -> Any:
    SE_Manager = pawn.StatusEffectManagerComponent
    wanted_se_index = 0
    found_se = False
    for i in SE_Manager.InstanceStacks:
        if SE_name == i.StatusEffectData.Name:
            found_se = True
            break
        wanted_se_index += 1
    if not found_se:
        if return_bool:
            return False
        else:
            return 0
    instances = SE_Manager.InstanceStacks[wanted_se_index].Instances
    num_of_instances = 0
    for inst in instances:
        num_of_instances += 1
    if return_bool:
        return num_of_instances > 0
    return num_of_instances

def CurrMoveSpeed(absolue=False) -> float:
    """
    Has two modes, absolute and relative.(default is relative)\n
    Absolute mode returns the velocity of the player.\n
    Relative mode returns the velocity of the player relative to the default speed.
    """
    static = Get_cls_instance('KismetMathLibrary')
    movement_comp = GetPlayerController().Pawn.OakCharacterMovement
    vel_vector = movement_comp.Velocity
    base_walkspeed = movement_comp.MaxWalkSpeed.BaseValue
    vel_float = static.VSize((vel_vector.X,vel_vector.Y,vel_vector.Z))
    if absolue:
        return vel_float
    return vel_float/base_walkspeed

def GetCurveFloatValue(time: float, curve: unrealsdk.UObject) -> float:
    """
    Returns the value of the curve at time.
    """
    static = Get_cls_instance('GbxGameSystemCoreBlueprintLibrary')
    return static.GetCurveFloatValue(curve, time)

def Stop_Momentum() -> None:
    """
    Stops the player momentum.
    """
    movement_comp = GetPlayerController().Pawn.OakCharacterMovement
    movement_comp.StopMovementImmediately()
    return

def GetLocation() -> Tuple[float, float, float]:
    """
    Returns the location of the player.
    """
    pawn = GetPlayerController().Pawn.CapsuleComponent.RelativeLocation
    return (pawn.X, pawn.Y, pawn.Z)

def ConditionHandler(condition: unrealsdk.UObject, cond_args: list[Any]) -> bool:
    """
    Returns True if the condition is met.\n
    Pass in all the arguments needed in condition in order.
    """
    static = Get_cls_instance('GbxCondition')
    return static.K2_EvaluateCondition(condition, *cond_args)

def DropHeldWeapon() -> None:
    """Drops the currently held weapon."""
    return GetPlayerController().Pawn.DropCurrentWeapon()

def ToggleHud(caller: unrealsdk.UObject, function = (), params = ()) -> None:
    """
    toggles hud visibility
    stores current visibility in hud.bShowHud
    """
    unrealsdk.Log('Toggled Hud')
    pc = GetPlayerController()
    hud = pc.GetHUD()
    inverse_visibility = not hud.bShowHud
    hud.SetHUDVisible(pc, inverse_visibility)
    hud.bShowHud = inverse_visibility

def inventory_inspect() -> None:
    static=Get_cls_instance('InventoryBlueprintLibrary')
    pawn = GetPlayerController().Pawn
    invbalstate = static.GetInventoryBalanceState(pawn)

def respec(caller: unrealsdk.UObject, function = (), params = ()):
    amc = GetPlayerController().Pawn.AbilityManagerComponent
    amc.PlayerAbilityTree.PurchaseAbilityRespec()
    return True













########## Testing ##########
#pyexec Data_Deriving.py


def __Datatable_test():
    unrealsdk.Log('== Datatable_test ==')
    dt_obj = GetObject('DataTable', '/Game/Enemies/Skag/_Shared/_Design/Balance/Table_Skag_Balance_Unique.Table_Skag_Balance_Unique')
    row_name = 'TrialBoss'
    column_name = 'HealthMultiplier_01_Primary_9_07801BE24749AFC87299AD91E1B82E12'
    out_value = GetDatatableValue(dt_obj, row_name, column_name)
    unrealsdk.Log(f'    {out_value}')

def __Att_Value_Test():
    unrealsdk.Log('== Att_Value_Test ==')
    att_obj = GetObject('GbxAttributeData', '/Game/GameData/Weapons/Att_Weapon_Damage.Att_Weapon_Damage')
    out_value = GetAttValue(att_obj)
    unrealsdk.Log(f'    {out_value}')

def __Query_Statuseffect_Test():
    unrealsdk.Log('== Query_Statuseffect_Test ==')
    game = GetGame()
    if game == 'Wonderlands':
        Status_name = 'SE_Ring_Min_SpellCrit_Damage'
    elif game == 'Borderlands3':
        Status_name = 'StatusEffect_Generic_ConsecutiveHitsDmgStack'
    out_count = Query_Statuseffect(Status_name)
    out_bool = Query_Statuseffect(Status_name, return_bool=True)
    unrealsdk.Log(f'    count: {out_count}')
    unrealsdk.Log(f'    bool: {out_bool}')

def __get_mayhem_level_test():
    unrealsdk.Log('== get_mayhem_level_test ==')
    out_level = GetMayhemLevel()
    unrealsdk.Log(f'    {out_level}')

def __CurrMoveSpeed_test():
    unrealsdk.Log('== CurrMoveSpeed_Test ==')
    out_speed = CurrMoveSpeed()
    out_speed_abs = CurrMoveSpeed(True)
    unrealsdk.Log(f'    Relative: {out_speed}')
    unrealsdk.Log(f'    Absolute: {out_speed_abs}')

def __get_location_test():
    unrealsdk.Log('== get_location_test ==')
    out_location = GetLocation()
    unrealsdk.Log(f'    X: {out_location[0]}')
    unrealsdk.Log(f'    Y: {out_location[1]}')
    unrealsdk.Log(f'    Z: {out_location[2]}')

def __GetObject_test():
    unrealsdk.Log('== GetObject_test ==')
    obj_name = 'Att_Weapon_Damage'
    out_object = GetObject('GbxAttributeData', obj_name)
    unrealsdk.Log(f'    {out_object}')

def __FindObject_test():
    unrealsdk.Log('== FindObject_test ==')
    obj_name = '/Game/GameData/Weapons/Att_Weapon_Damage.Att_Weapon_Damage'
    out_object = unrealsdk.FindObject('GbxAttributeData', obj_name)
    unrealsdk.Log(f'    {out_object}')

if __name__ == '__main__':
    # logtimetaken(__Datatable_test)()
    # logtimetaken(__Att_Value_Test)()
    # logtimetaken(__Query_Statuseffect_Test)()
    # logtimetaken(__GamepathToObjectpath_Test)()
    # logtimetaken(__get_object_test)()
    # logtimetaken(__get_mayhem_level_test)()
    # logtimetaken(__CurrMoveSpeed_test)()
    # logtimetaken(__get_location_test)()
    # logtimetaken(__GetObject_test)()
    # logtimetaken(__FindObject_test)()
    #caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct
    # GetPlayerController().Pawn.ShowConnectEffect()
    pass
if __name__ == '__main__':
    unrealsdk.RemoveConsoleCommand('respec')
    unrealsdk.RegisterConsoleCommand('respec', respec)
    unrealsdk.RemoveConsoleCommand('ToggleHud')
    unrealsdk.RegisterConsoleCommand('ToggleHud', ToggleHud)