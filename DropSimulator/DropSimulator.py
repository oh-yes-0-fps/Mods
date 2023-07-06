from __future__ import annotations
try:
    import Mods.bl3_typing as bl3
except ImportError:
    pass
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Editor Only
import unrealsdk
from unrealsdk import *
# from Mods.Util.Data_Deriving import Get_cls_instance, GetObject
import json
import sys


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
    # return unrealsdk.FindClass(cls_name).ClassDefaultObject


# pyexec DropSimulator/DropSimulator.py

ITEMS_TO_SPAWN = 20

jdata = []

ITEMPOOL: bl3.UItemPoolData = GetObject(
    "ItemPoolData", "/Game/GameData/Loot/ItemPools/ItemPool_DiamondKeyChest.ItemPool_DiamondKeyChest")

PLAYER: bl3.AOakCharacter_Player = unrealsdk.GetEngine(
).GameInstance.LocalPlayers[0].PlayerController.Pawn

PATTERN: bl3.ULootSpawnPatternData = GetObject(
    "LootSpawnPatternData", "/Game/GameData/Loot/SpawnPatterns/LootSpawnPattern_Default.LootSpawnPattern_Default")


def ActorToData(item_data: unrealsdk.UObject) -> list:
    """Converts an actor to a list"""

    def GetGame() -> str:
        """Returns \'Wonderlands\' or \'Borderlands3\' depending on the game."""
        return sys.executable.split('\\')[-1].replace('.exe', '')

    def ObjectToStr(obj: unrealsdk.UObject) -> str:
        """Converts an object to a string"""
        return f'{obj.Class.Name}|{obj.Outer.Name}.{obj.Name}'

    def __lst_handler(lst: list[unrealsdk.UObject]) -> list:
        """Converts a list of objects to a list of strings"""
        lst_str = []
        for i in lst:
            lst_str.append(ObjectToStr(i))
        return lst_str
    save_data = {
        "Level": int(item_data.GameStage),
        "InvData": ObjectToStr(item_data.InventoryData),
        "Balance": ObjectToStr(item_data.InventoryBalanceData),
        "ManuData": ObjectToStr(item_data.ManufacturerData),
        "Parts": __lst_handler(item_data.PartList),
        "GParts": __lst_handler(item_data.GenericPartList), }
    if GetGame() == 'Wonderlands':
        save_data.append(int(item_data.OverpowerLevel))
    if len(save_data['Parts']) == 0 and len(save_data['GParts']) == 0:
        return
    global jdata
    jdata.append(save_data)


class dropper:
    def __init__(self) -> None:
        self.actor = PLAYER
        self.bone = self.actor.ConnectEffectBoneName
        self.static: bl3.UOakBlueprintLibrary = Get_cls_instance(
            "OakBlueprintLibrary")
        self.itempool = ITEMPOOL
        self.pattern = PATTERN

    def spawn(self) -> None:
        self.static.SpawnLoot(self.actor, self.itempool,
                              self.bone, self.pattern, [], 0, False)


i_dropper = dropper()


def spawn_wrapper(a=(), b=(), c=()) -> None:
    global jdata
    jdata = []
    unrealsdk.RunHook(
        "/Game/Pickups/_Shared/_Design/BP_OakInventoryItemPickup.BP_OakInventoryItemPickup_C.UserConstructionScript", "item_Spawned", item_logger)
    for _ in range(ITEMS_TO_SPAWN):
        i_dropper.spawn()
    unrealsdk.RemoveHook(
        "/Game/Pickups/_Shared/_Design/BP_OakInventoryItemPickup.BP_OakInventoryItemPickup_C.UserConstructionScript", "item_Spawned")
    with open("Mods\\DropSimulator\\DropSimulator.json", "w") as f:
        json.dump(jdata, f, indent=4)


def item_logger(caller: bl3.ABP_OakInventoryItemPickup_C, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
    caller.SetLifeSpan(0.00001)
    ActorToData(caller.CachedInventoryBalanceComponent)


def LogChance(a=(), b=(), c=()) -> None:
    with open("Mods\\DropSimulator\\DropSimulator.json", "r") as f:
        data = json.load(f)
    chance_dict = {}
    for i in data:
        balance = i['Balance'].split('.')[-1]
        if balance in chance_dict:
            chance_dict[balance] += 1
        else:
            chance_dict[balance] = 1
    for j in chance_dict:
        unrealsdk.Log(f"  {j}: {(chance_dict[j] / len(data)):.2f}")


unrealsdk.RemoveConsoleCommand("spawn")
unrealsdk.RegisterConsoleCommand("spawn", spawn_wrapper)
unrealsdk.RemoveConsoleCommand("LogChance")
unrealsdk.RegisterConsoleCommand("LogChance", LogChance)
