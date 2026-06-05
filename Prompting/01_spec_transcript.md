# UnitConverter_09 — SPEC 단계 Export Transcript (01)
_Exported on 2026-06-05 from Cursor (Agent) — UnitConverter_09 · 브랜치 `spec`_

> 대화 요약본. 상세 산출은 `Report/01_spec_report.md`, `docs/`, `.cursor/` 참고.

---

## 1. 레거시 분석 · `docs/spec_analysis.md`

**User**

`@README.md` `@UnitConverter.py` — 레거시 코드 스멜과 PRD Gap을 목록으로 정리. OCP/SRP 위반, 입력 검증 부족, 확장성 문제 관점. 결과: `docs/spec_analysis.md`

**Cursor**

`UnitConverter.py`(37줄, 단일 `main()`)와 README 분석. OCP 5건(if/elif, 하드코딩 비율·출력), SRP 5건(God Function), 입력 검증 Gap(음수·빈 토큰·공백), 확장성 9건. `docs/spec_analysis.md` 작성.

**User**

방금 만든 문서 commit. `[SPEC]` 말머리.

**Cursor**

(Ask 모드로 커밋 불가 안내 후) Agent 모드에서 `b93b50b` — `[SPEC] Add legacy code smell and PRD gap analysis doc`

---

## 2. PRD → Test 추적표

**User**

README 요구사항 분석 → Requirement → Test ID 추적표. Requirement ID, 설명, Test ID, Track(A/B). `docs/prd_test_traceability.md`

**Cursor**

Track A=기본·품질, Track B=추가. REQ 21개, TC 30개(v1). `aa257c7` 커밋.

---

## 3. Dual Track 전략 (파일 생성 없음)

**User**

추적표 기반 Dual Track 전략 제안. Track A/B 구분, 왜 나눴는지 설명. 파일 생성 하지 말 것.

**Cursor**

- **Track A (Core):** 기본·품질·TC 18개 — 변환·검증·OCP/SRP
- **Track B (Extension):** 추가 요구·TC 12개 — 설정·등록·포맷
- README 구조·의존성·TDD·OCP 순서로 분리 이유 설명

---

## 4. Dual-Track RED 설계표 보완 (이미지 참고)

**User**

Dual track 예시 표 참고해 보완. 추적표 너무 복잡하면 업데이트 가능.

_(첨부: Dual-Track RED 설계표 — Track A UI/Boundary, Track B Domain/Logic)_

**Cursor (Ask 모드)**

- **축 변경:** Phase 기준 → **Layer 기준** (A=Boundary, B=Domain)
- TC 30 → 18 → **10(Minimal)** 제안
- 예시 표: `U-IN-01~03`, `U-OUT-01`, `D-CNV-01~03`, `D-REG-01`, `D-CFG-01`
- RED 순서: **Track B(Domain) 먼저** → Track A

**User**

총 몇 개에서 몇 개?

**Cursor**

TC **30 → 18 → 10**. REQ **21 → 19 → 11**(플랫).

**User**

이것도 좀 많은 것 같아.

**Cursor**

**10 TC** sweet spot 제안 (예시 표 9개 + JSON 1개). Green 후 `U-IN-04`, `D-CFG-02` 등 추가 가능.

---

## 5. 추적표 v3 (15 TC) · commit amend

**User**

15 TC 수준으로 만들고 commit amend.

**Cursor**

`prd_test_traceability.md` v3 전면 교체.

| Phase | Track A | Track B | TC |
|-------|---------|---------|-----|
| 1 Core | 6 | 4 | 10 |
| 2 Extension | 1 | 4 | 5 |
| **합계** | 7 | 8 | **15** |

추가: `D-CNV-04`, `U-IN-04`, `U-IN-05`, `D-CFG-02`, `D-REG-02`. amend `8a155fa` — `[SPEC] Simplify traceability to Dual-Track RED (15 TC)`

---

## 6. 최종 Dual Track 설계 · `docs/dual_track_design.md`

**User**

업데이트된 `prd_test_traceability.md` 기반 최종 dual track 설계표 작성.

**Cursor**

`dual_track_design.md` — RED 표, Gate 1/2, 실행 순서, REQ 16·TC 15. `4a77d74` → amend `9c30bf1` (Track A/B vs 실행 순서 B→A 명시 추가)

---

## 7. Track B가 Track A보다 먼저인 이유

**User**

왜 Track B가 Track A보다 먼저 나오지?

**Cursor**

- 의존성: Boundary는 Domain 위에 얹음 (`U-OUT-01`은 Converter 필요)
- TDD: Domain은 mock-free, Boundary는 I/O·통합
- SRP: 계산 실패 vs 검증 실패 분리
- **Track A/B = 레이어 이름**, **RED 순서 = B → A**

**User**

Track A — UI/Boundary, Track B — Domain/Logic 잖아.

**Cursor**

맞음. A/B는 레이어 구분이지 실행 순서가 아님. `dual_track_design.md`에 명시 추가 + amend `9c30bf1`.

