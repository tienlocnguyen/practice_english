#!/usr/bin/env python3
"""
English Practice - Exam Prep Vocabulary Generator (TOEFL & TOEIC)
Generates highly polished prep data for TOEFL & TOEIC split by professional and academic topics.
Includes phonetics from Ho Ngoc Duc's dictionary, customized contextual sentences, translations, and templates.
"""

import os
import re
import json
import requests

CONFIG_PATH = "config.json"
DATA_DIR = "data"

HO_NGOC_DUC_DICT_URL = "https://raw.githubusercontent.com/robert-strandh/VietAnh/master/anhviet.dict"

# Define TOEFL academic word lists with handcrafted context-aware sentences
TOEFL_TOPICS = [
    {
        "id": "toefl_bio",
        "name": "Biological Sciences",
        "name_vi": "Sinh học & Hệ sinh thái",
        "icon": "🐾",
        "words": [
            {
                "word": "evolution",
                "meaning": "sự tiến hóa (danh từ)",
                "image": "🐒",
                "example": "Darwin's theory of evolution explains how species adapt over time.",
                "example_vi": "Thuyết tiến hóa của Darwin giải thích cách các loài thích nghi theo thời gian.",
                "hint": "The gradual development of organisms over generations."
            },
            {
                "word": "species",
                "meaning": "loài sinh vật (danh từ)",
                "image": "🐾",
                "example": "Hundreds of marine species were discovered during the deep-sea expedition.",
                "example_vi": "Hàng trăm loài sinh vật biển đã được phát hiện trong cuộc thám hiểm biển sâu.",
                "hint": "A group of living organisms consisting of similar individuals."
            },
            {
                "word": "adaptation",
                "meaning": "sự thích nghi (danh từ)",
                "image": "🦎",
                "example": "The camel's hump is an adaptation for survival in arid desert climates.",
                "example_vi": "Bướu của lạc đà là một sự thích nghi để sinh tồn trong khí hậu sa mạc khô hạn.",
                "hint": "A change by which an organism becomes better suited to its environment."
            },
            {
                "word": "ecosystem",
                "meaning": "hệ sinh thái (danh từ)",
                "image": "🌳",
                "example": "Deforestation can quickly disrupt the balance of the local forest ecosystem.",
                "example_vi": "Nạn phá rừng có thể nhanh chóng làm gián đoạn sự cân bằng của hệ sinh thái rừng địa phương.",
                "hint": "A biological community of interacting organisms and their physical environment."
            },
            {
                "word": "habitat",
                "meaning": "môi trường sống (danh từ)",
                "image": "🏕️",
                "example": "Polar bears are losing their natural habitat due to melting sea ice.",
                "example_vi": "Gấu Bắc Cực đang mất đi môi trường sống tự nhiên do băng biển tan chảy.",
                "hint": "The natural home or environment of an animal, plant, or other organism."
            },
            {
                "word": "photosynthesis",
                "meaning": "quá trình quang hợp (danh từ)",
                "image": "🌿",
                "example": "Plants absorb sunlight to convert water and carbon dioxide into oxygen during photosynthesis.",
                "example_vi": "Thực vật hấp thụ ánh sáng mặt trời để chuyển đổi nước và carbon dioxide thành oxy trong quá trình quang hợp.",
                "hint": "Process by which green plants use sunlight to synthesize nutrients."
            },
            {
                "word": "organism",
                "meaning": "sinh vật, cá thể sống (danh từ)",
                "image": "🦠",
                "example": "A single-celled organism can perform all necessary life functions.",
                "example_vi": "Một sinh vật đơn bào có thể thực hiện tất cả các chức năng sống cần thiết.",
                "hint": "An individual animal, plant, or single-celled life form."
            },
            {
                "word": "diversity",
                "meaning": "sự đa dạng (danh từ)",
                "image": "🌈",
                "example": "Tropical rainforests are celebrated for their incredible biological diversity.",
                "example_vi": "Rừng mưa nhiệt đới nổi tiếng vì sự đa dạng sinh học đáng kinh ngạc của chúng.",
                "hint": "The state of showing a great deal of variety; very different species."
            },
            {
                "word": "predator",
                "meaning": "kẻ săn mồi (danh từ)",
                "image": "🦁",
                "example": "The lion remains one of the most formidable predators in the African savanna.",
                "example_vi": "Sư tử vẫn là một trong những loài thú săn mồi đáng sợ nhất ở thảo nguyên châu Phi.",
                "hint": "An animal that naturally preys on others."
            },
            {
                "word": "prey",
                "meaning": "con mồi (danh từ / động từ)",
                "image": "🐰",
                "example": "Hawks rely on their sharp eyesight to spot prey from high in the sky.",
                "example_vi": "Diều hâu dựa vào thị lực sắc bén để phát hiện con mồi từ trên trời cao.",
                "hint": "An animal that is hunted and killed by another for food."
            },
            {
                "word": "marine",
                "meaning": "thuộc về biển (tính từ)",
                "image": "🐳",
                "example": "Marine biologists study ocean life to protect coral reefs from warming waters.",
                "example_vi": "Các nhà sinh học biển nghiên cứu sự sống dưới đại dương để bảo vệ các rạn san hô khỏi vùng nước ấm lên.",
                "hint": "Relating to or found in the sea."
            },
            {
                "word": "gene",
                "meaning": "gen di truyền (danh từ)",
                "image": "🧬",
                "example": "Researchers identified the specific gene responsible for the plant's resistance to cold.",
                "example_vi": "Các nhà nghiên cứu đã xác định được loại gen cụ thể giúp cây có khả năng chống chịu lạnh.",
                "hint": "A unit of heredity passed from parent to offspring."
            },
            {
                "word": "mutation",
                "meaning": "sự đột biến (danh từ)",
                "image": "🧪",
                "example": "A genetic mutation caused the flowers to bloom in a bright blue hue.",
                "example_vi": "Một đột biến di truyền đã khiến những bông hoa nở ra sắc xanh lam rực rỡ.",
                "hint": "The changing of the structure of a gene, resulting in a variant form."
            },
            {
                "word": "hybrid",
                "meaning": "lai, giống lai (danh từ / tính từ)",
                "image": "🌾",
                "example": "This hybrid variety of corn grows much faster and resists pests effectively.",
                "example_vi": "Giống ngô lai này phát triển nhanh hơn nhiều và kháng sâu bệnh rất hiệu quả.",
                "hint": "An offspring of two plants or animals of different species or varieties."
            },
            {
                "word": "offspring",
                "meaning": "con cái, thế hệ sau (danh từ)",
                "image": "🐥",
                "example": "Birds spend a great deal of energy feeding and protecting their vulnerable offspring.",
                "example_vi": "Chim dành rất nhiều năng lượng để nuôi dưỡng và bảo vệ con non yếu ớt của chúng.",
                "hint": "A person's child or children / an animal's young."
            }
        ]
    },
    {
        "id": "toefl_hist",
        "name": "Archaeology & History",
        "name_vi": "Khảo cổ học & Lịch sử",
        "icon": "🏛️",
        "words": [
            {
                "word": "artifact",
                "meaning": "cổ vật, di vật (danh từ)",
                "image": "🏺",
                "example": "The museum displays a rare golden artifact from the Aztec civilization.",
                "example_vi": "Bảo tàng trưng bày một cổ vật bằng vàng quý hiếm từ nền văn minh Aztec.",
                "hint": "An object made by a human being, typically of historical or cultural interest."
            },
            {
                "word": "civilization",
                "meaning": "nền văn minh (danh từ)",
                "image": "🏛️",
                "example": "Ancient Roman civilization laid the groundwork for modern legal structures.",
                "example_vi": "Nền văn minh La Mã cổ đại đã đặt nền móng cho các cấu trúc luật pháp hiện đại.",
                "hint": "The stage of human social and cultural development that is considered most advanced."
            },
            {
                "word": "ancestors",
                "meaning": "tổ tiên (danh từ)",
                "image": "👴",
                "example": "Many families track their family tree to learn where their ancestors migrated from.",
                "example_vi": "Nhiều gia đình lần theo gia phả để tìm hiểu xem tổ tiên của họ đã di cư từ đâu đến.",
                "hint": "A person, typically one more remote than a grandparent, from whom one is descended."
            },
            {
                "word": "era",
                "meaning": "kỷ nguyên, thời đại (danh từ)",
                "image": "⏳",
                "example": "The collapse of the Berlin Wall marked the end of a long geopolitical era.",
                "example_vi": "Sự sụp đổ của Bức tường Berlin đã đánh dấu sự kết thúc của một kỷ nguyên địa chính trị lâu dài.",
                "hint": "A long and distinct period of history with a particular feature or characteristic."
            },
            {
                "word": "ancient",
                "meaning": "cổ xưa, cổ đại (tính từ)",
                "image": "🏛️",
                "example": "We stood in absolute awe looking at the ancient stones of Stonehenge.",
                "example_vi": "Chúng tôi đứng kinh ngạc tột độ khi nhìn vào những phiến đá cổ xưa của Stonehenge.",
                "hint": "Belonging to the very distant past and no longer in existence."
            },
            {
                "word": "fossil",
                "meaning": "hóa thạch (danh từ)",
                "image": "🦖",
                "example": "The fossil of a prehistoric fish was uncovered on the dry mountain slope.",
                "example_vi": "Hóa thạch của một loài cá tiền sử đã được phát hiện trên sườn núi khô cằn.",
                "hint": "The remains of a prehistoric organism preserved in petrified form."
            },
            {
                "word": "excavation",
                "meaning": "sự khai quật (danh từ)",
                "image": "⛏️",
                "example": "A delicate archaeological excavation revealed the foundations of a 2000-year-old temple.",
                "example_vi": "Một cuộc khai quật khảo cổ tỉ mỉ đã làm lộ ra nền móng của một ngôi đền 2000 năm tuổi.",
                "hint": "The action of excavating something, especially an archaeological site."
            },
            {
                "word": "primitive",
                "meaning": "nguyên thủy, thô sơ (tính từ)",
                "image": "🪵",
                "example": "They used primitive tools made from stone and bones to build shelter.",
                "example_vi": "Họ đã sử dụng các công cụ thô sơ làm từ đá và xương để xây dựng nơi trú ẩn.",
                "hint": "Relating to the character of an early stage in the evolutionary or historical development."
            },
            {
                "word": "migrate",
                "meaning": "di cư (động từ)",
                "image": "🦅",
                "example": "During winter, thousands of birds migrate south to seek warmer climates.",
                "example_vi": "Vào mùa đông, hàng ngàn con chim di cư về phía nam để tìm kiếm khí hậu ấm áp hơn.",
                "hint": "To move from one region or habitat to another, typically according to the season."
            },
            {
                "word": "nomadic",
                "meaning": "du mục (tính từ)",
                "image": "⛺",
                "example": "The nomadic tribes of Mongolia travel with their herds across the grasslands.",
                "example_vi": "Các bộ lạc du mục ở Mông Cổ di chuyển cùng đàn gia súc của họ qua các đồng cỏ.",
                "hint": "Living the life of a nomad; wandering from place to place."
            },
            {
                "word": "medieval",
                "meaning": "thuộc thời trung cổ (tính từ)",
                "image": "🏰",
                "example": "Scholars specialize in analyzing medieval Latin manuscripts found in monasteries.",
                "example_vi": "Các học giả chuyên phân tích các bản thảo Latinh thời trung cổ được tìm thấy trong các tu viện.",
                "hint": "Relating to the Middle Ages (approx. 5th to 15th century)."
            },
            {
                "word": "chronological",
                "meaning": "theo thứ tự thời gian (tính từ)",
                "image": "📅",
                "example": "The textbook arranges the events of the American Revolution in chronological order.",
                "example_vi": "Sách giáo khoa sắp xếp các sự kiện của Cách mạng Mỹ theo thứ tự thời gian.",
                "hint": "Starting with the earliest and following the order in which they occurred."
            },
            {
                "word": "heritage",
                "meaning": "di sản (danh từ)",
                "image": "🎭",
                "example": "Saving the ancient monument preserves a vital piece of the country's cultural heritage.",
                "example_vi": "Cứu vãn di tích cổ đại giúp bảo tồn một phần thiết yếu trong di sản văn hóa của quốc gia.",
                "hint": "Property or traditions that are valued and passed down from generation to generation."
            },
            {
                "word": "legacy",
                "meaning": "thừa dư, di sản để lại (danh từ)",
                "image": "📜",
                "example": "The Greek philosopher left behind a rich legacy of logical reasoning.",
                "example_vi": "Triết gia người Hy Lạp đã để lại một di sản phong phú về tư duy logic.",
                "hint": "An amount of money or property left to someone in a will / output of history."
            },
            {
                "word": "dynamic",
                "meaning": "động lực, năng động (tính từ / danh từ)",
                "image": "⚡",
                "example": "The historical dynamic between trade policies and immigration is deeply complex.",
                "example_vi": "Động lực lịch sử giữa chính sách thương mại và nhập cư cực kỳ phức tạp.",
                "hint": "Constant change, activity, or progress."
            }
        ]
    },
    {
        "id": "toefl_astro",
        "name": "Astronomy & Physics",
        "name_vi": "Thiên văn & Vật lý học",
        "icon": "🚀",
        "words": [
            {
                "word": "asteroid",
                "meaning": "tiểu hành tinh (danh từ)",
                "image": "☄️",
                "example": "A large asteroid collided with Earth millions of years ago, causing mass extinctions.",
                "example_vi": "Một tiểu hành tinh lớn đã va chạm với Trái đất hàng triệu năm trước, gây ra sự tuyệt chủng hàng loạt.",
                "hint": "A small rocky body orbiting the sun."
            },
            {
                "word": "atmosphere",
                "meaning": "bầu khí quyển (danh từ)",
                "image": "☁️",
                "example": "The dense atmosphere of Venus traps heat, making it the hottest planet.",
                "example_vi": "Bầu khí quyển dày đặc của sao Kim giữ nhiệt, biến nó thành hành tinh nóng nhất.",
                "hint": "The envelope of gases surrounding the earth or another planet."
            },
            {
                "word": "orbit",
                "meaning": "quỹ đạo (danh từ / động từ)",
                "image": "🛰️",
                "example": "Artificial satellites orbit the Earth to transmit telecommunication signals.",
                "example_vi": "Các vệ tinh nhân tạo quay quanh Trái đất để truyền tín hiệu viễn thông.",
                "hint": "The curved path of a celestial object or spacecraft around a star, planet, or moon."
            },
            {
                "word": "cosmic",
                "meaning": "thuộc vũ trụ (tính từ)",
                "image": "🌌",
                "example": "Spacewalking astronauts are exposed to high doses of dangerous cosmic radiation.",
                "example_vi": "Các phi hành gia đi bộ ngoài không gian phải tiếp xúc với liều lượng cao bức xạ vũ trụ nguy hiểm.",
                "hint": "Relating to the universe or cosmos, especially as distinct from earth."
            },
            {
                "word": "gravity",
                "meaning": "trọng lực (danh từ)",
                "image": "🍎",
                "example": "The moon has weaker gravity than Earth, which allows astronauts to leap high.",
                "example_vi": "Mặt trăng có trọng lực yếu hơn Trái đất, cho phép các phi hành gia nhảy rất cao.",
                "hint": "The force that attracts a body toward the center of the earth, or toward any other physical body."
            },
            {
                "word": "galaxy",
                "meaning": "thiên hà (danh từ)",
                "image": "🌀",
                "example": "Our solar system resides inside the spiral Andromeda-neighboring Milky Way galaxy.",
                "example_vi": "Hệ mặt trời của chúng ta nằm bên trong thiên hà xoắn ốc Ngân Hà láng giềng Andromeda.",
                "hint": "A system of millions or billions of stars, together with gas and dust, held together by gravitational attraction."
            },
            {
                "word": "eclipse",
                "meaning": "sự nhật thực / nguyệt thực (danh từ)",
                "image": "🌑",
                "example": "During a total solar eclipse, the moon briefly blocks out the sunlight completely.",
                "example_vi": "Trong suốt thời gian nhật thực toàn phần, mặt trăng tạm thời chặn hoàn toàn ánh sáng mặt trời.",
                "hint": "An obscuring of the light from one celestial body by the passage of another."
            },
            {
                "word": "friction",
                "meaning": "lực ma sát (danh từ)",
                "image": "🛹",
                "example": "The spacecraft generates intense heat because of air friction during atmospheric reentry.",
                "example_vi": "Tàu vũ trụ tạo ra nhiệt lượng cực lớn do ma sát không khí khi quay trở lại bầu khí quyển.",
                "hint": "The resistance that one surface or object encounters when moving over another."
            },
            {
                "word": "velocity",
                "meaning": "vận tốc (danh từ)",
                "image": "🏃",
                "example": "To escape Earth's gravity, a rocket must reach an immense escape velocity.",
                "example_vi": "Để thoát khỏi trọng lực của Trái đất, tên lửa phải đạt được một vận tốc thoát cực lớn.",
                "hint": "The speed of something in a given direction."
            },
            {
                "word": "thermal",
                "meaning": "thuộc về nhiệt (tính từ)",
                "image": "🌡️",
                "example": "Geothermal power plants tap into hot thermal energy stored deep beneath the surface.",
                "example_vi": "Các nhà máy điện địa nhiệt khai thác năng lượng nhiệt nóng lưu trữ sâu dưới lòng đất.",
                "hint": "Relating to heat."
            },
            {
                "word": "radiation",
                "meaning": "bức xạ (danh từ)",
                "image": "☢️",
                "example": "Heavy led shielding is required to protect laboratory technicians from harmful radiation.",
                "example_vi": "Cần có tấm chắn chì dày để bảo vệ các kỹ thuật viên phòng thí nghiệm khỏi bức xạ có hại.",
                "hint": "The emission of energy as electromagnetic waves or as subatomic particles."
            },
            {
                "word": "fusion",
                "meaning": "sự nóng chảy, phản ứng hạt nhân (danh từ)",
                "image": "💥",
                "example": "Nuclear fusion in the sun's core fuses hydrogen atoms to generate daylight energy.",
                "example_vi": "Phản ứng hợp hạch hạt nhân trong lõi mặt trời nung chảy các nguyên tử hydro để tạo ra năng lượng ánh sáng ban ngày.",
                "hint": "The process of joining two or more things together to form a single entity."
            },
            {
                "word": "nebula",
                "meaning": "tinh vân (danh từ)",
                "image": "🌌",
                "example": "A nebula is equivalent to an interstellar nursery where new stars are born from dust.",
                "example_vi": "Tinh vân tương đương với một vườn ươm giữa các vì sao, nơi những ngôi sao mới được sinh ra từ bụi.",
                "hint": "A cloud of gas and dust in outer space, visible in the night sky."
            },
            {
                "word": "kinetic",
                "meaning": "thuộc động năng (tính từ)",
                "image": "⚡",
                "example": "Wind turbines successfully convert the kinetic energy of wind into clean electricity.",
                "example_vi": "Các tuabin gió chuyển đổi thành công động năng của gió thành điện sạch.",
                "hint": "Relating to or resulting from motion."
            },
            {
                "word": "vacuum",
                "meaning": "chân không (danh từ)",
                "image": "🌌",
                "example": "Sound waves cannot travel through the absolute vacuum of outer space.",
                "example_vi": "Sóng âm thanh không thể truyền qua môi trường chân không tuyệt đối của không gian vũ trụ.",
                "hint": "A space entirely devoid of matter."
            }
        ]
    },
    {
        "id": "toefl_earth",
        "name": "Earth Sciences & Geology",
        "name_vi": "Địa chất & Khoa học Trái đất",
        "icon": "🌍",
        "words": [
            {
                "word": "glacier",
                "meaning": "sông băng (danh từ)",
                "image": "🏔️",
                "example": "Scientists monitor the retreat of the glacier to evaluate climate change rates.",
                "example_vi": "Các nhà khoa học theo dõi sự thu hẹp của sông băng để đánh giá tốc độ biến đổi khí hậu.",
                "hint": "A slowly moving mass or river of ice formed by the accumulation of snow."
            },
            {
                "word": "erosion",
                "meaning": "sự xói mòn (danh từ)",
                "image": "🏜️",
                "example": "Wind and water erosion shaped the stunning rock formations in the Grand Canyon.",
                "example_vi": "Sự xói mòn do gió và nước đã tạo nên những khối đá tuyệt đẹp ở hẻm núi Grand Canyon.",
                "hint": "The gradual destruction or diminution of something by wind, water, or other natural agents."
            },
            {
                "word": "seismic",
                "meaning": "thuộc địa chấn, động đất (tính từ)",
                "image": "📈",
                "example": "Delicate seismic sensors detect minor vibrations along tectonic plate fault lines.",
                "example_vi": "Các cảm biến địa chấn nhạy bén phát hiện các rung động nhỏ dọc theo các đường đứt gãy mảng kiến tạo.",
                "hint": "Relating to earthquakes or other vibrations of the earth and its objects."
            },
            {
                "word": "sedimentary",
                "meaning": "thuộc trầm tích (tính từ)",
                "image": "🪵",
                "example": "Fossils are primarily discovered within layers of ancient sedimentary rock.",
                "example_vi": "Hóa thạch chủ yếu được phát hiện bên trong các lớp đá trầm tích cổ đại.",
                "hint": "Relating to rock that has formed from sediment deposited by water or air."
            },
            {
                "word": "core",
                "meaning": "lõi, nhân Trái đất (danh từ / tính từ)",
                "image": "🔴",
                "example": "The outer core of Earth is composed mainly of liquid iron and nickel.",
                "example_vi": "Lõi ngoài của Trái đất chủ yếu bao gồm sắt và niken lỏng.",
                "hint": "The dense central region of a planet."
            },
            {
                "word": "eruption",
                "meaning": "sự phun trào (danh từ)",
                "image": "🌋",
                "example": "The volcanic eruption sent a massive cloud of ash high into the atmosphere.",
                "example_vi": "Sự phun trào núi lửa đã gửi một đám mây tro bụi khổng lồ lên cao bầu khí quyển.",
                "hint": "An act of exploding or bursting, especially of active volcanoes."
            },
            {
                "word": "continent",
                "meaning": "lục địa (danh từ)",
                "image": "🗺️",
                "example": "Millions of years ago, all seven regions were part of a single giant continent called Pangaea.",
                "example_vi": "Hàng triệu năm trước, tất cả bảy khu vực đều là một phần của một lục địa khổng lồ duy nhất gọi là Pangaea.",
                "hint": "Any of the world's main continuous expanses of land."
            },
            {
                "word": "topography",
                "meaning": "đại hình, địa hình học (danh từ)",
                "image": "⛰️",
                "example": "The complex topography of Norway features tall mountains and deep fjords.",
                "example_vi": "Địa hình phức tạp của Na Uy nổi bật với những ngọn núi cao và những vịnh hẹp sâu.",
                "hint": "The arrangement of the natural and artificial physical features of an area."
            },
            {
                "word": "peninsula",
                "meaning": "bán đảo (danh từ)",
                "image": "🏝️",
                "example": "The Korean Peninsula stretches south from the Asian mainland, bordered by water on three sides.",
                "example_vi": "Bán đảo Triều Tiên trải dài về phía nam từ lục địa châu Á, ba mặt giáp nước.",
                "hint": "A piece of land almost surrounded by water or projecting out into a body of water."
            },
            {
                "word": "resource",
                "meaning": "tài nguyên (danh từ)",
                "image": "💎",
                "example": "Fresh drinking water is a vital natural resource that remains scarce in some desert areas.",
                "example_vi": "Nước uống sạch là tài nguyên tự nhiên quan trọng đang trở nên khan hiếm ở một số vùng sa mạc.",
                "hint": "A stock or supply of materials or assets that can be drawn on by a person or organization."
            },
            {
                "word": "climate",
                "meaning": "khí hậu (danh từ)",
                "image": "☀️",
                "example": "Global warming causes extreme change patterns in local agricultural climates.",
                "example_vi": "Sự nóng lên toàn cầu gây ra các mô hình thay đổi khắc nghiệt trong khí hậu nông nghiệp địa phương.",
                "hint": "The weather conditions prevailing in an area in general or over a long period."
            },
            {
                "word": "tectonic",
                "meaning": "thuộc mảng kiến tạo (tính từ)",
                "image": "🗺️",
                "example": "The movement of massive tectonic plates can construct valleys or raise mountains.",
                "example_vi": "Sự di chuyển của các mảng kiến tạo khổng lồ có thể tạo ra các thung lũng hoặc nâng cao các ngọn núi.",
                "hint": "Relating to the structure of the earth's crust and the large-scale processes which take place within it."
            },
            {
                "word": "magma",
                "meaning": "mác-ma, đá nóng chảy (danh từ)",
                "image": "🌋",
                "example": "When underground magma breaks through the crust, it is called lava.",
                "example_vi": "Khi mác-ma dưới lòng đất phun qua lớp vỏ Trái đất, nó được gọi là dung nham.",
                "hint": "Hot fluid or semi-fluid material below or within the earth's crust."
            },
            {
                "word": "terrain",
                "meaning": "địa hình, địa thế (danh từ)",
                "image": "⛰️",
                "example": "The rugged terrain made marching search and rescue efforts extremely slow.",
                "example_vi": "Địa hình hiểm trở khiến cho các nỗ lực hành quân tìm kiếm cứu nạn tiến triển rất chậm.",
                "hint": "A stretch of land, especially with regard to its physical features."
            },
            {
                "word": "mineral",
                "meaning": "khoáng vật, khoáng chất (danh từ)",
                "image": "💎",
                "example": "Geologists examine the atomic structure of the mineral to identify its composition.",
                "example_vi": "Các nhà địa chất kiểm tra cấu trúc nguyên tử của khoáng vật để xác định thành phần của nó.",
                "hint": "A solid inorganic substance of natural occurrence."
            }
        ]
    },
    {
        "id": "toefl_econ",
        "name": "Economics & Public Policy",
        "name_vi": "Kinh tế học & Chính sách công",
        "icon": "📈",
        "words": [
            {
                "word": "inflation",
                "meaning": "sự lạm phát (danh từ)",
                "image": "💸",
                "example": "High inflation reduces the purchasing power of the national currency.",
                "example_vi": "Lạm phát cao làm giảm sức mua của đồng nội tệ.",
                "hint": "A general increase in prices and fall in the purchasing value of money."
            },
            {
                "word": "surplus",
                "meaning": "thặng dư, số dư (danh từ / tính từ)",
                "image": "📈",
                "example": "The country maintained a trade surplus by exporting more than it imported.",
                "example_vi": "Quốc gia này đã duy trì mức thặng dư thương mại bằng cách xuất khẩu nhiều hơn nhập khẩu.",
                "hint": "An amount of something left over when requirements have been met."
            },
            {
                "word": "deficit",
                "meaning": "sự thâm hụt, thâm hụt ngân sách (danh từ)",
                "image": "📉",
                "example": "The government is forced to borrow money to bridge its annual budget deficit.",
                "example_vi": "Chính phủ buộc phải vay tiền để bù đắp thâm hụt ngân sách hàng năm.",
                "hint": "The amount by which something, especially a sum of money, is too small."
            },
            {
                "word": "monopoly",
                "meaning": "sự độc quyền (danh từ)",
                "image": "🏢",
                "example": "Anti-trust regulations strive to break up any firm that establishes a monopoly.",
                "example_vi": "Các quy định chống độc quyền nỗ lực giải thể bất kỳ công ty nào thiết lập thế độc quyền.",
                "hint": "The exclusive possession or control of the supply of or trade in a commodity or service."
            },
            {
                "word": "tariff",
                "meaning": "thuế quan, thuế xuất nhập khẩu (danh từ)",
                "image": "💸",
                "example": "The president imposed a high tariff on imported steel to protect local mills.",
                "example_vi": "Tổng thống đã áp đặt mức thuế quan cao đối với thép nhập khẩu để bảo vệ các nhà máy thép địa phương.",
                "hint": "A tax or duty to be paid on a particular class of imports or exports."
            },
            {
                "word": "commodity",
                "meaning": "hàng hóa, thương phẩm (danh từ)",
                "image": "📦",
                "example": "Crude oil is the most heavily traded commodity in the global market.",
                "example_vi": "Dầu thô là loại hàng hóa được giao dịch nhiều nhất trên thị trường toàn cầu.",
                "hint": "A raw material or primary agricultural product that can be bought and sold."
            },
            {
                "word": "currency",
                "meaning": "tiền tệ (danh từ)",
                "image": "💵",
                "example": "Travelers can exchange their local currency at the airport terminal.",
                "example_vi": "Du khách có thể đổi đồng tiền tệ địa phương tại nhà ga sân bay.",
                "hint": "A system of money in common use in a country."
            },
            {
                "word": "capital",
                "meaning": "vốn, vốn đầu tư (danh từ)",
                "image": "💰",
                "example": "Our startup raised several million dollars in venture capital.",
                "example_vi": "Công ty khởi nghiệp của chúng tôi đã huy động được vài triệu đô la vốn đầu tư mạo hiểm.",
                "hint": "Wealth in the form of money or other assets owned by a person or organization."
            },
            {
                "word": "globalization",
                "meaning": "sự toàn cầu hóa (danh từ)",
                "image": "🌐",
                "example": "Globalization accelerates the exchange of cultural and technological ideas.",
                "example_vi": "Toàn cầu hóa thúc đẩy nhanh sự trao đổi các tư tưởng văn hóa và công nghệ.",
                "hint": "The process by which businesses or other organizations develop international influence."
            },
            {
                "word": "recession",
                "meaning": "sự suy thoái kinh tế (danh từ)",
                "image": "📉",
                "example": "High unemployment rates are a characteristic symptom of an economic recession.",
                "example_vi": "Tỷ lệ thất nghiệp cao là triệu chứng đặc trưng của một cuộc suy thoái kinh tế.",
                "hint": "A period of temporary economic decline during which trade and industrial activity are reduced."
            },
            {
                "word": "taxation",
                "meaning": "sự đánh thuế, hệ thống thuế (danh từ)",
                "image": "💸",
                "example": "The government funds public services like healthcare through progressive taxation.",
                "example_vi": "Chính phủ tài trợ cho các dịch vụ công như chăm sóc sức khỏe thông qua đánh thuế lũy tiến.",
                "hint": "The levying of tax by a government."
            },
            {
                "word": "subsidy",
                "meaning": "tiền trợ cấp, bao cấp (danh từ)",
                "image": "💰",
                "example": "Farmers receive a financial subsidy to make healthy food affordable for everyone.",
                "example_vi": "Các nông dân nhận được tiền trợ cấp tài chính để giúp thực phẩm lành mạnh có giá cả phải chăng cho mọi người.",
                "hint": "A sum of money granted by the state or a public body to help an industry or business."
            },
            {
                "word": "consumer",
                "meaning": "người tiêu dùng (danh từ)",
                "image": "🛒",
                "example": "Consumer confidence rose sharply following the positive employment report.",
                "example_vi": "Niềm tin của người tiêu dùng đã tăng mạnh sau báo cáo tích cực về việc làm.",
                "hint": "A person who purchases goods and services for personal use."
            },
            {
                "word": "commercial",
                "meaning": "thuộc thương mại (tính từ)",
                "image": "🏢",
                "example": "The area is zoned for commercial development rather than residential housing.",
                "example_vi": "Khu vực này được quy hoạch cho phát triển thương mại chứ không phải nhà ở dân cư.",
                "hint": "Concerned with or engaged in commerce."
            },
            {
                "word": "trade",
                "meaning": "giao thương, mậu dịch (danh từ / động từ)",
                "image": "🚢",
                "example": "The trade agreement removed heavy tariffs, boosting regional cooperation.",
                "example_vi": "Hiệp định thương mại đã dỡ bỏ các mức thuế quan cao, thúc đẩy hợp tác khu vực.",
                "hint": "The action of buying and selling goods and services."
            }
        ]
    },
    {
        "id": "toefl_psych",
        "name": "Psychology & Neurology",
        "name_vi": "Tâm lý học & Thần kinh học",
        "icon": "🧠",
        "words": [
            {
                "word": "cognitive",
                "meaning": "thuộc nhận thức (tính từ)",
                "image": "🧠",
                "example": "Puzzles and reading can maintain cognitive health in absolute old age.",
                "example_vi": "Trò chơi đố chữ và đọc sách có thể duy trì sức khỏe nhận thức ở tuổi già tuyệt đối.",
                "hint": "Relating to mental processes of perception, memory, judgment, and reasoning."
            },
            {
                "word": "perception",
                "meaning": "sự nhận thức, giác quan (danh từ)",
                "image": "👁️",
                "example": "Optical illusions demonstrate how easily our visual perception can be deceived.",
                "example_vi": "Ảo ảnh thị giác chứng minh nhận thức thị giác của chúng ta có thể dễ bị đánh lừa như thế nào.",
                "hint": "The ability to see, hear, or become aware of something through the senses."
            },
            {
                "word": "stimulus",
                "meaning": "tác nhân kích thích (danh từ)",
                "image": "⚡",
                "example": "The bright flashing light served as a powerful sensory stimulus for the child.",
                "example_vi": "Ánh sáng nhấp nháy rực rỡ đóng vai trò là một tác nhân kích thích giác quan mạnh mẽ đối với đứa trẻ.",
                "hint": "A thing or event that evokes a specific functional reaction in an organ or tissue."
            },
            {
                "word": "behavior",
                "meaning": "hành vi, cách cư xử (danh từ)",
                "image": "👤",
                "example": "Psychologists study human behavior in social groups to understand peer pressure.",
                "example_vi": "Các nhà tâm lý học nghiên cứu hành vi của con người trong các nhóm xã hội để hiểu về áp lực bạn bè.",
                "hint": "The way in which one acts or conducts oneself, especially toward others."
            },
            {
                "word": "consensus",
                "meaning": "sự đồng thuận, nhất trí (danh từ)",
                "image": "🤝",
                "example": "After hours of heated debate, the board finally reached a broad consensus.",
                "example_vi": "Sau hàng giờ tranh luận gay gắt, ban quản trị cuối cùng đã đạt được sự đồng thuận rộng rãi.",
                "hint": "A general agreement."
            },
            {
                "word": "collective",
                "meaning": "tập thể, chung (tính từ / danh từ)",
                "image": "👥",
                "example": "The society's collective memory of the war helps maintain peace.",
                "example_vi": "Ký ức tập thể của xã hội về chiến tranh giúp duy trì hòa bình.",
                "hint": "Done by people acting as a group."
            },
            {
                "word": "anxiety",
                "meaning": "sự lo âu (danh từ)",
                "image": "😰",
                "example": "Exam preparation and early planning can help alleviate students' high anxiety.",
                "example_vi": "Chuẩn bị ôn thi và lên kế hoạch sớm có thể giúp giảm bớt sự lo âu cao độ của học sinh.",
                "hint": "A feeling of worry, nervousness, or unease, typically about an imminent event."
            },
            {
                "word": "instinct",
                "meaning": "bản năng (danh từ)",
                "image": "🦁",
                "example": "Many animals rely on instinct rather than learned behavior to avoid predators.",
                "example_vi": "Nhiều loài động vật dựa vào bản năng thay vì hành vi học được để tránh động vật ăn thịt.",
                "hint": "An innate, typically fixed pattern of behavior in animals."
            },
            {
                "word": "conditioning",
                "meaning": "sự huấn luyện, tạo phản xạ (danh từ)",
                "image": "🐕",
                "example": "Pavlov became famous for his pioneering research in salivary conditioning of dogs.",
                "example_vi": "Pavlov đã trở nên nổi tiếng nhờ nghiên cứu tiên phong của mình về việc tạo phản xạ tiết nước bọt ở chó.",
                "hint": "The process of training oneself or an animal to behave in a certain way."
            },
            {
                "word": "subconscious",
                "meaning": "tiềm thức (danh từ / tính từ)",
                "image": "🧠",
                "example": "Dreams often provide a fascinating window into our deep subconscious fears.",
                "example_vi": "Giấc mơ thường mang lại một cửa sổ hấp dẫn mở vào nỗi sợ sâu thẳm trong tiềm thức của chúng ta.",
                "hint": "Concerning the part of the mind of which one is not fully aware."
            },
            {
                "word": "emotion",
                "meaning": "cảm xúc (danh từ)",
                "image": "❤️",
                "example": "Fear is a basic primal emotion that triggers our fight-or-flight response.",
                "example_vi": "Sợ hãi là một cảm xúc nguyên thủy cơ bản kích hoạt phản ứng chiến đấu hoặc bỏ chạy của chúng ta.",
                "hint": "A natural instinctive state of mind deriving from one's circumstances."
            },
            {
                "word": "empathy",
                "meaning": "sự thấu cảm (danh từ)",
                "image": "🤝",
                "example": "Developing empathy allows therapists to connect deeply with their struggling patients.",
                "example_vi": "Phát triển sự thấu cảm cho phép các nhà trị liệu kết nối sâu sắc với những bệnh nhân đang gặp khó khăn của họ.",
                "hint": "The ability to understand and share the feelings of another."
            },
            {
                "word": "neurosis",
                "meaning": "bệnh loạn thần kinh (danh từ)",
                "image": "🧠",
                "example": "Obsessive handwashing can be a classic manifestation of mild neurosis.",
                "example_vi": "Rửa tay ám ảnh có thể là biểu hiện kinh điển của bệnh loạn thần kinh nhẹ.",
                "hint": "A relatively mild mental illness that is not caused by organic disease."
            },
            {
                "word": "trauma",
                "meaning": "chấn thương tâm lý (danh từ)",
                "image": "😭",
                "example": "Childhood trauma can leave deep emotional scars that persist into adulthood.",
                "example_vi": "Chấn thương tâm lý thời thơ ấu có thể để lại những vết sẹo cảm xúc sâu sắc kéo dài đến tuổi trưởng thành.",
                "hint": "A deeply distressing or disturbing experience."
            },
            {
                "word": "sensory",
                "meaning": "thuộc giác quan (tính từ)",
                "image": "👁️",
                "example": "Our sensory receptors carry signals about temperature and pain directly to the brain.",
                "example_vi": "Các thụ thể giác quan của chúng ta truyền tín hiệu về nhiệt độ và đau đớn trực tiếp đến não.",
                "hint": "Relating to sensation or the physical senses."
            }
        ]
    },
    {
        "id": "toefl_art",
        "name": "Arts & Literature",
        "name_vi": "Nghệ thuật & Văn học",
        "icon": "🎨",
        "words": [
            {
                "word": "masterpiece",
                "meaning": "kiệt tác (danh từ)",
                "image": "🖼️",
                "example": "Leonardo da Vinci's Mona Lisa is widely considered a supreme artistic masterpiece.",
                "example_vi": "Tác phẩm Mona Lisa của Leonardo da Vinci được coi là một kiệt tác nghệ thuật tối cao.",
                "hint": "A work of outstanding artistry, skill, or workmanship."
            },
            {
                "word": "aesthetic",
                "meaning": "thống mỹ, tính thẩm mỹ (tính từ / danh từ)",
                "image": "✨",
                "example": "Minimalist home designs focus heavily on simple, clean aesthetic appeal.",
                "example_vi": "Thiết kế nhà tối giản tập trung mạnh mẽ vào sức hấp dẫn thẩm mỹ đơn giản và sạch sẽ.",
                "hint": "Concerned with beauty or the appreciation of beauty."
            },
            {
                "word": "canvas",
                "meaning": "vải bạt vẽ tranh (danh từ)",
                "image": "🎨",
                "example": "The artist stretched the canvas tightly over the wooden frame before painting.",
                "example_vi": "Họa sĩ đã kéo căng tấm vải vẽ tranh lên khung gỗ trước khi sơn.",
                "hint": "A strong, coarse unbleached cloth used as a surface for oil painting."
            },
            {
                "word": "genre",
                "meaning": "thể loại (danh từ)",
                "image": "📚",
                "example": "Science fiction remains my favorite literary genre because it sparks the imagination.",
                "example_vi": "Khoa học viễn tưởng vẫn là thể loại văn học yêu thích của tôi vì nó kích thích trí tưởng tượng.",
                "hint": "A category of artistic composition characterized by similarities in form, style, or subject matter."
            },
            {
                "word": "prose",
                "meaning": "văn xuôi (danh từ)",
                "image": "📖",
                "example": "Her elegant prose captures details far better than most formal poetry.",
                "example_vi": "Văn xuôi thanh lịch của cô ấy ghi lại các chi tiết tốt hơn nhiều so với hầu hết các bài thơ trang trọng.",
                "hint": "Written or spoken language in its ordinary form, without metrical structure."
            },
            {
                "word": "protagonist",
                "meaning": "nhân vật chính (danh từ)",
                "image": "👤",
                "example": "In the classical novel, the brave protagonist battles great hardships to save his home.",
                "example_vi": "Trong cuốn tiểu thuyết cổ điển, nhân vật chính dũng cảm chiến đấu với những khó khăn lớn để cứu ngôi nhà của mình.",
                "hint": "The leading character or one of the major characters in a drama, movie, novel."
            },
            {
                "word": "sculpture",
                "meaning": "tác phẩm điêu khắc (danh từ)",
                "image": "🗿",
                "example": "A marble sculpture of a Greek goddess stands at the center of the royal museum.",
                "example_vi": "Một bức tượng điêu khắc bằng đá cẩm thạch của một nữ thần Hy Lạp đứng ở giữa bảo tàng hoàng gia.",
                "hint": "The art of making two- or three-dimensional representative or abstract forms, especially by carving."
            },
            {
                "word": "avant-garde",
                "meaning": "tiên phong (tính từ / danh từ)",
                "image": "🚀",
                "example": "His avant-garde fashion designs challenged standard social norms of dress in 1920.",
                "example_vi": "Các thiết kế thời trang tiên phong của ông đã thách thức những chuẩn mực xã hội thông thường về trang phục vào năm 1920.",
                "hint": "Favoring or introducing experimental or unusual ideas."
            },
            {
                "word": "folklore",
                "meaning": "văn hóa dân gian (danh từ)",
                "image": "🎻",
                "example": "Generations passes on local history and values through traditional animal folklore.",
                "example_vi": "Nhiều thế hệ truyền tải lịch sử và giá trị địa phương thông qua truyện dân gian động vật truyền thống.",
                "hint": "The traditional beliefs, customs, and stories of a community, passed through word of mouth."
            },
            {
                "word": "metaphor",
                "meaning": "phép ẩn dụ (danh từ)",
                "image": "💡",
                "example": "In speech, the phrase 'time is money' is a widely utilized commercial metaphor.",
                "example_vi": "Trong văn nói, cụm từ 'thời gian là vàng bạc' là một phép ẩn dụ thương mại được sử dụng rộng rãi.",
                "hint": "A figure of speech in which a word or phrase is applied to an object or action to which it is not literally applicable."
            },
            {
                "word": "exhibition",
                "meaning": "triển lãm (danh từ)",
                "image": "🏛️",
                "example": "My local art student group sponsored a beautiful photography exhibition.",
                "example_vi": "Nhóm sinh viên nghệ thuật địa phương của tôi đã tài trợ cho một cuộc triển lãm ảnh tuyệt đẹp.",
                "hint": "A public display of works of art or other items of interest."
            },
            {
                "word": "abstract",
                "meaning": "trừu tượng (tính từ / danh từ)",
                "image": "🧩",
                "example": "It is hard to grasp abstract concepts without concrete physical examples.",
                "example_vi": "Thật khó để nắm bắt các khái niệm trừu tượng nếu không có các ví dụ hình thể cụ thể.",
                "hint": "Existing in thought or as an idea but not having a physical or concrete existence."
            },
            {
                "word": "portray",
                "meaning": "khắc họa, mô tả (động từ)",
                "image": "🎭",
                "example": "The movie strives to portray the hard lives of factory workers in the early industrial era.",
                "example_vi": "Bộ phim nỗ lực mô tả cuộc sống khó khăn của những công nhân nhà máy trong thời kỳ đầu công nghiệp.",
                "hint": "Depict (someone or something) in a work of art or literature."
            },
            {
                "word": "expression",
                "meaning": "sự biểu đạt, biểu cảm (danh từ)",
                "image": "😊",
                "example": "Art is a powerful form of emotional self-expression for troubled teenagers.",
                "example_vi": "Nghệ thuật là một hình thức biểu đạt bản thân mạnh mẽ về mặt cảm xúc cho thanh thiếu niên gặp khó khăn.",
                "hint": "The action of making known one's thoughts or feelings."
            },
            {
                "word": "architecture",
                "meaning": "kiến trúc (danh từ)",
                "image": "🏛️",
                "example": "Gothic architecture is characterized by tall columns, pointed arches, and flying buttresses.",
                "example_vi": "Kiến trúc Gothic đặc trưng bởi các cột cao, vòm nhọn và cấu trúc chống chịu lực bay.",
                "hint": "The art or practice of designing and constructing buildings."
            }
        ]
    },
    {
        "id": "toefl_tech",
        "name": "Technology & Science",
        "name_vi": "Công nghệ & Đột phá kỹ thuật",
        "icon": "💻",
        "words": [
            {
                "word": "revolutionize",
                "meaning": "cách mạng hóa (động từ)",
                "image": "🚀",
                "example": "Smartphones successfully managed to revolutionize the way people correspond and work.",
                "example_vi": "Điện thoại thông minh đã thành công trong việc cách mạng hóa cách mọi người liên lạc và làm việc.",
                "hint": "Change something radically or fundamentally."
            },
            {
                "word": "cybernetics",
                "meaning": "điều khiển học (danh từ)",
                "image": "🤖",
                "example": "Cybernetics bridges the gap between mechanical automation and human neural signals.",
                "example_vi": "Điều khiển học thu hẹp khoảng cách giữa tự động hóa cơ khí và tín hiệu thần kinh của con người.",
                "hint": "The science of communications and automatic control systems in both machines and living things."
            },
            {
                "word": "algorithm",
                "meaning": "thuật toán (danh từ)",
                "image": "🧮",
                "example": "The search engine's secret algorithm ranks sites based on user satisfaction and loading speed.",
                "example_vi": "Thuật toán bí mật của công cụ tìm kiếm xếp hạng các trang web dựa trên sự hài lòng của người dùng và tốc độ tải trang.",
                "hint": "A process or set of rules to be followed in calculations or other problem-solving operations."
            },
            {
                "word": "database",
                "meaning": "cơ sở dữ liệu (danh từ)",
                "image": "📦",
                "example": "Staff must secure the database containing customers' personal financial credit credentials.",
                "example_vi": "Nhân viên phải bảo mật cơ sở dữ liệu chứa thông tin tín dụng tài chính cá nhân của khách hàng.",
                "hint": "A structured set of data held in a computer, especially one that is accessible in various ways."
            },
            {
                "word": "hardware",
                "meaning": "phần cứng (danh từ)",
                "image": "🔌",
                "example": "Upgrading your computer's memory hardware will accelerate video editing software.",
                "example_vi": "Nâng cấp phần cứng bộ nhớ máy tính của bạn sẽ tăng tốc phần mềm chỉnh sửa video.",
                "hint": "The physical parts of a computer."
            },
            {
                "word": "automation",
                "meaning": "sự tự động hóa (danh từ)",
                "image": "🤖",
                "example": "Industrial automation increased production metrics while lowering physical labor requirements.",
                "example_vi": "Tự động hóa công nghiệp đã tăng chỉ số sản xuất đồng thời giảm bớt yêu cầu lao động thể chất.",
                "hint": "The use of largely automatic equipment in a system of manufacturing or other production process."
            },
            {
                "word": "network",
                "meaning": "mạng lưới (danh từ / động từ)",
                "image": "🌐",
                "example": "A robust local area network connects all corporate workstations to the central database server.",
                "example_vi": "Một mạng nội bộ mạnh mẽ kết nối tất cả các máy trạm của doanh nghiệp với máy chủ cơ sở dữ liệu trung tâm.",
                "hint": "A group of interconnected people or things."
            },
            {
                "word": "synthesize",
                "meaning": "tổng hợp (động từ)",
                "image": "🧪",
                "example": "Chemical engineers synthesize durable polymers inside clean laboratory environments.",
                "example_vi": "Các kỹ sư hóa học tổng hợp các polyme bền vững bên trong môi trường phòng thí nghiệm sạch mượt.",
                "hint": "Combine elements or materials in a single entity."
            },
            {
                "word": "digital",
                "meaning": "kỹ thuật số (tính từ)",
                "image": "💾",
                "example": "The digital revolution replaced vinyl records and legacy tape with streaming data.",
                "example_vi": "Cuộc cách mạng kỹ thuật số đã thay thế đĩa than và băng đĩa cũ bằng truyền dữ liệu trực tuyến.",
                "hint": "Expressed as series of the digits 0 and 1, typically represented by values."
            },
            {
                "word": "innovation",
                "meaning": "sự đổi mới, sáng kiến mới (danh từ)",
                "image": "💡",
                "example": "Constant technological innovation keeps the electronics manufacturer ahead of foreign rivals.",
                "example_vi": "Sự đổi mới công nghệ liên tục giúp nhà sản xuất điện tử đi trước các đối thủ nước ngoài.",
                "hint": "The action or process of innovating; a new method or idea."
            },
            {
                "word": "electronic",
                "meaning": "thuộc về điện tử (tính từ)",
                "image": "📺",
                "example": "They manufactured lighter electronic components utilizing carbon nanotubes.",
                "example_vi": "Họ đã sản xuất các linh kiện điện tử nhẹ hơn bằng cách sử dụng ống nano carbon.",
                "hint": "Having or operating with components such as microchips."
            },
            {
                "word": "artificial",
                "meaning": "nhân tạo (tính từ)",
                "image": "🤖",
                "example": "Artificial sweeteners mimic sugar but contain zero calories, helping weight loss.",
                "example_vi": "Chất làm ngọt nhân tạo bắt chước đường nhưng chứa không calo, giúp giảm cân hữu ích.",
                "hint": "Made or produced by human beings rather than occurring naturally."
            },
            {
                "word": "transmit",
                "meaning": "truyền tải, phát sóng (động từ)",
                "image": "📡",
                "example": "Fiber optic cables transmit data packages across oceans at absolute speed.",
                "example_vi": "Cáp quang truyền dữ liệu qua các đại dương với tốc độ tuyệt đối mượt mà.",
                "hint": "Pass on from one place or person to another."
            },
            {
                "word": "program",
                "meaning": "chương trình, viết chương trình (danh từ / động từ)",
                "image": "💻",
                "example": "Students learn to program efficient robotic systems during the summer school seminar.",
                "example_vi": "Học sinh học cách lập trình các hệ thống robot hiệu quả trong hội thảo trường học mùa hè.",
                "hint": "A series of coded software instructions to control the operation of a computer."
            },
            {
                "word": "process",
                "meaning": "quy trình, xử lý (danh từ / động từ)",
                "image": "🏭",
                "example": "Computers process millions of operations per second to render complex simulations.",
                "example_vi": "Máy tính xử lý hàng triệu phép tính mỗi giây để hiển thị mô phỏng phức tạp.",
                "hint": "A series of actions or steps taken in order to achieve a particular end."
            }
        ]
    },
    {
        "id": "toefl_env",
        "name": "Climate & Environment",
        "name_vi": "Thời tiết & Bảo vệ Môi trường",
        "icon": "🍀",
        "words": [
            {
                "word": "greenhouse",
                "meaning": "nhà kính (danh từ / tính từ)",
                "image": "🏡",
                "example": "The greenhouse effect traps warm heat, which causes global temperatures to rise.",
                "example_vi": "Hiệu ứng nhà kính giữ lại nhiệt ấm, là nguyên nhân làm tăng nhiệt độ toàn cầu.",
                "hint": "A glass building in which plants are grown / related to gas trapping heat."
            },
            {
                "word": "pollution",
                "meaning": "sự ô nhiễm (danh từ)",
                "image": "🏭",
                "example": "Automobile combustion emissions are a primary source of air pollution in giant cities.",
                "example_vi": "Khí thải đốt xe ô tô là nguồn gây ô nhiễm không khí hàng đầu ở các thành phố khổng lồ.",
                "hint": "The presence in or introduction into the environment of a substance or thing that has harmful effects."
            },
            {
                "word": "renewable",
                "meaning": "có thể tái tạo (tính từ)",
                "image": "☀️",
                "example": "Transitioning to renewable energy like solar power reduce global carbon footprints.",
                "example_vi": "Chuyển đổi sang năng lượng tái tạo như điện mặt trời làm giảm lượng khí thải carbon toàn cầu.",
                "hint": "Not depleted when used, because it is of a source that occurs naturally."
            },
            {
                "word": "ozone",
                "meaning": "tầng ô-zôn (danh từ)",
                "image": "🛡️",
                "example": "The ozone layer blocks harmful ultraviolet radiation from reaching Earth's surface.",
                "example_vi": "Tầng ô-zôn chặn bức xạ cực tím có hại tiếp cận bề mặt Trái đất.",
                "hint": "A colorless toxic gas with a pungent odor, forming a protective planetary shield."
            },
            {
                "word": "conservation",
                "meaning": "sự bảo tồn, gìn giữ (danh từ)",
                "image": "🦁",
                "example": "Marine conservation programs strive to repair damaged coral reefs and protect endangered species.",
                "example_vi": "Các chương trình bảo tồn biển nỗ lực phục hồi các rạn san hô bị hư hại và bảo vệ các loài có nguy cơ tuyệt chủng.",
                "hint": "Prevention of wasteful use of a resource / preservation of wildlife."
            },
            {
                "word": "biodegradable",
                "meaning": "có thể phân hủy sinh học (tính từ)",
                "image": "📦",
                "example": "Using biodegradable food packaging reduces the amount of plastic in landfills.",
                "example_vi": "Sử dụng bao bì thực phẩm có thể phân hủy sinh học làm giảm lượng nhựa trong các bãi chôn lấp.",
                "hint": "Capable of being decomposed by bacteria or other living organisms."
            },
            {
                "word": "emissions",
                "meaning": "khí thải (danh từ số nhiều)",
                "image": "💨",
                "example": "The international accord mandates a dramatic reduction in carbon emissions by 2030.",
                "example_vi": "Hiệp ước quốc tế quy định việc cắt giảm mạnh mẽ lượng khí thải carbon vào năm 2030.",
                "hint": "The production and discharge of something, especially gas or radiation."
            },
            {
                "word": "deforestation",
                "meaning": "nạn phá rừng (danh từ)",
                "image": "🪵",
                "example": "Deforestation causes severe habitat loss and contributes significantly to climate change.",
                "example_vi": "Nạn phá rừng gây mất môi trường sống trầm trọng và đóng góp đáng kể vào biến đổi khí hậu.",
                "hint": "The action of clearing a wide area of trees."
            },
            {
                "word": "sustainable",
                "meaning": "bền vững (tính từ)",
                "image": "🌿",
                "example": "Organic, sustainable farming practices maintain soil fertility without toxic chemicals.",
                "example_vi": "Các phương pháp canh tác hữu cơ, bền vững duy trì độ phì nhiêu của đất mà không cần hóa chất độc hại.",
                "hint": "Able to be maintained at a certain rate or level; ecological balance preservation."
            },
            {
                "word": "precipitation",
                "meaning": "lượng mưa, sự kết tủa (danh từ)",
                "image": "🌧️",
                "example": "The local weather forecast calls for heavy precipitation throughout the entire weekend.",
                "example_vi": "Dự báo thời tiết địa phương dự đoán lượng mưa lớn trong suốt cả cuối tuần.",
                "hint": "Rain, snow, sleet, or hail that falls to the ground."
            },
            {
                "word": "drought",
                "meaning": "hạn hán (danh từ)",
                "image": "🏜️",
                "example": "A continuous decade of drought caused major rivers in the region to dry up completely.",
                "example_vi": "Hạn hán kéo dài suốt một thập kỷ liên tục khiến các con sông lớn trong vùng bị cạn kiệt hoàn toàn.",
                "hint": "A prolonged period of abnormally low rainfall, leading to a shortage of water."
            },
            {
                "word": "ecology",
                "meaning": "sinh thái học (danh từ)",
                "image": "🌳",
                "example": "The study of forest ecology highlights the cooperative interactions between fungi and trees.",
                "example_vi": "Nghiên cứu sinh thái học rừng làm nổi bật các tương tác hợp tác giữa nấm và cây thân gỗ.",
                "hint": "The political or scientific study of the relations of organisms to one another and to physical surroundings."
            },
            {
                "word": "toxic",
                "meaning": "độc hại (tính từ)",
                "image": "🧪",
                "example": "Factory supervisors were heavily fined for dumping toxic waste products into the local river.",
                "example_vi": "Các giám sát viên nhà máy đã bị phạt nặng vì đổ chất thải độc hại ra dòng sông địa phương.",
                "hint": "Poisonous or very harmful."
            },
            {
                "word": "alternative",
                "meaning": "thay thế (tính từ / danh từ)",
                "image": "🔄",
                "example": "Geothermal and wind are excellent alternative options for standard coal-based electricity plants.",
                "example_vi": "Địa nhiệt và gió là những tùy chọn thay thế tuyệt vời cho nhà máy điện chạy bằng than tiêu chuẩn.",
                "hint": "One of two or more available possibilities / alternative power."
            },
            {
                "word": "recycle",
                "meaning": "tái chế (động từ)",
                "image": "♻️",
                "example": "Civic programs encourage households to partition and recycle glass, plastic, and paper.",
                "example_vi": "Các chương trình dân sự khuyến khích các hộ gia đình phân chia và tái chế thủy tinh, nhựa và giấy.",
                "hint": "Convert waste into reusable material."
            }
        ]
    },
    {
        "id": "toefl_edu",
        "name": "Campus Life & Education",
        "name_vi": "Đời sống Đại học & Giáo dục",
        "icon": "🎓",
        "words": [
            {
                "word": "syllabus",
                "meaning": "đề cương môn học (danh từ)",
                "image": "📖",
                "example": "The professor distributed the detailed syllabus on the first day of the academic semester.",
                "example_vi": "Giáo sư đã phát đề cương môn học chi tiết vào ngày đầu tiên của học kỳ học thuật.",
                "hint": "An outline of the subjects in a course of study or teaching."
            },
            {
                "word": "curriculum",
                "meaning": "chương trình giảng dạy (danh từ)",
                "image": "📚",
                "example": "The university math department decided to revise its undergraduate calculus curriculum.",
                "example_vi": "Khoa toán trường đại học đã quyết định điều chỉnh chương trình giảng dạy giải tích bậc cử nhân của mình.",
                "hint": "The subjects comprising a course of study in a school or college."
            },
            {
                "word": "scholarship",
                "meaning": "học bổng (danh từ)",
                "image": "🎓",
                "example": "She won an academic scholarship that covers tuition and dormitory housing fees completely.",
                "example_vi": "Cô ấy đã giành được một học bổng học thuật đài thọ hoàn toàn học phí và phí ký túc xá.",
                "hint": "A grant or payment made to support a student's education, awarded on the basis of academic merit."
            },
            {
                "word": "faculty",
                "meaning": "giảng viên, ban giám hiệu (danh từ)",
                "image": "👤",
                "example": "The physics faculty consists of distinguished Nobel laureate researchers.",
                "example_vi": "Đội ngũ giảng viên vật lý bao gồm các nhà nghiên cứu đoạt giải Nobel nổi tiếng.",
                "hint": "The teaching staff of a university or college."
            },
            {
                "word": "registrar",
                "meaning": "phòng đào tạo, hộ tịch viên (danh từ)",
                "image": "🏢",
                "example": "Students must consult the registrar to obtain official copies of academic transcripts.",
                "example_vi": "Sinh viên phải tham khảo phòng đào tạo để lấy bản sao chính thức của bảng điểm học thuật.",
                "hint": "An official in an academic institution who handles student registrations and grades."
            },
            {
                "word": "thesis",
                "meaning": "luận văn tốt nghiệp (danh từ)",
                "image": "📖",
                "example": "To graduate with honors, she must write and defend a 50-page economics thesis.",
                "example_vi": "Để tốt nghiệp loại ưu, cô ấy phải viết và bảo vệ một luận văn kinh tế học dài 50 trang.",
                "hint": "A long essay or dissertation involving personal research, written by a candidate for a college degree."
            },
            {
                "word": "tuition",
                "meaning": "học phí (danh từ)",
                "image": "💵",
                "example": "College tuition fees are rising faster than standard annual household inflation metrics.",
                "example_vi": "Phí học phí đại học đang tăng nhanh hơn so với các chỉ số lạm phát hộ gia đình hàng năm tiêu chuẩn.",
                "hint": "A sum of money charged for teaching or instruction by a school, college, or university."
            },
            {
                "word": "semester",
                "meaning": "học kỳ (danh từ)",
                "image": "📅",
                "example": "Our university divides the academic calendar year into a fall and a spring semester.",
                "example_vi": "Trường đại học của chúng tôi chia năm học học thuật thành học kỳ mùa thu và học kỳ mùa xuân.",
                "hint": "A half-year term in a school or college, typically lasting fifteen to eighteen weeks."
            },
            {
                "word": "internship",
                "meaning": "kỳ thực tập, công việc thực tập (danh từ)",
                "image": "💼",
                "example": "Getting a summer internship at a software company boosts your employment opportunities.",
                "example_vi": "Có được một công việc thực tập mùa hè tại công ty phần mềm giúp tăng cơ hội việc làm của bạn.",
                "hint": "The position of a student or trainee who works in an organization, sometimes without pay, to gain work experience."
            },
            {
                "word": "prerequisite",
                "meaning": "điều kiện tiên quyết (danh từ / tính từ)",
                "image": "🔑",
                "example": "Basic algebra is an absolute prerequisite for taking advanced calculus classes.",
                "example_vi": "Đại số cơ bản là điều kiện tiên quyết tuyệt đối để tham gia các lớp giải tích nâng cao.",
                "hint": "A thing that is required as a prior condition for something else to happen or exist."
            },
            {
                "word": "major",
                "meaning": "chuyên ngành (danh từ / động từ)",
                "image": "🎓",
                "example": "He decided to major in artificial intelligence and minor in economics.",
                "example_vi": "Anh ấy quyết định chọn chuyên ngành chính là trí tuệ nhân tạo và chuyên ngành phụ là kinh tế học.",
                "hint": "The main subject of study for an undergraduate university student."
            },
            {
                "word": "dormitory",
                "meaning": "ký túc xá (danh từ)",
                "image": "🏢",
                "example": "Living in a freshman dormitory helps students make friends and integrate easily.",
                "example_vi": "Sống trong ký túc xá sinh viên năm nhất giúp sinh viên kết bạn và hòa nhập dễ dàng.",
                "hint": "A large bedroom for a number of people in a school or institution."
            },
            {
                "word": "academic",
                "meaning": "thuộc học thuật, học viện (tính từ)",
                "image": "📚",
                "example": "The academic journal publishes peer-reviewed research papers twice a month.",
                "example_vi": "Tạp chí học thuật xuất bản các bài báo nghiên cứu được bình duyệt từ chuyên gia hai lần một tháng.",
                "hint": "Relating to education and scholarship."
            },
            {
                "word": "assignment",
                "meaning": "bài tập về nhà, nhiệm vụ phân công (danh từ)",
                "image": "📝",
                "example": "The physics teacher gave us a challenging research assignment due next Monday.",
                "example_vi": "Giáo viên vật lý định cho chúng tôi một bài tập nghiên cứu đầy thử thách hạn chót thứ Hai tới.",
                "hint": "A piece of work or job that someone is given to do."
            },
            {
                "word": "lecture",
                "meaning": "bài giảng, thuyết trình (danh từ / động từ)",
                "image": "🗣️",
                "example": "The guest speaker delivered an interesting lecture on ancient Mayan astronomy.",
                "example_vi": "Diễn giả khách mời đã trình bày một bài thuyết trình thú vị về thiên văn học Maya cổ đại.",
                "hint": "An educational talk to an audience, especially to students in a university."
            }
        ]
    }
]

