# import unrealsdk as unrealsdk
# from unrealsdk import *
from typing import Callable, Union, Any, overload, Optional
# from bl3_typing import UGameEngine

# This isn't meant to actually be used, it's just a placeholder for the type hinting
# The idea is it can be for testing and such but should never publish a mod depending up this


#################$Base Functions$#################
#hook stuff
def RegisterHook(unrealFuncPath: str, hookName: str, hookFunc: Callable) -> None:
    """
    Registers a hook to a function\n
    Upon the hooked unreal function being called the python func will run\n
    Hooked python funcs need to take in 3 arguments that will be\n
      caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct\n
    You can find the unreal function path by finding it by name in the SDKDumps\n
    Args:\n
        unrealFuncPath (str): The path to the function to hook\n
        hookName (str): The name of the hook\n
        hookFunc (Callable): The function to call when the hooked function is called
    """

def RemoveHook(unrealFuncPath: str, hookName: str) -> None:
    """
    Removes a hook from a function\n
    If hook does not exist will do nothing
    Args:\n
        unrealFuncPath (str): The path to the function to remove the hook from\n
        hookName (str): The name of the hook to remove
    """

def RunHook(unrealFuncPath: str, hookName: str, hookFunc: Callable) -> None:
    """
    Removes then Registers a hook to ensure it uses newest code\n
    Upon the hooked unreal function being called the python func will run\n
    Hooked python funcs need to take in 3 arguments that will be\n
      ^caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct\n
    You can find the unreal function path by finding it by name in the SDKDumps\n
    Args:\n
        unrealFuncPath (str): The path to the function to hook\n
        hookName (str): The name of the hook\n
        hookFunc (Callable): The function to call when the hooked function is called
    """

def RegisterConsoleCommand(CommandName: str, CommandFunc: Callable) -> None:
    """
    Registers a console command\n
    function passed in must have 3 arguments, last 2 with default values\n
    Args:\n
        CommandName (str): The name of the command\n
        CommandFunc (Callable): The function to call when the command is run
    """

def RemoveConsoleCommand(CommandName: str) -> None:
    """
    Removes a console command\n
    If command is not registered it does nothing
    Args:\n
        CommandName (str): The name of the command to remove
    """






#Base object stuff
def KeepAlive(obj: UObject) -> None:
    """
    Keeps an object alive\n
    This will try to prevent the object from being garbage collected\n
    Args:\n
        obj (unrealsdk.UObject): The object to keep alive
    """

def ConstructObject(Class: str, Outer: UObject = GetEngine(), Name: str = "", Template: UObject = UObject(),SetFlags: int = 0x1) -> UObject:
    """
    Will construct an object of the given class name\n
    If Template is given the new objects properties will be created as identical to template\n
    Args:\n
        ClassName (str): The name of the class to construct\n
        Outer (unrealsdk.UObject): The outer of the object to construct\n
        Name (str): The name of the object to construct\n
        Template (unrealsdk.UObject): The object to copy properties from\n
        SetFlags (int): The flags to set on the object\n
    Returns:\n
        unrealsdk.UObject: The object constructed
    """
    # InternalSetFlags = 0x00
    # CopyTransientsFromDefault = 0x0
    # InstanceGraph = None
    # bAssumeTemplateIsArchetype = False

def GetEngine() -> UObject:
    """
    Returns the UGameEngine object
    Returns:\n
        unrealsdk.UObject: The engine object
    """

def LoadPackage(PackageName: str, flags:int = 0, force:bool = False) -> UPackage:
    """
    Loads a package\n
    Args:\n
        PackageName (str): The name of the package to load\n
        flags (int): The flags to load the package with\n
        force (bool): If true will force the package to load\n
    Returns:\n
        unrealsdk.UPackage: The package loaded
    """

#Find stuff
def FindObject(Class:Union[str,UClass], ObjectFullName:str) -> UObject:
    """
    Finds an object by its full name\n
    Can either supply a class or a string of the class name\n
    You can find the full name of an object by looking at the SDKDumps\n
    Args:\n
        Class (str or unrealsdk.UClass): The class of the object to find\n
        ObjectFullName (str): The full name of the object to find\n
    Returns:\n
        unrealsdk.UObject: The object found
    """

def FindAll(ClassName: str, FindSubclasses:bool = False) -> list[UObject]:
    """
    Finds all loaded objects of the given class name\n
    Args:\n
        ClassName (str): The name of the class to find\n
        FindSubclasses (bool): If true will find all subclasses of the given class\n
    Returns:\n
        list[unrealsdk.UObject]: A list of all objects of the given class
    """

def FindClass(ClassName: str) -> UClass:
    """
    Finds a class by its name\n
    Args:\n
        ClassName (str): The name of the class to find\n
    Returns:\n
        unrealsdk.UClass: The class found
    """

