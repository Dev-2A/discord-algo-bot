# 🤖 discord-algo-bot

> Solved.ac 연동 Discord 알고리즘 스터디 봇

약점 태그 기반 문제 추천, 풀이 기록, 주간 랭킹 자동 공지를 지원하는 스터디 봇입니다.
[Solved.ac 라이벌 트래커](https://github.com/Dev-2A/solvedac-rival-tracker)와 연동되는 생태계의 일부입니다.

---

## ✨ 주요 기능

| 명령어 | 설명 |
| --- | --- |
| `!등록 [핸들]` | Solved.ac 핸들 등록 + 풀이 기록 자동 동기화 |
| `!오늘문제` | 약점 태그 기반 맞춤 문제 추천 |
| `!완료 [문제번호]` | 풀이 완료 기록 + 태그 통계 갱신 |
| `!기록 [개수]` | 최근 풀이 기록 조회 |
| `!약점` | 내 약점 태그 통계 조회 |
| `!동기화` | Solved.ac 풀이 기록 최신화 |
| `!프로필 [@멘션]` | 본인 또는 상대방 프로필 조회 |
| `!라이벌 [@멘션]` | 1:1 통계 비교 (티어 / 풀이 수 / 이번 주) |
| `!랭킹` | 이번 주 풀이 수 랭킹 조회 |
| `!서버현황` | 스터디 그룹 전체 통계 |
| `!랭킹공지` | 주간 랭킹 수동 공지 (관리자 전용) |
| `!help` | 명령어 목록 |

> 📢 매주 **월요일 오전 9시**에 주간 랭킹이 지정 채널에 자동 공지됩니다.

---

## 🛠️ 기술 스택

- **Python** 3.11+
- **discord.py** 2.3.2
- **aiohttp** — Solved.ac API 비동기 호출
- **SQLite** — 사용자 / 풀이 기록 / 태그 통계 저장
- **APScheduler** — 주간 랭킹 자동 공지

---

## 📁 프로젝트 구조

```text
discord-algo-bot/
├── bot/
│   ├── cogs/
│   │   ├── help_cog.py     # !help
│   │   ├── register.py     # !등록
│   │   ├── recommend.py    # !오늘문제, !약점, !동기화
│   │   ├── record.py       # !완료, !기록, !프로필
│   │   ├── scheduler.py    # 주간 랭킹 자동 공지
│   │   └── rival.py        # !라이벌, !서버현황
│   ├── db/
│   │   ├── database.py     # DB 초기화
│   │   ├── user_repo.py    # 사용자 CRUD
│   │   ├── record_repo.py  # 풀이 기록 CRUD
│   │   └── tag_repo.py     # 태그 통계 CRUD
│   ├── solvedac/
│   │   ├── client.py       # Solved.ac API 클라이언트
│   │   └── parser.py       # 문제 파싱 유틸
│   └── utils/
│       ├── weakness_analyzer.py  # 약점 태그 분석
│       ├── recommender.py        # 문제 추천 엔진
│       ├── ranking.py            # 주간 랭킹 계산
│       ├── rival.py              # 라이벌 비교
│       └── error_handler.py      # 공통 에러 핸들러
├── data/                   # SQLite DB (Git 미포함)
├── .env.example
├── config.py
├── main.py
└── requirements.txt
```

---

## 🚀 시작하기

### 1. 레포지토리 클론

```cmd
git clone https://github.com/Dev-2A/discord-algo-bot.git
cd discord-algo-bot
```

### 2. 가상환경 생성 + 패키지 설치

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경변수 설정

```cmd
copy .env.example .env
```

`.env` 파일을 열어서 아래 값을 입력:

```env
DISCORD_TOKEN=your_discord_bot_token_here
RANKING_CHANNEL_ID=your_channel_id_here
SOLVED_HANDLES=tangi826,handle2
```

### 4. 봇 실행

```cmd
python main.py
```

---

## 🔗 Discord 봇 설정

1. [Discord Developer Portal](https://discord.com/developers/applications) 에서 애플리케이션 생성
2. Bot 탭 → Token 복사 → `.env`의 `DISCORD_TOKEN`에 입력
3. OAuth2 → URL Generator → `bot` 스코프 선택
4. Bot Permissions: `Send Messages`, `Embed Links`, `Read Message History`, `View Channels`
5. 생성된 URL로 테스트 서버에 초대

---

## 🔗 연관 프로젝트

- [solvedac-rival-tracker](https://github.com/Dev-2A/solvedac-rival-tracker) — Solved.ac 라이벌 통계 대시보드

---

## 📄 라이선스

MIT © [Dev-2A](https://github.com/Dev-2A)
