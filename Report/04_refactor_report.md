# Unit Converter — REFACTOR 단계 보고서 (04)

> **프로젝트:** UnitConverter_09  
> **단계:** REFACTOR (패키지 구조 이전) — **Gate 1 완료**  
> **브랜치:** `refactor` (기준: `green` @ `b135cc8`)  
> **작성 일자:** 2026-06-05  
> **기준:** `docs/architecture.md` · `docs/refactor_plan.md` · `docs/prd_test_traceability.md`

---

## 1. REFACTOR 단계 목표

| 항목 | 내용 |
|------|------|
| **목표** | GREEN 루트 모듈 → `unit_converter/` 패키지로 OCP/SRP 레이어 분리 |
| **범위 (Gate 1)** | Step 0~3 — `domain/` + `application/` + 얇은 CLI |
| **회귀 가드** | Golden Master 18 TC + Phase 1 Core 11 TC **전부 Green 유지** |
| **Gate 1** | Phase 1 TC 10 + Golden Master + `python UnitConverter.py` ✅ |
| **다음 단계** | Step 4~6 — `config/` · `infrastructure/` · Formatter Strategy (Gate 2) |

---

## 2. AS-IS vs TO-BE 비교

### 2.1 구조 변화

| | GREEN (AS-IS) | REFACTOR (TO-BE, Gate 1) |
|---|---|---|
| **구조** | 루트 3파일 평면 import | `unit_converter/` 패키지 (2 레이어) |
| **변환** | `converter.py` 함수 + 하드코딩 비율 | `UnitRegistry` + `UnitConverter` 클래스 |
| **검증** | `validate()` 파싱+검증 혼합 | `InputParser` + `InputValidator` 분리 |
| **출력** | `process()` 인라인 f-string | `TableFormatter` + `ConversionService` |
| **CLI** | `process()` + `main()` | 얇은 `main()` + `process()` shim |
| **설정** | 매직 넘버 하드코딩 | `UnitRegistry.default()` (Step 4에서 JSON) |

### 2.2 레이어 의존성

```
UnitConverter.py
       │
       ▼
application/          ← Track A (Boundary)
  parser.py
  validator.py
  formatter.py
  service.py
       │
       ▼
domain/               ← Track B (Domain)
  models.py
  registry.py
  converter.py
  exceptions.py
```

**규칙:** `domain/`은 `application/`에 의존하지 않음 (NFR-02 ✅)

---

## 3. Step별 수행 내역

| Step | 작업 | 생성·변경 파일 | 커밋 |
|------|------|----------------|------|
| Plan | 리팩토링 계획 문서 | `docs/refactor_plan.md` | `37e15bd` |
| **1a** | 패키지 골격 + 값 객체 + 예외 | `domain/models.py`, `exceptions.py` | `a7d228b` |
| **1b~1c** | UnitRegistry + UnitConverter | `domain/registry.py`, `converter.py`, 루트 `converter.py` shim | `0fccc70` |
| **2a** | InputParser | `application/parser.py`, `exceptions.py` | `6e7de7c` |
| **2b** | InputValidator + shim | `application/validator.py`, 루트 `validator.py` shim | `26165e0` |
| **2c** | TableFormatter + ConversionService | `application/formatter.py`, `service.py`, `UnitConverter.py` | `23dc1dd` |
| **3** | 얇은 CLI main — **Gate 1** | `UnitConverter.py` | `0db7cc5` |

### 3.1 Golden Master 안전 전략 (Strangler Fig + Shim)

| 루트 shim | 위임 대상 | Golden Master import |
|-----------|-----------|----------------------|
| `converter.py` | `UnitConverter.to_meter`, `convert_all` | `from converter import ...` |
| `validator.py` | `InputParser` → `InputValidator` | `from validator import validate, ValidationError, ...` |
| `UnitConverter.process` | `ConversionService.run` | `from UnitConverter import process` |

**동결 항목:** `Decimal` 반올림 로직 · 5자리 수치 · 에러 메시지 문자열 · CLI 2줄 출력 형식

---

## 4. Track B — Domain / Logic

