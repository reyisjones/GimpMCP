# 🎬 Animated GIF Generation Guide

## Overview

The animated GIF generator creates sequences of images from text prompts and compiles them into smooth animations. Perfect for creating animated storyboards, demonstrations, or creative visual sequences.

---

## Quick Start

### Basic Usage

```bash
./generate_animation.sh \
  "A sunrise over mountains" \
  "Morning light on peaks" \
  "Full daylight landscape" \
  "mountain_sunrise"
```

This creates an animated GIF with 3 frames saved as `animations/mountain_sunrise.gif`.

---

## Features

### ✨ Key Capabilities

- **Automated Frame Generation**: Creates individual PNG frames from text descriptions
- **AI-Powered**: Uses Stable Diffusion for high-quality frames
- **Frame Validation**: Ensures all frames are generated successfully before compilation
- **Configurable**: Control frame rate, resolution, and output format
- **Interpolation**: Generate smooth transitions between keyframes
- **Batch Processing**: Handle multiple animations efficiently

### 🎯 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--frame-rate` | Frames per second | 10 fps |
| `--width` | Frame width in pixels | 512px |
| `--height` | Frame height in pixels | 512px |
| `--use-ai` | Enable AI generation | Required flag |
| `--loop` | Loop count (0=infinite) | 0 |
| `--interpolate` | Frames between prompts | 1 |

---

## Usage Examples

### Example 1: Simple 3-Frame Animation

```bash
./generate_animation.sh \
  "A seed in soil" \
  "A sprout emerging" \
  "A small plant with leaves" \
  "plant_growth"
```

**Output**: `animations/plant_growth.gif` (3 frames, ~30KB)

### Example 2: Longer Animation with More Frames

```bash
python3 generate_animation.py \
  --prompts \
    "Dawn sky with stars fading" \
    "Sunrise with orange horizon" \
    "Morning sky with clouds" \
    "Midday bright blue sky" \
    "Afternoon golden light" \
    "Sunset with purple hues" \
    "Dusk with emerging stars" \
    "Night sky full of stars" \
  --output-name "day_cycle.gif" \
  --frame-rate 5 \
  --use-ai
```

**Output**: `animations/day_cycle.gif` (8 frames, ~200KB)

### Example 3: High Resolution Animation

```bash
python3 generate_animation.py \
  --prompts \
    "Closed flower bud at dawn" \
    "Flower beginning to open" \
    "Half-opened flower" \
    "Fully bloomed flower in sunlight" \
  --output-name "flower_bloom.gif" \
  --width 1024 \
  --height 1024 \
  --frame-rate 8 \
  --use-ai
```

**Output**: `animations/flower_bloom.gif` (4 frames @ 1024x1024, ~500KB)

### Example 4: Smooth Interpolated Animation

```bash
python3 generate_animation.py \
  --prompts \
    "A red cube" \
    "A yellow sphere" \
    "A blue pyramid" \
  --output-name "morphing_shapes.gif" \
  --interpolate 3 \
  --frame-rate 15 \
  --use-ai
```

**Output**: 9 total frames (3 keyframes + 6 interpolated) for smooth transitions

### Example 5: Character Animation

```bash
./generate_animation.sh \
  "Character standing still, neutral pose" \
  "Character raising arms, happy expression" \
  "Character jumping with joy, arms up" \
  "Character landing, arms down" \
  "Character standing still again" \
  "character_jump"
```

---

## Advanced Usage

### Python Script Direct Usage

For full control, use the Python script directly:

```bash
python3 generate_animation.py \
  --prompts "prompt1" "prompt2" "prompt3" \
  --output-dir "my_animations" \
  --output-name "custom.gif" \
  --frame-rate 12 \
  --width 800 \
  --height 600 \
  --use-ai \
  --loop 5 \
  --interpolate 2
```

### Parameters Explained

**`--prompts`** (required)
- List of text descriptions for each frame
- Minimum 2 prompts required
- More prompts = longer animation

**`--output-dir`** (optional)
- Directory for frames and final GIF
- Default: `animations/`
- Created automatically if doesn't exist

**`--output-name`** (optional)
- Name of final GIF file
- Default: `animation.gif`
- Automatically adds `.gif` extension

**`--frame-rate`** (optional)
- Animation speed in frames per second
- Range: 1-30 fps
- Lower = slower, smoother
- Higher = faster, snappier

**`--width` / `--height`** (optional)
- Frame dimensions in pixels
- Recommended: 512x512 (balance of quality/size)
- Max recommended: 1024x1024

**`--use-ai`** (flag)
- Enable AI generation for high-quality frames
- Without flag: uses fast PIL sketches
- AI mode takes ~10-15s per frame

**`--loop`** (optional)
- Number of times animation repeats
- 0 = infinite loop (default)
- N = plays N times then stops

