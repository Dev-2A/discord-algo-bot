import discord
from discord.ext import commands
from bot.db import user_repo
from bot.solvedac.client import get_user_info
from bot.utils.weakness_analyzer import sync_solved_problems


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="등록")
    async def register(self, ctx, handle: str = None):
        """
        !등록 [핸들] - Solved.ac 핸들 등록
        예) !등록 tangi826
        """
        if not handle:
            await ctx.send("❌ 핸들을 입력해줘!\n사용법: `!등록 [solved.ac 핸들]`")
            return
        
        # 이미 등록된 사용자 확인
        existing = user_repo.get_user(str(ctx.author.id))
        if existing:
            await ctx.send(
                f"⚠️ 이미 `{existing['handle']}`로 등록되어 있어!\n"
                f"변경하려면 관리자에게 문의해줘."
            )
            return
        
        # Solved.ac에서 핸들 존재 확인
        msg = await ctx.send(f"🔍 `{handle}` 핸들 확인 중...")
        user_info = await get_user_info(handle)
        if not user_info:
            await msg.edit(content=f"❌ `{handle}` 핸들을 찾을 수 없어. 다시 확인해줘!")
            return
        
        # DB 등록
        success = user_repo.register_user(str(ctx.author.id), handle)
        if not success:
            await msg.edit(content=f"❌ `{handle}` 핸들은 이미 다른 사람이 등록했어!")
            return
        
        tier = user_info.get("tier", 0)
        solved = user_info.get("solvedCount", 0)
        
        await msg.edit(
            content=(
                f"✅ **{ctx.author.display_name}** 님 등록 완료!\n"
                f"핸들: `{handle}` | 티어: {tier} | 풀이 수: {solved}문제\n"
                f"⏳ 풀이 기록 동기화 중..."
            )
        )
        
        # 풀이 기록 동기화
        new_count = await sync_solved_problems(str(ctx.author.id), handle)
        await msg.edit(
            content=(
                f"✅ **{ctx.author.display_name}** 님 등록 완료!\n"
                f"핸들: `{handle}` | 티어: {tier} | 풀이 수: {solved}문제\n"
                f"📥 풀이 기록 동기화 완료 ({new_count}문제 불러옴)"
            )
        )


async def setup(bot):
    await bot.add_cog(Register(bot))