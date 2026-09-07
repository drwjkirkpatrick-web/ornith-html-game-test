#!/usr/bin/env python3
"""Build the Ornith HTML5 Game Test Report PDF with wrapped table cells."""
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

OUT = "/home/walker/projects/ornith-html-game-test/Ornith_HTML5_Game_Test_Report.pdf"

page_size = letter
content_width = page_size[0] - 2 * 72  # 468pt

styles = getSampleStyleSheet()
cell_style = ParagraphStyle('Cell', parent=styles['BodyText'],
    fontSize=9, leading=12, spaceBefore=0, spaceAfter=0)
header_style = ParagraphStyle('Hdr', parent=cell_style,
    fontName='Helvetica-Bold', textColor=colors.black)
small_style = ParagraphStyle('Small', parent=styles['BodyText'],
    fontSize=9, leading=13)

story = []

def h(text, level=1):
    story.append(Paragraph(text, styles[f'Heading{level}']))

def p(text):
    story.append(Paragraph(text, small_style))
    story.append(Spacer(1, 6))

def t(rows, col_fractions, header=True):
    """Build a table with wrapped cells. rows[0] = header if header=True."""
    col_widths = [content_width * f for f in col_fractions]
    wrapped = []
    for ri, row in enumerate(rows):
        wr = []
        for cell in row:
            text = str(cell) if cell else ""
            s = header_style if (ri == 0 and header) else cell_style
            wr.append(Paragraph(text, s))
        wrapped.append(wr)
    tbl = Table(wrapped, colWidths=col_widths, repeatRows=1 if header else 0)
    style_list = [
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]
    if header:
        style_list.append(("BACKGROUND", (0,0), (-1,0), colors.lightgrey))
    tbl.setStyle(TableStyle(style_list))
    story.append(tbl)
    story.append(Spacer(1, 10))

# ========== PAGE 1: Title + Summary + Config ==========
h("Ornith-1.0-9B HTML5 Game Coding Test", 1)
p("Detailed Findings Report &mdash; September 7, 2026")
p("<b>Model:</b> Ornith-1.0-9B-MTP-IQ3_M (4.4 GB GGUF, IQ3_M quantization, MTP-enabled)")
p("<b>Platform:</b> NVIDIA Jetson (ARM64), 8 GB RAM, llama.cpp server, 64K context, Q4 KV cache, FlashAttention on, all layers on GPU")
p("<b>Objective:</b> Test Ornith-1.0-9B's ability to build an HTML5 canvas game across 5 iterative steps, evaluating code quality, reasoning capability, and stability. Compare findings against prior DeepSeek R1 7B Q2_K testing.")

h("Executive Summary", 2)
p("Ornith-1.0-9B at IQ3_M quantization successfully produced syntactically valid HTML5/JavaScript code across all three completed steps. Unlike DeepSeek R1 7B Q2_K (which failed catastrophically with 6 confirmed failure patterns), Ornith generated clean, runnable single-file HTML with zero syntax errors on every attempt. The model demonstrated genuine code comprehension &mdash; in Step 2, it correctly recognized that gravity and jumping were already implemented in the Step 1 output and declined to duplicate the code. However, the test was cut short at Step 4 when the llama-server process was OOM-killed (exit code 137) due to memory pressure on the 8 GB Jetson, highlighting a critical infrastructure constraint for this model's 64K context window.")

h("Test Configuration", 2)
t([
    ["Parameter", "Value"],
    ["Model", "Ornith-1.0-9B-MTP-IQ3_M.gguf"],
    ["File size", "4.4 GB"],
    ["Quantization", "IQ3_M"],
    ["Server", "llama.cpp (llama-server)"],
    ["Context window", "65,536 tokens"],
    ["KV cache", "Q4_0 (both key and value)"],
    ["Flash attention", "Enabled"],
    ["GPU layers", "99 (all)"],
    ["Threads", "6"],
    ["Batch size", "512, ub=128"],
    ["Chat template", "Jinja (--jinja)"],
    ["Temperature", "0.7"],
    ["Max tokens", "100,000 (unlimited ceiling)"],
    ["Platform", "NVIDIA Jetson (ARM64, 8 GB RAM)"],
    ["GUI/GDM", "Off (for RAM availability)"],
    ["Ollama", "Off"],
    ["KV cache persistence", "~/.llama-kv-cache/ (2TB NVMe)"],
], [0.38, 0.62])

