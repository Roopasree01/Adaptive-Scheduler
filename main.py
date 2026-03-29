# Import required classes from the core folder
from core.process import Process
from core.system import AdaptiveSystem

def get_valid_input(prompt, allow_zero=True):
    while True:
        try:
            value=int(input(prompt))
            if value<0:
                print("Value must be >=0")
                continue
            if not allow_zero and value==0:
                print("Value must be > 0")
                continue
            return value
        except ValueError:
            print("Invalid input. Enter a number.")

while True:
    choice = input("Enter a mode (1: Default, 2: Custom input): ")

    if choice in ["1", "2"]:
        break
    else:
        print("Invalid input. Enter 1 or 2.")

# --- Default Mode ---
if choice=="1":
    print("\nUsing default processes...\n")

    # Predefined proceeses 
    processes=[
        Process("P1", 10, 100, 0),
        Process("P2", 5, 200, 2),
        Process("P3", 8, 150, 4)
    ]

    total_memory=500
    time_quantum=3

# --- User Input Mode ---
else:
    print("\nEnter process details:\n")

    processes=[]

    n=get_valid_input("Enter number of processes: ")  # Number of processes

    for i in range(n):
        pid=f"P{i+1}"  # Auto generate process id

        bt=get_valid_input(f"Enter burst time for {pid}: ")  # Take burst time as input
        mem=get_valid_input(f"Enter memory for {pid}: ")     # Take memory required for the process as input
        at=get_valid_input(f"Enter arrival time for {pid}: ") # Take arrival time as input

        processes.append(Process(pid, bt, mem, at))  # Add these processes to list

    total_memory=get_valid_input("\nEnter total system memory: ") # Take system level memory as input

    while True:
        time_quantum=input("Enter initial time quantum: ")  # Take initial time quantum as an input


        if time_quantum=="":
            time_quantum=3
            break
        try:
            time_quantum=int(time_quantum)
            if(time_quantum<=0):
                print("Invalid input")
                continue
            break
        except ValueError:
            print("Invalid input")

# Run the system
system=AdaptiveSystem(processes, total_memory, time_quantum)

# start the simulation
system.run()