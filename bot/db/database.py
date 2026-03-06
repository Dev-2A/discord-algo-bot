import sqlite3
import os
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """DB 테이블 초기화 (최초 1회)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 사용자 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id  TEXT    NOT NULL UNIQUE,
            handle      TEXT    NOT NULL UNIQUE,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    
    # 풀이 기록 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solve_records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id  TEXT    NOT NULL,
            problem_id  INTEGER NOT NULL,
            title       TEXT,
            level       INTEGER,
            tags        TEXT,   -- JSON 배열로 저장 (예: '["dp","graph"]')
            solved_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            UNIQUE (discord_id, problem_id)
        )
    """)

    # 약점 태그 통계 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_stats (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id  TEXT    NOT NULL,
            tag         TEXT    NOT NULL,
            solve_count INTEGER NOT NULL DEFAULT 0,
            updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            UNIQUE (discord_id, tag)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ DB 초기화 완료")