from components.material import Material

Bone = Material('bone', 'Bone', 1, 1, 1, 1, 0.1)
Skin = Material('skin', 'Skin', 0.1, 0, 1, 0.1, 0.1)
Flesh = Material('flesh', 'Flesh', 0.2, 0, 1, 0.2, 0.1)
Wood = Material('wood', 'Wood', 1, 0.5, 1, 0.5, 1)
Stone = Material('stone', 'Stone', 2, 1, 0.5, 2, 0.5)
Iron = Material('iron', 'Iron', 2, 2, 1, 2, 1)

material_templates = {
    Bone.uid: Bone,
    Skin.uid: Skin,
    Flesh.uid: Flesh,
    Wood.uid: Wood,
    Stone.uid: Stone,
    Iron.uid: Iron
}
