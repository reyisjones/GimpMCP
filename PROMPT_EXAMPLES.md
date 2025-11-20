# GIMP MCP Image Generator - Prompt Examples & Guide

## How to Use the Image Generator

### Basic Command Structure
```bash
python MCP/gimp-image-gen/gimp_image_gen.py --prompt "Your description" --output_file "output/filename.png" [--use-ai]
```

### Modes
- **Default Mode**: Simple PIL-based sketches (fast, basic shapes)
- **AI Mode**: Add `--use-ai` flag for realistic AI-generated images using Stable Diffusion

---

## Prompt Writing Guide

### Best Practices for Effective Prompts

1. **Be Specific**: Include details about style, composition, and perspective
2. **Include Art Style**: Mention artistic style (minimalist, realistic, cartoon, sketch, etc.)
3. **Specify Colors**: Black and white, vibrant colors, monochrome, etc.
4. **Define View/Angle**: Side view, top-down, front view, isometric, etc.
5. **Add Mood/Atmosphere**: Bright, dark, moody, cheerful, dramatic, etc.
6. **Mention Details**: Clean lines, detailed textures, simple shapes, etc.

### Prompt Structure Template
```
[Subject] in [Style], [View/Angle], [Color Scheme], [Details], [Mood/Atmosphere]
```

---

## Sample Prompts by Category

### 🚗 Vehicles & Transportation

**Example 1: Classic Car**
```bash
"A vintage 1960s sports car in red, side view, detailed chrome accents, realistic style, sunset lighting, photographic quality"
```

**Example 2: Futuristic Vehicle**
```bash
"A sleek futuristic hovering vehicle, isometric view, metallic silver and blue, clean geometric design, sci-fi concept art style"
```

**Example 3: Simple Bicycle**
```bash
"A minimalist bicycle illustration, side profile, black and white line art, clean simple lines, flat design style"
```

---

### 🏠 Architecture & Buildings

**Example 4: Modern House**
```bash
"A modern minimalist house with large windows, front view, white exterior with wood accents, architectural rendering style, bright daylight"
```

**Example 5: Fantasy Castle**
```bash
"A majestic medieval castle on a hilltop, distant view, stone towers and flags, dramatic cloudy sky, fantasy art style, epic atmosphere"
```

**Example 6: Coffee Shop Interior**
```bash
"A cozy coffee shop interior, warm lighting, wooden furniture, plants on shelves, people sitting and chatting, warm color palette, illustration style"
```

---

### 👤 Characters & People

**Example 7: Superhero Character**
```bash
"A superhero character in dynamic flying pose, full body view, vibrant red and blue costume, comic book art style, action-packed energy"
```

**Example 8: Business Professional**
```bash
"A professional businesswoman in formal attire, portrait view, confident expression, clean background, corporate photography style, natural lighting"
```

**Example 9: Fantasy Wizard**
```bash
"An elderly wizard with long white beard holding a glowing staff, full body, purple robes with stars, mystical atmosphere, fantasy illustration style"
```

---

### 🌄 Nature & Landscapes

**Example 10: Mountain Landscape**
```bash
"A majestic mountain range at sunrise, wide panoramic view, snow-capped peaks, colorful sky with orange and pink clouds, landscape photography style"
```

**Example 11: Tropical Beach**
```bash
"A serene tropical beach with palm trees, turquoise water, white sand, clear blue sky, vacation paradise, bright vibrant colors, travel photography style"
```

**Example 12: Forest Path**
```bash
"A mystical forest path with sunlight filtering through trees, atmospheric fog, green moss on rocks, peaceful mood, nature photography style"
```

---

### 🎨 Abstract & Artistic

**Example 13: Geometric Pattern**
```bash
"Abstract geometric pattern with triangles and circles, vibrant colors, symmetrical design, modern digital art style, flat design"
```

**Example 14: Watercolor Flowers**
```bash
"Delicate watercolor painting of wildflowers, soft pastel colors, flowing organic shapes, artistic loose brushstrokes, light and airy feel"
```

**Example 15: Cyberpunk Cityscape**
```bash
"Neon-lit cyberpunk city at night, towering skyscrapers, flying vehicles, rain-soaked streets, purple and cyan neon lights, cinematic sci-fi atmosphere"
```

---

### 🍕 Food & Beverages

**Example 16: Gourmet Dish**
```bash
"A gourmet plated dish with steak and vegetables, top-down view, restaurant quality presentation, garnished with herbs, food photography style, professional lighting"
```

**Example 17: Coffee Cup**
```bash
"A steaming cup of cappuccino with latte art, close-up view, wooden table background, warm morning light, cozy cafe atmosphere, food photography"
```

**Example 18: Fresh Fruit**
```bash
"An arrangement of fresh tropical fruits on white background, bright colors, clean composition, commercial product photography style, studio lighting"
```

---

### 🎮 Games & Technology

**Example 19: Gaming Setup**
```bash
"A modern gaming setup with RGB lighting, dual monitors, mechanical keyboard, gaming chair, dark room with colorful lights, tech photography style"
```

**Example 20: Robot Character**
```bash
"A friendly robot character with rounded design, white and blue colors, cartoon style, cheerful expression, clean simple shapes, suitable for kids"
```

---

## Tips for Better Results

### For AI Mode (--use-ai):
- More detailed prompts = better results
- Include artistic style references (e.g., "in the style of...")
- Specify quality terms: "highly detailed", "8k resolution", "professional photography"
- Mention lighting: "golden hour", "studio lighting", "dramatic shadows"

### For Default Mode (PIL-based):
- Keep it simple and descriptive
- Focus on basic shapes and compositions
- Good for quick sketches and storyboards
- Best for placeholders and concept drafts

---

## Command Examples

### Generate with AI (Recommended for final images)
```bash
# Realistic vehicle
python MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "A luxury sports car in metallic blue, side view, detailed reflections, photorealistic, studio lighting" \
  --output_file "output/sports_car.png" \
  --use-ai

# Landscape scene
python MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "A serene Japanese garden with cherry blossoms, koi pond, stone lantern, peaceful atmosphere, spring season" \
  --output_file "output/japanese_garden.png" \
  --use-ai
```

### Generate Quick Sketch (Default mode)
```bash
# Storyboard draft
python MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "A hero character standing on cliff overlooking city" \
  --output_file "output/storyboard_01.png"
```

---

## Integration with VS Code MCP

When using this tool through VS Code's GPT-4o Agent, you can simply describe what you want:

**User**: "Generate an image of a cozy reading nook with bookshelves and a window"

**Agent**: Will automatically call the tool with appropriate prompt and parameters

**User**: "Create a futuristic spaceship design in black and white"

**Agent**: Will generate the image and save it to your output folder

---

## Troubleshooting

### If AI generation fails:
- The tool will automatically fall back to PIL-based generation
- Check your internet connection
- Try simplifying the prompt
- The free API may have rate limits

### For best quality:
- Use `--use-ai` flag for important images
- Be descriptive and specific in your prompts
- Include style references and technical details
- Experiment with different phrasings

---

## Need More Help?

- Check the `README.md` for installation instructions
- See `QUICKSTART.md` for setup guide
- Review `INTEGRATION_SUMMARY.md` for MCP integration details
