from station import Station
from job import Job

from numpy import Inf

class JobSource(Station):

    def __init__(self, factory, entityID, x, y, jobType, jobIntervalFunc, nextStepMethod='shortest'):
        super().__init__(factory, entityID, "Source", x, y, job_capacity=Inf, queue_capacity=0, nextStepMethod=nextStepMethod)
        self.jobIntervalFunc = jobIntervalFunc
        self.jobType = jobType
        self.totalJobs = 0
        self.timeTilNextJob = 0
    
    def reset(self):
        super().reset()
        self.totalJobs = 0
        self.timeTilNextJob = 0

    #Override
    def step(self, time_unit, current_time):
        # Time to create new job
        if self.timeTilNextJob <= 0:
            newJob = Job(self.factory, self.totalJobs, self.jobType, current_time)
            self.current_jobs.append(newJob)
            newJob.startJob(current_time, self.entityID)
            print(f"Job {newJob.jobID} created at {current_time}")
            self.factory.throughputStatsEntry({'JobID': newJob.jobID, 'CreationTime':current_time, 'SourceID':self.entityID})
            self.timeTilNextJob = self.jobIntervalFunc()
            self.totalJobs += 1
        else: # Or keep waiting
            self.timeTilNextJob -= time_unit

        for job in self.current_jobs:
            self.completeJob(job, current_time)
    
    #Override
    def addJob():
        pass
