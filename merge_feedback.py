#!/usr/bin/env python3
"""
Merge feedback files from the feedback/ folder into a single consolidated file.

Usage:
    python merge_feedback.py [--input-dir FOLDER] [--output FILE]

Reads all .json feedback files exported by the browser from the specified folder
(default: feedback/) and merges them into a single consolidated feedback file.
Duplicate entries (same word + field + suggestion) are removed.
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def load_feedback_file(filepath):
    """Load a single feedback JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if 'feedback' in data:
        return data['feedback']
    if isinstance(data, list):
        return data
    return []


def make_dedup_key(entry):
    """Create a deduplication key from feedback entry."""
    return (
        entry.get('level', ''),
        entry.get('topic', ''),
        entry.get('word', ''),
        entry.get('field', ''),
        entry.get('suggestion', ''),
        entry.get('comment', '')
    )


def merge_feedback_files(input_dir, output_file):
    """Merge all feedback JSON files from input_dir into output_file."""
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Folder '{input_dir}' does not exist.")
        return False

    files = sorted(input_path.glob('*.json'))
    if not files:
        print(f"❌ No .json files found in '{input_dir}'.")
        return False

    all_entries = []
    seen = set()
    loaded_count = 0

    for fpath in files:
        try:
            entries = load_feedback_file(fpath)
            for entry in entries:
                key = make_dedup_key(entry)
                if key not in seen:
                    seen.add(key)
                    if 'status' not in entry:
                        entry['status'] = 'pending'
                    all_entries.append(entry)
            loaded_count += 1
            print(f"  📄 Loaded {fpath.name} ({len(entries)} entries)")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ⚠️ Skipped {fpath.name}: {e}")

    merged = {
        'merged_at': datetime.now().isoformat(),
        'source_files': loaded_count,
        'total_entries': len(all_entries),
        'feedback': all_entries
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Merged {len(all_entries)} unique entries from {loaded_count} files.")
    print(f"   Output: {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Merge feedback files into one consolidated file.')
    parser.add_argument('--input-dir', default='feedback', help='Folder with feedback .json files (default: feedback)')
    parser.add_argument('--output', default='feedback_merged.json', help='Output merged file (default: feedback_merged.json)')
    args = parser.parse_args()

    print("🔄 Merging feedback files...")
    merge_feedback_files(args.input_dir, args.output)


if __name__ == '__main__':
    main()
