# ESG Mate AI

고등학생 특별활동을 위한 Streamlit 기반 ESG 학습 앱입니다.

## 주요 기능

1. ESG AI 챗봇
2. ESG 뉴스 3줄 요약 및 E/S/G 분류
3. ESG 자가진단과 점수 시각화
4. 진단 결과 기반 개선 활동 제안

OpenAI API 키가 없어도 자가진단, 규칙 기반 뉴스 분류, 기본 개선 제안은 작동합니다.

## 로컬 실행

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

패키지 설치 및 실행:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## OpenAI API 키 설정

프로젝트 폴더에 `.streamlit/secrets.toml` 파일을 만들고 다음 내용을 입력합니다.

```toml
OPENAI_API_KEY = "실제_API_키"
OPENAI_MODEL = "gpt-4.1-mini"
```

`.streamlit/secrets.toml`은 `.gitignore`에 포함되어 있으므로 GitHub에 업로드되지 않습니다.

## GitHub 업로드

```bash
git init
git add .
git commit -m "Initial ESG Mate AI app"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

## Streamlit Community Cloud 배포

1. GitHub 저장소에 코드를 업로드합니다.
2. Streamlit Community Cloud에서 저장소, 브랜치, `app.py`를 선택합니다.
3. 앱 설정의 Secrets에 다음을 입력합니다.

```toml
OPENAI_API_KEY = "실제_API_키"
OPENAI_MODEL = "gpt-4.1-mini"
```

4. Deploy를 실행합니다.

## 프로젝트 구조

```text
esg-mate-streamlit/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── .streamlit/
    └── secrets.toml.example
```

## 주의

이 앱은 교육용 프로토타입입니다. 공식 ESG 평가, 공시, 법률 또는 투자 자문에 사용하지 마세요.
