from station import Station
import pandas as pd

class Machine(Station):

    def __init__(self, factory, entityID, machineType, x, y, TTFFunc, job_capacity=1, queue_capacity=0, nextStepMethod='shortest'):
        super().__init__(factory, entityID, machineType, x, y, job_capacity, queue_capacity, nextStepMethod)
        self.timeToFinishFunc = TTFFunc

    def willFail(self):
        return False

    #Override
    def addJob(self, job, current_time):
        job.startJob(current_time, self.entityID)
        # If added job can go straight to processing
        if self.getProcessingSize() < self.job_capacity:
            job.toProcessing(current_time, self.timeToFinishFunc())
            self.current_jobs.append(job)
        # If it needs to go to queue
        elif self.getQueueSize() < self.queue_capacity:
            job.toWaiting(current_time)
            self.job_queue.append(job)    

    #Override
    def step(self, time_unit, current_time):
        # Check for jobs that can go from queue to processing
        while len(self.current_jobs) < self.job_capacity and len(self.job_queue) > 0:
            job = self.job_queue.pop(0)
            job.toProcessing(current_time, self.timeToFinishFunc())
            self.current_jobs.append(job)
        
        for job in self.current_jobs:
            # Probabilistically determine if job will fail
            if self.willFail():
                pass # FAIL
            else:
                job.decreaseTTF(time_unit)

            # Job Finished
            if (job.isProcessing() or job.isIdle()) and job.getTimeToFinish() <= 0:
                self.completeJob(job, current_time)
    
        self.factory.machineStatsEntry({"MachineID": self.entityID, "Time": current_time, "Queue Size": len(self.job_queue), "Processing": sum([1 if j.isProcessing() else 0 for j in self.current_jobs]), "Idle": sum([1 if j.isIdle() else 0 for j in self.current_jobs])})
        #print(f"M{self.machineID}, Time {current_time}: Job {[i.jobID for i in self.current_jobs]} IP, Jobs {[i.jobID for i in self.job_queue]} in line")
