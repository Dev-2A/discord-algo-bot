TIER_NAMES = {
    0: "Unrated",
    1: "브론즈 V", 2: "브론즈 IV", 3: "브론즈 III", 4: "브론즈 II", 5: "브론즈 I",
    6: "실버 V", 7: "실버 IV", 8: "실버 III", 9: "실버 II", 10: "실버 I",
    11: "골드 V", 12: "골드 IV", 13: "골드 III", 14: "골드 II", 15: "골드 I",
    16: "플래 V", 17: "플래 IV", 18: "플래 III", 19: "플래 II", 20: "플래 I",
    21: "다이아 V", 22: "다이아 IV", 23: "다이아 III", 24: "다이아 II", 25: "다이아 I",
    26: "루비 V", 27: "루비 IV", 28: "루비 III", 29: "루비 II", 30: "루비 I",
}

TAG_KO = {
    "dp": "다이나믹 프로그래밍",
    "graphs": "그래프",
    "greedy": "그리디",
    "implementation": "구현",
    "math": "수학",
    "data_structures": "자료구조",
    "string": "문자열",
    "bfs": "BFS",
    "dfs": "DFS",
    "binary_search": "이분탐색",
    "sorting": "정렬",
    "tree": "트리",
    "simulation": "시뮬레이션",
    "backtracking": "백트래킹",
    "two_pointer": "투 포인터",
}


def parse_problem(raw: dict) -> dict:
    """API 응답에서 필요한 필드만 추출"""
    tags = [t["key"] for t in raw.get("tags", [])]
    return {
        "problem_id": raw["problemId"],
        "title": raw["titleKo"],
        "level": raw["level"],
        "tier_name": TIER_NAMES.get(raw["level"], "Unrated"),
        "tags": tags,
        "accepted_user_count": raw.get("acceptedUserCount", 0),
        "url": f"https://www.acmicpc.net/problem/{raw['problemId']}",
    }


def get_tier_name(level: int) -> str:
    return TIER_NAMES.get(level, "Unrated")


def get_tag_ko(tag: str) -> str:
    return TAG_KO.get(tag, tag)


def get_recommend_level_range(user_tier: int) -> tuple[int, int]:
    """사용자 티어 기준 ±2 범위 반환"""
    min_level = max(1, user_tier - 2)
    max_level = min(30, user_tier + 2)
    return min_level, max_level