from entity import Entity

class Resource(Entity):

    def __init__(self, factory, entityID, x, y, resource_type):
        super().__init__(factory, entityID, resource_type, x, y)
        self.resource_type = resource_type
        
    #Override
    def step(self, time_unit, current_time):
        pass

    def assignJob(self, job):
        self.job = job
