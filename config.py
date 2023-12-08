from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str("REAL_DATABASE_URL")
BOT_TOKEN = env.str("BOT_TOKEN")

echo = True
