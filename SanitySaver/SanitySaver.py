import unrealsdk as unrealsdk
from unrealsdk import *
import json
from os.path import exists
import sys
from typing import Callable, List
from Mods.Util.SaveGameInterface import SaveGame

DEBUG = True


class ParentSaveManager:

    def __init__(self):
        self.player = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.Pawn

    def ActorToData(self, item: unrealsdk.UObject) -> list:
        """Converts an actor to a list"""
        def __lst_handler(lst: list[unrealsdk.UObject]) -> list:
            """Converts a list of objects to a list of strings"""
            lst_str = []
            for i in lst:
                lst_str.append(self.ObjectToStr(i))
            return lst_str
        try:
            item_data = item.BalanceStateComponent
        except:
            item_data = item.InventoryBalanceState
        save_data = [
            int(item_data.GameStage),
            self.ObjectToStr(item_data.InventoryData),
            self.ObjectToStr(item_data.InventoryBalanceData),
            self.ObjectToStr(item_data.ManufacturerData),
            __lst_handler(item_data.PartList),
            __lst_handler(item_data.GenericPartList),
            list(item_data.AdditionalData),
            __lst_handler(item_data.CustomizationPartList),
            int(item_data.ReRollCount),
            False]
        if self.GetGame() == 'Wonderlands':
            save_data.append(int(item_data.OverpowerLevel))
        with open('Mods\\SanitySaver\\parts.json', 'r') as f:
            base_parts = set(json.load(f))
        part_classes = set()
        if len(save_data[4]) == 0 and len(save_data[5]) == 0:
            return None
        for i in save_data[4]:
            part_classes.add(i.split('|')[0])
            if i not in base_parts:
                unrealsdk.Log(f'unknow part {i} found on {save_data[2]}')
                return save_data
        if len(list(part_classes)) != 1:
            unrealsdk.Log(f'part class mismatch {part_classes} on {save_data[2]}')
            return save_data
        for i in save_data[5]:
            if i not in base_parts:
                unrealsdk.Log(f'unknow part {i} found on {save_data[2]} for anoints')
                return save_data
        return None

    def DataToActor(self, item_data: list) -> unrealsdk.UObject:
        """Converts a saved item list to an actor"""
        def __lst_handler(lst: list[str]) -> list[unrealsdk.UObject]:
            """Converts a list of strings to a list of objects"""
            lst_obj = []
            for i in lst:
                lst_obj.append(self.GetObject(i.split('|')[0], i.split('|')[1]))
            return lst_obj
        static = self.Get_cls_instance('InventoryBlueprintLibrary')
        save_struct = [
            item_data[0],
            self.GetObject(item_data[1].split('|')[0], item_data[1].split('|')[1]),
            self.GetObject(item_data[2].split('|')[0], item_data[2].split('|')[1]),
            self.GetObject(item_data[3].split('|')[0], item_data[3].split('|')[1]),
            __lst_handler(item_data[4]),
            __lst_handler(item_data[5]),
            item_data[6],
            __lst_handler(item_data[7]),
            item_data[8],
            item_data[9]]
        if self.GetGame() == 'Wonderlands':
            save_struct.append(item_data[10])
        return static.BuildInventory(self.GetWorld(), False, self.GetLocation(), tuple(save_struct))

    def Get_cls_instance(self,cls_name: str) -> unrealsdk.UObject:
        """Returns the default object of the class"""
        return unrealsdk.FindAll(cls_name)[0]

    def GetWorld(self) -> unrealsdk.UObject:
        return unrealsdk.GetEngine().GameViewport.World

    def GetLocation(self) -> tuple[float, float, float]:
        """
        Returns the location of the player.
        """
        pawn = self.GetPlayerController().Pawn.CapsuleComponent.RelativeLocation
        return (pawn.X, pawn.Y, pawn.Z)

    def GetPlayerController(self) -> unrealsdk.UObject:
        """Returns the player controller"""
        PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        return PC

    def GetObject(self, cls_name: str, obj_path: str) -> unrealsdk.UObject:
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
        return None

    def GetGame(self) -> str:
        """Returns \'Wonderlands\' or \'Borderlands3\' depending on the game."""
        return sys.executable.split('\\')[-1].replace('.exe','')

    def ObjectToStr(self,obj: unrealsdk.UObject) -> str:
        """Converts an object to a string"""
        return f'{obj.Class.Name}|{obj.Outer.Name}.{obj.Name}'


