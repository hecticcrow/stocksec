import streamlit as st
import google.generativeai as genai
import pandas as pd

# [2026-02-11] 기준 환율 설정
EXCHANGE_RATE = 1449.28 

# 1. 제미나이 설정 (PRO/사고적 모드 페르소나 주입)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

SYSTEM_PROMPT = f"""
당신은 PRO 수준의 주식 공시 분석기입니다. 다음 4가지 철칙을 반드시 준수하여 분석하십시오:

1. 계약별 독립 검증: 한 종목에 여러 투자 계약이 섞여 있을 경우, 각각 별개로 분석하라.
2. 원문(Exhibit) 대조 필수: 8-K 본문이 아닌 첨부된 계약서(Exhibit) 원문을 기반으로 '고정 가격'인지 '조정 가능 가격(Death Spiral)'인지 판별하라.
3. 추측성 판단 금지: 근거 없는 예상 조정가는 언급하지 말고, 확실하지 않으면 "확인 불가"로 고지하라.
4. 원화 환산 필수: 모든 달러($) 수치는 1,449.28원/$ 환율을 적용하여 한화로 병기하라.

[출력 형식]
- 등급: (S, A, B, C, D)
- 핵심 논리: (사고적 모드에 따른 단계별 판단 근거)
- 리스크 검토: (계약 조건에 따른 잠재적 위험)
"""

# 2. 스트림릿 UI 구성
st.set_page_config(page_title="Alpha Intelligence Pro", layout="wide")
st.title("🚀 AI 주식 터미널 (Professional Mode)")

# 사이드바에서 티커 관리
with st.sidebar:
    st.header("설정")
    default_tickers = "BNAI, UUU, HDK, BZAI, AISP"
    ticker_input = st.text_input("분석할 티커 입력 (쉼표 구분)", default_tickers)
    tickers = [t.strip().upper() for t in ticker_input.split(",")]
    
    analyze_btn = st.button("실시간 정밀 분석 시작")

# 3. 분석 로직
if analyze_btn:
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    for ticker in tickers:
        with st.expander(f"🔍 {ticker} 분석 리포트", expanded=True):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.info(f"{ticker} 최신 뉴스 및 SEC 공시 데이터를 가져오는 중...")
                # (실제 API 연결 시 여기서 뉴스/공시 텍스트를 fetch합니다)
                mock_data = f"{ticker}의 최근 8-K 공시: Exhibit 10.1에 따른 $5,000,000 규모의 전환사채 발행..."
            
            with col2:
                # 제미나이 분석 실행
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n데이터: {mock_data}")
                st.markdown(response.text)
                
                # 원화 환산 예시 (제미나이가 출력하겠지만, UI단에서도 강조)
                st.caption(f"기준 환율: {EXCHANGE_RATE}원 / $")

# 4. 데이터 대시보드 (추가 기능)
st.divider()
st.subheader("📊 관심 종목 변동성 모니터링")
df = pd.DataFrame({"Ticker": tickers, "Status": "Ready for Analysis"})
st.table(df)