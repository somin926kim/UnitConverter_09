# PRD → Test 추적표 (Requirement Traceability Matrix)

> **기준 문서:** `README.md`  
> **작성 일자:** 2026-06-05  
> **현재 테스트 코드:** 미구현 (Test ID는 구현 예정 TC 기준으로 정의)

---

## 1. Track · Phase 정의

| 구분 | Track A — UI / Boundary | Track B — Domain / Logic |
|------|---------------------------|---------------------------|
| **레이어** | 입력 파싱·검증·출력 | 변환 계산·등록·설정 로드 |
| **SRP** | Parser, Validator, Formatter | Converter, Registry, ConfigLoader |
| **RED 특징** | Given 문자열 → Then 메시지/줄 수 | Given 숫자 → Then 값(±ε) |
| **TC 접두어** | `U-*` | `D-*` |

| Phase | 범위 | README Activities | TC 수 |
|-------|------|-------------------|-------|
| **Phase 1** | Core (기본·품질) | 2~3단계 | 10 |
| **Phase 2** | Extension (추가) | 4단계 | 5 |
| **합계** | | | **15** |

> **Track** = 어디를 테스트할지 (경계 vs 도메인)  
> **Phase** = 언제 구현할지 (Core → Extension)

**표시/내부 정밀도 SSOT:** Domain `D-CNV-*`는 비율·산술 검증용 **소수 5자리** 고정(예: 8.20210 ft, 2.73403 yard); Boundary/README CLI(`U-OUT-01`, FR-02)는 **소수 1자리 반올림 표시**(README: 8.2 feet, 2.7 yard).

---

## 2. Dual-Track RED 설계표

### Phase 1 — Core (10 TC)

#### Track B — Domain (먼저 Red)

| Test ID | 함수 | Given → Then (Expected RED) | REQ | Phase |
|---------|------|----------------------------|-----|-------|
| **D-CNV-01** | `to_meter` | 1 feet → 0.3048 m (±ε) | REQ-BIZ-01, REQ-FUNC-03 | 1 |
| **D-CNV-02** | `convert_all` | 2.5 m → 8.20210 ft (소수 5자리) | REQ-BIZ-01, REQ-FUNC-02 | 1 |
| **D-CNV-03** | `convert_all` | feet → yard, meter 경유 일관성 | REQ-BIZ-03 | 1 |
| **D-CNV-04** | `convert_all` | 2.5 m → 2.73403 yard (소수 5자리; 표시는 SSOT 1자리) | REQ-BIZ-02, REQ-FUNC-02 | 1 |

#### Track A — Boundary

| Test ID | Given | Then (Expected RED) | REQ | Phase |
|---------|-------|---------------------|-----|-------|
| **U-IN-01** | `""` | Format error message | REQ-VAL-02 | 1 |
| **U-IN-02** | `meter` (콜론 없음) | Format error | REQ-VAL-02 | 1 |
| **U-IN-03** | `meter:-1` | Reject negative values | REQ-VAL-01 | 1 |
| **U-IN-04** | `mile:1` | Unknown unit error | REQ-VAL-03 | 1 |
| **U-IN-05** | `:2.5` 또는 `meter:` | Format error | REQ-VAL-02 | 1 |
| **U-OUT-01** | `meter:2.5` | stdout **2줄** (`feet`·`yard`만, README `2.5 meter = …` 형식·소수 1자리); **입력 meter 단독 행·meter→meter 줄 없음** (FR-02「다른」지원 단위) | REQ-FUNC-01, REQ-FUNC-02 | 1 |

### Phase 2 — Extension (5 TC)

| Test ID | Track | 함수 / Given | Then (Expected RED) | REQ | Phase |
|---------|-------|--------------|---------------------|-----|-------|
| **D-CFG-01** | B | `load_json` — 손상된 파일 | `ConfigError` 발생 | REQ-CFG-01 | 2 |
| **D-CFG-02** | B | `load_json` — valid `units.json` | 3단위(meter/feet/yard) 로드 | REQ-CFG-01, REQ-CFG-02 | 2 |
| **D-REG-01** | B | `register` — cubit = 0.4572 m | 등록 후 cubit 변환 가능 | REQ-REG-01, REQ-FUNC-04 | 2 |
| **D-REG-02** | B | `convert_all` — cubit 입력 | cubit ↔ meter/feet/yard 상호 변환 | REQ-REG-02 | 2 |
| **U-FMT-01** | A | `meter:2.5`, format=JSON | 유효한 JSON 구조·값 | REQ-FMT | 2 |

---

## 3. Requirement → Test ID 추적표

