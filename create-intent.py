import os
import json
from dotenv import load_dotenv


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
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


def main():
    with open('questions.json', 'r', encoding='utf-8') as file:
        themes = json.load(file)

    for theme, sets in themes.items():
        create_intent(
            'kruser-support-bot',
            theme,
            sets['questions'],
            [sets['answer']]
        )


if __name__ == '__main__':
    load_dotenv()
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    main()