# Define TOEIC corporate word lists with handcrafted context-aware sentences
TOEIC_TOPICS = [
    {
        "id": "toeic_office",
        "name": "Office Communications",
        "name_vi": "Giao tiếp Văn phòng",
        "icon": "💼",
        "words": [
            {
                "word": "memo",
                "meaning": "thông báo nội bộ (danh từ)",
                "image": "📄",
                "example": "The HR department sent out a company-wide memo detailing the new dress code.",
                "example_vi": "Phòng nhân sự đã gửi một thông báo nội bộ toàn công ty chi tiết về quy định trang phục mới.",
                "hint": "A written proposal or reminder in a business environment."
            },
            {
                "word": "agenda",
                "meaning": "chương trình nghị sự, lịch trình họp (danh từ)",
                "image": "📅",
                "example": "We should review the group agenda before the marketing meeting begins.",
                "example_vi": "Chúng ta nên xem xét kỹ chương trình nghị sự của nhóm trước khi cuộc họp tiếp thị bắt đầu.",
                "hint": "A list of items to be discussed at a formal meeting."
            },
            {
                "word": "collaborate",
                "meaning": "hợp tác (động từ)",
                "image": "🤝",
                "example": "Our design and development teams collaborate to build beautiful user interfaces.",
                "example_vi": "Các đội ngũ thiết kế và phát triển của chúng tôi hợp tác để xây dựng giao diện người dùng đẹp mắt.",
                "hint": "Work jointly on an activity, especially to produce or create something."
            },
            {
                "word": "extension",
                "meaning": "số máy lẻ, sự mở rộng (danh từ)",
                "image": "📞",
                "example": "Please dial extension 402 to reach the customer finance support representative directly.",
                "example_vi": "Vui lòng gọi số máy lẻ 402 để kết nối trực tiếp với đại diện hỗ trợ tài chính khách hàng.",
                "hint": "An additional telephone connected to a main line / an expansion of time."
            },
            {
                "word": "correspond",
                "meaning": "trao đổi thư từ, liên lạc (động từ)",
                "image": "✉️",
                "example": "We correspond with our international regional sales branches daily via secure email.",
                "example_vi": "Chúng tôi trao đổi thư từ liên lạc hàng ngày với các chi nhánh bán hàng khu vực quốc tế qua email bảo mật.",
                "hint": "Communicate by exchanging letters, memos, or emails."
            },
            {
                "word": "archive",
                "meaning": "kho lưu trữ, lưu trữ (danh từ / động từ)",
                "image": "📦",
                "example": "Please register and archive old bookkeeping records in the secure basement facility.",
                "example_vi": "Vui lòng đăng ký và lưu trữ các hồ sơ kế toán cũ trong cơ sở tầng hầm an toàn.",
                "hint": "A collection of historical documents or records / storing old files."
            },
            {
                "word": "teleconference",
                "meaning": "hội nghị truyền hình từ xa (danh từ / động từ)",
                "image": "📡",
                "example": "The executive board scheduled a teleconference to discuss the merger with Japanese clients.",
                "example_vi": "Ban điều hành đã lên lịch một cuộc họp từ xa qua điện thoại để thảo luận về việc sáp nhập với khách hàng Nhật Bản.",
                "hint": "A conference with participants in different locations linked by telecommunication."
            },
            {
                "word": "bulletin",
                "meaning": "bản tin, thông báo nhanh (danh từ)",
                "image": "📝",
                "example": "Remember to pin the local office safety bulletin onto the lobby announcement board.",
                "example_vi": "Hãy nhớ ghim bản tin an toàn văn phòng địa phương lên bảng thông báo ở sảnh chờ.",
                "hint": "A brief public notice of an event, investigation, or official matter."
            },
            {
                "word": "workstation",
                "meaning": "máy trạm, vị trí làm việc (danh từ)",
                "image": "💻",
                "example": "IT support set up a dual-monitor computer workstation for the new senior accountant.",
                "example_vi": "Bộ phận hỗ trợ CNTT đã thiết lập vị trí máy trạm màn hình kép cho kế toán trưởng mới.",
                "hint": "A computer intended for individual use, or a designated work area in an office."
            },
            {
                "word": "feedback",
                "meaning": "phản hồi (danh từ)",
                "image": "💬",
                "example": "Collecting consumer feedback helps us isolate and fix firmware bugs very fast.",
                "example_vi": "Thu thập phản hồi của người dùng giúp chúng tôi khoanh vùng và sửa lỗi phần sụn rất nhanh.",
                "hint": "Information about reactions to a product, a person's performance of a task."
            },
            {
                "word": "recipient",
                "meaning": "người nhận (danh từ)",
                "image": "👤",
                "example": "Confirm the billing recipient's physical address before shipping fragile cargo items.",
                "example_vi": "Xác nhận địa chỉ thực của người nhận hóa đơn trước khi vận chuyển hàng hóa dễ vỡ.",
                "hint": "A person who receives or is awarded something."
            },
            {
                "word": "dispatch",
                "meaning": "gửi đi, điều động, phái đi (động từ / danh từ)",
                "image": "🚢",
                "example": "Courier services will dispatch a motorcycle carrier to collect your signature.",
                "example_vi": "Dịch vụ chuyển phát nhanh sẽ điều động một nhân viên vận chuyển xe máy đến để lấy chữ ký của bạn.",
                "hint": "Send off to a destination or for a purpose."
            },
            {
                "word": "document",
                "meaning": "tài liệu, văn bản (danh từ / động từ)",
                "image": "📂",
                "example": "You must secure every physical legal document inside lockable filing cabinets.",
                "example_vi": "Bạn phải bảo mật mọi tài liệu pháp lý vật lý bên trong tủ tài liệu có khóa.",
                "hint": "A piece of written, printed, or electronic matter that provides information."
            },
            {
                "word": "priority",
                "meaning": "sự ưu tiên (danh từ)",
                "image": "⭐",
                "example": "Resolving customer complaint issues is our absolute number one corporate priority.",
                "example_vi": "Giải quyết các vấn đề khiếu nại của khách hàng là ưu tiên tuyệt đối số một của doanh nghiệp chúng tôi.",
                "hint": "The fact or condition of being regarded as more important than others."
            },
            {
                "word": "response",
                "meaning": "câu trả lời, phản hồi (danh từ)",
                "image": "💬",
                "example": "Our technical support guarantees a helpful response to queries within two hours.",
                "example_vi": "Đội ngũ kỹ thuật hỗ trợ chúng tôi đảm bảo có câu phản hồi hữu ích cho các thắc mắc trong vòng hai giờ.",
                "hint": "A verbal or written answer / a reaction to something."
            }
        ]
    },
    {
        "id": "toeic_market",
        "name": "Marketing & Public Relations",
        "name_vi": "Tiếp thị & Quan hệ công chúng",
        "icon": "📣",
        "words": [
            {
                "word": "brochure",
                "meaning": "tờ rơi quảng cáo, sách mỏng quảng cáo (danh từ)",
                "image": "📄",
                "example": "Our new marketing brochure showcases several of our luxury holiday tourist villas.",
                "example_vi": "Cuốn sách mỏng quảng cáo tiếp thị mới của chúng tôi giới thiệu một số biệt thự du lịch nghỉ dưỡng sang trọng.",
                "hint": "A small book or magazine containing pictures and information about a product."
            },
            {
                "word": "campaign",
                "meaning": "chiến dịch (danh từ / động từ)",
                "image": "🚀",
                "example": "The online advertising campaign increased organic site traffic by forty percent.",
                "example_vi": "Chiến dịch quảng cáo trực tuyến đã tăng lưu lượng truy cập trang web tự nhiên lên 40 phần trăm.",
                "hint": "An organized course of action to achieve a particular goal, especially in business."
            },
            {
                "word": "consumer",
                "meaning": "người tiêu dùng (danh từ)",
                "image": "🛒",
                "example": "Consumer preferences are rapidly shifting toward eco-friendly and organic grocery products.",
                "example_vi": "Thị hiếu của người tiêu dùng đang chuyển dịch nhanh chóng sang các sản phẩm tạp hóa hữu cơ thân thiện với môi trường.",
                "hint": "A person who purchases goods and services for personal use."
            },
            {
                "word": "launch",
                "meaning": "tung ra, khai trương, phát động (động từ / danh từ)",
                "image": "🚀",
                "example": "The electronics giant plan to launch its new tablet at the San Francisco seminar.",
                "example_vi": "Gã khổng lồ điện tử có kế hoạch tung ra chiếc máy tính bảng mới của mình tại hội thảo San Francisco.",
                "hint": "Start or set in motion an activity or product commercial release."
            },
            {
                "word": "endorse",
                "meaning": "khuyến nghị, quảng nghị quảng cáo, chứng thực (động từ)",
                "image": "⭐",
                "example": "Famous sports athletes are paid millions to endorse professional running shoes.",
                "example_vi": "Các vận động viên thể thao nổi tiếng được trả hàng triệu đô la để quảng nghị chứng thực cho giày chạy bộ chuyên nghiệp.",
                "hint": "Declare one's public approval or support of a product in advertising advertisements."
            },
            {
                "word": "logo",
                "meaning": "hình biểu trưng, biểu tượng thương hiệu (danh từ)",
                "image": "🏷️",
                "example": "The graphic designer crafted a simple yet highly memorable brand logo.",
                "example_vi": "Nhà thiết kế đồ họa đã tạo ra một biểu tượng thương hiệu logo đơn giản nhưng cực kỳ đáng nhớ.",
                "hint": "A symbol or other small design adopted by an organization to identify its products."
            },
            {
                "word": "wholesale",
                "meaning": "bán sỉ, bán buôn (danh từ / tính từ / phó từ)",
                "image": "🏢",
                "example": "Retail outlets buy cargo lots at wholesale prices before marking up the final prices.",
                "example_vi": "Các cửa hàng bán lẻ mua các lô hàng hóa với giá bán sỉ trước khi tăng giá bán cuối cùng.",
                "hint": "The selling of goods in large quantities to be retd by others."
            },
            {
                "word": "promote",
                "meaning": "quảng bá, thúc đẩy, thăng chức (động từ)",
                "image": "📈",
                "example": "Companies utilize social media systems to promote their seasonal discount coupons.",
                "example_vi": "Các công ty sử dụng hệ thống truyền thông xã hội để quảng bá các phiếu giảm giá theo mùa của họ.",
                "hint": "Support or actively encourage / publicize a product or feature."
            },
            {
                "word": "demographic",
                "meaning": "nhóm nhân khẩu học, đối tượng (danh từ / tính từ)",
                "image": "📊",
                "example": "Our primary marketing demographic is tech-savvy young professionals aged 20 to 35.",
                "example_vi": "Nhóm nhân khẩu học tiếp thị chính của chúng tôi là các chuyên gia trẻ hiểu biết công nghệ từ 20 đến 35 tuổi.",
                "hint": "A particular sector of a population."
            },
            {
                "word": "inventory",
                "meaning": "hàng tồn kho, bảng kiểm kê (danh từ)",
                "image": "📦",
                "example": "Store employees close the shop early to perform a complete electronic inventory count.",
                "example_vi": "Các nhân viên cửa hàng đóng cửa tiệm sớm để thực hiện một cuộc đếm kiểm kê hàng tồn kho điện tử hoàn chỉnh.",
                "hint": "A complete list of items such as property, goods in stock, or contents of a building."
            },
            {
                "word": "advertisement",
                "meaning": "mục quảng cáo, bài quảng cáo (danh từ)",
                "image": "📺",
                "example": "Pinning a graphic advertisement on high-traffic websites boosted our sales numbers.",
                "example_vi": "Ghim một bài quảng cáo đồ họa trên các trang web có lượng truy cập cao đã thúc đẩy doanh số bán hàng của chúng tôi.",
                "hint": "A notice or announcement in a public medium promoting a product, service, or event."
            },
            {
                "word": "strategy",
                "meaning": "chiến lược (danh từ)",
                "image": "💡",
                "example": "The executive board designed an aggressive marketing strategy to acquire global shares.",
                "example_vi": "Ban điều hành đã thiết kế một chiến lược tiếp thị tấn công mạnh mẽ để giành cổ phần toàn cầu.",
                "hint": "A plan of action or policy designed to achieve a major or overall aim."
            },
            {
                "word": "target",
                "meaning": "đối tượng hướng tới, mục tiêu (danh từ / động từ)",
                "image": "🎯",
                "example": "It is critical to target regional localized issues during sales communications campaigns.",
                "example_vi": "Việc hướng tới mục tiêu các vấn đề địa phương hóa khu vực trong các chiến dịch truyền thông bán hàng rất quan trọng.",
                "hint": "A person, object, or result at which an action, game, or campaign is directed."
            },
            {
                "word": "display",
                "meaning": "trưng bày, hiển thị (động từ / danh từ)",
                "image": "🖼️",
                "example": "The luxury fashion retailer created a beautiful window display in Paris.",
                "example_vi": "Nhà bán lẻ thời trang xa xỉ đã tạo ra một ô trưng bày cửa sổ tuyệt đẹp ở Paris.",
                "hint": "Show/exhibit elements for community inspection."
            },
            {
                "word": "questionnaire",
                "meaning": "bảng câu hỏi khảo sát (danh từ)",
                "image": "📝",
                "example": "Please complete this online user satisfaction questionnaire to get a ten-off coupon.",
                "example_vi": "Vui lòng hoàn thành bảng câu hỏi khảo sát mức độ hài lòng này để nhận phiếu giảm giá mười phần trăm.",
                "hint": "A set of printed or written questions with a choice of answers, devised for the purposes of a survey."
            }
        ]
    },
    {
        "id": "toeic_hr",
        "name": "Human Resources & Recruiting",
        "name_vi": "Nhân sự & Tuyển dụng",
        "icon": "👥",
        "words": [
            {
                "word": "resume",
                "meaning": "sơ yếu lý lịch (danh từ)",
                "image": "📄",
                "example": "Candidates must submit a professional resume highlighting their technical engineering experiences.",
                "example_vi": "Các ứng viên phải nộp một sơ yếu lý lịch chuyên nghiệp nêu bật kinh nghiệm kỹ thuật công trình của họ.",
                "hint": "A brief account of a person's education, qualifications, and previous experience."
            },
            {
                "word": "qualified",
                "meaning": "đủ điều kiện, đạt chuẩn (tính từ)",
                "image": "✅",
                "example": "To get hired for the manager role, you must be highly qualified in public relations fields.",
                "example_vi": "Để được tuyển dụng vào vai trò quản lý, bạn phải cực kỳ đủ điều kiện trong lĩnh vực quan hệ công chúng.",
                "hint": "Officially recognized as being trained to a particular level or competent to do something."
            },
            {
                "word": "candidate",
                "meaning": "ứng viên (danh từ)",
                "image": "👤",
                "example": "The successful candidate will demonstrate excellent bilingual English and Vietnamese skills.",
                "example_vi": "Ứng viên thành công sẽ chứng tỏ kỹ năng song ngữ tiếng Anh và tiếng Việt xuất sắc.",
                "hint": "A person who applies for a job or is nominated for an election."
            },
            {
                "word": "vacancy",
                "meaning": "vị trí trống, phòng trống (danh từ)",
                "image": "🏢",
                "example": "We have an urgent junior developer vacancy open inside our accounting department.",
                "example_vi": "Chúng tôi có một vị trí trống nhà phát triển cấp thấp khẩn cấp trong bộ phận kế toán của mình.",
                "hint": "An unoccupied position or job / unoccupied room in a boarding house."
            },
            {
                "word": "pension",
                "meaning": "lương hưu, tiền hưu trí (danh từ)",
                "image": "💰",
                "example": "Corporate employees receive a generous retirement pension plan upon reaching sixty.",
                "example_vi": "Các nhân viên doanh nghiệp nhận được kế hoạch lương hưu trí hào phóng khi đạt tuổi 60.",
                "hint": "A regular payment made during a person's retirement from an investment fund."
            },
            {
                "word": "benefit",
                "meaning": "quyền lợi, phúc lợi, lợi ích (danh từ / động từ)",
                "image": "🏥",
                "example": "The job offer includes excellent benefits such as medical insurance and flexible holidays.",
                "example_vi": "Lời đề nghị công việc bao gồm lợi ích phúc lợi tuyệt vời như bảo hiểm y tế và kỳ nghỉ linh hoạt.",
                "hint": "An advantage or profit gained from something / perks offered by a company."
            },
            {
                "word": "payroll",
                "meaning": "bảng lương, danh sách phát lương (danh từ)",
                "image": "💵",
                "example": "HR processors managed to complete the payroll checks on time despite software glitches.",
                "example_vi": "Người xử lý nhân sự đã quản lý để hoàn thành kiểm tra bảng lương đúng hạn mặc dù có lỗi phần mềm.",
                "hint": "A list of a company's employees and the amount of money they are to be paid."
            },
            {
                "word": "terminate",
                "meaning": "chấm dứt, sa thải, dừng hợp đồng (động từ)",
                "image": "❌",
                "example": "Management decided to terminate the contract of the vendor because of poor maintenance.",
                "example_vi": "Quản lý quyết định chấm dứt hợp đồng của nhà cung cấp do chế độ bảo trì kém.",
                "hint": "Bring to an end / dismiss an employee."
            },
            {
                "word": "interview",
                "meaning": "phỏng vấn (danh từ / động từ)",
                "image": "👥",
                "example": "Applicants should dress strictly in business attire for their final job interview.",
                "example_vi": "Các ứng cử viên nên ăn mặc lịch sự trong trang phục công sở cho buổi phỏng vấn việc làm cuối cùng của họ.",
                "hint": "A meeting of people face to face, especially for consultation or employment recruiting."
            },
            {
                "word": "probation",
                "meaning": "thời gian thử việc (danh từ)",
                "image": "⏳",
                "example": "Newly recruited engineers undergo a two-month probation period before receiving a full contract.",
                "example_vi": "Các kỹ sư mới được tuyển dụng trải qua thời gian thử việc hai tháng trước khi nhận hợp đồng đầy đủ.",
                "hint": "The release of an offender from detention, subject to a period of good behavior / testing time."
            },
            {
                "word": "recruit",
                "meaning": "tuyển dụng, lính mới (động từ / danh từ)",
                "image": "🏢",
                "example": "We seek to recruit talented software engineers specializing in network security algorithms.",
                "example_vi": "Chúng tôi tìm kiếm tuyển dụng các kỹ sư phần mềm tài năng chuyên về thuật toán bảo mật mạng.",
                "hint": "Enroll someone in the armed forces / hire new staff."
            },
            {
                "word": "supervisor",
                "meaning": "người giám sát (danh từ)",
                "image": "👤",
                "example": "If you need to log overtime hours, you must acquire written permission from your supervisor.",
                "example_vi": "Nếu bạn cần đăng ký số giờ làm thêm, bạn phải xin chữ ký cấp phép bằng văn bản từ người giám sát của mình.",
                "hint": "A person who stands over/supervies a person or an activity."
            },
            {
                "word": "application",
                "meaning": "đơn xin việc, ứng dụng (danh từ)",
                "image": "📝",
                "example": "Write a professional cover letter to attach with your employment application.",
                "example_vi": "Hãy viết một thư xin việc ngắn chuyên nghiệp để đ kèm đơn xin việc của bạn.",
                "hint": "A formal request to an authority for something / software program."
            },
            {
                "word": "resignation",
                "meaning": "đơn xin thôi việc, sự từ chức (danh từ)",
                "image": "📄",
                "example": "The senior marketing manager submitted his formal resignation sheet to seek other positions.",
                "example_vi": "Giám đốc tiếp thị cấp cao đã nộp đơn xin thôi việc chính thức để tìm kiếm các vị trí khác.",
                "hint": "An act of retiring or giving up a position."
            },
            {
                "word": "reference",
                "meaning": "người giới thiệu, thư giới thiệu, tham chiếu (danh từ)",
                "image": "📞",
                "example": "We requested references from her previous university professor to confirm her technical skills.",
                "example_vi": "Chúng tôi yêu cầu tài liệu thư giới thiệu từ giáo sư đại học cũ của cô ấy để xác minh kỹ năng kỹ thuật của cô ấy.",
                "hint": "A letter from a previous employer testifying to someone's ability or character."
            }
        ]
    },
    {
        "id": "toeic_finance",
        "name": "Finance, Accounting & Banking",
        "name_vi": "Tài chính, Ngân hàng & Kế toán",
        "icon": "💵",
        "words": [
            {
                "word": "audit",
                "meaning": "kiểm toán, cuộc kiểm toán (danh từ / động từ)",
                "image": "📊",
                "example": "An external accounting firm conducted an annual financial audit to ensure transparency.",
                "example_vi": "Một công ty kế toán bên ngoài đã thực hiện cuộc kiểm toán tài chính hàng năm để đảm bảo tính minh bạch.",
                "hint": "An official inspection of an individual's or organization's accounts, typically by an independent body."
            },
            {
                "word": "budget",
                "meaning": "ngân sách (danh từ / động từ)",
                "image": "💰",
                "example": "Managers must restrict department travel expenditure to meet our tight annual budget.",
                "example_vi": "Các quản lý phải hạn chế chi tiêu đi lại của bộ phận để đáp ứng ngân sách hàng năm eo hẹp của chúng tôi.",
                "hint": "An estimate of income and expenditure for a set period of time."
            },
            {
                "word": "bankrupt",
                "meaning": "phá sản (tính từ / danh từ / động từ)",
                "image": "📉",
                "example": "The retail retail supplier went bankrupt after failing to cover its immense credit debts.",
                "example_vi": "Nhà cung cấp bán lẻ đã phá sản sau khi không thể trang trải khoản nợ tín dụng khổng lồ của mình.",
                "hint": "Declared by law unable to pay outstanding debts."
            },
            {
                "word": "interest",
                "meaning": "lãi suất, sự quan tâm, lợi ích (danh từ)",
                "image": "📈",
                "example": "Savings accounts in state-directed institutions generate a stable, low annual interest payout.",
                "example_vi": "Tài khoản tiết kiệm trong tổ chức do nhà nước quản lý tạo ra khoản thanh toán lãi suất hàng năm thấp và ổn định.",
                "hint": "Money pd regularly at a particular rate for the use of money lent."
            },
            {
                "word": "transaction",
                "meaning": "giao dịch (danh từ)",
                "image": "💵",
                "example": "The credit card holder received an immediate mobile notification about the transaction.",
                "example_vi": "Chủ sở hữu thẻ tín dụng đã nhận được thông báo di động ngay lập tức về giao dịch vừa xảy ra.",
                "hint": "An instance of buying or selling something; a business deal."
            },
            {
                "word": "invoice",
                "meaning": "hóa đơn thanh toán (danh từ / động từ)",
                "image": "📄",
                "example": "Please send the client an official legal invoice detailing the cost of shipping supplies.",
                "example_vi": "Vui lòng gửi cho khách hàng một hóa đơn thanh toán chính thức chi tiết chi phí vật tư vận chuyển.",
                "hint": "A list of goods sent or services provided, with a statement of the sum due for these."
            },
            {
                "word": "portfolio",
                "meaning": "danh mục đầu tư, hồ sơ năng lực (danh từ)",
                "image": "📂",
                "example": "A diversified stock portfolio minimizes financial losses during localized market downturn recessions.",
                "example_vi": "Một danh mục đầu tư cổ phiếu đa dạng hóa giảm thiểu tổn thất tài chính trong các thời kỳ suy thoái thị trường địa phương.",
                "hint": "A range of investments held by a person or organization."
            },
            {
                "word": "revenue",
                "meaning": "doanh thu (danh từ)",
                "image": "📈",
                "example": "The software giant generated bumper revenue following the release of its computer operating codes.",
                "example_vi": "Gã khổng lồ phần mềm đã tạo ra doanh thu kỷ lục sau khi phát hành các mã điều hành máy tính của mình.",
                "hint": "Income, especially when of a company or organization and of a substantial nature."
            },
            {
                "word": "ledger",
                "meaning": "sổ cái kế toán (danh từ)",
                "image": "📖",
                "example": "Junior bookkeepers record debit and credit transactions manually inside the physical database ledger.",
                "example_vi": "Các nhân viên ghi sổ cấp thấp ghi nhận các giao dịch nợ và có theo cách thủ công bên trong sổ cái kế toán vật lý.",
                "hint": "A book or other collection of financial accounts of a particular type."
            },
            {
                "word": "credit",
                "meaning": "tín dụng, lòng tin (danh từ / động từ)",
                "image": "💳",
                "example": "Having excellent credit status enables startups to borrow investment capital at lower rates.",
                "example_vi": "Có trạng thái tín dụng xuất sắc cho phép các công ty khởi nghiệp vay vốn đầu tư với lãi suất thấp hơn.",
                "hint": "The ability of a customer to obtain goods or services before payment, based on the trust."
            },
            {
                "word": "asset",
                "meaning": "tài sản, tài sản quý (danh từ)",
                "image": "🏢",
                "example": "Commercial property and industrial warehouses are valuable corporate assets.",
                "example_vi": "Bất động sản thương mại và nhà kho công nghiệp là những tài sản doanh nghiệp có giá trị.",
                "hint": "An item of property owned by a person or company, regarded as having value."
            },
            {
                "word": "liability",
                "meaning": "khoản nợ phải trả, trách nhiệm pháp lý (danh từ)",
                "image": "💸",
                "example": "Outstanding invoice payments and employee payroll checks are listed under short-term liabilities.",
                "example_vi": "Các khoản hóa đơn thanh toán tồn đọng và chi trả lương cho nhân viên được liệt kê dưới mục nợ phải trả ngắn hạn.",
                "hint": "The state of being responsible for something, especially by law / a financial debt."
            },
            {
                "word": "deposit",
                "meaning": "tiền đặt cọc, tiền gửi ngân hàng (danh từ / động từ)",
                "image": "💵",
                "example": "The tenant pd a security deposit equivalent to one month's lease to secure the room.",
                "example_vi": "Người thuê nhà đã trả một khoản tiền đặt cọc bảo đảm tương đương với một tháng tiền thuê để giữ phòng.",
                "hint": "A sum of money kept in a bank account, or pd as a first installment on a purchase."
            },
            {
                "word": "referee",
                "meaning": "người giới thiệu, trọng tài (danh từ)",
                "image": "👤",
                "example": "The banking candidate listed three distinguished financial referees on her application form.",
                "example_vi": "Ứng cử viên ngành ngân hàng đã liệt kê ba người tham chiếu tài chính xuất sắc trên đơn xin việc của mình.",
                "hint": "A person who can testify to your character or skills (in professional applications)."
            },
            {
                "word": "reconcile",
                "meaning": "đối chiếu, hòa giải (động từ)",
                "image": "⚖️",
                "example": "Accountants must reconcile monthly bank statements with internal ledger balances closely.",
                "example_vi": "Kế toán phải đối chiếu bảng sao kê ngân hàng hàng tháng với số dư sổ cái nội bộ một cách chặt chẽ.",
                "hint": "Make financial accounts consistent with another / settle relationships."
            }
        ]
    },
    {
        "id": "toeic_travel",
        "name": "Travel & Hotel Hospitality",
        "name_vi": "Du lịch & Khách sạn",
        "icon": "✈️",
        "words": [
            {
                "word": "itinerary",
                "meaning": "lịch trình chuyến đi (danh từ)",
                "image": "🗺️",
                "example": "The travel tourist assistant emailed a complete daily itinerary including domestic flights.",
                "example_vi": "Trợ lý du lịch lữ hành đã gửi email một lịch trình chuyến đi hàng ngày đầy đủ bao gồm cả các chuyến bay nội địa.",
                "hint": "A planned route or journey."
            },
            {
                "word": "boarding",
                "meaning": "sự lên tàu/lên máy bay (danh từ / tính từ)",
                "image": "✈️",
                "example": "Passengers must exhibit their physical boarding pass to airport staff at the terminal gate.",
                "example_vi": "Hành khách phải xuất trình thẻ lên máy bay vật lý cho nhân viên sân bay tại cửa nhà ga.",
                "hint": "The action of getting on a ship, plane, or train."
            },
            {
                "word": "hospitality",
                "meaning": "lòng hiếu khách, ngành nhà hàng khách sạn (danh từ)",
                "image": "🏨",
                "example": "Five-star hotel resorts are celebrated internationally for their unmatched hospitality.",
                "example_vi": "Các khu nghỉ dưỡng khách sạn năm sao nổi tiếng quốc tế vì lòng hiếu khách chưa từng có của họ.",
                "hint": "The friendly and generous reception and entertainment of guests."
            },
            {
                "word": "concierge",
                "meaning": "quầy phục vụ khách, người hỗ trợ khách hàng (danh từ)",
                "image": "👤",
                "example": "Ask the front concierge desk to make dinner reservations at a nearby seafood eatery.",
                "example_vi": "Hãy hỏi quầy phục vụ khách ở phía trước để đặt chỗ ăn tối tại một quán ăn hải sản gần đó.",
                "hint": "A hotel employee whose job is to assist guests by booking tours, making theatre reservations."
            },
            {
                "word": "delayed",
                "meaning": "bị trì hoãn, trễ giờ (tính từ / động từ)",
                "image": "⏳",
                "example": "Our connecting flight to Tokyo was severely delayed because of heavy winter storms.",
                "example_vi": "Chuyến bay kết nối của chúng tôi đến Tokyo đã bị trì hoãn nghiêm trọng do bão bão tuyết mùa đông lớn.",
                "hint": "Late or postponed."
            },
            {
                "word": "accommodation",
                "meaning": "chỗ ở, phòng nghỉ (danh từ)",
                "image": "🏨",
                "example": "The business conference package covers physical hotel accommodation and buffet dinner fees.",
                "example_vi": "Gói hội nghị kinh doanh đài thọ hoàn toàn chỗ ở phòng nghỉ khách sạn và chi phí tiệc ăn tối buffet.",
                "hint": "Temporary lodging / room and food in a hotel environment."
            },
            {
                "word": "reservation",
                "meaning": "sự đặt chỗ trước (danh từ)",
                "image": "📞",
                "example": "It is critical to call ahead to guarantee a dinner table reservation during weekend hours.",
                "example_vi": "Quan trọng là cần gọi điện trước để bảo đảm sự đặt chỗ trước bàn ăn tối trong các giờ cuối tuần.",
                "hint": "An arrangement to have something kept for a particular person's use."
            },
            {
                "word": "excursion",
                "meaning": "chuyến tham quan ngắn, dã ngoại (danh từ)",
                "image": "🚌",
                "example": "Guided tours organize an early morning excursion to explore ancient temple ruins.",
                "example_vi": "Các chuyến tham quan có hướng dẫn tổ chức một chuyến dã ngoại ngắn buổi sáng để khám phá tàn tích đền cổ.",
                "hint": "A short journey or trip, especially one taken as a leisure activity."
            },
            {
                "word": "luggage",
                "meaning": "hành lý (danh từ)",
                "image": "🧳",
                "example": "Airport clerks weigh passengers' luggage to check if it exceeds standard free cargo weights.",
                "example_vi": "Các nhân viên sân bay cân hành lý của hành khách để kiểm tra xem nó có vượt quá hạn mức cân nặng miễn phí không.",
                "hint": "Suitcases and bags containing a traveler's belongings."
            },
            {
                "word": "terminal",
                "meaning": "nhà ga sân bay/xe khách, thiết bị cuối (danh từ / tính từ)",
                "image": "🚇",
                "example": "A shuttle bus connects the international terminal directly to local train locations.",
                "example_vi": "Một chuyến xe đưa đón kết nối nhà ga quốc tế trực tiếp với các vị trí ga tàu hỏa địa phương.",
                "hint": "The end of a railway or other transport line / airport station building."
            },
            {
                "word": "destination",
                "meaning": "điểm đến (danh từ)",
                "image": "🏖️",
                "example": "Da Nang remains a highly popular vacation destination for domestic and foreign travelers.",
                "example_vi": "Đà Nẵng vẫn là điểm đến kỳ nghỉ dưỡng vô cùng nổi tiếng đối với khách du lịch trong và ngoài nước.",
                "hint": "The place to which someone or something is going or being sent."
            },
            {
                "word": "departure",
                "meaning": "giờ khởi hành, sự khởi hành (danh từ)",
                "image": "🛫",
                "example": "Confirm your airport boarding gate time on the giant digital departures board.",
                "example_vi": "Xác nhận giờ khởi hành lên máy bay tại cổng sân bay trên bảng thông tin khởi hành kỹ thuật số khổng lồ.",
                "hint": "The action of leaving, especially to start a journey."
            },
            {
                "word": "ticket",
                "meaning": "vé (danh từ / động từ)",
                "image": "🎟️",
                "example": "I purchased an electronic ticket via my mobile wallet helper to avoid waiting lines.",
                "example_vi": "Tôi đã mua một chiếc vé điện tử qua ứng dụng ví di động của mình để tránh phải xếp hàng chờ đợi.",
                "hint": "A piece of paper or electronic document showing that the holder is entitled to something."
            },
            {
                "word": "shuttle",
                "meaning": "xe buýt đưa đón chặng ngắn (danh từ / động từ)",
                "image": "🚌",
                "example": "The hotel organizes a complimentary shuttle to transport guests straight to the beach.",
                "example_vi": "Khách sạn tổ chức một chuyến xe buýt đưa đón miễn phí để chở khách thẳng tới sau bãi biển.",
                "hint": "A form of transport that travels regularly between two places."
            },
            {
                "word": "check-in",
                "meaning": "thủ tục nhận phòng/lên máy bay, sự đăng nhập (danh từ / động từ)",
                "image": "🔑",
                "example": "The standard hotel check-in hour begins at two in the afternoon.",
                "example_vi": "Giờ làm thủ tục nhận phòng khách sạn tiêu chuẩn bắt đầu vào lúc hai giờ chiều.",
                "hint": "The act of registering one's arrival, especially at an airport or hotel."
            }
        ]
    },
    {
        "id": "toeic_health",
        "name": "Health, Medical & Safety",
        "name_vi": "Sức khỏe & An toàn lao động",
        "icon": "🏥",
        "words": [
            {
                "word": "prescription",
                "meaning": "đơn thuốc (danh từ)",
                "image": "💊",
                "example": "You must display a valid doctor's prescription before purchasing strong antibiotic pills.",
                "example_vi": "Bạn phải trình một đơn thuốc hợp lệ của bác sĩ trước khi mua các loại thuốc kháng sinh mạnh.",
                "hint": "An instruction written by a medical practitioner that authorizes a patient to be provided with a medicine."
            },
            {
                "word": "physical",
                "meaning": "thuộc cơ thể, cuộc kiểm tra sức khỏe tổng quát (tính từ / danh từ)",
                "image": "🏋️",
                "example": "Corporate safety regulations mandate that all candidates undergo an annual physical exam.",
                "example_vi": "Các quy định an toàn của doanh nghiệp bắt buộc tất cả các ứng cử viên phải trải qua một cuộc kiểm tra sức khỏe tổng quát hàng năm.",
                "hint": "Relating to the body as opposed to the mind / general medical checkup."
            },
            {
                "word": "clinic",
                "meaning": "phòng khám (danh từ)",
                "image": "🏥",
                "example": "The community clinic provides basic dental care and vaccines at near-free costs.",
                "example_vi": "Phòng khám cộng đồng cung cấp dịch vụ chăm sóc răng miệng cơ bản và vắc-xin với chi phí gần như miễn phí.",
                "hint": "An establishment or hospital department where outpatients are given medical treatment."
            },
            {
                "word": "symptom",
                "meaning": "triệu chứng bệnh (danh từ)",
                "image": "🌡️",
                "example": "A persistent dry cough is a classic clinical symptom of common viral lung infections.",
                "example_vi": "Ho khan kéo dài là triệu chứng lâm sàng kinh điển của tình trạng nhiễm trùng phổi do virus thông thường.",
                "hint": "A physical or mental feature which is regarded as indicating a condition of disease."
            },
            {
                "word": "evacuation",
                "meaning": "sự sơ tán, sự rút lui (danh từ)",
                "image": "🚨",
                "example": "Fire safety officers conducted a complete corporate building evacuation drill yesterday.",
                "example_vi": "Các nhân viên an toàn phòng cháy chữa cháy đã tiến hành một buổi diễn tập sơ tán tòa nhà doanh nghiệp hoàn chỉnh vào hôm qua.",
                "hint": "The action of evacuating a person or a place of danger."
            },
            {
                "word": "hygiene",
                "meaning": "vệ sinh, vệ sinh phòng dịch (danh từ)",
                "image": "🧼",
                "example": "Washing hands regularly maintains basic corporate restaurant hygiene safety benchmarks.",
                "example_vi": "Rửa tay thường xuyên giúp duy trì các tiêu chuẩn về an toàn vệ sinh cơ bản cho nhà hàng thuộc tập đoàn.",
                "hint": "Conditions or practices conducive to maintaining health and preventing disease, especially through cleanliness."
            },
            {
                "word": "workspace",
                "meaning": "vị trí, không gian làm việc (danh từ)",
                "image": "💻",
                "example": "Keeping a tidy, clean workspace limits mental stress and increases creative productivity.",
                "example_vi": "Giữ gìn không gian làm việc gọn gàng, sạch sẽ giúp giảm căng thẳng tinh thần và tăng năng suất sáng tạo.",
                "hint": "The area compiled for a single employee workstation."
            },
            {
                "word": "wellness",
                "meaning": "sự khỏe mạnh, thể chất cân bằng (danh từ)",
                "image": "🍀",
                "example": "Our corporate wellness program includes complimentary gym passes and nutrition advice classes.",
                "example_vi": "Chương trình chăm sóc sức khỏe thể chất cân bằng của doanh nghiệp chúng tôi bao gồm thẻ tập thể dục miễn phí và các lớp tư vấn thiết thực về dinh dưỡng.",
                "hint": "The state of being in good health, especially as an actively pursued goal."
            },
            {
                "word": "therapist",
                "meaning": "nhà vật lý trị liệu, bác sĩ trị liệu (danh từ)",
                "image": "👤",
                "example": "The sports therapist designed a personalized training routine to heal the athlete's knee tendon.",
                "example_vi": "Bác sĩ trị liệu thể thao đã thiết kế một bài tập cá nhân hóa nhằm chữa lành gân kheo đầu gối của vận động viên.",
                "hint": "A person skilled in a particular type of therapy."
            },
            {
                "word": "insurance",
                "meaning": "bảo hiểm (danh từ)",
                "image": "🛡️",
                "example": "Excellent medical insurance covers hospital lodging bills and dental operations completely.",
                "example_vi": "Chương trình bảo hiểm y tế xuất sắc đài thọ hoàn toàn các hóa đơn nằm viện và phẫu thuật răng miệng.",
                "hint": "An arrangement by which a company or state guarantees compensation for specified loss, damage, illness."
            },
            {
                "word": "hazard",
                "meaning": "mối nguy hiểm, rủi ro (danh từ / động từ)",
                "image": "⚠️",
                "example": "Unplugging overheating machines early avoids major electrical hazard events inside factories.",
                "example_vi": "Rút phích cắm các loại máy quá nóng sớm giúp tránh các sự cố nguy hiểm về điện nghiêm trọng bên trong nhà máy.",
                "hint": "A danger or risk."
            },
            {
                "word": "emergency",
                "meaning": "trường hợp khẩn cấp (danh từ / tính từ)",
                "image": "🚨",
                "example": "Keep the designated emergency exit stairs completely clear of packaging crates.",
                "example_vi": "Hãy giữ cho lối rẽ cầu thang thoát hiểm khẩn cấp được chỉ định hoàn toàn trống sạch khỏi các thùng các-tông.",
                "hint": "A serious, unexpected, and often dangerous situation requiring immediate action."
            },
            {
                "word": "prevention",
                "meaning": "sự phòng ngừa, ngăn chặn (danh từ)",
                "image": "🛡️",
                "example": "Regular machinery maintenance is the ultimate key to industrial hazard prevention.",
                "example_vi": "Bảo trì máy móc thường xuyên là chiếc chìa khóa quan trọng nhất để phòng ngừa các mối nguy hiểm công nghiệp.",
                "hint": "The action of stopping something from happening or arising."
            },
            {
                "word": "condition",
                "meaning": "điều kiện, tình trạng sức khỏe (danh từ / động từ)",
                "image": "📊",
                "example": "The physical clinic reported that the worker is in excellent medical condition.",
                "example_vi": "Phòng khám kiểm tra thể chất báo cáo rằng công nhân này đang có điều kiện tình trạng sức khỏe tuyệt vời.",
                "hint": "The state of something with regard to its appearance, quality, or working order."
            },
            {
                "word": "medicine",
                "meaning": "y học, thuốc uống (danh từ)",
                "image": "💊",
                "example": "Traditional natural medicine uses ginger roots to settle stomach upset symptoms quickly.",
                "example_vi": "Y học tự nhiên truyền thống sử dụng củ gừng để làm dịu các triệu chứng rối loạn dạ dày nhanh chóng.",
                "hint": "The science or practice of the diagnosis, treatment, and prevention of disease / pharmaceutical pills."
            }
        ]
    },
    {
        "id": "toeic_logistics",
        "name": "Logistics & Purchasing",
        "name_vi": "Vận chuyển & Kho vận",
        "icon": "🚢",
        "words": [
            {
                "word": "cargo",
                "meaning": "hàng hóa vận chuyển (danh từ)",
                "image": "🚢",
                "example": "The massive freight vessel carried thousands of cargo containers from Shanghai.",
                "example_vi": "Con tàu chở hàng khổng lồ đã vận chuyển hàng ngàn container hàng hóa từ Thượng Hải.",
                "hint": "Goods carried on a ship, aircraft, or motor vehicle."
            },
            {
                "word": "carrier",
                "meaning": "hãng vận tải, người vận chuyển (danh từ)",
                "image": "🚚",
                "example": "We contracted an international logistics carrier to handle container shipments to Europe.",
                "example_vi": "Chúng tôi đã ký hợp đồng với một hãng vận tải hậu cần quốc tế để xử lý các chuyến hàng container đến châu Âu.",
                "hint": "A person or company that undertakes the professional professional transport of goods, passengers."
            },
            {
                "word": "wholesale",
                "meaning": "bán buôn, bán sỉ (danh từ / tính từ)",
                "image": "🏢",
                "example": "Buying wholesale units directly reduces the cost of restaurant ingredients enormously.",
                "example_vi": "Mua các đơn vị bán buôn trực tiếp làm giảm thiểu đáng kể chi phí nguyên liệu nhà hàng.",
                "hint": "The business of selling goods in large quantities at low prices."
            },
            {
                "word": "shipment",
                "meaning": "lô hàng vận chuyển, sự gửi hàng (danh từ)",
                "image": "📦",
                "example": "The factory supervisor confirmed that the raw steel shipment was delivered on time.",
                "example_vi": "Giám sát viên nhà máy xác nhận rằng lô hàng thép thô đã được giao đúng hẹn.",
                "hint": "A quantity of goods shipped; a cargo."
            },
            {
                "word": "tariff",
                "meaning": "thuế quan, biểu thuế xuất nhập khẩu (danh từ)",
                "image": "💸",
                "example": "Imposing a strict import tariff protected domestic manufacturers but raised retail prices.",
                "example_vi": "Việc áp dụng mức thuế quan nhập khẩu nghiêm ngặt đã bảo vệ các nhà sản xuất nội địa nhưng làm tăng giá bán lẻ.",
                "hint": "A tax or duty to be pd on a particular class of imports or exports."
            },
            {
                "word": "courier",
                "meaning": "nhân viên chuyển phát nhanh (danh từ)",
                "image": "🏍️",
                "example": "We sent the original signed building contract via an express courier yesterday morning.",
                "example_vi": "Chúng tôi đã gửi bản hợp đồng xây dựng có chữ ký gốc qua một nhân viên chuyển phát nhanh sáng hôm qua.",
                "hint": "A messenger who transports goods, legal archives, documents, packages."
            },
            {
                "word": "warehouse",
                "meaning": "nhà kho (danh từ / động từ)",
                "image": "🏢",
                "example": "Forklifts transport shipping crates safely inside our modern commercial warehouse.",
                "example_vi": "Xe nâng bốc xếp các thùng hàng vận chuyển một cách an toàn bên trong nhà kho thương mại hiện đại của chúng tôi.",
                "hint": "A large building where raw materials or manufactured goods may be stored before export."
            },
            {
                "word": "dispatch",
                "meaning": "gửi đi, điều vận, giải quyết nhanh (động từ / danh từ)",
                "image": "📦",
                "example": "Logistics managers must dispatch custom cargo sets within twenty-four hours.",
                "example_vi": "Các quản lý hậu cần phải gửi đi các lô hàng hàng hóa tùy chỉnh trong vòng hai mươi tư giờ.",
                "hint": "Send off to a destination or for a purpose."
            },
            {
                "word": "fragile",
                "meaning": "dễ vỡ, mỏng manh (tính từ)",
                "image": "🥛",
                "example": "Attach 'Fragile' warning stickers onto boxes containing glass culinary dining cups.",
                "example_vi": "Hãy dán nhãn cảnh báo 'Dễ vỡ' lên các hộp giấy chứa cốc chén thủy tinh ăn uống.",
                "hint": "Easily broken or damaged."
            },
            {
                "word": "tracking",
                "meaning": "theo dõi, định vị lịch trình (danh từ / tính từ)",
                "image": "📍",
                "example": "Customers utilize their online tracking code to review delivery updates in real-time.",
                "example_vi": "Khách hàng sử dụng mã định vị theo dõi trực tuyến để kiểm tra cập nhật giao hàng theo thời gian thực.",
                "hint": "The monitoring of cargo paths / recording locations of shipment packages."
            },
            {
                "word": "receipt",
                "meaning": "hóa đơn nhận tiền, biên lai (danh từ)",
                "image": "📄",
                "example": "Please present your purchase receipt to process product refund claims at customer service.",
                "example_vi": "Vui lòng xuất trình biên lại hóa đơn mua hàng để xử lý các yêu cầu hoàn tiền sản phẩm tại quầy dịch vụ khách hàng.",
                "hint": "A written statement confirming that money or goods have been received."
            },
            {
                "word": "delivery",
                "meaning": "sự giao hàng (danh từ)",
                "image": "📦",
                "example": "Home delivery charges are waived for orders exceeding eighty dollars in value.",
                "example_vi": "Chi phí phí giao hàng tận nhà được miễn cho các đơn hàng vượt quá giá trị tám mươi đô la.",
                "hint": "The carrying and turning over of letters, goods, or packages to a recipient."
            },
            {
                "word": "transport",
                "meaning": "vận tải, giao thông (danh từ / động từ)",
                "image": "🚚",
                "example": "Public transport networks reduce automobile emissions in crowded metropolitan zones.",
                "example_vi": "Các mạng lưới giao thông vận tải công cộng cắt giảm lượng khí thải ô tô trong các vùng đô thị đông đúc.",
                "hint": "Take or carry people or goods from one place to another."
            },
            {
                "word": "order",
                "meaning": "đơn đặt hàng, trật tự, gọi món (danh từ / động từ)",
                "image": "🛒",
                "example": "The purchaser placed an online order for twenty new computer hardware monitors.",
                "example_vi": "Nhân viên mua hàng đã đặt một đơn đặt hàng trực tuyến cho hai mươi màn hình phần cứng máy tính mới.",
                "hint": "An authoritative command / request for supply of goods."
            },
            {
                "word": "supply",
                "meaning": "nguồn cung, cung cấp (danh từ / động từ)",
                "image": "📦",
                "example": "The office manager ordered a semester supply of printing paper and staples.",
                "example_vi": "Trưởng phòng văn phòng đã đặt một lượng nguồn cung giấy in và ghim dập cho cả một học kỳ.",
                "hint": "Make something available to someone / a stock of a resource."
            }
        ]
    },
    {
        "id": "toeic_restaurant",
        "name": "Restaurants, Dining & Banquets",
        "name_vi": "Nhà hàng & Tiệc chiêu đãi",
        "icon": "🍔",
        "words": [
            {
                "word": "culinary",
                "meaning": "thuộc bếp núc, nghệ thuật ẩm thực (tính từ)",
                "image": "🍳",
                "example": "The executive chef trained at a distinguished culinary art institute in Rome.",
                "example_vi": "Đầu bếp trưởng điều hành đã học tập tại một viện nghệ thuật ẩm thực xuất sắc ở Rome.",
                "hint": "Of or relating to rural/specialized cooking or the kitchen."
            },
            {
                "word": "catering",
                "meaning": "dịch vụ ăn uống, phục vụ tiệc (danh từ)",
                "image": "🍽️",
                "example": "The company hired a local catering vendor to organize the annual wedding banquet.",
                "example_vi": "Công ty đã thuê một nhà cung cấp dịch vụ phục vụ tiệc địa phương để tổ chức tiệc cưới hàng năm.",
                "hint": "The provision of food and drink at a social event or other gathering."
            },
            {
                "word": "reservation",
                "meaning": "sự đặt chỗ trước (danh từ)",
                "image": "📞",
                "example": "Our online reservation calendar allows guests to schedule custom table seating slots.",
                "example_vi": "Lịch đặt chỗ trước trực tuyến của chúng tôi cho phép khách tự chọn các khung giờ đặt bàn ăn tùy chỉnh.",
                "hint": "An arrangement to have something kept for a particular person's use."
            },
            {
                "word": "recipe",
                "meaning": "công thức làm món ăn (danh từ)",
                "image": "📖",
                "example": "The baker preserves a secret family recipe to make light, crispy croissants.",
                "example_vi": "Thợ làm bánh lưu giữ một công thức gia đình bí mật để làm ra những chiếc sừng bò nhẹ và giòn nở.",
                "hint": "A set of instructions for preparing a particular dish, including a list of the ingredients required."
            },
            {
                "word": "gourmet",
                "meaning": "người sành ăn, món ăn cao cấp sành điệu (danh từ / tính từ)",
                "image": "🍷",
                "example": "The hotel restaurant serves a delicious three-course gourmet lunch package.",
                "example_vi": "Nhà hàng khách sạn phục vụ một gói bữa trưa ba món sành ăn ngon miệng.",
                "hint": "Relating to high-quality or exotic food, or a person who understands exquisite dining."
            },
            {
                "word": "chef",
                "meaning": "đầu bếp, bếp trưởng (danh từ)",
                "image": "👨‍🍳",
                "example": "The pastry chef decorated the luxury anniversary chocolate cake beautifully.",
                "example_vi": "Đầu bếp bánh ngọt đã trang trí chiếc bánh sô-cô-la kỷ niệm sang trọng tuyệt đẹp.",
                "hint": "A professional cook, typically the chief cook in a restaurant."
            },
            {
                "word": "seating",
                "meaning": "sự sắp xếp chỗ ngồi, chỗ ngồi (danh từ)",
                "image": "🪑",
                "example": "Our wedding banquet hall has comfortable seating capacity for three hundred guests.",
                "example_vi": "Phòng tổ chức tiệc cưới của chúng tôi có sức chứa chỗ ngồi thoải mái cho ba trăm quan khách.",
                "hint": "The arrangement of seats in a building, vehicle / collective seats."
            },
            {
                "word": "dietary",
                "meaning": "thuộc chế độ ăn uống, kiêng khem (tính từ / danh từ)",
                "image": "🥗",
                "example": "Please notify the catering staff about any specific dietary restrictions or allergies.",
                "example_vi": "Vui lòng thông báo cho nhân viên phục vụ tiệc về bất kỳ hạn chế ăn kiêng hoặc dị ứng cụ thể nào.",
                "hint": "Relating to diets, food rules, or nutritional patterns."
            },
            {
                "word": "gratuity",
                "meaning": "tiền boa, tiền thưởng dịch vụ (danh từ)",
                "image": "💵",
                "example": "For group parties exceeding eight guests, an eighteen percent gratuity is added directly.",
                "example_vi": "Đối với các nhóm họp tiệc vượt quá tám người, một khoản tiền boa mười tám phần trăm được cộng trực tiếp.",
                "hint": "A tip given to a waiter, taxicab driver, or other service worker."
            },
            {
                "word": "banquet",
                "meaning": "bữa tiệc lớn, yến tiệc (danh từ / động từ)",
                "image": "🍽️",
                "example": "The prime minister hosted a formal state banquet to honor visiting foreign dignitaries.",
                "example_vi": "Thủ tướng đã chủ trì một bữa yến tiệc nhà nước trang trọng để vinh danh các quan chức cấp cao nước ngoài đến thăm.",
                "hint": "An elaborate and formal evening meal for many people."
            },
            {
                "word": "menu",
                "meaning": "thực đơn (danh từ)",
                "image": "📜",
                "example": "The restaurant updated its autumn menu to include organic pumpkin soup.",
                "example_vi": "Nhà hàng đã cập nhật thực đơn mùa thu của mình bao gồm món súp bí đỏ hữu cơ.",
                "hint": "A list of dishes available in a restaurant."
            },
            {
                "word": "beverage",
                "meaning": "đồ uống, thức uống (danh từ)",
                "image": "🍹",
                "example": "Alcohols and soft carbonated sodas are list under beverage charges.",
                "example_vi": "Các loại rượu bia và soda sủi bọt có ga khác được liệt kê trong phần chi phí đồ uống.",
                "hint": "A drink other than water."
            },
            {
                "word": "dining",
                "meaning": "sự ăn uống, phòng ăn (danh từ / tính từ)",
                "image": "🍽️",
                "example": "We enjoyed a lovely fine dining experience at the ocean-front hotel.",
                "example_vi": "Chúng tôi đã tận hưởng một trải nghiệm ăn uống cao cấp tuyệt vời tại khách sạn trước biển.",
                "hint": "The activity of eating dinner / related to meal environments."
            },
            {
                "word": "buffet",
                "meaning": "tiệc đứng, tiệc tự chọn (danh từ)",
                "image": "🥗",
                "example": "The breakfast buffet offers a wonderful selection of pastries and fresh fruits.",
                "example_vi": "Quầy tiệc đứng buffet ăn sáng cung cấp một sự lựa chọn tuyệt vời gồm bánh ngọt và trái cây tươi.",
                "hint": "A meal consisting of several dishes from which guests serve themselves."
            },
            {
                "word": "venue",
                "meaning": "địa điểm tổ chức sự kiện (danh từ)",
                "image": "🏢",
                "example": "Our marketing banquet coordinator picked a scenic lakeside venue for the conference.",
                "example_vi": "Điều phối viên tiệc tiếp thị của chúng tôi đã chọn một địa điểm tổ chức bên hồ tuyệt đẹp cho hội nghị.",
                "hint": "The place where something happens, especially an organized event such as a concert or match."
            }
        ]
    },
    {
        "id": "toeic_support",
        "name": "Customer Support & Client Relations",
        "name_vi": "Bảo hành & Hỗ trợ Khách hàng",
        "icon": "🤝",
        "words": [
            {
                "word": "inquiry",
                "meaning": "yêu cầu thăm hỏi, yêu cầu giải đáp (danh từ)",
                "image": "💬",
                "example": "The customer relations support desk resolves every basic email inquiry within a day.",
                "example_vi": "Quầy hỗ trợ quan hệ khách hàng giải quyết mọi yêu cầu giải đáp qua email cơ bản trong vòng một ngày.",
                "hint": "An act of asking for information / official query."
            },
            {
                "word": "complaint",
                "meaning": "khiếu nại, phản nàn (danh từ)",
                "image": "🗣️",
                "example": "A formal warranty complaint was filed regarding the broken screen hardware.",
                "example_vi": "Một khiếu nại chính thức đã được gửi liên quan đến sự cố nứt vỡ phần cứng màn hình.",
                "hint": "A statement that a situation is unsatisfactory or unacceptable."
            },
            {
                "word": "warranty",
                "meaning": "sự bảo hành, cam kết bảo hành (danh từ)",
                "image": "🛡️",
                "example": "The electronic brand offers a three-year replacement warranty on all laptop hardware.",
                "example_vi": "Thương hiệu điện tử cung cấp bảo hành thay thế ba năm cho tất cả phần cứng máy tính xách tay.",
                "hint": "A written guarantee given to the purchaser of a new product promising to repair or replace."
            },
            {
                "word": "loyalty",
                "meaning": "lòng trung thành, sự gắn bó khách hàng (danh từ)",
                "image": "⭐",
                "example": "Our supermarket rewards customer loyalty with points redeemable for discount vouchers.",
                "example_vi": "Siêu thị của chúng tôi phần thưởng lòng trung thành của khách hàng bằng điểm có thể quy đổi ra hóa đơn giảm giá.",
                "hint": "The quality of being loyal to a brand or community."
            },
            {
                "word": "troubleshooting",
                "meaning": "khắc phục sự cố, xử lý lỗi (danh từ / động từ)",
                "image": "🔧",
                "example": "Review active steps inside our online troubleshooting guide before calling local agents.",
                "example_vi": "Hãy đọc xem các bước trong hướng dẫn khắc phục sự cố trực tuyến của chúng tôi trước khi gọi cho đại diện địa phương.",
                "hint": "Solve problems, especially systemic or technological malfunctions."
            },
            {
                "word": "representative",
                "meaning": "người đại diện, nhân viên bán hàng/CSKH (danh từ)",
                "image": "👤",
                "example": "Please remain on the line, a customer service representative will be with you shortly.",
                "example_vi": "Vui lòng giữ máy, một nhân viên đại diện dịch vụ khách hàng sẽ hỗ trợ bạn sớm.",
                "hint": "A person chosen or appointed to act or speak for another or group."
            },
            {
                "word": "press release",
                "meaning": "thông cáo báo chí (danh từ)",
                "image": "📄",
                "example": "The executive director published a press release detailing the new alternative energy vehicle.",
                "example_vi": "Giám đốc điều hành đã xuất bản một thông cáo báo chí chi tiết về chiếc xe năng lượng thay thế mới.",
                "hint": "An official statement sent to newspapers giving information on a particular matter."
            },
            {
                "word": "patron",
                "meaning": "khách hàng quen thuộc, người bảo trợ (danh từ)",
                "image": "👤",
                "example": "The local library sent a small thank-you gift to its most generous patrons.",
                "example_vi": "Thư viện địa phương đã gửi một món quà cảm ơn nhỏ tới những người ủng hộ bảo trợ hào phóng nhất của mình.",
                "hint": "A customer or supporter, especially a regular traveler or consumer."
            },
            {
                "word": "satisfaction",
                "meaning": "sự hài lòng (danh từ)",
                "image": "😊",
                "example": "We conduct annual studies to gauge consumer satisfaction rates with our software upgrades.",
                "example_vi": "Chúng tôi thực hiện các nghiên cứu hàng năm để đo lường tỷ lệ hài lòng của người dùng đối với các bản nâng cấp phần mềm.",
                "hint": "Fulfillment of one's wishes, expectations, or needs, or the pleasure derived from this."
            },
            {
                "word": "refund",
                "meaning": "sự hoàn tiền, trả lại tiền (danh từ / động từ)",
                "image": "💵",
                "example": "If the shipping package arrives damaged, you are eligible to claim a full refund.",
                "example_vi": "Nếu gói hàng vận chuyển đến bị hư hại, bạn có đủ điều kiện để yêu cầu hoàn lại tiền đầy đủ.",
                "hint": "A repayment of a sum of money, typically to a dissatisfied customer."
            },
            {
                "word": "assistance",
                "meaning": "sự hỗ trợ, giúp đỡ (danh từ)",
                "image": "🤝",
                "example": "Staff is fully trained to deliver immediate physical assistance to disabled clients.",
                "example_vi": "Nhân viên được đào tạo đầy đủ để sẵn sàng cung cấp sự hỗ trợ thể chất ngay lập tức cho khách hàng khuyết tật.",
                "hint": "The provision of money, resources, or help in doing something."
            },
            {
                "word": "contract",
                "meaning": "hợp đồng, ký kết (danh từ / động từ)",
                "image": "📄",
                "example": "Always review the small print inside contracts before appending your official signature.",
                "example_vi": "Hãy luôn đọc kỹ các điều khoản nhỏ bên trong hợp đồng trước khi ký chữ ký chính thức của bạn.",
                "hint": "A written or spoken agreement, especially one concerning employment, sales, or tenancy."
            },
            {
                "word": "client",
                "meaning": "khách hàng, đối tác (danh từ)",
                "image": "👤",
                "example": "The legal consultation firm represents several high-profile corporate clients.",
                "example_vi": "Công ty tư vấn pháp lý đại diện cho một số đối tác khách hàng doanh nghiệp tầm cỡ lớn.",
                "hint": "A person or organization using the services of a lawyer or other professional person."
            },
            {
                "word": "resolution",
                "meaning": "giải pháp, sự giải quyết, độ phân giải (danh từ)",
                "image": "✅",
                "example": "After a brief negotiation meeting, both companies reached a mutually agreeable resolution.",
                "example_vi": "Sau một cuộc họp đàm phán ngắn, cả hai công ty đã đạt được một giải pháp đồng thuận đôi bên.",
                "hint": "A firm decision to do or not to do something / sorting out relationship issue."
            },
            {
                "word": "support",
                "meaning": "sự hỗ trợ, ủng hộ (danh từ / động từ)",
                "image": "🤝",
                "example": "We hired extra student clerks to deal with customer support operations during holidays.",
                "example_vi": "Chúng tôi đã tuyển thêm nhân viên hỗ trợ sinh viên để giải quyết các hoạt động chăm sóc khách hàng trong các ngày nghỉ lễ.",
                "hint": "Bear all or part of the weight of / give assistance to."
            }
        ]
    },
    {
        "id": "toeic_property",
        "name": "Real Estate & Facilities",
        "name_vi": "Bất động sản & Mặt bằng cơ sở",
        "icon": "🏢",
        "words": [
            {
                "word": "tenant",
                "meaning": "người thuê nhà/căn hộ (danh từ)",
                "image": "👤",
                "example": "Safety rules require that every tenant register their vehicle with the building concierge.",
                "example_vi": "Các quy tắc an toàn yêu cầu mỗi người thuê nhà phải đăng ký xe của họ với quầy phục vụ tòa nhà.",
                "hint": "A person who occupies land or property rented from a landlord."
            },
            {
                "word": "lease",
                "meaning": "hợp đồng cho thuê, cho thuê (danh từ / động từ)",
                "image": "📄",
                "example": "The electronic business firm signed a five-year lease on a new downtown office building.",
                "example_vi": "Công ty kinh doanh điện tử đã ký hợp đồng cho thuê năm năm đối với một tòa nhà văn phòng mới ở trung tâm thành phố.",
                "hint": "A contract by which one party conveys land, property, services to another for a specified time."
            },
            {
                "word": "leasehold",
                "meaning": "quyền sở hữu tài sản thuê, tài sản thuê (danh từ / tính từ)",
                "image": "🏡",
                "example": "They purchased the leasehold apartment rather than buying freehold property.",
                "example_vi": "Họ đã mua căn hộ có thời hạn thuê thay vì mua tài sản sở hữu vĩnh viễn.",
                "hint": "The holding of property by lease."
            },
            {
                "word": "utilities",
                "meaning": "dịch vụ tiện ích công cộng, điện nước gas (danh từ số nhiều)",
                "image": "🚰",
                "example": "Monthly rent costs cover public utilities like water and security trash clearance.",
                "example_vi": "Chi phí thuê nhà hàng tháng đài thọ các dịch vụ tiện ích công cộng như nước và dọn rác bảo vệ bãi đỗ xe.",
                "hint": "Services such as electricity, gas, water, or public transport that are useful to the community."
            },
            {
                "word": "renovation",
                "meaning": "sự cải tạo, tu sửa (danh từ)",
                "image": "🔨",
                "example": "The historic hotel will undergo a multimillion-dollar renovation starting next spring.",
                "example_vi": "Khách sạn cổ kính sẽ trải qua một cuộc cải tạo trị giá nhiều triệu đô la bắt đầu vào mùa xuân tới.",
                "hint": "The action of renovating a building or structure."
            },
            {
                "word": "property",
                "meaning": "bất động sản, tài sản sở hữu (danh từ)",
                "image": "🏢",
                "example": "Investing in seaside property remains dynamic and highly profitable in dry tourist seasons.",
                "example_vi": "Đầu tư vào bất động sản ven biển vẫn rất sôi động và có lợi nhuận cao trong các mùa du lịch khô ráo.",
                "hint": "A thing or things belonging to someone; possessions collectively / land and buildings."
            },
            {
                "word": "landlord",
                "meaning": "chủ nhà, chủ đất (danh từ)",
                "image": "👴",
                "example": "The helpful landlord immediately hired a professional plumber to fix the kitchen utilities.",
                "example_vi": "Người chủ nhà tốt bụng đã lập tức thuê một thợ sửa ống nước chuyên nghiệp đến để sửa chữa các tiện ích nhà bếp.",
                "hint": "A person, especially a man, who rents land, a building, or an apartment to a tenant."
            },
            {
                "word": "mortgage",
                "meaning": "khoản thế chấp, thế chấp (danh từ / động từ)",
                "image": "🏠",
                "example": "Young couples borrow bank loans to cover their thirty-year home mortgage.",
                "example_vi": "Các cặp vợ chồng trẻ vay tiền ngân hàng để trang trải khoản thế chấp nhà thời hạn ba mươi năm.",
                "hint": "A legal agreement by which a bank or other creditor lends money at interest in exchange for taking title."
            },
            {
                "word": "appraisal",
                "meaning": "sự thẩm định, đánh giá giá trị (danh từ)",
                "image": "📊",
                "example": "Arrange an independent appraisal of the property before closing the purchase contract.",
                "example_vi": "Hãy sắp xếp một cuộc thẩm định độc hại về giá trị bất động sản trước khi khép lại hợp đồng mua bán.",
                "hint": "An act of assessing something or someone / a formal evaluation of property value or employees."
            },
            {
                "word": "maintenance",
                "meaning": "sự bảo dưỡng, bảo trì (danh từ)",
                "image": "🔧",
                "example": "Regular maintenance of factory machines prevents expensive safety hazard disruptions.",
                "example_vi": "Việc bảo dưỡng máy móc nhà máy thường xuyên giúp ngăn ngừa gián đoạn về mối nguy hiểm an toàn tốn kém.",
                "hint": "The process of maintaining or preserving someone or something, especially machinery or buildings."
            },
            {
                "word": "estate",
                "meaning": "bất động sản, di sản điền trang (danh từ)",
                "image": "🏡",
                "example": "The family owns a beautiful wine estate located in the south of France.",
                "example_vi": "Gia đình sở hữu một điền trang rượu vang tuyệt đẹp nằm ở phía nam nước Pháp.",
                "hint": "An extensive area of land in the country, usually with a large house, owned by one person or family / real estate."
            },
            {
                "word": "contract",
                "meaning": "hợp đồng (danh từ / động từ)",
                "image": "📄",
                "example": "Read every paragraph inside the tenancy contract before handing over security deposits.",
                "example_vi": "Hãy đọc kỹ mọi đoạn văn bản bên trong hợp đồng thuê nhà trước khi bàn trả tiền đặt cọc bảo đảm.",
                "hint": "A written or spoken agreement, especially one concerning employment, sales, or tenancy."
            },
            {
                "word": "resident",
                "meaning": "cư dân, người trú ngụ (danh từ / tính từ)",
                "image": "👤",
                "example": "Older residents of the community favor preserving the botanical forest garden layout.",
                "example_vi": "Những cư dân lớn tuổi của cộng đồng ưu tiên việc gìn giữ cảnh quan vườn bách thảo rừng.",
                "hint": "A person who lives somewhere permanently or on a long-term basis."
            },
            {
                "word": "vacancy",
                "meaning": "vị trí trống, chỗ còn trống (danh từ)",
                "image": "🏢",
                "example": "The apartment building manager advertised a new residential vacancy in the newsletter.",
                "example_vi": "Người quản lý tòa nhà chung cư đã quảng cáo một căn hộ trống còn trống mới trong bản tin tháng.",
                "hint": "An unoccupied position or job / an unoccupied room or apartment available for rent."
            },
            {
                "word": "furnish",
                "meaning": "trang bị đồ đạc nội thất, cung cấp (động từ)",
                "image": "🪑",
                "example": "The hospitality company decided to brand and furnish all rental apartments with minimalist sofas.",
                "example_vi": "Công ty khách sạn đã quyết định định hình thương hiệu và trang bị đồ đạc nội thất cho tất cả căn hộ cho thuê bằng ghế sofa tối giản.",
                "hint": "Provide a house or room with furniture and fittings."
            }
        ]
    }
]