| REQ ID | Requirement 설명 (README 출처) | Test ID | Track |
|--------|-------------------------------|---------|-------|
| REQ-FUNC-01 | `unit:value` 형식으로 입력 수신 | U-OUT-01 | A |
| REQ-FUNC-02 | 입력값을 다른 모든 지원 단위로 변환 출력 | U-OUT-01, D-CNV-02, D-CNV-04 | A+B |
| REQ-FUNC-03 | meter / feet / yard 지원 | D-CNV-01, D-CNV-03, U-OUT-01 | A+B |
| REQ-FUNC-04 | 단위 추가 시 기존 코드 변경 최소화 (OCP) | D-REG-01, D-REG-02 | B |
| REQ-BIZ-01 | `1 meter = 3.28084 feet` | D-CNV-01, D-CNV-02 | B |
| REQ-BIZ-02 | `1 meter = 1.09361 yard` | D-CNV-04 | B |
| REQ-BIZ-03 | feet ↔ yard는 meter 기준 경유 | D-CNV-03 | B |
| REQ-VAL-01 | 음수 입력 거부 | U-IN-03 | A |
| REQ-VAL-02 | 잘못된 형식 거부 | U-IN-01, U-IN-02, U-IN-05 | A |
| REQ-VAL-03 | 없는 단위 거부 | U-IN-04 | A |
| REQ-ARCH | OCP/SRP — 책임 분리·확장 시 Converter 무변경 | *(구조)*, D-REG-01, U-FMT-01 | A+B |
| REQ-CFG-01 | JSON/YAML 설정 로드·오류 처리 | D-CFG-01, D-CFG-02 | B |
| REQ-CFG-02 | 설정 변경 시 코드 수정 불필요 | D-CFG-02 | B |
| REQ-REG-01 | 동적 단위 등록 (예: cubit) | D-REG-01 | B |
| REQ-REG-02 | 등록 즉시 변환 사용 | D-REG-02 | B |
| REQ-FMT | JSON / CSV / 표 출력 (대표: JSON) | U-FMT-01 | A |

**총 REQ 16개 · TC 15개**

### PRD 커버리지 (README 추가 항목)

| README 요구 | TC | 비고 |
|-------------|-----|------|
| yard 변환 (1.09361) | D-CNV-04, U-OUT-01 | Domain 2.73403 yard / CLI 표시 2.7 yard (SSOT §1) |
| unknown unit 검증 | U-IN-04 | 품질 요구사항 충족 |
| YAML 설정 | — | Green 후 `D-CFG-03` 추가 가능 |
| CSV / 표 출력 | U-FMT-01 | Strategy 1종 Green = OCP 입증, 나머지 데모 |
| 테스트 코드로 검증 | D-CNV-* | 도메인 TC가 핵심 |

---

## 4. RED 실행 순서

```
Phase 1 — Core (Activities 2~3)
────────────────────────────────
Track B:  D-CNV-01 → D-CNV-02 → D-CNV-03 → D-CNV-04
Track A:  U-IN-01 → U-IN-02 → U-IN-03 → U-IN-04 → U-IN-05 → U-OUT-01
── Gate 1: Core Green ──

Phase 2 — Extension (Activity 4)
────────────────────────────────
Track B:  D-CFG-01 → D-CFG-02 → D-REG-01 → D-REG-02
Track A:  U-FMT-01
── Gate 2: Full PRD Green ──
```

**원칙:** Track B 도메인 TC를 먼저 Green → Track A 경계 TC 통합. Phase 2 진행 중 Phase 1 TC 10개 회귀 Green 유지.

---

## 5. 이전 버전 매핑 (v1 → v2)

| 항목 | v1 (이전) | v2 (현재) |
|------|-----------|-----------|
| Track 기준 | Phase (기본 vs 추가) | Layer (Boundary vs Domain) |
| REQ 수 | 21 | 16 |
| TC 수 | 30 | 15 |
| ARCH TC | TC-A-ARCH-001~004 (4개) | 구조 + D-REG/U-FMT 확장으로 검증 |
| TC-A-BIZ-001~006 | 6개 | D-CNV-01~04 (4개) |
| TC-A-VAL-001~004 | 4개 | U-IN-01~05 (5개) |
| TC-B-FMT-001~004 | 4개 | U-FMT-01 (1개) |

### Green 후 선택적 추가 TC

| Test ID | Given → Then | 추가 시점 |
|---------|--------------|-----------|
| D-CFG-03 | YAML 설정 로드 | Phase 2 여유 시 |
| U-FMT-02 | format=CSV → 헤더 + 행 | Phase 2 여유 시 |
| U-FMT-03 | format=table → 표 형태 출력 | Phase 2 여유 시 |

---

## 6. 커버리지 요약

| Phase | Track A | Track B | TC | 구현 상태 |
|-------|---------|---------|-----|-----------|
| 1 Core | 6 | 4 | 10 | ❌ 미구현 |
| 2 Extension | 1 | 4 | 5 | ❌ 미구현 |
| **합계** | **7** | **8** | **15** | ❌ 미구현 |
