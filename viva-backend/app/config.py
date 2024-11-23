from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AI Model Settings

    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gpt-4o"
    ANTHROPIC_API_KEY: str
    CLAUDE_MODEL_NAME: str = "claude-3-sonnet-20240229"
    LLM_MODEL_TYPE: str = "ChatGPT"
    LLM_MODEL_NAME_FOR_BASIC_CHAT: str
    ASSISTANT_ID: str

    # Database Settings
    DATABASE_URL: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DBNAME: str

    # OSS Settings
    OSS_ACCESS_KEY_ID: str
    OSS_ACCESS_KEY_SECRET: str
    ACCESS_KEY_ID: str
    ACCESS_KEY_SECRET: str
    BUCKET_NAME: str
    ENDPOINT: str

    # Authentication Settings
    GOOGLE_CLIENT_ID: str
    JWT_ALGORITHM: str
    JWT_SECRET: str

    # External Services
    ASSEMBLYAI_API_KEY: str
    ELEVENLABS_API_KEY: str
    ELEVENLABS_MODEL: str
    ANKI_CONNECT_URL: str

    # Prompt Files
    SEGMENT_PROMPT_FILE1: str
    SEGMENT_PROMPT_FILE2: str
    SEGMENT_PROMPT_FILE3: str

    # Other Settings
    PYTHONPATH: str
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = "./env"
        case_sensitive = True

config = Settings() 