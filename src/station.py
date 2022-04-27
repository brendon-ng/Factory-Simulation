from abc import ABC, abstractmethod

from entity import Entity
from numpy import Inf
import numpy as np

class Station(Entity, ABC):
    def __init__(self, factory, entityID, entityType, x, y, job_capacity, queue_capacity, nextStepMethod):
        super().__init__(factory, entityID, entityType, x, y)
        self.nextSteps = []
        self.nextStepMethod = nextStepMethod
        self.job_capacity = job_capacity
        self.queue_capacity = queue_capacity
        self.job_queue = []
        self.current_jobs = []
    
    def reset(self):
        super().reset()
        self.job_queue = []
        self.current_jobs = []
    
    @abstractmethod
    def addJob(self, job, current_time):
        pass

    def completeJob(self, job, current_time):
        job.toIdle(current_time)
        self.factory.addWaitingJob(job, self)

    def moveJob(self, job, current_time):
        assert(len(self.nextSteps) > 0, f"Entity {self.entityID} must have a next step")
        dest = self.getNextStep()
        if(dest is not None):
            job.endJob(current_time)
            dest.addJob(job, current_time)
            self.current_jobs.remove(job)
            return True
        else:
            job.toIdle(current_time)
            return False
    
    def addNext(self, nextStep):
        self.nextSteps.append(nextStep)

    def getNextStep(self):
        assert(self.nextStepMethod in [None, 'shortest', 'random'])
        if self.nextStepMethod==None:
            return None
        elif self.nextStepMethod=='shortest':
            shortest = Inf
            dest = None
            for machine in self.nextSteps:
                if (machine.getProcessingSize() < machine.getProcessingCap()):
                    return machine
                if(machine.getQueueSize() < shortest) and (machine.getQueueSize() < machine.getQueueCap()):
                    dest = machine
                    shortest = machine.getQueueSize()
            return dest
        elif self.nextStepMethod == 'random':
            return self.nextSteps[np.random.randint(0,len(self.nextSteps))]
    
    def getNextSteps(self):
        return self.nextSteps
    
    def getQueueSize(self):
        return len(self.job_queue)
    
    def getProcessingSize(self):
        return len(self.current_jobs)
    
    def getProcessingCap(self):
        return self.job_capacity
    
    def getQueueCap(self):
        return self.queue_capacity
