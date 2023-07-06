import unrealsdk as unrealsdk
from unrealsdk import *
from typing import List, Optional, Tuple
from functools import lru_cache
import threading




class randomizer:
    """
    Give this class a list of categories to whitelist.
    Extreme will make things more random, but will also make it more likely to crash.
    """
    def __init__(self, whitelist: List[str] = [], extreme = False) -> None:
        self.whitelist = whitelist
        self.extreme = extreme

    @property
    @lru_cache(maxsize=3)
    def categories(self) -> List:
        whitelist = self.whitelist
        """
        Gets category objects for filtering.
        
        Options: Artifacts, Assault Rifles, Class Mods, Grenade Mods, \n
        Heavy Weapons, Pistols, Shields, Shotguns,SMGs, Sniper Rifles.
        """
        avail_categories = list(unrealsdk.FindAll('GearBuilderCategoryData'))
        final_list = set()
        for cat in avail_categories:
            if cat.CategoryName in whitelist:
                final_list.add(cat)
        return final_list

    @property
    def rand_item_type(self):
        weapons = ['Assault Rifles', 'Pistols', 'SMGs', 'Shotguns', 'Sniper Rifles', 'Heavy Weapons']
        gear = ['Artifacts', 'Shields', 'Class Mods', 'Grenade Mods']
        whitelist = self.whitelist
        if len(whitelist) == 0:
            raise ValueError('No categories were given to the randomizer.')
        #if item in whitelist is in weapons and an item in whitelist is in gear, raise error
        if any(i in whitelist for i in weapons) and any(i in whitelist for i in gear):
            raise ValueError('Cannot randomize both weapons and gear.')
        if any(i in whitelist for i in weapons):
            return 'Weapon'
        else:
            return 'Gear'

    @lru_cache(maxsize=3)
    def __get_balances(self) -> List:
        """
        Finds all balances within the parameters of the whitelist.
        """
        all_bal = unrealsdk.FindAll('InventoryBalanceData')
        out_bal = []
        for bal in all_bal:
            if bal.GearBuilderCategory is None:
                continue
            if bal.GearBuilderCategory in self.categories:
                out_bal.append(bal)
        return out_bal

    @lru_cache(maxsize=None)
    def __get_parts(self) -> List:
        """
        Finds all parts within the parameters of the whitelist.
        """
        name_to_class = {
            'Artifacts' : ['BPInvPart_Artifact_C'],
            'Shields' : ['BPInvPart_Shield_C'],
            'Class Mods' : ['BPInvPart_ClassMod_C'],
            'Grenade Mods' : ['BPInvPart_GrenadeMod_C'],
            'Assault Rifles' : ['BPInvPart_AR_COV_C', 'BPInvPart_JAK_AR_C', 'BPInvPart_AR_DAL_C', 'BPInvPart_VLA_AR_C', 'BPInvPart_AR_TOR_C'],
            'Pistols' : ['BPInvPart_PS_COV_C', 'BPInvPart_Jakobs_Pistol_C', 'BPInvPart_Pistol_DAL_C', 'BPInvPart_PS_VLA_C', 'BPInvPart_PS_TOR_C','BPInvPart_PS_ATL_C','BPInvPart_PS_MAL_C','BPInvPart_Tediore_Pistol_C'],
            'SMGs' : ['BPInvPart_SM_TED_C', 'BPInvPart_Maliwan_SMG_C', 'BPInvPart_SM_Hyperion_C', 'BPInvPart_Dahl_SMG_C'],
            'Shotguns' : ['BPInvPart_SG_Torgue_C','BPInvPart_SG_JAK_C','BPInvPart_SG_TED_C','BPInvPart_SG_MAL_C'],
            'Sniper Rifles' : ['BPInvPart_VLA_SR_C', 'BPInvPart_MAL_Sr_C', 'BPInvPart_SR_JAK_C', 'BPInvPart_SR_HYP_C','BPInvPart_SR_DAL_C'],
            'Heavy Weapons' : ['BPInvPart_HW_VLA_C', 'BPInvPart_HW_TOR_C', 'BPInvPart_HW_ATL_C','BPInvPart_HW_COV_C']
        }
        wanted_part_classes = []
        for cat in self.categories:
            cat_lst = name_to_class[cat.CategoryName]
            for cls in cat_lst:
                wanted_part_classes.append(unrealsdk.FindClass(cls))
        all_parts = unrealsdk.FindAll('InventoryPartData', True)
        selected_parts = []
        generic_parts = []
        part_class_blacklist = set(['VehiclePartData','OakVehiclePartData','BPVehiclePart_C','OakWeaponMayhemPartData'])
        for part in all_parts:
            if part.Class.Name in part_class_blacklist:
                continue
            if 'Default__' in part.Name:
                continue
            if part.Class.Name == 'InventoryGenericPartData':
                generic_parts.append(part)
                continue
            if part.Class in wanted_part_classes:
                if 'endgame' in str(part.Name).lower():
                    continue
                selected_parts.append(part)
        return selected_parts, generic_parts

    def __part_fixer(self) -> None:
        parts = self.__get_parts()[0]
        gen_parts = self.__get_parts()[1]
        for part in parts:
            part.Dependencies = []
            part.Excluders = []
        if 'Class Mods' in self.whitelist:
            uistats = unrealsdk.FindAll('UIStatData', True)
            for stat in uistats:
                if stat.SectionName == 'LegendaryClassModInfo':
                    stat.SectionName = 'Secondary'
        for part in gen_parts:
            part.InventoryAttributeEffects = []
        

    @lru_cache(maxsize=25)
    def balance_constructor(self, body_part) -> tuple((bool,List, List)):
        parts = self.__get_parts()[0]
        parts_sorted = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for part in parts:
            part_type = part.PartType
            if part_type > 15:
                part.PartType = 15
                part_type = 15
            if self.rand_item_type == 'Weapon':
                if 'material_' in str(part.Name).lower() or 'mat_' in str(part.Name).lower():
                    part.PartType = 16
                    part_type = 16
            parts_sorted[part_type].append(part)
        if body_part != None: parts_sorted[0] = [body_part]
        start_idx = 0
        PartTypeTOC_lst = []
        for lst in parts_sorted:
            num_of_parts = len(lst)
            PartTypeTOC_lst.append((start_idx, num_of_parts))
            start_idx += num_of_parts
        AllParts_lst = []
        weight_strct = (1.5,(None,'None','None'),None,None,1.5)
        for lst in parts_sorted:
            for part in lst:
                AllParts_lst.append((part, weight_strct))
        return (True, PartTypeTOC_lst, AllParts_lst)


    @lru_cache(maxsize=1)
    def generic_part_handler(self):
        generic_parts = self.__get_parts()[1]
        weight_strct = (1.5,(None,'None','None'),None,None,1.5)
        gen_part_out_lst = []
        for part in generic_parts:
            gen_part_out_lst.append((part, weight_strct))
        return (True, gen_part_out_lst)


    def randomize(self) -> None:
        loaded_com = unrealsdk.FindAll('BPInv_ClassModData2_C')[0]
        if self.extreme:
            pass
        else:
            self.__part_fixer()
            balances = self.__get_balances()
            for bal in balances:
                try:
                    if self.rand_item_type == 'Weapon': bodypart = bal.RuntimePartList.AllParts[0].PartData
                    else: bodypart = None
                except IndexError:
                    # unrealsdk.Log(bal)
                    continue
                if self.whitelist == ['Class Mods']: bal.InventoryData = loaded_com
                bal.RuntimePartList = self.balance_constructor(bodypart)
                bal.RuntimeGenericPartList = self.generic_part_handler()
                bal.DlcInventorySetData = None
        for i in self.whitelist:
            unrealsdk.Log(f'Randomization of {i} is complete.')

