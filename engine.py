__author__ = 'Nathan'

import pygame
import graphics
import random
import map
from action import Action
from tribute import Tribute
from goal import Goal
from mapReader import read_map
from random import randint
from pygame.locals import *
import json

class GameEngine(object):
    """
    here we will essentially manage everything and probably handle the controls
    """
    constants = range(1)
    is_looping = False
    tributes = []
    PAUSED = False
    cur_trib = None
    tributes_by_district = []
    map_dims = []
    FIGHT_MESSAGES = False
    @staticmethod
    def start():
        me = GameEngine
        d = json.load(open('./distributions/action_values.json'))
        #create actions (will be overwritten in a minute)
        move_up = Action([], '', 1, 0, (0, -1), 'move_up')
        move_down = Action([], '', 1, 1, (0, 1), 'move_down')
        move_right = Action([], '', 1, 2, (1, 0), 'move_right')
        move_left = Action([], '', 1, 3, (-1, 0), 'move_left')
        hunt = Action([d['hunt']], ["hunger"], 1, 4,(0, 0), 'hunt')
        fight = Action([d['fight']], ["kill"], 1, 5, (0, 0), 'fight')
        scavenge = Action([d['scavenge']], ["getweapon"], 1, 6, (0, 0), 'scavenge')
        craft = Action([d['craft']], ["getweapon"], 1, 7, (0, 0), 'craft')
        hide = Action([d['hide']], ["hide"], 1, 8, (0, 0), 'hide')
        getwater = Action([d['get_water']], ["thirst"], 1, 9, (0, 0), 'get_water')
        rest = Action([d['rest']], ["rest"], 1, 10, (0, 0), 'rest')
        talk_ally = Action([d['talk_ally']], ["ally"], 1, 11, (0, 0), 'talk_ally')
        explore = Action(d['explore'], ['hunger', 'thirst', 'kill'], 1, 12, (0, 0), 'explore')
        me.FIGHT_MESSAGES = d['fight_messages']
        #create actions (will be overwritten in a minute)
        hunger = Goal("hunger", 2)
        thirst = Goal("thirst", 2)
        goal_rest = Goal("rest", 0)
        kill = Goal("kill", 0)
        goal_hide = Goal("hide", 0)
        getweapon = Goal("getweapon", 0)
        ally = Goal("ally", 0)

        goals = {'hunger': hunger, 'thirst': thirst, 'rest': goal_rest, 'kill': kill, 'hide': goal_hide,
                 'get_weapon': getweapon, 'ally': ally}
        actions = [move_up, move_down, move_right, move_left, hunt, fight, scavenge, craft, hide, getwater, rest, talk_ally, explore]

        #create the goals here
        #not really needed right now

        init_locations = [(x, y) for x in range(15, 30) for y in range(15, 35)]
        districts = ['d' + str(x) for x in range(1, 4)]

        for d in districts:
            location = random.choice(init_locations)
            init_locations.remove(location)
            t1 = Tribute(goals, actions, *location, district=d, gender='male')
            me.tributes.append(t1)

            location = random.choice(init_locations)
            init_locations.remove(location)
            t2 = Tribute(goals, actions, *location, district=d, gender='female')
            me.tributes.append(t2)
            me.tributes_by_district.append((d, t1, t2))

        for i in range(len(me.tributes)):
            init_tribute = me.create_goals(me.tributes[i])
            me.tributes[i].goals = init_tribute
            #me.create_actions(me.tributes[i])

        map_to_be_used = 'maps/all_terr.jpg'
        me.dims = (110, 70)
        me.map_dims = (50, 50)
        me.game_map = read_map(map_to_be_used)
        me.view = graphics.GameView(*me.dims)
        me.map = map.Map(map_to_be_used)
        me.state = me.map.seed_game_state(me.tributes)  # game.game_state()
        me.is_looping = True
        me.cur_trib = me.tributes[0]
        while me.is_looping and GameEngine.loop():
            pass

    @staticmethod
    def stop():
        GameEngine.is_looping = False

    @staticmethod
    def loop():
        """
        What to do on each loop iteration
        @return: None
        """
        me = GameEngine
        buttons = me.view.get_buttons()
        names = me.view.get_names()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    me.PAUSED = not me.PAUSED
                if event.key == K_f:
                    me.cur_trib.goals['hunger'].modify_value(-10)
                if event.key == K_d:
                    me.cur_trib.goals['thirst'].modify_value(-10)
                if event.key == K_w:
                    me.cur_trib.get_weapon()
                    me.cur_trib.goals['get_weapon'].modify_value(-10)

            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[0] / 10
                y = pos[1] / 10
                for tribute in me.tributes:
                    if (x,y) == tribute.state:
                        me.cur_trib = tribute
                    else:
                        name_pos = 0
                        for button in buttons:
                            if button.collidepoint(pos):
                                for tribute in me.tributes:
                                    if tribute.first_name == names[name_pos]:
                                        me.cur_trib = tribute
                            name_pos += 1

        if not me.PAUSED:
            for x in range(50):
                for y in range(50):
                    me.game_map[x][y].tribute = None

            for tribute in me.tributes:
                me.game_map[tribute.state[0]][tribute.state[1]].tribute = tribute

            for tribute in me.tributes:
                tribute.act(me.game_map, me.state)  # finds best_action and does it.
                tribute.end_turn()
                death = tribute.check_dead()
                if death is not None:
                    print tribute.first_name, " ", tribute.last_name, " death by ", death
                    me.tributes.remove(tribute)
                    if me.cur_trib == tribute and len(me.tributes) > 1:
                        me.cur_trib = random.choice(me.tributes)
            if len(me.tributes) == 1:
                me.PAUSED = True;
            me.view.render(me.state, me.cur_trib, me.tributes_by_district, me.tributes, 0)
            me.state.update()
        else:
            if len(me.tributes) == 1:
                me.view.render(me.state, me.cur_trib, me.tributes_by_district, me.tributes, 1)
            else:
                me.view.render(me.state, me.cur_trib, me.tributes_by_district, me.tributes, 0)
        return True

    @staticmethod
    def create_actions(tribute):
        #Move action
        move_up = Action([], '', 1, 0, (0, -1), 'move_up')
        move_down = Action([], '', 1, 1, (0, 1), 'move_down')
        move_right = Action([], '', 1, 2, (1, 0), 'move_right')
        move_left = Action([], '', 1, 3, (-1, 0), 'move_left')


        ################ INDEX LIST
        # 0-3 movement
        # 4 hunt
        # 5 fight
        # 6 scavenge
        # 7 craft
        # 8 hide
        # 9 water
        # 10 rest
        # 11 talk

        ############## ACTION ATTRIBUTES
        #1. How much I get back for doing the action in 2. EDIT THIS ONE
        #2. The action (lists, so it can affect more than one thing.)
        #3. Duration
        #4. Index
        #5. Movement Stuff (don't mess wid that)

        #as long as you hunt, you'll get at least 10 food points, maybe more depending on attributes & individual
        hunger_stats = (tribute.attributes['endurance']/2)+tribute.attributes['hunting_skill']-(tribute.attributes['size']/5)
        food_energy = 10 + randint(0, hunger_stats)
        food_rest = (tribute.attributes['stamina'] - 1)/100
        hunt = Action([food_energy,food_rest], ["hunger","rest"], 1, 4,(0,0),'hunt')

        #if you fight your "bloodlust" goes down. If you're friendly, killng someone drastically reduces your desire to kill
        #someone else. Unless you have a friendliness of 1
        kill_stats = (((1/tribute.attributes['bloodlust'])*3)+(tribute.attributes['friendliness']-1))
        if(int(tribute.district[1:]) == 1 or int(tribute.district[1:]) == 2 or int(tribute.district[1:])):
            kill_stats += 3
        else:
            kill_stats += 5
        fight = Action([kill_stats], ["kill"], 1, 5, (0,0),'fight')

        #If they find a weapon, they'll get back 15 "find weapon" points, which will generally cover
        #about 150 of wanting a weapon, and not having one. Same w/ crafting
        scavenge = Action([15], ["getweapon"], 1, 6, (0,0),'scavenge')
        craft = Action([15], ["getweapon"], 1, 7, (0,0),'craft')

        #If you're small and good at hiding, you get more points for it
        #You also recover some rest
        hide_stats = ((3/(tribute.attributes['size']+tribute.attributes['strength']))+((tribute.attributes['camouflage_skill']-1)/4))
        hide = Action([hide_stats, 3], ["hide", "rest"], 1, 8, (0,0),'hide')

        #As long as you drink, you'll get at least 10 drink points. Maybe more depending on attributes & individual
        thirst_stats = (tribute.attributes['endurance'])-(tribute.attributes['size']/5)
        thirst_energy = 10 + randint(0, thirst_stats)
        getwater = Action([thirst_energy], ["thirst"], 1, 9, (0,0),'get_water')

        #Resting will automatically recover 10 rest points. Maybe more depending on attributes & individual
        rest_stats = (tribute.attributes['stamina'] * 2)
        rest_energy = 10 + randint(0, rest_stats)
        rest = Action([rest_energy], ["rest"], 1, 10, (0,0), 'rest')

        #If you're friendly, talking to buddies recovers a bunch of talking-to-buddy points
        #And the smaller, weaker, and more terrible at fighting you are, the more recovery you get for making a buddy
        ally_stats = (tribute.attributes['friendliness'] + (1/tribute.attributes['size']) + (1/tribute.attributes['strength']) + (0.5/tribute.attributes['fighting_skill']))
        talk_ally = Action([ally_stats], ["ally"], 1, 11, (0,0),'talk_ally')

        explore = Action([3], ['multiple'], 1, 12, (0, 0), 'explore')

        new_actions = [move_up, move_down, move_right, move_left, hunt,
                      fight, scavenge, craft, hide, getwater, rest, talk_ally, explore]

        tribute.actions = new_actions

        return tribute

    @staticmethod
    def create_goals(tribute):
        #Base Hunger Thirst and Rest Values
        hunger = Goal("hunger", 2)
        thirst = Goal("thirst", 2)
        rest = Goal("rest", 5)

        #Start-of-Game goals based on attributes and individual
        district = int(tribute.district[1:])
        if district == 1 or district == 2 or district == 4:
            kill_base = 5
        else:
            kill_base = 1
        kill_limit = kill_base + ((tribute.attributes['bloodlust']-1)*2) + (11/tribute.attributes['friendliness']) + ((tribute.attributes['size']-1)/2) + ((tribute.attributes['fighting_skill']-1)/2) + ((tribute.attributes['strength']-1)/2)
        kill_stats = randint(kill_base, kill_limit) * 10

        if(tribute.attributes['size'] + tribute.attributes['strength']) < 4:
            hide_base = 10
        else:
            hide_base = 0
        hide_limit = hide_base + (10/tribute.attributes['size']) + (5/tribute.attributes['strength']) + (tribute.attributes['camouflage_skill'] * 2) - tribute.attributes['fighting_skill']
        hide_stats = randint(hide_base, hide_limit)


        get_weapon_stats = ((tribute.attributes['weapon_skill']-1)*2) - (tribute.attributes['crafting_skill']-1)
        ally_stats = tribute.attributes['friendliness'] - tribute.attributes['bloodlust']


        kill = Goal("kill", kill_stats, 100)
        hide = Goal("hide", hide_stats)
        getweapon = Goal("getweapon", get_weapon_stats)
        ally = Goal("ally", ally_stats)
        fear = Goal("fear", 0)

        return {'hunger': hunger, 'thirst': thirst, 'rest': rest, 'kill': kill, 'hide': hide, 'get_weapon': getweapon,
                'ally': ally, 'fear': fear}
