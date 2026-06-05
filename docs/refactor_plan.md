# Refactor Plan — AS-IS vs TO-BE 비교 및 안전한 이전 순서

> **기준 문서:** `docs/architecture.md`  
> **브랜치:** `refactor` (기준: `green` @ GREEN 완료)  
> **작성 일자:** 2026-06-05  
> **회귀 가드:** `tests/test_golden_master.py` (15 TC + Golden Master)

---

## 1. 문서 목적

GREEN 단계에서 동작하는 **루트 모듈 구조**를 `docs/architecture.md`의 **목표 패키지 구조**로 이전한다.  
모든 단계에서 **Golden Master + 15 TC Green**을 유지하는 것이 최우선이다.

---

## 2. AS-IS (현재) vs TO-BE (목표) 비교

### 2.1 디렉터리 구조

#### AS-IS — GREEN 완료 후

```
UnitConverter_09/
│
├── UnitConverter.py          # CLI main + process() 오케스트레이션 (31줄)
├── converter.py                # to_meter, convert_all (루트 모듈, 하드코딩 비율)
├── validator.py                # validate() — 파싱+검증 혼합 (루트 모듈)
│
└── tests/
    ├── test_domain.py          # D-CNV-01~04  → converter import
    ├── test_boundary.py        # U-IN-01~05, U-OUT-01 → validator, UnitConverter import
    └── test_golden_master.py   # 회귀 스냅샷 (루트 API 고정)
```

#### TO-BE — `docs/architecture.md` §3

```
UnitConverter_09/
│
├── UnitConverter.py                 # CLI 진입점만 (얇은 main)
│
├── unit_converter/                  # 메인 패키지
│   ├── application/                 # Track A — Boundary
│   │   ├── parser.py                # InputParser
│   │   ├── validator.py             # InputValidator
│   │   ├── formatter.py             # OutputFormatter (Strategy)
│   │   └── service.py               # ConversionService
│   │
│   ├── domain/                      # Track B — Domain
│   │   ├── models.py                # Unit, ParsedInput, ConversionResult
│   │   ├── converter.py             # UnitConverter (변환만)
│   │   ├── registry.py              # UnitRegistry
│   │   └── exceptions.py            # DomainError, UnknownUnitError, ...
│   │
│   └── infrastructure/              # Track B — 외부 연동 (Phase 2)
│       └── config_loader.py         # JsonConfigLoader
│
├── config/
│   └── units.json                   # 기본 3단위 비율 (Phase 2)
│
└── tests/
    ├── test_domain.py
    ├── test_boundary.py
    └── test_golden_master.py
```

### 2.2 모듈·책임 매핑

| AS-IS (루트) | TO-BE (패키지) | Gap | Phase |
|--------------|----------------|-----|-------|
| `converter.METER_TO_*` 상수 | `domain/registry.py` + `config/units.json` | 비율 하드코딩, Registry 없음 | 1→2 |
| `converter.to_meter()` | `domain/converter.py` `UnitConverter.to_meter()` | 함수형 → 클래스+Registry 주입 | 1 |
| `converter.convert_all()` | `domain/converter.py` `UnitConverter.convert_all()` | 동일 | 1 |
| `validator.validate()` (파싱+검증) | `application/parser.py` + `application/validator.py` | SRP 미분리 | 1 |
| `validator.KNOWN_UNITS` | `domain/registry.py` `UnitRegistry` | 단위 목록 이중 관리 | 1 |
| `UnitConverter.process()` | `application/service.py` + `application/formatter.py` | 포맷 Strategy 없음 | 1→2 |
| `UnitConverter.main()` | `UnitConverter.py` (얇은 main) + `ConversionService` | 부분 분리됨 | 1 |
| *(없음)* | `domain/models.py` | 값 객체 없음 | 1 |
| *(없음)* | `domain/exceptions.py` | `ValidationError`만 루트에 존재 | 1 |
| *(없음)* | `infrastructure/config_loader.py` | 설정 외부화 없음 | 2 |
| *(없음)* | `application/formatter.py` (JSON/CSV/Table) | Table만 인라인 f-string | 2 |

### 2.3 레이어 의존성 비교