| 항목 | 내용 |
|------|------|
| **패키지** | `unit_converter/domain/` |
| **파일** | `models.py`, `exceptions.py`, `registry.py`, `converter.py` |
| **TC** | D-CNV-01~04 — **4/4 Green** (mock-free) |
| **OCP** | Converter 알고리즘 **무변경** — Registry 주입만 추가 |

### 4.1 UnitRegistry (`registry.py`)

| 단위 | ratio_to_meter | 의미 |
|------|----------------|------|
| meter | 1.0 | 기준 단위 |
| feet | 3.28084 | 1 meter = 3.28084 feet |
| yard | 1.09361 | 1 meter = 1.09361 yard |

`default()` 클래스 메서드로 3단위 기본 등록. `register()` API는 Step 5에서 확장 예정.

### 4.2 UnitConverter (`converter.py`)

| 메서드 | 동작 | GREEN 대비 |
|--------|------|------------|
| `to_meter(unit, value)` | meter/feet만 지원, yard 입력 시 `ValueError` | **동일** (Phase 1 유산) |
| `convert_all(unit, value)` | meter 경유 → 5자리 dict, 입력 단위 제외 | **동일** (Registry 비율 사용) |

---

## 5. Track A — UI / Boundary

| 항목 | 내용 |
|------|------|
| **패키지** | `unit_converter/application/` |
| **파일** | `parser.py`, `validator.py`, `formatter.py`, `service.py`, `exceptions.py` |
| **TC** | U-IN-01~05 + U-OUT-01 — **7/7 Green** |

### 5.1 책임 분리

| 클래스 | 책임 | 이전 위치 |
|--------|------|-----------|
| `InputParser` | `unit:value` → `ParsedInput` | `validate()` 전반 |
| `InputValidator` | 음수·단위 존재 검사 | `validate()` 후반 |
| `TableFormatter` | f-string 1자리 출력 | `process()` 인라인 |
| `ConversionService` | parse → validate → convert → format | `process()` 오케스트레이션 |

### 5.2 검증 메시지 (Golden Master 동일)

| 상수 / 패턴 | 메시지 |
|-------------|--------|
| `FORMAT_ERROR` | `Invalid format. Use unit:value (ex: meter:2.5)` |
| `NEGATIVE_ERROR` | `Negative values are not allowed` |
| unknown unit | `Unknown unit: {unit}` |

### 5.3 CLI (`UnitConverter.py`)

```python
def main():
    service = build_default_service()
    raw = input("Insert value for converting (ex: meter:2.5): ")
    try:
        for line in service.run(raw):
            print(line)
    except ValidationError as e:
        print(e.args[0])
```

`process()`는 `_service.run()` shim — Golden Master `test_golden_cli_process` 호환.

---

## 6. REFACTOR 원칙 준수 여부

Agent SSOT: `docs/refactor_plan.md` · `.cursor/skills/unit-converter-tdd/SKILL.md`

| 규칙 | 요구 | 준수 |
|------|------|------|
| Copy-then-delegate | 한 번에 cut 금지, shim 유지 | ✅ |
| Converter 알고리즘 동결 | Phase 2에서도 본체 무변경 | ✅ |
| Golden Master 메시지·수치 동결 | 스냅샷 변경 없음 | ✅ |
| Track B → Track A 순서 | Domain 선행, Application 후행 | ✅ |
| 1 Step = 1 커밋 | `[REFACTOR]` 말머리 | ✅ (7 Step 커밋) |
| `domain/` 독립성 | application에 의존 금지 | ✅ |

---

## 7. pytest 검증 (Gate 1)

```bash
python -m pytest tests/ -v
```

| 항목 | 결과 |
|------|------|
| Phase 1 Core (`test_domain` + `test_boundary`) | **11 passed** |
| Golden Master (`test_golden_master`) | **18 passed** |
| **합계** | **29 passed**, 0 failed |
| exit code | `0` |

### 7.1 수동 CLI 확인

```bash
echo meter:2.5 | python UnitConverter.py
```