def download_dictionary():
    """Download Ho Ngoc Duc dictionary or return blank dict if download fails."""
    print("📥 Downloading Ho Ngoc Duc's English-Vietnamese Dictionary for phonetic verification...")
    try:
        r = requests.get(HO_NGOC_DUC_DICT_URL, timeout=30)
        r.raise_for_status()
        content = r.content.decode('utf-8', errors='ignore')
        print(f"✅ Successfully downloaded {len(content)} characters. Parsing...")
        return parse_dictionary_content(content)
    except Exception as e:
        print(f"⚠️ Failed to download online dictionary: {e}. Falling back to default phonetics.")
        return {}

def parse_dictionary_content(content):
    """Parse dictionary content to word -> entry mapping."""
    raw_entries = re.split(r'\n(?=@)', content)
    parsed_dict = {}
    for raw in raw_entries:
        lines = [l.strip() for l in raw.split('\n') if l.strip()]
        if not lines:
            continue
        line1 = lines[0]
        if not line1.startswith('@'):
            continue
        header = line1[1:]
        word = header
        phonetic = ""
        
        match = re.search(r'/(.*?)/', header)
        if match:
            phonetic = '/' + match.group(1) + '/'
            word = header[:match.start()].strip()
        else:
            parts = header.split(' ', 1)
            if len(parts) > 1:
                word = parts[0]
                phonetic = parts[1]
                
        word_clean = word.strip().lower().replace('_', ' ')
        parsed_dict[word_clean] = phonetic.strip()
    return parsed_dict

