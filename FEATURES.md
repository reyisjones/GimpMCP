# GIMP MCP Feature Extensions

This document outlines the complete feature set for the GIMP MCP workflow, integrating existing image generation and animation capabilities with new GIMP-based enhancement and post-processing features. Each feature includes functionality, expected inputs/outputs, and related GIMP operations.

## Integrated Pipeline Architecture

```
Text Prompt → AI Generation → Enhancement → Post-Processing → Output
                    ↓              ↓              ↓
              [gimp_image_gen] [enhance_image] [optimize_output]
                    ↓              ↓              ↓
              Frame Sequence → Preprocessing → GIF Compilation
                    ↓              ↓              ↓
           [generate_animation] [preprocess_frames] [create_gif]
```

## Existing Features (Core Generation)

### A. AI Image Generation
- **Functionality**: Generate high-quality images from text prompts using Stable Diffusion APIs with fallback to PIL-based drafts.
- **Inputs**: `prompt` (str), `output_file` (str), `use_ai` (bool).
- **Outputs**: PNG image file.
- **APIs**: Hugging Face Inference API, Pollinations.ai.
- **Status**: ✅ Implemented in `MCP/gimp-image-gen/gimp_image_gen.py`.

### B. Animated GIF Generation
- **Functionality**: Generate frame sequences from multiple prompts with optional interpolation, compile into animated GIF.
- **Inputs**: `prompts` (list), `frame_rate` (int), `resolution` (tuple), `interpolate` (int).
- **Outputs**: Series of PNG frames + compiled GIF.
- **Features**: Frame validation, resolution normalization, loop control.
- **Status**: ✅ Implemented in `generate_animation.py`.

## New Features (GIMP Enhancement Pipeline)

### 0. Auto Image Enhancement (Priority: Critical)
- **Functionality**: One-click enhancement for AI-generated images - auto levels, denoise, sharpen, artifact removal using GIMP batch operations.
- **Inputs**: `image_path`, `output_path`, `preset` (light|medium|aggressive), `operations` (list: auto-levels, denoise, sharpen, despeckle).
- **Outputs**: Enhanced image with improved quality and reduced AI artifacts.
- **GIMP Ops**: `gimp-levels-stretch`, `plug-in-despeckle`, `plug-in-unsharp-mask`, `plug-in-gauss` (selective blur).
- **Pipeline Hook**: Can be applied automatically via `--enhance` flag in generation scripts.
- **Errors**: Invalid preset, missing input file.

### 0a. Frame Preprocessing for Animation
- **Functionality**: Batch enhance all animation frames before GIF compilation - ensures consistent quality and smooth transitions.
- **Inputs**: `frame_directory`, `operations` (list), `preset` (str), `output_directory`.
- **Outputs**: Directory of enhanced frames ready for GIF compilation.
- **GIMP Ops**: Same as auto-enhancement, applied in batch with progress tracking.
- **Pipeline Hook**: Integrated into `generate_animation.py` workflow.
- **Errors**: Frame validation failures, inconsistent sizes.

### 0b. Post-Generation Optimization
- **Functionality**: Final quality pass on generated images/animations - color grading, sharpness tuning, artifact cleanup.
- **Inputs**: `image_path`, `color_profile` (str), `sharpness` (float), `cleanup_level` (int).
- **Outputs**: Polished final output.
- **GIMP Ops**: Color curves, selective sharpening, noise reduction.
- **Pipeline Hook**: Final step before delivery.
- **Errors**: Invalid color profile, over-processing detection.

## 1. Resize & Format Conversion (Priority: High)
- Functionality: Resize an image to target dimensions or by max side while optionally keeping aspect ratio; convert to specified format (PNG, JPEG, WEBP).
- Inputs: `image_path`, `output_path`, `width`, `height`, `keep_aspect` (bool), `format` (str), `quality` (int, JPEG/WebP only).
- Outputs: Resized image file at `output_path` with new format.
- GIMP Ops: `gimp-image-scale`, `file-png-save`, `file-jpeg-save`, `file-webp-export` (analogs).
- Errors: Missing file, unsupported format, invalid size.

## 2. Smart Crop
- Functionality: Crop image to given box or center crop by dimensions; placeholder for face or focal detection.
- Inputs: `image_path`, `output_path`, either `left, top, right, bottom` OR `target_width, target_height, mode`.
- Outputs: Cropped image.
- GIMP Ops: `gimp-image-crop`.
- Errors: Invalid region, smaller than requested, negative coordinates.

