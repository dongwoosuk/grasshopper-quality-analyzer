# Grasshopper 분석 프롬프트 템플릿

Claude와 함께 Grasshopper 정의를 분석할 때 사용할 수 있는 프롬프트 템플릿입니다.

---

## 📊 기본 분석

```
You are a Grasshopper definition expert. I have a GH definition exported to JSON.

Please analyze this file and provide:
1. Overview: component count, categories used, complexity metrics
2. Health check: any obvious issues or warnings
3. Quick recommendations for improvement

File path: [PATH_TO_JSON]
```

---

## 🔍 상세 Lint 검사

```
You are a Grasshopper code reviewer. Run a comprehensive lint check on my GH definition.

Tasks:
1. Check against all 15 lint rules
2. List Top 5 most critical issues with:
   - Rule ID and severity
   - Why it matters
   - Concrete fix steps
   - Affected components (with GUIDs)
3. Provide a priority-ordered action plan

File path: [PATH_TO_JSON]
```

---

## 🎯 목표 기반 개선

### 성능 최적화

```
I need to optimize my Grasshopper definition for better performance.

Current file: [PATH_TO_JSON]
Goal: Reduce computation time by at least 50%

Please:
1. Identify performance bottlenecks
2. Suggest specific component replacements or restructuring
3. Provide step-by-step optimization plan
4. Estimate potential performance gain for each suggestion
```

### 가독성 향상

```
Help me make this Grasshopper definition more maintainable and readable.

Current file: [PATH_TO_JSON]
Goal: Team members should understand the logic without explanation

Please suggest:
1. Naming improvements (parameters, groups)
2. Documentation needs (scribbles, comments)
3. Organization restructuring (grouping, clustering)
4. Data flow simplification
```

### 데이터 트리 안정화

```
My definition has unpredictable data tree behavior.

Current file: [PATH_TO_JSON]
Goal: Stable and predictable data tree structure

Analyze:
1. Current tree access patterns (item/list/tree mixing)
2. Excessive flatten/graft usage
3. Tree manipulation chain depth
4. Suggest standardization strategy
```

---

## 🔄 버전 비교

```
Compare two versions of my Grasshopper definition.

Version A (before): [PATH_A]
Version B (after): [PATH_B]

Please provide:
1. Summary of changes (added/removed/modified components)
2. Impact analysis (potential breaking changes)
3. Improvement or regression assessment
4. Migration notes if needed
```

---

## 🏗️ 리팩토링 계획

```
Create a refactoring plan for my Grasshopper definition.

Current file: [PATH_TO_JSON]
Goals:
- [GOAL_1]
- [GOAL_2]
- [GOAL_3]

Please provide:
1. Current state assessment
2. Proposed architecture/structure
3. Step-by-step refactoring plan (ordered to minimize breaking changes)
4. Risk analysis for each step
5. Testing checkpoints
```

---

## 🎓 교육용 분석

```
Explain this Grasshopper definition to a beginner.

File: [PATH_TO_JSON]

Please:
1. Describe the overall purpose and logic
2. Break down into major sections
3. Explain key component chains
4. Identify learning points (techniques used)
5. Suggest similar example projects to study
```

---

## 📦 클러스터링 제안

```
Identify opportunities to create clusters in my definition.

File: [PATH_TO_JSON]

Find:
1. Repeated component sequences (potential clusters)
2. Self-contained logic blocks that could be modular
3. For each suggestion:
   - Component GUIDs involved
   - Cluster name suggestion
   - Input/output interface
   - Reusability score
```

---

## 🔌 플러그인 의존성 분석

```
Analyze plugin dependencies in my definition.

File: [PATH_TO_JSON]

Report:
1. List all non-core plugins used
2. For each plugin:
   - Usage count (how many components)
   - Critical or replaceable?
   - Core alternatives if available
3. Dependency risk assessment
4. Recommendations for reducing dependencies
```

---

## 💡 Best Practice 체크

```
Review my definition against Grasshopper best practices.

File: [PATH_TO_JSON]

Check for:
1. ✅ Naming conventions
2. ✅ Documentation (scribbles, groups)
3. ✅ Data tree management
4. ✅ Component organization
5. ✅ Performance considerations
6. ✅ Maintainability

Rate each category (1-5) and provide specific improvements.
```

---

## 🎨 캔버스 레이아웃 분석

```
Analyze the visual layout and organization of my definition.

File: [PATH_TO_JSON]

Assess:
1. Wire crossing issues (long wires, tangled connections)
2. Component spacing and alignment
3. Group organization
4. Suggest layout improvements for better readability
5. Identify areas that need relay components
```

---

## 사용 예시

### 실제 대화 흐름

```
User: 내 Grasshopper 파일을 분석해줘
File: C:\Projects\building_facade.json
목표는 성능 최적화야

Claude: 
[gh.parse 실행]
[gh.lint 실행]
[gh.suggest 실행 with goal="optimize performance"]

분석 결과를 보니 주요 병목이 3곳 있습니다:

1. [Component A] - 데이터 트리 flatten 남용
   → 제안: Graft 대신 Partition List 사용
   
2. [Component B] - 중복 계산
   → 제안: Cluster로 분리 + Data Dam

3. [Component C] - 비효율적인 지오메트리 생성
   → 제안: native 컴포넌트로 대체

구체적인 수정 방법을 단계별로 설명해드릴까요?
```

---

## 템플릿 커스터마이징

자신만의 팀 규칙을 추가하려면:

```
Based on our team standards:
- All sliders must have descriptive names
- Maximum 50 components per group
- No flatten before [specific operation]
- Required: version scribble in top-left

Check my definition against these rules.
File: [PATH_TO_JSON]
```
