import unrealsdk as unrealsdk
from unrealsdk import *
import json
# import Mods.StatDisplay as SD
import sys
import csv
JSON_PATH = '.\\Mods\\Combat_Logger\\combat_log.json'
class default_data:
    def __init__(self):
        pass
################################################################################################
###for any of these lists put a # in front of the line to disable that source
###
    Dmg_Sources = [ 
        'DamageSource_Bullet_C',
        'DamageSource_ForceOnly_C',#parent of ground slam?
        'DamageSource_Melee_C',
        'DamageSource_Projectile_C',
        'DamageSource_Shield_C',
        'DamageSource_Slide_C',
        ##bl3
        'DamageSource_StuckGrenade_C',
        'DamageSource_Skill_C',
        'DamageSource_Passive_Skill_C',
        'DamageSource_Grenade_C',
        'DamageSource_Artifact_C',
        'DamageSource_Aftershock_C',
        ##wl
        'DamageSource_Gear_C',
        'DamageSource_SpellMod_C',
        'DamageSource_Ability_C',
        'DamageSource_StatusEffect_C',
        'DamageSource_Enchantment_C',
        #Stuff that prob never needs to be logged
        #'DamageSource_Environmental_C',
        #'DamageSource_GrenadeDoT_C',
        #'DamageSource_Vehicle_C',
    ]

    Dmg_Types = [
    ######Elements
        'DmgType_Cryo_Impact_C',
        'DmgType_Fire_Impact_C',
        'DmgType_Shock_Impact_C',
        'DmgType_Normal_C',
        ##bl3
        'DmgType_Corrosive_Impact_C',
        'DmgType_Radiation_Impact_C',
        ##wl
        'DmgType_Poison_Impact_C',
        'DmgType_Void_Impact_C',
        'DmgType_DarkMagic_Impact_C',
        ##Statuses
        'DmgType_Shock_Status_C',
        'DmgType_Fire_Status_C',
        ##bl3
        'DmgType_Corrosive_Status_C',
        'DmgType_Radiation_Status_C',
        ##wl
        'DmgType_Poison_Status_C',
        'DmgType_DarkMagic_Status_C',
        'DmgType_Cryo_Status_C',
    ######Misceallenous(not specified to game)
        'DmgType_Artifact_RearEnder_C',
        'DmgType_Healing_C',
        'DmgType_HealingArmor_C',
        'DmgType_HealingDefault_C',
        'DmgType_ShieldHeal_C',
        #DmgType_ShieldsOnly_C will be automatically added as its a child of Shock
    ]
################################################################################################
###Just logic code past here, only mess with it if you know what you're doing
###

class CombatEvent_memory:
    def __init__(self):
        self.Evenets = []

def get_cls(in_cls_lst: list[str]):
    out_cls_lst = []
    for cls in in_cls_lst:
        try:
            tmp = unrealsdk.FindClass(cls)
            if tmp != None:
                out_cls_lst.append(tmp)
        except:
            pass
    return out_cls_lst

def find_child_classes(cls: str, curr_cls_lst) -> list:
    all_classes = unrealsdk.FindAll(cls, True)
    out_lst = []
    # unrealsdk.Log(all_classes)
    for i in curr_cls_lst:
        for j in all_classes:
            c = j.Class
            while c:
                if c.Name == 'Object':
                    break
                try:
                    if c.SuperField.Name == i.Name:
                        out_lst.append(j.Class)
                        break
                except AttributeError:
                    pass
                c = c.SuperField
    out_lst.extend(curr_cls_lst)
    return out_lst

class CombatEvent_settings:
    def __init__(self,default = default_data()):
        self.AllowSeflDmg = False
        self.DmgSources = find_child_classes('DamageSource', get_cls(default.Dmg_Sources))
        self.DmgTypes = find_child_classes('GbxDamageType', get_cls(default.Dmg_Types))
        self.player_cont = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.useClassChildren = True
        self.default = default
        self.minimum_dmg = 134_217_728#2^27
        self.Log_stats = False

    def toggleAllowSelfDmg(self):
        self.AllowSeflDmg = not self.AllowSeflDmg
        unrealsdk.Log(f"Allow Self Damage set to {self.AllowSeflDmg}")

    def toggleStatLog(self):
        self.Log_stats = not self.Log_stats
        unrealsdk.Log(f"Stat Logging set to {self.Log_stats}")
    
    def DoubleMinDmg(self):
        self.minimum_dmg *= 2
        unrealsdk.Log(f"Minimum Damage set to {self.minimum_dmg:,}")

    def HalveMinDmg(self):
        if self.minimum_dmg > 1:
            self.minimum_dmg /= 2
            unrealsdk.Log(f"Minimum Damage set to {self.minimum_dmg:,}")
        else:
            unrealsdk.Log(f"Minimum Damage is already 1")

