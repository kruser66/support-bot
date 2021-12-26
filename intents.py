import os
import json
from dotenv import load_dotenv


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts):
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def detect_intent_texts(project_id, session_id, texts, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(
        text=texts,
        language_code=language_code
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


def main(project_id):
    with open('questions.json', 'r', encoding='utf-8') as file:
        themes = json.load(file)

    for theme, sets in themes.items():
        create_intent(
            project_id=project_id,
            display_name=theme,
            training_phrases_parts=sets['questions'],
            # передаем списком, если ответ всего один
            message_texts=[sets['answer']]
        )


if __name__ == '__main__':
    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    google_project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    main(google_project_id)
