#!/usr/bin/env python3
"""
Offline tool to review and accept/reject vocabulary feedback.
Approved feedback with suggestions are synced back to the original data files.

Usage:
    python review_feedback.py [--feedback FILE] [--data-dir DIR]

Interactive CLI tool that presents each pending feedback entry and lets you:
  - Accept (a): Apply the suggestion to the original data file
  - Reject (r): Mark as rejected
  - Skip (s): Leave as pending for later review
"""

import json
import os
import sys
import argparse
from pathlib import Path


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def find_data_file(data_dir, level):
    """Find the data file for a given level."""
    candidates = [
        os.path.join(data_dir, f'level{level}.json'),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def apply_suggestion(data_file, topic_id, word_str, field, suggestion):
    """Apply a suggestion to the original data file. Returns True if successful."""
    data = load_json(data_file)

    VALID_FIELDS = {'word', 'meaning', 'phonetic', 'image', 'audio', 'example', 'example_vi', 'hint'}

    for topic in data.get('topics', []):
        if topic['id'] != topic_id:
            continue
        for word_entry in topic.get('words', []):
            if word_entry.get('word') != word_str:
                continue
            if field in word_entry or field in VALID_FIELDS:
                old_val = word_entry.get(field, None)
                word_entry[field] = suggestion
                save_json(data_file, data)
                return True, old_val
            elif field == 'other':
                return False, None
            else:
                return False, None

    return False, None


def display_entry(idx, total, entry):
    """Display a feedback entry for review."""
    print(f"\n{'='*60}")
    print(f"  Feedback {idx + 1}/{total}")
    print(f"{'='*60}")
    print(f"  Level:    {entry.get('level', '?')}")
    print(f"  Topic:    {entry.get('topic', '?')}")
    print(f"  Word:     {entry.get('word', '?')}")
    print(f"  Field:    {entry.get('field', '?')}")
    print(f"  Current:  {entry.get('current_value', '?')}")
    print(f"  Comment:  {entry.get('comment', '(none)')}")
    print(f"  Suggest:  {entry.get('suggestion', '(none)')}")
    print(f"  Status:   {entry.get('status', 'pending')}")
    print(f"  Date:     {entry.get('created_at', '?')}")
    print(f"{'─'*60}")


def review_feedback(feedback_file, data_dir):
    """Interactive review loop for feedback entries."""
    if not os.path.exists(feedback_file):
        print(f"❌ Feedback file not found: {feedback_file}")
        return

    data = load_json(feedback_file)
    entries = data.get('feedback', [])
    if not entries:
        print("ℹ️ No feedback entries to review.")
        return

    pending = [(i, e) for i, e in enumerate(entries) if e.get('status', 'pending') == 'pending']
    if not pending:
        print("ℹ️ No pending feedback entries. All have been reviewed.")
        return

    print(f"\n📋 Found {len(pending)} pending feedback entries out of {len(entries)} total.\n")

    accepted = 0
    rejected = 0
    skipped = 0

    for seq, (idx, entry) in enumerate(pending):
        display_entry(seq, len(pending), entry)

        while True:
            choice = input("  [a]ccept / [r]eject / [s]kip / [q]uit > ").strip().lower()
            if choice in ('a', 'accept'):
                suggestion = entry.get('suggestion', '').strip()
                if not suggestion:
                    print("  ⚠️ No suggestion provided. Cannot auto-apply.")
                    confirm = input("  Accept without applying changes? [y/n] > ").strip().lower()
                    if confirm == 'y':
                        entries[idx]['status'] = 'accepted'
                        accepted += 1
                        print("  ✅ Marked as accepted (no changes applied).")
                    else:
                        continue
                else:
                    level = entry.get('level', '')
                    data_file = find_data_file(data_dir, level)
                    if not data_file:
                        print(f"  ⚠️ Data file for level '{level}' not found in {data_dir}.")
                        entries[idx]['status'] = 'accepted'
                        accepted += 1
                        print("  ✅ Marked as accepted (data file not found, no sync).")
                    else:
                        success, old_val = apply_suggestion(
                            data_file, entry.get('topic', ''),
                            entry.get('word', ''), entry.get('field', ''),
                            suggestion
                        )
                        if success:
                            entries[idx]['status'] = 'accepted'
                            entries[idx]['applied'] = True
                            accepted += 1
                            print(f"  ✅ Applied: '{old_val}' → '{suggestion}' in {os.path.basename(data_file)}")
                        else:
                            print(f"  ⚠️ Could not find word/field in data file.")
                            confirm = input("  Accept anyway? [y/n] > ").strip().lower()
                            if confirm == 'y':
                                entries[idx]['status'] = 'accepted'
                                accepted += 1
                            else:
                                continue
                break

            elif choice in ('r', 'reject'):
                entries[idx]['status'] = 'rejected'
                rejected += 1
                print("  ❌ Rejected.")
                break

            elif choice in ('s', 'skip'):
                skipped += 1
                print("  ⏭️ Skipped.")
                break

            elif choice in ('q', 'quit'):
                print("\n⏹️ Review stopped early.")
                data['feedback'] = entries
                save_json(feedback_file, data)
                print(f"\n📊 Summary: {accepted} accepted, {rejected} rejected, {skipped} skipped")
                print(f"   Results saved to {feedback_file}")
                return

            else:
                print("  Please enter 'a', 'r', 's', or 'q'.")

    # Save results
    data['feedback'] = entries
    save_json(feedback_file, data)
    print(f"\n{'='*60}")
    print(f"📊 Review complete!")
    print(f"   Accepted: {accepted}")
    print(f"   Rejected: {rejected}")
    print(f"   Skipped:  {skipped}")
    print(f"   Results saved to {feedback_file}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description='Review and accept/reject vocabulary feedback.')
    parser.add_argument('--feedback', default='feedback_merged.json',
                        help='Feedback file to review (default: feedback_merged.json)')
    parser.add_argument('--data-dir', default='data',
                        help='Directory with original level JSON files (default: data)')
    args = parser.parse_args()

    print("📝 Vocabulary Feedback Review Tool")
    print("─" * 40)
    review_feedback(args.feedback, args.data_dir)


if __name__ == '__main__':
    main()
