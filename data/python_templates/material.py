from components.material import Material


# This Assumes most pieces of armor will have 1 AC as base.


Skin = Material('skin', 'Skin', hardness=0, sharpness=0, potency=0.2, weight=0.1, value=0)
Flesh = Material('flesh', 'Flesh', hardness=0, sharpness=0, potency=0.2, weight=0.15, value=0)
Fur = Material('fur', 'Fur', hardness=0.1, sharpness=0, potency=0.2, weight=1, value=1)
Leather = Material('leather', 'Leather', hardness=0.1, sharpness=0, potency=0.2, weight=1, value=1)
StuddedLeather = Material('studded_leather', 'Studded Leather', hardness=0.2, sharpness=0, potency=0.2, weight=1.3, value=4.5)
Wood = Material('wood', 'Wood', hardness=0.3, sharpness=0.4, potency=0.5, weight=3, value=0.5)
Scale = Material('scale', 'Scale', hardness=0.4, sharpness=0.5, potency=0.4, weight=4.5, value=5)
Bone = Material('bone', 'Bone', hardness=0.5, sharpness=0.5, potency=0.5, weight=5, value=1)
Stone = Material('stone', 'Stone', hardness=0.5, sharpness=0.2, potency=0.1, weight=6, value=0.1)
Silver = Material('silver', 'Silver', hardness=0.5, sharpness=0.5, potency=1, weight=6, value=125)
Gold = Material('gold', 'Gold', hardness=0.5, sharpness=0.5, potency=2, weight=6, value=250)
Chain = Material('chain', 'Chain', hardness=0.6, sharpness=0.3, potency=0.5, weight=5.5, value=7.5)
Bronze = Material('bronze', 'Bronze', hardness=0.6, sharpness=0.8, potency=0.6, weight=7, value=8)
Iron = Material('iron', 'Iron', hardness=0.7, sharpness=1, potency=0.6, weight=6, value=20)
Steel = Material('steel', 'Steel', hardness=0.8, sharpness=1.2, potency=0.8, weight=6.5, value=150)

material_templates = {
    Skin.uid: Skin,
    Flesh.uid: Flesh,
    Fur.uid: Fur,
    Leather.uid: Leather,
    StuddedLeather.uid: StuddedLeather,
    Wood.uid: Wood,
    Scale.uid: Scale,
    Bone.uid: Bone,
    Stone.uid: Stone,
    Silver.uid: Silver,
    Gold.uid: Gold,
    Chain.uid: Chain,
    Bronze.uid: Bronze,
    Iron.uid: Iron,
    Steel.uid: Steel
}
