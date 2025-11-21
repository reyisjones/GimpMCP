#!/usr/bin/env python3
"""
Image Enhancement Module
Applies quality improvements to AI-generated images using Pillow and optional GIMP batch operations.
"""
import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import subprocess
import tempfile
import json


class ImageEnhancer:
    """Enhance images with auto-levels, denoise, sharpen, and artifact removal"""
    
    PRESETS = {
        'light': {
            'auto_levels': True,
            'denoise': 1,
            'sharpen': 0.3,
            'despeckle': False,
            'brightness': 1.05,
            'contrast': 1.05,
            'saturation': 1.0
        },
        'medium': {
            'auto_levels': True,
            'denoise': 2,
            'sharpen': 0.5,
            'despeckle': True,
            'brightness': 1.1,
            'contrast': 1.1,
            'saturation': 1.05
        },
        'aggressive': {
            'auto_levels': True,
            'denoise': 3,
            'sharpen': 0.8,
            'despeckle': True,
            'brightness': 1.15,
            'contrast': 1.15,
            'saturation': 1.1
        }
    }
    
    def __init__(self, use_gimp=False, gimp_path=None):
        """
        Initialize image enhancer
        
        Args:
            use_gimp (bool): Whether to use GIMP batch operations for advanced enhancement
            gimp_path (str): Path to GIMP executable (auto-detected if None)
        """
        self.use_gimp = use_gimp
        self.gimp_path = gimp_path or self._find_gimp()
        
        if use_gimp and not self.gimp_path:
            print("⚠ GIMP not found. Falling back to Pillow-only enhancement.")
            self.use_gimp = False
    
    def _find_gimp(self):
        """Auto-detect GIMP installation"""
        possible_paths = [
            '/Applications/GIMP.app/Contents/MacOS/gimp',
            '/usr/local/bin/gimp',
            '/usr/bin/gimp',
            'gimp'  # System PATH
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, 
                                      timeout=5)
                if result.returncode == 0:
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return None
    
    def enhance(self, image_path, output_path, preset='medium', operations=None):
        """
        Enhance an image using the specified preset or custom operations
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save enhanced image
            preset (str): Enhancement preset (light|medium|aggressive)
            operations (dict): Custom operations to override preset
            
        Returns:
            dict: Result with status, message, and output path
        """
        try:
            if not os.path.exists(image_path):
                return self._error("input_not_found", f"Input image not found: {image_path}")
            
            # Load preset or use custom operations
            if operations is None:
                if preset not in self.PRESETS:
                    return self._error("invalid_preset", f"Unknown preset: {preset}")
                operations = self.PRESETS[preset].copy()
            
            print(f"\n{'='*60}")
            print(f"🎨 Enhancing image: {os.path.basename(image_path)}")
            print(f"📋 Preset: {preset}")
            print(f"{'='*60}\n")
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            
            # Open image
            img = Image.open(image_path)
            original_mode = img.mode
            
            # Convert to RGB for processing if needed
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            # Apply PIL-based enhancements
            img = self._apply_pil_enhancements(img, operations)
            
            # Apply GIMP-based enhancements if enabled
            if self.use_gimp:
                temp_path = output_path + '.temp.png'
                img.save(temp_path, 'PNG')
                result = self._apply_gimp_enhancements(temp_path, output_path, operations)
                
                if result['status'] == 'error':
                    print(f"⚠ GIMP enhancement failed: {result['message']}")
                    print("  Falling back to PIL-only result")
                    img.save(output_path, 'PNG')
                else:
                    # GIMP succeeded, clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            else:
                # Save PIL-enhanced image
                img.save(output_path, 'PNG')
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"\n✓ Enhancement complete: {output_path}")
            print(f"  File size: {file_size:.2f} KB")
            print(f"{'='*60}\n")
            
            return self._success(output_path)
            
        except Exception as e:
            return self._error("enhancement_failed", str(e))
    
    def _apply_pil_enhancements(self, img, operations):
        """Apply PIL-based image enhancements"""
        print("🔧 Applying PIL enhancements...")
        
        # Auto levels (histogram stretch)
        if operations.get('auto_levels'):
            print("  • Auto levels")
            img = self._auto_levels(img)
        
        # Denoise (median filter)
        denoise_level = operations.get('denoise', 0)
        if denoise_level > 0:
            print(f"  • Denoise (level {denoise_level})")
            for _ in range(denoise_level):
                img = img.filter(ImageFilter.MedianFilter(size=3))
        
        # Brightness adjustment
        brightness = operations.get('brightness', 1.0)
        if brightness != 1.0:
            print(f"  • Brightness ({brightness:.2f})")
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
        
        # Contrast adjustment
        contrast = operations.get('contrast', 1.0)
        if contrast != 1.0:
            print(f"  • Contrast ({contrast:.2f})")
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
        
        # Saturation adjustment
        saturation = operations.get('saturation', 1.0)
        if saturation != 1.0:
            print(f"  • Saturation ({saturation:.2f})")
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(saturation)
        
        # Sharpening
        sharpen = operations.get('sharpen', 0)
        if sharpen > 0:
            print(f"  • Sharpen ({sharpen:.2f})")
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.0 + sharpen)
        
        return img
    
    def _auto_levels(self, img):
        """Stretch histogram to improve contrast"""
        if img.mode not in ('L', 'RGB', 'RGBA'):
            return img
        
        # Get histogram and stretch it
        extrema = img.getextrema()
        
        if img.mode == 'L':
            # Grayscale
            if extrema[0] == extrema[1]:
                return img
            scale = 255.0 / (extrema[1] - extrema[0])
            offset = -extrema[0] * scale
            return img.point(lambda x: x * scale + offset)
        else:
            # RGB/RGBA - process each channel
            channels = img.split()
            processed = []
            
            for i, channel in enumerate(channels):
                if i < 3:  # Only process RGB, not alpha
                    extrema_c = channel.getextrema()
                    if extrema_c[0] != extrema_c[1]:
                        scale = 255.0 / (extrema_c[1] - extrema_c[0])
                        offset = -extrema_c[0] * scale
                        channel = channel.point(lambda x: x * scale + offset)
                processed.append(channel)
            
            return Image.merge(img.mode, processed)
    
    def _apply_gimp_enhancements(self, input_path, output_path, operations):
        """Apply GIMP batch enhancements using Script-Fu"""
        print("🎨 Applying GIMP enhancements...")
        
        # Build GIMP Script-Fu commands
        script = self._build_gimp_script(input_path, output_path, operations)
        
        try:
            # Write script to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.scm', delete=False) as f:
                f.write(script)
                script_path = f.name
            
            # Run GIMP in batch mode
            cmd = [
                self.gimp_path,
                '-i',  # No interface
                '-b', f'(load "{script_path}")',
                '-b', '(gimp-quit 0)'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=60,
                text=True
            )
            
            # Clean up script
            os.remove(script_path)
            
            if result.returncode != 0:
                return self._error("gimp_failed", f"GIMP returned error: {result.stderr}")
            
            if not os.path.exists(output_path):
                return self._error("gimp_no_output", "GIMP did not produce output file")
            
            print("  ✓ GIMP enhancement complete")
            return self._success(output_path)
            
        except subprocess.TimeoutExpired:
            return self._error("gimp_timeout", "GIMP operation timed out")
        except Exception as e:
            return self._error("gimp_error", str(e))
    
    def _build_gimp_script(self, input_path, output_path, operations):
        """Build Script-Fu code for GIMP batch processing"""
        script = f"""
(define (enhance-image input-file output-file)
  (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE input-file input-file)))
         (drawable (car (gimp-image-get-active-layer image))))
    
"""
        
        # Despeckle
        if operations.get('despeckle'):
            script += """
    ; Despeckle to remove artifacts
    (plug-in-despeckle RUN-NONINTERACTIVE image drawable 3 1 7 248)
"""
        
        # Auto levels (histogram stretch)
        if operations.get('auto_levels'):
            script += """
    ; Auto levels
    (gimp-levels-stretch drawable)
"""
        
        # Unsharp mask for sharpening
        sharpen = operations.get('sharpen', 0)
        if sharpen > 0:
            radius = min(5.0, sharpen * 5)
            amount = min(1.5, sharpen * 2)
            script += f"""
    ; Unsharp mask
    (plug-in-unsharp-mask RUN-NONINTERACTIVE image drawable {radius} {amount} 0)
"""
        
        # Save and cleanup
        script += f"""
    ; Save result
    (file-png-save RUN-NONINTERACTIVE image drawable "{output_path}" "{output_path}" 0 9 0 0 0 0 0)
    
    ; Cleanup
    (gimp-image-delete image)))

(enhance-image "{input_path}" "{output_path}")
"""
        
        return script
    
    def _success(self, output_path):
        """Return success result"""
        return {
            'status': 'ok',
            'code': 'success',
            'message': 'Enhancement completed successfully',
            'output_path': output_path
        }
    
    def _error(self, code, message):
        """Return error result"""
        return {
            'status': 'error',
            'code': code,
            'message': message,
            'output_path': None
        }


