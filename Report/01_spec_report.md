# Unit Converter — SPEC 단계 보고서 (01)

> **프로젝트:** UnitConverter_09  
> **단계:** SPEC (설계·분석·추적·Cursor Harness)  
> **브랜치:** `spec`  
> **작성 일자:** 2026-06-05  
> **기준:** README.md Activities 1단계 (0.5시간) + SPEC 산출 확장

---

## 1. SPEC 단계 목표

| 항목 | 내용 |
|------|------|
| **목표** | 레거시 코드·PRD Gap 분석, Dual-Track TDD 설계, FR/NFR·패키지 목표 구조 확정, RED 단계 Agent 규칙 정의 |
| **범위** | 문서·`.cursor/` 설정만 — **프로덕션·테스트 코드 미작성** |
| **다음 단계** | RED (`tests/` + `pytest.fail`) → GREEN → REFACTOR (`unit_converter/` 패키지) |

---

## 2. Activities 1단계 달성 요약

README Activities **「1. 문제 코드 및 기본 요구사항 분석 (0.5시간)」** 에 해당하는 SPEC 작업을 수행하고, 이후 단계(2~4)를 위한 **설계·추적·Harness** 까지 선행 정리했다.

| Activities | SPEC 산출 | 상태 |
|------------|-----------|------|
| 1. 코드·요구사항 분석 | `docs/spec_analysis.md` | ✅ |
| 2~3. 기본·품질 + TC (선행 설계) | `docs/prd_test_traceability.md`, `docs/dual_track_design.md` | ✅ 설계만 |
| 4. 추가 요구 (선행 설계) | 추적표 Phase 2 · architecture FR-09~11 | ✅ 설계만 |
| Agent Harness | `.cursor/rules`, `skills`, `commands` | ✅ |

---

## 3. AS-IS 분석 (레거시)

### 3.1 분석 대상

- **파일:** `UnitConverter.py` (37줄, 단일 `main()`)
- **동작:** `meter` / `feet` / `yard` 3단위 변환, 콜론 형식·숫자·unknown unit 부분 검증

### 3.2 핵심 Gap (PRD 대비)

| 구분 | AS-IS | PRD 목표 |
|------|-------|----------|
| 아키텍처 | God Function | OCP/SRP 클래스 구성 |
| 단위 확장 | if/elif·print 추가 | Registry·변경 최소화 |
| 입력 검증 | 음수·빈 토큰 미처리 | 음수·형식·없는 단위 |
| 설정 | 매직 넘버 하드코딩 | JSON/YAML 외부화 |
| 테스트 | 없음 | 15 TC (Dual-Track) |
| 추가 기능 | 없음 | 동적 등록·출력 포맷 |

### 3.3 레거시 스멜 요약

| 원칙 | 주요 이슈 |
|------|-----------|
| **OCP** | 단위·비율·출력 변경 시 `main()` 직접 수정 |
| **SRP** | 입출력·파싱·검증·변환·출력 한 함수에 혼재 |
| **입력 검증** | `meter:-1`, `:2.5`, `meter:` 등 미처리 |
| **확장성** | 테스트·설정·패키지 구조 부재 |

**상세:** `docs/spec_analysis.md`

---

## 4. SPEC 산출물 목록

### 4.1 문서 (`docs/`)

| 문서 | 역할 | 핵심 내용 |
|------|------|-----------|
| `spec_analysis.md` | Gap·스멜 분석 | OCP/SRP/검증/확장성 20+ 항목, PRD Gap 매트릭스 |
| `prd_test_traceability.md` | REQ ↔ Test 추적 | **15 TC** · REQ 16개 · Track A/B · Phase 1/2 |
| `dual_track_design.md` | Dual Track 최종 설계 | RED 설계표 · Gate 1/2 · 실행 순서 · Track B 선행 명시 |
| `architecture.md` | REFACTOR 목표 구조 | `unit_converter/` 패키지 · **FR 11 · NFR 8** 매핑 · RED 규칙 §12 |

### 4.2 Cursor Harness (`.cursor/`)

