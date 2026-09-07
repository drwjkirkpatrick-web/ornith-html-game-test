# Ornith-1.0-9B HTML5 Game Coding Test

Detailed findings from testing **Ornith-1.0-9B-MTP-IQ3_M** on an iterative HTML5 canvas game development task.

## Overview

| Field | Value |
|-------|-------|
| Model | Ornith-1.0-9B-MTP-IQ3_M.gguf (4.4 GB) |
| Platform | NVIDIA Jetson (ARM64, 8 GB RAM) |
| Server | llama.cpp with 64K context, Q4 KV cache, FlashAttention |
| Date | September 7, 2026 |
| Steps completed | 3 of 5 (Step 4 OOM-killed) |

## Key Findings

1. **Valid code on every step** — All 3 completed steps passed `node --check` JS syntax validation with zero errors
2. **Genuine code comprehension** — Step 2: Ornith recognized gravity/jumping were already implemented and returned the file unchanged rather than duplicating code
3. **Clean output** — Zero code-fence artifacts, no CSS semicolon errors, no brace imbalance, no fragmentation
4. **OOM crash at Step 4** — 64K context + 4.4 GB model weights exceeded 8 GB RAM under memory pressure
5. **Dramatically outperforms DeepSeek R1 7B Q2_K** — which failed all 6 attempts with 6 confirmed failure patterns

## Test Steps

| Step | Prompt | Tokens | Speed | Result |
|------|--------|--------|-------|--------|
| 1 | Create HTML5 canvas + player + arrow keys | 5,445 | 9.5 tok/s | 19.6 KB valid HTML |
| 2 | Add gravity and jumping | 5,720 | 9.0 tok/s | Unchanged (already present) |
| 3 | Add platforms + collision detection | 6,808 | 8.6 tok/s | 24.4 KB valid HTML (+148 lines) |
| 4 | Add mobile touch controls | — | — | OOM killed (exit 137) |
| 5 | (Not reached) | — | — | — |

## Files

- `Ornith_HTML5_Game_Test_Report.pdf` — Full detailed report with tables
- `build_report.py` — PDF generation script
- `steps/step1.html` through `step3.html` — Generated game code
- `steps/step*_raw.json` — Full API responses with thinking traces
- `steps/step*_meta.json` — Generation metrics
- `thinking/step*_thinking.txt` — Reasoning traces saved for research

## Report

See `Ornith_HTML5_Game_Test_Report.pdf` for the full 9-page report with:
- Generation metrics tables
- Code validation results
- Thinking trace analysis
- Ornith vs DeepSeek R1 7B comparison
- OOM failure analysis
- Conclusions and recommendations