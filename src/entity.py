from abc import ABC, abstractmethod

class Entity(ABC):

    def __init__(self, factory, entityID, entityType, x, y):
        self.factory=factory
        self.entityID = entityID
        self.entityType = entityType
        self.x = x
        self.y = y
        self.originalX = x
        self.originalY = y

        self.factory.addEntity(self)
    
    def reset(self):
        self.x = self.originalX
        self.y = self.originalY
        
    @abstractmethod
    def step(self, time_unit, current_time):
        pass

    def getFactory(self):
        return self.factory

    def getEntityID(self):
        return self.entityID
    
    def getEntityType(self):
        return self.entityType
    
    def getCoordinates(self):
        return (self.x, self.y)