**`--interpolate`** (optional)
- Generate transition frames between prompts
- 1 = no interpolation (default)
- 2+ = adds N-1 frames between each prompt

---

## Frame Generation Process

### Step-by-Step Workflow

1. **Input Validation**
   - Validates prompt count (minimum 2)
   - Checks output directory permissions
   - Verifies frame rate and resolution parameters

2. **Frame Generation**
   - Iterates through each prompt
   - Generates individual PNG files
   - Names: `frame_0001.png`, `frame_0002.png`, etc.
   - Resizes to target resolution

3. **Frame Validation**
   - Checks all frames exist
   - Verifies file integrity
   - Confirms correct dimensions
   - Reports any corrupted frames

4. **GIF Compilation**
   - Loads all validated frames
   - Converts to RGB color space
   - Applies frame duration timing
   - Optimizes file size
   - Saves final animated GIF

5. **Cleanup & Report**
   - Displays file size and stats
   - Reports total animation duration
   - Lists output file locations

---

## Performance Guidelines

### Frame Count vs. Generation Time

| Frames | AI Mode | Sketch Mode |
|--------|---------|-------------|
| 3-5    | ~45s    | ~3s         |
| 6-10   | ~90s    | ~5s         |
| 11-20  | ~3min   | ~10s        |
| 21+    | ~5min+  | ~15s+       |

### File Size Estimates

| Resolution | 5 Frames | 10 Frames | 20 Frames |
|------------|----------|-----------|-----------|
| 256x256    | ~50KB    | ~100KB    | ~200KB    |
| 512x512    | ~150KB   | ~300KB    | ~600KB    |
| 1024x1024  | ~500KB   | ~1MB      | ~2MB      |

### Optimization Tips

1. **Use appropriate resolution**: 512x512 is ideal for web use
2. **Limit frame count**: 10-20 frames is usually sufficient
3. **Adjust frame rate**: Lower fps = smaller file size
4. **Enable optimization**: Built-in GIF optimization reduces size by ~30%

---

## Prompt Writing Tips

### For Smooth Animations

✅ **Good Prompts** (gradual changes):
```
"Sun below horizon, dark sky"
"Sun partially visible, orange glow"
"Sun fully risen, bright morning"
```

❌ **Poor Prompts** (abrupt changes):
```
"Night scene"
"Day scene"
```

### Consistency is Key

Maintain consistent:
- **Perspective**: Same viewing angle
- **Style**: Same artistic approach
- **Subject**: Keep main subject in frame
- **Lighting**: Gradual lighting changes

### Example: Character Walk Cycle

```bash
python3 generate_animation.py \
  --prompts \
    "Character standing, left foot forward" \
    "Character lifting right foot, arms swinging" \
    "Character right foot forward, weight shifted" \
    "Character lifting left foot, arms swinging back" \
  --output-name "walk_cycle.gif" \
  --frame-rate 8 \
  --interpolate 2 \
  --use-ai
```

---

## Troubleshooting

### Issue: "At least 2 prompts required"
**Solution**: Provide minimum 2 prompts for animation

### Issue: Frame generation fails
**Solution**: 
- Check internet connection (AI mode)
- Try sketch mode (remove `--use-ai`)
- Simplify prompts

### Issue: GIF file too large
**Solutions**:
- Reduce resolution (e.g., 256x256)
- Decrease frame count
- Lower frame rate
- The script auto-optimizes GIFs

### Issue: Animation too fast/slow
**Solution**: Adjust `--frame-rate` parameter
- Slower: `--frame-rate 5`
- Faster: `--frame-rate 20`

### Issue: Frames look inconsistent
**Solutions**:
- Use more detailed, consistent prompts
- Enable interpolation for transitions
- Keep lighting and style descriptions consistent

---

## Output Structure

```
animations/
├── frame_0001.png          # Individual frames
├── frame_0002.png
├── frame_0003.png
├── ...
└── animation.gif           # Final compiled GIF
```

All frames are preserved for manual editing or recompilation.

---

## Integration with Main Tool

The animation generator integrates seamlessly with the main image generator:

```bash
# Generate frames with main tool
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Frame 1 description" \
  --output_file "animations/frame_0001.png" \
  --use-ai

# Then compile manually with PIL
from PIL import Image
frames = [Image.open(f"animations/frame_{i:04d}.png") for i in range(1, 6)]
frames[0].save("output.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
```

---

## Future Enhancements

- [ ] Video format support (MP4, WebM)
- [ ] Reverse animation option
- [ ] Bounce effect (forward then backward)
- [ ] Frame-by-frame preview before compilation
- [ ] Batch animation generation from scripts
- [ ] Custom easing functions for interpolation
- [ ] Audio support for video formats

---

**Need Help?**
- Review examples above
- Check [README.md](README.md) for general setup
- See [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md) for prompt tips

---

**Version**: 3.1.0  
**Feature**: Animated GIF Generation  
**Status**: ✅ Production Ready
