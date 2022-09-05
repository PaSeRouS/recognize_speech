import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')

    with open("training_phrases.json", "r", encoding='utf-8') as file:
        training_phrases_json = file.read()

    training_phrases = json.loads(training_phrases_json)
    
    for display_name, content in training_phrases.items():
        create_intent(
            project_id=project_id,
            display_name=display_name,
            training_phrases_parts=content['questions'],
            message_texts=content['answer']
        )
