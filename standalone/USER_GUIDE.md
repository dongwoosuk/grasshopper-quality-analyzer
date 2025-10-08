# 🎯 Grasshopper Live Analyzer - User Guide

## 📦 풀 패키지 - 일반 유저용

Grasshopper 안에서 바로 사용할 수 있는 **완전한 분석 도구**입니다!

---

## 🚀 빠른 시작

### 1단계: 설치
1. Python 컴포넌트를 캔버스에 추가
2. 아래 스크립트 중 하나를 복사해서 붙여넣기
3. 입력/출력 연결
4. 완료! 🎉

### 2단계: 선택하기
상황에 맞는 컴포넌트를 선택하세요:

| 컴포넌트 | 용도 | 난이도 |
|---------|------|-------|
| **All-in-One** | 모든 기능 (추천!) | ⭐⭐ |
| **Health Check** | 빠른 체크 | ⭐ |
| **Issue Finder** | 상세한 이슈 찾기 | ⭐⭐ |
| **Auto-Fix** | 자동 수정 | ⭐⭐ |
| **Statistics** | 통계만 보기 | ⭐ |

---

## 🎨 컴포넌트 상세 가이드

### 1. All-in-One (추천 ⭐)

**가장 강력한 올인원 도구**

#### 입력:
- `run` (Button): 분석 실행
- `mode` (Number Slider 0-4): 분석 모드
  - `0` = 빠른 체크
  - `1` = 전체 분석
  - `2` = 통계만
  - `3` = 이슈 상세
  - `4` = 자동 수정
- `auto_fix` (Boolean): 자동 수정 활성화
- `highlight_issues` (Boolean): 캔버스에서 하이라이트

#### 출력:
- `report` (Panel): 메인 리포트
- `score` (Number): 건강도 점수 (0-100)
- `errors` (Panel): 에러 목록
- `warnings` (Panel): 경고 목록
- `stats` (Panel): 통계 요약
- `fixed` (Panel): 수정된 내용

#### 사용 예시:
```
[Button] → run
[Slider 0-4] → mode
[Toggle] → auto_fix
[Toggle] → highlight_issues

     ↓

[All-in-One Python Component]

     ↓

report → [Panel]
score → [Panel]
errors → [Panel]
warnings → [Panel]
```

---

### 2. Health Check

**가장 간단한 건강 체크**

#### 입력:
- `x` (Button): 실행
- `style` (Text): 'simple', 'compact', 'full'

#### 출력:
- `report` (Panel): 리포트
- `score` (Number): 점수
- `issues` (Number): 이슈 수

#### 언제 사용?
- 작업 중 빠른 체크
- 파일 저장 전 확인
- 간단한 건강도 확인

---

### 3. Issue Finder

**특정 이슈 타입 찾기**

#### 입력:
- `x` (Button): 실행
- `check_errors` (Boolean): 에러 체크
- `check_warnings` (Boolean): 경고 체크
- `check_info` (Boolean): 정보 체크

#### 출력:
- `errors` (List): 에러 목록
- `warnings` (List): 경고 목록
- `info` (List): 정보 목록
- `summary` (Text): 요약

#### 언제 사용?
- 특정 타입 이슈만 보고 싶을 때
- 에러만 집중해서 수정
- 상세한 이슈 리스트 필요

---

### 4. Auto-Fix

**자동 수정 도구**

#### 입력:
- `x` (Button): 실행
- `fix_names` (Boolean): 파라미터 자동 이름 지정
- `highlight` (Boolean): 이슈 하이라이트
- `name_prefix` (Text): 이름 접두사 (기본: "Param")

#### 출력:
- `report` (Text): 수정 내용
- `fixed_count` (Number): 수정된 항목 수

#### 언제 사용?
- 빠르게 이름 없는 파라미터 수정
- 문제 있는 컴포넌트 찾기
- 배치 수정

---

### 5. Statistics

**문서 통계**

#### 입력:
- `x` (Button): 실행

#### 출력:
- `component_count` (Number): 컴포넌트 수
- `wire_count` (Number): 와이어 수
- `group_count` (Number): 그룹 수
- `by_category` (Text): 카테고리별 분석
- `breakdown` (Text): 전체 분석

#### 언제 사용?
- 파일 복잡도 확인
- 컴포넌트 분포 분석
- 문서화용 데이터

---

## 📊 건강도 점수 시스템

### 점수 계산:
- 시작: 100점
- 에러: -10점/개
- 경고: -5점/개
- 정보: -2점/개

### 등급:
- **90-100점**: ✅ Excellent - 완벽!
- **70-89점**: 👍 Good - 좋음
- **50-69점**: ⚠️ Needs Attention - 주의 필요
- **0-49점**: ❌ Critical - 심각