```
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

---

## 8. Gate 1 체크리스트 (`architecture.md` §10)

| # | 항목 | FR/NFR | Gate 1 |
|---|------|--------|--------|
| 1 | `domain/`이 `application/`에 의존하지 않음 | NFR-02 | ✅ |
| 2 | Formatter 추가 시 Converter 무변경 | NFR-01 | ✅ (TableFormatter만) |
| 3 | `register("cubit", 0.4572)` 후 변환 | FR-10 | ❌ Step 5 |
| 4 | `units.json` 수정만으로 비율 반영 | FR-09, NFR-07 | ❌ Step 4 |
| 5 | Domain TC mock-free Green | NFR-06 | ✅ |
| 6 | Phase 1 TC 10 Green | FR-08 | ✅ |
| 7 | `python UnitConverter.py` 실행 유지 | NFR-08 | ✅ |
| 8 | Golden Master 18 시나리오 Green | 회귀 가드 | ✅ |

---

## 9. 구현 파일 구조 (Gate 1 시점)

```
UnitConverter_09/
├── UnitConverter.py                 # 얇은 main + process() shim
├── converter.py                     # shim → domain/converter
├── validator.py                     # shim → application/parser+validator
│
├── unit_converter/
│   ├── application/                 # Track A
│   │   ├── parser.py                # InputParser
│   │   ├── validator.py             # InputValidator
│   │   ├── formatter.py             # TableFormatter
│   │   ├── service.py               # ConversionService, build_default_service()
│   │   └── exceptions.py            # ValidationError, FORMAT_ERROR, NEGATIVE_ERROR
│   │
│   └── domain/                      # Track B
│       ├── models.py                # Unit, ParsedInput, ConversionResult
│       ├── exceptions.py            # DomainError, UnknownUnitError
│       ├── registry.py              # UnitRegistry
│       └── converter.py             # UnitConverter
│
├── docs/
│   └── refactor_plan.md             # 이전 순서 SSOT
│
└── tests/
    ├── test_domain.py               # D-CNV-* (루트 converter import)
    ├── test_boundary.py             # U-IN-*, U-OUT-01
    └── test_golden_master.py        # 회귀 스냅샷 — 18 TC
```

> 루트 `converter.py`, `validator.py` shim은 Golden Master 회귀 가드로 **유지**.

---

## 10. Git 이력 (REFACTOR 커밋)

| 커밋 | 메시지 | Step |
|------|--------|------|
| `37e15bd` | `[REFACTOR] Add refactor plan with Golden Master-safe migration order` | Plan |
| `a7d228b` | `[REFACTOR] Add domain models and exceptions skeleton` | 1a |
| `0fccc70` | `[REFACTOR] Extract UnitRegistry and UnitConverter with root shim` | 1b~1c |
| `6e7de7c` | `[REFACTOR] Add InputParser for unit:value parsing` | 2a |
| `26165e0` | `[REFACTOR] Add InputValidator and validator root shim` | 2b |
| `23dc1dd` | `[REFACTOR] Add TableFormatter and ConversionService` | 2c |
| `0db7cc5` | `[REFACTOR] Thin CLI main — Gate 1 Phase 1 Green` | 3 |

**브랜치:** `refactor`  
**분기 기준:** GREEN 종료 `b135cc8` · Golden Master `8d67062`

---

## 11. REFACTOR 실행 순서 (Gate 1 완료)

```
REFACTOR — Gate 1 (완료)
────────────────────────
Plan:     docs/refactor_plan.md                              ✅
Step 1:   domain/ (models → registry → converter) + shim     ✅
Step 2:   application/ (parser → validator → service)    ✅
Step 3:   얇은 CLI main                                      ✅
Gate 1:   29 passed + CLI 수동 확인                          ✅

