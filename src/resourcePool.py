from entity import Entity
from resourceObject import Resource

class ResourcePool(Entity):
    def __init__(self, factory, entityID, x, y, resource_type, max_resources):
        super().__init__(factory, entityID, resource_type+"_pool", x, y)
        self.resource_type = resource_type
        self.max_resources = max_resources
        self.resources = [self.createResource(i) for i in range(self.max_resources)]
    
    def reset(self):
        super().reset()
        self.resources = [self.createResource(i) for i in range(self.max_resources)]

    #Override
    def step(self, time_unit, current_time):
        pass

    def createResource(self, id):
        if self.resource_type == 'redback':
            redback = Resource(self.factory, id, 0, 0, "Redback")
            return redback
        else:
            return Resource(self.factory, id, 0, 0, self.resource_type)
    
    def acquireResource(self, job):
        if self.numResourcesRemaining() > 0:
            resource = self.resources.pop(0)
            resource.assignJob(job)
            job.assignResource(resource)
            print(f"Job {job.jobID} acquired resource {resource.entityID}")
            return resource
        else:
            return None
    
    def addResource(self, resource):
        print(f"Resource {resource.entityID} returned")
        self.resources.append(resource)

    def numResourcesRemaining(self):
        return len(self.resources)