#### AS-IS (평면 import)

```
UnitConverter.py ──→ validator.py
                 └──→ converter.py

tests/test_boundary.py ──→ validator.py, UnitConverter.py
tests/test_domain.py   ──→ converter.py
tests/test_golden_master.py ──→ 위 3개 전부
```

- `domain` / `application` 레이어 구분 없음
- `converter`와 `validator`가 각각 단위·비율을 **독립적으로** 알고 있음 (DRY 위반)

#### TO-BE (단방향 의존)

```
UnitConverter.py
       │
       ▼
application/  (parser, validator, formatter, service)
       │
       ▼
domain/  (models, converter, registry, exceptions)
       ▲
       │
infrastructure/  (config_loader)
```

- `domain/`은 `application/`, `infrastructure/`에 **의존하지 않음**
- `validator`는 `registry`를 주입받아 단위 존재 여부 판단 (SSOT)

### 2.4 설계 원칙 충족도

| 원칙 | AS-IS (GREEN) | TO-BE (목표) |
|------|---------------|--------------|
| **SRP** | 3파일 분리 (부분) — `validate`가 파싱+검증 혼합 | 레이어별 단일 책임 클래스 |
| **OCP** | 단위·비율·포맷 변경 시 소스 수정 | Registry / Formatter / ConfigLoader 확장 |
| **테스트 가능성** | Domain TC mock-free ✅ | 동일 유지 |
| **CLI 호환** | `python UnitConverter.py` ✅ | 얇은 main 유지 |
| **설정 외부화** | ❌ | `config/units.json` |
| **동적 단위 등록** | ❌ | `UnitRegistry.register()` |

### 2.5 TC · Gate 현황

| 구분 | TC 수 | 현재 상태 | Gate |
|------|-------|-----------|------|
| Phase 1 Core | 10 | ✅ Green (`D-CNV-*`, `U-IN-*`, `U-OUT-01`) | **Gate 1** — REFACTOR Step 3 후 |
| Phase 2 Extension | 5 | ❌ 미구현 (`D-CFG-*`, `D-REG-*`, `U-FMT-01`) | **Gate 2** — REFACTOR Step 6 후 |
| Golden Master | 7 함수·시나리오 | ✅ Green (루트 API 스냅샷) | **매 Step 필수** |

---

## 3. Golden Master 안전 전략

### 3.1 Golden Master가 고정하는 공개 API

`tests/test_golden_master.py`는 아래 **루트 모듈 API**에 직접 의존한다.

| import 경로 | 고정 항목 |
|-------------|-----------|
| `UnitConverter.process` | CLI 2줄 출력 형식 (`{value} {unit} = {x.x} {target}`) |
| `UnitConverter.main` | 프롬프트 문자열, stdout, 에러 1줄 출력 |
| `converter.to_meter` | 5자리 산술 (feet→meter 등) |
| `converter.convert_all` | 5자리 dict, 입력 단위 제외 |
| `validator.validate` | `(unit, value)` 반환, 예외 메시지 **문자열 일치** |
| `validator.FORMAT_ERROR` | `"Invalid format. Use unit:value (ex: meter:2.5)"` |
| `validator.NEGATIVE_ERROR` | `"Negative values are not allowed"` |

> **핵심:** 리팩터 중 **이 API 시그니처·메시지·수치를 변경하면 Golden Master가 즉시 Red**가 된다.

### 3.2 Strangler Fig + Shim 패턴

가장 안전한 이전 방식은 **구현을 패키지로 옮기고, 루트 모듈은 얇은 재export(shim)로 유지**하는 것이다.

```
[새 구현]  unit_converter/domain/converter.py
                ↑
[shim]     converter.py  →  from unit_converter.domain.converter import to_meter, convert_all
                ↑
[테스트]   test_golden_master.py  (import 변경 없음)
```

