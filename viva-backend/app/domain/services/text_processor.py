from infrastructure.text.chat_gpt_agent import ChatGptAgent


class TextProcessor:

    @staticmethod
    def swap_label_if_necessary(content):
        # Step 1: Read the conversation from a .txt file
        lines = content
        # Step 2: Parse the conversation to count words
        word_count_A = 0
        word_count_B = 0
        for line in lines:
            speaker, sentence = line.split(': ', 1)
            words = sentence.split()
            if speaker == 'speaker A':
                word_count_A += len(words)
            elif speaker == 'speaker B':
                word_count_B += len(words)
        # Step 3: Rewrite the conversation to a new .txt file
        print(f"Speaker A spoke {word_count_A} words")
        print(f"Speaker B spoke {word_count_B} words")

        # Swap speakers if B spoke more than A
        if word_count_B > word_count_A:
            revised_lines = []  # Initialize a new list to hold revised lines
            for line in lines:
                speaker, sentence = line.split(': ', 1)
                if speaker == 'speaker A':
                    speaker = 'speaker B'
                elif speaker == 'speaker B':
                    speaker = 'speaker A'
                revised_line = f"{speaker}: {sentence}"
                revised_lines.append(revised_line)  # Append the revised line to the list
        else:
            revised_lines = lines

        print("Conversation revised and saved to revised_conversation.txt")
        return revised_lines  # Return the revised list of lines

    @staticmethod
    def get_utterances_from_Transcript(json_data):
        utterances = json_data.get("utterances", [])
        content = []
        if utterances is not None:
            for entry in utterances:
                speaker = entry["speaker"]
                text = entry["text"]
                content.append(f"speaker {speaker}: {text}")
        content_labeled = TextProcessor.swap_label_if_necessary(content)
        print("TXT file created successfully!" + " - ")
        # Save the content to the txt file
        with open("/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/utterances.txt", 'w') as file:
            file.write('\n'.join(content_labeled))
        return content_labeled

    def generate_english_sentences_by_ai(self, file_name):
        with open (file_name, "r") as f:
            words = f.read()
        i = 0
        with open("sentence_list.txt", "a") as ff:
            for word in words.split("\n"):
                sentence = ChatGptAgent().generate_sentence_for_word(word)
                res = word + "---" + sentence + "\n"
                ff.write(str(res))
                i += 1
                print(i)
                print(word)

    def split_and_save_to_pg(self):
        with open("", "r") as f:
            content = f.read()
            s = content.split("---")


if __name__ == "__main__":
    # with open("/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/transcripts.txt", 'r') as file:
    #     transcript = json.load(file)
    # content_labeled = TextProcessor.get_utterances_from_Transcript(transcript)
    # print(content_labeled)

    #
    TextProcessor().generate_english_sentences_by_ai("active_words.txt")
    print("over")
