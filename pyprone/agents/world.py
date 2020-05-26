from typing import List

from pyprone.core import PrObj
from pyprone.entities import PrTextFactory

class PrWorld(PrObj):
    """
    set of entities - only one [Obj]
    no secret - showuld be globally shared to all Views and Acts
    """
    def __init__(self, name: str):
        super().__init__(name)

        self.entities: List[PrObj] = []

        self.entities.append(PrTextFactory('con', '>>>'))
        self.entities.append(PrTextFactory('mon'))

    def show(self):
        """ show what I have """
        for entity in self.entities:
            if isinstance(entity, PrObj):
                self.log(f'has : {entity.whoami}')

    def find_id(self, target: any) -> int:
        """ find object id from name """
        if target:
            if isinstance(target, int):
                return target
            if isinstance(target, str):
                for entity in self.entities:
                    if entity.name == target:
                        return entity.id
        return None

    def find(self, target: any) -> PrObj:
        """ find object from target_id """
        if target:
            target_id: int = self.find_id(target)
            for entity in self.entities:
                if isinstance(entity, PrObj):
                    if entity.id == target_id:
                        return entity
        self.log(f'couldn\'t find the PrObj for target : {target_id}')
        return None
