class Process:
    def __init__(self, pid, burst_time, memory, arrival_time):
        self.pid=pid                    # Unique process id
        self.burst_time=burst_time      # total CPu time required for a process
        self.remaining_time=burst_time  # Time still left to complete a process
        self.memory=memory              # Memory required by a process
        self.arrival_time=arrival_time  # Time at which the process arrived

        self.state="NEW"                # State of the process is new in the beginning (New -> Ready -> Running -> Completed)

        self.waiting_time=0             # Time spent waiting in queue
        self.turnaround_time=0          # Total time from start to the end
        self.start_time=None            # Time when the process started first
        self.end_time=None              # Time when the process finished
