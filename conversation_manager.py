class ConversationManager():
    def __init__(self):
        self.history = []
    
    def add_message(self, user, role, message):
        entry = {"role": role, "content": message}
        
        self.history.append(entry)
    
    def get_history(self, user):
        return self.history