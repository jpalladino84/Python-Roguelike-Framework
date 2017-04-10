# TODO Anything could have an EFFECTS component
# TODO This component would keep active effects and respond to queries about modifiers.
# TODO It could also apply effects itself, like damage or healing.
# TODO It should be called in a sort of update loop.


class Effects(object):
    def __init__(self, host_object):
        self.host_object = host_object
        self.active_effects = []

    def update(self):
        finished_effects = []
        for effect in self.active_effects:
            effect.update()
            if effect.finished():
                finished_effects.append(effect)

        for effect in finished_effects:
            self.active_effects.remove(effect)
