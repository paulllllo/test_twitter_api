from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Twitter API Credentials
    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_CLIENT_ID: str
    TWITTER_CLIENT_SECRET: str
    TWITTER_REDIRECT_URI: str = "https://bf35-129-205-124-218.ngrok-free.app/callback"
    
    # Scopes for Twitter API
    TWITTER_SCOPES: list = ["tweet.read", "tweet.write", "users.read"]
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
