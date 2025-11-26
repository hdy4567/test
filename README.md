# GitHub Trending Repository Analyzer 🔥

자동으로 GitHub trending 리포지터리를 분석하고 4가지 핵심 요소로 리포트를 생성하는 도구입니다.

## ✨ 주요 기능

이 도구는 Slack #일반 채널의 요구사항에 따라 GitHub trending 리포지터리를 다음 4가지 핵심 요소로 분석합니다:

### 📋 분석 항목

1. **#문제정의** - 해결하려는 핵심 문제, 솔루션 접근법, 사용 사례
2. **#아키텍처_툴** - 시스템 아키텍처, 기술 스택, 핵심 구성요소
3. **#데이터플로우** - 개발부터 런타임까지 전체 흐름, 비동기 처리, 데이터 구조
4. **#문서화** - 문서 구조와 철학, 접근법 및 특징, 커뮤니티 지원

### 🎯 추가 기능

- 🔥 **인기 토론 분석**: 가장 활발한 이슈와 토론 추적
- 📊 **자동 리포트 생성**: 텍스트 및 JSON 형식 리포트
- ⚡ **실시간 데이터**: GitHub API를 통한 최신 정보

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.7 이상
- `requests` 라이브러리

### 설치

```bash
# 저장소 클론
git clone https://github.com/hdy4567/test.git
cd test

# 의존성 설치
pip install requests
```

### 사용 방법

#### 기본 사용

```bash
python github_trending_analyzer.py
```

#### GitHub Token 사용 (권장)

GitHub API rate limit를 높이기 위해 personal access token을 사용할 수 있습니다:

```bash
export GITHUB_TOKEN="your_github_token_here"
python github_trending_analyzer.py
```

#### Python 코드에서 사용

```python
from github_trending_analyzer import GitHubTrendingAnalyzer

# Analyzer 초기화
analyzer = GitHubTrendingAnalyzer(github_token="your_token")

# Trending 리포지터리 가져오기
trending = analyzer.get_trending_repos(language='python', since='daily', limit=5)

# 특정 리포지터리 분석
analysis = analyzer.analyze_repository('owner', 'repo')

# 리포트 생성
report = analyzer.generate_report([analysis])
print(report)
```

## 📊 출력 예시

프로그램을 실행하면 다음과 같은 결과를 얻을 수 있습니다:

```
🔥 GitHub Trending Repository Analysis Report
================================================================================
Generated: 2025-11-26 14:30:00

================================================================================
📊 Repository 1: owner/repo-name
================================================================================

📌 Basic Information
   ⭐ Stars: 12,345
   🔱 Forks: 1,234
   💬 Language: Python
   📝 Description: Amazing tool for developers
   🔗 URL: https://github.com/owner/repo

🎯 #1 Problem Definition
   • Has clear problem statement: ✅
   • README length: 15,234 characters

🏗️ #2 Architecture & Tools
   • Primary language: Python
   • Detected technologies: python, docker, kubernetes, fastapi
   • Has architecture diagram: ✅

🔄 #3 Data Flow
   • Mentions API: ✅
   • Mentions Database: ✅
   • Mentions Async: ✅
   • Has flow diagram: ✅

📚 #4 Documentation
   • Has README: ✅
   • Has installation guide: ✅
   • Has usage examples: ✅
   • Has contributing guide: ✅
   • Has license: ✅
   • Open issues: 42

💬 Hot Discussions
   1. Feature request: Add support for X
      • Issue #123 | 45 comments | open
      • https://github.com/owner/repo/issues/123
```

## 📁 출력 파일

프로그램 실행 후 다음 파일들이 생성됩니다:

- `github_trending_analysis_YYYYMMDD_HHMMSS.txt` - 사람이 읽기 쉬운 텍스트 리포트
- `github_trending_analysis_YYYYMMDD_HHMMSS.json` - 기계가 처리하기 쉬운 JSON 데이터

## 🔧 고급 설정

### 언어별 필터링

```python
analyzer = GitHubTrendingAnalyzer()
trending = analyzer.get_trending_repos(
    language='python',  # 특정 언어 필터
    since='weekly',     # 'daily', 'weekly', 'monthly'
    limit=10            # 가져올 리포지터리 수
)
```

### 커스텀 분석

```python
# 특정 리포지터리 상세 정보
details = analyzer.get_repo_details('owner', 'repo')

# README 가져오기
readme = analyzer.get_readme('owner', 'repo')

# 이슈 목록 가져오기
issues = analyzer.get_repo_issues('owner', 'repo', state='open', limit=10)
```

## 📝 GitHub Token 발급 방법

1. GitHub 계정에 로그인
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. "Generate new token" 클릭
4. 필요한 권한 선택:
   - `public_repo` (공개 리포지터리 접근)
   - `read:user` (사용자 정보 읽기)
5. Token 생성 후 안전한 곳에 저장

## 🤝 기여하기

이 프로젝트는 Slack #일반 채널의 요구사항을 기반으로 만들어졌습니다.

개선 사항이나 버그 리포트는 언제든 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

MIT License - 자유롭게 사용하세요!

## 🙏 감사의 말

이 프로젝트는 Slack #일반 채널의 GitHub 트렌딩 분석 요청에서 시작되었습니다.

- Perplexity를 사용한 초기 분석 아이디어
- 4가지 핵심 요소 분석 프레임워크
- 커뮤니티 피드백

## 📞 연락처

문의사항이 있으시면 GitHub Issues를 통해 알려주세요!

---

**Made with ❤️ by hdy4567**
