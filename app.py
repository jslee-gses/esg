import os
from typing import Dict, List

import pandas as pd
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="ESG Mate AI",
    page_icon="🌱",
    layout="wide",
)

ESG_KNOWLEDGE = """
ESG는 환경(Environment), 사회(Social), 지배구조(Governance)를 뜻한다.
환경에는 온실가스 감축, 에너지 절약, 폐기물 관리, 자원순환 등이 포함된다.
사회에는 근로자 안전, 인권, 다양성, 지역사회 기여, 개인정보 보호 등이 포함된다.
지배구조에는 윤리경영, 이사회 운영, 내부통제, 정보공개 등이 포함된다.
탄소중립은 배출한 온실가스와 흡수·제거한 온실가스의 순배출량을 0으로 만드는 것이다.
RE100은 기업이 사용하는 전력의 100%를 재생에너지로 조달하겠다는 국제 캠페인이다.
ISSB는 국제지속가능성기준위원회이며 지속가능성 관련 재무정보 공시기준을 개발한다.
KSSB는 한국의 지속가능성 공시기준 체계를 가리키는 표현으로 사용된다.
""".strip()

QUESTIONS: List[Dict[str, str]] = [
    {"category": "E", "text": "에너지 사용량을 정기적으로 기록하고 있나요?"},
    {"category": "E", "text": "분리배출과 폐기물 감축 활동을 하고 있나요?"},
    {"category": "E", "text": "일회용품 사용을 줄이기 위한 규칙이 있나요?"},
    {"category": "E", "text": "친환경 제품이나 재생에너지를 우선적으로 사용하나요?"},
    {"category": "S", "text": "구성원의 안전과 건강을 위한 교육을 하고 있나요?"},
    {"category": "S", "text": "차별과 괴롭힘을 예방하는 규칙이 있나요?"},
    {"category": "S", "text": "지역사회 봉사나 기부 활동에 참여하나요?"},
    {"category": "S", "text": "개인정보를 안전하게 관리하고 있나요?"},
    {"category": "G", "text": "의사결정 과정과 책임자를 명확히 공개하나요?"},
    {"category": "G", "text": "부정행위와 이해충돌을 방지하는 규칙이 있나요?"},
    {"category": "G", "text": "예산과 활동 결과를 구성원에게 투명하게 공유하나요?"},
    {"category": "G", "text": "문제가 발생했을 때 신고하고 개선하는 절차가 있나요?"},
]

FALLBACK_ACTIONS = {
    "E": [
        "월별 전기·수도 사용량을 기록하고 전월과 비교하세요.",
        "일회용품 감축과 분리배출 규칙을 한 장짜리 안내문으로 만드세요.",
        "조명 끄기, 냉난방 적정온도 유지 등 실천 캠페인을 운영하세요.",
    ],
    "S": [
        "안전·인권·개인정보 보호 교육을 짧게라도 정기 운영하세요.",
        "구성원의 의견을 익명으로 받을 수 있는 설문 창구를 만드세요.",
        "지역사회 봉사활동을 학기별 1회 이상 기획하세요.",
    ],
    "G": [
        "주요 의사결정, 담당자, 일정, 결과를 표로 공개하세요.",
        "윤리규칙과 문제 신고 절차를 간단한 문서로 정리하세요.",
        "활동 예산과 성과를 정기적으로 공유하세요.",
    ],
}


def get_api_key() -> str:
    """Read the API key from Streamlit secrets first, then environment variables."""
    try:
        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        return os.getenv("OPENAI_API_KEY", "")


def get_model_name() -> str:
    try:
        return st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini")
    except Exception:
        return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def call_ai(system_prompt: str, user_prompt: str) -> str:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=get_model_name(),
        instructions=system_prompt,
        input=user_prompt,
    )
    return response.output_text.strip()


