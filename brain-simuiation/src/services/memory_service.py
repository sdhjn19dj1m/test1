class MemoryService:
    def __init__(self):
# Initialize a simple memory storage
        self.memory = []

    def store(self, data):
# Add data to memory storage        
      self.memory.append(data)
        
        # Return to storage status
        stored_data = {
            "status": "stored",
            "data": data,
            "memory_size": len(self.memory)
        }
        return stored_data

    def retrieve(self, index):
        """
        Retrieval data
        Data stored according to indexes
        """
        if 0 <= index < len(self.memory):
            return {
                "status": "retrieved",
                "data": self.memory[index]
            }
        else:
            return {
                "status": "error",
                "message": "Index out of range"
            }
