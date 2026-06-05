# Dual Track 설계표 (Final)

> **기준 문서:** `README.md`  
> **추적표:** `docs/prd_test_traceability.md`  
> **작성 일자:** 2026-06-05  
> **TC:** 15개 (Phase 1: 10 · Phase 2: 5)

---

## 1. 설계 개요

Unit Converter를 **두 개의 Track(레이어)** 으로 분리하여 TDD RED → Green → Refactor 사이클을 적용한다.

| Track | 명칭 | 책임 | TC 접두어 |
|-------|------|------|-----------|
| **A** | UI / Boundary | 입력 파싱·검증·출력 포맷 | `U-*` |
| **B** | Domain / Logic | 변환 계산·단위 등록·설정 로드 | `D-*` |

| Phase | 범위 | README Activities | Gate |
|-------|------|-------------------|------|
| **Phase 1** | Core — 기본·품질 요구사항 | 2~3단계 (~2.5h) | Gate 1 |
| **Phase 2** | Extension — 추가 요구사항 | 4단계 (~2h) | Gate 2 |

```
┌─────────────────────────────────────────────────────┐
│  Track A — UI / Boundary                            │
│  Parser · Validator · Formatter · CLI               │
├─────────────────────────────────────────────────────┤
│  Track B — Domain / Logic                           │
│  Converter · UnitRegistry · ConfigLoader            │
└─────────────────────────────────────────────────────┘
         ↑ Phase 2: CFG / REG / FMT 확장
         ↑ Phase 1: Core 변환·검증
```

> **Track A/B = 레이어 구분 · RED 실행 순서 = Domain(B) → Boundary(A)**  
> Track 이름의 알파벳(A, B)은 **레이어 종류**를 뜻하며, **먼저 구현·테스트할 Track**을 의미하지 않는다.  
> Phase 1 RED는 의존성상 **Track B(Domain)를 먼저** Green으로 만든 뒤 **Track A(Boundary)** 를 통합한다.

| | Track A — UI / Boundary | Track B — Domain / Logic |
|--|-------------------------|---------------------------|
| **레이어 역할** | 파싱 · 검증 · 출력 | 변환 · 등록 · 설정 |
| **RED 실행 순서** | **2번째** (Domain 주입 후) | **1번째** (mock 불필요) |

---

## 2. Track 분리 원칙

### 2.1 왜 A / B로 나누는가

| 원칙 | Track A (Boundary) | Track B (Domain) |
|------|--------------------|------------------|
| **SRP** | 사용자 입·출력, 형식 검증 | 순수 변환·등록·설정 |
| **테스트** | Given 문자열 → Then 메시지/줄 수 | Given 숫자 → Then 값(±ε) |
| **의존성** | Track B를 주입받아 사용 | Track A에 의존하지 않음 |
| **RED 순서** | Phase 1 후반 · Phase 2 | **Phase 1 선행** (mock 불필요) |

Track B를 먼저 Green으로 만든 뒤 Track A에서 통합한다.  
Phase 2(REG/CFG/FMT)는 Track B 확장 + Track A Formatter 추가로 OCP를 입증한다.

### 2.2 OCP / SRP 대응

| README 품질 요구 | 설계 대응 | 검증 TC |
|------------------|-----------|---------|
| SRP | Parser / Validator / Converter / Formatter 분리 | Track A·B 분리 자체 |
| OCP | `UnitRegistry.register()`, `OutputFormatter` Strategy | D-REG-01, U-FMT-01 |
| 입력 검증 | Validator 단독 모듈 | U-IN-01 ~ U-IN-05 |
| 테스트 검증 | Domain TC mock-free | D-CNV-01 ~ D-CNV-04 |

---

## 3. 목표 아키텍처

```
UnitConverter.py              # CLI 진입점 (얇은 main)
│
├── application/              # Track A
│   ├── parser.py             # unit:value 파싱
│   ├── validator.py          # 형식·음수·단위 검증
│   └── formatter.py          # JSON / CSV / Table (Strategy)
│
├── domain/                   # Track B
│   ├── converter.py          # to_meter, convert_all
│   ├── registry.py           # UnitRegistry (등록·조회)
│   └── exceptions.py         # ConfigError 등
│
├── infrastructure/           # Track B (Phase 2)
│   └── config_loader.py      # JSON/YAML 로드
│
├── config/
│   └── units.json            # 기본 3단위 비율
│
└── tests/
    ├── test_boundary.py      # U-* TC
    └── test_domain.py        # D-* TC
```

