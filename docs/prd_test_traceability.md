# PRD → Test 추적표 (Requirement Traceability Matrix)

> **기준 문서:** `README.md`  
> **작성 일자:** 2026-06-05  
> **현재 테스트 코드:** 미구현 (Test ID는 구현 예정 TC 기준으로 정의)

---

## 1. Track 정의

| Track | 범위 | README 출처 | Activities |
|-------|------|-------------|------------|
| **A** | 기본 요구사항 · 비즈니스 로직 · 품질 요구사항 | 기본 요구사항, 비즈니스 로직, 품질 요구사항 | 2~3단계 (구현 + TC) |
| **B** | 추가 요구사항 | 추가 요구사항 | 4단계 (구현 + TC) |

---

## 2. ID 명명 규칙

| 구분 | 패턴 | 예시 |
|------|------|------|
| Requirement ID | `REQ-{Track}-{영역}-{순번}` | `REQ-A-FUNC-001` |
| Test ID | `TC-{Track}-{영역}-{순번}` | `TC-A-FUNC-001` |

**영역 코드**

| 코드 | 의미 |
|------|------|
| FUNC | 기능 (입력·출력·단위 지원) |
| BIZ | 비즈니스 로직 (변환 비율·계산) |
| ARCH | 아키텍처 (OCP, SRP) |
| VAL | 입력 검증 |
| CFG | 설정 외부화 |
| REG | 동적 단위 등록 |
| FMT | 출력 포맷 |

---

## 3. Requirement → Test ID 추적표

### 3.1 Track A — 기본 · 품질 요구사항

| Requirement ID | Requirement 설명 | 대응 Test ID | Track |
|----------------|------------------|--------------|-------|
| REQ-A-FUNC-001 | `unit:value` 형식(예: `meter:2.5`)으로 사용자 입력을 받는다 | TC-A-FUNC-001, TC-A-VAL-002 | A |
| REQ-A-FUNC-002 | 입력값을 **다른 모든 지원 단위**로 변환하여 출력한다 | TC-A-FUNC-002, TC-A-FUNC-003, TC-A-FUNC-004 | A |
| REQ-A-FUNC-003 | 현재 지원 단위: `meter`, `feet`, `yard` | TC-A-FUNC-002, TC-A-FUNC-003, TC-A-FUNC-004, TC-A-VAL-004 | A |
| REQ-A-FUNC-004 | 새 단위 추가 시 기존 코드 변경을 최소화한다 (OCP 설계 목표) | TC-A-ARCH-001, TC-A-ARCH-002 | A |
| REQ-A-FUNC-005 | 각 단위 간 변환 정확성을 테스트 코드로 검증한다 | TC-A-BIZ-001 ~ TC-A-BIZ-006 | A |
| REQ-A-BIZ-001 | `1 meter = 3.28084 feet` 비율로 변환한다 | TC-A-BIZ-001, TC-A-BIZ-002, TC-A-BIZ-004 | A |
| REQ-A-BIZ-002 | `1 meter = 1.09361 yard` 비율로 변환한다 | TC-A-BIZ-003, TC-A-BIZ-005, TC-A-BIZ-006 | A |
| REQ-A-BIZ-003 | feet ↔ yard 변환은 meter 기준 단위를 경유하여 계산한다 | TC-A-BIZ-004, TC-A-BIZ-005, TC-A-BIZ-006 | A |
| REQ-A-ARCH-001 | OCP를 만족하는 설계 (확장에 열림, 수정에 닫힘) | TC-A-ARCH-001, TC-A-ARCH-002 | A |
| REQ-A-ARCH-002 | SRP를 만족하는 클래스 구성 (책임별 분리) | TC-A-ARCH-003, TC-A-ARCH-004 | A |
| REQ-A-VAL-001 | 음수 입력값을 거부하고 적절한 오류를 반환한다 | TC-A-VAL-001 | A |
| REQ-A-VAL-002 | 잘못된 입력 형식(콜론 없음, 빈 값 등)을 거부한다 | TC-A-VAL-002, TC-A-VAL-003 | A |
| REQ-A-VAL-003 | 존재하지 않는 단위 입력 시 오류를 반환한다 | TC-A-VAL-004 | A |

