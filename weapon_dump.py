import unrealsdk as unrealsdk
from unrealsdk import *
from Mods.Data_Deriving import GetDatatableValue, GetPlayerController, GetAttValue, GetObject, GetGame
import json

def dict_to_str(obj):
    from json import JSONEncoder
    iterable = JSONEncoder(skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, indent=2, separators=None,
        default=None, sort_keys=False).iterencode(obj)
    return ''.join(iterable)


def modifier_struct_to_dict(struct: unrealsdk.UObject) -> dict:
    try:
        mod_value = struct.ModifierValue
        return_dict = {
            'AttributeToModify': str(struct.AttributeToModify.Name),
            'ModifierType': str(struct.ModifierType['Name']),
            'ModifierValue': {
                'BaseValue': float(mod_value.BaseValueConstant),
                'DataTableRef': ['None', 'None', 'None'],
                'BaseValueAttribute': 'None',
                'AttributeInitializer': 'None',
                'BaseScalar': float(mod_value.BaseValueScale)
            }
        }
        if mod_value.DataTableValue.DataTable not in (None, None):
            return_dict['ModifierValue']['DataTableValue'] = [
                str(mod_value.DataTableValue.DataTable.Name),
                str(mod_value.DataTableValue.RowName),
                str(mod_value.DataTableValue.ValueName)[:-35],
            ]
        if mod_value.BaseValueAttribute != None:
            return_dict['ModifierValue']['BaseValueAttribute'] = str(mod_value.BaseValueAttribute.Name)
        if mod_value.AttributeInitializer != None:
            return_dict['ModifierValue']['AttributeInitializer'] = str(mod_value.AttributeInitializer.Name)
    except:
        return_dict = {'Error': 'Failed to convert modifier struct to dict.'}
    return return_dict



blurb = 'stats are current value with buffs'
weapon_dump_dict = {
    'note': blurb,
    'name': str,
    'invdata': str,
    'manu': str,
    'balance': str,
    'level': int,
    'bonus_levels': int,
    'stats': {
        'damage': float,
        'firerate': float,
        'projectiles_per_shot': float,
        'accuracy': float,
        'reload_time': float,
        'magazine_size': float,
        'burst': {'delay': float, 'shots': int},
        'radius': float,
    },
    'modifiers': {
        'WeaponUseModeAttributeEffects': {
            1: list[dict],
            2: list[dict],
            3: list[dict]
        },
        'InventoryAttributeEffects': list[dict],
        'InstigatorAttributeEffects': list[dict]
    },
    'lightprojectile': str,
    'damage_source': str,
    'damage_type': str,
    'abilities': list,
    'cdm': list,
    'parts': list,
    'Gparts': list
}


try:
    _player = GetPlayerController().Pawn
    _weapon = _player.GetActiveWeapon(0)
    _weapon_fire_comp = _weapon.CurrentFireComponent
    _weapon_balance_state = _weapon.BalanceStateComponent
except:
    weapon_dump_dict = {'Error': 'Failed to get player or weapon.'}

unrealsdk.Log('#Weapon Dump#')
name_list = []
for name in _weapon_balance_state.NamePartList:
    name_list.append(str(name.PartName))
weapon_dump_dict['name'] = str(' '.join(name_list))
weapon_dump_dict['invdata'] = str(_weapon_balance_state.InventoryData.Name)
weapon_dump_dict['manu'] = str(_weapon_balance_state.ManufacturerData.Name)
weapon_dump_dict['balance'] = str(_weapon_balance_state.InventoryBalanceData.Name)
weapon_dump_dict['level'] = int(_weapon_balance_state.GameStage)
try:
    weapon_dump_dict['stats'] = {
        'damage': float(_weapon_fire_comp.Damage.Value),
        'firerate': float(_weapon_fire_comp.FireRate.Value),
        'projectiles_per_shot': float(_weapon_fire_comp.ProjectilesPerShot.Value),
        'accuracy': float((1/(float(_weapon_fire_comp.AccuracyImpulse.Value + 0.01)))*float(_weapon_fire_comp.Spread.Value)),
        'reload_time': GetAttValue(GetObject('GbxAttributeData', '/Game/GameData/Weapons/Att_Weapon_ReloadTime.Att_Weapon_ReloadTime')),
        'magazine_size': GetAttValue(GetObject('GbxAttributeData', '/Game/GameData/Weapons/Att_Weapon_MaxLoadedAmmo.Att_Weapon_MaxLoadedAmmo')),
        'burst': {'delay': float(_weapon_fire_comp.BurstFireDelay.Value), 'shots': int(_weapon_fire_comp.AutomaticBurstCount.Value)},
        'radius': _weapon_fire_comp.DamageRadius.Value}
except:
    weapon_dump_dict['stats'] = {'Error': 'Failed to get stats.'}