class CombatEvent:
    def __init__(self, settings: CombatEvent_settings, event: unrealsdk.FStruct):
        self.settings = settings
        self.event = event
        self.log = True
        self.Debug = False
    def verify(self):
        if self.event.Damage <= self.settings.minimum_dmg:
            self.log = False
            if self.Debug:unrealsdk.Log(f"Damage too low: {self.event.Damage}")
        if self.event.DamageSource.Class not in self.settings.DmgSources:
            self.log = False
            if self.Debug:unrealsdk.Log(f"DamageSource not in list: {self.event.DamageSource.Class}")
        if self.event.DamageType.Class not in self.settings.DmgTypes:
            self.log = False
            if self.Debug:unrealsdk.Log(f"DamageType not in list: {self.event.DamageType}")
        if self.event.InstigatedBy != self.settings.player_cont:
            self.log = False
            if self.Debug:unrealsdk.Log(f"InstigatedBy not player: {self.event.InstigatedBy}")
    def out(self):
        DamagePerHealthType = []
        for i in self.event.Details.DamagePerHealthType:
            tmp_dct = {'HealthType': i.HealthType.Name, 'Damage': i.Damage}
            DamagePerHealthType.insert(0,tmp_dct)
        out_dct = {
            'Enemy': str,
            'Damage': int(self.event.Damage),
            'DamageSource': str(self.event.DamageSource.Name).removesuffix('_C').removeprefix('Default__'),
            'DamageType': str(self.event.DamageType.Name).removesuffix('_C').removeprefix('Default__'),
            'WasCritical': self.event.Details.bWasCrit,
            'Radius': self.event.Details.DamageRadius,
            'DamagePerHealthType': DamagePerHealthType,
            'Stats': 'Not Logged'
        }
        return out_dct

def OnCombatLogEvent(caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct):
    if bool(caller == event_settings.player_cont.Pawn.OakDamageComponent) and event_settings.AllowSeflDmg == False:
        return
    else:
        combat_data = CombatEvent(event_settings, params)
        combat_data.verify()
        if combat_data.log:
            with open(JSON_PATH, 'r') as j:
                combat_dct = combat_data.out()
                if event_settings.Log_stats:
                    # SD.main()
                    pass
                combat_dct['Enemy'] = caller.GetOwner().Name
                jdata = json.load(j)
                jdata.append(combat_dct)
            with open(JSON_PATH, 'w') as j:
                json.dump(jdata, j, indent=4)

###Console commands
def ToCSV(c, f=(), p=()):
    with open(JSON_PATH, 'r') as j:
        jdata = json.load(j)
    csv_list = [['Enemy', 'Damage', 'DamageSource', 'DamageType', 'WasCritical', 'Radius', 'DamageDoneToEnemy', 'HealthTypeDamaged']]
    for i in jdata:
        tmp_lst = []
        tmp_lst.append(i['Enemy'])
        tmp_lst.append(i['Damage'])
        tmp_lst.append(i['DamageSource'])
        tmp_lst.append(i['DamageType'])
        tmp_lst.append(i['WasCritical'])
        tmp_lst.append(i['Radius'])
        dmg_to_enemy = 0
        for j in i['DamagePerHealthType']:
            dmg_to_enemy += j['Damage']
        tmp_lst.append(dmg_to_enemy)
        tmp_lst.append(i['DamagePerHealthType'][0]['HealthType'])
        csv_list.append(tmp_lst)
    csv_path = JSON_PATH.removesuffix('.json') + '.csv'
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_list)
def log_highest_num(c, f=(), p=()):
    with open(JSON_PATH, 'r') as j:
        jdata = json.load(j)
        highest = 0
        idx = -1
        for i in jdata:
            if i['Damage'] > highest:
                highest = i['Damage']
            idx += 1
        unrealsdk.Log(f"Highest Damage: {highest} at index {idx}")
def toggleAllowSelfDmg(c, f=(), p=()):
    event_settings.toggleAllowSelfDmg()
def DoubleMinDmg(c, f=(), p=()):
    event_settings.DoubleMinDmg()
def HalveMinDmg(c, f=(), p=()):
    event_settings.HalveMinDmg()
