import unrealsdk as unrealsdk #i looooooooooooooooooooooooooooooove gay butt sex 🤨
from unrealsdk import *
import json
from typing import Dict, List, Optional, Tuple
from functools import lru_cache
import threading



class part_data:
    def __init__(self) -> None:
        pass

    @property
    @lru_cache(maxsize=None)
    def PartTypeEnum(self) -> Dict:
        with open('Mods\\Item_Randomizer\\part_enums.json') as f:
            return json.load(f)

class randomizer:
    """
    Give this class a list of categories to whitelist.
    Extreme will make things more random, but will also make it more likely to crash.
    """
    def __init__(self, whitelist: List[str] = [], extreme = False) -> None:
        self.whitelist = whitelist
        self.extreme = extreme
        self.weap_parts = []

    @property
    @lru_cache(maxsize=None)
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

    @lru_cache(maxsize=None)
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
            'Assault Rifles' : ['BPInvPart_AR_COV_C', 'BPInvPart_JAK_AR_C', 'BPInvPart_AR_DAL_C', 'BPInvPart_VLA_AR_C', 'BPInvPart_AR_TOR_C', 'BPInvPart_ATL_AR_C','BPInvPart_PS_DAL_C'],
            'Pistols' : ['BPInvPart_PS_COV_C', 'BPInvPart_Jakobs_Pistol_C', 'BPInvPart_Pistol_DAL_C', 'BPInvPart_PS_VLA_C', 'BPInvPart_PS_TOR_C','BPInvPart_PS_ATL_C','BPInvPart_PS_MAL_C','BPInvPart_Tediore_Pistol_C'],
            'SMGs' : ['BPInvPart_SM_TED_C', 'BPInvPart_Maliwan_SMG_C', 'BPInvPart_SM_Hyperion_C', 'BPInvPart_Dahl_SMG_C'],
            'Shotguns' : ['BPInvPart_SG_Torgue_C','BPInvPart_SG_JAK_C','BPInvPart_SG_TED_C','BPInvPart_SG_MAL_C','BPInvPart_Hyperion_Shotgun_C'],
            'Sniper Rifles' : ['BPInvPart_VLA_SR_C', 'BPInvPart_MAL_SR_C', 'BPInvPart_SR_JAK_C', 'BPInvPart_SR_HYP_C','BPInvPart_SR_DAL_C'],
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
                selected_parts.append(part)
        return selected_parts, generic_parts

    def __weap_part_sorter(self) -> List:
        """
        Sorts weapon parts into having better part typing.
        """
        parts = self.__get_parts()[0]
        part_type_dict = part_data().PartTypeEnum
        part_cat_type = {
            'Body' : 0,
            'Body_Mod' : 1,
            'Barrel' : 2,
            'Barrel_Mod' : 3,
            'Grip' : 4,
            'Foregrip' : 5,
            'Stock' : 6,
            'Accessory' : 7,
            'AltMod' : 8,
            'Magazine' : 9,
            'Scope' : 10,
            'Elemental' : 11,
            'Material' : 12,
        }
        for part in parts:
            cls = part.Class.Name
            if cls in set(['VehiclePartData','OakVehiclePartData','BPVehiclePart_C','OakWeaponMayhemPartData']):
                continue
            try:
                part_type_name = part_type_dict[cls][str(part.PartType)]
            except Exception as e:
                unrealsdk.Log(f'Error: {e}, Class: {cls},Part: {part.Name}, PartType: {part.PartType}', level = -1)
                continue
            if part_type_name == 'Trash':
                continue
            part.PartType = part_cat_type[part_type_name]
            self.weap_parts.append(part)

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
        

    @lru_cache(maxsize=None)
    def gear_balance_constructor(self) -> tuple((bool,List, List)):
        parts = self.__get_parts()[0]
        parts_sorted = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for part in parts:
            part_type = part.PartType
            if part_type > 15:
                part.PartType = 15
                part_type = 15
            parts_sorted[part_type].append(part)
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

    @lru_cache(maxsize=None)
    def weap_balance_constructor(self) -> tuple((bool,List, List)):
        parts = self.weap_parts
        parts_sorted = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        bHasBodyPart = False
        for part in parts:
            cls = part.Class.Name
            part_type = part.PartType
            if part_type == 0 and not bHasBodyPart:
                bHasBodyPart = True
            elif part_type == 0 and bHasBodyPart:
                continue
            parts_sorted[part_type].append(part)
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

    @lru_cache(maxsize=None)
    def generic_part_handler(self):
        """Returns a list of generic parts"""
        generic_parts = self.__get_parts()[1]
        weight_strct = (1.5,(None,'None','None'),None,None,1.5)
        gen_part_out_lst = []
        for part in generic_parts:
            gen_part_out_lst.append((part, weight_strct))
        return (True, gen_part_out_lst)

    def weap_part_count_modifier(self, balance: unrealsdk.UObject) -> None:
        """Modifies the number of parts that can be generated for a weapon based on rarity"""
        balance.MaxNumPrefixes = 3 #more text means more things... right?
        bodypart = None
        try:
            bodypart = balance.RuntimePartList.AllParts[0].PartData
        except IndexError:
            pass
        bal_parts = self.weap_balance_constructor()
        bal_parts[-1][0] = (bodypart, (1.5,(None,'None','None'),None,None,1.5))
        balance.RuntimePartList = bal_parts
        partset = balance.PartSetData
        part_enum = partset.PartTypeEnum
        rarity_name = str(balance.RarityData.Name).split('_')[-1]
        rarity_part_count = { #this is so rarity matters alot more than just pure random
            'Common': {'normal': (0,0), 'special': (1,1), 'single': (1,1)},
            'Uncommon': {'normal': (0,1), 'special': (1,1), 'single': (1,1)},
            'Rare': {'normal': (1,1), 'special': (1,1), 'single': (1,1)},
            'VeryRare': {'normal': (1,2), 'special': (1,2), 'single': (1,1)},
            'Legendary': {'normal': (2,2), 'special': (2,2), 'single': (1,1)}
        }
        part_type_dct = {
            0: 'single', #body
            1: 'normal', #body mod
            2: 'special',#barrel
            3: 'normal', #barrel mod
            4: 'normal', #grip
            5: 'normal', #foregrip
            6: 'normal', #stock
            7: 'normal', #accessory
            8: 'special',#alt mode
            9: 'single', #magazine
            10: 'single',#scope
            11: 'single',#elemental
            12: 'single' #material
        }
        def __part_range(part_type: int, raity: str) -> Tuple[int, int]:
            part_type_name = part_type_dct[part_type]
            part_range = rarity_part_count[raity][part_type_name]
            return part_range
        def __get_bal_parts(part_type: int, bal_partlist: Tuple[bool, List, List]) -> List[unrealsdk.UObject]:
            toc = bal_partlist[1]
            all_parts = bal_partlist[2]
            start_idx = toc[part_type][0]
            end_idx = start_idx + toc[part_type][1]
            parts = all_parts[start_idx:end_idx]
            return parts
        ActorPartLists = []
        for part_idx in range(13):
            ActorPartLists.append((part_enum,part_idx,True,False,__part_range(part_idx, rarity_name),True,__get_bal_parts(part_idx, bal_parts)))
        partset.ActorPartLists = ActorPartLists

    def randomize(self) -> None:
        loaded_com = unrealsdk.FindAll('BPInv_ClassModData2_C')[0]
        if self.extreme:
            pass
        else:
            self.__part_fixer()
            balances = self.__get_balances()
            if self.rand_item_type == 'Weapon': self.__weap_part_sorter()
            for bal in balances:
                if self.rand_item_type == 'Weapon':
                    bodypart = None
                    try:
                        bodypart = bal.RuntimePartList.AllParts[0].PartData
                    except IndexError:
                        continue
                    self.weap_part_count_modifier(bal)
                    bal.RuntimePartList.AllParts[0] = (bodypart, (1.5,(None,'None','None'),None,None,1.5))
                else:
                    if self.whitelist == ['Class Mods']: bal.InventoryData = loaded_com
                    bal.RuntimePartList = self.gear_balance_constructor()
                bal.RuntimeGenericPartList = self.generic_part_handler()
                bal.DlcInventorySetData = None
        for i in self.whitelist:
            unrealsdk.Log(f'Randomization of {i} is complete.', level = 5)

