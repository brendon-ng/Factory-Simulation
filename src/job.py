class Job:

    def __init__(self, factory, jobID, jobType, creationTime):
        self.factory = factory
        self.jobID = jobID
        self.jobType = jobType
        self.creationTime = creationTime
        self.status = None
        self.timeToFinish = None

        # cumulative timing stats over all entities
        self.totProcessingTime = 0
        self.totIdleTime = 0
        self.totWaitingTime = 0

        # cumulative timing stats over current entity (reset to 0 when moved to new entity)
        self.curProcessingTime = 0
        self.curIdleTime = 0
        self.curWaitingTime = 0

    # Start job and timing stats within a certain entity
    def startJob(self, current_time, entityID):
        self.jobStart = current_time
        self.entityID = entityID
        # clear current entity timing stats
        self.curIdleTime = 0
        self.curProcessingTime = 0
        self.curWaitingTime = 0

    # End job at the current entity
    def endJob(self, current_time):
        if self.isWaiting():
            self.curWaitingTime += current_time - self.waitingStart
            self.totWaitingTime += self.curWaitingTime
        if self.isProcessing():
            self.curProcessingTime += current_time - self.processingStart
            self.totProcessingTime += self.curProcessingTime
        if self.isIdle():
            self.curIdleTime += current_time - self.idleStart
            self.totIdleTime += self.curIdleTime
        self.status = None
        # save stats
        self.factory.jobStatsEntry({'JobID':self.jobID, 'MachineID':self.entityID, 'TotTime':current_time-self.jobStart, 'ProcTime':self.curProcessingTime, 'IdleTime':self.curIdleTime, 'WaitingTime': self.curWaitingTime})

    # Finish entire life of the job (over all entities)
    def finish(self, finishTime, sinkID):
        self.finishTime = finishTime
        self.latency = self.finishTime-self.creationTime
        self.factory.throughputStatsUpdate(self.jobID, {'SinkID':sinkID, 'FinishTime':finishTime, 'Latency':self.latency, 'ProcTime':self.totProcessingTime, 'IdleTime':self.totIdleTime, 'WaitingTime':self.totWaitingTime})

    def toWaiting(self, current_time):
        assert(not self.isProcessing() or self.processingStart is not None)
        assert(not self.isIdle() or self.idleStart is not None)
        assert(not self.isWaiting() or self.waitingStart is not None)
        if self.isProcessing():
            self.curProcessingTime += current_time - self.processingStart
            self.totProcessingTime += self.curProcessingTime
        if self.isIdle():
            self.curIdleTime += current_time - self.idleStart
            self.totIdleTime += self.curIdleTime
        if not self.isWaiting():
            self.status = 'waiting'
            self.waitingStart = current_time
        assert(self.status == 'waiting')

    def toProcessing(self, current_time, TTF):
        assert(not self.isProcessing() or self.processingStart is not None)
        assert(not self.isIdle() or self.idleStart is not None)
        assert(not self.isWaiting() or self.waitingStart is not None)
        if self.isWaiting():
            self.curWaitingTime += current_time - self.waitingStart
            self.totWaitingTime += self.curWaitingTime
        if self.isIdle():
            self.curIdleTime += current_time - self.idleStart
            self.totIdleTime += self.curIdleTime
        if not self.isProcessing():
            self.status = 'processing'
            self.processingStart = current_time
        assert(self.status == 'processing')

        self.setTTF(TTF)
    
    def toIdle(self, current_time):
        assert(not self.isProcessing() or self.processingStart is not None)
        assert(not self.isIdle() or self.idleStart is not None)
        assert(not self.isWaiting() or self.waitingStart is not None)
        if self.isWaiting():
            self.curWaitingTime += current_time - self.waitingStart
            self.totWaitingTime += self.curWaitingTime
        if self.isProcessing():
            self.curProcessingTime += current_time - self.processingStart
            self.totProcessingTime += self.curProcessingTime
        if not self.isIdle():
            self.status = 'idle'
            self.idleStart = current_time
        assert(self.status == 'idle')

    def assignResource(self, resource):
        self.resource = resource
    
    def getResource(self):
        return self.resource

    def setTTF(self, TTF):
        self.timeToFinish = TTF
    
    def decreaseTTF(self, amt):
        self.timeToFinish -= amt

    def getTimeToFinish(self):
        return self.timeToFinish
    
    def isProcessing(self):
        return self.status=='processing'
    
    def isIdle(self):
        return self.status=='idle'
    
    def isWaiting(self):
        return self.status=='waiting'

    