### 3.2 Track B — 추가 요구사항

| Requirement ID | Requirement 설명 | 대응 Test ID | Track |
|----------------|------------------|--------------|-------|
| REQ-B-CFG-001 | 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드한다 | TC-B-CFG-001, TC-B-CFG-002, TC-B-CFG-003 | B |
| REQ-B-CFG-002 | 설정 파일 변경 시 코드 수정 없이 비율을 반영한다 | TC-B-CFG-002, TC-B-CFG-004 | B |
| REQ-B-REG-001 | 사용자 입력으로 새 단위와 비율을 동적으로 등록한다 (예: `1 cubit = 0.4572 meter`) | TC-B-REG-001, TC-B-REG-002 | B |
| REQ-B-REG-002 | 등록된 단위를 즉시 변환에 사용할 수 있다 | TC-B-REG-002, TC-B-REG-003 | B |
| REQ-B-FMT-001 | JSON 형태로 변환 결과를 출력할 수 있다 | TC-B-FMT-001 | B |
| REQ-B-FMT-002 | CSV 형태로 변환 결과를 출력할 수 있다 | TC-B-FMT-002 | B |
| REQ-B-FMT-003 | 표(table) 형태로 변환 결과를 출력할 수 있다 | TC-B-FMT-003 | B |
| REQ-B-FMT-004 | 출력 포맷(JSON / CSV / 표)을 선택할 수 있다 | TC-B-FMT-001, TC-B-FMT-002, TC-B-FMT-003, TC-B-FMT-004 | B |

---

## 4. Test ID 상세 목록

### 4.1 Track A — Test Cases

| Test ID | Test 설명 | 검증 Requirement | 유형 |
|---------|-----------|------------------|------|
| TC-A-FUNC-001 | `meter:2.5` 입력 시 파싱 성공, 단위·값 분리 | REQ-A-FUNC-001 | 기능 |
| TC-A-FUNC-002 | `meter` 입력 → feet, yard 포함 전 단위 출력 | REQ-A-FUNC-002, REQ-A-FUNC-003 | 기능 |
| TC-A-FUNC-003 | `feet` 입력 → meter, yard 포함 전 단위 출력 | REQ-A-FUNC-002, REQ-A-FUNC-003 | 기능 |
| TC-A-FUNC-004 | `yard` 입력 → meter, feet 포함 전 단위 출력 | REQ-A-FUNC-002, REQ-A-FUNC-003 | 기능 |
| TC-A-BIZ-001 | 1 meter → 3.28084 feet (정방향) | REQ-A-BIZ-001, REQ-A-FUNC-005 | 단위 변환 |
| TC-A-BIZ-002 | 3.28084 feet → 1 meter (역방향) | REQ-A-BIZ-001, REQ-A-FUNC-005 | 단위 변환 |
| TC-A-BIZ-003 | 1 meter → 1.09361 yard (정방향) | REQ-A-BIZ-002, REQ-A-FUNC-005 | 단위 변환 |
| TC-A-BIZ-004 | 1 feet → yard (meter 경유, feet↔yard) | REQ-A-BIZ-001, REQ-A-BIZ-003, REQ-A-FUNC-005 | 단위 변환 |
| TC-A-BIZ-005 | 1 yard → feet (meter 경유, feet↔yard) | REQ-A-BIZ-002, REQ-A-BIZ-003, REQ-A-FUNC-005 | 단위 변환 |
| TC-A-BIZ-006 | `meter:2.5` → feet ≈ 8.2, yard ≈ 2.7 (README 예시) | REQ-A-BIZ-001, REQ-A-BIZ-002, REQ-A-FUNC-002 | 단위 변환 |
| TC-A-ARCH-001 | 새 단위 클래스/등록 추가 시 기존 변환기 코드 수정 없음 | REQ-A-FUNC-004, REQ-A-ARCH-001 | 아키텍처 |
| TC-A-ARCH-002 | 새 출력 포맷 추가 시 변환 로직 코드 수정 없음 | REQ-A-ARCH-001 | 아키텍처 |
| TC-A-ARCH-003 | 파싱·검증·변환·출력이 별도 클래스/모듈로 분리됨 | REQ-A-ARCH-002 | 아키텍처 |
| TC-A-ARCH-004 | 변환 로직 단위 테스트 시 I/O(mock) 없이 실행 가능 | REQ-A-ARCH-002, REQ-A-FUNC-005 | 아키텍처 |
| TC-A-VAL-001 | 음수 값(`meter:-1`) 입력 시 오류 반환 | REQ-A-VAL-001 | 검증 |
| TC-A-VAL-002 | 콜론 없는 입력(`meter2.5`) 시 오류 반환 | REQ-A-VAL-002, REQ-A-FUNC-001 | 검증 |
| TC-A-VAL-003 | 빈 단위/값(`:2.5`, `meter:`) 입력 시 오류 반환 | REQ-A-VAL-002 | 검증 |
| TC-A-VAL-004 | 미지원 단위(`mile:1`) 입력 시 오류 반환 | REQ-A-VAL-003, REQ-A-FUNC-003 | 검증 |