---

## 8. 아키텍처 · FR/NFR (`docs/architecture.md`)

**User**

OCP/SRP Python 패키지 구조 제안, PRD FR/NFR 매핑. SPEC 단계만, 코드 변경 없음. `docs/architecture.md`

**Cursor**

`unit_converter/` (application/domain/infrastructure), FR 11, NFR 8, REFACTOR 적용 순서. `d20592d` 커밋.

**User**

(동일 요청 + Rule 예시)

RED 금지 규칙: 구현 금지, `pytest.fail` 허용, skip/xfail 금지, 1 RED=1 커밋

**Cursor**

`architecture.md` §12 RED 규칙 추가 (문서). 사용자 의도는 `.cursor/` 반영이었음 — 다음 턴에서 수정.

---

## 9. `.cursor/` Harness (의도 정정)

**User**

아니 — `.cursor/rules/`, `.cursor/skills/`, `.cursor/commands/` 만들 때 반영해달라는 뜻이었어.

**Cursor**

생성:

```
.cursor/rules/     project.mdc, red.mdc, refactor.mdc
.cursor/skills/unit-converter-tdd/   SKILL.md, reference.md
.cursor/commands/    tdd-red.md, tdd-green.md, spec-only.md
```

RED 규칙 verbatim 반영. `architecture.md`는 `.cursor/` SSOT 링크만 보완. `9416db0` 커밋.

**User**

commit 해줘

**Cursor**

완료 (`9416db0`).

**User**

.cursor 폴더 commit 해줘

**Cursor**

이미 `9416db0`에 포함됨 (8파일). 미추적: `.cursor.zip`만 존재.

---

## 10. SPEC 보고서 · Export Transcript

**User**

지금까지 SPEC 단계 작업 Report → `Report/01_spec_report.md`

**Cursor**

SPEC 보고서 작성 — Activities 1 + 선행 설계·Harness, 산출물·Git 6커밋·회고.

**User**

export transcript → `Prompting/01_spec_transcript.md`

**Cursor**

본 문서 작성.

---

## 11. SPEC 단계 Git 커밋 요약

| 커밋 | 메시지 |
|------|--------|
| `b93b50b` | [SPEC] Add legacy code smell and PRD gap analysis doc |
| `aa257c7` | [SPEC] Add PRD to Test ID traceability matrix |
| `9c30bf1` | [SPEC] Add final Dual Track design document |
| `8a155fa` | [SPEC] Simplify traceability to Dual-Track RED (15 TC) *(amend)* |
| `d20592d` | [SPEC] Add target package architecture with FR/NFR mapping |
| `9416db0` | [SPEC] Add Cursor rules, skills, commands for Dual-Track TDD |

---

## 12. 확정 Dual-Track RED (15 TC) — 스냅샷

### Track B — Domain (RED 1번째)

| Test ID | Given → Then |
|---------|--------------|
| D-CNV-01 | 1 feet → 0.3048 m |
| D-CNV-02 | 2.5 m → 8.20210 ft |
| D-CNV-03 | feet → yard, meter 경유 일관 |
| D-CNV-04 | 2.5 m → 2.73403 yard |
| D-CFG-01 | 손상 JSON → ConfigError |
| D-CFG-02 | valid units.json → 3단위 |
| D-REG-01 | cubit 등록 → 변환 가능 |
| D-REG-02 | cubit ↔ meter/feet/yard |

### Track A — Boundary

| Test ID | Given → Then |
|---------|--------------|
| U-IN-01 | `""` → Format error |
| U-IN-02 | `meter` → Format error |
| U-IN-03 | `meter:-1` → Negative |
| U-IN-04 | `mile:1` → Unknown unit |
| U-IN-05 | `:2.5` / `meter:` → Format error |
| U-OUT-01 | `meter:2.5` → ≥3줄 출력 |
| U-FMT-01 | format=JSON → 유효 JSON |

---

## 13. 산출물 ↔ Report 연결

| Prompting / Report | 파일 |
|--------------------|------|
| 본 Transcript | `Prompting/01_spec_transcript.md` |
| SPEC 보고서 | `Report/01_spec_report.md` |
| Gap 분석 | `docs/spec_analysis.md` |
| 추적표 | `docs/prd_test_traceability.md` |
| Dual Track 설계 | `docs/dual_track_design.md` |
| 패키지·FR/NFR | `docs/architecture.md` |
| Agent Harness | `.cursor/rules`, `skills`, `commands` |

---

## 14. 다음 단계 (대화에서 합의)

1. **RED:** `/tdd-red` · `tests/` only · `pytest.fail` · 1묶음=1커밋
2. **순서:** D-CNV-01 → … → U-OUT-01 → Phase 2
3. **금지:** `unit_converter/` · GREEN 전 `UnitConverter.py` 대규모 리팩터

---

_본 Export는 SPEC 단계 Cursor 세션의 대화 흐름을 요약한 것이다. 도구 호출·내부 추론은 생략했다._