def main():
    parser = argparse.ArgumentParser(
        description="Enhance AI-generated images with auto-levels, denoise, sharpen, and artifact removal"
    )
    parser.add_argument(
        'input',
        help="Input image file"
    )
    parser.add_argument(
        '-o', '--output',
        help="Output image file (default: input_enhanced.png)"
    )
    parser.add_argument(
        '-p', '--preset',
        choices=['light', 'medium', 'aggressive'],
        default='medium',
        help="Enhancement preset (default: medium)"
    )
    parser.add_argument(
        '--use-gimp',
        action='store_true',
        help="Use GIMP batch operations for advanced enhancement"
    )
    parser.add_argument(
        '--gimp-path',
        help="Path to GIMP executable (auto-detected if not specified)"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Output result as JSON"
    )
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(args.input)
        output_path = f"{base}_enhanced{ext}"
    
    # Create enhancer
    enhancer = ImageEnhancer(use_gimp=args.use_gimp, gimp_path=args.gimp_path)
    
    # Enhance image
    result = enhancer.enhance(args.input, output_path, preset=args.preset)
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result['status'] == 'error':
            print(f"\n✗ Error: {result['message']}")
            sys.exit(1)
    
    sys.exit(0 if result['status'] == 'ok' else 1)


if __name__ == '__main__':
    main()
