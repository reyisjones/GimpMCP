#!/usr/bin/env python3
"""
Batch Storyboard Generator
Generates multiple storyboard panels from a list of prompts
"""
import os
import sys
from pathlib import Path

# Add MCP directory to path
sys.path.insert(0, str(Path(__file__).parent / "MCP" / "gimp-image-gen"))
from gimp_image_gen import generate_image

def generate_batch_storyboards(prompts, output_dir="storyboards"):
    """
    Generate multiple storyboard images from a list of prompts.
    
    Args:
        prompts (list): List of prompt strings
        output_dir (str): Directory to save output images
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎨 Generating {len(prompts)} storyboard panels...")
    print(f"📁 Output directory: {output_dir}\n")
    
    for idx, prompt in enumerate(prompts, start=1):
        output_file = os.path.join(output_dir, f"panel_{idx:03d}.png")
        
        print(f"[{idx}/{len(prompts)}] Generating: {prompt[:60]}...")
        try:
            generate_image(prompt, output_file, use_gimp=False)
            print(f"    ✓ Saved: {output_file}\n")
        except Exception as e:
            print(f"    ✗ Error: {e}\n")
    
    print(f"🎉 Batch generation complete! {len(prompts)} panels created in '{output_dir}'")

if __name__ == "__main__":
    # Example: Generate storyboard panels for "El Manjar de los Dioses" trailer
    example_prompts = [
        "Panel 1: Young Carlos in Hatillo, Puerto Rico, holding his first guitar, humble neighborhood in background",
        "Panel 2: Carlos and Reyis meeting for the first time, exchanging music ideas, excited expressions",
        "Panel 3: Early band rehearsal in cramped garage, instruments scattered, passionate playing",
        "Panel 4: Band members discussing their sound, whiteboard with song ideas, creative energy",
        "Panel 5: First live performance at small local venue, nervous but determined faces",
        "Panel 6: Audience reaction shot, people connecting with the music, emotional atmosphere",
    ]
    
    # Allow custom prompts via command line
    if len(sys.argv) > 1:
        # User provided custom output directory
        output_dir = sys.argv[1]
    else:
        output_dir = "storyboards"
    
    generate_batch_storyboards(example_prompts, output_dir)
    
    print("\n💡 Tip: Edit this script to add your own prompts!")
    print(f"   Generated images are ready for refinement in GIMP or other editors.")
