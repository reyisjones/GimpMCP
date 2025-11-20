from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import requests
from urllib.parse import quote

def generate_image(prompt, output_file, use_gimp=False):
    """
    Generates a storyboard image using PIL/Pillow.

    Args:
        prompt (str): The text description for the image.
        output_file (str): The path to save the generated PNG.
        use_gimp (bool): Whether to enable GIMP post-processing (default: False).
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir:  # Only create directory if path contains a directory
        os.makedirs(output_dir, exist_ok=True)
    
    # Create a new image with white background
    width, height = 1920, 1080
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple border
    border_color = '#333333'
    draw.rectangle([(10, 10), (width-10, height-10)], outline=border_color, width=3)
    
    # Add title text
    try:
        # Try to use a nicer font if available
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw title
    title = "STORYBOARD DRAFT"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) / 2, 40), title, fill='black', font=title_font)
    
    # Draw prompt text (word-wrapped)
    margin = 100
    max_width = width - 2 * margin
    y_offset = 150
    
    words = prompt.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=text_font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    for line in lines:
        draw.text((margin, y_offset), line, fill='#333333', font=text_font)
        y_offset += 50
    
    # Draw placeholder sketch indicators
    sketch_color = '#CCCCCC'
    center_x, center_y = width // 2, height // 2
    
    # Draw simple composition guides
    draw.ellipse([(center_x - 200, center_y - 150), (center_x + 200, center_y + 150)], 
                 outline=sketch_color, width=2)
    draw.line([(center_x - 250, center_y), (center_x + 250, center_y)], 
              fill=sketch_color, width=1)
    draw.line([(center_x, center_y - 200), (center_x, center_y + 200)], 
              fill=sketch_color, width=1)
    
    # Add a note at the bottom
    note = "Generated Draft • Refine in GIMP or other image editor"
    note_bbox = draw.textbbox((0, 0), note, font=text_font)
    note_width = note_bbox[2] - note_bbox[0]
    draw.text(((width - note_width) / 2, height - 60), note, fill='#999999', font=text_font)
    
    # Save the image
    image.save(output_file, 'PNG')
    print(f"✓ Image saved: {output_file}")

    # GIMP integration disabled due to hanging issues
    if use_gimp:
        print("Note: GIMP post-processing is disabled. Use GIMP manually to refine the image.")

def generate_image_with_ai(prompt, output_file):
    """
    Generates an image using Stable Diffusion based on the text description.

    Args:
        prompt (str): The text description for the image.
        output_file (str): The path to save the generated PNG.
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating image with Stable Diffusion...")
    print(f"Prompt: {prompt}")
    
    # Try multiple Stable Diffusion API endpoints
    apis = [
        {
            "name": "Hugging Face Inference API",
            "url": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
            "method": "huggingface"
        },
        {
            "name": "Pollinations.ai",
            "url": "https://image.pollinations.ai/prompt/{}",
            "method": "pollinations"
        }
    ]
    
    for api in apis:
        try:
            print(f"Trying {api['name']}...")
            
            if api['method'] == 'huggingface':
                headers = {"Content-Type": "application/json"}
                # Note: Add your Hugging Face token if needed: headers["Authorization"] = "Bearer YOUR_TOKEN"
                payload = {"inputs": prompt}
                response = requests.post(api['url'], headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    with open(output_file, "wb") as f:
                        f.write(response.content)
                    print(f"✓ AI-generated image saved: {output_file}")
                    return
                else:
                    print(f"  {api['name']} returned status {response.status_code}")
                    
            elif api['method'] == 'pollinations':
                # Pollinations.ai - Free, no API key required
                url = api['url'].format(quote(prompt))
                response = requests.get(url, timeout=60)
                
                if response.status_code == 200:
                    with open(output_file, "wb") as f:
                        f.write(response.content)
                    print(f"✓ AI-generated image saved: {output_file}")
                    return
                else:
                    print(f"  {api['name']} returned status {response.status_code}")
                    
        except requests.exceptions.Timeout:
            print(f"  {api['name']} timed out")
        except Exception as e:
            print(f"  {api['name']} error: {str(e)}")
    
    # Fallback to PIL-based generation if all APIs fail
    print("\n⚠ All AI APIs failed. Falling back to PIL-based generation...")
    generate_image(prompt, output_file, use_gimp=False)

def main():
    parser = argparse.ArgumentParser(description="Generate storyboard images with AI or PIL.")
    parser.add_argument("--prompt", required=True, help="Text description for the image.")
    parser.add_argument("--output_file", required=True, help="Path to save the generated PNG.")
    parser.add_argument("--use-ai", action="store_true", help="Use Stable Diffusion AI for image generation.")
    args = parser.parse_args()

    if args.use_ai:
        generate_image_with_ai(args.prompt, args.output_file)
    else:
        generate_image(args.prompt, args.output_file, use_gimp=False)
    
    print(f"\nImage generated successfully: {args.output_file}")

if __name__ == "__main__":
    main()