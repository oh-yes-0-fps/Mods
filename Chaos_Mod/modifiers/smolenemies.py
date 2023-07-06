import unrealsdk as unrealsdk
from unrealsdk import *

class modifier:
    def __init__(self):
        self.name = "Smol Enemies"
        self.description = "Makes all enemies smaller"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        def scale(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
            level = self.world.PersistentLevel
            enemies = unrealsdk.FindAll('BPChar_Enemy_C', True)
            for enemy in enemies:
                if enemy.Outer == level:
                    enemy_mesh = enemy.Mesh
                    enemy_mesh.SetRelativeScale3D((0.5, 0.5, 0.5))
            return True
        unrealsdk.RegisterHook('/Script/Engine.GbxSpawnActorAsyncManager.SpawnActorAsync', 'scale', scale)

    def deactivate(self):
        level = self.world.PersistentLevel
        enemies = unrealsdk.FindAll('BPChar_Enemy_C', True)
        for enemy in enemies:
            if enemy.Outer == level:
                enemy_mesh = enemy.Mesh
                enemy_mesh.SetRelativeScale3D((1, 1, 1))
        unrealsdk.RemoveHook('/Script/Engine.GbxSpawnActorAsyncManager.SpawnActorAsync', 'scale')