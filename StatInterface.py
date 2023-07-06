import unrealsdk as unrealsdk
from unrealsdk import *
import sys

def dict_to_str(obj):
    from json import JSONEncoder
    iterable = JSONEncoder(skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, indent=2, separators=None,
        default=None, sort_keys=False).iterencode(obj)
    return ''.join(iterable)
                                                                                                                                                                #comments should be in this line
#BP_OakAttributeComponent_C
class bl3_struct_data:
    def __init__(self):
        self.SourceStruct = [
            'Bullet_32_00C5C4A64E4D62A6E142168CD3682B53',
            'Grenade_33_B86BE45A4D32AF449A502DB4F7C6A5FC',
            'Melee_34_0DEF868B48EFA9D1D7C730956D617AEC',
            'Shield_36_EF2E31A34911FE1EB2EEC2AFD9A6450C',
            'Skill_37_B8A29EEC49C43F47944AA3861600D35B',
            'PassiveSkill_73_48ACDDC647CC21F34063379AEEB607B5',
            #'Skill_IgnoreIO_42_7A6DE2A942BEDB22AABEAF8B7920A782',                                                                                              #pointless?
            'Vehicle_43_A75E8224491A98014FE9D0AD1F584796',
            #'InteractiveObject_46_0E1BB1BD45F7083BAA0EBC92AAFBCA69',                                                                                           #deadass have no idea what this could be for
            'ButtStomp_49_A56C89A74AF90AB593A582955329D3B2',                                                                                                    #slam... just call it slam gbx
            #'Slide_51_4E3DBAA44CAC7C07345ED29E4E22C434',                                                                                                       #Who asked?
            #'Environmental_54_3CD0B8494596B6B6C20E7EA352A89886',                                                                                               #typically player doesnt have bonuses to this
            #'Rocket_35_09A06D2A411E425283DFF58D532EDEA8',                                                                                                      #huh?
            'AssaultRifle_58_3537AA3741E07C15FCA4D4B2E48033C6',
            'Shotgun_60_9927887C422A095EEE5CDA9B8B03BA5B',
            'SMG_62_0FDC2CFD424FF18484D9499528795BD5',
            'Pistol_64_0E3518094921C23317F4DC9D9E4F4511',
            'SniperRifle_66_ECF086E140BBA6057EEC9CAD1066FA4D',
            'HeavyWeapon_70_F6B518774A1F6249FF0125BC1D1BBBA3']
        self.TypeStruct = [
            'Normal_26_00C5C4A64E4D62A6E142168CD3682B53',
            'Fire_27_B86BE45A4D32AF449A502DB4F7C6A5FC',
            'Shock_28_0DEF868B48EFA9D1D7C730956D617AEC',
            'Corrosive_29_09A06D2A411E425283DFF58D532EDEA8',
            'Radiation_32_EF2E31A34911FE1EB2EEC2AFD9A6450C',
            'Cryo_31_B8A29EEC49C43F47944AA3861600D35B']
