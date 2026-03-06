import aiohttp

BASE_URL = "https://solved.ac/api/v3"


async def get_user_info(handle: str) -> dict | None:
    """사용자 정보 조회"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/user/show",
                               params={"handle": handle}) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def get_user_solved_problems(handle: str, page: int = 1) -> dict | None:
    """사용자가 푼 문제 목록 조회"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/search/problem",
                               params={
                                   "query": f"solved_by:{handle}",
                                   "sort": "solved",
                                   "direction": "desc",
                                   "page": page
                               }) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def get_problem_info(problem_id: int) -> dict | None:
    """특정 문제 정보 조회"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/problem/show",
                               params={"problemId": problem_id}) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def search_problems_by_tag(tag: str, min_level: int = 1,
                                 max_level: int = 30,
                                 page: int = 1) -> dict | None:
    """태그 + 난이도 범위로 문제 검색"""
    query = f"tag:{tag} tier:{min_level}..{max_level}"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/search/problem",
                               params={
                                   "query": query,
                                   "sort": "random",
                                   "page": page
                               }) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def get_user_level(handle: str) -> int:
    """사용자의 현재 티어 반환 (없으면 1)"""
    info = await get_user_info(handle)
    if info:
        return info.get("tier", 1)
    return 1