from station import Station

from numpy import Inf

class JobSink(Station):
    
    def __init__(self, factory, entityID, x, y):
        super().__init__(factory, entityID, "Sink", x, y, job_capacity=Inf, queue_capacity=0, nextStepMethod=None)
        self.totalJobs = 0
    
    def reset(self):
        super().reset()
        self.totalJobs = 0
    
    #Override
    def addJob(self, job, current_time):
        job.endJob(current_time)
        job.finish(current_time, self.entityID)
        self.totalJobs += 1
        #print(f"Job {job.jobID} Finished at {current_time}!")

    #Override
    def step(self, time_unit, current_time):
        pass
            
