"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
# from evennia import default_cmds


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """
    pass


class ChargenException(Exception):
    pass


class ChargenFatalException(ChargenException):
    pass


class ChargenInputException(ChargenException):
    pass


class CmdChargenNext(BaseCommand):
    """
    Next command for the chargen system.
    """

    key = "next"
    help_category = "chargen"

    def func(self):
        self.chargen_states = [
            None,
            'name',
            'gender',
            'type',
            'background',
            'starting_skill',
            'done'
        ]

        if self.caller.db.chargen_state not in self.chargen_states:
            '''shouldn't be possible'''
            raise ChargenFatalException('Unknown chargen state.')

        if self.caller.db.chargen_state == 'done':
            '''shouldn't be possible'''
            raise ChargenFatalException('You already finished chargen.')

        if self.caller.db.chargen_state is None:
            self.caller.msg('You\'ll need to answer a few questions about your new character.\n First, '
                            'you\'ll need to choose your character\' first and last name.')
        elif self.caller.db.chargen_state == 'name':
            if not self.caller.db.first_name or not self.caller.db.last_name:
                self.caller.msg('Must set both first and last names before continuing on.')
                return
        elif self.caller.db.chargen_state == 'gender':
            if not self.caller.db.gender:
                self.caller.msg('Must pick a gender, or neither, before continuing on.')
                return
        elif self.caller.db.chargen_state == 'type':
            if not self.caller.db.combatant_type:
                self.caller.msg('Must pick one of the three class types before continuing on.')
                return
        elif self.caller.db.chargen_state == 'background':
            if not self.caller.db.background:
                self.caller.msg('Must pick a background before continuing on.')
                return
        elif self.caller.db.chargen_state == 'starting_skill':
            if not self.caller.db.starting_skill:
                self.caller.msg('Must pick a starting skill before continuing on.')
                return

        '''if no errors, advance on'''
        new_state = self.next_state()
        self.caller.db.chargen_state = new_state

        next_command = CmdChargenSet.class_from_state(new_state)(self.caller)
        next_command.send_instructions()

    def next_state(self):
        for i in range(len(self.chargen_states)):
            if self.chargen_states[i] == self.caller.db.chargen_state:
                return self.chargen_states[i+1]


class CmdChargenSet(BaseCommand):
    """
    Master command for the chargen system.

    This is kinda gross, I'm sure there's a better way to do this?
    """

    key = "set"
    help_category = "chargen"

    @staticmethod
    def class_from_state(current_state):
        cls = CmdChargenSet.get_cmd_map().get(current_state)
        if not cls:
            raise ChargenInputException('Unknown class for state: {0}'.format(current_state))
        return cls

    @staticmethod
    def get_cmd_map():
        return {
            'name': ChargenSetName,
            'gender': ChargenSetGender,
            'type': ChargenSetCombatantType,
            'background': ChargenSetBackground,
            'starting_skill': ChargenSetStartingSkill,
            'done': ChargenSetDone
        }

    def func(self):
        "This performs the actual command"
        if self.caller.db.chargen_state is None:
            '''Shouldn't get called before the chargen state is set'''
            self.caller.msg("You shouldn't be doing this? You don't have a chargen state.")
            return
        if self.caller.db.chargen_state is 'done':
            self.caller.msg('You already finished chargen.')
            return

        cmd_cls = self.class_from_state(self.caller.db.chargen_state)
        cmd_object = cmd_cls(self.caller)

        try:
            cmd_object.key, cmd_object.value = self.parse_chargen_args()
        except ValueError:
            cmd_object.send_instructions('Improper command usage')
            return
        except UnicodeDecodeError:
            cmd_object.send_instructions('All characters in name must be in standard ASCII alphabet')
            return

        try:
            cmd_object.run()
        except ChargenException as err:
            if type(err) == ChargenFatalException:
                self.caller.msg('Fatal chargen error: {0}'.format(err.message))
            else:
                if err.message:
                    cmd_object.send_instructions('Chargen error: {0}'.format(err.message))
                else:
                    cmd_object.send_instructions()
            return

        self.caller.msg("Set {0} to {1}".format(cmd_object.key, cmd_object.value))


    def parse_chargen_args(self):
        """self.args is a string of everything after set, including a leading space"""
        args = self.args.strip().split(' ')
        if len(args) < 2:
            ''' always expecting key/value pair '''
            raise ValueError

        key = args[0].lower()

        """ make sure it's ascii """
        value = ' '.join(args[1:]).encode('ascii')
        value = value.lower()

        return key, value


class ChargenSetSubtype(object):
    def __init__(self, caller):
        self.caller = caller
        self.key = None
        self.value = None

    def format_instructions(self):
        if self.valid_values:
            return self.instructions + "\nValid values: {0}".format(', '.join(self.valid_values))
        return self.instructions

    def send_instructions(self, error_msg=None):
        if not self.instructions:
            self.caller.msg('This shouldn\'t happen, no valid instructions found')
            return

        if error_msg:
            self.caller.msg(error_msg)

        self.caller.msg(self.format_instructions())

    def validate(self, key, value):
        if self.valid_keys and key not in self.valid_keys:
            fmt_keys = ', '.join(self.valid_keys)
            raise ChargenInputException('Invalid key: {0}\nAcceptable keys: {1}'.format(key, fmt_keys))
        if self.valid_values and value not in self.valid_values:
            raise ChargenInputException('Invalid value: {0}'.format(value))


