"""
Find matching image pairs in watermarked and no-watermark directories
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from pathlib import Path

# Define paths
no_watermark_path = "wm-nowm/train/no-watermark/"
watermark_path = "wm-nowm/train/watermark/"

print("Finding matching image pairs...")

# Get all images from both directories
all_wm_images = glob.glob(os.path.join(watermark_path, "*.*"))
all_no_wm_images = glob.glob(os.path.join(no_watermark_path, "*.*"))

# Extract just the filenames (not full paths)
wm_filenames = {os.path.basename(path): path for path in all_wm_images}
no_wm_filenames = {os.path.basename(path): path for path in all_no_wm_images}

# Find matching filenames
matching_names = set(wm_filenames.keys()) & set(no_wm_filenames.keys())

# Create pairs
matching_pairs = [
    {
        'filename': name,
        'watermark': wm_filenames[name],
        'no_watermark': no_wm_filenames[name]
    }
    for name in matching_names
]

print(f"\n{'='*80}")
print(f"MATCHING PAIRS SUMMARY")
print(f"{'='*80}")
print(f"Total watermarked images:     {len(all_wm_images):,}")
print(f"Total no-watermark images:    {len(all_no_wm_images):,}")
print(f"Matching pairs found:         {len(matching_pairs):,}")
print(f"{'='*80}")

# Show first 20 matching pairs
print(f"\nFirst 20 matching pairs:")
for i, pair in enumerate(matching_pairs[:20], 1):
    print(f"  {i:2d}. {pair['filename']}")

# Save matching pairs to a file
with open('matching_pairs.txt', 'w') as f:
    f.write(f"Total matching pairs: {len(matching_pairs)}\n")
    f.write("="*80 + "\n\n")
    for pair in matching_pairs:
        f.write(f"{pair['filename']}\n")
        f.write(f"  Watermark:    {pair['watermark']}\n")
        f.write(f"  No-watermark: {pair['no_watermark']}\n\n")

print(f"\n✓ Saved complete list to: matching_pairs.txt")

# Function to extract watermark
def extract_watermark_by_subtraction(wm_path, no_wm_path):
    """Extract watermark by subtracting images"""
    wm_img = cv2.imread(wm_path, cv2.IMREAD_GRAYSCALE)
    no_wm_img = cv2.imread(no_wm_path, cv2.IMREAD_GRAYSCALE)
    
    # Calculate absolute difference
    watermark = cv2.absdiff(wm_img, no_wm_img)
    
    # Enhance
    watermark_enhanced = cv2.equalizeHist(watermark)
    
    # Calculate statistics
    intensity = np.mean(watermark_enhanced)
    _, mask = cv2.threshold(watermark_enhanced, 30, 255, cv2.THRESH_BINARY)
    coverage = (np.count_nonzero(mask) / mask.size) * 100
    
    return intensity, coverage

# Analyze some pairs
if len(matching_pairs) > 0:
    print(f"\nAnalyzing first 10 matching pairs...")
    print(f"{'='*80}")
    print(f"{'Filename':<50} {'Intensity':<12} {'Coverage'}")
    print(f"{'-'*80}")
    
    for pair in matching_pairs[:10]:
        try:
            intensity, coverage = extract_watermark_by_subtraction(
                pair['watermark'], pair['no_watermark']
            )
            print(f"{pair['filename'][:48]:<50} {intensity:>8.2f}    {coverage:>8.2f}%")
        except Exception as e:
            print(f"{pair['filename'][:48]:<50} ERROR: {str(e)[:20]}")
    
    print(f"{'='*80}")

print("\n✓ Analysis complete!")
print("\nYou can now use these matching pairs in your notebook for direct watermark extraction!")

