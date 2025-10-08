# 🦗 Grasshopper Live Analyzer - Standalone Package

## 🎯 개요

Grasshopper 내부에서 **바로 사용 가능한** 완전한 정의 분석 도구!

- ✅ MCP/Claude 불필요
- ✅ 실시간 분석
- ✅ 자동 수정 기능
- ✅ 5가지 컴포넌트
- ✅ 15+ Lint 규칙

---

## 🚀 빠른 시작

### 30초 설치
```
1. Python 컴포넌트 추가
2. component_all_in_one.py 복사
3. 경로 수정 (1줄)
4. Button 연결
5. 완료!
```

### 첫 실행
```
[Button] → [All-in-One] → [Panel]
```

**그게 전부입니다!** 🎉

---

## 📦 포함된 것

### 5개 컴포넌트
1. **All-in-One** ⭐ - 모든 기능
2. **Health Check** - 빠른 체크
3. **Issue Finder** - 이슈 검색
4. **Auto-Fix** - 자동 수정
5. **Statistics** - 통계

### 분석 기능
- 🔍 15+ Lint 규칙
- 📊 건강도 점수 (0-100)
- ⚡ 실시간 분석
- 🔧 자동 수정
- 🎯 문제 하이라이트
- 📈 상세 통계

---

## 💡 주요 기능

### 1. 실시간 Lint 체크
```python
❌ Dangling Inputs (에러)
⚠️  Dangling Outputs (경고)
⚠️  Unnamed Parameters (경고)
ℹ️  Missing Groups (정보)
... 15+ 규칙
```

### 2. 건강도 점수
```
100점 - 에러×10 - 경고×5 - 정보×2

✅ 90-100: Excellent
👍 70-89: Good
⚠️  50-69: Needs Attention
❌ 0-49: Critical
```

### 3. 자동 수정
```
✅ 파라미터 자동 이름 지정
🔍 문제 컴포넌트 하이라이트
📊 수정 전/후 비교
```

### 4. 다양한 리포트
```
- Simple: 한 줄 요약
- Compact: 패널용 요약
- Full: 완전한 상세 리포트
```

---

## 📖 문서

### 시작하기
- **INSTALLATION.md** - 설치 가이드
- **USER_GUIDE.md** - 완전한 사용 가이드

### 고급
- **../analyzer/lint_rules.py** - 규칙 상세
- **gh_live_analyzer.py** - API 문서

---

## 🎨 사용 예시

### 예시 1: 작업 중 체크
```
작업 → 버튼 클릭 → 점수 확인 → 계속 작업
```

### 예시 2: 파일 정리
```
Full Analysis → 이슈 확인 → Auto-Fix → 수동 수정
```

### 예시 3: 공유 전
```
Find Issues → 에러 0 확인 → Statistics → 최종 체크
```

---

## 🔧 기술 사양

### 요구사항
- Rhino 7/8
- Grasshopper
- Python 2.7 (GH 내장)

### 지원 기능
- ✅ 실시간 문서 스캔
- ✅ 컴포넌트 분석
- ✅ 와이어 추적
- ✅ 런타임 에러/경고
- ✅ 자동 수정 (일부)

### 제한사항
- ⚠️  큰 파일 느릴 수 있음 (>1000 컴포넌트)
- ⚠️  일부 수정만 자동화
- ⚠️  그룹 생성은 수동

---

## 🎯 사용 사례

### 개인
- 작업 중 실시간 체크
- 파일 저장 전 검증
- 코드 품질 유지

### 팀
- 표준 품질 기준
- 코드 리뷰
- 온보딩 도구

### 교육
- 베스트 프랙티스 학습
- 일반적 실수 방지
- 정의 품질 이해

---

## 📊 통계

### 코드
- 핵심 엔진: ~600줄
- 컴포넌트: 5개
- Lint 규칙: 15+개
- 함수: 30+개

### 기능
- 자동 체크: 7가지
- 수동 체크: 8가지
- 자동 수정: 2가지
- 리포트 스타일: 3가지

---

## 🔄 vs MCP 버전

### Standalone (이것!)
✅ 설치 간단
✅ Grasshopper만 필요
✅ 실시간 분석
✅ 빠른 피드백
⚠️  기본 분석
⚠️  자동 수정 제한

### MCP + Claude
✅ 완전한 분석
✅ AI 제안
✅ GHX/JSON 파싱
✅ 버전 비교
⚠️  설정 복잡
⚠️  외부 의존성

### 언제 뭘 쓸까?
```
일상 작업 → Standalone
상세 분석 → MCP + Claude
파일 공유 → 둘 다
팀 표준 → 둘 다
```

---

## 🚧 개발 로드맵

### v1.0 (현재) ✅
- [x] 핵심 분석 엔진
- [x] 5개 컴포넌트
- [x] 15 Lint 규칙
- [x] 자동 수정 (기본)
- [x] 문서 완성

### v1.1 (계획)
- [ ] 더 많은 자동 수정
- [ ] 성능 최적화
- [ ] 커스텀 규칙
- [ ] 히스토리 추적

### v2.0 (미래)
- [ ] 컴포넌트 자동 정렬
- [ ] 와이어 정리
- [ ] 성능 분석
- [ ] 팀 대시보드

---

## 🤝 기여

### 버그 리포트
1. 재현 단계
2. 예상 결과
3. 실제 결과
4. GH 버전

### 기능 제안
1. 사용 사례
2. 예상 동작
3. 우선순위

### 코드 기여
1. Fork
2. Branch
3. Commit
4. Pull Request

---

## 📄 라이선스

MIT License - 자유롭게 사용/수정/배포 가능

---

## 🙏 감사

- Grasshopper 팀
- Rhino Python
- Steinberg Hart 팀
- 모든 베타 테스터

---

## 📞 연락처

- **Email**: soku@steinberghart.com
- **Team**: Steinberg Hart
- **GitHub**: (추가 예정)

---

## 📚 관련 프로젝트

### 같은 프로젝트
- **MCP Analyzer** - Claude 통합
- **dual_save** - GH/GHX 동시 저장
- **export_to_json** - JSON 내보내기

### 외부 도구
- **Grasshopper** - Rhino parametric design
- **Claude** - AI assistant
- **MCP** - Model Context Protocol

---

## 🎉 시작하기

```
1. INSTALLATION.md 읽기
2. 컴포넌트 설치
3. USER_GUIDE.md 읽기
4. 첫 분석 실행
5. 즐기기! 🦗
```

---

**Happy Grasshoppering!**

Version: 1.0.0  
Release Date: 2025-01-06  
Status: ✅ Stable & Ready
