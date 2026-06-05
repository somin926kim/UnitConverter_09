# TDD RED — 실패 테스트 먼저

Unit Converter **Dual-Track TDD** — **RED 단계만**. GREEN/REFACTOR·`unit_converter/` 구현은 하지 않는다.  
절차 SSOT: `.cursor/skills/unit-converter-tdd/SKILL.md` · Test ID: `reference.md` · 규칙: `.cursor/rules/unit-converter-red.mdc`

---

## 필수 선언

**응답 첫 줄:**

```
Phase: red | Track: A|B | Test ID: D-CNV-01 (또는 U-IN-01)
```

한국어. git commit은 **1 RED 묶음 = 1 커밋** (`[RED] …`). push는 사용자 요청 시만.

---

## RED 단계 금지 규칙

- **RED 단계에서 구현 코드 작성 금지**
- **`pytest.fail("RED: ...")` 허용**
- **`skip` / `xfail` 금지**
- **1 RED 묶음 = 1 커밋**

---

## 절차

1. **Test ID 확인** — `docs/prd_test_traceability.md` · `.cursor/skills/unit-converter-tdd/reference.md`
2. **Track 확인** — B(Domain) 선행 권장: `D-CNV-*` → `U-IN-*` → `U-OUT-01`
3. **파일** — `tests/test_domain.py` (D-*) · `tests/test_boundary.py` (U-*)
4. **AAA 테스트** — Given/When/Then 주석
5. **Then** — `pytest.fail("RED: {TestID} — …")` 한 줄. assert 본문·통과 더미 없음
6. **`tests/`만 수정** — `unit_converter/` · `config/` · `UnitConverter.py` **수정 금지**
7. **pytest** — 대상 **FAIL** (exit ≠ 0) 확인 후 보고

**Track B RED 권장 순서:** D-CNV-01 → 02 → 03 → 04  
**Track A RED 권장 순서:** U-IN-01 → 02 → 03 → 04 → 05 → U-OUT-01

---

## pytest 예시 (bash)

```bash
python -m pytest tests/test_domain.py::test_d_cnv_01_to_meter_feet -v
python -m pytest tests/test_boundary.py -k "u_in_03" -v
python -m pytest tests/ -v
```

**RED 성공 기준:** exit code ≠ 0 · FAIL에 Test ID · `pytest.fail("RED: …")` 또는 ImportError.

---

## 보고

```markdown
## RED 보고
- Test ID / Track / Phase:
- pytest: (명령 + exit code + FAIL 한 줄)
- 변경 파일: tests/ … 만
- 커밋: [RED] … (1 묶음 = 1 커밋)
```

---

## 금지

| 금지 | 이유 |
|------|------|
| `unit_converter/` · `config/` 작성 | RED는 실패 테스트만 |
| `UnitConverter.py` 리팩터 | GREEN/REFACTOR까지 보류 |
| Track B Domain `@patch` | Dual-Track — mock-free |
| assert 완화·더미 통과 | Loop 우회 |
| `pytest.skip` · `xfail` | RED 증거 훼손 |