def update_phonetics(topics, parsed_dict):
    """Ensure every word has a correct phonetic notation using the dictionary lookup."""
    print("⚡ Verifying and matching phonetics...")
    for t in topics:
        for w in t['words']:
            word_str = w['word'].lower()
            dict_phonetic = parsed_dict.get(word_str)
            if dict_phonetic:
                w['phonetic'] = dict_phonetic
            else:
                # Basic phonetic fallback if not present
                w['phonetic'] = f"/{word_str}/"
            # Explicitly clear audio as per layout
            w['audio'] = ""

def write_level_file(filename, level_id, label, label_vi, desc, topics):
    """Write compile-ready level JSON file."""
    filepath = os.path.join(DATA_DIR, filename)
    data = {
        "level": level_id,
        "label": label,
        "label_vi": label_vi,
        "description": desc,
        "topics": topics
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"💾 Written {filepath} successfully with {len(topics)} topics.")

def update_config():
    """Register TOEIC & TOEFL level files under config.json."""
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ config.json not found in the root workspace folder.")
        return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    levels = config.get('levels', [])
    toefl_path = "data/leveltoefl.json"
    toeic_path = "data/leveltoeic.json"
    
    # Normalize paths with forward slashes
    existing_normalized = [p.replace('\\', '/') for p in levels]
    
    if toefl_path not in existing_normalized:
         levels.append(toefl_path)
    if toeic_path not in existing_normalized:
         levels.append(toeic_path)
         
    config['levels'] = levels
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"✅ Registered Level files under {CONFIG_PATH}.")

