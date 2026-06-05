# Architecture — 목표 패키지 구조 (SPEC)

> **단계:** SPEC (설계만) · **적용 시점:** REFACTOR  
> **기준 문서:** `README.md`  
> **관련 SPEC:** `spec_analysis.md`, `prd_test_traceability.md`, `dual_track_design.md`  
> **작성 일자:** 2026-06-05

---

## 1. 문서 목적

본 문서는 **REFACTOR 단계에서 적용할 목표 Python 패키지 구조**를 정의한다.  
현재 레거시 `UnitConverter.py`(단일 `main()`)를 OCP/SRP를 만족하는 구조로 전환하기 위한 **설계 명세**이며, **코드 변경은 포함하지 않는다.**

| 현재 (AS-IS) | 목표 (TO-BE) |
|--------------|--------------|
| 1파일 · 37줄 · God Function | 레이어 분리 · 패키지화 |
| if/elif 단위 분기 | Registry + Strategy |
| 하드코딩 비율 | Config 외부화 |
| 테스트 없음 | Dual-Track TC 15개 |

---

## 2. 설계 원칙

### 2.1 SRP (Single Responsibility Principle)

각 모듈·클래스는 **하나의 변경 이유**만 갖는다.

| 모듈 | 단일 책임 | 변경 이유 |
|------|-----------|-----------|
| `Parser` | `unit:value` 문자열 → 구조체 | 입력 형식 규칙 변경 |
| `Validator` | 파싱 결과 유효성 검사 | 검증 정책 변경 |
| `Converter` | 기준단위(meter) 경유 변환 | *(변환 알고리즘 고정 — Phase 2에서도 무변경)* |
| `UnitRegistry` | 단위·비율 등록·조회 | 단위 추가/등록 방식 |
| `ConfigLoader` | 설정 파일 → Registry 주입 | JSON/YAML 포맷 |
| `OutputFormatter` | 변환 결과 → 문자열 | 출력 포맷 추가 |
| `ConversionService` | 유스케이스 오케스트레이션 | CLI 흐름 변경 |
| `UnitConverter.py` | CLI 진입·I/O | 실행 방식만 |

### 2.2 OCP (Open-Closed Principle)

**확장에는 열려 있고, 수정에는 닫혀 있다.**

| 확장 시나리오 | OCP 대응 | 수정 없이 유지되는 모듈 |
|---------------|----------|-------------------------|
| 새 단위 추가 (cubit) | `UnitRegistry.register()` | `Converter` |
| 새 출력 포맷 (CSV) | `OutputFormatter` 구현체 추가 | `Converter`, `Parser` |
| 설정 소스 변경 (YAML) | `ConfigLoader` 구현체 추가 | `Converter`, `Registry` API |
| 새 검증 규칙 | `Validator` 확장 | `Converter` |

**OCP 핵심 확장 지점**

```
UnitRegistry.register(name, ratio_to_meter)   # 단위 확장
OutputFormatter (Protocol)                     # 포맷 확장
ConfigLoader.load(path) → UnitRegistry         # 설정 소스 확장
```

---

## 3. 목표 패키지 구조

```
UnitConverter_09/
│
├── UnitConverter.py                 # CLI 진입점 (README 호환, 얇은 main)
│
├── unit_converter/                  # 메인 패키지
│   ├── __init__.py
│   │
│   ├── application/                 # Track A — UI / Boundary
│   │   ├── __init__.py
│   │   ├── parser.py                # InputParser
│   │   ├── validator.py             # InputValidator
│   │   ├── formatter.py             # OutputFormatter (Strategy)
│   │   └── service.py               # ConversionService (오케스트레이션)
│   │
│   ├── domain/                      # Track B — Domain / Logic
│   │   ├── __init__.py
│   │   ├── models.py                # Unit, ParsedInput, ConversionResult
│   │   ├── converter.py             # UnitConverter (변환만)
│   │   ├── registry.py              # UnitRegistry
│   │   └── exceptions.py            # DomainError, UnknownUnitError, ...
│   │
│   └── infrastructure/              # Track B — 외부 연동
│       ├── __init__.py
│       └── config_loader.py         # JsonConfigLoader, YamlConfigLoader
│
├── config/
│   └── units.json                   # 기본 3단위 비율
│
└── tests/
    ├── test_domain.py               # D-* TC (Track B)
    └── test_boundary.py             # U-* TC (Track A)
```

