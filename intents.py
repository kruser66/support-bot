import os
import json
from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts):

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


def main():
    '''
    Пример файла json для загрузки вопросов и ответов в DialogFlow:
    {
        "Устройство на работу": {
            "questions": [
                "Как устроиться к вам на работу?",
                "Как устроиться к вам?",
                "Как работать у вас?",
                "Хочу работать у вас",
                "Возможно-ли устроиться к вам?",
                "Можно-ли мне поработать у вас?",
                "Хочу работать редактором у вас"
            ],
            "answer": "Если вы хотите устроиться к нам, 
            напишите на почту game-of-verbs@gmail.com мини-эссе о себе и 
            прикрепите ваше портфолио."
        },
        "Забыл пароль": {
            "questions": [
                "Не помню пароль",
                "Не могу войти",
                "Проблемы со входом",
                "Забыл пароль",
                "Забыл логин",
                "Восстановить пароль",
                "Как восстановить пароль",
                "Неправильный логин или пароль",
                "Ошибка входа",
                "Не могу войти в аккаунт"
            ],
            "answer": "Если вы не можете войти на сайт, 
            воспользуйтесь кнопкой «Забыли пароль?» под формой входа. 
            Вам на почту прийдёт письмо с дальнейшими инструкциями. 
            Проверьте папку «Спам», иногда письма попадают в неё."
        },
    }
    '''
    load_dotenv()
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

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
    main()
