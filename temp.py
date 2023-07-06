import unrealsdk as unrealsdk
from unrealsdk import *

from Mods.Data_Deriving import GetDatatableValue

columns = ['RarityWeightLevelBias_5_057BA6074423BC84C3853592FAE98B1F',
           'CommonWeightModifier_21_3D483428462299E5B6AF02B6CC0F65CC',
           'UncommonWeightModifier_12_A1CB19B648A9D93482D9DC83713A2FB5',
           'RareWeightModifier_16_F11E138D458B57D473F062A6C52A5F58',
           'VeryRareWeightModifier_17_8A0A186D4D4FC53ADDFB71A8A7F589DA',
           'LegendaryWeightModifier_18_B98DE11946C28DF64D94E197F7FED9BE']
tables = unrealsdk.FindAll('DataTable')
loot_tables = []
for i in tables:
    try:
        if i.RowStruct.Name == 'Struct_LootRarityModifierData':
            loot_tables.append(i)
    except:
        pass
static = unrealsdk.FindAll('DataTableFunctionLibrary')[0]
for i in loot_tables:
    unrealsdk.Log(static.GetDataTableRowNames(i, ['yes']))


# static = unrealsdk.FindAll('AttributeInitializer')[0]

# eMultiplier = 1
# eLevel = 2
# ePower = 22
# eOffset = 0
# unrealsdk.Log(eMultiplier*((eLevel**ePower)+eOffset))
# unrealsdk.Log(static.EvaluateBalanceFormula(
#     eMultiplier, eLevel, ePower, eOffset))

# def refresh():
#     PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
#     saved_skill_tree = PC.CurrentSavegame.AbilityData
#     ability_manager = PC.Pawn.AbilityManagerComponent
#     skill_tree = ability_manager.PlayerAbilityTree
#     def run(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
#         """used to refresh and apply skills properly and not have remnants from previous skill tree"""
#         ability_manager.PurchaseAbilityRespec()
#         end_points_left = saved_skill_tree.AbilityPoints
#         spec_guide = list(saved_skill_tree.TreeItemList)
#         tree_item_list = skill_tree.Items
#         for i in range(len(spec_guide)):
#             if spec_guide[i].MaxPoints != 0:
#                 tree_item = tree_item_list[i].ItemData
#                 for j in range(spec_guide[i].Points):
#                     # unrealsdk.Log(f'Purchasing {tree_item}', level = 5)
#                     skill_tree.AddPointToAbilityTreeItem(tree_item)
#                     skill_tree.ClientAddItemPoint(tree_item)
#         skill_tree.AbilityPoints = end_points_left
#         return True
#     unrealsdk.RunHook('/Script/OakGame.DiscoveryComponent.ClientDiscoverLevel', 'skill_refresh', run)
