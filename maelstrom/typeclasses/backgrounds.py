"""
Backgrounds

Character background determines certain chargen options
"""
from .skills import COMBAT_SKILLS, NONCOMBAT_SKILLS


class CharacterCaste(object):
    starting_skills = None


class CasteUnderworld(CharacterCaste):
    pass


class CastePeasant(CharacterCaste):
    pass


class CasteHighborn(CharacterCaste):
    pass


ALL_CASTES = [
    CasteUnderworld,
    CastePeasant,
    CasteHighborn
]


class CharacterCombatantType(object):
    string = None
    combat_slots = None
    noncom_slots = None
    starting_skills = None


class CombatantTypeCombatant(CharacterCombatantType):
    string = 'combatant'
    combat_slots = 3
    noncom_slots = 1
    starting_skills = COMBAT_SKILLS


class CombatantTypeNoncombatant(CharacterCombatantType):
    string = 'non-combatant'
    combat_slots = 1
    noncom_slots = 3
    starting_skills = NONCOMBAT_SKILLS


class CombatantTypeBalanced(CharacterCombatantType):
    string = 'balanced'
    combat_slots = 2
    noncom_slots = 2
    starting_skills = NONCOMBAT_SKILLS


ALL_COMBATANT_TYPES = [
    CombatantTypeBalanced,
    CombatantTypeCombatant,
    CombatantTypeNoncombatant
]


class CharacterBackground(object):
    caste = None
    type = None
    bonus_skills = None


class BackgroundThug(CharacterBackground):
    string = 'thug'
    caste = CasteUnderworld
    type = CombatantTypeCombatant


class BackgroundThief(CharacterBackground):
    string = 'thief'
    caste = CasteUnderworld
    type = CombatantTypeNoncombatant


class BackgroundUrchin(CharacterBackground):
    string = 'urchin'
    caste = CasteUnderworld
    type = CombatantTypeBalanced


class BackgroundPage(CharacterBackground):
    string = 'page'
    caste = CasteHighborn
    type = CombatantTypeCombatant


class BackgroundStudent(CharacterBackground):
    string = 'student'
    caste = CasteHighborn
    type = CombatantTypeNoncombatant


class BackgroundHighborn(CharacterBackground):
    string = 'highborn'
    caste = CasteHighborn
    type = CombatantTypeBalanced


class BackgroundSurvivalist(CharacterBackground):
    string = 'survivalist'
    caste = CastePeasant
    type = CombatantTypeCombatant


class BackgroundApprentice(CharacterBackground):
    string = 'apprentice'
    caste = CastePeasant
    type = CombatantTypeNoncombatant


class BackgroundAdventurer(CharacterBackground):
    string = 'adventurer'
    caste = CastePeasant
    type = CombatantTypeBalanced


ALL_BACKGROUNDS = [
    BackgroundApprentice,
    BackgroundSurvivalist,
    BackgroundAdventurer,
    BackgroundHighborn,
    BackgroundPage,
    BackgroundStudent,
    BackgroundThief,
    BackgroundThug,
    BackgroundUrchin
]


def backgrounds_by_caste(caste):
    if type(caste) != CharacterCaste:
        raise ValueError('must pass caste type')
    return [x for x in ALL_BACKGROUNDS if x.caste == caste]
