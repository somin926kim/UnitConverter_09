# TDD GREEN — 최소 구현

Unit Converter **GREEN 단계**. 지정 Test ID를 **통과**시키는 **최소 구현**만. REFACTOR(패키지 분리)는 하지 않는다.

절차: `.cursor/skills/unit-converter-tdd/SKILL.md` · Test ID: `reference.md`

---

## 필수 선언

**응답 첫 줄:**

```
Phase: green | Track: A|B | Test ID: D-CNV-01
```

---

## 절차

1. 대상 RED 테스트의 `pytest.fail` → **실제 assert**로 교체
2. **최소 코드**로 해당 TC만 Green (과도한 REFACTOR 금지)
3. `pytest` 대상 테스트 **PASS** 확인
4. 기존 Green TC **회귀 없음** 확인
5. 커밋: `[GREEN] …`

## 허용

- `UnitConverter.py` 최소 수정 또는 임시 모듈
- `tests/` assert 구현

## 금지 (REFACTOR까지)

- `unit_converter/` 전체 패키지 구조 이전 (`docs/architecture.md`는 REFACTOR 시)
- unrelated TC 대량 수정
- Track B Domain `@patch`

## 보고

```markdown
## GREEN 보고
- Test ID / Track:
- pytest: PASS (명령 + exit 0)
- 변경 파일:
- 다음: 다음 RED 또는 REFACTOR (사용자 지시)
```
