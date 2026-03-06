import discord
from discord.ext import commands


async def handle_error(ctx, error):
    """공통 에러 핸들러"""
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"❌ 필수 인자가 빠졌어!\n"
            f"`!help {ctx.command.name}` 으로 사용법을 확인해봐."
        )
    
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            f"❌ 잘못된 형식이야!\n"
            f"숫자가 필요한 곳에 문자를 입력하진 않았는지 확인해봐."
        )
    
    elif isinstance(error, commands.CommandNotFound):
        pass    # 없는 명령어는 무시
    
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ 이 명령어는 관리자만 사용할 수 있어!")
    
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ 너무 빠르게 호출했어! "
            f"{error.retry_after:.1f}초 후에 다시 시도해줘."
        )
    
    else:
        print(f"[ERROR] {ctx.command} 실행 중 오류: {error}")
        await ctx.send(
            "⚠️ 알 수 없는 오류가 발생했어. 잠시 후 다시 시도해줘!"
        )