#Logging
def CallPostEdit(NewValue: bool) -> None:
    """TODO: Add description"""

def DoInjectedCallNext() -> None:
    """TODO: Add description"""

def LogAllCalls(Enabled: bool) -> None:
    """
    While enabled all object function calls will be logged to the unrealsdk.log\n
    Only ProcessEvent, ProcessEvent and staticexec will be logged so native functions aren't\n
    Args:\n
        Enabled (bool): True to enable logging, False to disable
    """

#Realized i can't do this because its not in the sdk
# class LogLevels:
#     WARNING = -1
#     INFO = 0
#     CONSOLE = 2
#     MISC = 4
#     HOOKS = 6
#     INTERNAL = 8

def Log(*args:Any, level:int = 0) -> None:
    """
    Logs a function call to the unrealsdk.log\n
    Can pass in any number of strings to log in 1 line\n
      ^w/o spaces inbetween them\n
    To set level u have to use the Level=int keyword argument\n
    Args:\n
        Args([]str): The strings to log out\n
        level(int): The logging level to use, 0 is default\n
    """

def SetConsoleLogLevel(Level:int = 4) -> None:
    """
    Sets the logging level for the console\n
    Args:\n
        Level (int): The logging level to use, 4 is default
    """

def SetFileLogLevel(Level:int = 4) -> None:
    """
    Sets the logging level for the file\n
    Args:\n
        Level (int): The logging level to use, 4 is default
    """

def GetVersion() -> tuple[int, int, int]:
    """
    Returns the version of the sdk as a tuple\n
    Returns:\n
        tuple[int, int, int]: The version of the sdk
    """

#################$Base Classes$#################

class UObject:
    """
    Base Object for all unreal objects
    """
    def __init__(self): ...

    Class: UClass
    Name: str
    Outer: UObject
    ObjectFlags: int
    InternalIndex: int

    @staticmethod
    def StaticClass() -> UClass:
        """
        Returns:\n
            unrealsdk.UClass: The class of the object
        """

    @staticmethod
    def FindClass(ClassName: str) -> UClass:
        """
        Finds a class by its name\n
        Args:\n
            ClassName (str): The name of the class to find\n
        Returns:\n
            unrealsdk.UClass: The class found
        """

    @staticmethod
    def FindObjectsRegex(Regex: str) -> list[UObject]:
        """
        Finds all objects whose names match the given regex\n
        Args:\n
            Regex (str): The regex to match\n
        Returns:\n
            list[unrealsdk.UObject]: A list of all objects that match the regex
        """

    @staticmethod
    def FindObjectsContaining(String: str) -> list[UObject]:
        """
        Finds all objects whose names contain the given string\n
        Args:\n
            String (str): The string to match\n
        Returns:\n
            list[unrealsdk.UObject]: A list of all objects that match the string
        """

    @staticmethod
    def FindAll(ClassName: str, FindSubclasses:bool = False) -> list[UObject]:
        """
        Finds all loaded objects of the given class name\n
        Args:\n
            ClassName (str): The name of the class to find\n
            FindSubclasses (bool): If true will find all subclasses of the given class\n
        Returns:\n
            list[unrealsdk.UObject]: A list of all objects of the given class
        """

    @staticmethod
    def FindObject(Class: UClass, ObjectFullName: str) -> UObject:
        """
        Finds an object by its full name\n
        Args:\n
            Class (unrealsdk.UClass): The class of the object to find\n
            ObjectFullName (str): The full name of the object to find\n
        Returns:\n
            unrealsdk.UObject: The object found
        """

    def GetPackageObject(self) -> UPackage:
        """
        Returns:\n
            unrealsdk.UPackage: The package the object is in
        """

    def GetNameCpp(self) -> str:
        """
        Returns:\n
            str: The name of the object in C++ format
        """

    def DumpObject(self) -> None:
        """
        Logs all the fields of the object and their values to the log\n
        """

    def GetAddress(self) -> int:
        """
        Returns:\n
            int: The address of the object
        """

    def GetFullName(self) -> str:
        """
        Returns:\n
            str: {class name} {object outers}.{object name}
        """

    def GetName(self) -> str:
        """
        Returns:\n
            str: {object outers}.{object name}
        """

    def ExecuteUbergraph(self, Entry: int) -> None:
        """
        Will run the objects uber graph with the entry point\n
        Note: This isn't a part of unrealsdk explicitly but every UObject has it so
        """

    def __repr__(self) -> str:
        """
        Returns:\n
            str: GetFullName()
        """

class UField(UObject):
    def __init__(self): ...

    Next: UField

class UStruct(UField):
    def __init__(self): ...

    SuperField: UStruct
    Children: UField
    PropertySize: int

    def FindChildByName(self, Name: str) -> UField:
        """
        Finds a child field by its name\n
        Args:\n
            Name (str): The name of the field to find\n
        Returns:\n
            unrealsdk.UField: The field found
        """