REFACTOR — Gate 2 (미완)
────────────────────────
Step 4:   config/units.json + JsonConfigLoader               ❌
Step 5:   UnitRegistry.register() 확장                       ❌
Step 6:   OutputFormatter Strategy (JSON/CSV/Table)        ❌
Gate 2:   Phase 2 TC 5 + 회귀 29 Green                     ❌
```

---

## 12. Phase 2 미완료 (Gate 2 대상)

| Test ID | Track | 목표 모듈 | Phase |
|---------|-------|-----------|-------|
| D-CFG-01 | B | `infrastructure/config_loader.py` | 2 |
| D-CFG-02 | B | `config/units.json` 로드 | 2 |
| D-REG-01 | B | `UnitRegistry.register()` | 2 |
| D-REG-02 | B | cubit 상호 변환 | 2 |
| U-FMT-01 | A | `OutputFormatter` JSON Strategy | 2 |

---

## 13. Phase 1 커버리지 요약

| Phase | Track A | Track B | TC | GREEN | REFACTOR (Gate 1) | Golden |
|-------|---------|---------|-----|-------|-------------------|--------|
| 1 Core | 6 | 4 | 10 | ✅ 10/10 | ✅ 10/10 | ✅ 18 snapshot |
| 2 Extension | 1 | 4 | 5 | ❌ 0/5 | ❌ 0/5 | — |
| **합계** | **7** | **8** | **15** | **10/15** | **10/15** | ✅ |

---

## 14. FR/NFR 매핑 (REFACTOR 후)

| 모듈 | FR | NFR | Gate |
|------|-----|-----|------|
| `domain/converter.py` | FR-02, FR-05~07 | NFR-01 (닫힘), NFR-06 | 1 ✅ |
| `domain/registry.py` | FR-03 | NFR-01 (확장 지점) | 1 ✅ / 2 ❌ |
| `application/parser.py` | FR-01 | NFR-04, NFR-02 | 1 ✅ |
| `application/validator.py` | — | NFR-03~05 | 1 ✅ |
| `application/formatter.py` | FR-02 (표시) | NFR-01 | 1 ✅ (Table만) |
| `application/service.py` | FR-02 | NFR-02, NFR-08 | 1 ✅ |
| `infrastructure/config_loader.py` | FR-09 | NFR-07 | 2 ❌ |
| `UnitConverter.py` | — | NFR-08 | 1 ✅ |

---

## 15. 알려진 제한사항 (Phase 1 유산)

| 항목 | 내용 |
|------|------|
| `to_meter` yard 미지원 | GREEN부터 `meter`/`feet`만 — yard 입력 시 `ValueError` (validator는 yard 허용) |
| Registry 이중 인스턴스 | shim마다 `UnitRegistry.default()` 별도 생성 — Phase 2에서 DI 통합 가능 |
| Formatter Strategy | `TableFormatter`만 — JSON/CSV는 Step 6 |
| 테스트 import | `test_domain.py` 등 루트 shim 경유 — 패키지 직접 import 전환은 선택 작업 |

---

## 16. 참고 문서 맵

```
Report/01_spec_report.md           ← SPEC 종료
Report/02_red_report.md            ← RED 종료
Report/03_green_report.md          ← GREEN + Gate 1 (GREEN 시점)
Report/04_refactor_report.md       ← 본 문서 (REFACTOR Gate 1)
Prompting/04_refactor_transcript.md ← REFACTOR Export Transcript
docs/refactor_plan.md              ← 이전 순서·shim 전략 SSOT
docs/architecture.md               ← TO-BE 패키지 · FR/NFR
tests/test_golden_master.py        ← 회귀 가드
```

---

## 17. 회고 (REFACTOR Gate 1)

| 항목 | 내용 |
|------|------|
| **달성** | `unit_converter/` 2레이어 구축, Gate 1 통과, Golden Master 29 TC Green 유지 |
| **전략** | Strangler Fig + 루트 shim — 테스트 import 변경 없이 패키지 이전 |
| **커밋** | Plan 1 + Step 7 = **8커밋** (`[REFACTOR]`) |
| **결정** | Converter 알고리즘·메시지·수치 **동결** — 회귀 0건 |
| **다음** | Step 4~6 — `config/units.json`, `register()`, Formatter Strategy → Gate 2 |

---

*본 보고서는 REFACTOR Gate 1(Step 0~3) 완료 시점 스냅샷이다. Gate 2(Phase 2 Extension) 완료 후 본 문서 §12·§13을 갱신할 수 있다.*
