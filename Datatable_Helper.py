import unrealsdk as unrealsdk
from unrealsdk import *
from Data_Deriving import GetObject, logtype, Get_cls_instance

#pyexec Datatable_Helper.py

def dump_struct(cls: unrealsdk.UClass) -> list:
    unrealsdk.Log(f'cls: {cls}')
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

class DataTable:
    def __init__(self, datatable:unrealsdk.UObject) -> None:
        self.Object = datatable

def test():
    dt_obj = GetObject('DataTable', '/Game/GameData/Loot/RarityWeighting/DataTable_Lootable_BalanceData.DataTable_Lootable_BalanceData')
    struct = dt_obj.RowStruct
    logtype(struct)
    unrealsdk.Log(f'Children: {struct.InnerProperty.Children}')

# def test2():
#     att_class = unrealsdk.FindClass("BP_OakAttributeComponent_C", True)
#     def get_cls_prop(cls: unrealsdk.UClass, name: str) -> unrealsdk.UProperty:
#         while cls:
#             prop = cls.Children
#             while prop:
#                 if prop.Name == name:
#                     return prop
#                 prop = prop.Next
#             cls = cls.SuperField
#     name = 'TypeInstigatorMultipliers'
#     struct = get_cls_prop(att_class, name).InnerProperty
#     logtype(struct)
#     unrealsdk.Log(f'Children: {struct.Children}')

def test3():
    dt_obj = GetObject('DataTable', '/Game/GameData/Loot/RarityWeighting/DataTable_Lootable_BalanceData.DataTable_Lootable_BalanceData')
    static = Get_cls_instance('DataTableFunctionLibrary')
    logtype(dt_obj)
    RowNames = []
    columns = static.GetDataTableRowNames(dt_obj, RowNames)
    unrealsdk.Log(f'Columns: {columns}')

test3()
# test()
# unrealsdk.Log('-----------------')
# test2()