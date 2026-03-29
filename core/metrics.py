# Class to track the system performance 
class Metrics:
    def __init__(self):
        self.busy_time=0   # Total time CPU was busy actively executing

    def update(self, execution_time):
        self.busy_time+=execution_time   # CPU was busy during execution

    def cpu_utilization(self, current_time):
        if current_time==0:
            return 0
        return (self.busy_time/current_time)*100