| 규칙 | 설명 |
|------|------|
| **Copy-then-delegate** | 로직을 **복사**해 패키지에 넣고, 동작 확인 후 루트에서 위임. 한 번에 cut하지 않음. |
| **Shim 유지** | Phase 1 Gate 통과 전까지 `converter.py`, `validator.py` 삭제 금지. |
| **알고리즘 동결** | `to_meter` / `convert_all` 산술·반올림 로직 변경 금지 (OCP, Golden Master 수치 고정). |
| **메시지 동결** | 에러 문자열 상수는 Golden Master가 검증 — 변경 시 TC·Golden Master 동시 수정 필요. |
| **Step 단위 검증** | 매 Step 후 `pytest tests/test_golden_master.py` → `pytest` 전체. |

### 3.3 금지 사항 (Golden Master 붕괴 방지)

| 금지 | 이유 |
|------|------|
| Golden Master 수정을 Step 1~3에서 먼저 진행 | 스냅샷이 없어지면 회귀 감지 불가 |
| `converter.py` 삭제 후 shim 없이 진행 | import 경로 단절 |
| Registry 도입 시 기본 3단위 비율 변경 | 수치 스냅샷 전체 실패 |
| `validate()` 시그니처를 `ParsedInput` 반환으로 즉시 변경 | shim 없이는 Golden Master·U-IN TC Red |
| Phase 1에서 Formatter Strategy 전면 도입 | 출력 형식 변경 위험 — Table 기본 포맷 먼저 동치 확인 |

---

## 4. 안전한 리팩토링 순서

`docs/architecture.md` §8.2 순서를 Golden Master 안전 제약에 맞게 구체화한다.  
**1 Step = 1 커밋** (`[REFACTOR]` 말머리) 권장.

### Step 0 — 기준선 확정 (선행)

| 항목 | 내용 |
|------|------|
| **작업** | `refactor` 브랜치에서 전체 테스트 Green 확인 |
| **명령** | `pytest tests/test_golden_master.py && pytest` |
| **Gate** | 15 TC + Golden Master 전부 Green — 이 상태가 **롤백 기준선** |

---

### Step 1 — Domain 레이어 추출 (Track B)

> 의존성 최하단부터. `application/`은 아직 건드리지 않음.

#### 1a. 패키지 골격 + 값 객체 + 예외

| 생성 | 내용 |
|------|------|
| `unit_converter/__init__.py` | 패키지 선언 |
| `unit_converter/domain/__init__.py` | |
| `unit_converter/domain/models.py` | `Unit`, `ParsedInput`, `ConversionResult` dataclass |
| `unit_converter/domain/exceptions.py` | `DomainError`, `UnknownUnitError` (기존 메시지 호환) |

- 기존 루트 모듈 **무변경** → Golden Master Green 유지

#### 1b. UnitRegistry (하드코딩 3단위)

| 생성 | 내용 |
|------|------|
| `unit_converter/domain/registry.py` | `UnitRegistry` — meter/feet/yard, 비율 AS-IS와 **동일** |

```python
# 기본 등록값 (converter.py와 동일해야 함)
meter: 1.0
feet:  3.28084   # 1 meter = 3.28084 feet
yard:  1.09361   # 1 meter = 1.09361 yard
```

#### 1c. UnitConverter 클래스 (로직 이전)

| 생성 | 내용 |
|------|------|
| `unit_converter/domain/converter.py` | `UnitConverter(registry)` — `to_meter`, `convert_all` |

- `converter.py`의 `Decimal` 반올림·`_round5` 로직을 **그대로** 이전
- 루트 `converter.py`를 shim으로 교체:

```python
# converter.py (shim)
from unit_converter.domain.converter import UnitConverter
from unit_converter.domain.registry import UnitRegistry

_registry = UnitRegistry.default()  # 3단위 기본
_converter = UnitConverter(_registry)

to_meter = _converter.to_meter
convert_all = _converter.convert_all
```

| 검증 | `pytest tests/test_golden_master.py tests/test_domain.py` |
|------|-----------------------------------------------------------|
| Gate | Golden Master 수치·`convert_all` dict 키 동일 |

---

### Step 2 — Application 레이어 추출 (Track A)

> `validator.validate` / `UnitConverter.process` 분리. 루트 shim 유지.

#### 2a. InputParser

| 생성 | 내용 |
|------|------|
| `unit_converter/application/parser.py` | `InputParser.parse(raw) → ParsedInput` |
| | 기존 `validate()` 내 `split`, `float` 로직 분리 |