---

## 🔍 체크되는 항목들

### ❌ 에러 (Errors)
1. **GH001: Dangling Inputs**
   - 연결 안 된 입력
   - 예상치 못한 기본값 사용 가능
   - **수정**: 필요한 입력 연결

2. **GHRT1: Runtime Errors**
   - 실행 중 에러
   - 컴포넌트가 제대로 작동 안 함
   - **수정**: 에러 메시지 확인 후 수정

### ⚠️ 경고 (Warnings)
1. **GH002: Dangling Outputs**
   - 사용 안 되는 출력
   - 불필요한 계산
   - **수정**: 출력 사용 또는 컴포넌트 제거

2. **GH003: Unnamed Parameters**
   - 이름 없는 파라미터
   - 이해하기 어려움
   - **수정**: 의미있는 이름 부여
   - **자동 수정 가능!**

3. **GHRT2: Runtime Warnings**
   - 실행 중 경고
   - 잠재적 문제
   - **수정**: 경고 메시지 확인

### ℹ️ 정보 (Info)
1. **GH004: Missing Groups**
   - 그룹 없음
   - 복잡한 정의 정리 필요
   - **수정**: Ctrl+G로 그룹 생성

2. **GH012: Preview Disabled**
   - 미리보기 꺼짐
   - 디버깅 어려움
   - **수정**: 필요한 곳만 미리보기 활성화

---

## 💡 실전 워크플로우

### 시나리오 1: 작업 중 빠른 체크
```
1. Health Check 컴포넌트 사용
2. mode = 0 (Quick Check)
3. 점수 확인
4. 90점 이상이면 계속 작업
5. 70점 이하면 이슈 확인
```

### 시나리오 2: 파일 정리
```
1. All-in-One 사용
2. mode = 1 (Full Analysis)
3. 모든 이슈 확인
4. mode = 4 (Auto-Fix)
5. auto_fix = True
6. 남은 이슈 수동 수정
7. 다시 체크
```

### 시나리오 3: 파일 공유 전
```
1. All-in-One 사용
2. mode = 3 (Find Issues)
3. 에러 0개 확인
4. 경고 최소화
5. Statistics로 문서 크기 확인
6. 그룹/이름 정리
7. 최종 체크
```

### 시나리오 4: 큰 파일 최적화
```
1. Statistics로 현황 파악
2. Issue Finder로 문제 찾기
3. Auto-Fix로 간단한 것 수정
4. 수동으로 복잡한 것 수정
5. 다시 Statistics로 개선 확인
```

---

## 🎯 팁 & 트릭

### 성능 팁
- 큰 파일은 mode=0으로 시작
- 자주 체크하면서 작업
- 90점 이상 유지 목표

### 정리 팁
- 파라미터는 항상 이름 붙이기
- 10개 이상이면 그룹 만들기
- 사용 안 하는 출력 정리
- 주석/스크리블 추가

### 협업 팁
- 공유 전 반드시 체크
- 에러 0개 목표
- 점수 기준 정하기 (예: 80점 이상)
- 표준 이름 규칙 정하기

---

## 🐛 문제 해결

### "No active Grasshopper document"
- Grasshopper가 열려있는지 확인
- 파일이 로드되어 있는지 확인

### "Module not found"
- 스크립트 상단의 경로 확인
- 경로가 맞는지 확인
```python
gh_path = r"C:\Users\...\RhinoScripts\src\gh\standalone"
```

### "분석이 너무 느려요"
- 큰 파일은 mode=0 사용
- Statistics만 보기 (mode=2)
- 일부 체크만 활성화

### "자동 수정이 안 돼요"
- auto_fix = True 확인
- 현재는 이름 붙이기만 지원
- 다른 수정은 수동으로

---

## 📈 향후 기능 (계획)

- [ ] 더 많은 자동 수정
- [ ] 컴포넌트 자동 정렬
- [ ] 와이어 정리
- [ ] 성능 최적화 제안
- [ ] 히스토리 추적
- [ ] 팀 표준 체크
- [ ] 커스텀 규칙

---

## 🎓 더 배우기

### 문서
- `README.md` - 전체 프로젝트 개요
- `FORMAT_COMPARISON.md` - GHX vs JSON
- `PROMPTS.md` - Claude 사용법

### 개발자용
- MCP 서버로 Claude 통합
- 더 많은 lint 규칙
- JSON 분석 (100% 정확)

---

## 💬 피드백

문제가 있거나 제안사항이 있으면:
1. GitHub Issues (있다면)
2. 팀 Slack
3. soku@steinberghart.com

---

**Happy Grasshoppering! 🦗**

Version 1.0.0
Last Updated: 2025-01-06
