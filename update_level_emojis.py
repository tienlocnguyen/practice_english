#!/usr/bin/env python3
"""
English Practice - Smart Emoji/Image Mapper
Updates the "image" field for English words in the generated dictionary levels (Level 10-19)
to use accurate, context-aware, and interesting emojis rather than simple first-letter indicators.
"""

import os
import re
import json
import sys

# Define target paths
DATA_DIR = "data"

# Comprehensive keyword-based emoji map
# Both English words (lowercased) and Vietnamese translation keywords are checked.
KEYWORD_MAPPINGS = [
    # 📱 Technology & Computing
    (r'\b(byte|data|database|software|hardware|code|coding|encode|encoding|decode|algorithm|program|programming|script|system|network|server|user|website|web|internet|online|cyber|screen|monitor|keyboard|mouse|computer|digital|virtual|tech|innovation|innovative|toner|printer|tablet|dos|plc|oem|connector|link|byte|băng thông|mạng|phần mềm|phần cứng|thuật toán|cơ sở dữ liệu|lập trình|trang web|máy tính|kỹ thuật số)\b', '💻'),
    (r'\b(automation|robot|robotic|ai|artificial|automata|synthetic|tự động|nhân tạo|người máy)\b', '🤖'),
    (r'\b(battery|charge|electric|electricity|electronic|circuit|plug|wire|kích hoạt|activation|power|năng lượng|điện|mạch điện)\b', '🔌'),
    
    # 🏥 Medical & Health & Safety
    (r'\b(flu|fever|cough|sneeze|cold|vomit|symptom|illness|disease|infection|viral|virus|bacteria|sick|pain|headache|stomach|wound|injury|trauma|suffering|hurt|cúm|bệnh|đau|sốt|ho|viêm|nhiễm trùng|vết thương)\b', '🤒'),
    (r'\b(prescription|drug|pill|capsule|medicine|medical|clinic|hospital|doctor|nurse|surgeon|therapist|physiotherapist|examination|physical|wellness|safety|hazard|emergency|evacuation|treatment|thuốc|đơn thuốc|phòng khám|bệnh viện|bác sĩ|trị liệu|an toàn|sơ tán|khẩn cấp)\b', '🏥'),
    (r'\b(healthy|health|hygiene|clean|cleanliness|soap|wash|vệ sinh|sạch sẽ|sức khỏe)\b', '🧼'),
    
    # 🌌 Space & Physics
    (r'\b(astro|astronomy|astronomer|space|cosmic|cosmos|universe|galaxy|nebula|star|planet|asteroid|orbit|satellite|rocket|alien|gravity|friction|velocity|reentry|vacuum|thiên văn|vũ trụ|thiên hà|ngôi sao|hành tinh|vệ tinh|tên lửa|người ngoài hành tinh|trọng lực|chân không)\b', '🌌'),
    (r'\b(thermal|heat|temperature|physics|radiation|fusion|kinetic|quantum|atomic|nuclear|reaction|nhiệt|vật lý|bức xạ|phóng xạ|hạt nhân)\b', '⚛️'),
    
    # 🎨 Arts & Crafts
    (r'\b(art|artist|artwork|painting|canvas|paint|draw|drawing|drew|sculpture|statue|museum|exhibition|gallery|portrait|aesthetic|masterpiece|nghệ thuật|họa sĩ|bức tranh|vẽ|điêu khắc|tượng|triển lãm|chân dung|kiệt tác)\b', '🎨'),
    (r'\b(music|song|sing|singer|tune|rap|melody|rhythm|concert|instrument|violin|guitar|piano|band|album|theatre|theater|movie|film|documentary|drama|genre|avant-garde|protagonist|âm nhạc|bài hát|ca sĩ|giai điệu|nhạc cụ|kịch|phim|thể loại|nhân vật chính)\b', '🎵'),
    (r'\b(design|sketch|creative|fashion|costume|cosmetic|charm|beautiful|trang phục|mỹ phẩm|thiết kế|sáng tạo|đẹp)\b', '✨'),
    
    # 📚 Reading, Education, Academics
    (r'\b(book|read|literature|prose|poem|poetry|novel|writer|author|authoritative|thesis|dictionary|syllabus|curriculum|major|assignment|lecture|academic|study|scholarship|registrar|sách|đọc|văn học|văn xuôi|thơ|tiểu thuyết|luận văn|giáo trình|đề cương|môn học|bài tập|bài giảng|học bổng|phòng đào tạo)\b', '📚'),
    
    # 🌳 Nature, Plants & Agriculture
    (r'\b(tree|forest|wood|jungle|plant|flower|floral|garden|gardening|grass|lawn|seed|stem|leaf|growing|grew|crop|organic|nature|natural|cây|rừng|thực vật|hoa|vườn|cỏ|bãi cỏ|hạt giống|thân cây|lá|phát triển|tự nhiên)\b', '🌳'),
    (r'\b(farmer|farm|agriculture|agricultural|harvest|harvesting|cultivate|cultivation|ranch|cattle|meadow|cottage|greenhouse|nông dân|nông nghiệp|thu hoạch|trang trại|đồng cỏ|nhà kính)\b', '👩‍🌾'),
    (r'\b(corn|grain|wheat|rice|maize|soy|barley|ngô|bắp|lúa|gạo|ngũ cốc)\b', '🌽'),
    (r'\b(glacier|ice|snow|winter|frost|cold|precipitation|drought|erosion|seismic|geology|earth|tectonic|terrain|topography|peninsula|continent|island|bay|sea|ocean|marine|shore|coast|lake|river|water|basin|sông băng|băng|tuyết|mùa đông|mưa|hạn hán|xói mòn|địa chất|trái đất|kiến tạo|địa hình|bán đảo|lục địa|đảo|vịnh|biển|đại dương|bờ biển|sông|hồ|lưu vực)\b', '🌍'),
    (r'\b(mineral|gem|stone|rock|diamond|gold|silver|ore|coal|fuel|oil|gas|magma|lava|volcano|eruption|khoáng sản|đá|kim cương|vàng|bạc|quặng|than|dầu|khí|núi lửa|phun trào)\b', '🌋'),
    
    # 🐾 Animals & Biology
    (r'\b(animal|predator|prey|mammal|species|organism|ecosystem|ecology|habitat|extinction|conservation|biodivers|diversity|evolution|fossil|mutation|gene|hybrid|offspring|động vật|thú|săn mồi|con mồi|loài|sinh vật|hệ sinh thái|môi trường sống|tuyệt chủng|di truyền|đột biến|lai|con non|thế hệ sau)\b', '🐾'),
    (r'\b(bird|wings|fly|feather|hawk|eagle|parrot|chim|cánh|bay|lông vũ|diều hâu|đại bàng|vẹt)\b', '🐦'),
    (r'\b(fish|fishing|fisher|seaweed|shark|whale|crab|shell|cod|marine|cá|đánh cá|ngư dân|tảo biển|cá mập|cá voi|cua|vỏ|cá tuyết)\b', '🐟'),
    (r'\b(insect|bug|bee|ant|spider|mosquito|côn trùng|ong|kiến|nhện|muỗi)\b', '🐜'),
    (r'\b(mouse|rat|squirrel|rodent|rabbit|bunny|chuột|sóc|gặm nhấm|thỏ)\b', '🐭'),
    (r'\b(lion|tiger|bear|wolf|fox|dog|cat|feline|canine|monkey|gorilla|ape|chimp|sheep|goat|cow|pig|horse|camel|sư tử|hổ|gấu|sói|cáo|chó|mèo|khỉ|gấu trúc|cừu|dê|bò|heo|ngựa|lạc đà)\b', '🦁'),
    (r'\b(reptile|snake|lizard|turtle|frog|toad|bò sát|rắn|thằn lằn|rùa|ếch|nhái)\b', '🦎'),
    
    # 🥣 Food & Kitchen & Dining
    (r'\b(food|dining|meal|banquet|buffet|feast|gourmet|recipe|catering|cook|cooking|chef|restaurant|menu|waiter|waitress|cafe|beverage|drink|wine|soup|croissant|baker|pastry|thức ăn|bữa ăn|tiệc|món ăn|công thức|nấu ăn|đầu bếp|nhà hàng|thực đơn|đồ uống|rượu|súp|bánh)\b', '🥣'),
    
    # 👕 Clothes & Apparel
    (r'\b(clothes|clothing|wear|apparel|garment|suit|shirt|tshirt|dress|underwear|pantyhose|socks|pants|jeans|coat|jacket|hat|cap|shoe|shoes|boot|nylon|fabric|silk|wool|cotton|quần áo|mặc|áo|váy|đồ lót|tất|vớ|quần|áo khoác|mũ|nón|giày|sợi nylon|vải)\b', '👕'),
    
    # 💵 Financial, Economics, Business, Corporate, Legal
    (r'\b(money|cash|currency|dollar|euro|coin|finance|financial|banking|bank|wallet|account|accounting|accountant|ledger|bookkeeping|audit|auditor|tax|taxation|fee|cost|budget|pension|retirement|payroll|salary|pay|payment|interest|capital|transaction|invoice|billing|portfolio|investment|invest|stock|share|broker|revenue|profit|loss|liability|debt|credit|asset|deposit|reconcile|bankrupt|bankruptcy|referee|tiền|đồng tiền|tài chính|ngân hàng|ví|tài khoản|kế toán|bảng cân đối|sổ cái|kiểm toán|thuế|chi phí|ngân sách|lương hưu|bảng lương|lương|thanh toán|lãi suất|vốn|giao dịch|hóa đơn|danh mục đầu tư|đầu tư|cổ phiếu|cổ phần|doanh thu|lợi nhuận|khoản nợ|nợ|tín dụng|tài sản|tiền gửi|đối chiếu|phá sản)\b', '💵'),
    (r'\b(trade|market|marketing|selling|sale|purchase|buy|buyer|client|customer|consumer|advertisement|advertising|brochure|campaign|logo|wholesale|demographic|target|strategy|sales|retail|store|retailer|promot|promotion|wholesale|pricing|discount|coupon|satisfaction|thương mại|thị trường|tiếp thị|bán|mua|khách hàng|người tiêu dùng|quảng cáo|chiến dịch|nhãn hiệu|bán sỉ|bán buôn|đối tượng|mục tiêu|chiến lược|khuyến mãi|giảm giá|phiếu mua hàng|sự hài lòng)\b', '💸'),
    (r'\b(company|corporate|firm|enterprise|business|office|workplace|workstation|memo|agenda|collaborate|meeting|teleconference|bulletin|recipient|dispatch|document|priority|contract|manager|director|executive|management|hr|human resources|recruiting|hired|interview|qualif|resume|candidate|vacancy|probation|recruit|supervisor|resignation|application|reference|công ty|doanh nghiệp|văn phòng|nơi làm việc|máy trạm|thông báo|chương trình|hợp tác|cuộc họp|bản tin|người nhận|gửi đi|tài liệu|ưu tiên|hợp đồng|quản lý|giám đốc|nhân sự|tuyển dụng|phỏng vấn|ứng viên|vị trí trống|thử việc|giám sát|từ chức|đơn xin việc|tham chiếu)\b', '🏢'),
    (r'\b(law|legal|court|judge|jury|justice|lawyer|trial|suit|suing|sue|litigation|guilty|crime|criminal|prison|jail|police|theft|robbery|murder|killer|terrorist|terrorism|violence|violent|struggle|ethical|ethics|luật|pháp lý|tòa án|thẩm phán|bồi thẩm đoàn|luật sư|phiên tòa|vụ kiện|kiện|tranh chấp|có tội|tội phạm|tù|nhà tù|cảnh sát|kẻ giết người|khủng bố|bạo lực|đạo đức)\b', '⚖️'),
    
    # ✈️ Travel & Hotel Hospitality
    (r'\b(travel|tourism|tourist|vacation|holiday|trip|journey|route|map|itinerary|boarding|flight|plane|airplane|airport|passenger|terminal|departure|arrival|ticket|destination|resort|hotel|hospitality|concierge|excursion|accommodation|room|reservation|du lịch|nghỉ mát|kỳ nghỉ|chuyến đi|lịch trình|vé máy bay|máy bay|sân bay|hành khách|nhà ga|khởi hành|điểm đến|khách sạn|hiếu khách|quầy phục vụ|dã ngoại|chỗ ở|đặt chỗ)\b', '✈️'),
    
    # 🚚 Logistics, Cargo & Physical Storage
    (r'\b(logistic|logistics|cargo|carrier|shipment|shuttle|courier|transport|delivery|warehouse|freight|dispatch|tracking|receipt|fragile|box|crate|package|bag|luggage|suitcase|truck|train|bus|car|vehicle|hậu cần|hàng hóa|vận tải|lô hàng|chuyển phát|giao hàng|nhà kho|theo dõi|biên lai|dễ vỡ|thùng|hộp|gói hàng|hành lý|vali|xe tải|tàu hỏa|xe buýt|xe hơi|phương tiện)\b', '🚚'),
    
    # 👥 Social & Society
    (r'\b(people|person|student|teenager|child|kid|baby|parent|mother|father|family|friend|peer|society|social|consensus|collective|cooperation|association|union|guild|người|sinh viên|học sinh|thanh thiếu niên|trẻ em|gia đình|bạn bè|xã hội|đồng thuận|tập thể|hợp tác|hiệp hội)\b', '👥'),
    
    # 🏛️ Leaders, Religion & History
    (r'\b(president|pope|king|queen|emperor|royal|prince|princess|nobility|leader|chief|bishop|monastery|priest|church|chapel|temple|sacred|divine|ancient|civilization|historical|history|era|medieval|archaeology|artifact|ancestors|heritage|legacy|fossil|tổng thống|vua|nữ hoàng|hoàng gia|lãnh đạo|giám mục|tu viện|linh mục|nhà thờ|đền|cổ đại|văn minh|lịch sử|thời đại|trung cổ|khảo cổ|cổ vật|tổ tiên|di sản|hóa thạch)\b', '🏛️'),
    
    # ⚡ General Actions / Verbs fallback
    (r'\b(run|running|jump|jumping|climb|climbing|kick|kicking|speed|fast|quick|accelerate|go|going|move|moving|push|pushing|pull|pulling|hold|holding|strike|striking|hit|hitting|swim|swimming|chạy|nhảy|leo|đá|tốc độ|nhanh|di chuyển|đẩy|kéo|giữ|đánh|bơi)\b', '⚡'),
    
    # 🏆 Sports & Achievements
    (r'\b(sport|sports|game|games|play|player|win|winning|won|lose|losing|lost|champion|trophy|medal|match|score|goal|football|soccer|tennis|golf|athlete|attain|attainment|perfect|perfectly|thể thao|trò chơi|chơi|thắng|thua|nhà vô địch|cúp|huy chương|trận đấu|điểm số|bàn thắng|bóng đá|vận động viên|đạt được|hoàn hảo)\b', '🏆')
]

