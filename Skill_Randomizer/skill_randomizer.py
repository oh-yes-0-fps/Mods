from typing import Callable
import unrealsdk as unrealsdk
from unrealsdk import *
import json
import random
from functools import lru_cache
from os.path import exists
from Mods.Util.SaveGameInterface import SaveGame

DEBUG = 3

def GetPlayerController() -> unrealsdk.UObject:
    """Returns the player controller BPChar"""
    PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
    return PC

def respec():
    unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController.Pawn.AbilityManagerComponent.PurchaseAbilityRespec()


class SkillRandomizer:
    """
    Class used for skill tree randomization.
    
    Step 1: Geta all possible skills from skills.json
    Step 2: Generate a tree structure list for the randomization
        with length being total of all skill slots with either a 0 for skill or 1 for augment
    Step 3: interate through the tree structure list and replace each item with an index of the chosen skill
    Step 4: Apply the tree structure list to the player's skill tree
    """
    def __init__(self,amc):
        self.amc = amc
        self.augment_class = unrealsdk.FindClass('OakPlayerAbilityTreeItemData_ActionAbilityAugment')
        self.ability_class = unrealsdk.FindClass('OakPlayerAbilityTreeItemData_Ability')
        self.selected_skills = []

    def curr_player(self):
        return str(GetPlayerController().Pawn.Name).replace('BPChar_', '').replace('_C', '')

    @property
    @lru_cache(maxsize=None)
    def Skills(self):
        skls = []
        with open('.\\Mods\\Skill_Randomizer\\skills.json','r') as f:
            jdata = json.load(f)
        skls.extend(jdata[self.curr_player()])
        skls.extend(jdata['ALL'])
        return skls

    def SkillTreeStructure(self):
        tree = []
        branches = list(self.amc.PlayerAbilityTree.TreeData.Branches)
        for branch in branches:
            for tier in branch.Tiers:
                for skill in tier.Items:
                    if int(skill.MaxPoints) > 0:
                        if skill.Class == self.augment_class:
                            tree.append(1)
                        elif skill.Class == self.ability_class:
                            tree.append(0)
        return tree


    def get_random_skill(self, binary: int):
        """Returns a random skill from the skill list"""
        if binary:
            is_augment = True
        else:
            is_augment = False
        tmp_lst = []
        for i in self.Skills:
            if i not in self.selected_skills:
                if i['is_augment'] == is_augment:
                    tmp_lst.append(i)
        if len(tmp_lst) == 0:
            unrealsdk.Log(f'No skills found with augment {is_augment}')
        skill = tmp_lst[int(random.randrange(0,len(tmp_lst)))]
        self.selected_skills.append(skill)
        return skill

    def __get_skill(self,skill_name: str):
        """Returns UClass of a skill from class name"""
        return unrealsdk.FindClass(skill_name)

    def __get_augment(self,augment_name: str):
        """Returns UObject of an augment from object name"""
        augments = unrealsdk.FindAll('OakActionAbilityAugmentData', True)
        if self.curr_player() != 'Gunner':
            for aug in augments:
                if augment_name in aug.Name:
                    return aug
        else:
            possible_aug_list = []
            for aug in augments:
                if augment_name in aug.Name:
                    possible_aug_list.append(aug)
            return random.choice(possible_aug_list)
        return None

    def RestoreSkillTree(self):
        """Restores the skill tree to the default state"""
        with open('.\\Mods\\Skill_Randomizer\\skills.json', 'r') as f:
            self.selected_skills = json.load(f)[self.curr_player()]
        self.ApplySkillTree(5)

    def SkillGetter(self):
        if 'SkillSelection' in SaveGame:
            SkillSelection = SaveGame['SkillSelection']
            if len(SkillSelection) > 0:
                self.selected_skills = SkillSelection
            else:
                return False
        else:
            tree_struct = self.SkillTreeStructure()
            self.selected_skills = list(map(self.get_random_skill,tree_struct))
            respec()
        SaveGame['SkillSelection'] = self.selected_skills
        return True

    def ApplySkillTree(self,points_per_tier: int):
        """Uses the class's selected_skills list to change the skill tree of the player"""
        unrealsdk.Log(self.selected_skills, level = DEBUG)
        branches = list(self.amc.PlayerAbilityTree.TreeData.Branches)
        skill_idx = 0
        for branch in branches:
            points_needed = -points_per_tier
            for tier in branch.Tiers:
                if points_needed < 1:
                    pass
                else:
                    tier.BranchPointsToUnlock = points_needed
                points_needed += points_per_tier
                for skill in tier.Items:
                    if int(skill.MaxPoints) > 0:# and str(skill.ItemDisplayType['Name']) == 'Passive'
                        if skill.Class == self.ability_class:
                            rand_skill = self.selected_skills[skill_idx]
                            skill.AbilityClass = self.__get_skill(rand_skill['AbilityName'])
                            skill.ItemFrameName = rand_skill['ItemFrameName']
                            skill.MaxPoints = rand_skill['MaxPoints']
                        elif skill.Class == self.augment_class:
                            rand_skill = self.selected_skills[skill_idx]
                            skill.AugmentData = self.__get_augment(rand_skill['AbilityName'])
                            skill.ItemFrameName = rand_skill['ItemFrameName']
                            skill.MaxPoints = rand_skill['MaxPoints']
                        skill_idx += 1
        unrealsdk.Log('Finished Applying skills', DEBUG)

    def debug(self):
        branches = list(self.amc.PlayerAbilityTree.TreeData.Branches)
        for branch in branches:
            for tier in branch.Tiers:
                unrealsdk.Log(f'{tier.BranchPointsToUnlock}', DEBUG)
                for skill in tier.Items:
                    if int(skill.MaxPoints) > 0 and str(skill.ItemDisplayType['Name']) == 'Passive':
                        unrealsdk.Log(f'{skill.Class} - {skill.ItemFrameName} - {skill.MaxPoints}', DEBUG)
                        if skill.Class == self.augment_class:
                            unrealsdk.Log(f'Augment: {skill.AugmentData}', DEBUG)
                        elif skill.Class == self.ability_class:
                            unrealsdk.Log(f'Ability: {skill.AbilityClass}', DEBUG)



