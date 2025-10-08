# 🔧 경로 설정 - 3가지 방법

## 문제
매번 경로를 수동으로 바꾸는 것이 불편함

## 해결 방법

---

## 방법 1: 자동 감지 (가장 쉬움 ⭐)

### 스크립트 상단에 추가:

```python
import sys
import os

def find_gh_analyzer():
    """자동으로 gh_live_analyzer.py 위치 찾기"""
    common_paths = [
        r"C:\GH_Analyzer\standalone",
        r"C:\Users\{}\Desktop\gh_analyzer\standalone".format(os.environ.get('USERNAME', '')),
        r"C:\Users\{}\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone".format(os.environ.get('USERNAME', '')),
    ]
    for p in common_paths:
        if os.path.exists(os.path.join(p, "gh_live_analyzer.py")):
            return p
    return None

# 자동 감지
gh_path = find_gh_analyzer()

# 못 찾으면 수동 설정 (fallback)
if not gh_path:
    gh_path = r"여기에_수동_경로"

if gh_path and gh_path not in sys.path:
    sys.path.insert(0, gh_path)
```

---

## 방법 2: Input 파라미터로 받기 (유연함 ⭐⭐)

### 컴포넌트 입력 추가:
```
- run: Button
- path: Text (선택적)
```

### 스크립트:
```python
import sys

# path 입력이 있으면 사용, 없으면 자동 감지
if 'path' in dir() and path:
    gh_path = str(path)
else:
    # 자동 감지 또는 기본값
    gh_path = r"기본_경로"

if gh_path not in sys.path:
    sys.path.insert(0, gh_path)
```

### 사용법:
```
1. 일반 사용: path 입력 비워둠 → 자동 감지
2. 특별한 경우: Text Panel로 경로 연결
```

---

## 방법 3: 환경 변수 사용 (고급 ⭐⭐⭐)

### Windows 환경 변수 설정:
```
1. 시스템 속성 → 환경 변수
2. 새로 만들기:
   변수 이름: GH_ANALYZER_PATH
   변수 값: C:\...\gh_analyzer\standalone
```

### 스크립트:
```python
import sys
import os

gh_path = os.environ.get('GH_ANALYZER_PATH', r"기본_경로")

if gh_path not in sys.path:
    sys.path.insert(0, gh_path)
```

---

## 🎯 추천 사용법

### 개인 사용:
```python
# 방법 1 사용 (자동 감지)
# 한 번 설정하면 모든 컴퓨터에서 작동
```

### 팀 사용:
```python
# 방법 2 사용 (Input 파라미터)
# 각자 자기 경로를 Panel로 연결
```

### 고급 사용자:
```python
# 방법 3 사용 (환경 변수)
# 시스템 전체에서 사용 가능
```

---

## 📝 모든 컴포넌트에 적용하기

### Template 만들기:

```python
"""
[Component Name]
[Description]

Inputs:
- run: Button
- path: Text (OPTIONAL) - Custom path
- [other inputs...]

Outputs:
- [outputs...]
"""

import sys
import os

# === AUTO PATH (복사해서 모든 스크립트에 붙여넣기) ===

if 'path' in dir() and path:
    gh_path = str(path)
else:
    def find_gh_analyzer():
        common_paths = [
            r"C:\GH_Analyzer\standalone",
            r"C:\Users\{}\Desktop\gh_analyzer\standalone".format(os.environ.get('USERNAME', '')),
            r"C:\Users\{}\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone".format(os.environ.get('USERNAME', '')),
        ]
        for p in common_paths:
            if os.path.exists(os.path.join(p, "gh_live_analyzer.py")):
                return p
        return None
    gh_path = find_gh_analyzer()

if not gh_path:
    gh_path = r"FALLBACK_PATH_HERE"  # ← 여기만 수정

if gh_path and gh_path not in sys.path:
    sys.path.insert(0, gh_path)

# === 여기부터 원래 코드 ===

from gh_live_analyzer import GHLiveAnalyzer

# ... rest of your code ...
```

---

## 🚀 빠른 적용

### 기존 스크립트 수정:

**Before:**
```python
gh_path = r"C:\Users\...\standalone"
if gh_path not in sys.path:
    sys.path.insert(0, gh_path)
```

**After:**
```python
# 위의 AUTO PATH 섹션 전체를 복사해서 붙여넣기
```

---

## 💡 각 방법의 장단점

| 방법 | 장점 | 단점 | 추천 |
|------|------|------|------|
| 자동 감지 | 편함, 자동 | 표준 경로 필요 | ⭐⭐⭐ |
| Input 파라미터 | 유연함, 명확 | Input 추가 필요 | ⭐⭐⭐ |
| 환경 변수 | 시스템 전체 | 초기 설정 복잡 | ⭐⭐ |

---

## 🎯 실전 예시

### 시나리오 1: 개인 작업
```
→ 자동 감지 사용
→ 폴더를 표준 위치에 배치:
  C:\GH_Analyzer\standalone
```

### 시나리오 2: 팀 작업
```
→ Input 파라미터 사용
→ .gh 파일에 Text Panel 포함
→ 각자 자기 경로 입력
```

### 시나리오 3: 배포
```
→ 자동 감지 + Fallback
→ 일반 사용자는 자동 감지
→ 안 되면 수동 입력
```

---

## ✅ 테스트

### 경로 확인 스크립트:

```python
import sys
import os

# AUTO PATH
if 'path' in dir() and path:
    gh_path = str(path)
else:
    def find_gh_analyzer():
        common_paths = [
            r"C:\GH_Analyzer\standalone",
            r"C:\Users\{}\Desktop\gh_analyzer\standalone".format(os.environ.get('USERNAME', '')),
            r"C:\Users\{}\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone".format(os.environ.get('USERNAME', '')),
        ]
        for p in common_paths:
            if os.path.exists(os.path.join(p, "gh_live_analyzer.py")):
                return p
        return None
    gh_path = find_gh_analyzer()

# Output result
if gh_path and os.path.exists(os.path.join(gh_path, "gh_live_analyzer.py")):
    a = f"✅ Found!\n\nPath: {gh_path}\n\nMode: {'Custom Input' if 'path' in dir() and path else 'Auto-detected'}"
else:
    a = f"❌ Not found!\n\nTried: {gh_path}\n\nPlease provide path via input or edit fallback path"
```

이 스크립트로 먼저 테스트하세요!

---

**이제 경로 걱정 없이 사용하세요!** 🎉
