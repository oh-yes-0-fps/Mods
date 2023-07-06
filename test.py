from __future__ import annotations
from secrets import choice
try:
    import Mods.bl3_typing as bl3
except ImportError:
    pass
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Editor Only

import unrealsdk as unrealsdk
from unrealsdk import *
# , GetDatatableRow
from Mods.Util.Data_Deriving import GetAttValue, GetObject, GetDatatableValue

# Notes
# Local = BalanceStateComponent -> BalanceTableRowHandle/InheritedBalanceTableRowHandle
# Global = OakModifierManagerActor
#
#
# /Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary

modifier_manager = unrealsdk.FindAll('OakModifierManagerActor')[1]
fields = ['GlobalRarityWeightLevelBias',
          'GlobalCommonRarityWeightModifier',
          'GlobalUncommonRarityWeightModifier',
          'GlobalRareRarityWeightModifier',
          'GlobalVeryRareRarityWeightModifier',
          'GlobalLegendaryRarityWeightModifier']

itemRarityTable = {
    "Common": {
        'IntroductionLevel': 0,
        'BaseWeight': 100,
        'ExponentForGrowthRate': 0,
        'RarityWeightLevelBiasMultiplier': 0,
        'GlobalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityModifier_01_Common.Att_RarityModifier_01_Common'),
        'LocalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_LocalRarityModifier_01_Common.Att_LocalRarityModifier_01_Common'),
        'WEIGHT': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_01_Common.Att_RarityWeight_01_Common')
    },
    "Uncommon": {
        'IntroductionLevel': 0,
        'BaseWeight': 5,
        'ExponentForGrowthRate': 0.3,
        'RarityWeightLevelBiasMultiplier': 0,
        'GlobalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityModifier_02_Uncommon.Att_RarityModifier_02_Uncommon'),
        'LocalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_LocalRarityModifier_02_Uncommon.Att_LocalRarityModifier_02_Uncommon'),
        'WEIGHT': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_02_Uncommon.Att_RarityWeight_02_Uncommon')
    },
    "Rare": {
        'IntroductionLevel': 0,
        'BaseWeight': 0.5,
        'ExponentForGrowthRate': 0.35,
        'RarityWeightLevelBiasMultiplier': 0,
        'GlobalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityModifier_03_Rare.Att_RarityModifier_03_Rare'),
        'LocalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_LocalRarityModifier_03_Rare.Att_LocalRarityModifier_03_Rare'),
        'WEIGHT': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_03_Rare.Att_RarityWeight_03_Rare')
    },
    "VeryRare": {
        'IntroductionLevel': 0,
        'BaseWeight': 0.05,
        'ExponentForGrowthRate': 0.5,
        'RarityWeightLevelBiasMultiplier': 0,
        'GlobalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityModifier_04_VeryRare.Att_RarityModifier_04_VeryRare'),
        'LocalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_LocalRarityModifier_04_VeryRare.Att_LocalRarityModifier_04_VeryRare'),
        'WEIGHT': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_04_VeryRare.Att_RarityWeight_04_VeryRare')
    },
    "Legendary": {
        'IntroductionLevel': 0,
        'BaseWeight': 0.001,
        'ExponentForGrowthRate': 0.5,
        'RarityWeightLevelBiasMultiplier': 0,
        'GlobalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityModifier_05_Legendary.Att_RarityModifier_05_Legendary'),
        'LocalWeightModifierAttribute': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_LocalRarityModifier_05_Legendary.Att_LocalRarityModifier_05_Legendary'),
        'WEIGHT': GetObject('GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_05_Legendary.Att_RarityWeight_05_Legendary')
    }
}


def __Datatable_test():
    unrealsdk.Log('== Datatable_test ==')
    dt_obj = GetObject(
        'DataTable', '/Game/GameData/Loot/RarityWeighting/DataTable_ItemRarity.DataTable_ItemRarity')
    row_name = 'Legendary'
    column_name = 'RarityWeightLevelBiasMultiplier_19_7300719D4F7F4FC6DF1BFEB015FF4364'
    out_value = GetDatatableValue(dt_obj, row_name, column_name)
    unrealsdk.Log(f'    {out_value}')


def EvaluateBalanceFormula(multiplier: float, level: float, power: float, offset: float) -> float:
    return multiplier*((level**power)+offset)


