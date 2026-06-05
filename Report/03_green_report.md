# Unit Converter — GREEN 단계 보고서 (03)

> **프로젝트:** UnitConverter_09  
> **단계:** GREEN (최소 구현) + Golden Master (REFACTOR 전)  
> **브랜치:** `green`  
> **작성 일자:** 2026-06-05  
> **기준:** `docs/prd_test_traceability.md` · `docs/dual_track_design.md` · `.cursor/commands/tdd-green.md`

---

## 1. GREEN 단계 목표

| 항목 | 내용 |
|------|------|
| **목표** | Phase 1 Core **10 TC** `pytest.fail` → assert, **최소 구현**으로 Green |
| **범위** | `converter.py` · `validator.py` · `UnitConverter.py` · `tests/` — **`unit_converter/` 패키지 REFACTOR 전** |
| **Gate 1** | D-CNV-01~04 + U-IN-01~05 + U-OUT-01 **전부 Green** |
| **다음 단계** | REFACTOR — `docs/architecture.md` 패키지 구조 이전 (Golden Master 회귀 유지) |

---

## 2. Green 완료 Test ID (Phase 1 Core — 10/10)

| Test ID | 함수 | Given → Then | REQ | Green 커밋 |
|---------|------|--------------|-----|------------|
| **D-CNV-01** | `test_d_cnv_01_to_meter_feet` | 1 feet → 0.3048 m (±ε) | REQ-BIZ-01, REQ-FUNC-03 | `485a685` |
| **D-CNV-02** | `test_d_cnv_02_convert_all_feet` | 2.5 m → 8.20210 ft (5자리) | REQ-BIZ-01, REQ-FUNC-02 | `79e8592` |
| **D-CNV-03** | `test_d_cnv_03_feet_yard_consistency` | feet → yard, meter 경유 일관 | REQ-BIZ-03 | `60248dc` |
| **D-CNV-04** | `test_d_cnv_04_convert_all_yard` | 2.5 m → 2.73403 yard (5자리) | REQ-BIZ-02, REQ-FUNC-02 | `7353791` |
| **U-IN-01** | `test_u_in_01_empty_input` | `""` → Format error | REQ-VAL-02 | `4650ee6` |
| **U-IN-02** | `test_u_in_02_no_colon` | `meter` → Format error | REQ-VAL-02 | `c5250c7` |
| **U-IN-03** | `test_u_in_03_reject_negative` | `meter:-1` → Negative 거부 | REQ-VAL-01 | `aac8d71` |
| **U-IN-04** | `test_u_in_04_unknown_unit` | `mile:1` → Unknown unit | REQ-VAL-03 | `15f3471` |
| **U-IN-05** | `test_u_in_05_empty_token` | `:2.5` / `meter:` → Format error | REQ-VAL-02 | `03ffff0` |
| **U-OUT-01** | `test_u_out_01_meter_stdout` | `meter:2.5` → stdout 2줄(feet·yard, 1자리) | REQ-FUNC-01, REQ-FUNC-02 | `f7875d5` |

**미구현 (Phase 2 — Extension, 5 TC):** D-CFG-01, D-CFG-02, D-REG-01, D-REG-02, U-FMT-01

---

## 3. Track B — Domain / Logic (4/4 Green)

| 항목 | 내용 |
|------|------|
| **파일** | `tests/test_domain.py` · `converter.py` |
| **TC 수** | 4 (`D-CNV-01` ~ `D-CNV-04`) |
| **레이어** | `to_meter()`, `convert_all()` — **mock-free** |
| **실행 순서** | GREEN **Track A보다 선행** (B → A) |

### 3.1 구현 진화