# Standard neutral custom falling-back cycle
FALLBACK_CYCLE = ['💡', '🧩', '✨', '📌', '🔍', '✏️', '🌟', '🛡️', '🏷️', '📦']

def clean_word(word):
    """Retains alphabetic characters for lookup keys."""
    return re.sub(r'[^a-zA-Z\s]', '', word).strip().lower()

def match_emoji(word, meaning, hint, word_idx):
    """Finds the most specific emoji mapping using regular expressions on word, meaning and hints."""
    word_cleaned = clean_word(word)
    text_to_test = f"{word_cleaned} | {meaning.lower()} | {hint.lower()}"
    
    # 1. Search through our regular expression rules
    for regex_pattern, emoji in KEYWORD_MAPPINGS:
        if re.search(regex_pattern, text_to_test):
            return emoji
            
    # 2. Dynamic falling-back based on index to provide nice diverse icons instead of plain single placeholder
    return FALLBACK_CYCLE[word_idx % len(FALLBACK_CYCLE)]

def process_file(filepath):
    """Processes a single level JSON file, updates word emojis, and writes it back."""
    if not os.path.exists(filepath):
        print(f"⚠️ File check failed: {filepath} not found.")
        return False
        
    print(f"📖 Reading {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to parse JSON from {filepath}: {e}")
        return False
        
    updated_count = 0
    words_processed = 0
    
    for t_idx, topic in enumerate(data.get('topics', [])):
        for w_idx, word_entry in enumerate(topic.get('words', [])):
            word = word_entry.get('word', '')
            meaning = word_entry.get('meaning', '')
            hint = word_entry.get('hint', '')
            current_image = word_entry.get('image', '')
            
            # Match the best context-aware emoji
            new_emoji = match_emoji(word, meaning, hint, words_processed)
            words_processed += 1
            
            # Since generating lists we changed image, let's update if it differs or is basic first-letter placeholder
            if current_image != new_emoji:
                word_entry['image'] = new_emoji
                updated_count += 1
                
    print(f"⚡ Done mapping. Updated {updated_count}/{words_processed} words with smart emojis.")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f"💾 Saved {filepath} successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to write back to {filepath}: {e}")
        return False

def main():
    print("🌟 --- SMART EMOJI MAPPER FOR DICTIONARY LEVELS --- 🌟")
    
    # Determine target files
    targets = []
    
    if len(sys.argv) > 1:
        # User supplied explicit files
        for arg in sys.argv[1:]:
            targets.append(arg)
    else:
        # Default auto check level14.json & other dictionary level files 10 to 19
        for lvl_id in range(10, 20):
            path = os.path.join(DATA_DIR, f"level{lvl_id}.json")
            if os.path.exists(path):
                targets.append(path)
                
    if not targets:
        print("❌ No matching files found inside 'data/' folder. Please provide paths explicitly.")
        sys.exit(1)
        
    print(f"📋 Queued files for processing: {targets}")
    
    success = True
    for t_path in targets:
        if not process_file(t_path):
            success = False
            
    if success:
        print("\n🎉 --- ALL QUEUED LEVELS SUCCESSFULLY RE-IMAGE MAPPED --- 🎉")
    else:
        print("\n⚠️ --- INCOMPLETE RETRIEVAL IN SOME LEVEL FILES --- ⚠️")

if __name__ == '__main__':
    main()
