from datetime import datetime
import uuid

class ConversationManager():
    def __init__(self, auth, storage):
        self.auth = auth
        self.storage = storage
        self.curr_convo_id = None
    
    def create_new_conversation(self):
        user_id = self.auth.get_user_id()
        if user_id is not None:
            timestamp = datetime.now().isoformat()
            convo_id = str(uuid.uuid4())
            conversation = {
                "id": convo_id,
                "user_id": user_id,
                "messages": []
            }
        
        if self.storage.save_conversation(user_id, convo_id, conversation):
            self.curr_convo_id = convo_id
        else:
            #TODO: handle error
            raise Exception("Couldnt save convo")
        

    def add_message(self, role, message):
        user_id = self.auth.get_user_id()

        if user_id is not None:
            if self.curr_convo_id is None:
                self.create_new_conversation()
            
            new_message = {"role": role, "content": message}

            curr_messages = self.storage.load_conversation(user_id, self.curr_convo_id)['messages']
            curr_messages.append(new_message)
            if not self.storage.save_conversation(user_id, self.curr_convo_id, curr_messages):
                raise Exception("Couldn't save convo")
        else:
            raise Exception("couldnt get user id")
    
    def get_current_convo(self):
        user_id = self.auth.get_user_id()

        if user_id is not None:
            return self.storage.load_conversation(user_id, self.curr_convo_id)['messages']
        else:
            raise Exception("couldnt get current user")
