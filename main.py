import asyncio
import discord
from discord.ext import commands
from config import DISCORD_TOKEN, COMMAND_PREFIX
from bot.db import init_db

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

COGS = [
    "bot.cogs.register",
    "bot.cogs.recommend",
    "bot.cogs.record",
]

@bot.event
async def on_ready():
    init_db()
    print(f"✅ 봇 로그인 완료: {bot.user} (ID: {bot.user.id})")
    print(f"📋 로드된 Cog: {', '.join(COGS)}")


async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())