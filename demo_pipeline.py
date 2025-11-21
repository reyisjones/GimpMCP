#!/usr/bin/env python3
"""
Complete Pipeline Example
Demonstrates the full workflow: prompt → generate → enhance → animate → optimize
"""
import os
import sys
from pathlib import Path

# Add MCP directory to path
sys.path.insert(0, str(Path(__file__).parent / "MCP" / "gimp-image-gen"))
from gimp_image_gen import generate_image_with_ai
from enhance_image import ImageEnhancer
from generate_animation import AnimationGenerator


def demo_single_image_workflow():
    """Demonstrate single image generation with enhancement"""
    print("\n" + "="*60)
    print("DEMO 1: Single Image Generation + Enhancement")
    print("="*60 + "\n")
    
    # Step 1: Generate image
    prompt = "A majestic mountain landscape at sunset, realistic lighting, high detail"
    raw_output = "demo_output/mountain_raw.png"
    
    print("Step 1: Generating image with AI...")
    os.makedirs("demo_output", exist_ok=True)
    generate_image_with_ai(prompt, raw_output)
    print(f"✓ Generated: {raw_output}\n")
    
    # Step 2: Enhance image
    enhanced_output = "demo_output/mountain_enhanced.png"
    print("Step 2: Enhancing image...")
    
    enhancer = ImageEnhancer(use_gimp=False)
    result = enhancer.enhance(raw_output, enhanced_output, preset='medium')
    
    if result['status'] == 'ok':
        print(f"✓ Enhanced: {enhanced_output}\n")
    else:
        print(f"✗ Enhancement failed: {result['message']}\n")
    
    print("Compare the results:")
    print(f"  Raw: {raw_output}")
    print(f"  Enhanced: {enhanced_output}\n")


def demo_animation_workflow():
    """Demonstrate animation generation with integrated enhancement"""
    print("\n" + "="*60)
    print("DEMO 2: Animation Generation with Auto-Enhancement")
    print("="*60 + "\n")
    
    # Define animation prompts
    prompts = [
        "A hot air balloon floating in a clear blue sky, morning light",
        "The balloon drifting higher, same style and lighting",
        "The balloon at altitude with clouds around it, consistent perspective",
        "The balloon descending slightly, evening golden hour light"
    ]
    
    # Create animation generator with enhancement enabled
    generator = AnimationGenerator(
        output_dir="demo_output/balloon_frames",
        frame_rate=8,
        resolution=(800, 600),
        enhance=True,
        enhancement_preset='medium',
        use_gimp=False
    )
    
    print("Generating and enhancing animation frames...")
    frame_paths = generator.generate_frames(prompts, use_ai=True)
    
    # Validate frames
    if generator.validate_frames(frame_paths):
        # Create GIF
        gif_path = generator.create_gif(frame_paths, "balloon_demo.gif", loop=0)
        
        if gif_path:
            print(f"\n✓ Demo animation complete: {gif_path}")
            print(f"  Frames: {len(frame_paths)}")
            print(f"  Enhanced: Yes")
            print(f"  Output: {gif_path}\n")
    else:
        print("\n✗ Frame validation failed\n")


def demo_batch_enhancement():
    """Demonstrate batch enhancement of existing frames"""
    print("\n" + "="*60)
    print("DEMO 3: Batch Enhancement of Existing Frames")
    print("="*60 + "\n")
    
    # Create some test frames first
    print("Creating test frames...")
    os.makedirs("demo_output/test_frames", exist_ok=True)
    
    test_prompts = [
        "Simple geometric pattern, red and blue",
        "Simple geometric pattern, green and yellow",
        "Simple geometric pattern, orange and purple"
    ]
    
    for idx, prompt in enumerate(test_prompts, 1):
        frame_path = f"demo_output/test_frames/frame_{idx:04d}.png"
        generate_image_with_ai(prompt, frame_path)
        print(f"  Created: frame_{idx:04d}.png")
    
    print("\nEnhancing frames in batch...")
    
    from preprocess_frames import FramePreprocessor
    
    preprocessor = FramePreprocessor(use_gimp=False)
    result = preprocessor.preprocess_frames(
        "demo_output/test_frames",
        output_directory="demo_output/test_frames_enhanced",
        preset='aggressive'
    )
    
    if result['status'] == 'ok':
        print(f"\n✓ Batch enhancement complete")
        print(f"  Enhanced: {result['success_count']} frames")
        print(f"  Failed: {result['failure_count']} frames")
        print(f"  Output: {result['output_directory']}\n")
    else:
        print(f"\n✗ Batch enhancement failed: {result['message']}\n")


def demo_comparison():
    """Generate side-by-side comparison of enhancement presets"""
    print("\n" + "="*60)
    print("DEMO 4: Enhancement Preset Comparison")
    print("="*60 + "\n")
    
    # Generate base image
    prompt = "A detailed portrait of a robot, metallic surfaces, studio lighting"
    base_image = "demo_output/robot_base.png"
    
    print("Generating base image...")
    os.makedirs("demo_output", exist_ok=True)
    generate_image_with_ai(prompt, base_image)
    print(f"✓ Generated: {base_image}\n")
    
    # Test each preset
    presets = ['light', 'medium', 'aggressive']
    enhancer = ImageEnhancer(use_gimp=False)
    
    print("Testing enhancement presets...")
    for preset in presets:
        output = f"demo_output/robot_{preset}.png"
        print(f"\n  Preset: {preset}")
        result = enhancer.enhance(base_image, output, preset=preset)
        
        if result['status'] == 'ok':
            print(f"  ✓ {output}")
        else:
            print(f"  ✗ Failed: {result['message']}")
    
    print("\nComparison files created:")
    print(f"  Base: {base_image}")
    for preset in presets:
        print(f"  {preset.capitalize()}: demo_output/robot_{preset}.png")
    print()


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("🎨 GIMP MCP - Complete Pipeline Demo")
    print("="*60)
    print("\nThis demo showcases:")
    print("  1. Single image generation + enhancement")
    print("  2. Animation with integrated enhancement")
    print("  3. Batch enhancement of existing frames")
    print("  4. Enhancement preset comparison")
    print("\nAll outputs will be saved to demo_output/")
    print("="*60)
    
    input("\nPress Enter to start the demos...")
    
    try:
        # Run demos
        demo_single_image_workflow()
        input("Press Enter to continue to next demo...")
        
        demo_animation_workflow()
        input("Press Enter to continue to next demo...")
        
        demo_batch_enhancement()
        input("Press Enter to continue to next demo...")
        
        demo_comparison()
        
        print("\n" + "="*60)
        print("✓ All demos complete!")
        print("="*60)
        print("\nGenerated files:")
        print("  demo_output/")
        print("    ├── mountain_raw.png")
        print("    ├── mountain_enhanced.png")
        print("    ├── balloon_frames/")
        print("    ├── balloon_demo.gif")
        print("    ├── test_frames/")
        print("    ├── test_frames_enhanced/")
        print("    ├── robot_base.png")
        print("    ├── robot_light.png")
        print("    ├── robot_medium.png")
        print("    └── robot_aggressive.png")
        print("\nExplore these files to see the enhancement quality!")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
