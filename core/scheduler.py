from collections import deque # Importing deque from collections library (deque is efficient)

# Class implementing Round Robin Scheduling
class RoundRobinScheduler:
    def __init__(self, time_quantum):
        self.time_quantum=time_quantum   # Time quantum
        self.queue=deque()               # Ready queue

    # Add process to the ready queue
    def add_process(self, process):
        process.state="READY"            # Mark process state as "ready"
        self.queue.append(process)

    # Check if the queue is empty
    def is_empty(self):
        return len(self.queue)==0
    
    # Get the next process to execute
    def get_next(self):
        if self.queue:
            return self.queue.popleft() # As queue behave in FIFO manner
        return None
    
    # Readd the process in the ready queue if it's not completed
    def requeue(self, process):
        process.state="READY"          # Set the state of the process as "ready"
        self.queue.append(process)     # Add the process at the end of the queue

        