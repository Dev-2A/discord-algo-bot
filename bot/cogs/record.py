import discord
from discord.ext import commands
from bot.db import user_repo, record_repo, tag_repo
from bot.solvedac.client import get_problem_info
from bot.solvedac.parser import parse_problem, get_tier_name, get_tag_ko


class Record(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="완료")
    async def record_solve(self, ctx, problem_id: int = None):
        """
        !완료 [문제번호] - 풀이 완료 기록
        예) !완료 1001
        """
        if not problem_id:
            await ctx.send(
                "❌ 문제 번호를 입력해줘!\n사용법: `!완료 [문제번호]`"
            )
            return
        
        user = user_repo.get_user(str(ctx.author.id))
        if not user:
            await ctx.send(
                "❌ 등록된 핸들이 없어!\n`!등록 [solved.ac 핸들]` 로 먼저 등록해줘."
            )
            return
        
        # 이미 기록된 문제인지 확인
        if record_repo.is_already_solved(str(ctx.author.id), problem_id):
            await ctx.send(
                f"⚠️ **{problem_id}번** 문제는 이미 기록되어 있어! 👍"
            )
            return
        
        msg = await ctx.send(f"🔍 **{problem_id}번** 문제 정보 가져오는 중...")
        
        # Solved.ac에서 문제 정보 조회
        raw = await get_problem_info(problem_id)
        if not raw:
            await msg.edit(
                content=f"❌ **{problem_id}번** 문제를 찾을 수 없어. 번호를 다시 확인해줘!"
            )
            return
        
        problem = parse_problem(raw)
        
        # DB에 풀이 기록 저장
        added = record_repo.add_solve_record(
            discord_id=str(ctx.author.id),
            problem_id=problem["problem_id"],
            title=problem["title"],
            level=problem["level"],
            tags=problem["tags"],
        )
        
        if not added:
            await msg.edit(content=f"⚠️ **{problem_id}번** 문제는 이미 기록되어 있어!")
            return
        
        # 태그 통계 갱신
        for tag in problem["tags"]:
            tag_repo.upsert_tag_stat(str(ctx.author.id), tag)
        
        # 총 풀이 수 조회
        total = len(record_repo.get_user_records(str(ctx.author.id)))
        tier_name = get_tier_name(problem["level"])
        tag_names = " ".join(
            f"`{get_tag_ko(t)}`" for t in problem["tags"][:5]
        )
        
        embed = discord.Embed(
            title="✅ 풀이 기록 완료!",
            color=0x57F287,
        )
        embed.add_field(
            name="문제",
            value=f"**[{problem['problem_id']}. {problem['title']}]({problem['url']})**",
            inline=False,
        )
        embed.add_field(name="난이도", value=tier_name, inline=True)
        embed.add_field(name="누적 풀이", value=f"{total}문제", inline=True)
        embed.add_field(
            name="태그",
            value=tag_names if tag_names else "없음",
            inline=False,
        )
        embed.set_footer(
            text=f"{ctx.author.display_name} | 약점 태그 통계가 갱신됐어!"
        )
        
        await msg.delete()
        await ctx.send(embed=embed)
    
    @commands.command(name="기록")
    async def show_records(self, ctx, count: int = 5):
        """
        !기록 [개수] - 최근 풀이 기록 조회 (기본 5개)
        예) !기록 10
        """
        user = user_repo.get_user(str(ctx.author.id))
        if not user:
            await ctx.send(
                "❌ 등록된 핸들이 없어!\n`!등록 [solved.ac 핸들]` 로 먼저 등록해줘."
            )
            return
        
        records = record_repo.get_user_records(str(ctx.author.id))
        if not records:
            await ctx.send("📭 아직 기록된 풀이가 없어. `!완료 [문제번호]` 로 기록해봐!")
            return
        
        count = min(count, 20) # 최대 20개
        recent = records[:count]
        total = len(records)
        
        lines = []
        for r in recent:
            tier = get_tier_name(r["level"])
            date = r["solved_at"][:10]
            lines.append(
                f"`{r['problem_id']}` **{r['title']}** "
                f"- {tier} ({date})"
            )
        
        embed = discord.Embed(
            title=f"📋 {ctx.author.display_name} 님의 최근 풀이 기록",
            description="\n".join(lines),
            color=0x5865F2,
        )
        embed.set_footer(text=f"총 {total}문제 기록됨 | 핸들: {user['handle']}")
        await ctx.send(embed=embed)
    
    @commands.command(name="프로필")
    async def profile(self, ctx, member: discord.Member = None):
        """
        !프로필 [@멘션] - 본인 또는 다른 사람 프로필 조회
        예) !프로필 / !프로필 @친구
        """
        target = member or ctx.author
        user = user_repo.get_user(str(target.id))
        if not user:
            name = target.display_name
            await ctx.send(f"❌ **{name}** 님은 아직 등록되지 않았어!")
            return
        
        records = record_repo.get_user_records(str(target.id))
        total = len(records)
        
        from bot.db import tag_repo as tr
        top_tags = tr.get_all_tag_stats(str(target.id))[:3]
        weak_tags = tr.get_weak_tags(str(target.id), limit=3)
        
        top_str = " ".join(
            f"`{get_tag_ko(t['tag'])}`" for t in top_tags
        ) or "없음"
        weak_str = " ".join(
            f"`{get_tag_ko(t['tag'])}`" for t in weak_tags
        ) or "없음"
        
        embed = discord.Embed(
            title=f"👤 {target.display_name} 님의 프로필",
            color=0xEB459E,
        )
        embed.add_field(name="핸들", value=f"`{user['handle']}`", inline=True)
        embed.add_field(name="총 풀이", value=f"{total}문제", inline=True)
        embed.add_field(name="강점 태그", value=top_str, inline=False)
        embed.add_field(name="약점 태그", value=weak_str, inline=False)
        embed.set_footer(text=f"가입일: {user['created_at'][:10]}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Record(bot))