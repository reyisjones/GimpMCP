# 🚀 GIMP MCP Integration - Quick Start Guide

## 30-Second Setup

```bash
# 1. Navigate to project
cd /path/to/GimpMCP

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install Pillow

# 4. Test the integration
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Test storyboard scene" \
  --output_file "test.png"
```

## Expected Output

```
✓ Image saved: test.png
Image generated successfully: test.png
```

## Using with VS Code GPT-4o Agent

Once setup is complete, simply ask the agent:

> "Generate a storyboard image showing [your scene description]"

The agent will automatically:
1. Activate the virtual environment
2. Invoke the `gimp-image-gen` tool
3. Create the image
4. Return the file path

## Command Reference

### Basic Usage
```bash
source .venv/bin/activate && python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Your scene description" \
  --output_file "path/to/output.png"
```

### Generate Multiple Images
```bash
source .venv/bin/activate

# Panel 1
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Opening scene: Band formation in Hatillo" \
  --output_file "storyboard/panel_01.png"

# Panel 2
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Mid-scene: First rehearsal together" \
  --output_file "storyboard/panel_02.png"

# Panel 3
python3 MCP/gimp-image-gen/gimp_image_gen.py \
  --prompt "Closing: First live performance" \
  --output_file "storyboard/panel_03.png"
```

## Tips

- **Always activate the virtual environment first**: `source .venv/bin/activate`
- **Use `python3` instead of `python`** on macOS
- **GIMP warnings are safe to ignore** - they don't affect image generation
- **Output directories are created automatically** if they don't exist

## Verify GIMP Installation (Optional)

```bash
gimp --version
```

If not installed:
```bash
brew install gimp
```

## Next Steps

1. ✅ Setup complete - start generating images!
2. 📖 Read the full [README.md](README.md) for detailed documentation
3. 🔧 Review [MCP/GIMP_MCP_Setup_and_Automation.md](MCP/GIMP_MCP_Setup_and_Automation.md) for troubleshooting

---

**Quick Links:**
- [Full Documentation](README.md)
- [Setup Guide](MCP/GIMP_MCP_Setup_and_Automation.md)
- [Original Guide](MCP/Guide.md)
