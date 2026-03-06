import random
from bot.solvedac.client import search_problems_by_tag, get_user_level
from bot.solvedac.parser import parse_problem, get_recommend_level_range
from bot.db import record_repo
from bot.utils.weakness_analyzer import get_weak_tags


async def recommend_problem(discord_id: str, handle: str) -> dict | None:
    """
    약점 태그 기반 문제 추천.
    이미 푼 문제는 제외하고 반환.
    """
    # 1. 사용자 티어 조회
    user_tier = await get_user_level(handle)
    min_level, max_level = get_recommend_level_range(user_tier)
    
    # 2. 약점 태그 목록 가져오기 (최대 3개)
    weak_tags = get_weak_tags(discord_id, limit=3)
    if not weak_tags:
        return None
    
    # 3. 약점 태그 중 랜덤 선택
    random.shuffle(weak_tags)
    
    for tag_info in weak_tags:
        tag = tag_info["tag"]
        
        # 4. 해당 태그 + 난이도 범위로 문제 검색
        data = await search_problems_by_tag(tag, min_level, max_level)
        if not data or not data.get("items"):
            continue
        
        # 5. 이미 푼 문제 제외
        solved_ids = {
            r["problem_id"] for r in record_repo.get_user_records(discord_id)
        }
        candidates = [
            parse_problem(p) for p in data["items"]
            if p["problemId"] not in solved_ids
        ]
        
        if candidates:
            chosen = random.choice(candidates)
            chosen["recommended_tag"] = tag
            return chosen
    
    return None