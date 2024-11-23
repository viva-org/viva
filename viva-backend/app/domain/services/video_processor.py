import json

import assemblyai as aai

from infrastructure.speech.assemblyai_client import AssemblyAIClient


class VideoProcessor:

    def get_transcript_from_video(self, uploaded_file):
        transcriber = AssemblyAIClient().get_transcriber()
        transcript = transcriber.transcribe(uploaded_file)
        print(f"Transcription succeed: {transcript.id}")
        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
        transcript_path = "/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/transcripts.txt"
        # 确保目录存在
        with open(transcript_path, 'w') as file:
            json.dump(transcript.json_response, file)
        print(transcript.json_response)
        print("get transcripts successfully!")
        return transcript.json_response


if __name__ == "__main__":
    VideoProcessor().get_transcript_from_video('/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/2024/240330_compressed.mp4')