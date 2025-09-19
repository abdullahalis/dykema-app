class ConversationManager():
    def __init__(self):
        pass
        self.history = []
    
    def addMessage(self, role, message):
        entry = {"role": role, "content": message}
        self.history.append(entry)
    
    def getHistory(self):
        return self.history