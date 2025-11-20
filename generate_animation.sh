#!/bin/bash

# GIMP MCP Animation Generator - Batch Script
# Usage: ./generate_animation.sh "prompt1" "prompt2" "prompt3" ... [output_name]

# Check if prompts are provided
if [ $# -lt 2 ]; then
    echo "Error: At least 2 prompts required"
    echo "Usage: ./generate_animation.sh \"prompt1\" \"prompt2\" \"prompt3\" ... [output_name]"
    echo ""
    echo "Example:"
    echo "  ./generate_animation.sh \\"
    echo "    \"A sunrise over mountains\" \\"
    echo "    \"Morning light on mountain peaks\" \\"
    echo "    \"Full daylight mountain landscape\" \\"
    echo "    \"mountain_animation\""
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH="${SCRIPT_DIR}/.venv/bin/python"
SCRIPT_PATH="${SCRIPT_DIR}/generate_animation.py"

# Extract output name if provided (last argument if it doesn't look like a prompt)
LAST_ARG="${@: -1}"
if [[ ! "$LAST_ARG" =~ [[:space:]] ]] && [[ ${#LAST_ARG} -lt 30 ]]; then
    OUTPUT_NAME="${LAST_ARG}.gif"
    # Remove last argument from prompts
    PROMPTS=("${@:1:$#-1}")
else
    OUTPUT_NAME="animation.gif"
    PROMPTS=("$@")
fi

# Display info
echo "=================================================="
echo "GIMP MCP Animation Generator"
echo "=================================================="
echo "Frames: ${#PROMPTS[@]}"
echo "Output: animations/${OUTPUT_NAME}"
echo "Mode: AI-Powered (Stable Diffusion)"
echo "=================================================="
echo ""

# Execute the animation generation
"${PYTHON_PATH}" "${SCRIPT_PATH}" \
    --prompts "${PROMPTS[@]}" \
    --output-name "${OUTPUT_NAME}" \
    --use-ai \
    --frame-rate 10 \
    --width 512 \
    --height 512

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Success! Animation saved to: animations/${OUTPUT_NAME}"
    echo "=================================================="
else
    echo ""
    echo "=================================================="
    echo "✗ Error: Animation generation failed"
    echo "=================================================="
    exit 1
fi