def classify_news(text: str) -> str:
    lowered = text.lower()
    e_words = ["탄소", "기후", "환경", "재생에너지", "폐기물", "온실가스", "energy", "climate"]
    s_words = ["인권", "노동", "안전", "지역사회", "다양성", "개인정보", "human rights", "safety"]
    g_words = ["이사회", "윤리", "지배구조", "공시", "감사", "내부통제", "governance", "board"]
    scores = {
        "환경(E)": sum(word in lowered for word in e_words),
        "사회(S)": sum(word in lowered for word in s_words),
        "지배구조(G)": sum(word in lowered for word in g_words),
    }
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "종합 ESG"


def fallback_summary(text: str) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    selected = sentences[:3]
    if not selected:
        return "요약할 뉴스 내용을 입력해 주세요."
    return "\n".join(f"- {sentence}." for sentence in selected)


def score_label(score: float) -> str:
    if score >= 80:
        return "우수"
    if score >= 60:
        return "보통"
    return "개선 필요"


st.title("🌱 ESG Mate AI")
st.caption("고등학생 특별활동을 위한 간단한 ESG 학습·진단 앱")

with st.sidebar:
    st.header("설정")
    if get_api_key():
        st.success("AI 기능 사용 가능")
        st.caption(f"모델: {get_model_name()}")
    else:
        st.warning("API 키 없음: 기본 기능으로 실행됩니다.")
        st.caption("Streamlit Secrets에 OPENAI_API_KEY를 추가하면 AI 기능이 활성화됩니다.")

    st.divider()
    st.markdown("**주의사항**")
    st.caption("이 앱의 결과는 학습용이며 기업의 공식 ESG 평가나 법률·회계 자문이 아닙니다.")

chat_tab, news_tab, diagnosis_tab, action_tab = st.tabs(
    ["💬 ESG 챗봇", "📰 뉴스 요약", "✅ ESG 자가진단", "💡 개선 제안"]
)

