# Import all the core components from the other files
from core.scheduler import RoundRobinScheduler
from core.memory import Memorymanager
from core.metrics import Metrics

# Main system that integrated everything
class AdaptiveSystem:
    def __init__(self, processes, total_memory, time_quantum):
        self.scheduler=RoundRobinScheduler(time_quantum) # CPU scheduler
        self.memory=Memorymanager(total_memory)          # Memory manager
        self.metrics=Metrics()                           # Perfromace tracker
        self.time=0                                      # System clock to track the simulation tiem 
        self.processes=processes                         # List of processes
        self.gantt=[]
        self.halt_reason=None                            # Set if simulation stops early (e.g. impossible memory)

    # Adaptive logiv to change the time quantum based on the cpu usage
    def adaptive_time_quantum(self, cpu_usage):
        if cpu_usage>80:
            return 2         # Reduce time quantum if cpu is overloaded
        elif cpu_usage<30:
            return 5         # Increase time quantum if cpu is underutilized
        return 3             # Default time quantum
    
    # Main loop for execution
    def run(self):

        print("\n--- SYSTEM START ---\n")

        not_arrived=self.processes.copy()  # processes that are still waiting

        while True:

            # Iterate over the copy
            for p in not_arrived[:]:   
                if p.arrival_time<=self.time:          # Check arrival time
                    if self.memory.allocate(p):        # Try to allocate memory
                        self.scheduler.add_process(p)  # Add to ready queue
                        not_arrived.remove(p)          # Remove from waiting list
                    else:
                        p.state="WAITING"
            # handling CPU Idle condiiton
            if self.scheduler.is_empty():              # No process in the ready queue
                if not_arrived:                        # But some processes are present in the waiting queue
                    arrived=[p for p in not_arrived if p.arrival_time<=self.time]
                    if arrived:
                        free_mem=self.memory.total_memory-self.memory.used_memory
                        too_big=[p for p in arrived if p.memory>self.memory.total_memory]
                        if too_big:
                            self.halt_reason=(
                                "Cannot load "+", ".join(p.pid for p in too_big)+
                                ": each needs more memory than the system total ("+str(self.memory.total_memory)+")."
                            )
                            print("\n--- HALT:", self.halt_reason, "---\n")
                            break
                        if all(p.memory>free_mem for p in arrived):
                            self.halt_reason=(
                                "No waiting process fits in free memory ("+str(free_mem)+
                                "); simulation cannot progress (memory deadlock)."
                            )
                            print("\n--- HALT:", self.halt_reason, "---\n")
                            break
                    print(f"Time {self.time}: CPU Idle")
                    self.time+=1 # Move time forward
                    continue     # Skip the rest iteration
                else:
                    break        # break out of loop if no process left
                
            process=self.scheduler.get_next()  # Get next process
            process.state="RUNNING"

            if process.start_time is None:
                process.start_time=self.time   # Record the first execution time (start time)

            # Adaptive adjustment of time quantum
            cpu=self.metrics.cpu_utilization(self.time)
            self.scheduler.time_quantum=self.adaptive_time_quantum(cpu)

            if process.remaining_time<0:
                process.remaining_time=0

            # Execute the process for the time quantum (for the remainig time in case the processes burst time left is less than the time quantum)
            execution_time=min(process.remaining_time, self.scheduler.time_quantum) 
            start_time=self.time 

            print(f"Time {self.time}: Running {process.pid} "
                  f"(Remaining: {process.remaining_time}, Time Quantum: {self.scheduler.time_quantum})")  # print the execution info
            
            self.time+=execution_time                # advance system clock

            end_time=self.time
            self.gantt.append((process.pid, start_time, end_time, self.scheduler.time_quantum))

            process.remaining_time-=execution_time   # Reduce remaining burst time
            self.metrics.update(execution_time)       # Update cpu busy time

            for p in self.scheduler.queue:
                p.waiting_time+=execution_time       # update waiting timw for all other processes

            # Reque the process if its not finished
            if process.remaining_time>0:
                self.scheduler.requeue(process)

            else:
                process.state="TERMINATED" # Mark the status as completed
                process.end_time=self.time # Record the end time of the process

                # Calculate the turnaround time
                process.turnaround_time=process.end_time-process.arrival_time

                print(f"{process.pid} completed at time {self.time}")

                self.memory.deallocate(process) # Free memory

        print("\n--- SYSTEM END ---\n")

        print("Gantt Chart:")

        # Print process sequence
        for entry in self.gantt:
            print(f"| {entry[0]} ", end="")

        print("|")

        # Print timeline
        for entry in self.gantt:
            print(f"{entry[1]}   ", end="")

        # Print last end time
        if self.gantt:
            print(self.gantt[-1][2])

        # Print stats
        cpu_util=self.metrics.cpu_utilization(self.time)
        print("CPU Utilization: ", cpu_util)

        total_wt=0
        total_tat=0

        for p in self.processes:
            print(f"{p.pid} | Waiting: {p.waiting_time} | Turnaround: {p.turnaround_time}")
            total_wt+=p.waiting_time
            total_tat+=p.turnaround_time

        if self.processes:
            print("\nAverage Waiting Time: ", total_wt/len(self.processes))
            print("Average Turnaround Time: ", total_tat/len(self.processes))