class rand_helper:
    def __init__(self, extreme: bool):
        pass
    def all_wep_rand(self):
        # unrealsdk.Log('Randomizing all weapons...')
        if not self.extreme:
            randomizer(whitelist=['Shotguns']).randomize()
            randomizer(whitelist=['Assault Rifles']).randomize()
            randomizer(whitelist=['Sniper Rifles']).randomize()
            randomizer(whitelist=['SMGs']).randomize()
            randomizer(whitelist=['Pistols']).randomize()
            randomizer(whitelist=['Heavy Weapons']).randomize()
        else:
            randomizer(whitelist=['Shotguns', 'Assault Rifles', 'Sniper Rifles', 'SMGs', 'Pistols', 'Heavy Weapons'], extreme = True).randomize()
    def all_gear_rand(self):
        # unrealsdk.Log('Randomizing all gear...')
        randomizer(whitelist=['Artifacts']).randomize()
        randomizer(whitelist=['Shields']).randomize()
        randomizer(whitelist=['Class Mods']).randomize()
        randomizer(whitelist=['Grenade Mods']).randomize()


def rand_all(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct):
    wep_thread = threading.Thread(target=rand_helper().all_wep_rand)
    gear_thread = threading.Thread(target=rand_helper().all_gear_rand)
    threads = [wep_thread, gear_thread]
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    unrealsdk.RemoveHook('/Script/OakGame.MenuMapMenuFlow.OnPlayerControllerLogIn', 'login_rand_wep')
    return True

unrealsdk.RegisterHook('/Script/OakGame.MenuMapMenuFlow.OnPlayerControllerLogIn', 'login_rand_wep', rand_all)
unrealsdk.Log('Item Randomizer Started')

