import machine, jobSource, jobSink, utils, resourcePool, resourcePickup, resourceDrop
import numpy as np
import pandas as pd
from collections import OrderedDict

class Factory:

    def __init__(self):
        self.time_unit = None
        self.head = None
        self.factoryEntities = []
        self.waitingJobs = OrderedDict()

        self.resetStats()
        self.init()


    def reset(self):
        self.resetStats()
        for entity in self.factoryEntities:
            entity.reset()
        self.waitingJobs = OrderedDict()
        
    
    def resetStats(self):
        self.machineStats = pd.DataFrame(columns = ['MachineID', 'Time', 'Queue Size', 'Processing', 'Idle'])
        self.throughputStats = pd.DataFrame(columns=['JobID', 'CreationTime', 'FinishTime', 'SourceID', 'SinkID', 'Latency', 'ProcTime', 'IdleTime', 'WaitingTime'])
        self.jobStats = pd.DataFrame(columns=['JobID', 'MachineID', 'TotTime', 'ProcTime', 'IdleTime', 'WaitingTime'])

        self.jobsCreated = 0
        self.jobsFinished = 0
        self.jobCreationRate = 0
        self.throughput = 0
        self.avgLatency = 0
        self.avgIdle = 0
        self.avgProc = 0
        self.avgWaiting = 0

        self.elapsedTime = 0
    

    # Initialize Factory Layout
    def init(self):
        source = jobSource.JobSource(self, "srcA", -9, 0, "test", lambda: np.random.exponential(75))
        self.head = source
        pan_pool = resourcePool.ResourcePool(self, 'p1', 0, 0, "pan", 15)
        pan_pickup = resourcePickup.ResourcePickup(self, "pan pickup", "Pan Pickup", 0, 0, pan_pool)
        source.addNext(pan_pickup)


        m0 = machine.Machine(self, 0, "Dough Flattener", 0, 0, lambda: np.random.normal(10, 5))
        pan_pickup.addNext(m0)

        m1 = machine.Machine(self, 1, "Topping Assembly", 0, 0, lambda: np.random.normal(60, 12))
        m0.addNext(m1)

        m2_0 = machine.Machine(self, 20, "Oven", 0, 0, lambda: np.random.normal(4*60, 48))
        m2_1 = machine.Machine(self, 21, "Oven", 0, 0, lambda: np.random.normal(4*60, 48))
        m2_2 = machine.Machine(self, 22, "Oven", 0, 0, lambda: np.random.normal(4*60, 48))
        m1.addNext(m2_0)
        m1.addNext(m2_1)
        m1.addNext(m2_2)

        m3_0_0 = machine.Machine(self, 300, "Oven", 0, 0, lambda: np.random.normal(9*60, 60))
        m3_0_1 = machine.Machine(self, 301, "Oven", 0, 0, lambda: np.random.normal(9*60, 60))
        m3_0_2 = machine.Machine(self, 302, "Oven", 0, 0, lambda: np.random.normal(9*60, 60))
        m2_0.addNext(m3_0_0)
        m2_0.addNext(m3_0_1)
        m2_0.addNext(m3_0_2)

        m3_1_0 = machine.Machine(self, 310, "Cooling", 0, 0, lambda: np.random.normal(9*60, 60))
        m3_1_1 = machine.Machine(self, 311, "Cooling", 0, 0, lambda: np.random.normal(9*60, 60))
        m3_1_2 = machine.Machine(self, 312, "Cooling", 0, 0, lambda: np.random.normal(9*60, 60))
        m2_1.addNext(m3_1_0)
        m2_1.addNext(m3_1_1)
        m2_1.addNext(m3_1_2)

        m3_2_0 = machine.Machine(self, 320, "Cooling", 0, 0, lambda: np.random.normal(9*60, 60))
        m3_2_1 = machine.Machine(self, 321, "Cooling", 0, 0, lambda: np.random.normal(9*60, 60))
        m3_2_2 = machine.Machine(self, 322, "Cooling", 0, 0, lambda: np.random.normal(9*60, 60))
        m2_2.addNext(m3_2_0)
        m2_2.addNext(m3_2_1)
        m2_2.addNext(m3_2_2)

        m4 = machine.Machine(self, 4, "Boxing", 0, 0, lambda: np.random.normal(10, 5), nextStepMethod="random", queue_capacity=9)
        m3_0_0.addNext(m4)
        m3_0_1.addNext(m4)
        m3_0_2.addNext(m4)
        m3_1_0.addNext(m4)
        m3_1_1.addNext(m4)
        m3_1_2.addNext(m4)
        m3_2_0.addNext(m4)
        m3_2_1.addNext(m4)
        m3_2_2.addNext(m4)

        pan_drop = resourceDrop.ResourceDrop(self, "pan_drop", "Pan Drop", 0, 0, pan_pool,  nextStepMethod='random')
        m4.addNext(pan_drop)
  
        sink  = jobSink.JobSink(self, -1, 0, 0)
        pan_drop.addNext(sink)
    

    def run(self, run_time, time_unit, start_time=0):
        for t in range(start_time, start_time+run_time, time_unit):
            self.step_all(self.head, time_unit, t)
            self.processWaitingJobs(t)
            self.elapsedTime += time_unit
    

    def step_all(self, head, time_unit, t):
        # BFS Processing of time step of factory tree
        visited = []
        queue = []
        visited.append(head)
        queue.append(head)
        while len(queue) > 0:
            cur = queue.pop(0)
            cur.step(time_unit, t)
            for child in cur.getNextSteps():
                if child not in visited:
                    visited.append(child)
                    queue.append(child)


    def processWaitingJobs(self, t):
        completed = []
        for job, entity in self.waitingJobs.items():
            if entity.moveJob(job, t):
                completed.append(job)
        for job in completed:
            self.waitingJobs.pop(job)

        
    def addWaitingJob(self, job, entity):
        if job not in self.waitingJobs.keys():
            self.waitingJobs[job] = entity


    def addEntity(self, entity):
        self.factoryEntities.append(entity)


    def updateFactoryStats(self):
        assert(len(self.throughputStats) == len(self.throughputStats['JobID'].unique()))
        self.jobsCreated = len(self.throughputStats)
        self.jobsFinished = len(self.throughputStats[~self.throughputStats['FinishTime'].isna()])
        self.jobCreationRate = self.jobsCreated/(self.elapsedTime/60/60)
        self.throughput = self.jobsFinished/(self.elapsedTime/60/60)
        self.avgLatency = np.mean(self.throughputStats['Latency'])
        self.avgIdle = np.mean(self.throughputStats['IdleTime'])
        self.avgProc = np.mean(self.throughputStats['ProcTime'])
        self.avgWaiting = np.mean(self.throughputStats['WaitingTime'])
    

    def printFactoryStats(self):
        self.updateFactoryStats()
        print(f"Factory Run Summary")
        print(f"--------------------------------------")
        print(f"Elapsed Time: {utils.returnAuto(self.elapsedTime)} ({self.elapsedTime}s)    Jobs Created: {self.jobsCreated}  Jobs Finished: {self.jobsFinished}")
        print(f"Job Creation Rate: %.2f jobs/hr   Throughput: %.2f jobs/hr"%(self.jobCreationRate, self.throughput))
        print(f"Avg Latency: {utils.returnAuto(self.avgLatency)} (%.2fs)  Avg Processing Time: {utils.returnAuto(self.avgProc)} (%.2fs)    Avg Idle Time: {utils.returnAuto(self.avgIdle)} (%.2fs)    Avg Waiting Time: {utils.returnAuto(self.avgWaiting)} (%.2fs)"%(self.avgLatency, self.avgProc, self.avgIdle, self.avgWaiting))


    def machineStatsEntry(self, entry):
        self.machineStats = self.machineStats.append(entry, ignore_index=True)


    def jobStatsEntry(self, entry):
        self.jobStats = self.jobStats.append(entry, ignore_index=True)
    

    def throughputStatsEntry(self, entry):
        self.throughputStats = self.throughputStats.append(entry, ignore_index=True)
    

    def throughputStatsUpdate(self, jobID, entry):
        for stat in entry:
            self.throughputStats.loc[self.throughputStats['JobID']==jobID, stat] = entry[stat]
        
    
    def getMachineStats(self):
        return self.machineStats
    

    def getThroughputStats(self):
        return self.throughputStats

    
    def getJobStats(self):
        return self.jobStats


    def getRunStats(self):
        return {'Elapsed Time': self.elapsedTime, 'JobsCreated': self.jobsCreated, 'JobsFinished': self.jobsFinished, 'JobCreationRate': self.jobCreationRate, 'Throughput': self.throughput, 'AvgLatency': self.avgLatency, 'AvgIdle': self.avgIdle, 'AvgProcessing': self.avgProc, 'AvgWaiting': self.avgWaiting}