class PlayerSaveManager(ParentSaveManager):
    def __init__(self):
        # self.player = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.Pawn
        self.save_dct = {str: {'Currency': {'Money': 0, 'Eridium': 0},'Equipped': [],'Inventory': [],}}
        self.save = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.CurrentSaveGame
        self.json_path = '.\\Mods\\SanitySaver\\player_save.json'
        super().__init__()

    def EquippedItemList(self) -> list[unrealsdk.UObject]:
        """Returns a list of all items equipped on the player"""
        pawn = self.player
        slot_list = pawn.EquipmentSlots
        item_lst = []
        for i in slot_list:
            equipped_actor = pawn.GetEquippedInventoryForSlot(i)
            if equipped_actor:
                item_lst.append(equipped_actor)
        return item_lst

    def AllItemList(self) -> list[unrealsdk.UObject]:
        """Returns a list of all items in the players inventory"""
        pawn = self.player
        inv_list = pawn.InventoryList.InventoryList.Items
        item_lst = []
        for i in range(len(list(inv_list))):
            if inv_list[i].StoredActor != None:
                item_lst.append(inv_list[i].StoredActor)
        return item_lst

    def GetCurrencyData(self) -> dict[str,int]:
        pawn = self.player
        inv_list = pawn.InventoryList.InventoryList.Items
        currency_dct = {'Money': 0, 'Eridium': 0}
        for i in inv_list:
            if i.StoredActor == None:
                if i.BaseCategoryDefinition.Name == 'InventoryCategory_Money':
                    currency_dct['Money'] = i.Quantity
                elif i.BaseCategoryDefinition.Name == 'InventoryCategory_Eridium':
                    currency_dct['Eridium'] = i.Quantity
        return currency_dct

    def WriteCurrencyData(self, dct: dict[str,int]) -> None:
        pawn = self.player
        inv_list = pawn.InventoryList
        money_category = self.GetObject('InventoryCategoryData','/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money')
        inv_list.AddExternalItem(money_category, None, int(dct['Money']), False, False, False, 0, True)
        eridium_category = self.GetObject('InventoryCategoryData','/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium')
        inv_list.AddExternalItem(eridium_category, None, int(dct['Eridium']), False, False, False, 0, True)

    def ExtractSave(self) -> None:
        save_id = str(self.save.SaveGameId)
        def RemoveInventoryDupes(self: PlayerSaveManager) -> list[unrealsdk.UObject]:
            """Removes Equipped items from the AllItemList"""
            fixed_inv_lst = []
            for i in self.AllItemList():
                if i not in self.EquippedItemList():
                    fixed_inv_lst.append(i)
            return fixed_inv_lst
        AllItemList_var = []
        for item in RemoveInventoryDupes(self):
            inv_data = self.ActorToData(item)
            if inv_data != None:
                AllItemList_var.append(inv_data)
        EquippedItemList_var = []
        for item in self.EquippedItemList():
            eqp_data = self.ActorToData(item)
            if eqp_data != None:
                EquippedItemList_var.append(eqp_data)
        save_data = {'Equipped': EquippedItemList_var,'Inventory': AllItemList_var}#'Currency': self.GetCurrencyData(),
        SaveGame['Items'] = save_data

    def ApplySave(self) -> None:
        player = self.player
        def __add_item(item_data: list) -> None:
            """Adds an item to the player's inventory"""
            if DEBUG:
                unrealsdk.Log('DEBUG: Adding item')
            try:
                InvCategory = item.BalanceStateComponent.InventoryData.InventoryCategory
            except AttributeError:
                InvCategory = item.InventoryBalanceState.InventoryData.InventoryCategory
            player.InventoryList.AddExternalItem(InvCategory,item,1,False,False,False,0,True)
        if 'Items' in SaveGame:
            if DEBUG:unrealsdk.Log('DEBUG: found save data')
            save_data = SaveGame['Items']
            for item in save_data['Equipped']:
                item = self.DataToActor(item)
                __add_item(item)
            for item in save_data['Inventory']:
                item = self.DataToActor(item)
                __add_item(item)
            return
        else:
            unrealsdk.Log('No save data found')
            self.ExtractSave()
            return




