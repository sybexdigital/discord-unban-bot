import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID", "0"))
CHECK_EVERY_MINUTES = 30
SESSION_ID = os.getenv("SESSION_ID", "")