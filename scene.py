from typing import List
from object import Object


class Scene:
    def __init__(self, objects: List[Object]):
        self.objects = objects

    def add_obj_to_scene(self, obj):
        self.objects.append(obj)

    def draw_scene(self, camera=None):
        for obj in self.objects:
            obj.draw(camera)