class wl_struct_data:
    def __init__(self):
        self.SourceStruct = [
            'Bullet_32_00C5C4A64E4D62A6E142168CD3682B53',
            'Grenade_33_B86BE45A4D32AF449A502DB4F7C6A5FC',                                                                                                      #should be spell
            'Melee_34_0DEF868B48EFA9D1D7C730956D617AEC',
            'Shield_36_EF2E31A34911FE1EB2EEC2AFD9A6450C',
            'Skill_37_B8A29EEC49C43F47944AA3861600D35B',                                                                                                        #Should really be called ability
            #'Skill_IgnoreIO_42_7A6DE2A942BEDB22AABEAF8B7920A782',                                                                                              #pointless?
            #'Vehicle_43_A75E8224491A98014FE9D0AD1F584796',                                                                                                     #not used in game
            #'InteractiveObject_46_0E1BB1BD45F7083BAA0EBC92AAFBCA69',                                                                                           #deadass have no idea what this could be for
            'ButtStomp_49_A56C89A74AF90AB593A582955329D3B2',                                                                                                    #slam... just call it slam gbx
            #'Slide_51_4E3DBAA44CAC7C07345ED29E4E22C434',                                                                                                       #Who asked?
            #'Environmental_54_3CD0B8494596B6B6C20E7EA352A89886',                                                                                               #typically player doesnt have bonuses to this
            #'Rocket_35_09A06D2A411E425283DFF58D532EDEA8',                                                                                                      #huh?
            'AssaultRifle_58_3537AA3741E07C15FCA4D4B2E48033C6',
            'Shotgun_60_9927887C422A095EEE5CDA9B8B03BA5B',
            'SMG_62_0FDC2CFD424FF18484D9499528795BD5',
            'Pistol_64_0E3518094921C23317F4DC9D9E4F4511',
            'SniperRifle_66_ECF086E140BBA6057EEC9CAD1066FA4D',
            'HeavyWeapon_70_F6B518774A1F6249FF0125BC1D1BBBA3',
            #'PassiveSkill_77_95DB83554C4B8538289B0ABFDE63FBFE',                                                                                                #pretty sure this isnt used in game
            #'Gear_76_9316750049C562A99DF7E1990ED825CD',                                                                                                        #nothing in base game buffs this but could uncomment if mods do
            #'Sword1H_92_A56D962B45608DCA031771BFFC6F6777',                                                                                                     #Very rarely are they individually buffed
            #'Sword2H_91_FB6F4DB64DDB34F04D64F5AA313F8696',                                                                                                     #^^^
            #'Blunt1H_93_736AD0C648F9BED32BD735B17830CD3B',                                                                                                     #^^^
            #'Axe1H_94_96E46C14419D1C550053EDA8877F0A61',                                                                                                       #^^^
            #'Dagger1H_95_D28D25D84C48736E8AC05A941E5C8F88',                                                                                                    #not used in game
            #'Throwing_96_E54BC06F473B117F989D24AE5A4BE099',                                                                                                    #pfft...
            #'SniperRifleXbow_100_EDD38CDE4347C31BB7CD5D96BAFBB9C5',                                                                                            #meant more fore receivers on enemies
            #'PistolXbow_103_C714EBC34C30624FEA6BA9AD4AB1B800',                                                                                                 #^^^
            #'AssaultRifleXbow_105_16A459F24C3FA050F7358BAE8C60CF7F',                                                                                           #^^^
            #'COVMagicBullet_109_0A55B6DB494ADEB57BD09488F7CB49E7',                                                                                             #^^^
            'TEDThrown_111_470AB0BD42FD364A51D571A4ED5805A2',
            'Companions_114_FD15483C4F409B00C74109BC7C9681BA',
            #'Barbarian_Skill_Ench_119_7338202B4C003CEF808C37B1EF62F1F2'                                                                                        #no way im about to have a whole entry for 1 enchant
            ]
        self.TypeStruct = [
            'Normal_26_00C5C4A64E4D62A6E142168CD3682B53',
            'Fire_27_B86BE45A4D32AF449A502DB4F7C6A5FC',
            'Shock_28_0DEF868B48EFA9D1D7C730956D617AEC',
            'Poison_33_09A06D2A411E425283DFF58D532EDEA8',
            'DarkMagic_34_EF2E31A34911FE1EB2EEC2AFD9A6450C',
            'Cryo_31_B8A29EEC49C43F47944AA3861600D35B',
            #'Void_37_0F9FD33F49A96011480048A6CB56A70B'                                                                                                         #Not used in game
            ]
def StatGetter():
    def __GetGame() -> str:
        """Returns \'Wonderlands\' or \'Borderlands3\' depending on the game."""
        return sys.executable.split('\\')[-1].replace('.exe','')
    game = __GetGame()
    stat_dct = {}
    def Att_comp_handler() -> dict[str,dict[str,dict[str,int]]]:#what is that output typing lol
        OakAttributeComponent = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.Pawn.BP_OakAttributeComponent
        struct_nme_props = ['DamageTypeModifiers','DamageSourceModifiers','DotDamageModifiers']                                                                 #to name keys in dict
        struct_dmg_props = ['TypeInstigatorMultipliers','SourceInstigatorMultipliers','EffectInstigatorMultipliers']                                            #attribute struct properties
        struct_tkn_props = ['TypeReceiverMultipliers','SourceReceiverMultipliers','EffectActorMultipliers']                                                     #^^^
        if game == 'Borderlands3':
            struct_data = bl3_struct_data()
        elif game == 'Wonderlands':
            struct_data = wl_struct_data()
        else:
            raise Exception('This mod is not compatible with this game.')
        att_comp_dct = {}
        for i in range(len(struct_nme_props)):
            tmp_dct = {}
            dmg_struct = getattr(OakAttributeComponent,struct_dmg_props[i])
            tkn_struct = getattr(OakAttributeComponent,struct_tkn_props[i])
            if struct_nme_props[i] == 'DamageSourceModifiers':
                struct_keys = struct_data.SourceStruct
            else:
                struct_keys = struct_data.TypeStruct
            for j in struct_keys:
                more_tmp_dct = {}
                more_tmp_dct['Dealt'] = getattr(dmg_struct,j).Value
                more_tmp_dct['Taken'] = getattr(tkn_struct,j).Value
                tmp_dct[j.split('_')[0]] = more_tmp_dct                                                                                                         #splitting to remove the GUID
            att_comp_dct[struct_nme_props[i]] = tmp_dct
        return att_comp_dct
    def damage_causer_handler():
        damage_causer = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.Pawn.DamageCauser
        tmp_dct = {}
        tmp_dct['DamageCauser'] = damage_causer.Value
        return tmp_dct

if __name__ == '__main__':
    StatGetter()