#!/usr/bin/env python3
"""
English Practice - Massive Vocabulary Generator (10,000 Essential Words)
Downloads Google 10,000 common words list and Ho Ngoc Duc's English-Vietnamese Dictionary,
parses and blends them, then outputs CEFR-based level JSON files and registers them in config.json.
"""

import os
import re
import json
import random
import sys
import requests

# Standard files and paths
CONFIG_PATH = "config.json"
DATA_DIR = "data"

# Google 10,000 common words list & Ho Ngoc Duc's PVDP English-Vietnamese dictionary
GOOGLE_WORDS_URL = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt"
HO_NGOC_DUC_DICT_URL = "https://raw.githubusercontent.com/robert-strandh/VietAnh/master/anhviet.dict"

# Emojis associated with first letters or common themes
ALPHABET_EMOJIS = {
    'a': '🍎', 'b': '⚽', 'c': '🐱', 'd': '🐶', 'e': '🐘', 'f': '🦊', 'g': '🍇', 'h': '🏠',
    'i': '🍦', 'j': '🧥', 'k': '🔑', 'l': '🦁', 'm': '🐵', 'n': '🎯', 'o': '🍊', 'p': '🥑',
    'q': '👑', 'r': '🚀', 's': '⭐️', 't': '🌳', 'u': '☔️', 'v': '🎻', 'w': '🍉', 'x': '👾',
    'y': '💛', 'z': '🦓'
}

COMMON_EMOJIS = {
    'danh từ': '📦', 'động từ': '⚡️', 'tính từ': '✨', 'phó từ': '🌀', 'giới từ': '📍',
    'animals': '🐾', 'food': '🍔', 'clothing': '👕', 'colors': '🎨', 'numbers': '🔢'
}

def download_data():
    """Download Google 10k words list and Ho Ngoc Duc dictionary."""
    print("📥 Downloading Google 10,000 common words list...")
    try:
        r_words = requests.get(GOOGLE_WORDS_URL, timeout=30)
        r_words.raise_for_status()
        google_words = [w.strip().lower() for w in r_words.text.splitlines() if w.strip()]
        print(f"✅ Downloaded {len(google_words)} common words.")
    except Exception as e:
        print(f"❌ Failed to download Google wordlist: {e}")
        sys.exit(1)

    print("📥 Downloading Ho Ngoc Duc's English-Vietnamese Dictionary...")
    try:
        r_dict = requests.get(HO_NGOC_DUC_DICT_URL, stream=True, headers={'Accept-Encoding': 'identity'}, timeout=60)
        r_dict.raise_for_status()
        dict_content = r_dict.content.decode('utf-8', errors='ignore')
        print(f"✅ Downloaded dictionary raw content ({len(dict_content)} characters).")
    except Exception as e:
        print(f"❌ Failed to download Ho Ngoc Duc dictionary: {e}")
        sys.exit(1)

    return google_words, dict_content

def parse_ho_ngoc_duc_dictionary(dict_content):
    """Parse the dictionary file into an entry mapping."""
    print("⚙️ Parsing dictionary entries...")
    raw_entries = re.split(r'\n(?=@)', dict_content)
    print(f"   Precheck: Splitted {len(raw_entries)} potential records.")
    
    parsed_dict = {}
    
    for idx, raw_entry in enumerate(raw_entries):
        lines = [l.strip() for l in raw_entry.split('\n') if l.strip()]
        if not lines:
            continue
            
        line1 = lines[0]
        if not line1.startswith('@'):
            continue
            
        header = line1[1:] # Strip @
        phonetic = ""
        word = header
        
        # Extract phonetics enclosed in /.../
        match_phonetic = re.search(r'/(.*?)/', header)
        if match_phonetic:
            phonetic = '/' + match_phonetic.group(1) + '/'
            word = header[:match_phonetic.start()].strip()
        else:
            # Fallback split
            parts = header.split(' ', 1)
            if len(parts) > 1:
                word = parts[0]
                phonetic = parts[1]
                
        word_clean = word.strip().lower().replace('_', ' ')
        
        meanings = []
        part_of_speech = ""
        examples = []
        
        for line in lines[1:]:
            if line.startswith('*'):
                pos = line[1:].strip()
                if pos:
                    part_of_speech = pos
                    meanings.append(f"({pos})")
            elif line.startswith('-'):
                mean = line[1:].strip()
                if mean:
                    meanings.append(mean)
            elif line.startswith('='):
                ex_part = line[1:].strip()
                if '+' in ex_part:
                    ex, tr = ex_part.split('+', 1)
                    examples.append((ex.strip().replace('_', ' '), tr.strip()))
                else:
                    examples.append((ex_part.replace('_', ' '), ''))
                    
        meaning_str = "; ".join(meanings) if meanings else ""
        
        parsed_dict[word_clean] = {
            'word': word_clean,
            'original_word': word.strip(),
            'phonetic': phonetic.strip(),
            'meaning': meaning_str.strip(),
            'part_of_speech': part_of_speech,
            'examples': examples
        }
        
    print(f"✅ Successfully compiled {len(parsed_dict)} key dictionary entries.")
    return parsed_dict

