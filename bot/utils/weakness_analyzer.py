from bot.db import tag_repo, record_repo
from bot.solvedac.client import get_user_solved_problems
from bot.solvedac.parser import parse_problem


async def sync_solved_problems(discord_id: str, handle: str) -> int:
    """
    Solved.ac에서 최근 푼 문제를 가져와 DB에 동기화.
    새로 추가된 문제 수를 반환.
    """
    new_count = 0
    page = 1
    
    while True:
        data = await get_user_solved_problems(handle, page=page)
        if not data or not data.get("items"):
            break
        
        for raw in data["items"]:
            problem = parse_problem(raw)
            
            # 이미 기록된 문제면 스킵
            if record_repo.is_already_solved(discord_id, problem["problem_id"]):
                continue
            
            # 풀이 기록 저장
            added = record_repo.add_solve_record(
                discord_id=discord_id,
                problem_id=problem["problem_id"],
                title=problem["title"],
                level=problem["level"],
                tags=problem["tags"],
            )
            
            if added:
                # 태그 통계 갱신
                for tag in problem["tags"]:
                    tag_repo.upsert_tag_stat(discord_id, tag)
                new_count += 1
        
        # 마지막 페이지면 종료
        total = data.get("count", 0)
        if page * 50 >= total:
            break
        page += 1
    
    return new_count


def get_weak_tags(discord_id: str, limit: int = 3) -> list[dict]:
    """
    약점 태그 반환.
    태그 통계가 없으면 기본 태그 목록 반환.
    """
    tags = tag_repo.get_weak_tags(discord_id, limit=limit)
    
    if not tags:
        # 통계 데이터 없을 때 기본 약점 태그
        default_tags = ["dp", "graphs", "greedy", "math", "binary_search"]
        return [{"tag": t, "solve_count": 0} for t in default_tags[:limit]]
    
    return tags


def get_tag_summary(discord_id: str) -> str:
    """태그 통계 요약 문자열 생성"""
    from bot.solvedac.parser import get_tag_ko
    
    all_stats = tag_repo.get_all_tag_stats(discord_id)
    if not all_stats:
        return "아직 풀이 기록이 없어요."
    
    total_solved = sum(s["solve_count"] for s in all_stats)
    
    # 상위 5개 태그
    top5 = all_stats[:5]
    lines = [f"📊 **태그별 풀이 통계** (총 {total_solved}문제)\n"]
    for i, stat in enumerate(top5, 1):
        tag_ko = get_tag_ko(stat["tag"])
        bar = "█" * min(stat["solve_count"], 10)
        lines.append(f"`{i}. {tag_ko}` {bar} {stat['solve_count']}문제")
    
    # 하위 3개 (약점)
    weak = tag_repo.get_weak_tags(discord_id, limit=3)
    if weak:
        lines.append("\n⚠️ **약점 태그**")
        for stat in weak:
            tag_ko = get_tag_ko(stat["tag"])
            lines.append(f"  • {tag_ko} ({stat['solve_count']}문제)")
    
    return "\n".join(lines)