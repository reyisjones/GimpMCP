# Image Enhancement Guide

Complete guide to using the GIMP MCP enhancement pipeline for improving AI-generated images and animation frames.

## Overview

The enhancement pipeline provides three complementary tools:

1. **`enhance_image.py`** - Single image enhancement with auto-levels, denoise, sharpen, and artifact removal
2. **`preprocess_frames.py`** - Batch enhancement for animation frames
3. **Integrated Enhancement** - Automatic enhancement via `--enhance` flags in generation scripts

## Quick Start

### Enhance a Single Image

```bash
# Basic usage with medium preset
python3 enhance_image.py input.png -o output.png

# Use aggressive enhancement
python3 enhance_image.py input.png -o output.png --preset aggressive

# Use GIMP for advanced enhancement (requires GIMP installation)
python3 enhance_image.py input.png -o output.png --use-gimp
```

### Enhance Animation Frames

```bash
# Enhance all frames in a directory
python3 preprocess_frames.py animations/ -o animations_enhanced/

# Use custom preset
python3 preprocess_frames.py animations/ --preset light

# Validate frames without enhancing
python3 preprocess_frames.py animations/ --validate-only
```

### Integrated Animation Enhancement

```bash
# Generate animation with automatic frame enhancement
python3 generate_animation.py \
  --prompts "Frame 1" "Frame 2" "Frame 3" \
  --use-ai \
  --enhance \
  --enhancement-preset medium
```

## Enhancement Presets

### Light
Best for: Already high-quality images, subtle refinement

- Auto levels: ✓
- Denoise: Level 1 (minimal)
- Sharpen: 0.3 (subtle)
- Despeckle: ✗
- Brightness boost: 1.05 (5%)
- Contrast boost: 1.05 (5%)
- Saturation: 1.0 (no change)

**Use cases:**
- High-quality AI generations
- Professional photos
- When you want to preserve original character

### Medium (Recommended)
Best for: Most AI-generated images, balanced enhancement

- Auto levels: ✓
- Denoise: Level 2 (moderate)
- Sharpen: 0.5 (noticeable)
- Despeckle: ✓
- Brightness boost: 1.10 (10%)
- Contrast boost: 1.10 (10%)
- Saturation: 1.05 (5%)

**Use cases:**
- Standard AI image generation output
- Animation frames from Pollinations.ai or similar
- General-purpose enhancement

### Aggressive
Best for: Low-quality images, heavy artifact removal

- Auto levels: ✓
- Denoise: Level 3 (strong)
- Sharpen: 0.8 (strong)
- Despeckle: ✓
- Brightness boost: 1.15 (15%)
- Contrast boost: 1.15 (15%)
- Saturation: 1.10 (10%)

**Use cases:**
- Noisy or grainy images
- Images with visible AI artifacts
- When you need maximum quality improvement

## Enhancement Operations

### Auto Levels
Stretches the histogram to utilize the full tonal range (0-255), improving contrast.

**GIMP equivalent:** `Colors → Auto → Levels Stretch`

### Denoise
Applies median filtering to reduce noise while preserving edges.

- Level 1: Single pass (subtle)
- Level 2: Two passes (moderate)
- Level 3: Three passes (aggressive)

**GIMP equivalent:** `Filters → Enhance → Despeckle`

### Brightness/Contrast
Multiplicative adjustment of image brightness and contrast.

**GIMP equivalent:** `Colors → Brightness-Contrast`

### Saturation
Adjusts color intensity without affecting luminosity.

**GIMP equivalent:** `Colors → Hue-Saturation`

### Sharpen
Enhances edge definition using unsharp mask technique.

**GIMP equivalent:** `Filters → Enhance → Unsharp Mask`

### Despeckle (GIMP only)
Advanced artifact removal using GIMP's despeckle filter.

**Requires:** `--use-gimp` flag

## GIMP Integration

### Enabling GIMP Enhancement

```bash
# Auto-detect GIMP installation
python3 enhance_image.py input.png --use-gimp

# Specify GIMP path explicitly
python3 enhance_image.py input.png --use-gimp --gimp-path /Applications/GIMP.app/Contents/MacOS/gimp
```

### GIMP Operations Used

When `--use-gimp` is enabled, these GIMP operations are applied via Script-Fu batch processing:

1. **`gimp-levels-stretch`** - Auto levels/histogram stretch
2. **`plug-in-despeckle`** - Remove small artifacts and noise
3. **`plug-in-unsharp-mask`** - Sharpen with radius and amount control
4. **`plug-in-gauss`** - Selective Gaussian blur (for specific use cases)

### GIMP vs Pillow-Only

| Feature | Pillow | GIMP |
|---------|--------|------|
| Speed | Fast | Slower |
| Despeckle | ✗ | ✓ |
| Advanced sharpening | Basic | Advanced (Unsharp Mask) |
| Artifact removal | Basic | Professional |
| Dependencies | None | GIMP installation |
| Batch processing | ✓ | ✓ |

## Complete Pipeline Examples

### Example 1: High-Quality Animation

```bash
# Generate + enhance in one step
python3 generate_animation.py \
  --prompts \
    "A bicycle on a sunny road, realistic lighting" \
    "The bicycle moving forward, consistent style" \
    "The bicycle farther ahead, same perspective" \
  --output-name bicycle.gif \
  --frame-rate 12 \
  --width 800 \
  --height 600 \
  --use-ai \
  --enhance \
  --enhancement-preset medium
```

