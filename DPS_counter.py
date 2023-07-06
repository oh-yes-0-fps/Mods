import unrealsdk as unrealsdk
from unrealsdk import *

######################################################################
##    CONFIGURATION
duration = 5       # Averages dps over this many seconds
auto_log = False   # to automatical log every 5 seconds
keybind = 'RightAlt'# keybind to log dps
######################################################################



class dps_counter:
    def __init__(self, time: float, auto_log: bool) -> None:
        self.auto_log = auto_log
        self.log_time = time.__round__()
        self.current_index = 0
        self.damage_lst = []
        for _ in range(self.log_time):
            self.damage_lst.append(0)

    @property
    def dps(self) -> float:
        return sum(self.damage_lst) / self.log_time

    def add_damage(self, damage: float) -> None:
        self.damage_lst[self.current_index] += damage

    def next_tick(self) -> None:
        self.current_index += 1
        if self.current_index >= self.log_time:
            if self.auto_log:
                unrealsdk.Log(f"DPS: {self.dps}")
            self.current_index = 0
        self.damage_lst[self.current_index] = 0

dps_counter_instance = dps_counter(duration, auto_log)
key = tuple([keybind])
PC = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
global time_for_second
time_for_second = 1
def tick_handler(caller: unrealsdk.UObject, function: unrealsdk.UFunction,params: unrealsdk.FStruct):
    if caller == PC:
        global time_for_second
        if PC.WasInputKeyJustPressed(key):
            unrealsdk.Log(f'DPS: {dps_counter_instance.dps}')
        delta_second = params.DeltaSeconds
        time_for_second -= delta_second
        if time_for_second <= 0:
            dps_counter_instance.next_tick()
            time_for_second = 1 + time_for_second
    return True

def damage_handler(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct):
    if params.InstigatedBy == PC:
        damage = params.Damage
        dps_counter_instance.add_damage(damage)
    return True

def dps_counter_start(a=(),b=(),c=()):
    unrealsdk.Log('DPS counter started')
    unrealsdk.RegisterHook('/Script/Engine.Actor.ReceiveTick', 'tickDPS', tick_handler)
    unrealsdk.RegisterHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'OnDamage', damage_handler)
def dps_counter_stop(a=(),b=(),c=()):
    unrealsdk.Log('DPS counter stopped')
    unrealsdk.RemoveHook('/Script/Engine.Actor.ReceiveTick', 'tickDPS')
    unrealsdk.RemoveHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'OnDamageDPS')

unrealsdk.RegisterConsoleCommand('DPS_start',dps_counter_start)
unrealsdk.RegisterConsoleCommand('DPS_stop',dps_counter_stop)