class rand_helper:
    def __init__(self):
        pass
    def all_wep_rand(self, mix= False):
        unrealsdk.Log('Randomizing all weapons...')
        if mix == False:
            randomizer(whitelist=['Shotguns']).randomize()
            randomizer(whitelist=['Assault Rifles']).randomize()
            randomizer(whitelist=['Sniper Rifles']).randomize()
            randomizer(whitelist=['SMGs']).randomize()
            randomizer(whitelist=['Pistols']).randomize()
            randomizer(whitelist=['Heavy Weapons']).randomize()
        else:
            randomizer(whitelist=['Shotguns', 'Assault Rifles', 'Sniper Rifles', 'SMGs', 'Pistols', 'Heavy Weapons']).randomize()
    def all_gear_rand(self):
        unrealsdk.Log('Randomizing all gear...')
        randomizer(whitelist=['Artifacts']).randomize()
        randomizer(whitelist=['Shields']).randomize()
        randomizer(whitelist=['Class Mods']).randomize()
        randomizer(whitelist=['Grenade Mods']).randomize()


def rand_all(caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct):
    wep_thread = threading.Thread(target=rand_helper().all_wep_rand)
    gear_thread = threading.Thread(target=rand_helper().all_gear_rand)
    threads = [wep_thread, gear_thread]
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return True
try:
    unrealsdk.RunHook('/Script/OakGame.MenuMapMenuFlow.OnPlayerControllerLogIn', 'login_rand_wep', rand_all)
    unrealsdk.Log('Weapon Randomizer Hooked')
except:
    unrealsdk.Log('Weapon Randomizer Hook Failed')
