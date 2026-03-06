import json
from bot.db.database import get_connection


def add_solve_record(discord_id: str, problem_id: int,
                     title: str, level: int, tags: list[str]) -> bool:
    """풀이 기록 추가. 이미 기록된 문제면 False"""
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO solve_records
               (discord_id, problem_id, title, level, tags)
               VALUES (?, ?, ?, ?, ?)""",
            (discord_id, problem_id, title, level, json.dumps(tags, ensure_ascii=False))
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_user_records(discord_id: str) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM solve_records WHERE discord_id = ? ORDER BY solved_at DESC",
        (discord_id,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["tags"] = json.loads(d["tags"]) if d["tags"] else []
        result.append(d)
    return result


def is_already_solved(discord_id: str, problem_id: int) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM solve_records WHERE discord_id = ? AND problem_id = ?",
        (discord_id, problem_id)
    ).fetchone()
    conn.close()
    return row is not None


def get_weekly_solve_counts() -> list[dict]:
    """이번 주 풀이 수 집계 (주간 랭킹용)"""
    conn = get_connection()
    rows = conn.execute("""
        SELECT discord_id, COUNT(*) as count
        FROM solve_records
        WHERE solved_at >= datetime('now', 'localtime', '-7 days')
        GROUP BY discord_id
        ORDER BY count DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]