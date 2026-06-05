# SPEC — 설계 문서만

Unit Converter **SPEC 단계**. **프로덕션·테스트 코드 작성 금지.**

---

## 필수 선언

**응답 첫 줄:**

```
Phase: spec
```

---

## 허용

- `docs/*.md` 작성·수정 (`spec_analysis`, `prd_test_traceability`, `dual_track_design`, `architecture`)
- `.cursor/rules/`, `.cursor/skills/`, `.cursor/commands/` 정의
- 레거시 `UnitConverter.py` **분석만** (수정 ❌)

## 금지

| 금지 | 대상 |
|------|------|
| 구현 | `unit_converter/`, `config/` |
| 테스트 | `tests/` |
| RED 우회 | SPEC에서 pytest·구현 선행 |

## SSOT 문서

| 문서 | 내용 |
|------|------|
| `docs/architecture.md` | REFACTOR 목표 패키지 · FR/NFR |
| `docs/dual_track_design.md` | Dual Track RED 15 TC |
| `docs/prd_test_traceability.md` | REQ ↔ Test ID |

## 커밋

`[SPEC] …` — 문서·Cursor 설정만.