#### 2b. InputValidator

| 생성 | 내용 |
|------|------|
| `unit_converter/application/validator.py` | `InputValidator(registry).validate(parsed)` |
| | 음수·단위 존재 검사 — 메시지 **Golden Master와 동일** |

- 루트 `validator.py` shim:

```python
# validator.py (shim)
from unit_converter.application.parser import InputParser
from unit_converter.application.validator import InputValidator
from unit_converter.domain.registry import UnitRegistry

_parser = InputParser()
_validator = InputValidator(UnitRegistry.default())

def validate(input_str: str) -> tuple[str, float]:
    parsed = _parser.parse(input_str)
    return _validator.validate(parsed)  # (unit, value) — 기존 시그니처 유지
```

#### 2c. TableFormatter + ConversionService

| 생성 | 내용 |
|------|------|
| `unit_converter/application/formatter.py` | `TableFormatter` — 기존 `process()` f-string 로직 |
| `unit_converter/application/service.py` | `ConversionService.run(raw) → list[str]` |

- `UnitConverter.process`는 service 위임으로 교체 (출력 동일해야 함)

| 검증 | `pytest tests/test_golden_master.py tests/test_boundary.py` |
|------|---------------------------------------------------------------|
| Gate | U-IN-* 메시지, U-OUT-01 2줄, Golden CLI 시나리오 Green |

---

### Step 3 — CLI 얇은 main + Gate 1

| 변경 | 내용 |
|------|------|
| `UnitConverter.py` | `main()`만 유지 — `ConversionService` 조립·호출 |
| | `process()`는 shim으로 `service.run` 위임 (Golden Master 호환) |

```python
# UnitConverter.py (목표 형태)
def main():
    service = build_default_service()  # Registry + Parser + Validator + Converter + TableFormatter
    raw = input("Insert value for converting (ex: meter:2.5): ")
    try:
        for line in service.run(raw):
            print(line)
    except ValidationError as e:
        print(e.args[0])
```

| 검증 | `pytest` **전체** (15 TC + Golden Master) |
|------|-------------------------------------------|
| **Gate 1** | Phase 1 TC 10 Green · Golden Master Green · `python UnitConverter.py` 수동 확인 |

#### Step 3 완료 후 선택 작업 (Gate 1 이후)

- `tests/test_domain.py` import를 `unit_converter.domain`으로 점진 전환 (Golden Master는 루트 shim 유지 가능)
- 루트 `converter.py`, `validator.py` shim **유지** (Golden Master 회귀 가드)

---

### Step 4 — Infrastructure + config (Phase 2 시작)

> Gate 1 통과 후. **Converter 알고리즘은 수정하지 않음** (OCP).

| 생성 | 내용 |
|------|------|
| `config/units.json` | §9 스키마 — 기존 하드코딩 비율과 **동일 값** |
| `unit_converter/infrastructure/config_loader.py` | `JsonConfigLoader.load(path) → UnitRegistry` |
| `UnitRegistry.default()` | 내부적으로 `units.json` 로드 (실패 시 기존 하드코딩 fallback 또는 `ConfigError`) |

| 검증 | `pytest tests/test_golden_master.py` — **수치 변화 없음** 확인 |
|------|------------------------------------------------------------------|
| 주의 | JSON 로드 후에도 Golden Master 수치가 동일해야 Phase 2 D-CFG TC 작성 가능 |

---

### Step 5 — Registry 동적 등록 API (Phase 2)

| 변경 | 내용 |
|------|------|
| `domain/registry.py` | `register(name, ratio_to_meter)` 공개 API |
| | cubit(0.4572) 등록 후 `convert_all` 확장 |

- **`domain/converter.py` 본체 로직 수정 없음** — Registry만 확장 (NFR-01)
- D-REG-01, D-REG-02 TC 추가·Green

| 검증 | Golden Master (Phase 1 시나리오) + D-REG-* Green |
|------|------------------------------------------------|

---

### Step 6 — OutputFormatter Strategy (Phase 2)

| 생성 | 내용 |
|------|------|
| `application/formatter.py` 확장 | `OutputFormatter` Protocol |
| | `JsonFormatter`, `CsvFormatter`, `TableFormatter` |
| `ConversionService` | format 인자·Strategy 주입 |

