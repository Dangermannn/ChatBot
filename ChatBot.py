import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import DefaultApiKeys

def init():
    authenticator = IAMAuthenticator(DefaultApiKeys.API_KEY)
    assistant = AssistantV2(
        version='2021-06-14',
        authenticator=authenticator
    )

    assistant.set_service_url(DefaultApiKeys.BASE_URL)

    session_id = createSession(assistant, DefaultApiKeys.ASSISTANT_ID)

    return authenticator, assistant, session_id

def createSession(assistant, assistant_id):    
    session = assistant.create_session(assistant_id).get_result()
    session_json = json.dumps(session, indent=2)
    session_dict = json.loads(session_json)
    return session_dict['session_id']

def deleteSession(assistant, session_id, assistant_id):
    assistant.delete_session(assistant_id, session_id).get_result()

def send_message(assistant, session_id, assistant_id, message):
    response = assistant.message(
        assistant_id = assistant_id,
        session_id = session_id,
        input={
            'message_type': 'text',
            'text': message
        }
    ).get_result()
    #print(response)
    return response['output']['generic'][0]['text'] if 'text' in response['output']['generic'][0] else ''

def main():
    authenticator, assistant, session_id = init()
    inputMessage = ''
    while inputMessage != "exit":
        inputMessage = input()
        print(send_message(assistant, session_id, DefaultApiKeys.ASSISTANT_ID, inputMessage))
    deleteSession(assistant, session_id, DefaultApiKeys.ASSISTANT_ID)
    print("Session has been removed.")

if __name__ == "__main__":
    main()
