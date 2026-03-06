import discord
from discord.ext import commands
from bot.db import user_repo
from bot.utils.rival import get_rival_comparison, build_vs_bar


class Rival(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="라이벌")
    async def rival(self, ctx, member: discord.Member = None):
        """
        !라이벌 [@멘션] - 나와 상대방의 통계 1:1 비교
        예) !라이벌 @친구
        """
        if not member:
            await ctx.send(
                "❌ 비교할 상대를 멘션해줘!\n"
                "사용법: `!라이벌 [@상대방]`"
            )
            return
        
        if member.id == ctx.author.id:
            await ctx.send("🤔 자기 자신과는 비교할 수 없어!")
            return
        
        user_me = user_repo.get_user(str(ctx.author.id))
        user_rival = user_repo.get_user(str(member.id))
        
        if not user_me:
            await ctx.send("❌ 네가 아직 등록되지 않았어!\n`!등록 [핸들]` 로 먼저 등록해줘.")
            return
        if not user_rival:
            await ctx.send(f"❌ **{member.display_name}** 님이 아직 등록되지 않았어!")
            return

        msg = await ctx.send("⚔️ 라이벌 비교 데이터 불러오는 중...")
        
        data = await get_rival_comparison(str(ctx.author.id), str(member.id))
        if not data:
            await msg.edit(content="❌ 데이터를 불러오지 못했어. 잠시 후 다시 시도해줘!")
            return
        
        a = data["a"]
        b = data["b"]
        
        # 티어 비교 막대
        tier_bar_a, tier_bar_b = build_vs_bar(a["tier"], b["tier"])
        # 풀이 수 비교 막대
        solved_bar_a, solved_bar_b = build_vs_bar(a["solved_count"], b["solved_count"])
        # 이번 주 비교 막대
        weekly_bar_a, weekly_bar_b = build_vs_bar(a["weekly_count"], b["weekly_count"])
        
        # 승자 판정 (티어 + 풀이 수 + 이번 주 합산)
        score_a = (a["tier"] > b["tier"]) + \
                  (a["solved_count"] > b["solved_count"]) + \
                  (a["weekly_count"] > b["weekly_count"])
        score_b = 3 - score_a
        
        if score_a > score_b:
            winner = f"🏆 **{a['handle']}** 우세!"
        elif score_b > score_a:
            winner = f"🏆 **{b['handle']}** 우세!"
        else:
            winner = "🤝 **팽팽한 라이벌!**"
        
        embed = discord.Embed(
            title=f"⚔️ {a['handle']} vs {b['handle']}",
            description=winner,
            color=0xFF6B6B,
        )
        embed.add_field(
            name="🎖️ 티어",
            value=(
                f"`{a['tier_name']}`\n"
                f"`{tier_bar_a}` vs `{tier_bar_b}`\n"
                f"`{b['tier_name']}`"
            ),
            inline=True,
        )
        embed.add_field(
            name="📚 총 풀이",
            value=(
                f"`{a['solved_count']}문제`\n"
                f"`{solved_bar_a}` vs `{solved_bar_b}`\n"
                f"`{b['solved_count']}문제`"
            ),
            inline=True,
        )
        embed.add_field(
            name="🔥 이번 주",
            value=(
                f"`{a['weekly_count']}문제`\n"
                f"`{weekly_bar_a}` vs `{weekly_bar_b}`\n"
                f"`{b['weekly_count']}문제`"
            ),
            inline=True,
        )

        weak_a_str = " / ".join(f"`{t}`" for t in a["weak_tags"]) or "없음"
        weak_b_str = " / ".join(f"`{t}`" for t in b["weak_tags"]) or "없음"

        embed.add_field(
            name=f"⚠️ {a['handle']} 약점",
            value=weak_a_str,
            inline=True,
        )
        embed.add_field(
            name=f"⚠️ {b['handle']} 약점",
            value=weak_b_str,
            inline=True,
        )
        embed.set_footer(
            text="Solved.ac 라이벌 트래커와 연동된 데이터 기준"
        )

        await msg.delete()
        await ctx.send(embed=embed)
    
    @commands.command(name="서버현황")
    async def server_status(self, ctx):
        """!서버현황 — 이 서버 스터디 그룹 전체 통계"""
        all_users = user_repo.get_all_users()
        if not all_users:
            await ctx.send("📭 아직 등록된 멤버가 없어!\n`!등록 [핸들]` 로 먼저 등록해줘.")
            return

        from bot.db import record_repo as rr
        from bot.utils.ranking import get_weekly_ranking

        weekly = get_weekly_ranking()
        weekly_total = sum(r["count"] for r in weekly)

        lines = []
        for u in all_users:
            records = rr.get_user_records(u["discord_id"])
            lines.append(f"• `{u['handle']}` — {len(records)}문제")

        embed = discord.Embed(
            title="📊 스터디 그룹 현황",
            description="\n".join(lines),
            color=0x57F287,
        )
        embed.add_field(
            name="👥 등록 멤버",
            value=f"{len(all_users)}명",
            inline=True,
        )
        embed.add_field(
            name="🔥 이번 주 합산",
            value=f"{weekly_total}문제",
            inline=True,
        )
        embed.set_footer(text="!랭킹 으로 순위를 확인해봐!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Rival(bot))