### 4.2 Track B — Test Cases

| Test ID | Test 설명 | 검증 Requirement | 유형 |
|---------|-----------|------------------|------|
| TC-B-CFG-001 | JSON 설정 파일에서 단위·비율 로드 | REQ-B-CFG-001 | 설정 |
| TC-B-CFG-002 | YAML 설정 파일에서 단위·비율 로드 | REQ-B-CFG-001 | 설정 |
| TC-B-CFG-003 | 설정 파일 누락/손상 시 적절한 오류 처리 | REQ-B-CFG-001 | 설정 |
| TC-B-CFG-004 | 설정 파일 비율 변경 후 변환 결과 반영 | REQ-B-CFG-002 | 설정 |
| TC-B-REG-001 | `1 cubit = 0.4572 meter` 형식으로 단위 등록 | REQ-B-REG-001 | 동적 등록 |
| TC-B-REG-002 | 등록 직후 `cubit:N` 입력 변환 성공 | REQ-B-REG-001, REQ-B-REG-002 | 동적 등록 |
| TC-B-REG-003 | 등록된 cubit이 기존 3단위와 상호 변환됨 | REQ-B-REG-002 | 동적 등록 |
| TC-B-FMT-001 | JSON 포맷 출력 — 구조·값 검증 | REQ-B-FMT-001, REQ-B-FMT-004 | 출력 |
| TC-B-FMT-002 | CSV 포맷 출력 — 헤더·행 검증 | REQ-B-FMT-002, REQ-B-FMT-004 | 출력 |
| TC-B-FMT-003 | 표(table) 포맷 출력 — 가독성·값 검증 | REQ-B-FMT-003, REQ-B-FMT-004 | 출력 |
| TC-B-FMT-004 | 포맷 옵션 미지정 시 기본(표) 출력 | REQ-B-FMT-004 | 출력 |

---

## 5. 역추적 매트릭스 (Test → Requirement)

