# app.py
import time
import textwrap
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# 기본 설정
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MBTI 맞춤 공부 플래너",
    page_icon="🧠",
    layout="wide"
)

# ──────────────────────────────────────────────────────────────────────────────
# 스타일(CSS) – 부드러운 그라데이션, 카드, 귀여운 애니메이션
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* 전체 배경 그라데이션 애니메이션 */
.stApp {
  background: linear-gradient(120deg,#F8FBFF,#F7F0FF,#F0FFF9,#FFF8F0);
  background-size: 400% 400%;
  animation: gradient 25s ease infinite;
}
@keyframes gradient {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}

/* 카드 스타일 */
.card {
  background: rgba(255,255,255,0.62);
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.06);
  backdrop-filter: blur(6px);
}

/* 섹션 타이틀 */
.h2 {
  font-weight: 800;
  font-size: 1.35rem;
  margin: 0 0 8px 0;
}

/* 작은 칩(라벨) */
.chip {
  display:inline-block;
  padding: 6px 10px;
  font-size: 0.85rem;
  border-radius: 999px;
  background: linear-gradient(90deg,#FFE3F3,#E6F0FF);
  border: 1px solid rgba(0,0,0,0.06);
  margin-right: 8px;
}

/* 떠다니는 이모지 */
.float-emoji {
  position: relative;
  display: inline-block;
  animation: floaty 5s ease-in-out infinite;
}
@keyframes floaty {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-6px) rotate(2deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}

/* 강조 박스 */
.highlight {
  background: linear-gradient(90deg,#fffef5,#f4fff5);
  border: 1px dashed rgba(0,0,0,0.15);
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 0.98rem;
}

/* 마크다운 목록 간격 조정 */
.block-container ul, .block-container ol {
  margin-top: 0.3rem;
}

.small-muted { color:#666; font-size:0.86rem; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# 데이터 & 로직
# ──────────────────────────────────────────────────────────────────────────────

MBTI_TYPES = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ",
]

NICKNAMES = {
    "ISTJ": "체계와 근성의 정석가 🧱",
    "ISFJ": "다정한 수호자, 성실한 기록러 🫶",
    "INFJ": "통찰의 멘토, 의미 탐구자 🔮",
    "INTJ": "전략의 설계자, 효율 장인 🧩",
    "ISTP": "냉정한 해결사, 실전 러버 🛠️",
    "ISFP": "섬세한 감각러, 감성 몰입가 🎨",
    "INFP": "가치 중심 꿈꾸는 학습자 🌱",
    "INTP": "논리 탐험가, 개념 수집가 🧠",
    "ESTP": "액션 퍼포머, 즉흥 실습왕 🏃",
    "ESFP": "에너지 메이커, 즐거움 큐레이터 🎉",
    "ENFP": "아이디어 폭죽, 연결의 마법사 ✨",
    "ENTP": "도전적 발명가, 토론 스페셜리스트 ⚡",
    "ESTJ": "실행 드라이버, 마감 지배자 📅",
    "ESFJ": "케어 리더, 팀 분위기 메이커 🤝",
    "ENFJ": "코치형 리더, 동기 부여가 🧭",
    "ENTJ": "전략 리더, 목표 달성 매니저 🚀",
}

def parse_mbti(mbti: str):
    mbti = mbti.upper()
    I_E, N_S, T_F, J_P = mbti[0], mbti[1], mbti[2], mbti[3]
    return I_E, N_S, T_F, J_P

def unique(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

LETTER_STRATEGIES = {
    "I": [
        "방해 없는 **깊은 몰입 블록(45–90분)**으로 핵심 단원 정복 🧘‍♂️",
        "세션 종료마다 **회고 노트**로 배운 3가지를 적기 ✍️",
        "핸드폰·알림 **완전 차단**하고 한 번에 하나만 집중 🔕",
    ],
    "E": [
        "**Teach-back(10분)**: 방금 배운 것을 친구/가상 청중에게 설명 🗣️",
        "20–30분 **스프린트 → 5분 몸 스트레칭** 리듬 유지 🏃",
        "주 1–2회 **그룹 스터디**로 책임감과 재미 업 🤝",
    ],
    "N": [
        "**마인드맵/개념 지도**로 큰 그림부터 연결 🗺️",
        "핵심 법칙을 **비유·스토리**로 재해석해 기억 강화 📖",
        "단원 시작 전 **개요→핵심 질문 3개** 세우기 ❓",
    ],
    "S": [
        "**예제→유사문제 세트**로 손에 익히기 🧩",
        "절차·공식은 **체크리스트**로 안정적으로 반복 ✅",
        "중요 표/그림은 **빈칸 채우기**로 암기 완성 🧾",
    ],
    "T": [
        "틀릴 때마다 **오류 로그** 작성(원인→교정→재테스트) 🪵",
        "개념 구조를 **로직 트리**로 정리 🌳",
        "진도·정답률을 **수치화**해 개선 추적 📊",
    ],
    "F": [
        "개념을 **사람/상황 스토리**에 얹어 의미 찾기 💞",
        "**공개 약속·동반 학습**으로 지속 동기 만들기 🤗",
        "자기 친절 루틴: 세션 후 **칭찬 한 줄** 남기기 🌷",
    ],
    "J": [
        "**시간 블록** 미리 예약(시작·끝·휴식 명확히) ⏱️",
        "각 과제의 **완료 정의(DoD)**를 문장으로 명확화 📝",
        "매 세션 **첫 5분 워밍업**(목표 재확인·환경 정돈) 🧹",
    ],
    "P": [
        "**타임박싱**으로 가볍게 시작(25/5 또는 15/3) 🧩",
        "**Hard-start, easy-finish**: 어려운 것 5분만 손대기 ⏳",
        "지루해지면 **테마 전환**(읽기→문제→요약→가르치기) 🔄",
    ],
}

LETTER_ENV = {
    "I": ["조용한 공간, 노이즈캔슬링, 집중 조명 💡"],
    "E": ["밝은 공간, **카페 사운드/백색소음**로 에너지 유지 ☕"],
    "N": ["화이트보드/태블릿으로 **그림·개념도** 확장 🖊️"],
    "S": ["책상 위 **교재·문제·메모**만 두는 미니멀 셋업 📚"],
    "T": ["**2모니터**(자료/작업 분리), 단축키 최적화 ⌨️"],
    "F": ["아늑한 조명·식물·향기 등 감성 셋업 🌿"],
    "J": ["정리된 책상, 파일/노트 체계적 분류 🗂️"],
    "P": ["**스탠딩/좌식** 전환, 포스트잇으로 즉흥 아이디어 ✨"],
}

LETTER_TOOLS = {
    "I": ["Forest/Focus To-Do(방해 차단) 🌲"],
    "E": ["StudyTogether/Discord(공유), Loom(teach-back) 🎥"],
    "N": ["Obsidian/Notion(연결 노트), Excalidraw(마인드맵) 🗺️"],
    "S": ["Anki/Quizlet(반복 암기), GoodNotes/OneNote 📒"],
    "T": ["Google Sheets/Excel(지표), Mermaid/Draw.io(로직) 📊"],
    "F": ["Habitica(게임화), Daylio/잠깐일기(감정 트래킹) 💖"],
    "J": ["Google Calendar/TickTick(타임블록) 📅"],
    "P": ["Trello/Todoist(칸반), Random Picker(랜덤 전환) 🎲"],
}

LETTER_PITFALLS = {
    "I": ["과도한 고립, 완벽주의로 진도 지연 ❄️"],
    "E": ["잡담/회의 과다로 깊은 몰입 부족 🔊"],
    "N": ["추상에 치우쳐 연습량 부족 ☁️"],
    "S": ["맥락 없는 암기로 이해 얕아짐 🧱"],
    "T": ["과도한 최적화·휴식 무시 🧨"],
    "F": ["기분 의존·질문 회피로 막힘 지속 😶"],
    "J": ["유연성 부족, 계획 과잉으로 소진 📐"],
    "P": ["시작 지연·마감 압박 🌀"],
}

LETTER_MOTIVATORS = {
    "I": ["진전 시각화(체크/그래프), 혼자만의 보상 🎁"],
    "E": ["공개 약속·짝 스터디·경쟁 요소 🏆"],
    "N": ["새로운 아이디어·실험 과제 🔬"],
    "S": ["체크리스트 완료감·눈에 보이는 성과 ✅"],
    "T": ["점수·정답률 향상, 기록 성장 📈"],
    "F": ["의미/도움의 가치, 따뜻한 피드백 💌"],
    "J": ["계획 달성의 쾌감·연속성 유지 🔗"],
    "P": ["새로움·자율성·선택권 🎯"],
}

def build_routine(hours: int, j_or_p: str):
    mins = int(hours * 60)
    # 소프트 기본: 25/5 또는 50/10 구성
    if mins <= 120:
        cycle = "25분 집중 → 5분 휴식"
        unit = 30
    elif mins <= 240:
        cycle = "50분 집중 → 10분 휴식"
        unit = 60
    else:
        cycle = "50분 집중 → 10분 휴식(4회) + 20분 롱브레이크"
        unit = 60

    blocks = max(1, mins // unit)
    if j_or_p == "J":
        headline = f"⏱️ 타임블록 루틴 ({hours}시간 / {blocks}블록)"
        steps = [
            "워밍업 5분: 오늘 목표 3줄·환경 정돈",
            f"{cycle} × {blocks} 블록",
            "마무리 10분: 회고 노트(배운 3가지·오류·다음 행동 1개)"
        ]
    else:
        headline = f"🎲 타임박싱 루틴 ({hours}시간 / {blocks}스프린트)"
        steps = [
            "랜덤 스타트 2분: 오늘 당기는 과제 바로 시작",
            f"{cycle} × {blocks} 스프린트 (지루해지면 테마 전환)",
            "마무리 5분: 성과 체크✔ / 내일 첫 한 걸음 한 줄"
        ]
    return headline, steps

def generate_plan(mbti: str, hours: int, mood: str):
    I_E, N_S, T_F, J_P = parse_mbti(mbti)

    strategies = unique(
        LETTER_STRATEGIES[I_E] +
        LETTER_STRATEGIES[N_S] +
        LETTER_STRATEGIES[T_F] +
        LETTER_STRATEGIES[J_P]
    )
    env = unique(
        LETTER_ENV[I_E] + LETTER_ENV[N_S] + LETTER_ENV[T_F] + LETTER_ENV[J_P]
    )
    tools = unique(
        LETTER_TOOLS[I_E] + LETTER_TOOLS[N_S] + LETTER_TOOLS[T_F] + LETTER_TOOLS[J_P]
    )
    pitfalls = unique(
        LETTER_PITFALLS[I_E] + LETTER_PITFALLS[N_S] + LETTER_PITFALLS[T_F] + LETTER_PITFALLS[J_P]
    )
    motivators = unique(
        LETTER_MOTIVATORS[I_E] + LETTER_MOTIVATORS[N_S] + LETTER_MOTIVATORS[T_F] + LETTER_MOTIVATORS[J_P]
    )
    routine_head, routine_steps = build_routine(hours, J_P)

    mood_tip = {
        "😎 의욕충만": "과감히 **어려운 과제부터 20분 돌파**해 탄력 받자!",
        "😵‍💫 피곤": "**15/3 미니 사이클**로 짧게 쪼개고, **물·스트레칭** 추가!",
        "😐 보통": "**50/10 안정 루틴**으로 꾸준히 전진하자.",
        "😥 불안": "**오류 로그로 가시화**하고, **쉬운 승리 1개** 먼저 쌓자."
    }.get(mood, "첫 5분은 환경 정돈·목표 쓰기로 시동을 걸자!")

    return {
        "nickname": NICKNAMES[mbti],
        "strategies": strategies,
        "environment": env,
        "tools": tools,
        "pitfalls": pitfalls,
        "motivators": motivators,
        "routine_head": routine_head,
        "routine_steps": routine_steps,
        "mood_tip": mood_tip
    }

def as_download_text(mbti, hours, plan):
    lines = []
    lines.append(f"[MBTI 맞춤 공부 플래너] {mbti} · {NICKNAMES[mbti]}")
    lines.append(f"- 목표 공부 시간: {hours}시간")
    lines.append("")
    lines.append("■ 핵심 전략")
    for s in plan["strategies"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("■ 추천 루틴")
    lines.append(f"- {plan['routine_head']}")
    for s in plan["routine_steps"]:
        lines.append(f"  • {s}")
    lines.append("")
    lines.append("■ 공부 환경")
    for s in plan["environment"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("■ 추천 도구")
    for s in plan["tools"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("■ 주의/보완")
    for s in plan["pitfalls"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("■ 동기 트리거")
    for s in plan["motivators"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append(f"■ 오늘의 가속 팁: {plan['mood_tip']}")
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────────────────────
# UI – 헤더
# ──────────────────────────────────────────────────────────────────────────────
left, right = st.columns([0.72, 0.28])
with left:
    st.markdown(
        "<div class='float-emoji' style='font-size:2.2rem'>📚✨</div> "
        "<span style='font-size:2.0rem; font-weight:800'>MBTI 맞춤 공부 플래너</span> "
        "<span class='float-emoji' style='font-size:2.2rem'>🧠⚡</span>",
        unsafe_allow_html=True
    )
    st.caption("내 성향에 딱 맞는 공부법을 레시피처럼 추천해 드려요. 이모지 가득, 효과 가득!")

with right:
    st.markdown("<span class='chip'>Pomodoro</span> <span class='chip'>Teach‑back</span> <span class='chip'>Mind‑map</span>", unsafe_allow_html=True)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# 사이드바 – 입력
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 설정")
    sel = st.selectbox("MBTI 선택", MBTI_TYPES, index=10)  # ENFP default for fun
    hours = st.slider("오늘 목표 공부 시간", 1, 8, 3)
    mood = st.selectbox("지금 기분 상태", ["😎 의욕충만", "😐 보통", "😵‍💫 피곤", "😥 불안"])
    st.markdown("---")
    go = st.button("플랜 만들기 🚀", use_container_width=True)
    st.caption("버튼을 누르면 맞춤 전략을 조합하고 풍선🎈이 날아가요!")

# ──────────────────────────────────────────────────────────────────────────────
# 본문 – 결과/카드
# ──────────────────────────────────────────────────────────────────────────────
placeholder = st.empty()

if not go:
    with placeholder.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='card'><div class='h2'>1) MBTI 선택</div><div>성향을 기준으로 공부법을 조합해요.</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'><div class='h2'>2) 시간/기분 설정</div><div>루틴·팁이 함께 맞춰져요.</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='card'><div class='h2'>3) 플랜 만들기</div><div>전략·도구·환경까지 한 번에!</div></div>", unsafe_allow_html=True)
        st.info("👈 왼쪽에서 MBTI와 시간을 고르고 **플랜 만들기 🚀**를 눌러주세요!")
else:
    with st.spinner("당신의 학습 DNA를 분석하는 중… 🧬"):
        # Progress 애니메이션
        prog = st.progress(0, text="맞춤 전략 조합 중…")
        for i in range(0, 101, 7):
            time.sleep(0.03)
            prog.progress(min(i, 100))
        prog.empty()

        plan = generate_plan(sel, hours, mood)

    st.balloons()
    if hasattr(st, "toast"):
        st.toast(f"{sel} · {plan['nickname']} — 맞춤 플랜 준비 완료!", icon="🎉")

    # 헤더 카드
    st.markdown(f"""
    <div class='card'>
      <div class='h2'>🎯 {sel} · {plan[nickname_key] if (nickname_key:='nickname') else NICKNAMES.get(sel,'')}</div>
      <div class='highlight'>오늘의 가속 팁: <b>{plan['mood_tip']}</b></div>
      <div class='small-muted' style='margin-top:6px'>* 성향 조합 기반 제안이므로, 본인에게 맞게 커스터마이징하세요.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # 탭 구성
    t1, t2, t3, t4, t5 = st.tabs(["🧩 핵심 전략", "⏱ 루틴", "🧪 환경·도구", "⚠️ 주의/보완", "🏅 미니 챌린지"])

    with t1:
        left, right = st.columns([0.64, 0.36])
        with left:
            st.markdown("<div class='h2'>Top 전략</div>", unsafe_allow_html=True)
            for s in plan["strategies"]:
                st.markdown(f"- {s}")
        with right:
            st.markdown("<div class='h2'>동기 트리거</div>", unsafe_allow_html=True)
            st.markdown("\n".join([f"- {m}" for m in plan["motivators"]]))

    with t2:
        st.markdown(f"#### {plan['routine_head']}")
        st.markdown("\n".join([f"- {s}" for s in plan["routine_steps"]]))
        with st.expander("⏳ 팁: 휴식 5–10분은 이렇게!"):
            st.markdown("- **눈·목 스트레칭** / **물 마시기** / **가벼운 산책** / **심호흡 1분** / 휴대폰은 보지 않기!")

    with t3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='h2'>공부 환경</div>", unsafe_allow_html=True)
            st.markdown("\n".join([f"- {e}" for e in plan["environment"]]))
        with c2:
            st.markdown("<div class='h2'>추천 도구</div>", unsafe_allow_html=True)
            st.markdown("\n".join([f"- {tool}" for tool in plan["tools"]]))

    with t4:
        st.warning("다음 함정에 빠지지 않도록 체크해요:")
        st.markdown("\n".join([f"- {p}" for p in plan["pitfalls"]]))

    with t5:
        # 성향 기반 미니 챌린지 3가지 구성
        challenges_pool = [
            "오늘 배운 핵심을 **10문장→3문장→1문장**으로 줄여보기 ✂️",
            "**Teach‑back 5분**: 목소리 메모로 설명 녹음 후 들어보기 🎙️",
            "**오류 로그**에 오늘의 실수 3개를 원인·교정과 함께 기록 🪵",
            "**마인드맵**으로 단원 전체를 10분 안에 다시 그리기 🗺️",
            "**Flashcard 20장** 스피드런: 헷갈리는 카드만 별표 ⭐",
            "**타임박싱 25/5 x 2** — 지루해지면 과제 테마 전환 🔄",
        ]
        # 조금 랜덤성: MBTI별 특정 항목 우선 노출
        I_E, N_S, T_F, J_P = parse_mbti(sel)
        picks = []
        if I_E == "E":
            picks += ["Teach‑back 5분", "타임박싱 25/5 x 2"]
        if N_S == "N":
            picks += ["마인드맵으로 단원 전체를 10분 안에 다시 그리기"]
        if T_F == "T":
            picks += ["오류 로그에 오늘의 실수 3개를 원인·교정과 함께 기록"]
        if J_P == "P":
            picks += ["타임박싱 25/5 x 2"]
        # 고정 텍스트와 풀을 합쳐 상위 3개만
        pretty = []
        for p in picks + challenges_pool:
            # 중복 제거
            title = p.replace("**","").replace("—","-")
            if title not in [x.replace("**","").replace("—","-") for x in pretty]:
                pretty.append(p)
            if len(pretty) >= 3:
                break
        st.markdown("\n".join([f"- {c}" for c in pretty[:3]]))

    # 다운로드
    txt = as_download_text(sel, hours, plan)
    st.download_button(
        "📥 내 플랜 .txt로 저장",
       