def toggleStatLog(c, f=(), p=()):
    event_settings.toggleStatLog()
def combat_log_help(c, f=(), p=()):
    unrealsdk.Log("Combat Log Commands:")
    unrealsdk.Log("    toggleAllowDot - Toggles if DoT damage is logged")
    unrealsdk.Log("    toggleAllowSelfDmg - Toggles if self damage is logged")
    unrealsdk.Log("    toggleUseClassChildren - Toggles if child classes of DamageSource and GbxDamageType are logged")
    unrealsdk.Log("    DoubleMinDmg - Doubles the minimum damage required to log")
    unrealsdk.Log("    HalveMinDmg - Halves the minimum damage required to log")
    unrealsdk.Log("    stop_cl - stops logging and terminates all hooks")
    unrealsdk.Log("    toggleStatLog - Toggles if stats are logged")
    unrealsdk.Log("    combat_log_help - Displays this help message")
    unrealsdk.Log("    ToCSV - Converts the json file to a csv file")


####################################
def start_cl(c=(), f=(), p=()):
    global is_started
    is_started = True
    unrealsdk.RunHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'CombatLog', OnCombatLogEvent)
    unrealsdk.RemoveConsoleCommand('ToggleSelfDmg')
    unrealsdk.RegisterConsoleCommand('ToggleSelfDmg',toggleAllowSelfDmg)
    unrealsdk.RemoveConsoleCommand('DoubleMinDmg')
    unrealsdk.RegisterConsoleCommand('DoubleMinDmg',DoubleMinDmg)
    unrealsdk.RemoveConsoleCommand('HalveMinDmg')
    unrealsdk.RegisterConsoleCommand('HalveMinDmg',HalveMinDmg)
    unrealsdk.RemoveConsoleCommand('combat_log_help')
    unrealsdk.RegisterConsoleCommand('combat_log_help',combat_log_help)
    unrealsdk.RemoveConsoleCommand('stop_cl')
    unrealsdk.RemoveConsoleCommand('toggleStatLog')
    unrealsdk.RegisterConsoleCommand('toggleStatLog',toggleStatLog)
    unrealsdk.RemoveConsoleCommand('log_highest_dmg')
    unrealsdk.RegisterConsoleCommand('log_highest_dmg',log_highest_num)
    unrealsdk.RemoveConsoleCommand('ToCSV')
    unrealsdk.RegisterConsoleCommand('ToCSV',ToCSV)
    unrealsdk.RemoveConsoleCommand('stop_cl')
    unrealsdk.RegisterConsoleCommand('stop_cl',stop_cl)
    unrealsdk.Log("Combat Logger Loaded")
    global event_settings
    event_settings = CombatEvent_settings()
    def __GetGame() -> str:
        """Returns \'Wonderlands\' or \'Borderlands3\' depending on the game."""
        return sys.executable.split('\\')[-1].replace('.exe','')
    if __GetGame() == 'Wonderlands':
        event_settings.minimum_dmg = 1_048_576#2^20
    with open(JSON_PATH, 'w') as file:
        json.dump(list(), file)


def stop_cl_outer(c, f=(), p=()):
    is_started = False
    stop_cl()

def stop_cl(c, f=(), p=()):
    unrealsdk.RemoveHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'CombatLog')
    unrealsdk.RemoveConsoleCommand('combat_log_help')
    unrealsdk.RemoveConsoleCommand('ToggleDot')
    unrealsdk.RemoveConsoleCommand('ToggleSelfDmg')
    unrealsdk.RemoveConsoleCommand('ToggleUseClassChildren')
    unrealsdk.RemoveConsoleCommand('DoubleMinDmg')
    unrealsdk.RemoveConsoleCommand('HalveMinDmg')
    unrealsdk.RemoveConsoleCommand('stop_cl')
    unrealsdk.RemoveConsoleCommand('toggleStatLog')
    unrealsdk.RemoveConsoleCommand('log_highest_dmg')
    unrealsdk.Log("Combat Logger Unloaded")
    unrealsdk.RemoveConsoleCommand('stop_cl')
    event_settings = None
    return True

def on_loadedinsave(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct):
    if is_started:
        start_cl()
unrealsdk.RemoveConsoleCommand('start_cl')
unrealsdk.RegisterConsoleCommand('start_cl',start_cl)
unrealsdk.RunHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade', 'quit_cl', stop_cl)
unrealsdk.RunHook('/Script/OakGame.OakCharacter_Player.ShowConnectEffect', 'load_cl', on_loadedinsave)




