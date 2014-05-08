import tribute


class LocationDefinition(object):

    def __init__(self):
        self.start_space = False     # True/False
        self.player_there = False   # True/False
        # Tribute that is in a space. Null otherwise
        self.tribute = None
        self.terrain = 0            # 0-15 Value for terrain Type
        self.food_chance = 0        # integer value for probability of food
        self.water_chance = 0       # integer value for probability of water
        self.visibility = 0         # integer value for visibility
        # for crafting: Integer Value probability of stick
        self.short_stick_chance = 0
        # for crafting: integer value probability of sharp stone
        self.sharp_stone_chance = 0
        # for crafting: integer value probability of feather
        self.feather_chance = 0
        # for crafting: integer value probability of vine
        self.vine_chance = 0
        self.speed_change = 0        # integer value movement speed changes
        self.weapon_chance = 0       # inter value for probability of weapon
        self.long_stick_chance = 0
        self.broad_stone_chance = 0
        self.long_grass_chance = 0
        self.reeds_chance = 0
        self.pebbles_chance = 0
        self.thorns_chance = 0

    ########### GETS ##############

    def get_start_space(self):
        return self.start_space

    def get_player_there(self):
        return self.player_there

    def get_tribute(self):
        return self.tribute

    def get_terrain(self):
        return self.terrain

    def get_food_chance(self):
        return self.food_chance

    def get_water_chance(self):
        return self.water_chance

    def get_short_stick_chance(self):
        return self.stick_chance

    def get_visibility(self):
        return self.visibility

    def get_sharp_stone_chance(self):
        return self.sharp_stone_chance

    def get_feather_chance(self):
        return self.feather_chance

    def get_vine_chance(self):
        return self.vine_chance

    def get_speed_change(self):
        return self.speed_change

    def get_weapon_chance(self):
        return self.weapon_chance

    def get_long_stick_chance(self):
        return self.long_stick_chance

    def get_broad_stone_chance(self):
        return self.broad_stone_chance

    def get_long_grass_chance(self):
        return self.long_grass_chance

    def get_reeds_chance(self):
        return self.reeds_chance

    def get_pebbles_chance(self):
        return self.pebbles_chance

    def get_thorns_chance(self):
        return self.thorns_chance

    ########### SETS ##############
    def set_start_space(self, input):
        self.start_space = input

    def set_player_there(self, input):
        self.player_there = input

    def set_tribute(self, input):
        self.tribute = input

    def set_terrain(self, input):
        self.terrain = input

    def set_food_chance(self, input):
        self.food_chance = input

    def set_water_chance(self, input):
        self.water_chance = input

    def set_short_stick_chance(self, input):
        self.stick_chance = input

    def set_visibility(self, input):
        self.visibility = input

    def set_sharp_stone_chance(self, input):
        self.sharp_stone_chance = input

    def set_feather_chance(self, input):
        self.feather_chance = input

    def set_vine_chance(self, input):
        self.vine_chance = input

    def set_speed_change(self, input):
        self.speed_change = input

    def set_weapon_chance(self, input):
        self.weapon_chance = input

    def set_long_stick_chance(self, input):
        self.long_stick_chance = input

    def set_broad_stone_chance(self, input):
        self.broad_stone_chance = input

    def set_long_grass_chance(self, input):
        self.long_grass_chance = input

    def set_reeds_chance(self, input):
        self.reeds_chance = input

    def set_pebbles_chance(self, input):
        self.pebbles_chance = input

    def set_thorns_chance(self, input):
        self.thorns_chance = input
