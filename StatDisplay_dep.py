import unrealsdk as unrealsdk
from unrealsdk import *
import sys
game = sys.executable.split('\\')[-1].replace('.exe','')
unrealsdk.Log(f"Current game is {game}")


att_class = unrealsdk.FindClass("BP_OakAttributeComponent_C", True)

#att_components = unrealsdk.FindAll("BP_OakAttributeComponent_C", True)

player_att_comp = None

def modifier_type_resolver(default=1.0,preadd=0.0,pos_scale=0.0, neg_scale=0.0,simple_scale=1.0, postadd=0.0) -> float:
    """
    Takes up to 6 arguments and returns a float value of the calculated value of the modifier.
    """
    return (default + preadd) * ((1 + pos_scale)/(1 - neg_scale)) * (simple_scale) + postadd

def GetPlayerController():
    PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
    return PC

player_pawn = GetPlayerController().Pawn
player_att_comp = player_pawn.BP_OakAttributeComponent



if player_att_comp is None:
    unrealsdk.Log('Player Attribute Component not found!')

struct_dmg_props = ['TypeInstigatorMultipliers','SourceInstigatorMultipliers','EffectInstigatorMultipliers']
struct_tkn_props = ['TypeReceiverMultipliers','SourceReceiverMultipliers','EffectActorMultipliers']

def damage_causer() -> unrealsdk.UObject:
    dmg_causer_obj = None
    dmg_causer_obj = player_pawn.DamageCauserComponent
    if dmg_causer_obj is None:
        unrealsdk.Log('Damage Causer Component not found!')
        return
    return dmg_causer_obj


def Causer_stat_getter(dmg_causer_obj) -> list:
    v1 = dmg_causer_obj.DamageDealtMultiplier.Value
    area_dmg = dmg_causer_obj.RadiusDamage_DamageMultiplier.Value
    area_radius = dmg_causer_obj.RadiusDamage_RadiusMultiplier.Value
    return [('Global Damage',v1), ('AOE Damage',area_dmg), ('AOE Radius',area_radius)]

def Critical_stat_getter(dmg_causer_obj) -> None:
    default_crit_dmg = dmg_causer_obj.DefaultCriticalHitMultiplier.Value
    if game == 'Wonderlands':
        default_crit_chance = dmg_causer_obj.DefaultCriticalHitChance.Value
        src_crit_mod_dmg = dmg_causer_obj.SourceCritDamageModifiers
        src_crit_mod_chance = dmg_causer_obj.SourceCritChanceModifiers
    unrealsdk.Log((' '*12)+'----------Crit stats----------')
    #default modifiers
    default_crit_dmg = 'Base Crit Damage: ' + str(default_crit_dmg)[:5]
    if game == 'Wonderlands':
        default_crit_chance = 'Base Crit Chance: ' + str(default_crit_chance)[:5]
        spacer1 = ' ' * (28 - len(default_crit_dmg))
        unrealsdk.Log(f'{default_crit_dmg}{spacer1}| {default_crit_chance}')
    else:
        unrealsdk.Log(default_crit_dmg)
    def crit_stat_struct_handler(struct: unrealsdk.UStruct) -> list:
        source = str(dmg_mod.DamageSource).split('.')[-1]
        if source == 'DamageSource':
            source = 'All'
        else:
            source = source.split('_')[1]
        preadd = dmg_mod.CritModifierPreAdd.Value
        postadd = dmg_mod.CritModifierPostAdd.Value
        scale = dmg_mod.CritModifierScale.Value
        simple_scale = dmg_mod.CritModifierSimpleScale.Value
        final_value = modifier_type_resolver(preadd=preadd, pos_scale=scale, simple_scale=simple_scale, postadd=postadd)
        return (source, final_value)
    if game == 'Wonderlands':
        crit_dmg_stats = []
        for dmg_mod in src_crit_mod_dmg:
            crit_dmg_stats.append(crit_stat_struct_handler(dmg_mod))
        crit_chance_stats = []
        for dmg_mod in src_crit_mod_chance:
            crit_chance_stats.append(crit_stat_struct_handler(dmg_mod))
        #Source modifiers
        num_of_rows = max(len(crit_dmg_stats), len(crit_chance_stats))
        unrealsdk.Log('#Crit Source Dmg Modifiers# | #Crit Source Chance Modifiers#')
        for i in range(num_of_rows):
            try:
                dmg_stat = f'{crit_dmg_stats[i][0]} Damage: {str(crit_dmg_stats[i][1])[:5]}'
            except IndexError:
                dmg_stat = ''
            try:
                chance_stat = f'{crit_chance_stats[i][0]} Chance: {str(crit_chance_stats[i][1])[:5]}'
            except IndexError:
                chance_stat = ''
            spacer2 = ' ' * (28 - len(dmg_stat))
            unrealsdk.Log(f'{dmg_stat}{spacer2}| {chance_stat}')





