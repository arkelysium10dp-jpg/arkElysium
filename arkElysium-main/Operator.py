from dataclasses import dataclass

from Object import TriggerBox, Object


"""
hp = max_hp
sp = max_sp
position: 0/1 (Melee, Ranged)
type_sp: 'PASSIVE' / 'OFFENSIVE'
defence: int
resistance: int
dmg: int
atk_speed: float
dmg_type: 0/1/2 'PHYSICAL' / 'ARTS' / 'TRUE'
dmg_area: Hitbox
dp_cost: int
init_sp: int
block: int
redeployment_time: float
direction: 0/1/2/3 (right, up, left, down)
"""
@dataclass
class OperatorData:

    # Attributes Declaration
    # using Type Hints
    hp: int
    sp: int
    position: int
    type_sp: int
    defence: int
    resistance: int
    dmg: int
    atk_speed: float
    dmg_type: int
    dmg_area: TriggerBox
    dp_cost: int
    init_sp: int
    block: int
    redeployment_time: float
    script: None | str


class OperatorObject(Object):
    def __init__(self, hp: int, sp: int, type_sp, defence: int, resistance: float, dmg: int, atk_speed: int, dmg_type,
                 dmg_area, direction, dp_cost: int, block:int, redeployment_time: float,
                 surface, x, y, anim = None, script = lambda a: None, hoverbox: TriggerBox = None, init_sp=0):
        super().__init__(surface, x, y, anim, script, hoverbox)
        self.max_hp = hp
        self.hp = hp
        self.max_sp = sp
        self.sp = init_sp
        self.type_sp = type_sp
        self.defence = defence
        self.resistance = resistance
        self.dmg = dmg
        self.atk_speed = atk_speed
        self.dmg_type = dmg_type
        self.dmg_area = dmg_area
        self.direction = direction
        self.dp_cost = dp_cost
        self.block = block
        self.redeployment_time = redeployment_time

    @staticmethod
    def initialize_agent(agent_data: OperatorData, direction, game, surface, x, y):
        OperatorObject(
            agent_data, direction=""
        )
        return

    def on_place(self, x, y):
        self.xy = x,y

    def is_area(self, x, y):
        return

    def on_collision(self, colliding_object):
        if self.hoverbox.triggered(colliding_object.xy):
            print("OPERATOR COLLIDED")
            return

    def attacked(self, attacker, dmg_type, dmg):
        match dmg_type:
            case "ARTS":
                self.hp -= dmg / self.resistance
            case "PHYSICAL":
                if (dmg - self.defence) > 0:
                    self.hp -= (dmg - self.defence)
            case "TRUE":
                self.hp -= dmg
        if self.hp <= 0:
            self.on_death(attacker)

    def attack(self, attacking_object):
        if self.type_sp == "OFFENSIVE":
            self.sp += 1
        attacking_object.attacked(self, self.dmg_type, self.dmg)

    def on_death(self, attacker):
        return