story.append(PageBreak())

# ========== PAGE 2: Step Results ==========
h("Step-by-Step Results", 2)

h("Generation Metrics Summary", 3)
t([
    ["Step", "Prompt", "Prompt Tok", "Comp Tok", "tok/s", "Time (s)", "Think chars", "Answer chars", "Finish"],
    ["1", "Create HTML5 canvas + player + arrow keys", "66", "5,445", "9.5", "571.5", "795", "19,504", "stop"],
    ["2", "Add gravity and jumping", "5,365", "5,720", "9.0", "632.1", "1,491", "20,078", "stop"],
    ["3", "Add platforms + collision detection", "5,369", "6,808", "8.6", "787.8", "988", "24,260", "stop"],
    ["4", "Add mobile touch controls", "5,369*", "&mdash;", "&mdash;", "&mdash;", "&mdash;", "&mdash;", "OOM KILLED"],
    ["5", "(Not reached)", "&mdash;", "&mdash;", "&mdash;", "&mdash;", "&mdash;", "&mdash;", "&mdash;"],
], [0.06, 0.28, 0.10, 0.09, 0.07, 0.08, 0.09, 0.10, 0.13])

p("*Step 4 prompt tokens estimated (payload sent but server crashed during generation).")
p("Speed degraded slightly across steps (9.5 to 8.6 tok/s) as context grew from 66 to 5,369 prompt tokens. Each step loaded the full prior code as context for continuity. Total generation time for 3 steps: ~33 minutes.")

h("Code Validation Results", 3)
t([
    ["Check", "Step 1", "Step 2", "Step 3"],
    ["HTML size (bytes)", "19,636", "19,636", "24,416"],
    ["HTML lines", "584", "584", "696"],
    ["JS size (chars)", "17,471", "17,471", "22,231"],
    ["&lt;!DOCTYPE html&gt;", "PASS", "PASS", "PASS"],
    ["Closing &lt;/html&gt;", "PASS", "PASS", "PASS"],
    ["&lt;canvas&gt; element", "PASS", "PASS", "PASS"],
    ["ArrowUp key handling", "PASS", "PASS", "PASS"],
    ["keydown listener", "PASS", "PASS", "PASS"],
    ["requestAnimationFrame", "PASS", "PASS", "PASS"],
    ["gravity references", "&mdash;", "3", "3"],
    ["jump references", "&mdash;", "6", "6"],
    ["platform references", "&mdash;", "&mdash;", "42"],
    ["collision references", "&mdash;", "&mdash;", "7"],
    ["AABB/Rect collision", "&mdash;", "&mdash;", "PASS"],
    ["node --check (JS syntax)", "VALID", "VALID", "VALID"],
    ["Code fence artifacts", "0", "0", "0"],
    ["Identical to prior step", "&mdash;", "YES (no change)", "NO (+148 lines)"],
], [0.38, 0.21, 0.21, 0.20])

p("All three completed steps passed JS syntax validation via node --check. Zero code fence artifacts leaked into output files. No CSS semicolon-to-comma errors, no brace imbalance, no output fragmentation.")

story.append(PageBreak())

# ========== PAGE 3: Thinking Analysis ==========
h("Thinking Trace Analysis", 2)
p("Ornith is a reasoning model (MTP = Multi-Token Prediction) that produces a reasoning_content thinking trace before the final answer. The thinking traces were saved for research at ~/projects/ornith-html-game-test/thinking/.")

h("Step 1 Thinking (795 chars)", 3)
p("Ornith planned a 5-point implementation: (1) HTML canvas element, (2) player sprite drawn programmatically with geometric shapes, (3) arrow key controls, (4) visual feedback/ground, (5) particles or effects for polish. It also noted: smooth movement with bounds checking, responsive canvas, clean code structure. It chose a space-themed platformer style with collectibles &mdash; going well beyond the minimal prompt requirements.")

h("Step 2 Thinking (1,491 chars) &mdash; Code Comprehension", 3)
p("This was the most notable finding. Ornith reviewed the Step 1 code and correctly identified that gravity and jumping were ALREADY implemented: 'Gravity is already applied in player.update() with this.vy += CONFIG.GRAVITY. Jumping is already implemented with Space/ArrowUp/KeyW. Ground collision: Sets vy to 0 and grounded to true.' It concluded: 'The game already HAS gravity and jumping. I should keep the code as-is since the gravity and jumping mechanics are already functional.' It returned the file unchanged rather than duplicating or breaking existing code.")
p("This demonstrates genuine code reading comprehension &mdash; the model parsed its own prior output, identified existing features, and made a correct no-op decision. This is qualitatively different from models that blindly re-implement regardless of existing state.")

