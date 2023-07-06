import unrealsdk as unrealsdk
from unrealsdk import *
#Chaos_Mod\modifiers\gigantamax.py
class modifier:
    def __init__(self):
        self.name = "Smol Enemies"
        self.description = "Makes all enemies smaller"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World
        self.cached_cam_behavior = None
        self.default_cam = None

    def activate(self):
        pawn = self.pc.Pawn
        player_mesh = pawn.Mesh
        player_mesh.SetRelativeScale3D((3.5, 3.5, 3.5))
        # pawn.BaseEyeHeight = float(pawn.BaseEyeHeight) * 3.5
        # pawn.CrouchedEyeHeight = float(pawn.CrouchedEyeHeight) * 3.5
        fp = pawn.FirstPerson
        fp.Arms.SetRelativeScale3D((3.5, 3.5, 3.5))
        fp.Legs.SetRelativeScale3D((3.5, 3.5, 3.5))
        # fp.ViewModelOffsetList[0].Translation.Y = 100
        # fp.BaseViewModelLocationOffset.Y = 100
        cam_modes = pawn.CameraModesSet.Modes
        bfound_offset_behavior = False
        for mode in cam_modes:
            if mode.Name == 'CameraMode_ThirdPersonViewModel':
                for behavior in mode.Behaviors:
                    if behavior.Class.Name == 'CameraBehavior_OffsetCameraRelative':
                        self.cached_cam_behavior = behavior
                        bfound_offset_behavior = True
                        break
                break
        if bfound_offset_behavior:
            for mode in cam_modes:
                if mode.Name == 'CameraMode_Default':
                    self.default_cam = mode
                    # behavior_lst = list(mode.Behaviors)
                    # for b in range(len(behavior_lst)):
                    #     if behavior_lst[b].Class.Name == 'CameraBehavior_AnchorToSocket':
                    #         behavior_lst[b] = self.cached_cam_behavior
                    # mode.Behaviors = behavior_lst
                    mode.bIsFirstPerson = False
                    mode.bAutoPerspectiveOverride = True
                    unrealsdk.Log('Added behavior to CameraMode_Default')

    def deactivate(self):
        pawn = self.pc.Pawn
        player_mesh = pawn.Mesh
        player_mesh.SetRelativeScale3D((1, 1, 1))
        # pawn.BaseEyeHeight = float(pawn.BaseEyeHeight) / 3.5
        # pawn.CrouchedEyeHeight = float(pawn.CrouchedEyeHeight) / 3.5
        fp = pawn.FirstPerson
        fp.Arms.SetRelativeScale3D((1, 1, 1))
        fp.Legs.SetRelativeScale3D((1, 1, 1))
        # fp.ViewModelOffsetList[0].Translation.Y = 0
        # fp.BaseViewModelLocationOffset.Y = 0
        self.default_cam.bIsFirstPerson = True
        self.default_cam.bAutoPerspectiveOverride = False
        

if __name__ == '__main__':
    test = modifier()
    unrealsdk.Log("Modifier name: " + test.name)
    unrealsdk.Log("Modifier description: " + test.description)
    test.activate()
    def deactivate(a=(),b=(),c=()):
        test.deactivate()
        unrealsdk.Log("Modifier deactivated")
    unrealsdk.RemoveConsoleCommand("deactivate")
    unrealsdk.RegisterConsoleCommand("deactivate", deactivate)