## 3. Watermark / Text Overlay
- Functionality: Add semi-transparent text or image watermark at specified position with padding.
- Inputs: `image_path`, `output_path`, `text` OR `watermark_image`, `position` (e.g., bottom-right), `opacity` (0-1), `font_size`, `color`.
- Outputs: Watermarked image.
- GIMP Ops: Layer creation, `gimp-layer-set-opacity`, merge layers.
- Errors: Missing font, invalid opacity, watermark bigger than base.

## 4. Color Adjustments (Brightness / Contrast / Saturation)
- Functionality: Adjust brightness, contrast, saturation via multiplicative or additive transforms.
- Inputs: `image_path`, `output_path`, `brightness` (-1..1), `contrast` (-1..1), `saturation` (-1..1).
- Outputs: Color-adjusted image.
- GIMP Ops: `gimp-brightness-contrast`, `gimp-hue-saturation`.
- Errors: Out-of-range params.

## 5. Layer Merge & Blend Modes
- Functionality: Merge overlay image with base using blend modes (normal, multiply, screen, overlay subset).
- Inputs: `base_path`, `overlay_path`, `output_path`, `blend_mode`, `opacity`.
- Outputs: Composited image.
- GIMP Ops: Layer modes & merges.
- Errors: Mismatched sizes (optional auto-resize), unsupported mode.

## 6. Background Removal (Simple Key / Threshold)
- Functionality: Make pixels similar to provided key color transparent (tolerance) OR remove near-white background.
- Inputs: `image_path`, `output_path`, `key_color` (hex/RGB), `tolerance` (0-255), `mode` (color-key|white).
- Outputs: PNG with transparency.
- GIMP Ops: Color select + clear.
- Errors: Invalid color, wrong mode.

## 7. Filter Pack (Blur / Sharpen / Edge)
- Functionality: Apply Gaussian blur, unsharp mask style sharpen, edge detection (Sobel).
- Inputs: `image_path`, `output_path`, `filter` (blur|sharpen|edge), `radius`/`amount` as applicable.
- Outputs: Filtered image.
- GIMP Ops: Gaussian blur, Sharpen, Edge detect.
- Errors: Unsupported filter, invalid radius.

## 8. Auto Levels / Histogram Equalization
- Functionality: Stretch histogram to min/max or equalize.
- Inputs: `image_path`, `output_path`, `mode` (levels|equalize).
- Outputs: Adjusted image.
- GIMP Ops: Levels, Equalize.
- Errors: Unsupported mode.

## 9. Image Stacking (Noise Reduction)
- Functionality: Average multiple aligned images to reduce noise (simple pixel average).
- Inputs: `image_paths` (list), `output_path`.
- Outputs: Stacked averaged image.
- GIMP Ops: Layer stack + blend average.
- Errors: Different sizes, empty list.

## 10. MCP Integration & Manifest Updates
- Functionality: Expose each feature as callable MCP commands with unified error JSON structure.
- Inputs: Feature-specific plus MCP request metadata.
- Outputs: Success or error payload + path.
- Errors: Standardized error codes.

## Error Handling Standard
Return structured dict: `{ "status": "ok"|"error", "code": <slug>, "message": <str>, "output_path": <path or None> }`.

## Testing Strategy
- Unit tests per feature in `tests/` using synthetic images.
- Validation: dimensions, pixel changes, file existence.
- Edge cases: invalid parameters, missing files.

## Implementation Roadmap

### Phase 1: Enhancement Pipeline (In Progress)
1. **Auto Image Enhancement** - Core enhancement module with GIMP batch wrapper
2. **Frame Preprocessing** - Batch enhancement for animation frames
3. **Pipeline Integration** - Add `--enhance` flags to generation scripts
4. **Testing & Validation** - Automated tests for all enhancement operations

### Phase 2: Core GIMP Operations
5. Resize & Convert
6. Crop
7. Watermark/Text
8. Color Adjust

### Phase 3: Advanced Processing
9. Blend Modes
10. Background Removal
11. Filter Pack
12. Auto Levels

### Phase 4: Specialized Features
13. Image Stacking
14. Post-Generation Optimization
15. MCP Command Integration/Manifest expansion

### Phase 5: Documentation & Examples
16. Enhancement guide with presets
17. Full pipeline examples
18. Troubleshooting and optimization tips

---
**Current Focus**: Implementing Phase 1 - Enhancement Pipeline
