import assemblyai as aai
import os
from dotenv import load_dotenv

class AssemblyAIClient:
    def get_transcriber(self):
        load_dotenv()
        aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        config = aai.TranscriptionConfig(
            speaker_labels=True,
            speakers_expected=2,
        )
        return aai.Transcriber(config=config)