- **TableFormatter**는 Step 2 출력과 **바이트 단위 동치** 유지 (Golden Master)
- U-FMT-01 TC Green

| 검증 | `pytest` 전체 |
|------|---------------|
| **Gate 2** | Phase 2 TC 5 Green · Phase 1 + Golden Master 회귀 Green |

---

## 5. Step별 검증 체크리스트

매 Step 완료 후 아래를 순서대로 실행한다.

```bash
# 1. Golden Master (최우선)
pytest tests/test_golden_master.py -v

# 2. Track B
pytest tests/test_domain.py -v

# 3. Track A
pytest tests/test_boundary.py -v

# 4. 전체
pytest -v
```

| Step | Golden Master | Phase 1 (10) | Phase 2 (5) | 루트 shim |
|------|:-------------:|:------------:|:-----------:|:---------:|
| 0 기준선 | ✅ | ✅ | — | ✅ |
| 1 Domain | ✅ | ✅ | — | ✅ converter |
| 2 Application | ✅ | ✅ | — | ✅ converter, validator |
| 3 Gate 1 | ✅ | ✅ | — | ✅ 전부 |
| 4 Config | ✅ | ✅ | D-CFG-* | ✅ |
| 5 Registry | ✅ | ✅ | D-REG-* | ✅ |
| 6 Gate 2 | ✅ | ✅ | ✅ | 선택적 정리 |

---

## 6. 롤백 기준

| 신호 | 조치 |
|------|------|
| Golden Master 1건이라도 Red | **즉시 중단**, 해당 Step 변경 revert |
| D-CNV 수치 drift | Registry 비율·Decimal 로직 diff — AS-IS 값 복원 |
| U-IN 메시지 drift | `FORMAT_ERROR`, `NEGATIVE_ERROR`, `Unknown unit:` 문자열 복원 |
| U-OUT 형식 drift | `TableFormatter`를 `process()` 인라인 로직과 diff |

---

## 7. 커밋 가이드

| Step | 커밋 예시 |
|------|-----------|
| 1a | `[REFACTOR] Add domain models and exceptions skeleton` |
| 1b~1c | `[REFACTOR] Extract UnitRegistry and UnitConverter with root shim` |
| 2a~2c | `[REFACTOR] Split parser/validator/service; keep validator shim` |
| 3 | `[REFACTOR] Thin CLI main — Gate 1 Phase 1 Green` |
| 4 | `[REFACTOR] Add config/units.json and JsonConfigLoader` |
| 5 | `[REFACTOR] Extend UnitRegistry.register for dynamic units` |
| 6 | `[REFACTOR] Add OutputFormatter strategy — Gate 2` |

---

## 8. REFACTOR 완료 체크리스트

`docs/architecture.md` §10 기준.

| # | 항목 | 확인 시점 |
|---|------|-----------|
| 1 | `domain/`이 `application/`에 의존하지 않음 | Step 1~2 |
| 2 | 새 Formatter 추가 시 `Converter` 무변경 | Step 6 |
| 3 | `register("cubit", 0.4572)` 후 변환 동작 | Step 5 |
| 4 | `units.json` 수정만으로 비율 반영 | Step 4 |
| 5 | Domain TC mock-free Green | 전 Step |
| 6 | Phase 1 TC 10 + Phase 2 TC 5 Green | Gate 1, Gate 2 |
| 7 | `python UnitConverter.py` 실행 유지 | Step 3~ |
| 8 | Golden Master 7 시나리오 Green | **매 Step** |

---

## 9. 참고 문서

| 문서 | 역할 |
|------|------|
| `docs/architecture.md` | TO-BE 패키지 · FR/NFR · §8.2 적용 순서 |
| `docs/dual_track_design.md` | Track A/B · Gate 정의 |
| `docs/prd_test_traceability.md` | 15 TC · Test ID |
| `tests/test_golden_master.py` | REFACTOR 회귀 스냅샷 SSOT |
| `.cursor/skills/unit-converter-tdd/SKILL.md` | TDD 절차 · Converter 동결 규칙 |
