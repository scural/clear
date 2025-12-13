# Finds matching image pairs in watermarked and no-watermark directories, combines TRAIN and VALID folders

import os
import glob
from pathlib import Path

folders = [
    {
        'name': 'train',
        'watermark': 'wm-nowm/train/watermark/',
        'no_watermark': 'wm-nowm/train/no-watermark/'
    },
    {
        'name': 'valid',
        'watermark': 'wm-nowm/valid/watermark/',
        'no_watermark': 'wm-nowm/valid/no-watermark/'
    }
]

all_matching_pairs = []

for folder in folders:
    wm_images = glob.glob(os.path.join(folder['watermark'], "*.*"))
    no_wm_images = glob.glob(os.path.join(folder['no_watermark'], "*.*"))
    
    wm_filenames = {os.path.basename(path): path for path in wm_images}
    no_wm_filenames = {os.path.basename(path): path for path in no_wm_images}
    
    matching_names = set(wm_filenames.keys()) & set(no_wm_filenames.keys())
    pairs = [
        {
            'filename': name,
            'watermark': wm_filenames[name],
            'no_watermark': no_wm_filenames[name],
            'source': folder['name']
        }
        for name in matching_names
    ]

    all_matching_pairs.extend(pairs)

with open('matching_pairs_list.py', 'w') as f:
    f.write("# List of matching image pairs (TRAIN + VALID combined)\n")
    f.write(f"# Total: {len(all_matching_pairs)} pairs\n\n")
    f.write("matching_pairs = [\n")
    for pair in all_matching_pairs:
        f.write("    {\n")
        f.write(f"        'filename': '{pair['filename']}',\n")
        f.write(f"        'watermark': '{pair['watermark']}',\n")
        f.write(f"        'no_watermark': '{pair['no_watermark']}'\n")
        f.write("    },\n")
    f.write("]\n")

print(f"\nSaved {len(all_matching_pairs):,} pairs to: matching_pairs_list.py")