def Register_CharacterLoadLate(func: Callable, seconds=3) -> None:
    """Registers a function to be called after the player is loaded"""
    def __LoadListener(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        unrealsdk.Log(f'listener called')
        delay_execution(func, seconds)
        return True
    unrealsdk.Log('Registering CharacterLoadLate')
    unrealsdk.RunHook('/Script/OakGame.OakCharacter_Player.ShowConnectEffect', 'StartListening_Skill', __LoadListener)

def delay_execution(func: Callable, delay: int, debug=False) -> None:
    global time_for_second
    global time_since_last_call
    time_since_last_call = 0
    time_for_second = 1
    def tick_handler(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        if caller == unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController:
            global time_for_second
            global time_since_last_call
            delta_second = params.DeltaSeconds
            time_for_second -= delta_second
            if time_for_second <= 0:
                time_for_second = 1 + time_for_second
                time_since_last_call += 1
            if time_since_last_call >= delay:
                func()
                unrealsdk.RemoveHook('/Script/Engine.Actor.ReceiveTick', f'{func.__name__}')
                time_since_last_call = 0
        return True
    unrealsdk.RunHook('/Script/Engine.Actor.ReceiveTick', f'{func.__name__}', tick_handler)

def run_randomizer():
    amc = GetPlayerController().Pawn.AbilityManagerComponent
    randomizer = SkillRandomizer(amc)
    if not randomizer.SkillGetter():
        return
    randomizer.ApplySkillTree(3)

def re_randomize(caller: unrealsdk.UObject, function = (),params = ()):
    del SaveGame['SkillSelection']
    run_randomizer()
    unrealsdk.Log('Re-Randomized', level = DEBUG)

def restore_skills(caller: unrealsdk.UObject, function = None,params = ()):
    reason = 'hooked'
    if function == None:
        respec()
        reason = 'command'
    amc = GetPlayerController().Pawn.AbilityManagerComponent
    SkillRandomizer(amc).RestoreSkillTree()
    unrealsdk.Log(f'Restored skill tree {reason}', level = DEBUG)
    return True

def skill_rand_disable(caller: unrealsdk.UObject, function = None,params = ()):
    if 'SkillSelection' in SaveGame:
        SaveGame['SkillSelection'] = []
        unrealsdk.Log('Disabled Skill Randomizer', level = DEBUG)
    return True

Register_CharacterLoadLate(run_randomizer, 3)
unrealsdk.RemoveConsoleCommand('rerandomize')
unrealsdk.RegisterConsoleCommand('rerandomize', re_randomize)
unrealsdk.RemoveConsoleCommand('restore_skills')
unrealsdk.RegisterConsoleCommand('restore_skills', restore_skills)
unrealsdk.RemoveConsoleCommand('skill_rand_disable')
unrealsdk.RegisterConsoleCommand('skill_rand_disable', skill_rand_disable)
unrealsdk.RunHook('/Script/OakGame.GFxPauseMenu.OnQuitChoiceMade', 'restore_quit', restore_skills)
unrealsdk.Log('Skill Randomizer Enabled')




