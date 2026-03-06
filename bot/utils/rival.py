from bot.db import user_repo, record_repo, tag_repo
from bot.solvedac.client import get_user_info
from bot.solvedac.parser import get_tier_name, get_tag_ko


async def get_rival_comparison(discord_id_a: str, discord_id_b: str) -> dict | None:
    """
    두 사용자의 통계를 비교해서 반환.
    Solved.ac 라이벌 트래커 프로젝트와 동일한 데이터 구조 사용.
    """
    user_a = user_repo.get_user(discord_id_a)
    user_b = user_repo.get_user(discord_id_b)
    
    if not user_a or not user_b:
        return None
    
    # Solved.ac 실시간 정보 조회
    info_a = await get_user_info(user_a["handle"])
    info_b = await get_user_info(user_b["handle"])
    
    if not info_a or info_b:
        return None
    
    # 이번 주 풀이 수
    weekly = record_repo.get_weekly_solve_counts()
    weekly_map = {r["dicsord_id"]: r["count"] for r in weekly}
    
    # 약점 태그
    weak_a = tag_repo.get_weak_tags(discord_id_a, limit=3)
    weak_b = tag_repo.get_weak_tags(discord_id_b, limit=3)
    
    return {
        "a": {
            "handle": user_a["handle"],
            "tier": info_a.get("tier", 0),
            "tier_name": get_tier_name(info_a.get("tier", 0)),
            "solved_count": info_a.get("solvedCount", 0),
            "rating": info_a.get("rating", 0),
            "weekly_count": weekly_map.get(discord_id_a, 0),
            "weak_tags": [get_tag_ko(t["tag"]) for t in weak_a],
        },
        "b": {
            "handle": user_b["handle"],
            "tier": info_b.get("tier", 0),
            "tier_name": get_tier_name(info_b.get("tier", 0)),
            "solved_count": info_b.get("solvedCount", 0),
            "rating": info_b.get("rating", 0),
            "weekly_count": weekly_map.get(discord_id_b, 0),
            "weak_tags": [get_tag_ko(t["tag"]) for t in weak_b],
        },
    }


def build_vs_bar(val_a: int, val_b: int, width: int = 10) -> tuple[str, str]:
    """두 값을 비율 막대로 변환"""
    total = val_a + val_b
    if total == 0:
        bar_a = "─" * width
        bar_b = "─" * width
    else:
        filled_a = round(val_a / total * width)
        filled_b = width - filled_a
        bar_a = "█" * filled_a + "░" * (width - filled_a)
        bar_b = "░" * (width - filled_b) + "█" * filled_b
    return bar_a, bar_b