#breaking order here cuz needed to get parts first to get some other things
raw_part_list = _weapon_balance_state.PartList
part_list=[]
try:
    for part in raw_part_list:
        part_list.append(str(part.Name))
    weapon_dump_dict['parts'] = part_list
    Gpart_list=[]
    for gpart in _weapon_balance_state.GenericPartList:
        Gpart_list.append(str(gpart.Name))
    weapon_dump_dict['Gparts'] = Gpart_list
except:
    weapon_dump_dict['parts'] = ['Error']
    weapon_dump_dict['Gparts'] = ['Error']
try:
    InventoryAttributeEffects_lst = []
    for part in raw_part_list:
        for inv_att_effect in part.InventoryAttributeEffects:
            InventoryAttributeEffects_lst.append(dict(modifier_struct_to_dict(inv_att_effect)))
    InstigatorAttributeEffects_lst = []
    for part in raw_part_list:
        for inst_att_effect in part.InstigatorAttributeEffects:
            InstigatorAttributeEffects_lst.append(dict(modifier_struct_to_dict(inst_att_effect)))
    WeaponUseModeAttributeEffects_lst1 = []
    WeaponUseModeAttributeEffects_lst2 = []
    WeaponUseModeAttributeEffects_lst3 = []
    for part in raw_part_list:
        for use_mode_att_effect in part.WeaponUseModeAttributeEffects:
            if int(use_mode_att_effect.UseModeBitmask) == 1:
                for final in use_mode_att_effect.AttributeEffects:
                    WeaponUseModeAttributeEffects_lst1.append(dict(modifier_struct_to_dict(final)))
            elif int(use_mode_att_effect.UseModeBitmask) == 2:
                for final in use_mode_att_effect.AttributeEffects:
                    WeaponUseModeAttributeEffects_lst2.append(dict(modifier_struct_to_dict(final)))
            elif int(use_mode_att_effect.UseModeBitmask) == 3:
                for final in use_mode_att_effect.AttributeEffects:
                    WeaponUseModeAttributeEffects_lst3.append(dict(modifier_struct_to_dict(final)))
    weapon_dump_dict['modifiers'] = {
        'WeaponUseModeAttributeEffects': {1: WeaponUseModeAttributeEffects_lst1, 2: WeaponUseModeAttributeEffects_lst2, 3: WeaponUseModeAttributeEffects_lst3},
        'InventoryAttributeEffects': InventoryAttributeEffects_lst,
        'InstigatorAttributeEffects': InstigatorAttributeEffects_lst}
except:
    weapon_dump_dict['modifiers'] = {'Error': 'Failed to get modifiers.'}
try:
    weapon_dump_dict['damage_source'] = str(_weapon_fire_comp.DamageSource.Name)
except:
    weapon_dump_dict['damage_source'] = 'None'
try:
    weapon_dump_dict['damage_type'] = str(_weapon_fire_comp.DamageType.Name)
except:
    weapon_dump_dict['damage_type'] = 'None'
try:
    weapon_dump_dict['lightprojectile'] = _weapon_fire_comp.LightProjectileData.Name
except:
    weapon_dump_dict['lightprojectile'] = 'None'
try:
    ability_list = []
    for struct in _weapon_balance_state.AbilityAspects:
        for abilities in struct.Abilities:
            ability_list.append(str(abilities.Ability.Name))
    weapon_dump_dict['abilities'] = ability_list
except:
    weapon_dump_dict['abilities'] = ['Error']
try:
    cdm_list = []
    for struct in _weapon_balance_state.ConditionalDamageAspectList:
        for cdms in struct.DamageConditionals:
            cdm_list.append(str(cdms.ConditionalModifier.Name))
    weapon_dump_dict['cdm'] = cdm_list
except:
    weapon_dump_dict['cdm'] = ['Error']
try:
    if GetGame() == 'Wonderlands':
        weapon_dump_dict['bonus_levels'] = GetDatatableValue(GetObject('DataTable', '/Game/GameData/Mayhem/Balance/Table_Mayhem_GlobalModifers.Table_Mayhem_GlobalModifers'),f'Overpower_Tier{str(_weapon_balance_state.OverpowerLevel)}_LevelEquivalency', 'Base_17_28B25EC8493D1EB6C2138A962F659BCD')
    elif GetGame() == 'Borderlands3':
        weapon_dump_dict['bonus_levels'] = 0
        for part in _weapon_balance_state.GenericPartList:
            if 'Mayhem' in part.Name:
                weapon_dump_dict['bonus_levels'] = part.MayhemLevel
except:
    weapon_dump_dict['bonus_levels'] = 'Error'

with open('.\Mods\weapon_dump.json', 'w') as f:
    json.dump(weapon_dump_dict, f, indent=4)

unrealsdk.Log(dict_to_str(weapon_dump_dict))
unrealsdk.Log('Done.')





