#!/usr/bin/env python3
"""
Frame Preprocessing Module
Batch enhance animation frames before GIF compilation to ensure consistent quality
"""
import os
import sys
import argparse
from pathlib import Path
import glob
from enhance_image import ImageEnhancer


class FramePreprocessor:
    """Batch enhance animation frames with progress tracking"""
    
    def __init__(self, use_gimp=False, gimp_path=None):
        """
        Initialize frame preprocessor
        
        Args:
            use_gimp (bool): Whether to use GIMP for enhancement
            gimp_path (str): Path to GIMP executable
        """
        self.enhancer = ImageEnhancer(use_gimp=use_gimp, gimp_path=gimp_path)
    
    def preprocess_frames(self, frame_directory, output_directory=None, 
                         preset='medium', operations=None, pattern='*.png'):
        """
        Enhance all frames in a directory
        
        Args:
            frame_directory (str): Directory containing frame images
            output_directory (str): Directory to save enhanced frames (default: frame_directory + '_enhanced')
            preset (str): Enhancement preset
            operations (dict): Custom operations
            pattern (str): Glob pattern for frame files
            
        Returns:
            dict: Result with status, enhanced frames list, and statistics
        """
        try:
            if not os.path.exists(frame_directory):
                return self._error("directory_not_found", f"Directory not found: {frame_directory}")
            
            # Determine output directory
            if output_directory is None:
                output_directory = frame_directory + '_enhanced'
            
            os.makedirs(output_directory, exist_ok=True)
            
            # Find all frame files
            frame_pattern = os.path.join(frame_directory, pattern)
            frame_files = sorted(glob.glob(frame_pattern))
            
            if not frame_files:
                return self._error("no_frames", f"No frames found matching pattern: {pattern}")
            
            print(f"\n{'='*60}")
            print(f"🎬 Preprocessing {len(frame_files)} animation frames")
            print(f"📁 Input: {frame_directory}")
            print(f"📁 Output: {output_directory}")
            print(f"📋 Preset: {preset}")
            print(f"{'='*60}\n")
            
            # Process each frame
            enhanced_frames = []
            failed_frames = []
            
            for idx, frame_path in enumerate(frame_files, 1):
                frame_name = os.path.basename(frame_path)
                output_path = os.path.join(output_directory, frame_name)
                
                print(f"[{idx}/{len(frame_files)}] Enhancing: {frame_name}")
                
                result = self.enhancer.enhance(
                    frame_path,
                    output_path,
                    preset=preset,
                    operations=operations
                )
                
                if result['status'] == 'ok':
                    enhanced_frames.append(output_path)
                    print(f"  ✓ Enhanced: {frame_name}\n")
                else:
                    failed_frames.append({
                        'frame': frame_name,
                        'error': result['message']
                    })
                    print(f"  ✗ Failed: {result['message']}\n")
            
            # Summary
            print(f"{'='*60}")
            print(f"✓ Preprocessing complete")
            print(f"  Enhanced: {len(enhanced_frames)}/{len(frame_files)} frames")
            if failed_frames:
                print(f"  Failed: {len(failed_frames)} frames")
            print(f"{'='*60}\n")
            
            return {
                'status': 'ok' if enhanced_frames else 'error',
                'code': 'success' if enhanced_frames else 'all_failed',
                'message': f'Enhanced {len(enhanced_frames)} frames',
                'enhanced_frames': enhanced_frames,
                'failed_frames': failed_frames,
                'output_directory': output_directory,
                'total_frames': len(frame_files),
                'success_count': len(enhanced_frames),
                'failure_count': len(failed_frames)
            }
            
        except Exception as e:
            return self._error("preprocessing_failed", str(e))
    
    def validate_frames(self, frame_directory, expected_resolution=None):
        """
        Validate that all frames exist and have consistent properties
        
        Args:
            frame_directory (str): Directory containing frames
            expected_resolution (tuple): Expected (width, height) or None
            
        Returns:
            dict: Validation result with status and issues list
        """
        from PIL import Image
        
        try:
            frame_files = sorted(glob.glob(os.path.join(frame_directory, '*.png')))
            
            if not frame_files:
                return self._error("no_frames", "No PNG frames found")
            
            issues = []
            resolutions = {}
            
            for frame_path in frame_files:
                frame_name = os.path.basename(frame_path)
                
                try:
                    with Image.open(frame_path) as img:
                        resolution = img.size
                        
                        # Track resolution distribution
                        if resolution not in resolutions:
                            resolutions[resolution] = []
                        resolutions[resolution].append(frame_name)
                        
                        # Check against expected resolution
                        if expected_resolution and resolution != expected_resolution:
                            issues.append({
                                'frame': frame_name,
                                'issue': 'wrong_resolution',
                                'expected': expected_resolution,
                                'actual': resolution
                            })
                        
                except Exception as e:
                    issues.append({
                        'frame': frame_name,
                        'issue': 'corrupt_or_unreadable',
                        'error': str(e)
                    })
            
            # Check for multiple resolutions
            if len(resolutions) > 1:
                for resolution, frames in resolutions.items():
                    if len(frames) < len(frame_files) / 2:  # Minority resolution
                        for frame in frames:
                            issues.append({
                                'frame': frame,
                                'issue': 'inconsistent_resolution',
                                'resolution': resolution,
                                'common_resolution': max(resolutions.keys(), key=lambda k: len(resolutions[k]))
                            })
            
            return {
                'status': 'ok' if not issues else 'warning',
                'code': 'validated' if not issues else 'issues_found',
                'message': f'Validated {len(frame_files)} frames',
                'total_frames': len(frame_files),
                'resolutions': {str(k): len(v) for k, v in resolutions.items()},
                'issues': issues
            }
            
        except Exception as e:
            return self._error("validation_failed", str(e))
    
    def _error(self, code, message):
        """Return error result"""
        return {
            'status': 'error',
            'code': code,
            'message': message
        }


