import json
import inspect
import os
from components.material import Material, materials


class ObjectEncoder(json.JSONEncoder):
    """
    Allows more leeway to encode json objects.
    Taken from http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    """
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class JsonTemplateManager(object):
    TEMPLATE_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    MATERIAL_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'materials.json')

    def __init__(self):
        self.material_templates = []
        #self._load_templates()

    def _load_templates(self):
        self.material_templates = self._load_material_templates()

    def _load_material_templates(self):
        if os.path.isfile(self.MATERIAL_FULL_PATH):
            with open(self.MATERIAL_FULL_PATH, 'r') as material_json_file:
                return [Material(**material) for material in json.load(material_json_file)]
        else:
            raise Exception("Materials template file not found at " + self.MATERIAL_FULL_PATH)

    def save(self):
        with open(self.MATERIAL_FULL_PATH, 'w') as material_json_file:
            json.dump(self.material_templates, material_json_file, cls=ObjectEncoder, sort_keys=True)

if __name__ == '__main__':
    template_manager = JsonTemplateManager()
    template_manager.material_templates = materials
    template_manager.save()