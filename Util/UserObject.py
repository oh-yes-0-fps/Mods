
from unrealsdk import *
import unrealsdk
from typing import Optional, Any

UserObject_lookup = {}

class UserObject:
    """
    
    
    """
    __python_fields__ = set(["p_Class", "p_Name", "p_Outer", "p_Template", "p_Object"])

    def __init__(self, Class:str, Name:str, Outer:unrealsdk.UObject = unrealsdk.GetEngine(), Template:Optional[UObject] = None) -> None:
        self.p_Class = Class
        self.p_Name = Name
        self.p_Outer = Outer
        self.p_Template = Template
        self.p_Object:unrealsdk.UObject = None
        full_name:str = f"{Outer.GetFullName()}.{Name}"
        # unrealsdk.Log(f"Found object {full_name}")
        # found_obj = unrealsdk.FindObject(Class, full_name)
        # if found_obj is not None:
        #     self.p_Object = found_obj
        #     unrealsdk.Log(f"Found object")
        # else:
        #     if Template:
        #         self.p_Object = unrealsdk.ConstructObject(Class = self.p_Class, Outer = self.p_Outer, Name = self.p_Name, Template = self.p_Template)
        #     else:
        #         self.p_Object = unrealsdk.ConstructObject(Class = self.p_Class, Outer = self.p_Outer, Name = self.p_Name)
        if Template:
            self.p_Object = unrealsdk.ConstructObject(Class = self.p_Class, Outer = self.p_Outer, Name = self.p_Name, Template = self.p_Template)
        else:
            self.p_Object = unrealsdk.ConstructObject(Class = self.p_Class, Outer = self.p_Outer, Name = self.p_Name)
        UserObject_lookup[full_name] = self
        unrealsdk.KeepAlive(self.p_Object)

    def UObject(self) -> UObject:
        return self.p_Object

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self.__python_fields__:
            return super().__setattr__(__name, __value)
        return self.p_Object.__setattr__(__name, __value)

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__python_fields__:
            return self.__getattr__(__name)
        return self.p_Object.__getattr__(__name)