### Example 2: Two-Stage Enhancement

```bash
# Stage 1: Generate frames
python3 generate_animation.py \
  --prompts "Frame 1" "Frame 2" "Frame 3" \
  --output-dir raw_frames \
  --use-ai

# Stage 2: Enhance frames separately
python3 preprocess_frames.py raw_frames/ -o enhanced_frames/ --preset aggressive

# Stage 3: Compile GIF from enhanced frames
python3 generate_animation.py \
  --prompts "Frame 1" "Frame 2" "Frame 3" \
  --output-dir enhanced_frames \
  --output-name final.gif
```

### Example 3: Custom Enhancement

Create a Python script with custom enhancement operations:

```python
from enhance_image import ImageEnhancer

enhancer = ImageEnhancer(use_gimp=True)

custom_ops = {
    'auto_levels': True,
    'denoise': 3,
    'sharpen': 1.0,
    'despeckle': True,
    'brightness': 1.2,
    'contrast': 1.15,
    'saturation': 1.1
}

result = enhancer.enhance(
    'input.png',
    'output.png',
    operations=custom_ops
)

print(result)
```

## Troubleshooting

### Enhancement Makes Images Worse

**Problem:** Images look over-processed or unnatural

**Solution:**
- Use `--preset light` instead of aggressive
- Reduce sharpen amount in custom operations
- Disable despeckle if details are being removed

### GIMP Enhancement Fails

**Problem:** `--use-gimp` returns errors

**Solutions:**
1. Check GIMP installation: `gimp --version`
2. Specify explicit path: `--gimp-path /path/to/gimp`
3. Fall back to Pillow-only (automatic on failure)

### Frames Have Inconsistent Quality

**Problem:** Some frames look better than others after enhancement

**Solution:**
- Use `preprocess_frames.py` for batch consistency
- Validate frames before enhancement: `--validate-only`
- Ensure all frames have same resolution

### Enhancement is Too Slow

**Problem:** Processing takes too long

**Solutions:**
- Don't use `--use-gimp` (Pillow is faster)
- Use `--preset light` for faster processing
- Process frames in parallel (custom script)

## Performance Benchmarks

Typical enhancement times for 800x600 images:

| Method | Time per Image |
|--------|----------------|
| Pillow (light) | 0.5s |
| Pillow (medium) | 1.0s |
| Pillow (aggressive) | 1.5s |
| GIMP (medium) | 3-5s |
| GIMP (aggressive) | 5-8s |

For animations with 10 frames:
- Pillow: ~10-15 seconds total
- GIMP: ~30-60 seconds total

## Best Practices

1. **Start with medium preset** - Works for 90% of use cases
2. **Preview before batch** - Test on one frame before enhancing all
3. **Use integrated enhancement** - Simpler than two-stage pipeline
4. **Validate frames** - Check for consistent resolution before enhancement
5. **GIMP for final output** - Use GIMP enhancement for important deliverables
6. **Pillow for iteration** - Use fast Pillow-only for quick iterations

## API Reference

### ImageEnhancer Class

```python
from enhance_image import ImageEnhancer

enhancer = ImageEnhancer(
    use_gimp=False,  # Whether to use GIMP batch operations
    gimp_path=None   # Path to GIMP (auto-detected if None)
)

result = enhancer.enhance(
    image_path='input.png',
    output_path='output.png',
    preset='medium',  # 'light' | 'medium' | 'aggressive'
    operations=None   # Custom ops dict (overrides preset)
)

# Result structure:
{
    'status': 'ok' | 'error',
    'code': 'success' | error_code,
    'message': 'Description',
    'output_path': '/path/to/output.png' | None
}
```

### FramePreprocessor Class

```python
from preprocess_frames import FramePreprocessor

preprocessor = FramePreprocessor(use_gimp=False)

result = preprocessor.preprocess_frames(
    frame_directory='animations/',
    output_directory='animations_enhanced/',
    preset='medium',
    operations=None,
    pattern='*.png'
)

# Result structure includes:
# - enhanced_frames: list of output paths
# - failed_frames: list of failures
# - success_count: number of enhanced frames
# - failure_count: number of failed frames
```

## Integration with MCP

Enhancement tools are designed to work seamlessly with the Model Context Protocol:

```json
{
  "tools": [
    {
      "name": "enhance_image",
      "type": "python",
      "entry": "enhance_image.py",
      "parameters": {
        "input": "string",
        "output": "string",
        "preset": "light|medium|aggressive"
      }
    },
    {
      "name": "preprocess_frames",
      "type": "python",
      "entry": "preprocess_frames.py",
      "parameters": {
        "input_directory": "string",
        "preset": "string"
      }
    }
  ]
}
```

## Next Steps

- Review [FEATURES.md](FEATURES.md) for complete feature roadmap
- See [ANIMATION_GUIDE.md](ANIMATION_GUIDE.md) for animation-specific tips
- Check [Guide.md](Guide.md) for smoother animation techniques
- Explore custom enhancement scripts in `examples/`

---

**Questions or issues?** Open an issue on the GitHub repository.
