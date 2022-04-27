from numpy import Inf
from station import Station

class ResourcePickup(Station):
    def __init__(self, factory, entityID, entityType, x, y, resource_pool, queue_capacity=Inf, nextStepMethod='shortest'):
        super().__init__(factory, entityID, entityType, x, y, job_capacity=Inf, queue_capacity=queue_capacity, nextStepMethod=nextStepMethod)
        self.resource_pool = resource_pool

    #Override
    def addJob(self, job, current_time):
        job.startJob(current_time, self.entityID)
        resource = self.resource_pool.acquireResource(job)
        if resource is not None: # if resource successfully acquired, send to next machine
            # Add to job queue, if it can be sent off, completeJob() will remove it from the queue
            # if it can't be sent off, it will be in the queue and Idle
            self.current_jobs.append(job)
            job.toIdle(current_time)
        else: # Keep waiting if no resource available
            assert(self.getQueueSize() < self.queue_capacity)
            job.toWaiting(current_time)
            self.job_queue.append(job)

    #Override
    def step(self, time_unit, current_time):
        # Jobs waiting for a resource
        for job in self.job_queue:
            assert(job.isWaiting())
            resource = self.resource_pool.acquireResource(job) # attempt to acquire
            if resource is not None: # if successful, send it along
                self.job_queue.remove(job) # remove from waiting queue
                job.toIdle(current_time)
                self.current_jobs.append(job) # add to jobs to pass along
        
        for job in self.current_jobs:
            assert(job.isIdle())
            self.completeJob(job, current_time)

        self.factory.machineStatsEntry({"MachineID": self.entityID, "Time": current_time, "Queue Size": len(self.job_queue), "Processing": sum([1 if j.isProcessing() else 0 for j in self.current_jobs]), "Idle": sum([1 if j.isIdle() else 0 for j in self.current_jobs])})
