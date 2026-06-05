# Unit Converter — RED 단계 보고서 (02)

> **프로젝트:** UnitConverter_09  
> **단계:** RED (실패 테스트 선행)  
> **브랜치:** `red`  
> **작성 일자:** 2026-06-05  
> **기준:** `docs/prd_test_traceability.md` · `docs/dual_track_design.md` · `.cursor/commands/tdd-red.md`

---

## 1. RED 단계 목표

| 항목 | 내용 |
|------|------|
| **목표** | Phase 1 Core **10 TC**에 대해 `tests/`만 추가하고, 전 TC가 **의도적 FAIL** 상태임을 증명 |
| **범위** | `tests/test_domain.py` · `tests/test_boundary.py` — **프로덕션·`unit_converter/` 미작성** |
| **다음 단계** | GREEN — Track B(Domain) 선행 Green → Track A(Boundary) 통합 → **Gate 1** |

---

## 2. 작성한 Test ID (Phase 1 Core — 10/10)

| Test ID | 함수 | Given → Then (RED 메시지 요약) | REQ | Phase |
|---------|------|-------------------------------|-----|-------|
| **D-CNV-01** | `test_d_cnv_01_to_meter_feet` | 1 feet → 0.3048 m (±ε) | REQ-BIZ-01, REQ-FUNC-03 | 1 |
| **D-CNV-02** | `test_d_cnv_02_convert_all_feet` | 2.5 m → 8.20210 ft (소수 5자리) | REQ-BIZ-01, REQ-FUNC-02 | 1 |
| **D-CNV-03** | `test_d_cnv_03_feet_yard_consistency` | feet → yard, meter 경유 일관성 | REQ-BIZ-03 | 1 |
| **D-CNV-04** | `test_d_cnv_04_convert_all_yard` | 2.5 m → 2.73403 yard (소수 5자리) | REQ-BIZ-02, REQ-FUNC-02 | 1 |
| **U-IN-01** | `test_u_in_01_empty_input` | `""` → Format error message | REQ-VAL-02 | 1 |
| **U-IN-02** | `test_u_in_02_no_colon` | `meter` → Format error (콜론 없음) | REQ-VAL-02 | 1 |
| **U-IN-03** | `test_u_in_03_reject_negative` | `meter:-1` → Reject negative values | REQ-VAL-01 | 1 |
| **U-IN-04** | `test_u_in_04_unknown_unit` | `mile:1` → Unknown unit error | REQ-VAL-03 | 1 |
| **U-IN-05** | `test_u_in_05_empty_token` | `:2.5` / `meter:` → Format error (빈 토큰) | REQ-VAL-02 | 1 |
| **U-OUT-01** | `test_u_out_01_meter_stdout` | `meter:2.5` → stdout 2줄(feet·yard, README 형식·소수 1자리); meter 줄 없음 | REQ-FUNC-01, REQ-FUNC-02 | 1 |

**미작성 (Phase 2 — Extension, 5 TC):** D-CFG-01, D-CFG-02, D-REG-01, D-REG-02, U-FMT-01

---

## 3. Track B — Domain / Logic

| 항목 | 내용 |
|------|------|
| **파일** | `tests/test_domain.py` |
| **TC 수** | 4 (`D-CNV-01` ~ `D-CNV-04`) |
| **레이어** | 변환 계산 (`to_meter`, `convert_all`) |
| **RED 특징** | Given 숫자·단위 → Then 값(±ε / 소수 5자리) — **mock-free** |
| **실행 순서** | RED·GREEN 모두 **Track A보다 선행** |

### 3.1 Test ID 상세

| Test ID | When (주석, GREEN 시 구현 대상) | Then |
|---------|--------------------------------|------|
| D-CNV-01 | `to_meter("feet", 1)` | 0.3048 m (±ε) |
| D-CNV-02 | `convert_all("meter", 2.5)` | feet = 8.20210 (5자리) |
| D-CNV-03 | `convert_all("feet", 1)` | yard = meter 경유 결과와 일치 |
| D-CNV-04 | `convert_all("meter", 2.5)` | yard = 2.73403 (5자리) |

**정밀도 SSOT:** Domain `D-CNV-*`는 비율·산술 검증용 **소수 5자리** (CLI 표시 1자리와 분리).

---

## 4. Track A — UI / Boundary

| 항목 | 내용 |
|------|------|
| **파일** | `tests/test_boundary.py` |
| **TC 수** | 6 (`U-IN-01` ~ `U-IN-05`, `U-OUT-01`) |
| **레이어** | 입력 파싱·검증·CLI stdout |
| **RED 특징** | Given 문자열 → Then 메시지/줄 수·형식 |
| **실행 순서** | Domain GREEN 후 Boundary 통합 (RED 작성은 U-IN → U-OUT 순) |

### 4.1 Test ID 상세