### 3.1 레이어 의존성

```
UnitConverter.py
       │
       ▼
application/          ← Track A (Boundary)
  service.py ──────────────┐
  parser.py                │
  validator.py             │ depends on
  formatter.py             ▼
                    domain/              ← Track B (Domain)
                      converter.py
                      registry.py
                           ▲
                           │ depends on
                    infrastructure/
                      config_loader.py
```

**규칙**

- `domain/`은 `application/`, `infrastructure/`에 **의존하지 않음**
- `application/`은 `domain/`을 **주입**받아 사용
- `infrastructure/`는 `domain/`의 `UnitRegistry`에 데이터 **주입**
- `UnitConverter.py`는 `application.service`만 호출

---

## 4. 모듈 상세 (REFACTOR 목표)

### 4.1 Domain — `unit_converter/domain/`

| 파일 | 클래스 / 함수 | 책임 | Phase |
|------|---------------|------|-------|
| `models.py` | `ParsedInput`, `ConversionResult`, `Unit` | 값 객체 | 1 |
| `registry.py` | `UnitRegistry` | 단위 등록·조회·`ratio_to_meter` 제공 | 1 |
| `converter.py` | `UnitConverter` | `to_meter()`, `convert_all()` | 1 |
| `exceptions.py` | `UnknownUnitError`, `ConfigError` | 도메인 예외 | 1·2 |

```python
# converter.py — REFACTOR 목표 시그니처 (설계만)
class UnitConverter:
    def __init__(self, registry: UnitRegistry): ...
    def to_meter(self, value: float, unit: str) -> float: ...
    def convert_all(self, value: float, unit: str) -> list[ConversionResult]: ...
```

```python
# registry.py — REFACTOR 목표 시그니처 (설계만)
class UnitRegistry:
    def register(self, name: str, ratio_to_meter: float) -> None: ...
    def get(self, name: str) -> Unit: ...
    def all_units(self) -> list[str]: ...
```

### 4.2 Application — `unit_converter/application/`

| 파일 | 클래스 | 책임 | Phase |
|------|--------|------|-------|
| `parser.py` | `InputParser` | `"meter:2.5"` → `ParsedInput` | 1 |
| `validator.py` | `InputValidator` | 형식·음수·단위 존재 검증 | 1 |
| `formatter.py` | `OutputFormatter` (Protocol) | JSON / CSV / Table Strategy | 2 |
| `service.py` | `ConversionService` | parse → validate → convert → format | 1 |

```python
# formatter.py — OCP Strategy (설계만)
class OutputFormatter(Protocol):
    def format(self, results: list[ConversionResult]) -> str: ...

class JsonFormatter(OutputFormatter): ...
class CsvFormatter(OutputFormatter): ...
class TableFormatter(OutputFormatter): ...
```

### 4.3 Infrastructure — `unit_converter/infrastructure/`

| 파일 | 클래스 | 책임 | Phase |
|------|--------|------|-------|
| `config_loader.py` | `JsonConfigLoader` | JSON → `UnitRegistry` | 2 |
| `config_loader.py` | `YamlConfigLoader` | YAML → `UnitRegistry` *(선택)* | 2 |

### 4.4 진입점 — `UnitConverter.py`

```python
# REFACTOR 목표 — 얇은 main (설계만)
def main():
    registry = build_registry()          # ConfigLoader or default
    service = ConversionService(
        parser=InputParser(),
        validator=InputValidator(registry),
        converter=UnitConverter(registry),
        formatter=get_formatter(args),   # Strategy
    )
    raw = input("Insert value for converting (ex: meter:2.5): ")
    print(service.run(raw))
```

---

## 5. FR / NFR 정의 및 매핑

### 5.1 Functional Requirements (FR)

README **기본 요구사항 · 비즈니스 로직 · 추가 요구사항**에서 도출.

