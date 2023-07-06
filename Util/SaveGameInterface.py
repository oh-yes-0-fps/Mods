from os import getlogin, mkdir
from os.path import exists
from typing import Any, Callable
import unrealsdk as unrealsdk
from unrealsdk import *
import json

SAVE_PROPERTIES = set(
    [
    'SaveGameId',
    'bLevelledSaveNeedsFixup',
    'LastSaveTimestamp',
    'TimePlayedSeconds',
    'AccumulatedLevelPersistenceResetTimerSeconds',
    'LevelPersistenceData',
    'PlayerClassData',
    'ResourcePools',
    'SavedRegions',
    'ExperiencePoints',
    'GameStatsData',
    'InventoryCategoryList',
    'InventoryItems',
    'EquippedInventoryList',
    'ActiveWeaponList',
    'AbilityData',
    'LastPlayThroughIndex',
    'PlaythroughsCompleted',
    'bShowNewPlaythroughNotification',
    'MissionPlaythroughsData',
    'ActiveTravelStationsForPlaythrough',
    'DiscoveryData',
    'LastActiveTravelStationForPlaythrough',
    'VehiclesUnlockedData',
    'VehiclePartsUnlocked',
    'VehicleLoadouts',
    'VehicleLastLoadoutIndex',
    'OakChallengeData',
    'SDUList',
    'SelectedCustomizations',
    'EquippedEmoteCustomizations',
    'SelectedColorCustomizations',
    'CrewQuartersRoom',
    'CrewQuartersGunRack',
    'UnlockedEchoLogs',
    'bHasPlayedSpecialEchoLogInsertAlready',
    'NicknameMappings',
    'GameStateSaveDataForPlaythrough',
    'ChallengeCategoryCompletionPcts',
    'CharacterSlotSaveGameData',
    'UITrackingSaveGameData',
    'PreferredGroupMode',
    'TimeOfDayData',
    'ZoneMapFODSavedData',
    'bIsNetReplicating',
    'CharacterGuardianRank',
    'ProfileChallengeDataForSerialization',
    'bOptionalObjectiveRewardFixupApplied',
    'bVehiclePartRewardsFixupApplied',
    'bLevelledSaveVehiclePartRewardsFixupApplied',
    'LastActiveLeague',
    'LastActiveLeagueInstance',
    'ActiveLeagueInstanceForEvent',
    'CurrentVaultCardDaySeed',
    'CurrentVaultCardWeekSeed',
    'PreferredCharacterName',
    'NameCharacterLimit',
    'GuardianRank',
    'LastActiveTravelStation',
    'GameStateSaveData',
    'ActiveTravelStations',
    ]
)