| Test ID | Given | Then |
|---------|-------|------|
| U-IN-01 | `""` | Format error message |
| U-IN-02 | `meter` | Format error (콜론 없음) |
| U-IN-03 | `meter:-1` | Reject negative values |
| U-IN-04 | `mile:1` | Unknown unit error |
| U-IN-05 | `:2.5` or `meter:` | Format error (빈 토큰) |
| U-OUT-01 | `meter:2.5` | stdout **2줄** (`feet`·`yard`, README `2.5 meter = …`, 소수 **1자리**); meter 단독/자기변환 줄 없음 |

**표시 SSOT:** `U-OUT-01`·FR-02 — README 예: `8.2 feet`, `2.7 yard` (소수 1자리).

---

## 5. RED 원칙 준수 여부

Agent SSOT: `.cursor/rules/unit-converter-red.mdc` · `.cursor/commands/tdd-red.md`

| 규칙 | 요구 | 준수 |
|------|------|------|
| RED 단계 구현 코드 금지 | `unit_converter/` · `config/` 생성·수정 없음 | ✅ |
| 레거시 리팩터 금지 | `UnitConverter.py` 미수정 (37줄 유지) | ✅ |
| `pytest.fail("RED: …")` 허용 | 10/10 TC Then에만 `pytest.fail` | ✅ |
| `skip` / `xfail` 금지 | 사용 없음 | ✅ |
| 통과용 assert·더미 없음 | assert 본문 없음 | ✅ |
| Track B `@patch` 금지 | Domain 테스트 mock 없음 | ✅ |
| `tests/`만 수정 | 테스트 파일 2개만 추가 | ✅ |
| 1 RED 묶음 = 1 커밋 | 3 커밋으로 10 TC 분리 | ✅ |
| AAA 주석 | Given / When / Then 주석 전 TC | ✅ |

### 5.1 pytest 검증 (2026-06-05)

```bash
python -m pytest tests/ -q --tb=line
```

| 항목 | 결과 |
|------|------|
| 수집 | 10 tests |
| 결과 | **10 failed**, 0 passed |
| exit code | `1` (≠ 0 — RED 성공 기준 충족) |
| 수집/Import 오류 | 없음 |

### 5.2 실패 원인 분류

| 원인 | 건수 | 비고 |
|------|------|------|
| **`pytest.fail("RED: …")`** | **10 / 10** | 전 TC 의도적 FAIL |
| **미구현 함수** (`ImportError`, `NameError` 등) | **0 / 10** | `to_meter` / `convert_all` 등은 **주석에만** 기술, 본문 미호출 |

> GREEN 단계에서 `pytest.fail`을 assert로 교체하면 미구현 호출·assert 실패가 나타날 수 있음. 현재 RED는 **실패 원인이 100% `pytest.fail`** 임.

### 5.3 Gate 1 RED 체크 (Phase 1)

| # | 항목 | 상태 |
|---|------|------|
| 1 | Phase 1 Core 10 TC RED 작성 | ✅ |
| 2 | 전 TC FAIL (exit ≠ 0) | ✅ |
| 3 | FAIL 메시지에 Test ID 포함 | ✅ |
| 4 | Phase 2 TC 미작성 (의도) | ✅ — Extension은 별도 RED 묶음 |

---

## 6. 테스트 파일 구조

```
tests/
├── test_domain.py      # Track B — D-CNV-01 ~ 04
└── test_boundary.py    # Track A — U-IN-01 ~ 05, U-OUT-01
```

| Track | 파일 | import | 비고 |
|-------|------|--------|------|
| B | `test_domain.py` | `pytest` only | Domain 로직 import 없음 |
| A | `test_boundary.py` | `pytest` only | CLI/Validator import 없음 |

---

## 7. Git 이력 (RED 커밋)

| 커밋 | 메시지 | 파일 |
|------|--------|------|
| `907edf6` | `[RED] D-CNV-01~04 domain to_meter and convert_all` | `tests/test_domain.py` |
| `0cb3a50` | `[RED] U-IN-01~05 boundary input validation` | `tests/test_boundary.py` |
| `fe0ca76` | `[RED] U-OUT-01 meter:2.5 CLI stdout two lines` | `tests/test_boundary.py` |

**브랜치:** `red` (기준: `spec` 이후 3 RED 커밋)  
**분기 기준 커밋:** `b5f56a3` `[SPEC] Fix precision SSOT and U-OUT-01 output Then`

---

## 8. RED 실행 순서 (완료)

```
Phase 1 — Core RED (완료)
─────────────────────────
Track B:  D-CNV-01 → D-CNV-02 → D-CNV-03 → D-CNV-04  ✅
Track A:  U-IN-01 → U-IN-02 → U-IN-03 → U-IN-04 → U-IN-05 → U-OUT-01  ✅
```

**원칙:** Track = 레이어(A Boundary / B Domain). **실행·GREEN 순서 = B → A.**

---

