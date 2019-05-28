"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from collections import defaultdict
import random


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    def at_object_creation(self):
        random.seed()
        self.db.attributes = {
                'strength': random.randint(20, 120),
                'dexterity': random.randint(20, 120),
                'agility': random.randint(20, 120),
                'endurance': random.randint(20, 120),
                'speed': random.randint(20, 120),
                'charisma': random.randint(20, 120),
                'intelligence': random.randint(20, 120),
                'willpower': random.randint(20, 120),
                'perception': random.randint(20, 120),
                'empathy': random.randint(20, 120),
                'memory': random.randint(20, 120),
                'judgement': random.randint(20, 120),
                'reasoning': random.randint(20, 120)
        }
        self.db.equipment = {
                'head': None,
                'face': None,
                'back': None,
                'right_shoulder': None,
                'left_shoulder': None,
                'neck': None,
                'chest': None,
                'waist': None,
                'right_foot': None,
                'left_foot': None,
                'right_leg': None,
                'left_leg': None,
                'right_arm': None,
                'left_arm': None,
                'right_hand': None,
                'left_hand': None,
                'held_left': None,
                'held_right': None
        }

        self.db.first_name = self.name
        self.db.last_name = None

        self.db.gender = None
        self.db.height = None
        self.db.weight = None

        self.db.appearance = {
                'complexion': 'nondescript',
                'eye_color': 'black',
                'hair_color': None,
                'hair_length': None,
                'hair_texture': None,
                'nose': 'nondescript',
                'lips': 'nondescript',
                'chin': 'nondescript'
        }

        self.db.age = 0
        self.db.skills = []

        self.db.hp = self.max_hp
        self.db.fatigue = self.max_fatigue
        self.db.chargen_state = None
        self.db.starting_skill = None
        self.db.combatant_type = None
        self.db.background = None
        self.db.background_caste = None

    @property
    def background_caste(self):
        caste_map = {
            'underworld': [
                'thug',
                'urchin',
                'thief'
            ],
            'gladiator': [
                'gladiator',
            ],
            'peasant': [
                ''
            ],
            'high-born': []
        }
        if not self.db.background:
            return None

    @property
    def max_hp(self):
        return self.db.attributes.get('endurance') * 1.2

    @property
    def max_fatigue(self):
        return self.db.attributes.get('endurance')

    def return_appearance(self, looker, **kwargs):
        """
        Overrides the default return_appearance;
        sets the format of the string returned when this object is looked at.

        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
            elif con.has_account:
                users.append("|c%s|n" % key)
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc
        if desc:
            string += "You see a %s" % desc
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.iteritems()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]
                thing_strings.append(key)

            string += "\n|wYou see:|n " + list_to_string(users + thing_strings)

        return string