| FR ID | 요구사항 | README 출처 | 담당 모듈 | Test ID |
|-------|----------|-------------|-----------|---------|
| **FR-01** | `unit:value` 형식 입력 수신 | 기본 #1 | `InputParser` | U-OUT-01 |
| **FR-02** | 입력값을 **모든 지원 단위**로 변환 출력 | 기본 #1, Overview | `UnitConverter.convert_all`, `ConversionService` | U-OUT-01, D-CNV-02, D-CNV-04 |
| **FR-03** | meter / feet / yard 지원 | 기본 #2 | `UnitRegistry` (기본 3단위) | D-CNV-01, D-CNV-03, U-OUT-01 |
| **FR-04** | 단위 추가 시 기존 코드 변경 최소화 | 기본 #3, Overview | `UnitRegistry.register()` | D-REG-01, D-REG-02 |
| **FR-05** | `1 m = 3.28084 ft` 변환 | 비즈니스 로직 | `UnitConverter` + Registry 비율 | D-CNV-01, D-CNV-02 |
| **FR-06** | `1 m = 1.09361 yard` 변환 | 비즈니스 로직 | `UnitConverter` + Registry 비율 | D-CNV-04 |
| **FR-07** | feet ↔ yard는 meter 경유 | 비즈니스 로직 | `UnitConverter.to_meter()` | D-CNV-03 |
| **FR-08** | 단위 변환 정확성 테스트 검증 | 기본 #4, Overview | `tests/test_domain.py` | D-CNV-* |
| **FR-09** | 변환 비율 JSON/YAML 외부 설정 | 추가 — 설정 외부화 | `JsonConfigLoader` | D-CFG-01, D-CFG-02 |
| **FR-10** | 동적 단위·비율 등록 (`cubit`) | 추가 — 동적 등록 | `UnitRegistry.register()` | D-REG-01, D-REG-02 |
| **FR-11** | JSON / CSV / 표 출력 선택 | 추가 — 출력 포맷 | `OutputFormatter` Strategy | U-FMT-01 |

### 5.2 Non-Functional Requirements (NFR)

README **품질 요구사항 · Overview 설계 목표**에서 도출.

| NFR ID | 요구사항 | README 출처 | 설계 대응 | 검증 |
|--------|----------|-------------|-----------|------|
| **NFR-01** | OCP — 확장에 열림, 수정에 닫힘 | 품질 #1 | Registry / Formatter / ConfigLoader Strategy | D-REG-01, U-FMT-01, Phase 2 Converter 무변경 |
| **NFR-02** | SRP — 책임별 클래스 구성 | 품질 #2 | §3 패키지 레이어 분리 | 모듈 경계, Track A/B 분리 |
| **NFR-03** | 음수 입력 거부 | 품질 #3 | `InputValidator.validate()` | U-IN-03 |
| **NFR-04** | 잘못된 형식 거부 | 품질 #3 | `InputParser` + `InputValidator` | U-IN-01, U-IN-02, U-IN-05 |
| **NFR-05** | 없는 단위 거부 | 품질 #3 | `InputValidator` + `UnknownUnitError` | U-IN-04 |
| **NFR-06** | 테스트 가능성 (Domain mock-free) | Overview #3, 기본 #4 | Domain ↔ Application 분리 | D-CNV-* mock 없이 Green |
| **NFR-07** | 설정 변경 시 코드 재배포 불필요 | 추가 — 설정 외부화 | `config/units.json` | D-CFG-02 |
| **NFR-08** | README CLI 호환 (`python UnitConverter.py`) | 가상환경 및 실행 | `UnitConverter.py` 얇은 진입점 유지 | U-OUT-01 |

---

## 6. FR/NFR → 패키지 매핑 매트릭스