## 9. 다음 GREEN 계획

### 9.1 Gate 1 목표 (Phase 1 Core Green)

| 항목 | 기준 (`dual_track_design.md` §6) |
|------|----------------------------------|
| TC | D-CNV-01~04, U-IN-01~05, U-OUT-01 **전부 Green** |
| 기능 | `meter:2.5` → feet·yard 2줄 출력 (README 형식, 소수 1자리) |
| 검증 | 음수·형식·unknown unit 거부 |
| 아키텍처 | Parser / Validator / Converter 분리 시작 (최소 구현) |

### 9.2 권장 GREEN 순서

| 순서 | Test ID | 작업 | 구현 위치 (최소) |
|------|---------|------|------------------|
| 1 | D-CNV-01 | `pytest.fail` → assert, `to_meter` | `UnitConverter.py` 또는 임시 `converter` 모듈 |
| 2 | D-CNV-02 | `convert_all` — feet 출력 (5자리) | 동일 |
| 3 | D-CNV-03 | feet → yard meter 경유 일관성 | 동일 |
| 4 | D-CNV-04 | meter → yard (5자리) | 동일 |
| 5 | U-IN-01 ~ 05 | Validator/Parser — 형식·음수·unknown | `UnitConverter.py` 또는 `validator` |
| 6 | U-OUT-01 | CLI 통합 — 2줄 stdout, 입력 단위 제외 | `UnitConverter.py` `main()` |

**원칙:** Track B **4 TC Green 완료 후** Track A U-IN → U-OUT 통합.  
**커밋:** `[GREEN] …` — RED와 동일하게 논리 묶음 단위 권장.

### 9.3 GREEN 시 테스트 전환

| RED | GREEN |
|-----|-------|
| `pytest.fail("RED: {ID} — …")` | `assert` / `pytest.approx` / `capsys` 등 실제 검증 |
| When 주석의 API | `to_meter`, `convert_all`, `parse`, `validate`, CLI 실행 |

**정밀도:** Domain assert는 **5자리**; `U-OUT-01`은 stdout **1자리** 반올림.

### 9.4 GREEN 금지·주의 (SPEC/RED 규칙 계승)

| 금지 | 이유 |
|------|------|
| Gate 1 전 REFACTOR (`unit_converter/` 풀 패키지) | GREEN = 최소 구현 우선 |
| `UnitConverter.py` 대규모 리팩터 선행 | Gate 1 통과 후 REFACTOR |
| Track B Domain `@patch` | mock-free 유지 |

### 9.5 Gate 1 이후 — Phase 2 (별도 RED → GREEN)

| 순서 | RED (미작성) | GREEN 목표 |
|------|--------------|------------|
| 1 | D-CFG-01, D-CFG-02 | JSON 설정 로드 |
| 2 | D-REG-01, D-REG-02 | cubit 동적 등록 |
| 3 | U-FMT-01 | JSON 출력 포맷 |
| — | **Gate 2** | 15/15 Green, Converter 본체 수정 없이 OCP 입증 |

---

## 10. Phase 1 커버리지 요약

| Phase | Track A | Track B | TC | RED | GREEN |
|-------|---------|---------|-----|-----|-------|
| 1 Core | 6 | 4 | 10 | ✅ 10/10 | ❌ 0/10 |
| 2 Extension | 1 | 4 | 5 | ❌ 0/5 | ❌ 0/5 |
| **합계** | **7** | **8** | **15** | **10/15** | **0/15** |

---

## 11. 참고 문서 맵

```
Report/01_spec_report.md          ← SPEC 종료 스냅샷
Report/02_red_report.md           ← 본 문서 (RED 종료)
docs/prd_test_traceability.md     ← REQ ↔ Test ID
docs/dual_track_design.md         ← Gate 1/2 · 실행 순서
.cursor/commands/tdd-red.md       ← RED Command
.cursor/skills/unit-converter-tdd/reference.md
tests/test_domain.py · test_boundary.py
```

---

## 12. 회고 (RED)

| 항목 | 내용 |
|------|------|
| **달성** | Phase 1 Core 10 TC RED 완료, 전 TC `pytest.fail` 기반 FAIL 검증 |
| **결정** | 실패 원인을 `pytest.fail`로만 유지 — GREEN 전 Import/미구현 혼선 방지 |
| **커밋** | Domain / U-IN / U-OUT 3묶음 — 1 RED 묶음 = 1 커밋 준수 |
| **다음** | GREEN Track B 선행 → Boundary 통합 → Gate 1 |
| **리스크** | GREEN 시 레거시 3줄 출력( meter 포함)과 U-OUT-01 불일치 — FR-02「다른 단위」만 출력하도록 수정 필요 |

---

*본 보고서는 RED 단계 종료(Phase 1 Core) 시점 스냅샷이다. GREEN 진행 후 `Report/03_green_report.md` 등으로 이어갈 수 있다.*