class FStruct:
    def __init__(self): ...
    
    structType: UStruct

    def GetBase(self) -> Any:
        """
        Returns:\n
            unrealsdk.FStruct: The base struct
        """

class UClass(UStruct):
    def __init__(self): ...
    

    ClassCastFlags: int
    ClassConfigName: str
    ClassDefaultObject: UObject
    ClassFlags: int

    bCooked:bool

    def GetProperties(self) -> list[UProperty]:
        """
        Returns:\n
            list[unrealsdk.UProperty]: A list of all properties in the struct
        """

    def GetFunctions(self) -> list[UFunction]:
        """
        Returns:\n
            list[unrealsdk.UFunction]: A list of all functions in the struct
        """

class UScriptStruct(UStruct):
    def __init__(self): ...

class UFunction(UStruct):
    def __init__(self): ...

    FunctionFlags: int
    RepOffset: int
    NumParms: int
    ParamsSize: int
    ReturnValueOffset: int
    Func: UStruct

class FFunction:
    def __init__(self): ...

    obj: UObject
    func: UFunction

    def __call__(self, *args: Any, **kwds: Any) -> Any: ...

class UPackage(UObject):
    def __init__(self): ...

class FArray:
    def __init__(self): ...

    def __getitem__(self, index: int) -> Any: ...

    def __setitem__(self, index: int, value: Any) -> None: ...

    def __iter__(self) -> Any: ...

    def __next__(self) -> Any: ...

    def __repr__(self) -> str: ...

    def __len__(self) -> int: ...

class UEnum(UField):
    #TODO
    def __init__(self): ...

class UConsole(UObject):
    def __init__(self): ...

    Scrollbakck: list[str]
    SBHead: int
    SBPos: int
    ConsoleSettings: UObject

class UProperty(UField):
    def __init__(self): ...

    ArrayDim: int
    ElementSize: int
    PropertyFlags: int
    RepIndex: int
    BlueprintReplicationCondition: int
    Offset_Internal: int
    RepNotifyFunc: str
    PropertyLinkNext: UProperty
    NextRef: UProperty
    DestructorLinkNext: UProperty
    PostConstructLinkNext: UProperty

class UStructProperty(UProperty):
    def __init__(self): ...
    InnerProperty: UStruct

class UStrProperty(UProperty):
    def __init__(self): ...

class UObjectProperty(UProperty):
    def __init__(self): ...
    PropertyClass: UClass

class UBoolProperty(UProperty):
    def __init__(self): ...

class UByteProperty(UProperty):
    def __init__(self): ...

class UFloatProperty(UProperty):
    def __init__(self): ...

class UIntProperty(UProperty):
    def __init__(self): ...

class UNameProperty(UProperty):
    def __init__(self): ...

class UArrayProperty(UProperty):
    def __init__(self): ...
    Inner: UProperty

class UDelegateProperty(UProperty):
    def __init__(self): ...

class UEnumProperty(UField):
    def __init__(self): ...

class UClassProperty(UProperty):
    def __init__(self): ...

class UInterfaceProperty(UProperty):
    def __init__(self): ...
    InterfaceClass: UClass

class UMapProperty(UProperty):
    def __init__(self): ...

class FScriptInterface:
    def __init__(self): ...

    ObjectPointer: UObject
    InterfacePointer: None

    def GetAddress(self) -> int: ...
    def GetInterfacePointer(self) -> int: ...


class FName:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string:str): ...
    @overload
    def __init__(self, string:str, index:int): ...

    Index: int
    Number: int

    @staticmethod
    def Names() -> list[FNameEntry]:
        """Returns a list of all FNames being used"""
    def GetName(self) -> str: ...

class FNameEntry:
    def __init__(self): ...
    Name: str

class FOutputDevice:
    def __init__(self): ...
    VfTable:None
    bSuppressEventTag:bool
    bAutoEmitLineTerminator:bool

class FFrame(FOutputDevice):
    def __init__(self) -> None: ...
    Node:UFunction
    Object:UObject
    PreviousFrame:FFrame
    Code: int
    Locals: int
    def SkipFunction(self) -> None: ...

class FString:
    def __init__(self, string:str): ...
    Count: int
    Max: int
    Data: Optional[str]

    def AsString(self) -> str: ...

class FScriptDelegate:
    def __init__(self, obj:UObject, name:str): ...

    def IsBound(self) -> bool: ...
    def ToString(self) -> str: ...

    def __repr__(self) -> str: ...

class FSoftObject:
    def __init__(self): ...

    object: UObject
    asset_path: str

class FSoftClass:
    def __init__(self): ...

    object: UClass
    asset_path: str