def Register_CharacterLoadLate(func: Callable, times_needed_to_be_called=1) -> None:
    """Registers a function to be called after the player is loaded"""
    global _times_called
    _times_called = 1
    global _times_needed_to_be_called
    _times_needed_to_be_called = times_needed_to_be_called
    def __delayedtrigger(a=(), b=(), c=()):
        global _times_called
        global _times_needed_to_be_called
        if _times_called == _times_needed_to_be_called:
            unrealsdk.Log(f'{func.__name__} called')
            func()
            unrealsdk.RemoveHook('/Script/OakGame.OakCharacter_Player.GetPet', f'Delayed{func.__name__}')
            unrealsdk.RemoveHook('/Game/PlayerCharacters/Beastmaster/_Shared/_Design/Character/BPChar_Beastmaster.BPChar_Beastmaster_C.GetPet', f'Delayed{func.__name__}FL4K')
            _times_called = 0
        else:
            _times_called += 1  
        return True
    def __LoadListener(a=(), b=(), c=()):
        unrealsdk.RunHook('/Script/OakGame.OakCharacter_Player.GetPet', f'Delayed{func.__name__}', __delayedtrigger)
        unrealsdk.RunHook('/Game/PlayerCharacters/Beastmaster/_Shared/_Design/Character/BPChar_Beastmaster.BPChar_Beastmaster_C.GetPet', f'Delayed{func.__name__}FL4K', __delayedtrigger)
        return True
    unrealsdk.RunHook('/Script/OakGame.OakCharacter_Player.ShowConnectEffect', 'StartListening_Sanity', __LoadListener)



#############################################################################

def ApplySave():
    unrealsdk.Log('Applying Save')
    PlayerSaveManager().ApplySave()
    unrealsdk.RunHook('/Script/OakGame.OakCharacter.RemovingFromInventory', 'DropItem', ExtractSaveWrapper_item)
    unrealsdk.RunHook('/Script/OakGame.OakCharacter.AddedToInventory', 'AddItem', ExtractSaveWrapper_item)
    unrealsdk.RunHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade', 'quit', ExtractSaveWrapper_quit)
Register_CharacterLoadLate(ApplySave, 40)

def ExtractSaveWrapper_item(a=(), b=(), c=()):
    global num_of_ticks
    num_of_ticks = 0
    def __delayedtrigger(a=(), b=(), c=()):
        global num_of_ticks
        if num_of_ticks == 10:
            unrealsdk.Log('Extracting Save; Reason: Item')
            PlayerSaveManager().ExtractSave()
            unrealsdk.RemoveHook('/Script/Engine.Actor.ReceiveTick', 'DelayExtractSave')
        else:
            num_of_ticks += 1
        return True
    unrealsdk.RunHook('/Script/Engine.Actor.ReceiveTick', 'DelayExtractSave', __delayedtrigger)
    return True

def ExtractSaveWrapper_quit(a=(), b=(), c=()):
    unrealsdk.Log('Extracting Save; Reason: Quit')
    PlayerSaveManager().ExtractSave()
    unrealsdk.RemoveHook('/Script/OakGame.OakCharacter.RemovingFromInventory', 'DropItem')
    unrealsdk.RemoveHook('/Script/OakGame.OakCharacter.AddedToInventory', 'AddItem')
    unrealsdk.RemoveHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade', 'quit')
    return True