| Test ID | Track | 대응 Requirement ID |
|---------|-------|---------------------|
| TC-A-FUNC-001 | A | REQ-A-FUNC-001 |
| TC-A-FUNC-002 | A | REQ-A-FUNC-002, REQ-A-FUNC-003 |
| TC-A-FUNC-003 | A | REQ-A-FUNC-002, REQ-A-FUNC-003 |
| TC-A-FUNC-004 | A | REQ-A-FUNC-002, REQ-A-FUNC-003 |
| TC-A-BIZ-001 | A | REQ-A-BIZ-001, REQ-A-FUNC-005 |
| TC-A-BIZ-002 | A | REQ-A-BIZ-001, REQ-A-FUNC-005 |
| TC-A-BIZ-003 | A | REQ-A-BIZ-002, REQ-A-FUNC-005 |
| TC-A-BIZ-004 | A | REQ-A-BIZ-001, REQ-A-BIZ-003, REQ-A-FUNC-005 |
| TC-A-BIZ-005 | A | REQ-A-BIZ-002, REQ-A-BIZ-003, REQ-A-FUNC-005 |
| TC-A-BIZ-006 | A | REQ-A-BIZ-001, REQ-A-BIZ-002, REQ-A-FUNC-002 |
| TC-A-ARCH-001 | A | REQ-A-FUNC-004, REQ-A-ARCH-001 |
| TC-A-ARCH-002 | A | REQ-A-ARCH-001 |
| TC-A-ARCH-003 | A | REQ-A-ARCH-002 |
| TC-A-ARCH-004 | A | REQ-A-ARCH-002, REQ-A-FUNC-005 |
| TC-A-VAL-001 | A | REQ-A-VAL-001 |
| TC-A-VAL-002 | A | REQ-A-VAL-002, REQ-A-FUNC-001 |
| TC-A-VAL-003 | A | REQ-A-VAL-002 |
| TC-A-VAL-004 | A | REQ-A-VAL-003, REQ-A-FUNC-003 |
| TC-B-CFG-001 | B | REQ-B-CFG-001 |
| TC-B-CFG-002 | B | REQ-B-CFG-001, REQ-B-CFG-002 |
| TC-B-CFG-003 | B | REQ-B-CFG-001 |
| TC-B-CFG-004 | B | REQ-B-CFG-002 |
| TC-B-REG-001 | B | REQ-B-REG-001 |
| TC-B-REG-002 | B | REQ-B-REG-001, REQ-B-REG-002 |
| TC-B-REG-003 | B | REQ-B-REG-002 |
| TC-B-FMT-001 | B | REQ-B-FMT-001, REQ-B-FMT-004 |
| TC-B-FMT-002 | B | REQ-B-FMT-002, REQ-B-FMT-004 |
| TC-B-FMT-003 | B | REQ-B-FMT-003, REQ-B-FMT-004 |
| TC-B-FMT-004 | B | REQ-B-FMT-004 |

---

## 6. 커버리지 요약

| Track | Requirement 수 | Test Case 수 | 구현 상태 |
|-------|----------------|--------------|-----------|
| **A** | 13 | 18 | ❌ 미구현 |
| **B** | 8 | 12 | ❌ 미구현 |
| **합계** | **21** | **30** | ❌ 미구현 |

### 6.1 README Activities ↔ Track 매핑

| Activities 단계 | 내용 | Track | 해당 REQ 범위 |
|-----------------|------|-------|---------------|
| 2 | 기본·품질 요구사항 구현 | A | REQ-A-FUNC, REQ-A-BIZ, REQ-A-ARCH, REQ-A-VAL |
| 3 | 단위변환·입력 검증 TC | A | TC-A-BIZ-*, TC-A-VAL-*, TC-A-FUNC-* |
| 4 | 추가 요구사항 구현 및 TC | B | REQ-B-CFG, REQ-B-REG, REQ-B-FMT |

---

## 7. 참고

- README Overview 3항목(*"각 단위 변환 로직은 테스트 코드로 검증"*)은 **REQ-A-FUNC-005** 및 **TC-A-BIZ-*** 시리즈로 추적한다.
- 아키텍처 요구(OCP/SRP)는 **TC-A-ARCH-*** 로 구조·확장성을 검증하며, 순수 기능 TC만으로는 충족 여부를 판단할 수 없다.
- Track B TC는 Track A 변환·검증 TC를 기반으로 하되, 설정·등록·포맷 레이어를 추가 검증한다.
