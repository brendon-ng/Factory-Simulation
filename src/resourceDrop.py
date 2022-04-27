from station import Station
from numpy import Inf

class ResourceDrop(Station):
    def __init__(self, factory, entityID, entityType, x, y, resource_pool, nextStepMethod='shortest'):
        super().__init__(factory, entityID, entityType, x, y, job_capacity=Inf, queue_capacity=0, nextStepMethod=nextStepMethod)
        self.resource_pool = resource_pool
    
    #Override
    def addJob(self, job, current_time):
        job.startJob(current_time, self.entityID)

        # Unlink resource and job and add back to resource pool
        resource = job.getResource()
        job.assignResource(None)
        resource.assignJob(None)
        self.resource_pool.addResource(resource)

        # Add to current jobs to be sent off to next step
        job.toIdle(current_time)
        self.current_jobs.append(job)
    
    #Override
    def step(self, time_unit, current_time):
        # Attempt to send off jobs
        for job in self.current_jobs:
            self.completeJob(job, current_time)
