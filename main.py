import asyncio
import discord
from discord.ext import commands

from config import DISCORD_TOKEN, COMMAND_PREFIX
from bot.db import init_db
from bot.utils.error_handler import handle_error

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=intents,
    help_command=None,  # 기본 help 비활성화 (커스텀으로 교체)
)

COGS = [
    "bot.cogs.help_cog",
    "bot.cogs.register",
    "bot.cogs.recommend",
    "bot.cogs.record",
    "bot.cogs.scheduler",
    "bot.cog.rival",
]


@bot.event
async def on_ready():
    init_db()
    print(f"{'='*40}")
    print(f"  ✅ 봇 로그인 완료")
    print(f"  🤖 {bot.user} (ID: {bot.user.id})")
    print(f"  📋 로드된 Cog: {len(COGS)}개")
    print(f"{'='*40}")


@bot.event
async def on_command_error(ctx, error):
    await handle_error(ctx, error)


async def main():
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"  ✅ Cog 로드: {cog}")
            except Exception as e:
                print(f"  ❌ Cog 로드 실패: {cog} — {e}")
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())