def get_cls_prop(cls: unrealsdk.UClass, name: str) -> unrealsdk.UProperty:
    while cls:
        prop = cls.Children
        while prop:
            if prop.Name == name:
                return prop
            prop = prop.Next
        cls = cls.SuperField

def dump_cls_fields(cls: unrealsdk.UClass) -> list:
    properties = []
    while cls:
        unrealsdk.Log(f"    = {cls.Name} =")
        if cls.Name in ("Object", "Actor"):
            unrealsdk.Log("<ommited>")
            return
        prop = cls.Children
        while prop:
            out = f"{prop.Name}"
            #unrealsdk.Log(out)#prop.Class.Name, 
            properties.append(out)
            prop = prop.Next
        cls = cls.SuperField
    return properties


def struct_reader(i: int) -> list:
    out_lst = []
    def sub_reader(name: str) -> list:
        out_lst_sub = []
        struct = get_cls_prop(att_class, name).InnerProperty
        fields = dump_cls_fields(struct)
        curr_struct = getattr(player_att_comp, name)
        for j in fields:
            stat_name = j.split('_')[0]
            stat_value = getattr(curr_struct, j).Value
            out_lst_sub.append(f'{stat_name}: {str(stat_value)[:5]}')
        return out_lst_sub
    left_list = sub_reader(struct_dmg_props[i])
    right_list = sub_reader(struct_tkn_props[i])
    unrealsdk.Log('#Damage Dealt#'+(' '*14)+'| '+'#Damage Taken#')
    for i in range(len(left_list)):
        spacer = ' ' * (28 - len(left_list[i]))
        out_string = f'{left_list[i]}{spacer}| {right_list[i]}'
        out_lst.append(out_string)
        unrealsdk.Log(out_string)
    return out_lst

def weapon_stat_getter():
    player_pawn = GetPlayerController().Pawn
    weapon_fire_comp = player_pawn.GetActiveWeapon(0).CurrentFireComponent
    damage = weapon_fire_comp.Damage.Value
    firerate = weapon_fire_comp.FireRate.Value
    projectile_per_shot = weapon_fire_comp.ProjectilesPerShot.Value
    unrealsdk.Log((' '*12)+'----------Weapon stats----------')
    dmg_string = f'Damage: {str(damage)[:11]} x {str(projectile_per_shot)}'
    spacer= ' ' * (28 - len(dmg_string))
    dps = damage*firerate*projectile_per_shot
    unrealsdk.Log(f'{dmg_string}{spacer}| Firerate: {str(firerate)[:8]}')
    unrealsdk.Log(f'Raw DPS: {str(dps)[:19]}\n Raw DPS means no buffs,crits or reloads')

def main():
    for item in range(3):
        struct_reader(item)
    other_stats = Causer_stat_getter(damage_causer())
    unrealsdk.Log((' '*12)+'----------other stats---------')
    for i in other_stats:
        unrealsdk.Log(i[0]+': '+str(i[1])[:5])
    Critical_stat_getter(damage_causer())
    weapon_stat_getter()


if __name__ == '__main__':
    main()
    unrealsdk.Log('Done')
    unrealsdk.Log(' ')