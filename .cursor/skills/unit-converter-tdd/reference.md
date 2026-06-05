# Unit Converter — Test ID Reference

> SSOT: `docs/prd_test_traceability.md` · `docs/dual_track_design.md`

## Track · Phase

| Track | Layer | TC | RED 순서 |
|-------|-------|-----|----------|
| B | Domain | `D-*` | **1번째** |
| A | Boundary | `U-*` | **2번째** |

## Phase 1 — Core (10 TC)

| Test ID | Given → Then |
|---------|--------------|
| D-CNV-01 | 1 feet → 0.3048 m (±ε) |
| D-CNV-02 | 2.5 m → 8.20210 ft |
| D-CNV-03 | feet → yard, meter 경유 일관 |
| D-CNV-04 | 2.5 m → 2.73403 yard |
| U-IN-01 | `""` → Format error |
| U-IN-02 | `meter` → Format error |
| U-IN-03 | `meter:-1` → Reject negative |
| U-IN-04 | `mile:1` → Unknown unit |
| U-IN-05 | `:2.5` / `meter:` → Format error |
| U-OUT-01 | `meter:2.5` → 출력 ≥ 3줄 |

## Phase 2 — Extension (5 TC)

| Test ID | Given → Then |
|---------|--------------|
| D-CFG-01 | 손상 JSON → ConfigError |
| D-CFG-02 | valid units.json → 3단위 |
| D-REG-01 | cubit=0.4572 m 등록 → 변환 가능 |
| D-REG-02 | cubit ↔ meter/feet/yard |
| U-FMT-01 | format=JSON → 유효 JSON |

## FR/NFR (요약)

| ID | 요약 |
|----|------|
| FR-01~03 | 입력·전단위 출력·3단위 |
| FR-04 | OCP 단위 확장 |
| FR-05~07 | m↔ft↔yard 비율 |
| FR-08 | TC 검증 |
| FR-09~11 | 설정·등록·포맷 |
| NFR-01~02 | OCP · SRP |
| NFR-03~05 | 입력 검증 |
| NFR-06~08 | mock-free · config · CLI |

상세: `docs/architecture.md` §5
