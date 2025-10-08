# Claude Desktop 연동 가이드

## Claude Desktop MCP 설정

### 1단계: MCP 서버 시작

```bash
# 필수 패키지 설치
pip install -r src/gh/requirements.txt

# 서버 시작
python src/gh/start_server.py
```

서버가 `http://127.0.0.1:5071`에서 실행됩니다.

### 2단계: Claude Desktop 설정

Claude Desktop 설정 파일 위치:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

설정 파일에 다음 추가:

```json
{
  "mcpServers": {
    "grasshopper": {
      "command": "C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\Grasshopper-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "grasshopper_mcp.bridge"]
    },
    "filesystem": {
      "command": "node",
      "args": [
        "C:\\Users\\Soku\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-filesystem\\dist\\index.js",
        "C:\\Users\\Soku\\Downloads",
        "C:\\Users\\Soku\\Documents"
      ]
    },
    "rhino_scripts": {
      "command": "python",
      "args": [
        "C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\vscode_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts"
      }
    },
    "gh_analyzer": {
      "command": "python",
      "args": [
        "C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\src\\gh\\mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts"
      }
    }
  }
}
```

### 3단계: Claude Desktop 재시작

설정 파일을 저장한 후 Claude Desktop을 완전히 종료하고 다시 시작하세요.

---

## 사용 가능한 도구

### 1. gh.parse(path)
정의 파일 분석 및 요약

**입력:**
```
path: JSON 파일 경로
```

**출력:**
- 문서 정보
- 컴포넌트/파라미터/와이어 통계
- 카테고리별 분포
- 분석 리포트

### 2. gh.lint(path, rules?)
Lint 검사 실행

**입력:**
```
path: JSON 파일 경로
rules: (선택) 체크할 규칙 ID 리스트 (예: ["GH001", "GH003"])
```

**출력:**
- 발견된 이슈 목록
- 심각도별 요약
- 수정 제안

### 3. gh.suggest(path, goal)
목표 기반 개선 제안

**입력:**
```
path: JSON 파일 경로
goal: 목표 설명 (예: "optimize performance", "improve readability")
```

**출력:**
- 우선순위별 제안
- 구체적인 수정 단계
- 컴포넌트 레벨 가이드

### 4. gh.diff(path_a, path_b)
두 버전 비교

**입력:**
```
path_a: 첫 번째 JSON 파일
path_b: 두 번째 JSON 파일
```

**출력:**
- 추가/삭제/변경된 컴포넌트
- 와이어 변경사항
- 변경 요약

---

## 테스트

### API 직접 테스트

```bash
# 서버 상태 확인
curl http://127.0.0.1:5071/

# 규칙 목록 확인
curl http://127.0.0.1:5071/gh/rules

# 분석 (POST)
curl -X POST http://127.0.0.1:5071/gh/parse \
  -H "Content-Type: application/json" \
  -d '{"path": "C:/temp/my_definition.json"}'
```

### Claude Desktop에서 테스트

Claude에게 다음과 같이 물어보세요:

```
내 Grasshopper 정의 파일을 분석해줘:
C:\temp\my_definition.json
```

Claude가 자동으로 적절한 MCP 도구를 사용합니다.