def main():
    print("🚀 --- EXAM PREP VOCABULARY GENERATOR INITIALIZED --- 🚀")
    
    dict_map = download_dictionary()
    
    print("\n📝 COMPILING TOEFL EXAM DATASET...")
    update_phonetics(TOEFL_TOPICS, dict_map)
    write_level_file(
        "leveltoefl.json", 
        "TOEFL", 
        "TOEFL", 
        "TOEFL Academic Prep", 
        "Từ vựng học thuật cao cấp chuẩn bị cho kỳ thi TOEFL — Phân loại chi tiết theo 10 chủ đề khoa học và xã hội.", 
        TOEFL_TOPICS
    )
    
    print("\n📝 COMPILING TOEIC EXAM DATASET...")
    update_phonetics(TOEIC_TOPICS, dict_map)
    write_level_file(
        "leveltoeic.json", 
        "TOEIC", 
        "TOEIC", 
        "TOEIC Business English", 
        "Từ vựng chuyên nghiệp thuộc giới văn phòng và giao thương quốc tế ôn luyện kỳ thi TOEIC.", 
        TOEIC_TOPICS
    )
    
    print("\n⚙️ UPDATING GLOBAL CONFIGURATION...")
    update_config()
    
    print("\n🎉 --- EXAM PREP DATASET GENERATION SUCCESSFUL --- 🎉")

if __name__ == '__main__':
    main()