class ChargenSetDone(ChargenSetSubtype):
    instructions = ('Go NORTH to finalize this section, or RESET to go back to the start\n')
    valid_values = None
    valid_keys = None

    def __init__(self, caller):
        super(ChargenSetDone, self).__init__(caller)

    def run(self):
        raise ChargenInputException


class ChargenSetName(ChargenSetSubtype):
    instructions = ('Use SET FIRST_NAME <name> or SET LAST_NAME <name>\n'
                    'Only one word allowed for each, no special characters or spaces.')
    valid_keys = [
        'first_name',
        'last_name'
    ]
    valid_values = None

    def __init__(self, caller):
        super(ChargenSetName, self).__init__(caller)

    def run(self):
        from typeclasses.characters import Character
        self.validate(self.key, self.value)

        """ ensure just the first letter is capitalized """
        self.value = self.value[0].upper() + self.value[1:].lower()

        if self.key == 'first_name':
            matches = Character.objects.filter(db_key__exact=self.value)
            if matches:
                if len(matches) != 1:
                    ''' should never happen '''
                    raise ChargenFatalException('Too many matching characters by that name?')
                if matches[0] != self.caller:
                    """ If there's a match, should be the same character. """
                    raise ChargenInputException('Name is already in use. Please pick another.')
            self.caller.db.first_name = self.value

            if self.caller.name != self.value:
                self.caller.msg('Renaming character to match new first name.')
                self.caller.name = self.value
        elif self.key == 'last_name':
            self.caller.db.last_name = self.value
        else:
            '''Should never get here?'''
            raise ChargenFatalException('Something weird happened, invalid key passed first check.')


class ChargenSetGender(ChargenSetSubtype):
    instructions = ('Use: SET GENDER <gender>\n'
                    'This has no mechanical effect in game.')
    valid_keys = [
        'gender'
    ]

    valid_values = [
        'male',
        'female',
        'neither'
    ]

    def __init__(self, caller):
        super(ChargenSetGender, self).__init__(caller)

    def run(self):
        self.validate(self.key, self.value)

        self.caller.db.gender = self.value


class ChargenSetCombatantType(ChargenSetSubtype):
    from typeclasses.backgrounds import ALL_COMBATANT_TYPES

    instructions = 'Use: SET COMBATANT_TYPE <type>'

    valid_keys = [
        'combatant_type'
    ]

    valid_values = [x.string for x in ALL_COMBATANT_TYPES]

    def __init__(self, caller):
        super(ChargenSetCombatantType, self).__init__(caller)

    def run(self):
        from typeclasses.backgrounds import ALL_COMBATANT_TYPES
        self.validate(self.key, self.value)

        combatant_type = [x for x in ALL_COMBATANT_TYPES if x.string == self.value]
        if not combatant_type:
            raise ChargenInputException('Cannot find matching combatant type')
        if len(combatant_type) != 1:
            raise ChargenFatalException('Too many matching combatant types?')

        self.caller.db.combatant_type = combatant_type[0]


class ChargenSetBackground(ChargenSetSubtype):
    instructions = 'Use: SET BACKGROUND <background type>'
    valid_keys = [
        'background'
    ]

    def __init__(self, caller):
        super(ChargenSetBackground, self).__init__(caller)

    @property
    def valid_values(self):
        from typeclasses.backgrounds import ALL_BACKGROUNDS
        res = [x.string for x in ALL_BACKGROUNDS if x.type == self.caller.db.combatant_type]
        return res

    def run(self):
        from typeclasses.backgrounds import ALL_BACKGROUNDS
        self.validate(self.key, self.value)

        chosen = [x for x in ALL_BACKGROUNDS if x.string == self.value]
        if not chosen:
            raise ChargenInputException('No matching background')
        if len(chosen) != 1:
            raise ChargenFatalException('Too many matching backgrounds?')
        self.caller.db.background = chosen[0]


class ChargenSetStartingSkill(ChargenSetSubtype):
    instructions = 'Use: SET SKILL <skill>'
    valid_keys = [
        'skill'
    ]

    def __init__(self, caller):
        super(ChargenSetStartingSkill, self).__init__(caller)

    @property
    def valid_values(self):
        if not self.caller.db.background or not self.caller.db.combatant_type:
            raise ValueError('Cannot set character background until caste and type are set')
        skills = set()

        if self.caller.db.background.bonus_skills:
            skills = set(skills | set(self.caller.db.background.bonus_skills))
        if self.caller.db.background.caste.starting_skills:
            skills = set(skills | set(self.caller.db.background.caste.starting_skills))
        if self.caller.db.combatant_type.starting_skills:
            skills = set(skills | set(self.caller.db.combatant_type.starting_skills))
        return [x.string for x in skills]

    def run(self):
        self.validate(self.key, self.value)
        self.caller.db.starting_skill = self.value


class CmdChargenReset(BaseCommand):
    key = "reset"
    help_category = "chargen"

    def func(self):
        self.caller.msg('Resetting chargen state.')
        self.caller.db.chargen_state = 'name'
        self.caller.db.starting_skill = None
        self.caller.db.background = None
        self.caller.db.combatant_type = None