| 경로 | 역할 |
|------|------|
| `rules/unit-converter-project.mdc` | alwaysApply — 단계·Track·문서 SSOT |
| `rules/unit-converter-red.mdc` | `tests/**` — RED 금지 규칙 |
| `rules/unit-converter-refactor.mdc` | `unit_converter/**` — OCP/SRP 목표 |
| `skills/unit-converter-tdd/SKILL.md` | Dual-Track TDD 절차 SSOT |
| `skills/unit-converter-tdd/reference.md` | 15 TC · FR 요약 |
| `commands/tdd-red.md` | `/tdd-red` — RED만 |
| `commands/tdd-green.md` | `/tdd-green` — 최소 구현 |
| `commands/spec-only.md` | `/spec-only` — 문서만 |

### 4.3 의도적으로 미작성 (SPEC 범위 외)

| 항목 | 이유 |
|------|------|
| `unit_converter/` 패키지 | REFACTOR 단계 |
| `tests/` | RED 단계 |
| `config/units.json` | RED/GREEN 이후 |
| `UnitConverter.py` 수정 | GREEN/REFACTOR |

---

## 5. Dual-Track 설계 결정

### 5.1 Track 정의 (레이어 기준)

| Track | 명칭 | 책임 | TC | RED 순서 |
|-------|------|------|-----|----------|
| **A** | UI / Boundary | 파싱·검증·출력 | `U-*` (7개) | **2번째** |
| **B** | Domain / Logic | 변환·등록·설정 | `D-*` (8개) | **1번째** |

> **Track A/B = 레이어 이름.** 실행 순서는 **Domain(B) → Boundary(A)** (의존성·mock-free TDD).

### 5.2 Phase · Gate

| Phase | TC 수 | Gate |
|-------|-------|------|
| Phase 1 Core | 10 | Gate 1 — 기본·품질 |
| Phase 2 Extension | 5 | Gate 2 — 설정·등록·JSON 출력 |
| **합계** | **15** | Full PRD Green |

**상세 RED 표:** `docs/dual_track_design.md` §4 · `docs/prd_test_traceability.md` §2

### 5.3 추적표 단순화 이력

| 버전 | TC 수 | 비고 |
|------|-------|------|
| v1 (초안) | 30 | REQ 21 — Activities 전체 커버, 실습에 과다 |
| v2 (보완) | 18 | Layer Track (Boundary/Domain) |
| **v3 (확정)** | **15** | Minimal + U-IN-04/05, D-CNV-04, D-CFG-02, D-REG-02 |

---

## 6. FR / NFR 매핑 (SPEC 확정)

### 6.1 Functional Requirements (FR)

| FR ID | 요약 | SPEC 문서 | REFACTOR 모듈 |
|-------|------|-----------|---------------|
| FR-01 | unit:value 입력 | 추적표 | `InputParser` |
| FR-02 | 전 단위 변환 출력 | 추적표 | `UnitConverter`, `ConversionService` |
| FR-03 | meter/feet/yard | 추적표 | `UnitRegistry` |
| FR-04 | OCP 단위 확장 | architecture | `UnitRegistry.register()` |
| FR-05~07 | 비즈니스 비율 | 추적표 | `UnitConverter` |
| FR-08 | 테스트 검증 | dual_track | `tests/` |
| FR-09~11 | 설정·등록·포맷 | architecture | `config_loader`, `formatter` |

### 6.2 Non-Functional Requirements (NFR)

| NFR ID | 요약 | SPEC 대응 |
|--------|------|-----------|
| NFR-01 | OCP | Registry · Formatter Strategy · Phase 2 Converter 무변경 |
| NFR-02 | SRP | application / domain / infrastructure 분리 |
| NFR-03~05 | 입력 검증 | U-IN-01~05 |
| NFR-06 | 테스트 가능성 | Domain TC mock-free, Track B 선행 |
| NFR-07 | 설정 무재배포 | `units.json` |
| NFR-08 | CLI 호환 | `UnitConverter.py` 얇은 main |

**상세:** `docs/architecture.md` §5~§6

---

## 7. REFACTOR 목표 패키지 (미적용·설계만)

```
UnitConverter.py                 # CLI (README 호환)
unit_converter/
  application/                   # Track A
    parser.py, validator.py, formatter.py, service.py
  domain/                        # Track B
    converter.py, registry.py, models.py, exceptions.py
  infrastructure/
    config_loader.py
config/units.json
tests/
  test_domain.py, test_boundary.py
```

**적용 시점:** REFACTOR (RED·GREEN 이후)  
**상세:** `docs/architecture.md` §3~§8