def UApplyRarityWeightLevelBias(LevelToDetermineRarityAt: float, GlobalRarityWeightLevelBias: float, LocalRarityWeightLevelBias: float, RarityWeightLevelBiasMultiplier: float, __WorldContext: UObject) -> float:
    return ((GlobalRarityWeightLevelBias + LocalRarityWeightLevelBias)*RarityWeightLevelBiasMultiplier) + LevelToDetermineRarityAt


def UCalculateRarityWeight(RarityTableRowHandle: str, LevelToDetermineRarityAt: float, GlobalRarityWeightLevelBias: float, LocalRarityWeightLevelBias: float, GlobalRarityWeightModifier: float, LocalRarityWeightModifier: float, __WorldContext: UObject) -> float:
    table_row = itemRarityTable.get(RarityTableRowHandle, None)
    if table_row is None:
        return -1
    if LevelToDetermineRarityAt < table_row['IntroductionLevel']:
        return 0
    biased_level = UApplyRarityWeightLevelBias(LevelToDetermineRarityAt, GlobalRarityWeightLevelBias,
                                               LocalRarityWeightLevelBias, table_row['RarityWeightLevelBiasMultiplier'], __WorldContext)
    formula_result = EvaluateBalanceFormula(
        table_row['BaseWeight'], biased_level, table_row['ExponentForGrowthRate'], 0)
    return (formula_result * GlobalRarityWeightModifier) * LocalRarityWeightModifier


def ValueResolver(RarityTableRowHandle: str, context: UObject) -> float:
    table_row = itemRarityTable.get(RarityTableRowHandle, None)
    if table_row is None:
        return -1
    LocalRarityWeightLevelBias = GetAttValue(GetObject(
        'GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_LocalRarityWeightLevelBias.Att_LocalRarityWeightLevelBias'), pawn=context)
    GlobalRarityWeightLevelBias = GetAttValue(GetObject(
        'GbxAttributeData', '/Game/GameData/Loot/RarityWeighting/Att_GlobalRarityWeightLevelBias.Att_GlobalRarityWeightLevelBias'), pawn=context)
    GameStage = GetAttValue(GetObject(
        'GbxAttributeData', '/Game/GameData/Attributes/Att_GameStage.Att_GameStage'), pawn=context)
    LocalWeightModifierAttribute = GetAttValue(
        table_row['LocalWeightModifierAttribute'], pawn=context, default=1)
    GlobalWeightModifierAttribute = GetAttValue(
        table_row['GlobalWeightModifierAttribute'], pawn=context, default=1)
    return UCalculateRarityWeight(RarityTableRowHandle, GameStage, GlobalRarityWeightLevelBias, LocalRarityWeightLevelBias, GlobalWeightModifierAttribute, LocalWeightModifierAttribute, context)


if __name__ == '__main__':
    import random
    level = unrealsdk.GetEngine().GameViewport.World.PersistentLevel
    enemies = unrealsdk.FindAll('BPChar_Enemy_C', True)
    enemies = [x for x in enemies if 'Default__' not in x.Name]
    context = choice(enemies)
    unrealsdk.Log(context)
    unrealsdk.Log('=== RarityWeight ===')
    weight = itemRarityTable['Legendary']['WEIGHT']
    unrealsdk.Log(
        f'    Legendary - {ValueResolver("Legendary", context)} vs {GetAttValue(weight, pawn=context)}')
    weight = itemRarityTable['VeryRare']['WEIGHT']
    unrealsdk.Log(
        f'    VeryRare - {ValueResolver("VeryRare", context)} vs {GetAttValue(weight, pawn=context)}')
    weight = itemRarityTable['Rare']['WEIGHT']
    unrealsdk.Log(
        f'    Rare - {ValueResolver("Rare", context)} vs {GetAttValue(weight, pawn=context)}')
    weight = itemRarityTable['Uncommon']['WEIGHT']
    unrealsdk.Log(
        f'    Uncommon - {ValueResolver("Uncommon", context)} vs {GetAttValue(weight, pawn=context)}')
    weight = itemRarityTable['Common']['WEIGHT']
    unrealsdk.Log(
        f'    Common - {ValueResolver("Common", context)} vs {GetAttValue(weight, pawn=context)}')
    __Datatable_test()
