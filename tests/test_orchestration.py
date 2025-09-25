import pytest
from orchestration.orchestration_manager import OrchestrationManager
from error.error_types import AuthError, StorageError

class FakeAuthManager:
    def __init__(self, user_id="test_user"):
        self.user_id = user_id

    def get_user_id(self):
        if not self.user_id:
            raise AuthError("No user logged in")
        return self.user_id

class FakeStorageManager:
    def __init__(self):
        self.conversations = {}
        self.counter = 0

    def get_messages(self, user_id, convo_id):
        if convo_id not in self.conversations:
            return []
        return self.conversations[convo_id]["messages"]

    def save_conversation(self, user_id, convo_id, messages):
        if convo_id is None:
            self.counter += 1
            convo_id = f"convo_{self.counter}"
            self.conversations[convo_id] = {"messages": messages, "title": "Untitled"}
        else:
            self.conversations[convo_id]["messages"] = messages
        return convo_id

    def get_conversations(self, user_id):
        return [{"id": cid, "title": data["title"], "updated_at": "2025-09-24T12:00:00"}
                for cid, data in self.conversations.items()]

    def get_conversation_id(self, user_id, title):
        for cid, data in self.conversations.items():
            if data["title"] == title:
                return cid
        raise StorageError("Conversation not found")

    def delete_conversation(self, user_id, convo_id):
        if convo_id not in self.conversations:
            raise StorageError("Conversation not found")
        del self.conversations[convo_id]

    def rename_conversation(self, user_id, convo_id, new_title):
        if convo_id not in self.conversations:
            raise StorageError("Conversation not found")
        self.conversations[convo_id]["title"] = new_title

class FakeLLMManager:
    def build_context(self, messages):
        return messages

    def generate_response(self, messages):
        last_user_msg = [m["content"] for m in messages if m["role"] == "user"][-1]
        yield last_user_msg[::-1]

@pytest.fixture
def orchestration():
    return OrchestrationManager(
        auth_manager=FakeAuthManager(),
        storage_manager=FakeStorageManager(),
        llm_manager=FakeLLMManager()
    )

def test_new_conversation_and_handle_prompt(orchestration):
    orch = orchestration
    orch.create_new_conversation()
    orch.handle_prompt("hello")
    assert orch.curr_convo_id is not None

    messages = orch._get_current_messages()
    assert messages[0]["content"] == "hello"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "olleh"

def test_list_conversations(orchestration):
    orch = orchestration
    orch.create_new_conversation()
    orch.handle_prompt("hi")
    # just ensure it does not raise
    orch.list_conversations()

def test_switch_conversation(orchestration):
    orch = orchestration
    orch.create_new_conversation()
    orch.handle_prompt("chat one")
    orch.rename_conversation("First Chat")

    orch.create_new_conversation()
    orch.handle_prompt("chat two")
    orch.rename_conversation("Second Chat")

    orch.switch_conversation("First Chat")
    assert orch.curr_convo_id in orch.storage_manager.conversations

def test_delete_conversation(orchestration):
    orch = orchestration
    orch.create_new_conversation()
    orch.handle_prompt("bye")
    orch.rename_conversation("Temp Chat")

    orch.delete_conversation("Temp Chat")
    titles = [c["title"] for c in orch.storage_manager.get_conversations("test_user")]
    assert "Temp Chat" not in titles

def test_rename_conversation_without_active(orchestration):
    orch = orchestration
    orch.curr_convo_id = None
    # should not throw, just print
    orch.rename_conversation("Should Fail")