class PySaveGame:
    """
    A Pyhton Accessible Save Game

    Structured as a dictionary, with the keys being the names of the save game properties.

    Extends the save game object and stores that data in a json file

    Gets current save game so will change what save its interfacing with upon changing characters
    """
    def __init__(self):
        self.savegame = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.CurrentSavegame
        self.savegame_properties = SAVE_PROPERTIES
        self.json_properties = set([])
        self.jdata = {}
        self.json_path = f'C:\\Users\\{getlogin()}\\Documents\\My Games\\Borderlands 3\\Saved\\SaveGames\\JSON'
        if not exists(self.json_path):
            mkdir(self.json_path)
        if self.savegame:
            self.read_json()
        self.savegame_functions = []
        unrealsdk.Log('PySaveGame Initialized', level=4)

    
    @property
    def SaveName(self) -> str:
        if self.savegame:
            return hex(self.savegame.SaveGameId)[2:].upper()
        else:
            return None

    def add_savegame_function(self, func: Callable) -> None:
        self.savegame_functions.append(func)
        def __hook_savegame_functions(self) -> None:
            for func in self.savegame_functions:
                unrealsdk.RunHook('/Script/OakGame.GFxExperienceBar.HandleSkillPointsChanged',f'Skill_Point_{func.__name__}',func)
                unrealsdk.RunHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade',f'On_Quit_{func.__name__}',func)
                unrealsdk.RunHook('/Script/OakGame.OakCharacter.AddedToInventory',f'Added_Item_{func.__name__}',func)
                unrealsdk.RunHook('/Script/OakGame.OakCharacter.RemovingFromInventory',f'Removed_Item_{func.__name__}',func)

    def remove_savegame_function(self, func: Callable) -> None:
        self.savegame_functions.remove(func)
        unrealsdk.RemoveHook('/Script/OakGame.GFxExperienceBar.HandleSkillPointsChanged',f'Skill_Point_{func.__name__}')
        unrealsdk.RemoveHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade',f'On_Quit_{func.__name__}')
        unrealsdk.RemoveHook('/Script/OakGame.OakCharacter.AddedToInventory',f'Added_Item_{func.__name__}')
        unrealsdk.RemoveHook('/Script/OakGame.OakCharacter.RemovingFromInventory',f'Removed_Item_{func.__name__}')


    def refresh(self) -> None:
        self.__init__()

    def read_json(self) -> None:
        try:
            with open(f'{self.json_path}\\{self.SaveName}.json', 'r') as f:
                data = dict(json.load(f))
            self.json_properties = set(data.keys())
            self.jdata = data
        except FileNotFoundError:
            with open(f'{self.json_path}\\{self.SaveName}.json', 'w') as f:
                json.dump({}, f)
            self.json_properties = set([])
            self.jdata = {}
        return None

    def __write_json(self) -> None:
        with open(f'{self.json_path}\\{self.SaveName}.json', 'w') as f:
            json.dump(self.jdata, f)
        return None

    def __getitem__(self, __key: str) -> Any:
        if __key in self.json_properties:
            return self.jdata[__key]
        elif __key in self.savegame_properties:
            return getattr(self.savegame, __key)
        else:
            raise KeyError(f'{__key} is not a valid key')
    
    def __setitem__(self, __key: str, __value: Any) -> None:
        if __key in self.savegame_properties:
            setattr(self.savegame, __key, __value)
        else :
            self.jdata[__key] = __value
            self.json_properties.add(__key)
            self.__write_json()

    def __delitem__(self, __key: str) -> None:
        if __key in self.json_properties:
            del self.jdata[__key]
            self.json_properties.remove(__key)
            self.__write_json()
        elif __key in self.savegame_properties:
            raise KeyError(f'{__key} is a save game property and cannot be deleted')
        else:
            raise KeyError(f'{__key} is not a valid key')

    def __contains__(self, __key: str) -> bool:
        return __key in self.json_properties or __key in self.savegame_properties

    def __iter__(self) -> Callable:
        raise NotImplementedError('Iterating over a PySaveGame is not supported')

    def __len__(self) -> int:
        return len(self.json_properties) + len(self.savegame_properties)

    def __repr__(self) -> str:
        return f'<PySaveGame: {hex(self.savegame.SaveGameId)}>'

    def __str__(self) -> str:
        return f'<PySaveGame: {hex(self.savegame.SaveGameId)}>'

    def __dir__(self) -> list:
        return list(self.json_properties) + list(self.savegame_properties)
    ###Not sure if this is a good idea, wonder if i can make it completely attr based
    # def __getattribute__(self, __key: str) -> Any:
    #     if __key in SAVE_PROPERTIES and self.savegame:
    #         return getattr(self.savegame, __key)
    #     else:
    #         raise AttributeError(f'{__key} is not a valid attribute')

    # def __setattr__(self, __key: str, __value: Any) -> None:
    #     if __key in SAVE_PROPERTIES and self.savegame:
    #         setattr(self.savegame, __key, __value)
    #     else:
    #         raise AttributeError(f'{__key} is not a valid attribute')

SaveGame = PySaveGame()
def refresh_map_load(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
    if caller.GetOwner().Class.Name == 'BPCont_Player_C':
        if unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.CurrentSavegame != None:
            SaveGame.savegame = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.CurrentSavegame
            unrealsdk.Log(f'Current Save Game: {SaveGame.savegame}', level = 5)
            SaveGame.read_json()
    return True
# unrealsdk.RunHook('/Script/OakGame.OakPlayerController.ServerSetReadyForSaveGameChannel', 'map_load', refresh_map_load)
unrealsdk.RunHook('/Script/OakGame.DiscoveryComponent.ClientDiscoverLevel', 'map_load', refresh_map_load)
def refresh_save_quit(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
    SaveGame.savegame = None
    SaveGame.jdata = {}
    SaveGame.json_properties = set([])
    # unrealsdk.Log('Save Game Quit')
    return True
unrealsdk.RunHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade', 'save_quit', refresh_save_quit)



def example():
    #reading data from unreal save game object
    data = SaveGame['SDUList']
    #writing data to unreal save game object
    SaveGame['SDUList'] = data

    #you have to write to the json file before reading from it
    #any key writen to savegame tahts not an unreal property will be stored in the json file
    SaveGame['test'] = 'test'
    #reading data from json file
    data = SaveGame['test']