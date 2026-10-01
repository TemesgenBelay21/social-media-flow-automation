from app.integrations.mock import MockPlatformAdapter


class TelegramAdapter(MockPlatformAdapter):
    platform_name = "telegram"
