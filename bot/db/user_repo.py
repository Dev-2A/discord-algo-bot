from bot.db.database import get_connection


def register_user(discord_id: str, handle: str) -> bool:
    """사용자 등록. 성공 시 True, 이미 존재 시 False"""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (discord_id, handle) VALUES (?, ?)",
            (discord_id, handle)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_user(discord_id: str) -> dict | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE discord_id = ?", (discord_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]