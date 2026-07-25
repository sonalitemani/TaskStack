from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = 'Task Stack'
    APP_ENV: str = 'development'
    DEBUG: bool = True 

    LOG_LEVEL: str 
    SERVER_PORT: int 

    JWT_SECRET: str 
    JWT_ALGORITHM: str 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int 
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int 

    DATABASE_URL: str
    SECRET_KEY: str 
    
    
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()