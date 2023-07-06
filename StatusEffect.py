import unrealsdk as unrealsdk
from unrealsdk import *
from functools import lru_cache


class StatusEffectInterface:
    """
    Helps in StatusEffect based effects and functions
    """
    def __init__(self, Target_Actor: unrealsdk.UObject) -> None:
        """
        Args: Target_Actor will typically be the player
        """
        self.Actor = Target_Actor
        # self.SEM = Target_Actor.StatusEffectManagerComponent
        self.SE_static = unrealsdk.FindAll('OakStatusEffectsStatics')
        self.InstanceRefArray = []

    @property
    def WeaponDOTdmg(self):
        try:
            weapon = self.Actor.GetActiveWeapon(0)
            damage = weapon.CurrentFireComponent.Damage.Value
            dot_mult = weapon.UseModeState[weapon.CurrentUseMode].DamageModifierComponent.BaseStatusEffectDamageOverride.Value
            return damage * dot_mult
        except:
            return 0



    def Add(self, StatusEffectData: unrealsdk.UObject, NumOfStacks=1, DotOveride=0):
        """
        Used for adding a SE to the Target_Actor the class is made with\n
        If you want to add to another actor as if Target Actor applied it use \'.Affect\'\n
        args: 
            StatusEffect has to be UStatusEffectData or a child of that.\n
            NumOfStacks is the amound of stacks to apply(cannot exceed stacking strategy)\n
            DotOveride: if 0 remove dot, if above 0 apply that exact amount of dps,\n
                if negative apply 1/|<num>| of your guns dot to target, I.E. -1 is 100% of gun dot\n
                and -10 is 10% of gun dot
        """
        Target = self.Actor
        @lru_cache(maxsize=1)
        def __spec_constructer(self, SED, _Target, DotOV):
            """Doing this just for the sake of organization and traceback"""
            spec_dct = {
                'StatusEffectData': SED,
                'EffectOwner': None, #supposed to be weak obj pointer to a class but idk how to
                'EffectOwnerContextOverride': None,#^^^^^^
                'DurationType': {},#enum not implemented yet
                'Duration': 0.0,
                'EffectInstigator': _Target.GetController(),
                'DamageCauser': _Target,
                'DamagePerSecond': 0
                       }
            if DotOV != 0:
                spec_dct['StatusEffectData'].bDoesDamageOverTime = False
            if DotOV > 0:
                spec_dct['StatusEffectData'].bDoesDamageOverTime = True
                spec_dct['DamagePerSecond'] = DotOV
            if DotOV < 0:
                spec_dct['StatusEffectData'].bDoesDamageOverTime = True
                spec_dct['DamagePerSecond'] = self.WeaponDOTdmg / abs(DotOV)



            