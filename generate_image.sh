#!/bin/bash

# GIMP MCP Image Generator - Batch Script
# Usage: ./generate_image.sh "Your prompt here" "output_filename"

# Check if prompt is provided
if [ -z "$1" ]; then
    echo "Error: No prompt provided"
    echo "Usage: ./generate_image.sh \"Your prompt here\" \"output_filename\""
    echo "Example: ./generate_image.sh \"A sunset over mountains\" \"sunset\""
    exit 1
fi

# Check if filename is provided
if [ -z "$2" ]; then
    echo "Error: No output filename provided"
    echo "Usage: ./generate_image.sh \"Your prompt here\" \"output_filename\""
    echo "Example: ./generate_image.sh \"A sunset over mountains\" \"sunset\""
    exit 1
fi

# Set variables
PROMPT="$1"
FILENAME="$2"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH="${SCRIPT_DIR}/.venv/bin/python"
SCRIPT_PATH="${SCRIPT_DIR}/MCP/gimp-image-gen/gimp_image_gen.py"
OUTPUT_FILE="${SCRIPT_DIR}/output/${FILENAME}.png"

# Create output directory if it doesn't exist
mkdir -p "${SCRIPT_DIR}/output"

# Display info
echo "=================================================="
echo "GIMP MCP Image Generator"
echo "=================================================="
echo "Prompt: ${PROMPT}"
echo "Output: ${OUTPUT_FILE}"
echo "Mode: AI-Powered (Stable Diffusion)"
echo "=================================================="
echo ""

# Execute the image generation
"${PYTHON_PATH}" "${SCRIPT_PATH}" \
    --prompt "${PROMPT}" \
    --output_file "${OUTPUT_FILE}" \
    --use-ai

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Success! Image saved to: ${OUTPUT_FILE}"
    echo "=================================================="
else
    echo ""
    echo "=================================================="
    echo "✗ Error: Image generation failed"
    echo "=================================================="
    exit 1
fi