| Test ID | 추가·변경 API | 핵심 구현 |
|---------|---------------|-----------|
| D-CNV-01 | `to_meter("feet", value)` | `value / 3.28084` |
| D-CNV-02 | `convert_all("meter", value)` | `{"feet": round(×3.28084, 5)}` |
| D-CNV-03 | meter 허브 패턴 | `to_meter` → 전 단위 변환, 입력 단위 제외 |
| D-CNV-04 | `Decimal` + `ROUND_HALF_UP` | `2.734025` → `2.73403` (banker's rounding 회피) |

### 3.2 Domain 정밀도 SSOT

| 항목 | 값 |
|------|-----|
| 비율 | `METER_TO_FEET = 3.28084`, `METER_TO_YARD = 1.09361` |
| 내부 반올림 | 소수 **5자리**, half-up (`Decimal`) |
| `to_meter` 지원 | `meter`, `feet` (yard 입력은 Phase 1 GREEN 미지원) |

---

## 4. Track A — UI / Boundary (7/7 Green)

| 항목 | 내용 |
|------|------|
| **파일** | `tests/test_boundary.py` · `validator.py` · `UnitConverter.py` |
| **TC 수** | 6 함수 / **7 pytest 항목** (U-IN-05 parametrize 2건) |
| **레이어** | 입력 검증 · CLI 출력 |
| **실행 순서** | Domain 4 TC Green 후 U-IN → U-OUT |

### 4.1 Validator (`validator.py`)

| Test ID | 검증 규칙 | 오류 메시지 |
|---------|-----------|-------------|
| U-IN-01 | 빈 문자열 | `Invalid format. Use unit:value (ex: meter:2.5)` |
| U-IN-02 | `:` 없음 | 동일 (FORMAT_ERROR) |
| U-IN-03 | `value < 0` | `Negative values are not allowed` |
| U-IN-04 | unit ∉ {meter, feet, yard} | `Unknown unit: {unit}` |
| U-IN-05 | 빈 unit 또는 빈 value | FORMAT_ERROR |

**검증 순서:** 빈 입력 → 콜론 → 빈 토큰 → float 파싱 → 음수 → unknown unit

### 4.2 U-IN-05 RED 리뷰 반영

RED 단계 리뷰: **「GREEN 시 `:2.5` / `meter:` 분리 검토」**

| RED | GREEN |
|-----|-------|
| 단일 테스트, Given에 `or` | `@pytest.mark.parametrize` — `empty_unit` / `empty_value` id 분리 |
| 1 pytest 항목 | 2 pytest 항목 (실패 추적 개선) |

### 4.3 CLI (`UnitConverter.py`)

| Test ID | API | 출력 |
|---------|-----|------|
| U-OUT-01 | `process("meter:2.5")` | `2.5 meter = 8.2 feet` · `2.5 meter = 2.7 yard` |

| 변경 | RED(레거시) | GREEN |
|------|-------------|-------|
| 출력 줄 수 | 3줄 (meter·feet·yard) | **2줄** (feet·yard만, FR-02) |
| 표시 정밀도 | float 전체 | **소수 1자리** (README SSOT) |
| 구조 | `main()` 단일 함수 | `process()` + `main()` (테스트 가능) |

---

## 5. GREEN 원칙 준수 여부

Agent SSOT: `.cursor/commands/tdd-green.md` · `.cursor/skills/unit-converter-tdd/SKILL.md`

| 규칙 | 요구 | 준수 |
|------|------|------|
| TC별 최소 구현 | 과도한 REFACTOR 금지 | ✅ |
| `unit_converter/` 풀 패키지 금지 | GREEN = 임시 모듈 | ✅ |
| Track B `@patch` 금지 | Domain mock-free | ✅ |
| `pytest.fail` → assert | 10/10 TC 전환 | ✅ |
| Track B 선행 | D-CNV → U-IN → U-OUT | ✅ |
| TC별 커밋 | 10 GREEN + 1 Golden Master | ✅ (11커밋) |

### 5.1 pytest 검증 (2026-06-05)

```bash
python -m pytest tests/ -v
```

| 항목 | 결과 |
|------|------|
| Phase 1 Core | **11 passed** (U-IN-05 parametrize 포함) |
| Golden Master | **18 passed** |
| **합계** | **29 passed**, 0 failed |
| exit code | `0` |

### 5.2 Gate 1 체크 (Phase 1)

| # | 항목 | 상태 |
|---|------|------|
| 1 | Phase 1 Core 10 TC Green | ✅ |
| 2 | `meter:2.5` → feet·yard 2줄 (README, 1자리) | ✅ |
| 3 | 음수·형식·unknown unit 거부 | ✅ |
| 4 | Domain meter 경유 변환 | ✅ |
| 5 | Golden Master (REFACTOR 전) | ✅ |

---

## 6. 구현 파일 구조 (GREEN 시점)

```
UnitConverter_09/
├── UnitConverter.py      # process(), main() — CLI 진입점
├── converter.py          # to_meter(), convert_all() — Domain (임시)
├── validator.py          # validate(), ValidationError — Boundary (임시)
└── tests/
    ├── test_domain.py         # Track B — 4 TC
    ├── test_boundary.py       # Track A — 6함수 / 7항목
    └── test_golden_master.py  # REFACTOR 회귀 스냅샷 — 18 TC
```

> REFACTOR 목표: `unit_converter/domain/converter.py`, `application/validator.py` 등으로 이전. Golden Master가 동작 고정.

---

## 7. Git 이력 (GREEN 커밋)

| 커밋 | 메시지 | Test ID / 범위 |
|------|--------|----------------|
| `485a685` | `[GREEN] D-CNV-01 to_meter feet to meter` | D-CNV-01 |
| `79e8592` | `[GREEN] D-CNV-02 convert_all meter to feet` | D-CNV-02 |
| `60248dc` | `[GREEN] D-CNV-03 convert_all feet-yard via meter` | D-CNV-03 |
| `7353791` | `[GREEN] D-CNV-04 convert_all meter to yard` | D-CNV-04 |
| `4650ee6` | `[GREEN] U-IN-01 empty input format error` | U-IN-01 |
| `c5250c7` | `[GREEN] U-IN-02 missing colon format error` | U-IN-02 |
| `aac8d71` | `[GREEN] U-IN-03 reject negative input values` | U-IN-03 |
| `15f3471` | `[GREEN] U-IN-04 unknown unit error` | U-IN-04 |
| `03ffff0` | `[GREEN] U-IN-05 empty token format error split cases` | U-IN-05 |
| `f7875d5` | `[GREEN] U-OUT-01 meter:2.5 CLI stdout two lines` | U-OUT-01 |
| `8d67062` | `Add golden master tests for Phase 1 refactor regression guard` | Golden Master |

**브랜치:** `green`  
**분기 기준:** RED 종료 `bc1f2e5` · SPEC `b5f56a3`

---

## 8. GREEN 실행 순서 (완료)

```
Phase 1 — Core GREEN (완료)
────────────────────────────
Track B:  D-CNV-01 → D-CNV-02 → D-CNV-03 → D-CNV-04  ✅
Track A:  U-IN-01 → U-IN-02 → U-IN-03 → U-IN-04 → U-IN-05 → U-OUT-01  ✅
Golden Master:  tests/test_golden_master.py  ✅
Gate 1:  Phase 1 Core 10/10 Green  ✅
```

---

## 9. Golden Master (REFACTOR 전)

| 항목 | 내용 |
|------|------|
| **파일** | `tests/test_golden_master.py` |
| **목적** | CLI 출력 · Domain 변환 · 검증 메시지 **스냅샷 고정** — REFACTOR 회귀 방지 |
| **TC 수** | 18 (parametrize 포함) |
| **기능 변경** | 없음 (관찰·고정만) |

### 9.1 스냅샷 범위

| 섹션 | 고정 대상 |
|------|-----------|
| `CLI_PROCESS_GOLDEN` | `process()` 4입력 |
| `test_golden_cli_main_*` | `main()` stdout 2건 |
| `CONVERT_ALL_GOLDEN` | Domain 5자리 4건 |
| `TO_METER_GOLDEN` | `to_meter` 2건 |
| `VALIDATION_ERROR_GOLDEN` | 검증 메시지 6건 |

---

## 10. 다음 REFACTOR 계획

| 순서 | 작업 | 기준 |
|------|------|------|
| 1 | `unit_converter/` 패키지 생성 | `docs/architecture.md` §3~4 |
| 2 | `converter.py` → `domain/converter.py` | OCP/SRP |
| 3 | `validator.py` → `application/validator.py` | Boundary 분리 |
| 4 | `UnitConverter.py` → 얇은 `main()` | `ConversionService` 호출 |
| 5 | **회귀** | Phase 1 11 TC + Golden Master 18 TC **Green 유지** |

### 10.1 Phase 2 (Gate 1 이후, 별도 RED → GREEN)

| 순서 | Test ID | 목표 |
|------|---------|------|
| 1 | D-CFG-01, D-CFG-02 | JSON 설정 로드 |
| 2 | D-REG-01, D-REG-02 | cubit 동적 등록 |
| 3 | U-FMT-01 | JSON 출력 포맷 |
| — | **Gate 2** | 15/15 Green |

---

## 11. Phase 1 커버리지 요약

| Phase | Track A | Track B | TC | RED | GREEN | Golden |
|-------|---------|---------|-----|-----|-------|--------|
| 1 Core | 6 | 4 | 10 | ✅ 10/10 | ✅ 10/10 | ✅ 18 snapshot |
| 2 Extension | 1 | 4 | 5 | ❌ 0/5 | ❌ 0/5 | — |
| **합계** | **7** | **8** | **15** | **10/15** | **10/15** | — |

---

## 12. 참고 문서 맵

```
Report/01_spec_report.md          ← SPEC 종료
Report/02_red_report.md           ← RED 종료
Report/03_green_report.md         ← 본 문서 (GREEN + Gate 1)
Prompting/03_green_transcript.md  ← GREEN Export Transcript
docs/architecture.md              ← REFACTOR 목표 패키지
docs/dual_track_design.md         ← Gate 1/2
tests/test_golden_master.py       ← REFACTOR 회귀 가드
```

---

## 13. 회고 (GREEN)

| 항목 | 내용 |
|------|------|
| **달성** | Phase 1 Core 10 TC Green, Gate 1 통과, Golden Master 18 TC 추가 |
| **결정** | GREEN = 루트 임시 모듈(`converter.py`, `validator.py`); REFACTOR에서 패키지 이전 |
| **커밋** | TC별 1커밋 × 10 + Golden Master 1커밋 |
| **이슈** | D-CNV-04: Python `round()` banker's rounding → `Decimal` half-up 도입 |
| **리뷰 반영** | U-IN-05 `:2.5` / `meter:` parametrize 분리 |
| **다음** | REFACTOR — Golden Master Green 유지하며 `unit_converter/` 이전 |

---

*본 보고서는 GREEN 단계 종료(Gate 1 + Golden Master) 시점 스냅샷이다. REFACTOR 진행 후 `Report/04_refactor_report.md` 등으로 이어갈 수 있다.*
