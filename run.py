from src.factory import Factory
import pandas as pd

factory = Factory()
factory.run(2*2600, 5)
factory.printFactoryStats()

machineStats = factory.getMachineStats()
throughputStats = factory.getThroughputStats()
jobStats = factory.getJobStats()

machineStats.to_csv("output/machineStats.csv")
throughputStats.to_csv("output/throughputStats.csv")
jobStats.to_csv("output/jobStats.csv")
