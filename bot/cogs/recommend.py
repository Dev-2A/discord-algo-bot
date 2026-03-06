import discord
from discord.ext import commands
from bot.db import user_repo
from bot.solvedac.parser import get_tier_name, get_tag_ko
from bot.utils.recommender import recommend_problem
from bot.utils.weakness_analyzer import get_weak_tags


class Recommend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="오늘문제")
    async def today_problem(self, ctx):
        """!오늘문제 - 약점 태그 기반 문제 추천"""
        user = user_repo.get_user(str(ctx.author.id))
        if not user:
            await ctx.send(
                "❌ 등록된 핸들이 없어!\n`!등록 [solved.ac 핸들]` 로 먼저 등록해줘."
            )
            return
        
        msg = await ctx.send("🎯 약점 태그 분석 중...")
        
        # 약점 태그 미리 보여주기
        weak_tags = get_weak_tags(str(ctx.author.id), limit=3)
        tag_names = " / ".join(
            f"`{get_tag_ko(t['tag'])}`" for t in weak_tags
        )
        await msg.edit(content=f"🔍 약점 태그: {tag_names}\n문제 탐색 중...")
        
        # 문제 추천
        problem = await recommend_problem(str(ctx.author.id), user["handle"])
        
        if not problem:
            await msg.edit(
                content=(
                    "😅 조건에 맞는 문제를 찾지 못했어.\n"
                    "`!동기화` 로 풀이 기록을 갱신한 뒤 다시 시도해봐!"
                )
            )
            return
        
        tag_ko = get_tag_ko(problem["recommended_tag"])
        tier_name = get_tier_name(problem["level"])
        all_tags = " ".join(
            f"`{get_tag_ko(t)}`" for t in problem["tags"][:5]
        )
        
        embed = discord.Embed(
            title=f"🎯 오늘의 추천 문제",
            color=0x7289DA,
        )
        embed.add_field(
            name="문제",
            value=f"**[{problem['problem_id']}. {problem['title']}]({problem['url']})**",
            inline=False,
        )
        embed.add_field(name="난이도", value=tier_name, inline=True)
        embed.add_field(name="추천 이유", value=f"약점 태그: {tag_ko}", inline=True)
        embed.add_field(name="태그", value=all_tags or "없음", inline=False)
        embed.set_footer(text=f"{ctx.author.display_name} 님을 위한 추천 | !완료 {problem['problem_id']} 로 기록하세요")
        
        await msg.delete()
        await ctx.send(embed=embed)
    
    @commands.command(name="약점")
    async def show_weakness(self, ctx):
        """!약점 - 내 약점 태그 통계 조회"""
        user = user_repo.get_user(str(ctx.author.id))
        if not user:
            await ctx.send("❌ 등록된 핸들이 없어!\n`!등록 [solved.ac 핸들]` 로 먼저 등록해줘.")
            return
        
        from bot.utils.weakness_analyzer import get_tag_summary
        summary = get_tag_summary(str(ctx.author.id))
        
        embed = discord.Embed(
            title=f"📊 {ctx.author.display_name} 님의 태그 통계",
            description=summary,
            color=0xF4A460,
        )
        embed.set_footer(text=f"핸들: {user['handle']}")
        await ctx.send(embed=embed)
    
    @commands.command(name="동기화")
    async def sync(self, ctx):
        """!동기화 - Solved.ac 풀이 기록 최신화"""
        user = user_repo.get_user(str(ctx.author.id))
        if not user:
            await ctx.send("❌ 등록된 핸들이 없어!\n`!등록 [solved.ac 핸들]` 로 먼저 등록해줘.")
            return

        msg = await ctx.send(f"⏳ `{user['handle']}` 풀이 기록 동기화 중...")
        from bot.utils.weakness_analyzer import sync_solved_problems
        new_count = await sync_solved_problems(str(ctx.author.id), user["handle"])
        await msg.edit(
            content=f"✅ 동기화 완료! 새로 추가된 문제: **{new_count}문제**"
        )


async def setup(bot):
    await bot.add_cog(Recommend(bot))