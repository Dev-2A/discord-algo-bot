from bot.db.database import get_connection


def upsert_tag_stat(discord_id: str, tag: str) :
    """태그 풀이 수 1 증가 (없으면 생성)"""
    conn = get_connection()
    conn.execute("""
        INSERT INTO tag_stats (discord_id, tag, solve_count)
        VALUES (?, ?, 1)
        ON CONFLICT (discord_id, tag)
        DO UPDATE SET
            solve_count = solve_count + 1,
            updated_at = datetime('now', 'localtime')
    """, (discord_id, tag))
    conn.commit()
    conn.close()


def get_weak_tags(discord_id: str, limit: int = 5) -> list[dict]:
    """풀이 수가 적은 약점 태그 반환"""
    conn = get_connection()
    rows = conn.execute("""
        SELECT tag, solve_count FROM tag_stats
        WHERE discord_id = ?
        ORDER BY solve_count ASC
        LIMIT ?
    """, (discord_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_tag_stats(discord_id: str) -> list[dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT tag, solve_count FROM tag_stats
        WHERE discord_id = ?
        ORDER BY solve_count DESC
    """, (discord_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]