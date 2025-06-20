import os
import dotenv

dotenv.load_dotenv()

class PostgresConfig:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    def __init__(self):
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")

class Config:
    PostgresConfig: PostgresConfig

    APP_HOST: str
    APP_PORT: int

    AI_KEY: str

    def __init__(self):
        self.PostgresConfig = PostgresConfig()
        self.APP_HOST = os.getenv("APP_HOST")
        self.APP_PORT = os.getenv("APP_PORT")
        self.AI_KEY = os.getenv("AI_KEY")

def new() -> Config:
    return Config()