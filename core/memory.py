# Class to handle memory allocation and deallocation
class Memorymanager:
    def __init__(self, total_memory):
        self.total_memory=total_memory  # Total system memory
        self.used_memory=0              # Total memory in use currently

    def allocate(self, process):
        free_memory=self.total_memory-self.used_memory  # Memory free for use

        # Check if memory is available
        if free_memory>=process.memory:                 
            self.used_memory+=process.memory  # Allocate the memory
            return True                       # Return True representing allocation is successful
        return False                          # Return False is allocation not succesful (not enough memory)

    # Free memory when process completes execution
    def deallocate(self, process):
        self.used_memory-=process.memory      # Release memory 