def generate_sentence_fallback(word, part_of_speech, meaning_vi):
    """Generate high-quality example sentences and translations based on grammar category."""
    word_cap = word.capitalize()
    
    templates_noun = [
        ("I can see the [word] from here.", "Tôi có thể nhìn thấy [meaning] từ đây."),
        ("This is a beautiful [word].", "Đây là một [meaning] tuyệt đẹp."),
        ("The [word] is very important to us.", "[Meaning] rất quan trọng đối với chúng tôi."),
        ("He bought a new [word] yesterday.", "Anh ấy đã mua một [meaning] mới hôm qua.")
    ]
    
    templates_verb = [
        ("We need to [word] this as soon as possible.", "Chúng tôi cần [meaning] điều này càng sớm càng tốt."),
        ("She wants to [word] English with everyone.", "Cô ấy muốn học cách [meaning] tiếng Anh với mọi người."),
        ("They didn't [word] anything about it.", "Họ đã không [meaning] bất cứ điều gì về nó."),
        ("Can you [word] with me?", "Bạn có thể [meaning] cùng tôi không?")
    ]

    templates_adj = [
        ("The weather today is very [word].", "Thời tiết hôm nay rất [meaning]."),
        ("She is a [word] person.", "Cô ấy là một người [meaning]."),
        ("This textbook makes learning [word] and interesting.", "Cuốn sách giáo khoa này làm cho việc học trở nên [meaning] và thú vị."),
        ("Our new house is very [word].", "Ngôi nhà mới của chúng tôi rất [meaning].")
    ]
    
    templates_fallback = [
        ("We will look up the word '[word]' today.", "Chúng ta sẽ tra cứu từ '[meaning]' ngày hôm nay."),
        ("This lesson covers '[word]'.", "Bài học này nói về '[meaning]'."),
        ("Can you explain the meaning of '[word]'?", "Bạn có thể giải thích ý nghĩa của '[meaning]' không?")
    ]
    
    # Process translation meaning (just first few words of vietnamese meaning)
    clean_meaning = meaning_vi.split(';')[0]
    clean_meaning = re.sub(r'\(.*?\)', '', clean_meaning).strip()
    if not clean_meaning:
        clean_meaning = "từ này"
        
    # Standardize articles or small categories
    if len(clean_meaning) > 25:
        clean_meaning = clean_meaning[:25] + "..."
        
    if "danh từ" in part_of_speech or "danh" in part_of_speech:
        tpl, tpl_vi = random.choice(templates_noun)
    elif "động từ" in part_of_speech or "động" in part_of_speech:
        tpl, tpl_vi = random.choice(templates_verb)
    elif "tính từ" in part_of_speech or "tính" in part_of_speech:
        tpl, tpl_vi = random.choice(templates_adj)
    else:
        tpl, tpl_vi = random.choice(templates_fallback)
        
    example = tpl.replace("[word]", word)
    example_vi = tpl_vi.replace("[meaning]", clean_meaning)
    
    return example, example_vi

