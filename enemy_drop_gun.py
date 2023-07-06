import unrealsdk as unrealsdk
from unrealsdk import *
from typing import List, Tuple
import sys

class EnemyDeathHandler:
    def __init__(self, enemy):
        self.enemy = enemy
        self.world = unrealsdk.GetEngine().GameViewport.World

    def __GetGame(self) -> str:
        """Returns \'Wonderlands\' or \'Borderlands3\' depending on the game."""
        return sys.executable.split('\\')[-1].replace('.exe','')

    def __get_enemy_weapons(self) -> List:
        weapons = []
        try:
            for slot in self.enemy.ActiveWeaponSlots:
                wep = self.enemy.GetWeapon(slot)
                if wep != None:
                    weapons.append(wep)
                    unrealsdk.Log(f'Found weapon: {wep.Name}')
        except:
            unrealsdk.Log('Failed to get enemy weapons')
        return weapons

    def __weapon_to_data(self, weapon: unrealsdk.UObject) -> Tuple:
        weapon_data = weapon.BalanceStateComponent
        out_data = [
            weapon_data.GameStage,
            weapon_data.InventoryData,
            weapon_data.InventoryBalanceData,
            weapon_data.ManufacturerData,
            weapon_data.PartList,
            weapon_data.GenericPartList,
            weapon_data.AdditionalData,
            weapon_data.CustomizationPartList,
            weapon_data.ReRollCount,
            True
        ]
        if self.__GetGame() == 'Wonderlands':
            out_data.append(int(weapon_data.OverpowerLevel))
        else:
            mayhem_lvl = int(unrealsdk.FindAll('MayhemModeFunctionLibrary')[0].GetMayhemLevel(self.world))
            if mayhem_lvl > 0:
                mayhem_parts = unrealsdk.FindAll('OakWeaponMayhemPartData')
                for part in mayhem_parts:
                    if part.MayhemLevel == mayhem_lvl:
                        out_data[5].append(part)
                        break
        return tuple(out_data)

    def __GetLocation(self) -> Tuple[float, float, float]:
        location_vector = self.enemy.CapsuleComponent.RelativeLocation
        return (location_vector.X, location_vector.Y, location_vector.Z)

    def drop_weapons(self) -> List[unrealsdk.UObject]:
        enemy_weapons = self.__get_enemy_weapons()
        out_weapons = []
        if len(enemy_weapons) == 0:
            return enemy_weapons
        else:
            spawn_location = self.__GetLocation()
            for weapon in enemy_weapons:
                weapon_data = self.__weapon_to_data(weapon)
                pickup = self.world.CreateInventory(self.world, True, spawn_location, weapon_data)
                out_weapons.append(pickup)
        return out_weapons

def on_enemy_death(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
    unrealsdk.Log("Enemy Died")
    enemy = caller.GetOwner()
    if enemy == unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.Pawn:
        return True
    dropped_wep = EnemyDeathHandler(enemy).drop_weapons()
    unrealsdk.Log(f'Dropped weapons: {dropped_wep}')
    return True
unrealsdk.RunHook('/Script/GbxGameSystemCore.DamageComponent.OnHealthResourceNowDepleted', 'EnemyDeathDropItem', on_enemy_death)
def disable(a=(), b=(), c=()):
    unrealsdk.RemoveHook('/Script/GbxGameSystemCore.DamageComponent.OnHealthResourceNowDepleted', 'EnemyDeathDropItem')
    unrealsdk.Log("Enemy drop gun disabled")
unrealsdk.RegisterConsoleCommand("disable", disable)
