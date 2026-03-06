import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import asyncio

from config import RANKING_CHANNEL_ID
from bot.utils.ranking import get_weekly_ranking, build_ranking_message


# 매주 월요일 오전 9시 공지
RANKING_TIME = time(hour=9, minute=0)


class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weekly_ranking.start()
    
    def cog_unload(self):
        self.weekly_ranking.cancel()
    
    @tasks.loop(time=RANKING_TIME)
    async def weekly_ranking(self):
        """매일 정해진 시각에 실행 - 월요일에만 공지"""
        if datetime.now().weekday() != 0:   # 0 = 월요일
            return
        
        channel = self.bot.get_channel(RANKING_CHANNEL_ID)
        if not channel:
            print(f"⚠️ 랭킹 채널을 찾을 수 없어요. RANKING_CHANNEL_ID를 확인해줘.")
            return
        
        ranking = get_weekly_ranking()
        message = build_ranking_message(ranking)
        
        now = datetime.now()
        week_str = f"{now.year}년 {now.month}월 {now.day - 7}일 ~ {now.month}월 {now.day - 1}일"
        
        embed = discord.Embed(
            title="🏆 주간 알고리즘 랭킹",
            description=message,
            color=0xFFD700,
        )
        embed.set_footer(text=f"집계 기간: {week_str}")
        await channel.send(embed=embed)
    
    @weekly_ranking.before_loop
    async def before_ranking(self):
        await self.bot.wait_until_ready()
    
    @commands.command(name="랭킹")
    async def show_ranking(self, ctx):
        """!랭킹 - 이번 주 랭킹 즉시 조회"""
        ranking = get_weekly_ranking()
        message = build_ranking_message(ranking)
        
        now = datetime.now()
        embed = discord.Embed(
            title="🏆 이번 주 알고리즘 랭킹",
            description=message,
            color=0xFFD700,
        )
        embed.set_footer(text=f"기준: 최근 7일 | {now.strftime('%Y-%m-%d %H:%M')} 조회")
        await ctx.send(embed=embed)
    
    @commands.command(name="랭킹공지")
    @commands.has_permissions(administrator=True)
    async def force_ranking(self, ctx):
        """!랭킹공지 - 관리자 전용: 주간 랭킹 즉시 공지"""
        channel = self.bot.get_channel(RANKING_CHANNEL_ID)
        if not channel:
            await ctx.send("❌ 랭킹 채널을 찾을 수 없어. `RANKING_CHANNEL_ID`를 확인해줘!")
            return
        
        ranking = get_weekly_ranking()
        message = build_ranking_message(ranking)
        
        now = datetime.now()
        embed = discord.Embed(
            title="🏆 주간 알고리즘 랭킹",
            description=message,
            color=0xFFD700,
        )
        embed.set_footer(text=f"수동 공지 | {now.strftime('%Y-%m-%d %H:%M')}")
        await channel.send(embed=embed)
        await ctx.send("✅ 랭킹 공지 완료!")


async def setup(bot):
    await bot.add_cog(Scheduler(bot))