### 3.1 모듈 ↔ Track 매핑

| 모듈 | Track | Phase | 담당 TC |
|------|-------|-------|---------|
| `parser.py` | A | 1 | U-OUT-01 |
| `validator.py` | A | 1 | U-IN-01 ~ U-IN-05 |
| `formatter.py` | A | 2 | U-FMT-01 |
| `converter.py` | B | 1 | D-CNV-01 ~ D-CNV-04 |
| `registry.py` | B | 2 | D-REG-01, D-REG-02 |
| `config_loader.py` | B | 2 | D-CFG-01, D-CFG-02 |

---

## 4. Dual-Track RED 설계표

### 4.1 Phase 1 — Core (10 TC)

#### Track B — Domain *(먼저 Red)*

| Test ID | 함수 | Given | Then (Expected RED) | REQ |
|---------|------|-------|---------------------|-----|
| **D-CNV-01** | `to_meter` | 1 feet | 0.3048 m (±ε) | REQ-BIZ-01, REQ-FUNC-03 |
| **D-CNV-02** | `convert_all` | 2.5 m | 8.20210 ft (소수 5자리) | REQ-BIZ-01, REQ-FUNC-02 |
| **D-CNV-03** | `convert_all` | 1 feet | yard 값 = meter 경유 결과와 일치 | REQ-BIZ-03 |
| **D-CNV-04** | `convert_all` | 2.5 m | 2.73403 yard (README 예시) | REQ-BIZ-02, REQ-FUNC-02 |

#### Track A — Boundary

| Test ID | Given | Then (Expected RED) | REQ |
|---------|-------|---------------------|-----|
| **U-IN-01** | `""` | Format error message | REQ-VAL-02 |
| **U-IN-02** | `meter` | Format error (콜론 없음) | REQ-VAL-02 |
| **U-IN-03** | `meter:-1` | Reject negative values | REQ-VAL-01 |
| **U-IN-04** | `mile:1` | Unknown unit error | REQ-VAL-03 |
| **U-IN-05** | `:2.5` 또는 `meter:` | Format error (빈 토큰) | REQ-VAL-02 |
| **U-OUT-01** | `meter:2.5` | 출력 ≥ 3줄 (meter/feet/yard) | REQ-FUNC-01, REQ-FUNC-02 |

---

### 4.2 Phase 2 — Extension (5 TC)

| Test ID | Track | 함수 / Given | Then (Expected RED) | REQ |
|---------|-------|--------------|---------------------|-----|
| **D-CFG-01** | B | `load_json` — 손상된 파일 | `ConfigError` 발생 | REQ-CFG-01 |
| **D-CFG-02** | B | `load_json` — valid `units.json` | meter/feet/yard 3단위 로드 | REQ-CFG-01, REQ-CFG-02 |
| **D-REG-01** | B | `register("cubit", 0.4572)` | cubit → meter 변환 가능 | REQ-REG-01, REQ-FUNC-04 |
| **D-REG-02** | B | `convert_all` — cubit 입력 | cubit ↔ meter/feet/yard | REQ-REG-02 |
| **U-FMT-01** | A | `meter:2.5`, format=JSON | 유효한 JSON 구조·값 | REQ-FMT |

---

## 5. RED 실행 순서

```
Phase 1 — Core
══════════════
  Track B (Domain)     Track A (Boundary)
  ─────────────────    ──────────────────
  D-CNV-01             (대기)
  D-CNV-02
  D-CNV-03
  D-CNV-04             U-IN-01
                       U-IN-02
                       U-IN-03
                       U-IN-04
                       U-IN-05
                       U-OUT-01  ← 통합

  ══ Gate 1: Core Green (TC 10/10) ══

Phase 2 — Extension
═══════════════════
  Track B (Domain)     Track A (Boundary)
  ─────────────────    ──────────────────
  D-CFG-01
  D-CFG-02
  D-REG-01
  D-REG-02             U-FMT-01

  ══ Gate 2: Full PRD Green (TC 15/15) ══
```

> 좌측 **Track B(Domain)가 항상 선행**한다. Track A는 Boundary 레이어이지만 실행 순서상 뒤에 온다.

**실행 규칙**

1. Track B Domain TC를 Phase 1에서 **반드시 선행** Green
2. Track A는 Domain 주입 후 Boundary TC Green
3. Phase 2 진행 중 **Phase 1 TC 10개 회귀 Green** 유지
4. Converter 본체는 Phase 2에서 **수정하지 않음** (OCP 입증)

