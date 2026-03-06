import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 기본 help 명령어 제거 후 커스텀으로 교체
        self.bot.remove_command("help")
    
    @commands.command(name="help", aliases=["도움말"])
    async def custom_help(self, ctx):
        """!help / !도움말 - 명령어 목록"""
        embed = discord.Embed(
            title="🤖 알고리즘 스터디 봇 명령어",
            description="Solved.ac 연동 스터디 봇이야. 아래 명령어를 사용해봐!",
            color=0x7289DA,
        )

        embed.add_field(
            name="📝 등록 / 동기화",
            value=(
                "`!등록 [핸들]` — Solved.ac 핸들 등록\n"
                "`!동기화` — 풀이 기록 최신화"
            ),
            inline=False,
        )

        embed.add_field(
            name="🎯 문제 추천",
            value=(
                "`!오늘문제` — 약점 태그 기반 문제 추천\n"
                "`!약점` — 내 약점 태그 통계 조회"
            ),
            inline=False,
        )

        embed.add_field(
            name="✅ 풀이 기록",
            value=(
                "`!완료 [문제번호]` — 풀이 완료 기록\n"
                "`!기록 [개수]` — 최근 풀이 기록 조회\n"
                "`!프로필 [@멘션]` — 프로필 조회"
            ),
            inline=False,
        )

        embed.add_field(
            name="🏆 랭킹",
            value=(
                "`!랭킹` — 이번 주 랭킹 조회\n"
                "`!라이벌` — 라이벌 비교\n"
                "`!랭킹공지` — 수동 공지 (관리자 전용)"
            ),
            inline=False,
        )

        embed.set_footer(text="매주 월요일 오전 9시에 주간 랭킹이 자동 공지돼!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))