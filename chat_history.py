from langchain_core.messages import HumanMessage, AIMessage

class SessionHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

session_histories = {}

def get_session_history(session_id):
    if session_id not in session_histories:
        session_histories[session_id] = SessionHistory()
    return session_histories[session_id]