def build_levels(google_words, parsed_dict):
    """Match words against dictionary and organize them into CEFR levels and topics."""
    print("🧙 Blending wordlists and building educational levels...")
    
    matched_words = []
    
    for word in google_words:
        # Filter down long/niche abbreviation/typo words
        if len(word) < 2 or not word.isalpha():
            continue
            
        dict_entry = parsed_dict.get(word)
        if not dict_entry or not dict_entry['meaning']:
            continue
            
        meaning = dict_entry['meaning']
        part_of_speech = dict_entry['part_of_speech']
        phonetic = dict_entry['phonetic'] or f"/{word}/"
        
        # Use existing example or generate fallback
        examples = dict_entry['examples']
        if examples:
            example, example_vi = examples[0]
            # If translation is missing
            if not example_vi:
                _, example_vi = generate_sentence_fallback(word, part_of_speech, meaning)
        else:
            example, example_vi = generate_sentence_fallback(word, part_of_speech, meaning)
            
        # Clean example_vi if it's too bracketed
        example_vi = example_vi.replace('+', '').strip()
        
        # Calculate matching emoji
        first_char = word[0].lower()
        emoji = ALPHABET_EMOJIS.get(first_char, '📝')
        for k, v in COMMON_EMOJIS.items():
            if k in part_of_speech or k in word:
                emoji = v
                break
                
        # Generate simple hint
        hint = f"Bắt đầu bằng chữ '{word[0].upper()}', nghĩa là: {meaning.split(';')[0]}"
        if len(hint) > 80:
            hint = hint[:77] + "..."
        matched_words.append({
            'word': word,
            'meaning': meaning,
            'phonetic': phonetic,
            'image': emoji,
            'audio': '',
            'example': example,
            'example_vi': example_vi,
            'hint': hint
        })
        
    print(f"📊 Google word matching got {len(matched_words)} high-quality validated words.")

    target_total_words = 10200
    current_count = len(matched_words)
    
    if current_count < target_total_words:
        needed = target_total_words - current_count
        print(f"➕ Filling the remaining {needed} words from the parsed dictionary...")
        
        # Collect matched words set for fast lookup
        already_matched = {w['word'] for w in matched_words}
        
        # Filter for clean entries
        dict_words_candidates = []
        for word_clean, entry in parsed_dict.items():
            if word_clean in already_matched:
                continue
            # Simple english alphabet words only (length 3 to 12)
            if not word_clean.isalpha() or len(word_clean) < 3 or len(word_clean) > 12:
                continue
            # Must have a valid meaning
            if not entry['meaning'] or len(entry['meaning']) < 3:
                continue
            dict_words_candidates.append(entry)
            
        print(f"   Collected {len(dict_words_candidates)} clean dictionary supplement candidates.")
        
        # Sort candidates alphabetically
        dict_words_candidates.sort(key=lambda x: x['word'])
        
        for entry in dict_words_candidates[:needed]:
            word = entry['word']
            meaning = entry['meaning']
            part_of_speech = entry['part_of_speech']
            phonetic = entry['phonetic'] or f"/{word}/"
            
            # Use existing example or generate fallback
            examples = entry['examples']
            if examples:
                example, example_vi = examples[0]
                if not example_vi:
                    _, example_vi = generate_sentence_fallback(word, part_of_speech, meaning)
            else:
                example, example_vi = generate_sentence_fallback(word, part_of_speech, meaning)
                
            example_vi = example_vi.replace('+', '').strip()
            
            # Calculate matching emoji
            first_char = word[0].lower() if word else 'a'
            emoji = ALPHABET_EMOJIS.get(first_char, '📝')
            for k, v in COMMON_EMOJIS.items():
                if k in part_of_speech or k in word:
                    emoji = v
                    break
                    
            # Generate simple hint
            hint = f"Bắt đầu bằng chữ '{word[0].upper()}', nghĩa là: {meaning.split(';')[0]}"
            if len(hint) > 80:
                hint = hint[:77] + "..."
                
            matched_words.append({
                'word': word,
                'meaning': meaning,
                'phonetic': phonetic,
                'image': emoji,
                'audio': '',
                'example': example,
                'example_vi': example_vi,
                'hint': hint
            })
            
    print(f"📊 Total massive dictionary blended list has {len(matched_words)} validated words.")
    
    # We will build 10 massive vocab levels
    # Each level will have 34 topics
    # Each topic will have 30 words
    # Total capacity = 10 * 34 * 30 = 10200 words!
    
    words_per_topic = 30
    topics_per_level = 34
    words_per_level = words_per_topic * topics_per_level # 1020 words
    
    levels_data = []
    
    level_names = [
        ("Dictionary Vol 1", "Từ vựng thông dụng tập 1", "Các từ vựng tiếng Anh cơ bản nhất — phần 1"),
        ("Dictionary Vol 2", "Từ vựng thông dụng tập 2", "Các từ vựng tiếng Anh cơ bản nhất — phần 2"),
        ("Dictionary Vol 3", "Từ vựng thông dụng tập 3", "Các từ vựng tiếng Anh trung cấp — phần 1"),
        ("Dictionary Vol 4", "Từ vựng thông dụng tập 4", "Các từ vựng tiếng Anh trung cấp — phần 2"),
        ("Dictionary Vol 5", "Từ vựng thông dụng tập 5", "Các từ vựng tiếng Anh trung cấp — phần 3"),
        ("Dictionary Vol 6", "Từ vựng thông dụng tập 6", "Các từ vựng nâng cao chuyên sâu — phần 1"),
        ("Dictionary Vol 7", "Từ vựng thông dụng tập 7", "Các từ vựng nâng cao chuyên sâu — phần 2"),
        ("Dictionary Vol 8", "Từ vựng học thuật tập 8", "Từ vựng Academic & SAT — phần 1"),
        ("Dictionary Vol 9", "Từ vựng học thuật tập 9", "Từ vựng Academic & SAT — phần 2"),
        ("Dictionary Vol 10", "Từ vựng thông dụng tập 10", "Từ vựng nâng cao bậc cao")
    ]
    
    for lvl_idx, (label, label_vi, desc) in enumerate(level_names):
        lvl_num = lvl_idx + 10 # Starting level index at 10 to avoid conflicting with existing levels
        start_word_idx = lvl_idx * words_per_level
        end_word_idx = start_word_idx + words_per_level
        
        level_words = matched_words[start_word_idx:end_word_idx]
        if not level_words:
            break
            
        topics = []
        for top_idx in range(topics_per_level):
            sub_start = top_idx * words_per_topic
            sub_end = sub_start + words_per_topic
            topic_words = level_words[sub_start:sub_end]
            if not topic_words:
                break
                
            topic_id = f"dict_{lvl_num}_{top_idx + 1}"
            topic_name = f"Lesson {top_idx + 1}"
            topic_name_vi = f"Bài học {top_idx + 1}"
            
            # Alternate standard icons for lessons
            lesson_icons = ['📚', '🧠', '🚀', '🎯', '🌟', '🧩', '📖', '💡', '📝', '⚡️', '🔍', '🔬']
            topic_icon = lesson_icons[top_idx % len(lesson_icons)]
            
            topics.append({
                'id': topic_id,
                'name': topic_name,
                'name_vi': topic_name_vi,
                'icon': topic_icon,
                'words': topic_words
            })
            
        levels_data.append({
            'level': str(lvl_num),
            'label': label,
            'label_vi': label_vi,
            'description': desc,
            'topics': topics
        })
        
    return levels_data