with chat_tab:
    st.subheader("ESG AI 챗봇")
    st.write("ESG 개념과 실천 방법을 질문해 보세요.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요. ESG에 대해 궁금한 점을 질문해 주세요."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("예: 탄소중립과 RE100의 차이는 무엇인가요?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                answer = call_ai(
                    "당신은 고등학생에게 ESG를 설명하는 친절한 교사입니다. "
                    "답변은 정확하고 쉬운 한국어로 5문장 이내로 작성하세요. "
                    "확실하지 않은 내용은 단정하지 마세요. 다음 기초자료를 참고하세요:\n"
                    + ESG_KNOWLEDGE,
                    prompt,
                )
            except Exception:
                answer = (
                    "현재 AI API를 사용할 수 없어 기본 설명을 제공합니다.\n\n"
                    + ESG_KNOWLEDGE
                    + "\n\n질문과 관련된 핵심어를 위 설명에서 찾아보세요."
                )
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

with news_tab:
    st.subheader("ESG 뉴스 3줄 요약")
    st.write("뉴스 기사 제목과 본문을 붙여 넣으면 ESG 분야를 분류하고 핵심을 요약합니다.")

    news_title = st.text_input("뉴스 제목", placeholder="예: A기업, 2030년 재생에너지 사용 확대")
    news_body = st.text_area(
        "뉴스 본문",
        height=220,
        placeholder="기사 내용을 붙여 넣으세요. 개인정보나 유료 기사 전문은 입력하지 마세요.",
    )

    if st.button("뉴스 분석하기", type="primary"):
        combined = f"제목: {news_title}\n본문: {news_body}".strip()
        if not news_body.strip():
            st.warning("뉴스 본문을 입력해 주세요.")
        else:
            category = classify_news(combined)
            st.metric("분류 결과", category)
            try:
                summary = call_ai(
                    "당신은 ESG 뉴스 편집자입니다. 입력된 기사만 근거로 사용하세요. "
                    "1) 핵심 사실, 2) ESG 관점의 의미, 3) 기업 또는 시민이 주목할 점을 "
                    "각 한 줄씩 한국어로 작성하세요. 과장하거나 새로운 사실을 만들지 마세요.",
                    combined,
                )
            except Exception:
                summary = fallback_summary(news_body)
            st.markdown("### 3줄 요약")
            st.markdown(summary)

with diagnosis_tab:
    st.subheader("ESG 자가진단")
    st.write("학교, 동아리 또는 가상의 기업을 대상으로 각 문항에 답해 보세요.")

    org_name = st.text_input("진단 대상", value="우리 학교/동아리")
    answer_map = {"아니요": 0, "일부 실천": 1, "잘 실천": 2}
    responses = []

    with st.form("diagnosis_form"):
        for index, item in enumerate(QUESTIONS, start=1):
            response = st.radio(
                f"{index}. [{item['category']}] {item['text']}",
                options=list(answer_map.keys()),
                horizontal=True,
                key=f"q_{index}",
            )
            responses.append({**item, "answer": response, "value": answer_map[response]})

        submitted = st.form_submit_button("진단 결과 보기", type="primary")

    if submitted:
        df = pd.DataFrame(responses)
        category_scores = (
            df.groupby("category")["value"].sum()
            / df.groupby("category")["value"].count()
            / 2
            * 100
        ).round(1)
        total_score = round(df["value"].sum() / (len(df) * 2) * 100, 1)

        st.session_state["diagnosis"] = {
            "organization": org_name,
            "total_score": total_score,
            "category_scores": category_scores.to_dict(),
            "responses": responses,
        }

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("종합 점수", f"{total_score}점")
        col2.metric("환경(E)", f"{category_scores.get('E', 0)}점")
        col3.metric("사회(S)", f"{category_scores.get('S', 0)}점")
        col4.metric("지배구조(G)", f"{category_scores.get('G', 0)}점")

        chart_df = pd.DataFrame(
            {
                "영역": ["환경(E)", "사회(S)", "지배구조(G)"],
                "점수": [
                    category_scores.get("E", 0),
                    category_scores.get("S", 0),
                    category_scores.get("G", 0),
                ],
            }
        ).set_index("영역")
        st.bar_chart(chart_df)
        st.info(f"{org_name}의 진단 수준: **{score_label(total_score)}**")

with action_tab:
    st.subheader("맞춤형 ESG 개선 제안")
    diagnosis = st.session_state.get("diagnosis")

    if not diagnosis:
        st.info("먼저 'ESG 자가진단' 탭에서 진단을 완료해 주세요.")
    else:
        scores = diagnosis["category_scores"]
        weakest = min(scores, key=scores.get)
        category_name = {"E": "환경", "S": "사회", "G": "지배구조"}[weakest]

        st.write(f"진단 대상: **{diagnosis['organization']}**")
        st.write(f"우선 개선 영역: **{category_name}({weakest})** · {scores[weakest]}점")

        weak_items = [
            item["text"]
            for item in diagnosis["responses"]
            if item["category"] == weakest and item["value"] < 2
        ]

        if st.button("개선 계획 만들기", type="primary"):
            try:
                prompt = (
                    f"대상: {diagnosis['organization']}\n"
                    f"종합점수: {diagnosis['total_score']}\n"
                    f"영역별 점수: {scores}\n"
                    f"우선 개선영역: {category_name}\n"
                    f"미흡 문항: {weak_items}\n"
                    "예산이 적은 고등학생 특별활동 수준에서 2주 안에 실행할 수 있는 "
                    "개선 활동 3개를 제안하세요. 각 활동은 활동명, 실행방법, 확인지표를 포함하세요."
                )
                suggestions = call_ai(
                    "당신은 고등학생 ESG 프로젝트 지도교사입니다. "
                    "실행 가능하고 안전하며 비용이 거의 들지 않는 제안만 작성하세요.",
                    prompt,
                )
                st.markdown(suggestions)
            except Exception:
                st.markdown("### 추천 개선 활동")
                for index, action in enumerate(FALLBACK_ACTIONS[weakest], start=1):
                    st.markdown(f"**{index}. {action}**")
                st.caption("API 키를 설정하면 진단 결과에 맞춘 더 구체적인 제안을 받을 수 있습니다.")

st.divider()
st.caption("ESG Mate AI · 교육 및 특별활동용 프로토타입")