h("Step 3 Thinking (988 chars)", 3)
p("Ornith planned a proper platform system with 5 components: (1) platform data structure (x, y, width, height, color), (2) platform rendering, (3) modified collision logic, (4) pre-positioned platforms at varied heights, (5) collision handling for landing on top, no pass-through, and multiple simultaneous contacts (highest platform wins). It mentioned AABB rectangle collision in its thinking. The implementation added 148 lines with 42 platform references, 7 collision references, and Rect/AABB structures.")

h("Thinking Trace Metrics", 2)
t([
    ["Step", "Think chars", "~Think tok", "Planning depth", "Code comprehension"],
    ["1", "795", "~200", "5-point plan + extra features", "N/A (first step)"],
    ["2", "1,491", "~370", "Reviewed existing code line-by-line", "YES &mdash; identified existing gravity/jump"],
    ["3", "988", "~250", "5-component platform system design", "YES &mdash; modified existing collision logic"],
], [0.08, 0.14, 0.14, 0.32, 0.32])

story.append(PageBreak())

# ========== PAGE 4: Comparison + OOM ==========
h("Comparison: Ornith-1.0-9B vs DeepSeek R1 7B Q2_K", 2)
p("Both models were tested on the same HTML5 game coding task on the same Jetson hardware. The contrast is stark.")

t([
    ["Metric", "Ornith-1.0-9B IQ3_M", "DeepSeek R1 7B Q2_K"],
    ["Quantization", "IQ3_M (4.4 GB)", "Q2_K (~2.9 GB)"],
    ["JS syntax valid (node --check)", "3/3 PASS", "0/6 PASS (all failed)"],
    ["Code fence artifacts", "0", "Frequent"],
    ["CSS semicolons as commas", "Never", "Confirmed failure pattern"],
    ["Output fragmentation", "Never (single file)", "Confirmed &mdash; multiple blocks"],
    ["Invented API calls", "Never", "Confirmed (e.g. createWaveshape)"],
    ["Brace imbalance (>5K chars)", "Never", "Confirmed failure pattern"],
    ["Output truncation mid-function", "Never", "Confirmed failure pattern"],
    ["Duplicate function loops", "Never", "Confirmed (rep_penalty < 1.15)"],
    ["Code comprehension", "YES (Step 2 no-op)", "Not observed"],
    ["Reasoning trace quality", "Clear, structured plans", "N/A (not a reasoning model)"],
    ["Steps completed", "3 of 5 (OOM crash)", "6 attempts, all failed"],
    ["Recommendation", "Suitable for code generation", "Use Q4_K_M or higher"],
], [0.38, 0.31, 0.31])

p("Key takeaway: Ornith-1.0-9B at IQ3_M produces clean, valid HTML5/JavaScript code. DeepSeek R1 7B at Q2_K cannot. The quantization difference (IQ3_M vs Q2_K) is significant &mdash; IQ3_M preserves enough precision for coherent code generation while Q2_K does not. However, the IQ3_M file is 4.4 GB vs 2.9 GB, consuming more of the Jetson's limited 8 GB RAM.")

h("Infrastructure Failure: Step 4 OOM Kill", 2)
p("Step 4 (Add mobile touch controls) was initiated successfully. The llama-server received the payload (26 KB, ~5,369 prompt tokens including full Step 3 code) and began generation. However, the server process was killed mid-generation with exit code 137 (SIGKILL by OOM killer).")

t([
    ["Factor", "Value"],
    ["Step attempted", "4 &mdash; Add mobile touch controls"],
    ["RAM at crash", "~320 MB available (of 7.4 GB)"],
    ["Process exit code", "137 (SIGKILL / OOM)"],
    ["Context window", "65,536 tokens"],
    ["KV cache memory (Q4)", "~28 KB/token x 65K = ~1.8 GB"],
    ["Model weights in RAM", "~4.4 GB (IQ3_M)"],
    ["Other processes", "Hermes gateway (270 MB), Chromium headless (50 MB)"],
    ["Root cause", "Context + weights + system overhead exceeded 8 GB"],
    ["Recovery attempts", "3 restart attempts &mdash; all OOM-killed within 42s"],
    ["RAM after crash", "6.4 GB free (model unloaded)"],
], [0.38, 0.62])

