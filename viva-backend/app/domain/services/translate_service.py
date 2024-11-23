from infrastructure.text.chat_gpt_agent import ChatGptAgent

def translate_english_sentence(sentence):
    translation = ChatGptAgent().translate_english_sentence(sentence)
    return translation
