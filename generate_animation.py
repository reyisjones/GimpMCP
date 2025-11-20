#!/usr/bin/env python3
"""
Animated GIF Generator
Generates a sequence of PNG images and compiles them into an animated GIF
"""
import os
import sys
import argparse
from pathlib import Path
from PIL import Image

# Add MCP directory to path
sys.path.insert(0, str(Path(__file__).parent / "MCP" / "gimp-image-gen"))
from gimp_image_gen import generate_image, generate_image_with_ai


class AnimationGenerator:
    """Generate animated GIF from a sequence of text prompts"""
    
    def __init__(self, output_dir="animations", frame_rate=10, resolution=(512, 512)):
        """
        Initialize animation generator
        
        Args:
            output_dir (str): Directory to save frames and final GIF
            frame_rate (int): Frames per second for the animation
            resolution (tuple): Output resolution (width, height)
        """
        self.output_dir = output_dir
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.frame_duration = int(1000 / frame_rate)  # milliseconds per frame
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_frame(self, prompt, frame_number, use_ai=True):
        """
        Generate a single animation frame
        
        Args:
            prompt (str): Text description for the frame
            frame_number (int): Frame index
            use_ai (bool): Whether to use AI generation
            
        Returns:
            str: Path to the generated frame
        """
        frame_filename = f"frame_{frame_number:04d}.png"
        frame_path = os.path.join(self.output_dir, frame_filename)
        
        print(f"[Frame {frame_number}] Generating: {prompt[:60]}...")
        
        try:
            if use_ai:
                generate_image_with_ai(prompt, frame_path)
            else:
                generate_image(prompt, frame_path, use_gimp=False)
            
            # Resize to target resolution if needed
            self._resize_frame(frame_path)
            
            print(f"    ✓ Saved: {frame_path}")
            return frame_path
            
        except Exception as e:
            print(f"    ✗ Error generating frame {frame_number}: {e}")
            return None
    
    def _resize_frame(self, frame_path):
        """Resize frame to target resolution"""
        try:
            with Image.open(frame_path) as img:
                if img.size != self.resolution:
                    img_resized = img.resize(self.resolution, Image.Resampling.LANCZOS)
                    img_resized.save(frame_path, 'PNG')
        except Exception as e:
            print(f"    ⚠ Warning: Could not resize frame: {e}")
    
    def generate_frames(self, prompts, use_ai=True):
        """
        Generate all animation frames
        
        Args:
            prompts (list): List of text descriptions for each frame
            use_ai (bool): Whether to use AI generation
            
        Returns:
            list: Paths to successfully generated frames
        """
        print(f"\n{'='*60}")
        print(f"🎬 Generating {len(prompts)} animation frames")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📏 Resolution: {self.resolution[0]}x{self.resolution[1]}")
        print(f"🎞️  Frame rate: {self.frame_rate} fps")
        print(f"{'='*60}\n")
        
        frame_paths = []
        
        for idx, prompt in enumerate(prompts, start=1):
            frame_path = self.generate_frame(prompt, idx, use_ai=use_ai)
            if frame_path:
                frame_paths.append(frame_path)
            else:
                print(f"\n⚠ Warning: Frame {idx} failed to generate")
        
        return frame_paths
    
    def validate_frames(self, frame_paths):
        """
        Validate that all frames were generated successfully
        
        Args:
            frame_paths (list): List of frame file paths
            
        Returns:
            bool: True if all frames are valid
        """
        print(f"\n🔍 Validating {len(frame_paths)} frames...")
        
        invalid_frames = []
        
        for frame_path in frame_paths:
            if not os.path.exists(frame_path):
                invalid_frames.append(frame_path)
                print(f"    ✗ Missing: {frame_path}")
            else:
                try:
                    with Image.open(frame_path) as img:
                        if img.size != self.resolution:
                            print(f"    ⚠ Size mismatch: {frame_path} ({img.size})")
                except Exception as e:
                    invalid_frames.append(frame_path)
                    print(f"    ✗ Corrupt: {frame_path} - {e}")
        
        if invalid_frames:
            print(f"\n✗ Validation failed: {len(invalid_frames)} invalid frames")
            return False
        
        print(f"✓ All {len(frame_paths)} frames validated successfully\n")
        return True
    
    def create_gif(self, frame_paths, output_filename="animation.gif", loop=0):
        """
        Compile PNG sequence into animated GIF
        
        Args:
            frame_paths (list): List of frame file paths
            output_filename (str): Name of output GIF file
            loop (int): Number of loops (0 = infinite)
            
        Returns:
            str: Path to generated GIF
        """
        if not frame_paths:
            print("✗ No frames to compile")
            return None
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        print(f"🎬 Compiling {len(frame_paths)} frames into GIF...")
        print(f"   Duration per frame: {self.frame_duration}ms")
        print(f"   Loop count: {'infinite' if loop == 0 else loop}")
        
        try:
            # Load all frames
            frames = []
            for frame_path in frame_paths:
                img = Image.open(frame_path)
                # Convert to RGB if necessary (GIF doesn't support transparency well)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                frames.append(img)
            
            # Save as animated GIF
            frames[0].save(
                output_path,
                format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=self.frame_duration,
                loop=loop,
                optimize=True
            )
            
            # Close all images
            for frame in frames:
                frame.close()
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✓ GIF created successfully: {output_path}")
            print(f"   File size: {file_size:.2f} MB")
            print(f"   Total frames: {len(frame_paths)}")
            print(f"   Animation duration: {len(frame_paths) * self.frame_duration / 1000:.2f}s")
            
            return output_path
            
        except Exception as e:
            print(f"✗ Error creating GIF: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate animated GIF from text prompt sequences"
    )
    parser.add_argument(
        "--prompts",
        nargs="+",
        required=True,
        help="List of prompts for each frame"
    )
    parser.add_argument(
        "--output-dir",
        default="animations",
        help="Directory to save frames and GIF (default: animations)"
    )
    parser.add_argument(
        "--output-name",
        default="animation.gif",
        help="Name of output GIF file (default: animation.gif)"
    )
    parser.add_argument(
        "--frame-rate",
        type=int,
        default=10,
        help="Frames per second (default: 10)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=512,
        help="Frame width in pixels (default: 512)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=512,
        help="Frame height in pixels (default: 512)"
    )
    parser.add_argument(
        "--use-ai",
        action="store_true",
        help="Use AI generation for frames (slower but higher quality)"
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=0,
        help="Number of loops (0 = infinite, default: 0)"
    )
    parser.add_argument(
        "--interpolate",
        type=int,
        default=1,
        help="Generate N interpolated frames between each prompt (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Create animation generator
    generator = AnimationGenerator(
        output_dir=args.output_dir,
        frame_rate=args.frame_rate,
        resolution=(args.width, args.height)
    )
    
    # Interpolate prompts if requested
    prompts = args.prompts
    if args.interpolate > 1:
        interpolated_prompts = []
        for i, prompt in enumerate(prompts):
            interpolated_prompts.append(prompt)
            if i < len(prompts) - 1:
                # Add interpolated frames
                for j in range(1, args.interpolate):
                    weight = j / args.interpolate
                    interpolated_prompt = f"Transition from ({prompt}) to ({prompts[i+1]}), stage {j}/{args.interpolate}"
                    interpolated_prompts.append(interpolated_prompt)
        prompts = interpolated_prompts
    
    # Generate frames
    frame_paths = generator.generate_frames(prompts, use_ai=args.use_ai)
    
    # Validate frames
    if not generator.validate_frames(frame_paths):
        print("\n⚠ Some frames failed validation. Proceeding with available frames...")
    
    # Create GIF
    gif_path = generator.create_gif(frame_paths, args.output_name, loop=args.loop)
    
    if gif_path:
        print(f"\n{'='*60}")
        print(f"🎉 Animation complete!")
        print(f"📁 GIF saved to: {gif_path}")
        print(f"🗂️  Frames saved to: {args.output_dir}/")
        print(f"{'='*60}\n")
    else:
        print("\n✗ Animation generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