p("The 64K context window is the primary memory consumer. With Q4 KV cache at ~28 KB/token, the full 65K context requires ~1.8 GB just for KV state. Combined with 4.4 GB model weights and system overhead, the 8 GB Jetson cannot sustain the server under memory pressure. Steps 1-3 succeeded because the context was smaller at start time. Step 4 failed because accumulated context (prior code + conversation) pushed total memory over the limit.")
p("Mitigation options: (1) Reduce context to 32K, (2) Use a smaller quantization (IQ2_XXS), (3) Run with fewer concurrent processes, (4) Enable swap (3.7 GB swap was available but insufficient), (5) Use the Hermes 3 3B Q5 model (smaller footprint) for longer iterative sessions.")

story.append(PageBreak())

# ========== PAGE 5: Code Summary + Conclusions + Files ==========
h("Code Output Summary", 2)
p("<b>Step 1:</b> Ornith produced a 584-line (19.6 KB) single-file HTML5 game titled 'Canvas Player Movement'. Features: canvas element, programmatic player sprite (geometric shapes), arrow key + WASD movement, Space/Up/W to jump, gravity system, ground collision, collectible items (coins), particle effects, score display, animated background gradient, responsive layout. This exceeded the prompt scope &mdash; the minimal ask was just 'player sprite that moves with arrow keys' but Ornith built a full platformer.")
p("<b>Step 2:</b> File returned unchanged (19,636 bytes, identical to Step 1). Ornith correctly identified gravity and jumping were already present and declined to duplicate code. The thinking trace shows line-by-line verification of existing implementation.")
p("<b>Step 3:</b> File grew to 696 lines (24.4 KB), titled 'Platform Adventure'. Added 148 lines: platform data structure (array of objects with x, y, width, height, color), platform rendering with visual styling, AABB rectangle collision detection, landing-on-top logic, multi-platform contact resolution (highest platform wins), pre-positioned platforms at varied heights. All prior features preserved.")

h("Conclusions", 2)
p("1. Ornith-1.0-9B at IQ3_M is a capable code generation model for HTML5/JavaScript. It produced valid, runnable code on every completed step with zero syntax errors.")
p("2. The model demonstrates genuine code comprehension &mdash; it reads and understands existing code before making changes, correctly avoiding duplicate implementations.")
p("3. The reasoning (thinking) traces are concise (200-370 tokens) and well-structured, providing useful insight into the model's planning process.")
p("4. The 64K context window is unsustainable on an 8 GB Jetson for iterative sessions. Step 4 OOM-killed the server. 32K context or a smaller model is recommended for multi-step workflows.")
p("5. Ornith dramatically outperforms DeepSeek R1 7B Q2_K on code generation. The IQ3_M quantization preserves enough precision for coherent output, while Q2_K does not.")
p("6. Speed (8.6-9.5 tok/s) is adequate for development but slow for interactive use. Total generation time for 3 steps was ~33 minutes.")

h("Files Saved for Research", 2)
t([
    ["File", "Contents"],
    ["steps/step1.html", "Step 1 game output (19.6 KB)"],
    ["steps/step2.html", "Step 2 output (identical to step1)"],
    ["steps/step3.html", "Step 3 output with platforms (24.4 KB)"],
    ["steps/step1_raw.json", "Full API response with thinking + answer"],
    ["steps/step2_raw.json", "Full API response"],
    ["steps/step3_raw.json", "Full API response"],
    ["steps/step1_meta.json", "Generation metrics"],
    ["steps/step2_meta.json", "Generation metrics"],
    ["steps/step3_meta.json", "Generation metrics"],
    ["thinking/step1_thinking.txt", "Reasoning trace (795 chars)"],
    ["thinking/step2_thinking.txt", "Reasoning trace (1,491 chars)"],
    ["thinking/step3_thinking.txt", "Reasoning trace (988 chars)"],
], [0.42, 0.58])
p("All files at: ~/projects/ornith-html-game-test/")

# Build with page numbers
def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(page_size[0] / 2.0, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=page_size,
    leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72,
    title="Ornith-1.0-9B HTML5 Game Coding Test - Detailed Findings",
    author="Walker Kirkpatrick / Hermes Agent")
doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)
print(f"PDF created: {OUT}")