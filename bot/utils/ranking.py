from bot.db import record_repo, user_repo
from bot.solvedac.parser import get_tag_ko


def get_weekly_ranking() -> list[dict]:
    """
    이번 주 풀이 수 기준 랭킹 반환.
    [{"discord_id": ..., "handle": ..., "count": ...}, ...]
    """
    counts = record_repo.get_weekly_solve_counts()
    users = {u["discord_id"]: u["handle"] for u in user_repo.get_all_users()}
    
    ranking = []
    for row in counts:
        discord_id = row["discord_id"]
        handle = users.get(discord_id, "알 수 없음")
        ranking.append({
            "discord_id": discord_id,
            "handle": handle,
            "count": row["count"],
        })
    
    return ranking


def build_ranking_message(ranking: list[dict]) -> str:
    """랭킹 임베드용 텍스트 생성"""
    if not ranking:
        return "이번 주 풀이 기록이 없어요 😢"
    
    medals = ["🥇", "🥈", "🥉"]
    lines = []
    
    for i, entry in enumerate(ranking):
        medal = medals[i] if i < 3 else f"`{i + 1}.`"
        lines.append(
            f"{medal} **{entry['handle']}** - {entry['count']}문제"
        )
    
    return "\n".join(lines)