import os
from dotenv import load_dotenv

load_dotenv()

# Discord 설정
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RANKING_CHANNEL_ID = int(os.getenv("RANKING_CHANNEL_ID", "0"))

# Solved.ac 설정
SOLVED_HANDLES = os.getenv("SOLVED_HANDLES", "").split(",")

# DB 설정
DB_PATH = os.path.join("data", "algo_bot.db")

# 봇 설정
COMMAND_PREFIX = "!"
WEEKLY_RANKING_DAY = "mon"  # 매주 월요일
WEEKLY_RANKING_HOUR = 9     # 오전 9시