from domain.services.text_processor import TextProcessor
from domain.services.video_processor import VideoProcessor
from infrastructure.text.chat_gpt_agent import ChatGptAgent
from infrastructure.text.llm_client.assistant import Assistant


class VideoReviewProcessor:
    def execute(self, video):
        if video is not None:
            videoProcessor = VideoProcessor()
            transcript = videoProcessor.get_transcript_from_video(video)
            utterances = TextProcessor.get_utterances_from_Transcript(transcript)
            url = ChatGptAgent().polish_expression(utterances)
            return url


if __name__ == '__main__':
    assistant = Assistant()  # 懒汉式初始化 assistant和thread
    with open("/Users/liuyishou/usr/projects/viva/files/utterances.txt", "r") as f:
        instruction = f.read()
        with open("utterances.txt", "r") as f:
            utterances = f.read()
    assistant.send_message(instruction + utterances)
    assistant.send_message("continue")
    video = 'https://imagehosting4picgo.oss-cn-beijing.aliyuncs.com/imagehosting/240222.mp4'
    url = VideoReviewProcessor().execute(video)
    print(url)


