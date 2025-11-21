# 🎨 GIMP MCP - AI Image Generator for VS Code

> Generate images from text descriptions using Stable Diffusion AI - integrated with VS Code through Model Context Protocol (MCP)

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.9+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

---

## 📖 Overview

GIMP MCP is an AI-powered image generation tool that integrates with VS Code through the Model Context Protocol. It enables you to generate images from text descriptions using Stable Diffusion, with automatic fallback to PIL-based sketches.

### ✨ Key Features

- 🤖 **AI-Powered**: Uses Stable Diffusion for realistic image generation
- ✨ **Smart Enhancement**: Auto-enhance images with denoise, sharpen, and artifact removal
- 🎯 **VS Code Integrated**: Works seamlessly with GPT-4o Agent via MCP
- ⚡ **Fast**: Sub-second generation for sketches, ~10s for AI images
- 🎨 **Dual Mode**: AI-generated or quick PIL-based drafts
- 📦 **Batch Processing**: Generate and enhance multiple images at once
- 🎬 **Animation Support**: Create animated GIFs with automatic frame enhancement
- 🖼️ **GIMP Integration**: Optional GIMP batch operations for professional-grade enhancement
- 🛠️ **Easy Setup**: Simple bash script for quick generation

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- VS Code with GPT-4o Agent
- Internet connection (for AI mode)

### Installation

```bash
# 1. Navigate to project directory
cd /path/to/GimpMCP

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Generate Your First Image

**Using the bash script:**
```bash
./generate_image.sh "A serene mountain landscape at sunset" "mountain_sunset"
```

**Using Python directly:**
```bash
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "A serene mountain landscape at sunset" \
  --output_file "output/mountain_sunset.png" \
  --use-ai
```

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 30 seconds
- **[ANIMATION_GUIDE.md](ANIMATION_GUIDE.md)** - Create animated GIFs from text sequences
- **[PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md)** - 20+ sample prompts and best practices
- **[INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)** - Technical implementation details
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates

---

## 💻 Usage

### Two Generation Modes

#### 1. AI Mode (Recommended)
Uses Stable Diffusion for realistic, detailed images:
```bash
./generate_image.sh "A futuristic cyberpunk city at night" "cyberpunk"
```

#### 2. Sketch Mode
Fast PIL-based placeholders for quick drafts:
```bash
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Quick concept sketch" \
  --output_file "output/sketch.png"
```

### VS Code Integration

Ask the GPT-4o Agent directly:
```
"Generate an image of a vintage sports car in red, sunset lighting"
```

The agent will automatically invoke the tool and create your image.

### Batch Generation

Generate multiple images at once:
```bash
python3 batch_generate.py output/storyboards
```

### Animation Generation

Create animated GIFs from text sequences:
```bash
./generate_animation.sh \
  "A sunrise over mountains" \
  "Morning light on peaks" \
  "Full daylight landscape" \
  "mountain_animation"
```

### Enhanced Animation (New!)

Generate with automatic frame enhancement:
```bash
python3 generate_animation.py \
  --prompts "Frame 1" "Frame 2" "Frame 3" \
  --use-ai \
  --enhance \
  --enhancement-preset medium \
  --output-name enhanced_animation.gif
```

### Image Enhancement

Enhance existing images:
```bash
# Basic enhancement
python3 enhance_image.py input.png -o output.png

# With GIMP for professional quality
python3 enhance_image.py input.png -o output.png --use-gimp --preset aggressive

