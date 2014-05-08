import random
import engine
import json
import copy
import sys
from probability import uniform_variable as u
from weaponInfo import weaponInfo
from weapon import weapon
import mapReader


class Particle(object):
    def __init__(self, state=(0, 0), width=1, height=1):
        self.state = state
        self.width, self.height = width, height

FIGHT_STATE = {'not_fighting': 0, 'fleeing': 1, 'fighting': 2}
NAVIGATION_POINTS = [(25, 25), (5, 5), (45, 5), (45, 45), (5, 45)]
FIGHT_EMERGENCY_CUTOFF = 80


class Tribute(Particle):
    #Goals = list of goals for tribute
    ################ ACTIONS
    # movement l,r,u,d
    # hunt
    # fight
    # scavenge
    # craft
    # hide
    # water
    # rest
    # talk
    ID_COUNTER = 0

    def __init__(self, goals, actions, x=0, y=0, district='d12', gender='male', do_not_load=False):
        Particle.__init__(self, (x, y), 1, 1)
        self.id = Tribute.ID_COUNTER
        Tribute.ID_COUNTER += 1
        self.goals = goals
        self.actions = actions

        # remove the fight action. we don't want them fighting unless someone is in range
        self.fight_action = actions[5]
        self.explore_action = actions[12]
        self.actions = self.actions[:5] + self.actions[6:12]

        self.district = district
        self.has_weapon = False
        self.weapon = weapon('')
        self.has_ally = False
        self.allies = []
        self.craft_pouch = []
        self.fighting_state = FIGHT_STATE['not_fighting']
        self.opponent = None
        self.last_opponent = None
        self.sighted = None
        self.last_sighted_location = None
        self.last_action = None
        self.printy_action = 'none'
        self.old_state = self.state
        self.visited_set = set()
        self.explore_point_index = 0
        self.explore_point = NAVIGATION_POINTS[self.explore_point_index]
        self.killed_by = None

        self.hidden = False

        self.weapon_info = weaponInfo()
        self.wep_can_craft = ''
        self.best_scavenge_choice = ''
        self.best_scavenge_points = 0

        if do_not_load:
            self.attributes = None
            self.gender = gender
            self.stats = None
            self.last_name = None
            self.first_name = None
            self.killed = None
        else:
            d = json.load(open('./distributions/stats.json'))

            self.attributes = {
                'size': u(d['size']['mean'], d['size']['spread']),
                'strength': u(d['strength']['mean'], d['strength']['spread']),
                'speed': u(d['speed']['mean'], d['speed']['spread']),
                'hunting_skill': u(d['hunting_skill'][self.district]['mean'],
                                   d['hunting_skill'][self.district]['spread']),
                'fighting_skill': u(d['fighting_skill'][self.district]['mean'],
                                    d['fighting_skill'][self.district]['spread']),
                'weapon_skill': u(d['weapon_skill'][self.district]['mean'], d['weapon_skill'][self.district]['spread']),
                'camouflage_skill': u(d['camouflage_skill'][self.district]['mean'],
                                      d['camouflage_skill'][self.district]['spread']),
                'friendliness': u(d['friendliness']['mean'], d['friendliness']['spread']),
                'district_prejudices': dict(d['district_prejudices'][self.district]),
                'stamina': u(d['stamina']['mean'], d['stamina']['spread']),
                'endurance': u(d['endurance']['mean'], d['endurance']['spread']),
                'crafting_skill': u(d['crafting_skill'][self.district]['mean'],
                                    d['crafting_skill'][self.district]['spread']),
                'bloodlust': u(d['bloodlust']['mean'], d['bloodlust']['spread']),
                'max_health': u(d['max_health']['mean'], d['max_health']['spread'])
            }
            self.gender = gender
            self.stats = {
                'health': self.attributes['max_health'],
                'energy': self.attributes['stamina'],
                'hunger_energy': 100
            }

            self.last_name = random.choice(d['last_names'])
            if self.gender == 'male':
                self.first_name = random.choice(d['first_names_male'])
            else:
                self.first_name = random.choice(d['first_names_female'])

            self.killed = False
            pass

    def clone(self):
        n_goals = {g: self.goals[g].clone() for g in self.goals}
        n_actions = self.actions[:5] + [self.fight_action] + self.actions[5:12] + [self.explore_action]
        n_district = self.district[:]
        n_gender = self.gender[:]
        n = Tribute(n_goals, n_actions, x=self.state[0], y=self.state[1], district=n_district,
                    gender=n_gender, do_not_load=True)
        n.killed = self.killed
        n.attributes = self.attributes.copy()
        n.stats = self.stats.copy()
        n.opponent = self.opponent
        n.sighted = self.sighted
        n.last_action = self.last_action
        n.printy_action = self.printy_action
        n.last_opponent = self.last_opponent
        n.best_scavenge_choice = self.best_scavenge_choice
        n.best_scavenge_points = self.best_scavenge_points
        n.visited_set = self.visited_set.copy()
        n.explore_point = self.explore_point
        n.explore_point_index = self.explore_point_index
        n.craft_pouch = self.craft_pouch
        n.wep_can_craft = self.wep_can_craft
        n.hidden = self.hidden
        n.last_sighted_location = self.last_sighted_location
        n.id = self.id
        return n

    def __repr__(self):
        s = '<Tribute>(' + self.last_name + ', ' + self.first_name + ', ' + self.gender + ')'
        return s

    def engage_in_combat(self, t):
        if self.fighting_state == FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['fighting']
            self.opponent = t
            self.last_opponent = self.opponent
            t.engage_in_combat(self)
            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' is engaging in combat with ' + str(t) + '!'
        elif self.fighting_state == FIGHT_STATE['fleeing']:
            self.opponent = t

            if self.opponent.fighting_state != FIGHT_STATE['fleeing']:
                t.engage_in_combat(self)

            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' is being chased by ' + str(t) + '!'

    def disengage_in_combat(self, t):
        if self.fighting_state != FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['not_fighting']
            self.opponent = None
            t.disengage_in_combat(self)
            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' is disengaging in combat with ' + str(t) + '!'

    @staticmethod
    def surmise_enemy_hit(tribute):
        """
        returns the estimate average HP hit for an enemy
        :param tribute: the enemy to surmise about
        :return: the surmised value
        """
        return 1 + int(tribute.has_weapon) * 5 + int(tribute.attributes['strength']) / 2

    def surmise_escape_turns(self, tribute):
        if self.attributes['speed'] >= tribute.attributes['speed']:
            turns = sys.maxint
        else:
            s = tribute.attributes['speed'] - self.attributes['speed']
            distance = abs(self.state[0] - tribute.state[0]) + abs(self.state[1] - tribute.state[1])
            turns = distance / s

        return turns

    @staticmethod
    def surmise_enemy_weakness(tribute):
        index = tribute.attributes['max_health'] - tribute.stats['health']
        val = float(index) / tribute.attributes['max_health']
        return int(round(val * 5))

    def enemy_in_range(self, game_state):
        for t in game_state.grid['particle']:
            p = t[3]
            d = abs(t[0] - self.state[0]) + abs(t[1] - self.state[1])
            if 0 < d < 5 and p not in self.allies:
                return p
        return None

    def hurt(self, damage, place):
        if engine.GameEngine.FIGHT_MESSAGES:
            print str(self) + ' was hit in the ' + place + ' for ' + str(damage) + ' damage'

        self.goals['kill'].modify_value(-3)
        self.stats['health'] -= damage
        self.goals['fear'].modify_value(damage * 10)
        if self.stats['health'] <= 0:
            self.killed = True
            self.killed_by = self.opponent
            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' was killed by ' + str(self.killed_by)
            self.disengage_in_combat((self.opponent or self.killed_by or self.last_opponent))

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def calc_min_discomfort(self, depth, max_depth, game_map, actions):
        min_val = sys.maxint

        if depth == max_depth:
            return self.calc_discomfort()

        for action in actions:
            tribute = self.clone()
            tribute.apply_action(action, game_map)
            min_val = min(tribute.calc_min_discomfort(depth + 1, max_depth, game_map, actions), min_val)

        return min_val

    def decide_fight_move(self):
        if self.goals['fear'].value < random.randrange(105, 150):
            actions = ['attack_head', 'attack_chest', 'attack_gut', 'attack_legs']
            return random.choice(actions)
        else:
            ###print str(self), ' became scared and is trying to flee!'
            return 'flee'

    def act(self, game_map, game_state):
        if self.fighting_state != FIGHT_STATE['fighting']:
            best_action = (None, sys.maxint)
            actions = self.actions

            self.sighted = self.enemy_in_range(game_state)
            if self.sighted:
                self.last_sighted_location = self.sighted.state

            if self.sighted and not self.sighted.killed:
                actions = self.actions + [self.fight_action]

            if self.goals['hunger'].value > 90 or self.goals['thirst'].value > 50 and self.sighted is None:
                actions = self.actions + [self.explore_action]
                self.explore_point = NAVIGATION_POINTS[self.explore_point_index]
            elif self.goals['kill'].value > FIGHT_EMERGENCY_CUTOFF and self.sighted is None:
                actions = self.actions + [self.explore_action]
                if self.last_sighted_location:
                    self.explore_point = self.last_sighted_location

            neighbors = mapReader.get_neighbors2(game_map, self.state)
            forbidden_states = []

            for trib in engine.GameEngine.tributes:
                if trib.state in neighbors and trib.id != self.id:
                    forbidden_states.append(trib.state)

            for a in actions:
                n_pos = mapReader.add_states(self.state, a.delta_state)
                if n_pos in forbidden_states:
                    continue
                t = copy.deepcopy(self)
                t.apply_action(a, game_map)
                v = t.calc_min_discomfort(0, 2, game_map, actions)
                if v < best_action[1]:
                    best_action = (a, v)

            self.do_action(best_action[0], game_map)

        elif self.fighting_state == FIGHT_STATE['fighting']:
            best_action = self.decide_fight_move()
            self.do_fight_action(best_action)

    def do_fight_action(self, action_name):

        if self.opponent and mapReader.l1_dist(self.state, self.opponent.state) > 2:
            self.disengage_in_combat(self.opponent)
            return

        if self.opponent.killed:
            self.disengage_in_combat(self.opponent)
            return

        self.goals['kill'].modify_value(-1)

        if self.opponent.hidden:
            print str(self), ' cannot find ', str(self.opponent)
            return

        self.last_action = action_name
        self.printy_action = action_name

        # with weapon 1d6 damage + 1d(str/2) + 1
        if self.has_weapon:
            damage = self.weapon.damage + random.randrange(1, (self.attributes['strength'] / 4) + 2) + \
                random.randint(0, self.attributes['weapon_skill']/2 + 1) + 1
        else:  # without, 1d2 damage + 1d(str)
            damage = random.randrange(1, 3) + random.randrange(1, self.attributes['strength'] + 1)
        draw = random.random()
        chance_mult = 1

        if self.attributes['fighting_skill'] > 3:
            chance_mult += 0.1

        if self.attributes['fighting_skill'] > 7:
            chance_mult += 0.15
        if engine.GameEngine.FIGHT_MESSAGES:
            if self.has_weapon:
                print str(self), ' swings his/her ', self.weapon.type

        if action_name == 'attack_head':
            if draw < 0.5 * chance_mult:
                self.opponent.hurt(damage + 2, 'head')
                self.goals['fear'].value = max(self.goals['fear'].value - (damage + 2) / 2, 0)
        elif action_name == 'attack_chest':
            if draw < 0.8 * chance_mult:
                self.opponent.hurt(damage + 1, 'chest')
                self.goals['fear'].value = max(self.goals['fear'].value - (damage + 1) / 2, 0)
        elif action_name == 'attack_gut':
            if draw < 0.8 * chance_mult:
                self.opponent.hurt(damage, 'gut')
                self.goals['fear'].value = max(self.goals['fear'].value - damage / 2, 0)
        elif action_name == 'attack_legs':
            if draw < 0.9 * chance_mult:
                self.opponent.hurt(damage - 1, 'legs')
                self.goals['fear'].value = max(self.goals['fear'].value - (damage - 1) / 2, 0)
        elif action_name == 'flee':
            self.opponent.disengage_in_combat(self)
            self.goals['kill'].value = 0
            self.fighting_state = FIGHT_STATE['fleeing']

    def do_action(self, action, game_map):
        self.hidden = False

        self.last_action = action
        self.printy_action = action.description
        rand = (random.randint(1, 10)) / 10
        loc = game_map[self.state[0]][self.state[1]]
        if 3 >= action.index >= 0:  # moving so don't know what gonna do here
            loc.setTribute(None)
            self.old_state = self.state
            (game_map[self.state[0]][self.state[1]]).setTribute(None)
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.map_dims[0],
                         (self.state[1] + action.delta_state[1]) % engine.GameEngine.map_dims[1])
            game_map[self.state[0]][self.state[1]].setTribute(self)
        elif action.index == 4:  # find food
            food_prob = loc.getFoodChance()
            if rand <= food_prob:
                self.goals['hunger'].modify_value(-action.values[0] * 3)
        elif action.index == 5:  # fight
            self.sighted.engage_in_combat(self)
            self.goals['kill'].value = max(self.goals['kill'].value - action.values[0], 0)
        elif action.index == 6:  # scavenge
            wep_prob = loc.getWeaponChance()
            goal = self.goals['get_weapon']
            if wep_prob > 0.9:
                if rand <= wep_prob:
                    self.get_weapon()
                    goal.modify_value(-action.values[0])
            else:
                # doCraftScavenge will return zero if you fail to find something, and one if you succeed
                #num = self.check_craft_scavenge(game_map)
                goal.modify_value(-self.best_scavenge_points * self.do_craft_scavenge(game_map,
                                                                                      self.best_scavenge_choice))
        elif action.index == 7:  # craft
            # Crafting Probability is factored into doCraftWeapon
            self.check_craft_weapon()
            if self.wep_can_craft != '':
                # Returns boolean if you did it or not
                crafted = self.do_craft_weapon(self.wep_can_craft)
                if crafted:
                    self.goals['get_weapon'].value = 0
                else:
                    self.goals['get_weapon'].modify_value(-self.attributes['crafting_skill'])
        elif action.index == 8:  # hide
            ub = self.attributes['camouflage_skill']
            if random.randrange(0, 11) < ub:
                self.hidden = True

        elif action.index == 9:  # get water
            water_prob = loc.getWaterChance()
            if rand <= water_prob:
                self.goals['thirst'].modify_value(-action.values[0])

        elif action.index == 10:  # rest
            self.goals['rest'].modify_value(-action.values[0])
        elif action.index == 11:  # talk ally
            f1 = self.attributes['friendliness']
            x = self.state[0]
            y = self.state[1]
            w = engine.GameEngine.map_dims[0]
            h = engine.GameEngine.map_dims[1]
            target = game_map[(x + 1) % w][y].tribute or \
                game_map[(x - 1) % w][y].tribute or \
                game_map[x][(y + 1) % h].tribute or \
                game_map[x][(y - 1) % h].tribute
            if not target:
                print 'No target for ally!'
            elif target not in self.allies and target.id != self.id:
                f2 = target.attributes['friendliness']
                a1 = self.attributes['district_prejudices'][target.district]
                a2 = target.attributes['district_prejudices'][self.district]
                v = (f1 + f2 + a1 + a2) / 224.0
                if random.random() < v:
                    if engine.GameEngine.FIGHT_MESSAGES:
                        print str(self), ' and ', str(target), ' have gotten allied!'
                    self.allies.append(target)
                    target.allies.append(self)
                    self.goals['ally'].value = 0

        elif action.index == 12:  # explore
            directions = mapReader.get_neighbors(game_map, self.state)
            evals = []

            for i, direction in enumerate(directions):
                if game_map[direction[0]][direction[1]].tribute is None:
                    evals.append((mapReader.l1_dist(direction, self.explore_point), direction, i))
            if len(evals) > 0:
                direction = min(evals, key=lambda x1: x1[0] + random.random() / 1000)  # rand is for breaking ties
                if mapReader.l1_dist(self.explore_point, direction[1]) < 3:
                    if self.goals['kill'].value > FIGHT_EMERGENCY_CUTOFF:
                        self.last_sighted_location = (self.explore_point[0] + u(0, 16),
                                                      self.explore_point[1] + u(0, 16))
                    else:
                        self.explore_point_index = (self.explore_point_index + 1) % len(NAVIGATION_POINTS)
                        self.explore_point = NAVIGATION_POINTS[self.explore_point_index]

                self.state = direction[1]

    def end_turn(self):
        if self.fighting_state != FIGHT_STATE['fleeing']:
            self.goals['kill'].modify_value(((self.attributes['bloodlust'] - 1) / 5.0) + 1)
        if int(self.district[1:]) == 1 or int(self.district[1:]) or int(self.district[1:]) == 4:
            self.goals['kill'].modify_value(0.1)
            if not self.has_weapon:
                self.goals['get_weapon'].modify_value(0.05)
        if int(self.district[1:]) == 1 or int(self.district[1:]) or int(self.district[1:]) == 4:
            self.goals['kill'].modify_value(0.25)
            if not self.has_weapon:
                self.goals['get_weapon'].modify_value((1 / (self.attributes['size'] + self.attributes['strength'])))
        if (self.attributes['size'] + self.attributes['strength']) < 4:
            if not self.has_ally and not self.has_weapon:
                self.goals['ally'].modify_value(0.05)
            if not self.has_ally and not self.has_weapon:
                self.goals['hide'].modify_value(0.01)

            self.goals['ally'].modify_value(0.05 / (len(self.allies) + 1)**2)

        self.goals['hunger'].modify_value(1.0 / self.attributes['endurance'] + self.attributes['size'] / 5.0)

        self.goals['thirst'].modify_value(1.0 / self.attributes['endurance'])

        self.goals['rest'].modify_value(1.0 / self.attributes['stamina'] + self.goals['hunger'].value / 50.0 +
                                        self.goals['thirst'].value / 30.0)

        self.goals['fear'].value = max(self.goals['fear'].value - 2.5, 0)
        if self.goals['fear'].value < 30 and self.fighting_state == FIGHT_STATE['fleeing']:
            self.fighting_state = FIGHT_STATE['not_fighting']

        if not self.has_weapon:
            self.goals['get_weapon'].modify_value(0.5)

        #goal.value = max(goal.value, 0)

    #Action will update the state of the world by calculating
    #Goal updates and where it is / fuzzy logic of where other tributes are
    #will update current selfs world.
    def apply_action(self, action, game_map):
        # [hunger, thirst, rest, kill, hide, getweapon, ally, fear]
        loc = game_map[self.state[0]][self.state[1]]

        distance_before = 0
        if self.last_opponent and self.fighting_state == FIGHT_STATE['fleeing']:
            distance_before = abs(self.state[0] - self.last_opponent.state[0]) + \
                abs(self.state[1] + self.last_opponent.state[1])

        if 3 >= action.index >= 0:  # moving so don't know what gonna do here
            self.old_state = self.state
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.map_dims[0],
                          (self.state[1] + action.delta_state[1]) % engine.GameEngine.map_dims[1])

            g = random.choice(self.goals.keys())
            self.goals[g].modify_value(0.5)
        elif action.index == 4:  # hunt
            food_prob = loc.getFoodChance()
            self.goals['hunger'].modify_value(-food_prob * action.values[0])
        elif action.index == 5:  # kill
            if abs(self.sighted.state[0] - self.state[0]) + abs(self.sighted.state[1] - self.state[1]) <= 2:
                self.goals['kill'].value = max(self.goals['kill'].value - action.values[0]*10, 0)

            if self.surmise_enemy_hit(self.sighted) > self.surmise_enemy_hit(self):
                self.goals['fear'].modify_value(5)
            if self.surmise_escape_turns(self.sighted) < 5:
                self.goals['fear'].modify_value(5)
            weakness = self.surmise_enemy_weakness(self.sighted)
            # self.goals['fear'].modify_value(-weakness
            if weakness < 1:
                self.goals['fear'].modify_value(-11)

        elif action.index == 6:  # scavenge
            wep_chance = loc.getWeaponChance()
            if wep_chance > 0.9 and not self.has_weapon:
                self.goals['get_weapon'].modify_value(-wep_chance * action.values[0])
            elif not self.has_weapon:
                self.goals['get_weapon'].modify_value(-self.check_craft_scavenge(game_map))

        elif action.index == 7:  # craft
            craft_prob = self.check_craft_weapon()
            self.goals['get_weapon'].modify_value(-(self.goals['get_weapon'].value * craft_prob))

        elif action.index == 8:  # hide
            self.goals['fear'].modify_value(-(action.values[0] * (self.attributes['camouflage_skill'] / 10.0)))
        elif action.index == 9:  # get_water
            water_prob = loc.getWaterChance()
            self.goals['thirst'].modify_value(-water_prob * action.values[0])
        elif action.index == 10:  # rest
            self.goals['rest'].modify_value(-action.values[0])
        elif action.index == 11:  # talk ally
            x = self.state[0]
            y = self.state[1]
            w = engine.GameEngine.map_dims[0]
            h = engine.GameEngine.map_dims[1]
            if (game_map[(x + 1) % w][y].tribute is not None and game_map[(x + 1) % w][y].tribute not in self.allies) or \
               (game_map[(x - 1) % w][y].tribute is not None and game_map[(x - 1) % w][y].tribute not in self.allies) or \
               (game_map[x][(y + 1) % h].tribute is not None and game_map[x][(y + 1) % h].tribute not in self.allies) or \
               (game_map[x][(y - 1) % h].tribute is not None and game_map[x][(y - 1) % h].tribute not in self.allies):
                self.goals['ally'].modify_value(-action.values[0])
        elif action.index == 12:  # explore
            self.goals['hunger'].value = max(self.goals['hunger'].value - action.values[0], 0)
            self.goals['thirst'].value = max(self.goals['thirst'].value - action.values[1], 0)
            self.goals['kill'].value = max(self.goals['thirst'].value - action.values[2], 0)

        distance_after = 1
        if self.last_opponent and self.fighting_state == FIGHT_STATE['fleeing']:
            distance_after = abs(self.state[0] - self.last_opponent.state[0]) + \
                abs(self.state[1] + self.last_opponent.state[1])

        if distance_after <= distance_before and self.fighting_state == FIGHT_STATE['fleeing']:
            self.goals['fear'].modify_value(100)

    def calc_discomfort(self):
        val = 0
        for goal in self.goals.itervalues():
            if goal.value > 0:
                val += goal.value * goal.value
        return val

    def check_dead(self):
        if self.goals['hunger'].value >= 200:
            self.killed = True
            return " starvation "

        if self.goals['thirst'].value >= 200:
            self.killed = True
            return " terminal dehydration "

        if self.goals['rest'].value >= 250:
            self.killed = True
            return " exhaustion "

        if self.killed:
            return self.killed_by
        else:
            return None

    def get_weapon(self):
        self.has_weapon = True
        weapon_type = random.randint(1, 10)
        self.weapon = weapon(self.weapon_info.weaponType(weapon_type))
        print str(self), ' has picked up a ', str(self.weapon)

    def check_craft_scavenge(self, game_map):
        self.best_scavenge_choice = ''
        self.best_scavenge_points = 0
        location = game_map[self.state[0]][self.state[1]]
        craft_types = self.weapon_info.craftTypes
        best_possible_points = 0
        for craft_type in craft_types:
            poss = self.ret_scav_type_prob(craft_type, location) * 10
            if poss != 0:
                mock_pouch = copy.deepcopy(self.craft_pouch)
                # If you've already got what you're scavenging for
                already_have = 0
                for item in mock_pouch:
                    if item == craft_type:
                        already_have = 1
                if already_have < 1:
                    mock_pouch.append(craft_type)
                    for current_weapon in self.weapon_info.weaponList:
                        poss_points = 0
                        can_craft = self.weapon_info.canCraft(current_weapon, mock_pouch)
                        if can_craft:
                            poss_points += 5 + self.weapon_info.weaponStrength(current_weapon) / 2
                            if poss_points > self.best_scavenge_points:
                                self.best_scavenge_points = poss_points
                                self.best_scavenge_choice = craft_type
                                best_possible_points = poss_points
                                return best_possible_points
                        else:
                            num_items_need_to_craft = \
                                len(self.weapon_info.itemsNeededToCraft(current_weapon, mock_pouch))
                            poss_points += 5 - num_items_need_to_craft + \
                                (self.weapon_info.weaponStrength(current_weapon)/10) + poss

                            if poss_points > self.best_scavenge_points:
                                self.best_scavenge_points = poss_points
                                self.best_scavenge_choice = craft_type
                                best_possible_points = poss_points

        return best_possible_points

    def do_craft_scavenge(self, game_map, resource_type):
        loc = game_map[self.state[0]][self.state[1]]
        current_type_prob = self.ret_scav_type_prob(resource_type, loc)
        chance = random.randint(1, 10)
        if chance <= 10 * current_type_prob:
            c_value = 1
            self.craft_pouch.append(resource_type)
        else:
            c_value = 0
        return c_value

    @staticmethod
    def ret_scav_type_prob(resource_type, loc):
        if resource_type == 'shortStick':
            current_type_prob = loc.shortStickChance
        elif resource_type == 'sharpStone':
            current_type_prob = loc.sharpStoneChance
        elif resource_type == 'feather':
            current_type_prob = loc.featherChance
        elif resource_type == 'vine':
            current_type_prob = loc.vineChance
        elif resource_type == 'longStick':
            current_type_prob = loc.longStickChance
        elif resource_type == 'broadStone':
            current_type_prob = loc.broadStoneChance
        elif resource_type == 'longGrass':
            current_type_prob = loc.longGrassChance
        elif resource_type == 'reeds':
            current_type_prob = loc.reedsChance
        elif resource_type == 'pebbles':
            current_type_prob = loc.pebblesChance
        elif resource_type == 'thorns':
            current_type_prob = loc.thornsChance
        else:
            current_type_prob = 0

        return current_type_prob

    # Returns the probability of Crafting a Weapon based on your items & skill
    def check_craft_weapon(self):
        prob_craft = self.attributes['crafting_skill']

        craftable_weapon = None
        max_wep_strength = 0
        num_items_craft_wep = 0
        can_craft = 0

        for wepType in self.weapon_info.weaponList:
            ans = self.weapon_info.canCraft(wepType, self.craft_pouch)
            if ans:
                can_craft = 1
                strength = self.weapon_info.weaponStrength(wepType)
                if strength > max_wep_strength:
                    max_wep_strength = strength
                    num_items_craft_wep = self.weapon_info.totalNumItemsToCraft(wepType)
                    craftable_weapon = wepType
                elif strength == max_wep_strength:
                    if self.weapon_info.totalNumItemsToCraft(wepType) < num_items_craft_wep:
                        max_wep_strength = strength
                        num_items_craft_wep = self.weapon_info.totalNumItemsToCraft(wepType)
                        craftable_weapon = wepType
                else:
                    craftable_weapon = self.wep_can_craft

        self.wep_can_craft = craftable_weapon
        return prob_craft * can_craft * 100

    # Craft the weapon based on your skill. If you fail to craft, you still lose the items. Wah-wah.
    def do_craft_weapon(self, wep_to_craft):
        items_used = self.weapon_info.totalItemsToCraft(wep_to_craft)
        for needed in items_used:
            for supply in self.craft_pouch:
                if needed == supply:
                    self.craft_pouch.remove(supply)
        chance = random.randint(1, 10)
        if chance <= self.attributes['crafting_skill']:
            crafted = True
            self.weapon = weapon(wep_to_craft)
        else:
            crafted = False

        self.wep_can_craft = None
        self.has_weapon = crafted
        return crafted