---

## 6. Gate 기준

### Gate 1 — Core Green (Phase 1)

| 항목 | 기준 |
|------|------|
| TC | D-CNV-01~04, U-IN-01~05, U-OUT-01 **전부 Green** |
| 기능 | `meter:2.5` 입력 → 3단위 변환 출력 |
| 검증 | 음수·형식·unknown unit 거부 |
| 아키텍처 | Parser / Validator / Converter 분리, Domain TC mock-free |

### Gate 2 — Full PRD Green (Phase 2)

| 항목 | 기준 |
|------|------|
| TC | Phase 1 10 + Phase 2 5 = **15/15 Green** |
| 설정 | JSON 로드·손상 파일 오류 처리 |
| 등록 | cubit 동적 등록 후 상호 변환 |
| OCP | Converter 수정 없이 REG/CFG/FMT 추가 |
| 출력 | JSON 포맷 출력 동작 |

---

## 7. Requirement 커버리지

| REQ ID | 설명 | Test ID |
|--------|------|---------|
| REQ-FUNC-01 | unit:value 입력 | U-OUT-01 |
| REQ-FUNC-02 | 전 단위 변환 출력 | U-OUT-01, D-CNV-02, D-CNV-04 |
| REQ-FUNC-03 | meter/feet/yard 지원 | D-CNV-01, D-CNV-03, U-OUT-01 |
| REQ-FUNC-04 | OCP — 변경 최소화 | D-REG-01, D-REG-02 |
| REQ-BIZ-01 | 1 m = 3.28084 ft | D-CNV-01, D-CNV-02 |
| REQ-BIZ-02 | 1 m = 1.09361 yard | D-CNV-04 |
| REQ-BIZ-03 | meter 경유 feet↔yard | D-CNV-03 |
| REQ-VAL-01 | 음수 거부 | U-IN-03 |
| REQ-VAL-02 | 형식 오류 거부 | U-IN-01, U-IN-02, U-IN-05 |
| REQ-VAL-03 | unknown unit 거부 | U-IN-04 |
| REQ-ARCH | OCP/SRP | 구조 + D-REG-01, U-FMT-01 |
| REQ-CFG-01 | 설정 로드·오류 | D-CFG-01, D-CFG-02 |
| REQ-CFG-02 | 설정 변경 반영 | D-CFG-02 |
| REQ-REG-01 | 동적 단위 등록 | D-REG-01 |
| REQ-REG-02 | 등록 즉시 사용 | D-REG-02 |
| REQ-FMT | 출력 포맷 | U-FMT-01 |

**총 REQ 16 · TC 15**

---

## 8. 커버리지 요약

| Phase | Track A | Track B | TC | 상태 |
|-------|---------|---------|-----|------|
| 1 Core | 6 | 4 | 10 | ❌ |
| 2 Extension | 1 | 4 | 5 | ❌ |
| **합계** | **7** | **8** | **15** | ❌ |

---

## 9. Green 후 선택적 확장

| Test ID | Track | Given → Then | 시점 |
|---------|-------|--------------|------|
| D-CFG-03 | B | YAML 설정 로드 | Phase 2 여유 |
| U-FMT-02 | A | format=CSV → 헤더 + 행 | Phase 2 여유 |
| U-FMT-03 | A | format=table → 표 출력 | Phase 2 여유 |

---

## 10. 레거시 대비 변화

| 항목 | `UnitConverter.py` (현재) | Dual Track (목표) |
|------|---------------------------|-------------------|
| 구조 | 단일 `main()` 37줄 | Track A + B 모듈 분리 |
| 단위 추가 | if/elif 수정 | `registry.register()` |
| 비율 | 매직 넘버 하드코딩 | `units.json` + ConfigLoader |
| 검증 | 부분 (음수 미구현) | U-IN-01~05 전체 |
| 테스트 | 없음 | RED 15 TC |
| 출력 | f-string 고정 | Formatter Strategy |

---

## 11. 참고 문서

| 문서 | 역할 |
|------|------|
| `docs/spec_analysis.md` | 레거시 스멜 · PRD Gap 분석 |
| `docs/prd_test_traceability.md` | REQ ↔ Test ID 상세 추적 |
| `docs/dual_track_design.md` | **본 문서** — 최종 설계·실행 가이드 |
