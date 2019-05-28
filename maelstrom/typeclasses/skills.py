class Skill(object):
    pass


class CombatSkill(Skill):
    pass


class SkillUnarmed(CombatSkill):
    string = 'unarmed'
    pass


class SkillShortswords(CombatSkill):
    string = 'short swords'
    pass


class SkillLongswords(CombatSkill):
    string = 'long swords'
    pass


class SkillDaggers(CombatSkill):
    string = 'daggers'
    pass


class SkillAxes(CombatSkill):
    string = 'axes'
    pass


class SkillClubs(CombatSkill):
    string = 'clubs'
    pass


class SkillShields(CombatSkill):
    string = 'shields'
    pass


class SkillSpears(CombatSkill):
    string = 'spears'
    pass


class SkillStaves(CombatSkill):
    string = 'staves'
    pass


class NoncombatSkill(Skill):
    pass


class SkillPickpocketing(NoncombatSkill):
    string = 'pickpocketing'
    pass


class SkillFarming(NoncombatSkill):
    string = 'farming'
    pass


class SkillWeaving(NoncombatSkill):
    string = 'weaving'
    pass


class SkillCooking(NoncombatSkill):
    string = 'cooking'
    pass


class SkillCarpentry(NoncombatSkill):
    string = 'carpentry'
    pass


class SkillTanning(NoncombatSkill):
    string = 'tanning'
    pass


class SkillSmelting(NoncombatSkill):
    string = 'smelting'
    pass


class SkillGemcutting(NoncombatSkill):
    string = 'gemcutting'
    pass


class SkillPapermaking(NoncombatSkill):
    string = 'papermaking'
    pass


class SkillMedicinePrep(NoncombatSkill):
    string = 'medicine preperation'
    pass


class SkillMasonry(NoncombatSkill):
    string = 'masonry'
    pass


class SkillTailoring(NoncombatSkill):
    string = 'tailoring'
    pass


class SkillWeaponcrafting(NoncombatSkill):
    string = 'weaponcrafting'
    pass


class SkillArmorcrafting(NoncombatSkill):
    string = 'armorcrafting'
    pass


class SkillFurniturecrafting(NoncombatSkill):
    string = 'furniturecrafting'
    pass


class SkillJewelrycrafting(NoncombatSkill):
    string = 'jewelrycrafting'
    pass


class SkillBuilding(NoncombatSkill):
    string = 'building'
    pass


class SkillMedicinecrafting(NoncombatSkill):
    string = 'medicinecrafting'
    pass


class SkillHealing(NoncombatSkill):
    string = 'healing'
    pass


class SkillBookbinding(NoncombatSkill):
    string = 'bookbinding'
    pass


NONCOMBAT_SKILLS = [
    SkillArmorcrafting,
    SkillBookbinding,
    SkillBuilding,
    SkillCarpentry,
    SkillCooking,
    SkillFarming,
    SkillFurniturecrafting,
    SkillGemcutting,
    SkillHealing,
    SkillMasonry,
    SkillMedicinecrafting,
    SkillMedicinePrep,
    SkillPapermaking,
    SkillPickpocketing,
    SkillSmelting,
    SkillTailoring,
    SkillTanning,
    SkillWeaponcrafting
]

COMBAT_SKILLS = [
    SkillAxes,
    SkillClubs,
    SkillDaggers,
    SkillLongswords,
    SkillShields,
    SkillShortswords,
    SkillSpears,
    SkillStaves,
    SkillUnarmed
]