---

## 8. RED 단계 규칙 (SPEC 확정)

Agent 실행 SSOT: `.cursor/rules/unit-converter-red.mdc` · `/tdd-red`

| 규칙 | 내용 |
|------|------|
| ❌ | RED 단계에서 **구현 코드 작성 금지** |
| ✅ | **`pytest.fail("RED: ...")` 허용** |
| ❌ | **`skip` / `xfail` 금지** |
| ✅ | **1 RED 묶음 = 1 커밋** (`[RED] …`) |

**권장 RED 순서:** D-CNV-01 → … → D-CNV-04 → U-IN-01 → … → U-OUT-01 → (Phase 2) D-CFG → D-REG → U-FMT-01

---

## 9. Git 이력 (SPEC 커밋)

| 커밋 | 메시지 | 주요 파일 |
|------|--------|-----------|
| `b93b50b` | [SPEC] 레거시 코드 스멜 및 PRD Gap 분석 | `docs/spec_analysis.md` |
| `aa257c7` | [SPEC] PRD to Test ID traceability matrix | `docs/prd_test_traceability.md` (v1) |
| `9c30bf1` | [SPEC] Dual Track design document | `docs/dual_track_design.md` |
| `8a155fa` | [SPEC] Traceability 15 TC (amend) | `prd_test_traceability.md` v3 |
| `d20592d` | [SPEC] architecture FR/NFR | `docs/architecture.md` |
| `9416db0` | [SPEC] Cursor rules/skills/commands | `.cursor/**`, `architecture.md` 보완 |

**브랜치:** `spec`  
**미커밋:** `.cursor.zip`, `UnitConverter.zip` (아카이브, 저장소 제외 권장)

---

## 10. SPEC 완료 기준 체크리스트

| # | 항목 | 상태 |
|---|------|------|
| 1 | 레거시·PRD Gap 문서화 | ✅ |
| 2 | Dual-Track RED 15 TC 정의 | ✅ |
| 3 | FR/NFR → 모듈 매핑 | ✅ |
| 4 | REFACTOR 목표 패키지 (OCP/SRP) | ✅ |
| 5 | Cursor RED/GREEN/SPEC Harness | ✅ |
| 6 | 프로덕션·테스트 코드 미작성 | ✅ |
| 7 | RED 단계 규칙 Agent 반영 | ✅ |

---

## 11. 다음 단계 (RED)

| 순서 | 작업 | Command / 문서 |
|------|------|----------------|
| 1 | `tests/` 디렉터리 생성 | — |
| 2 | D-CNV-01 RED | `/tdd-red` · Track B |
| 3 | Domain TC 순차 RED | `reference.md` |
| 4 | Boundary TC RED | U-IN → U-OUT |
| 5 | 1 묶음 = 1 커밋 | `[RED] D-CNV-01 …` |
| 6 | Gate 1 (10 TC FAIL 확인) | `dual_track_design.md` §6 |

**금지:** `unit_converter/` 생성 · `UnitConverter.py` 리팩터 (GREEN 전)

---

## 12. 참고 문서 맵

```
README.md
    ├── docs/spec_analysis.md          ← AS-IS
    ├── docs/prd_test_traceability.md  ← 15 TC 추적
    ├── docs/dual_track_design.md      ← Dual Track 실행
    ├── docs/architecture.md           ← FR/NFR · 패키지
    └── .cursor/                       ← Agent Harness
            ├── rules/
            ├── skills/unit-converter-tdd/
            └── commands/
```

---

## 13. 회고 (SPEC)

| 항목 | 내용 |
|------|------|
| **달성** | Activities 1 분석 + 2~4 선행 설계·Harness까지 SPEC 범위에서 문서·규칙 일원화 |
| **결정** | Track = 레이어(A Boundary / B Domain), 실행 = B → A |
| **단순화** | TC 30 → 15로 실습 TDD 부담 조정 |
| **리스크** | RED에서 구현 유혹 → `.cursor/rules`·`/tdd-red`로 차단 |
| **다음 리스크** | GREEN 시 과도한 REFACTOR 선행 → Gate별 최소 구현 유지 |

---

*본 보고서는 SPEC 단계 종료 시점 스냅샷이다. 구현·테스트 진행 후 `Report/02_red_report.md` 등으로 이어갈 수 있다.*
