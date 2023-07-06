import unrealsdk as unrealsdk
from unrealsdk import *
import random


def GetPlayerController() -> unrealsdk.UObject:
    """Returns the player controller BPChar"""
    PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
    return PC

class bpchar_scrubber:

    def __init__(self):
        self.bpchar = []
        self.team_blacklist = set(('Team_FriendlyToAll', 'Team_Players', 'Team_NonPlayers', 'Team_Neutral'))

    @property
    def player_team(self):
        return GetPlayerController().TeamComponent.Team

    def get_bpchar(self):
        out_lst = []
        spawners = unrealsdk.FindAll('SpawnFactory_OakAI', True)[2:]
        for spawner in spawners:
            if spawner.CachedTeam.Name not in self.team_blacklist:
                out_lst.append(spawner.AIActorClass)
        return out_lst

    def rand_bpchar_assign(self):
        spawners = unrealsdk.FindAll('SpawnFactory_OakAI', True)[2:]
        unrealsdk.Log('Getting BPChar')
        bpchar_list = self.get_bpchar()
        # unrealsdk.Log(bpchar_list)
        for spawner in spawners:
            if spawner.CachedTeam.Name not in self.team_blacklist:
                spawner.AIActorClass = random.choice(bpchar_list)
                unrealsdk.Log('set spawner')
        return True



# def spawner_randomizer(caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct):
#     main_class = bpchar_scrubber()
#     if params.WorldPackageName != '/Game/Maps/MenuMap/Loader':
#         unrealsdk.Log('Randomizing BPChar')
#         main_class.get_bpchar()
#         main_class.rand_bpchar_assign()
# unrealsdk.Log('Hooked enemy rand')
# unrealsdk.RunHook('/Script/Engine.PlayerController.ServerNotifyLoadedWorld', 'level_loaded_spawner_rand', spawner_randomizer)
enemies = unrealsdk.FindAll('BPChar_Enemy_C', True)
enemy_classes = set([])
for enemy in enemies:
    if 'Default__' in enemy.Name:
        enemy_classes.add(enemy.Class.Name)
with open('enemy_classes.txt', 'w') as f:
    for enemy in list(enemy_classes):
        f.write(enemy + '\n')