def save_levels_and_update_config(levels_data):
    """Save parsed level JSON files and update config.json with newly registered files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    generated_files = []
    
    for level_data in levels_data:
        lvl = level_data['level']
        filename = f"level{lvl}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(level_data, f, ensure_ascii=False, indent=2)
            f.write('\n')
            
        generated_files.append(filepath)
        print(f"💾 Written {filepath} with {len(level_data['topics'])} lessons ({sum(len(t['words']) for t in level_data['topics'])} words).")
        
    # Read existing config.json
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load existing config.json: {e}")
        return

    # Add both existing ones, precompiled ones (A, B, C, TOEFL) and newly generated massive dictionary files
    all_known_levels = [
        "data/level1.json",
        "data/level3.json",
        "data/level5.json",
        "data/levelA.json",
        "data/levelB.json",
        "data/levelC.json",
        "data/leveltoefl.json"
    ]
    
    for path in generated_files:
        path_slash = path.replace("\\", "/")
        if path_slash not in all_known_levels:
            all_known_levels.append(path_slash)
            
    # Update config.json
    config['levels'] = all_known_levels
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write('\n')
        
    print(f"✅ Successfully updated {CONFIG_PATH} with {len(all_known_levels)} levels.")

def main():
    print("🚀 --- MASSIVE DICTIONARY GENERATOR INITIALIZED --- 🚀")
    google_words, dict_content = download_data()
    parsed_dict = parse_ho_ngoc_duc_dictionary(dict_content)
    levels_data = build_levels(google_words, parsed_dict)
    save_levels_and_update_config(levels_data)
    print("🎉 --- GENERATION AND REGISTRATION FULLY COMPLETED --- 🎉")

if __name__ == '__main__':
    main()