| 패키지 / 모듈 | FR | NFR |
|---------------|-----|-----|
| `domain/converter.py` | FR-02, FR-05, FR-06, FR-07 | NFR-01 (닫힘), NFR-06 |
| `domain/registry.py` | FR-03, FR-04, FR-10 | NFR-01 (확장 지점) |
| `domain/models.py` | FR-01, FR-02 | NFR-02 |
| `domain/exceptions.py` | — | NFR-04, NFR-05 |
| `application/parser.py` | FR-01 | NFR-04, NFR-02 |
| `application/validator.py` | — | NFR-03, NFR-04, NFR-05 |
| `application/formatter.py` | FR-11 | NFR-01 (확장 지점) |
| `application/service.py` | FR-02 | NFR-02, NFR-08 |
| `infrastructure/config_loader.py` | FR-09 | NFR-07, NFR-01 |
| `config/units.json` | FR-09 | NFR-07 |
| `UnitConverter.py` | — | NFR-08 |
| `tests/test_domain.py` | FR-08 | NFR-06 |
| `tests/test_boundary.py` | FR-08 | NFR-03~05 |

---

## 7. Dual Track ↔ 패키지 매핑

| Track | 레이어 | 패키지 | RED 순서 |
|-------|--------|--------|----------|
| **B** | Domain / Logic | `domain/`, `infrastructure/` | **1번째** |
| **A** | UI / Boundary | `application/`, `UnitConverter.py` | **2번째** |

> Track A/B = 레이어 이름 · RED 실행 = Domain(B) → Boundary(A)  
> (`dual_track_design.md` §1 참고)

---

## 8. REFACTOR 단계 적용 순서

SPEC 단계에서는 **구현하지 않는다.** REFACTOR 시 아래 순서로 적용.

```
Step 0  tests/ RED 작성 (D-CNV → U-IN → U-OUT)
Step 1  domain/models.py, registry.py, converter.py, exceptions.py
Step 2  application/parser.py, validator.py, service.py
Step 3  UnitConverter.py → 얇은 main으로 교체
        ── Gate 1 (Phase 1 TC 10 Green) ──
Step 4  infrastructure/config_loader.py + config/units.json
Step 5  domain/registry.py register API 확장
Step 6  application/formatter.py (JsonFormatter → Csv/Table)
        ── Gate 2 (Phase 2 TC 15 Green) ──
```

### 8.1 레거시 → 목표 마이그레이션

| 레거시 (`UnitConverter.py`) | REFACTOR 후 |
|-----------------------------|-------------|
| `input()` | `UnitConverter.py` (진입점만) |
| `split(':', 1)` | `InputParser.parse()` |
| `float()` + try/except | `InputParser` + `InputValidator` |
| `if unit == "meter"` 분기 | `UnitRegistry.get()` |
| `value / 3.28084` | `UnitConverter.to_meter()` |
| `meter_value * 3.28084` | `UnitConverter.convert_all()` |
| `print(f"...")` | `OutputFormatter.format()` |

---

## 9. 설정 파일 스키마 (목표)

```json
{
  "base_unit": "meter",
  "units": {
    "meter": 1.0,
    "feet": 3.28084,
    "yard": 1.09361
  }
}
```

- `ratio` = **1 base_unit 당 해당 단위 값** (README 비즈니스 로직과 동일)
- `ConfigLoader`가 Registry에 주입 · 코드 내 매직 넘버 제거 (FR-09, NFR-07)

---

## 10. SPEC ↔ REFACTOR 체크리스트

REFACTOR 완료 시 아래를 확인한다.

| # | 항목 | FR/NFR |
|---|------|--------|
| 1 | `domain/`이 `application/`에 의존하지 않음 | NFR-02 |
| 2 | 새 Formatter 추가 시 `Converter` 무변경 | NFR-01 |
| 3 | `register("cubit", 0.4572)` 후 변환 동작 | FR-10 |
| 4 | `units.json` 수정만으로 비율 반영 | FR-09, NFR-07 |
| 5 | Domain TC mock-free Green | NFR-06 |
| 6 | Phase 1 TC 10 + Phase 2 TC 5 Green | FR-08 |
| 7 | `python UnitConverter.py` 실행 유지 | NFR-08 |

---

## 11. 참고 문서

| 문서 | 역할 |
|------|------|
| `docs/spec_analysis.md` | AS-IS Gap · 레거시 스멜 |
| `docs/prd_test_traceability.md` | REQ ↔ Test ID |
| `docs/dual_track_design.md` | Dual Track RED · Gate |
| `docs/architecture.md` | **본 문서** — REFACTOR 목표 패키지 · FR/NFR 매핑 |