def main():
    parser = argparse.ArgumentParser(
        description="Batch enhance animation frames before GIF compilation"
    )
    parser.add_argument(
        'input_directory',
        help="Directory containing animation frames"
    )
    parser.add_argument(
        '-o', '--output-directory',
        help="Output directory for enhanced frames (default: input_enhanced)"
    )
    parser.add_argument(
        '-p', '--preset',
        choices=['light', 'medium', 'aggressive'],
        default='medium',
        help="Enhancement preset (default: medium)"
    )
    parser.add_argument(
        '--pattern',
        default='*.png',
        help="File pattern for frames (default: *.png)"
    )
    parser.add_argument(
        '--use-gimp',
        action='store_true',
        help="Use GIMP for advanced enhancement"
    )
    parser.add_argument(
        '--gimp-path',
        help="Path to GIMP executable"
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help="Only validate frames without enhancing"
    )
    parser.add_argument(
        '--expected-resolution',
        help="Expected resolution as WIDTHxHEIGHT (e.g., 800x600)"
    )
    
    args = parser.parse_args()
    
    # Create preprocessor
    preprocessor = FramePreprocessor(
        use_gimp=args.use_gimp,
        gimp_path=args.gimp_path
    )
    
    # Parse expected resolution
    expected_resolution = None
    if args.expected_resolution:
        try:
            w, h = args.expected_resolution.split('x')
            expected_resolution = (int(w), int(h))
        except:
            print(f"✗ Invalid resolution format: {args.expected_resolution}")
            sys.exit(1)
    
    # Validate or preprocess
    if args.validate_only:
        result = preprocessor.validate_frames(
            args.input_directory,
            expected_resolution=expected_resolution
        )
        
        print(f"\n{'='*60}")
        print(f"🔍 Frame Validation Results")
        print(f"{'='*60}")
        print(f"Status: {result['status']}")
        print(f"Total frames: {result.get('total_frames', 0)}")
        print(f"Resolutions: {result.get('resolutions', {})}")
        
        if result.get('issues'):
            print(f"\n⚠ Issues found: {len(result['issues'])}")
            for issue in result['issues'][:10]:  # Show first 10
                print(f"  • {issue['frame']}: {issue['issue']}")
        else:
            print("\n✓ All frames validated successfully")
        
        print(f"{'='*60}\n")
        
    else:
        result = preprocessor.preprocess_frames(
            args.input_directory,
            output_directory=args.output_directory,
            preset=args.preset,
            pattern=args.pattern
        )
        
        if result['status'] == 'error':
            print(f"\n✗ Error: {result['message']}")
            sys.exit(1)
        
        if result.get('failed_frames'):
            print(f"\n⚠ Some frames failed:")
            for failed in result['failed_frames'][:10]:
                print(f"  • {failed['frame']}: {failed['error']}")
    
    sys.exit(0 if result['status'] in ('ok', 'warning') else 1)


if __name__ == '__main__':
    main()