# Batch enhance animation frames
python3 preprocess_frames.py animations/ -o animations_enhanced/
```

See **[ENHANCEMENT_GUIDE.md](ENHANCEMENT_GUIDE.md)** for complete enhancement documentation.

See **[ANIMATION_GUIDE.md](ANIMATION_GUIDE.md)** for detailed animation features.

---

## 🎨 Examples

Check **[PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md)** for 20+ categorized examples:

- 🚗 Vehicles & Transportation
- 🏠 Architecture & Buildings
- 👤 Characters & People
- 🌄 Nature & Landscapes
- 🎨 Abstract & Artistic
- 🍕 Food & Beverages
- 🎮 Games & Technology

### Sample Outputs

| Prompt | Output |
|--------|--------|
| "A simple 2D Volkswagen Beetle car in black and white, side view, minimalist design" | `beetle_ai.png` |
| "A serene Japanese garden with cherry blossoms, koi pond, stone lantern" | `japanese_garden.png` |
| "A futuristic cyberpunk city at night with neon lights, flying cars" | `cyberpunk_city.png` |

---

## 🗂️ Project Structure

```
GimpMCP/
├── .venv/                      # Python virtual environment
├── .vscode/
│   └── settings.json           # VS Code MCP configuration
├── MCP/
│   └── gimp-image-gen/
│       ├── manifest.json       # MCP tool definition (v2.0)
│       └── gimp_image_gen.py   # Core image generator
├── output/                     # Generated images
├── animations/                 # Animation frames and GIFs
├── generate_image.sh           # Quick generation script
├── generate_animation.sh       # Animation generation script
├── generate_animation.py       # Animation generator (Python)
├── batch_generate.py           # Batch processing
├── enhance_image.py            # Image enhancement tool (NEW)
├── preprocess_frames.py        # Frame batch enhancement (NEW)
├── requirements.txt            # Python dependencies
├── ENHANCEMENT_GUIDE.md        # Enhancement documentation (NEW)
├── FEATURES.md                 # Feature roadmap (NEW)
└── README.md                   # This file
```

---

## ⚙️ Configuration

### AI Provider

Currently uses **Pollinations.ai** (free, no API key required).

To add Hugging Face support:
1. Get API token from [Hugging Face](https://huggingface.co/)
2. Edit `gimp_image_gen.py`:
```python
headers["Authorization"] = "Bearer YOUR_TOKEN"
```

---

## 🔧 Troubleshooting

### Common Issues

**"Module 'PIL' not found"**
```bash
source .venv/bin/activate
pip install Pillow
```

**"Permission denied: ./generate_image.sh"**
```bash
chmod +x generate_image.sh
```

**"AI generation failed"**
- Check internet connection
- Tool automatically falls back to PIL mode
- Try simplifying the prompt

### Getting Help

- Review [QUICKSTART.md](QUICKSTART.md) for setup issues
- Check [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md) for prompt tips
- See [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md) for technical details

---

## 🎯 Tips for Best Results

### For AI Mode
- Be specific and descriptive
- Include artistic style ("photorealistic", "cartoon style", etc.)
- Mention lighting ("golden hour", "studio lighting")
- Add quality terms ("highly detailed", "professional")

### Example Good Prompts
```
✅ "A luxury sports car in metallic blue, side view, detailed reflections, photorealistic, studio lighting"
✅ "A cozy coffee shop interior, warm lighting, wooden furniture, people chatting, illustration style"
✅ "A majestic medieval castle on hilltop, dramatic cloudy sky, fantasy art style, epic atmosphere"
```

### Example Poor Prompts
```
❌ "A car" (too vague)
❌ "Nice picture of something" (no specifics)
❌ "Image" (not descriptive)
```

---

## 📊 Performance

| Mode | Speed | Quality | Use Case |
|------|-------|---------|----------|
| AI Mode | ~10-15s | High | Final images, presentations |
| Sketch Mode | <1s | Basic | Placeholders, quick drafts |
| Animation (5 frames) | ~45s | High | Animated sequences, demos |

---

## 🚀 Future Enhancements

- [ ] Support for DALL·E and other AI providers
- [ ] Custom image sizes and aspect ratios
- [ ] Style transfer from reference images
- [ ] Video format support (MP4, WebM) for animations
- [ ] Advanced GIMP scripting integration
- [ ] WebUI for non-technical users

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **Stable Diffusion** - AI image generation model
- **Pollinations.ai** - Free AI inference API
- **PIL/Pillow** - Python imaging library
- **Model Context Protocol** - VS Code integration framework

---

## 📞 Support

For questions or issues:
1. Check the documentation above
2. Review [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md)
3. See [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)

---

**Version**: 3.1.0  
**Last Updated**: November 19, 2025  
**Status**: ✅ Production Ready

Made with ❤️ for creative workflows
