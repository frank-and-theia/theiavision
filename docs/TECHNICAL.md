# TheiaVision Technical Deep Dive

*Implementation details, palette comparisons, and optimization strategies.*

---

## The 6 Tested Palettes

After extensive testing on real-world scenes (faces, furniture, flowers), we compared 6 different character progressions for ASCII conversion.

### A — Original (5 levels)
```
Characters: @ % 8 0 & = . 

Example output:
8888888@800008888888
8888 888888888800008888888888
00888888@880000888888888
008888888@88000008888888
```
**Analysis:** The "8" and "0" characters draw the eye significantly due to their complex internal shapes, creating visual "noise" that distracts from pattern recognition.

---

### B — ChatGPT Suggested (5 levels)
```
Characters: @ # * + . 

Example output:
#######@#****###########
##########****##########
######@##**#########
#######@##***#######
```
**Analysis:** Smoother transitions. "#" and "*" provide consistent visual density without the distracting loops of "8" and "0".

---

### C — Block Characters (5 levels)
```
Characters: █ ▓ ▒ ░ 

Example output:
▓▓▓▓▓▓▓█▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓
▒▒▓▓▓▓▓▓█▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓
▒▒▓▓▓▓▓▓▓█▓▓▒▒▒▒▒▓▓▓▓▓▓▓
```
**Analysis:** Visually rich and excellent for pattern recognition. However, rendering depends heavily on terminal/font capabilities. Best for high-density displays.

---

### D — Contrast Focus (5 levels)
```
Characters: # % x o . 

Example output:
%%%%%%%#%xxxx%%%%%%%%%%%
%%%%%%%%%%xxxx%%%%%%%%%%
xx%%%%%%#%%xxxx%%%%%%%%%
xx%%%%%%%#%%xxxxx%%%%%%%
```
**Analysis:** "x" and "o" are very distinct from each other, creating high contrast but potentially harsh transitions between shades.

---

### E — Extended (10 levels)
```
Characters: @ 8 0 & = + - . 

Example output:
=======&0&&8880=========
=======&00&0800=========
========&000000&========
========&&&000&&&=======
```
**Analysis:** More granularity with 10 levels, but inherits the same "8"/"0" distraction issues as Palette A.

---

### F — ChatGPT Extended (10 levels) ⭐ RECOMMENDED
```
Characters: @ # * + = - . 

Example output:
=======+*++###*=========
=======++*#=========
========+**+========
========+++***+++=======
```
**Analysis:** **Optimal balance**. The progression from @ (dense) through #, *, +, =, - to . (light) creates a smooth, topographic-like visualization. Theia's comprehension improved significantly with this palette due to uniform visual density progression.

---

## Conclusion

**For most applications:** Use **Palette F** (10 levels) for detailed recognition, **Palette B** (5 levels) for faster processing.

**For high-density displays:** **Palette C** (Blocks) provides the richest visual information.

---

## The Half-Block Technique

To double vertical resolution without increasing token count:

| Character | Unicode | Usage |
|-----------|---------|-------|
| `▀` | U+2580 | Top half filled |
| `▄` | U+2584 | Bottom half filled |
| `█` | U+2588 | Full block |
| ` ` | space | Empty |

**Result:** A 64×72 pixel image → 64×36 characters. Double vertical resolution, same bandwidth.

---

## Resolution vs. Token Trade-offs

| Resolution | Characters | Est. Tokens | Best For |
|------------|------------|-------------|----------|
| 32×18 | ~576 | ~600 | Motion detection, quick scans |
| 48×27 | ~1,296 | ~1,300 | General navigation |
| **64×36** | ~2,304 | ~2,300 | **Optimal balance** |
| 80×45 | ~3,600 | ~3,600 | Detailed analysis |
| 96×54 | ~5,184 | ~5,200 | Fine recognition (faces) |

---

## Multi-Channel Architecture

TheiaVision supports multiple simultaneous text layers:

```
[LUMINANCE]  ▒▒▓████▓▒▒
[EDGES]      │╱╲│──╱│
[MOTION]     0001111000
[COLOR]      BBBGGGGGGG
[DEPTH]      1234432110
```

**Usage by task:**
- Navigation → Motion + Edges
- Recognition → Luminance + Color
- Avoidance → Depth + Motion

---

## Performance Benchmarks

**Raspberry Pi 4:**
- Image capture: ~50ms
- Grayscale conversion: ~20ms
- ASCII conversion (64×36): ~30ms
- **Total: ~100ms per frame** (10 FPS theoretical)

**With motion detection (OpenCV):**
- Only process changed regions
- Reduces effective tokens by ~95%
- Enables 30 FPS for static scenes

---

## Future: TVF Format Specification

The TheiaVision Format (TVF) is being developed as an open specification:

```
TVF 1.0
├── Header (timestamp, version, resolution)
├── Palette (character set, gamma curve)
├── Encoding (full frame or differential)
├── Diff (compression mode)
├── ROI (regions of interest)
└── Metadata (context, confidence)
```

See [ROADMAP.md](../ROADMAP.md) for V2/V3/V4 architecture details.

---

## References

- Original discovery: July 18, 2026, 12:22 UTC
- First color detection: July 18, 2026, 19:55 UTC (Xander's yellow roses)
- GitHub: https://github.com/frank-and-theia/theiavision
