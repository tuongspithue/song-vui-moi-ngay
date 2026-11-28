# Bổ sung emoji theo định hướng gốc (thành ngữ, tục ngữ, món ăn, địa danh, văn hoá, ghép chữ): (loại, emoji, đáp án, nghĩa đen EN, ý nghĩa EN, Robot đoán sai EN, Robot đoán sai VI)
EMOJI2 = []
def K(kind, rows):
    for r in rows.strip().split('\n'):
        em, vi, en, mean, ge, gv = [x.strip() for x in r.split('|')]
        EMOJI2.append((kind, em, vi, en, mean, ge, gv))

K('TN', '''
😡 🐟 🔪 🪵|Giận cá chém thớt|Angry at the fish, chopping the board|Meaning: taking anger out on innocent things|A very angry chef?|Ông đầu bếp đang nổi giận hả?
🛢️ 🔥|Đổ dầu vào lửa|Pouring oil on the fire|Meaning: making a bad situation worse|A giant barbecue party?|Bữa tiệc nướng siêu to hả?
🪨 🙈 ✋|Ném đá giấu tay|Throwing a stone and hiding the hand|Meaning: doing harm in secret|A stone playing hide and seek?|Hòn đá chơi trốn tìm hả?
🦀 🏖️ 🌊|Dã tràng xe cát biển Đông|The crab rolls sand in the East Sea|Meaning: wasted effort|A crab building a sandcastle?|Chú cua xây lâu đài cát hả?
🍂 🌳 ⬅️|Lá rụng về cội|Falling leaves return to the roots|Meaning: people return to their homeland|A tree cleaning day?|Ngày dọn dẹp của cái cây hả?
🔔 👊 🔊|Chuông có đánh mới kêu|A bell rings only when struck|Meaning: you must act to get results|A very lazy bell?|Chiếc chuông lười biếng hả?
🪓 🚜 🛤️|Đẽo cày giữa đường|Carving a plow in the middle of the road|Meaning: changing your plan to follow every opinion|A carpenter on the highway?|Bác thợ mộc trên đường cao tốc hả?
😮 🌳 ⏳|Há miệng chờ sung|Open your mouth and wait for figs|Meaning: waiting for luck without effort|A hungry tree watcher?|Người ngắm cây đang đói bụng hả?
👞 🫃|Đi guốc trong bụng|Wearing clogs inside someone's belly|Meaning: knowing exactly what someone thinks|A shoe in my tummy?|Chiếc giày trong bụng tôi hả?
🗣️ 🐷 🦶|Nói toạc móng heo|Speak out the pig's hoof|Meaning: speaking very bluntly|A pig doing karaoke?|Chú heo đang hát karaoke hả?
🍋 ✊ 🗑️|Vắt chanh bỏ vỏ|Squeeze the lemon, throw away the peel|Meaning: using someone and then discarding them|Making lemonade?|Đang pha nước chanh hả?
🙈 🦎|Giấu đầu hở đuôi|Hide the head, show the tail|Meaning: a poor attempt to hide a secret|A shy lizard?|Chú thằn lằn nhút nhát hả?
💸 🤕|Tiền mất tật mang|Lose money and get hurt too|Meaning: losing twice over|A very expensive doctor?|Ông bác sĩ siêu đắt tiền hả?
👨‍🦯 🐘 🤚|Thầy bói xem voi|Fortune-tellers feeling an elephant|Meaning: judging the whole from only one part|Petting a giant gray wall?|Vuốt ve bức tường xám khổng lồ hả?
🚩 ✋|Cờ đến tay ai người ấy phất|Whoever holds the flag waves it|Meaning: seize the chance when it comes to you|A flag-waving contest?|Cuộc thi vẫy cờ hả?
🗣️ 🙏 ❤️ 🐍|Khẩu phật tâm xà|Buddha's mouth, snake's heart|Meaning: kind words but a wicked heart|A holy snake?|Con rắn thần thánh hả?
👩 🎤 👶 👍|Mẹ hát con khen hay|Mother sings, child says wonderful|Meaning: praise from people who love you is biased|A tiny music critic?|Nhà phê bình âm nhạc tí hon hả?
💧 🦆 😐|Nước đổ đầu vịt|Water poured on a duck's head|Meaning: advice that has no effect|A duck taking a shower?|Vịt đang tắm vòi sen hả?
🔥 🏠 😌 🏺|Cháy nhà hàng xóm bình chân như vại|The neighbor's house burns, calm as a jar|Meaning: not caring about other people's trouble|A very relaxed neighbor?|Ông hàng xóm siêu thư giãn hả?
🏠 ☔ ⬇️|Nhà dột từ nóc|The house leaks from the roof|Meaning: problems start from the top|A rainy day inside?|Ngày mưa trong nhà hả?
🐱 👴 🦊|Mèo già hóa cáo|An old cat turns into a fox|Meaning: people get cunning with age|A cat wearing a fox costume?|Mèo mặc đồ hóa trang thành cáo hả?
🐯 👨 🐯 👶|Hổ phụ sinh hổ tử|A tiger father has a tiger son|Meaning: a great father has a great son|A tiger family photo?|Ảnh gia đình nhà hổ hả?
🌸 🪞 🌙 💧|Hoa trong gương trăng đáy nước|Flowers in a mirror, the moon in the water|Meaning: something beautiful but unreal|A very wet mirror?|Chiếc gương bị ướt hả?
🦗 🦵 🚗|Châu chấu đá xe|A grasshopper kicks a car|Meaning: foolishly challenging something much stronger|A tiny soccer match?|Trận bóng đá siêu nhỏ hả?
''')

K('TU', '''
💪 🎯 ✅|Có chí thì nên|Where there is a will, there is a way|Meaning: determination leads to success|A strong archer?|Cung thủ khỏe mạnh hả?
🍚 🧼 👕 🌸|Đói cho sạch, rách cho thơm|Hungry but clean, tattered but fragrant|Meaning: keep your dignity even in hard times|A laundry soap song?|Bài hát về xà phòng giặt hả?
🏃 💨 ❌ 🎯|Dục tốc bất đạt|Haste does not reach the goal|Meaning: rushing leads to failure|A very fast missed arrow?|Mũi tên bay nhanh bị trượt hả?
🏮 🏠 ✨|Đèn nhà ai nấy rạng|Each house's lamp shines for itself|Meaning: everyone minds their own business|A lamp contest?|Cuộc thi đèn sáng hả?
🤐 1️⃣ ➡️ 9️⃣ 😊|Một sự nhịn chín sự lành|One bit of patience brings nine goods|Meaning: staying calm avoids trouble|A math lesson?|Bài học toán hả?
🌳 🌱 💧 ⛰️|Cây có cội nước có nguồn|Trees have roots, water has a source|Meaning: always remember where you come from|A gardening class?|Lớp học làm vườn hả?
👓 👴 🎂|Kính lão đắc thọ|Respect the elderly and live long|Meaning: honoring elders brings blessings|Grandpa's birthday glasses?|Kính sinh nhật của ông hả?
🌾 1️⃣ 💦 9️⃣|Một hạt thóc chín giọt mồ hôi|One grain of rice, nine drops of sweat|Meaning: food comes from hard work|A very sweaty rice grain?|Hạt gạo ướt đẫm mồ hôi hả?
🧑‍🌾 🍚 ✅|Có làm thì mới có ăn|If you don't work, you don't eat|Meaning: you must work to earn your living|A farmer's lunch box?|Hộp cơm trưa của bác nông dân hả?
''')

K('MA', '''
🍜 🦐 🐖|Hủ tiếu|Hu tieu noodle soup|A noodle soup from southern Vietnam|A noodle that sings?|Sợi mì biết hát hả?
🫔 🐖 🍄|Bánh cuốn|Steamed rice rolls|Thin rice rolls filled with pork and mushrooms|A rice blanket?|Chiếc chăn bằng gạo hả?
🍚 🟨 🦐|Bún đậu mắm tôm|Vermicelli with tofu and shrimp paste|A dish with fried tofu and a very strong dip|A very smelly picnic?|Buổi dã ngoại siêu thơm hả?
🌯 🐖 🔥|Chả giò|Fried spring rolls|Crispy golden rolls filled with pork and veggies|A golden cigar?|Điếu xì gà vàng hả?
🍲 🔥 🐟|Lẩu|Hot pot|A pot of soup cooked right at the table|A bubbling pot party?|Bữa tiệc nồi sôi sùng sục hả?
🥤 🟢 🟡 🔴|Chè ba màu|Three-color dessert|A sweet dessert with beans, jelly and coconut milk|A traffic light drink?|Ly nước đèn giao thông hả?
🥬 🧄 🔥|Rau muống xào tỏi|Stir-fried morning glory with garlic|A favorite Vietnamese vegetable dish|A salad on fire?|Món salad đang cháy hả?
🐖 🥚 🍚|Thịt kho trứng|Braised pork and eggs|A comforting dish in caramel sauce, popular at Tet|A pig having breakfast?|Chú heo ăn sáng hả?
🐚 🌿 🌶️|Ốc luộc|Boiled snails|Snails served with a lemongrass and chili dip|A snail parade?|Cuộc diễu hành của ốc sên hả?
🫓 🔥 🥚|Bánh tráng nướng|Grilled rice paper|A popular street snack, often called Vietnamese pizza|A crispy pizza?|Cái pizza giòn rụm hả?
🥛 🟣 🍚|Sữa chua nếp cẩm|Yogurt with purple sticky rice|A sweet and sour dessert|A purple milkshake?|Ly sữa lắc màu tím hả?
🍲 🐔 🍚|Cháo gà|Chicken porridge|A warm comfort food, loved when you feel unwell|A chicken in a bath?|Chú gà đang tắm hả?
🥩 🌿 🔥|Bò lá lốt|Beef wrapped in betel leaves|Grilled beef rolls with an aromatic leaf|A leaf wearing a steak?|Chiếc lá mặc áo bít tết hả?
☕ 🧂 🥛|Cà phê muối|Salted coffee|A drink from Huế with a salty cream layer|A very salty morning?|Buổi sáng mặn chát hả?
🥥 🍦|Kem dừa|Coconut ice cream|A cold dessert served in a coconut shell|A hairy ice cream?|Cây kem đầy lông hả?
🍵 🧊|Trà đá|Iced tea|The sidewalk drink of Vietnam|A cold cup of leaves?|Cốc lá cây lạnh hả?
🍌 🔥 🥥|Chuối nướng|Grilled banana|Sweet and smoky, served with coconut milk|A burnt banana?|Quả chuối bị cháy hả?
🍠 🔥|Khoai lang nướng|Roasted sweet potato|A warm snack on a cold day|A hot potato?|Củ khoai nóng bỏng tay hả?
''')

K('DD', '''
💦 ⛰️ 🇻🇳|Thác Bản Giốc|Ban Gioc Waterfall|A famous waterfall on the border in Cao Bằng|A giant shower?|Vòi sen khổng lồ hả?
🦀 📍 🌊|Mũi Cà Mau|Ca Mau Cape|The southernmost point of mainland Vietnam|A crab's address?|Địa chỉ nhà của cua hả?
🚩 ⛰️ 🇻🇳|Cột cờ Lũng Cú|Lung Cu Flag Tower|The northernmost point of Vietnam, in Hà Giang|A flag on a mountain?|Lá cờ trên đỉnh núi hả?
🍵 🌱 ⛰️|Đồi chè Mộc Châu|Moc Chau tea hills|Rolling green tea hills in Sơn La|A green carpet?|Tấm thảm xanh hả?
☁️ ⛰️ 🛣️|Đèo Hải Vân|Hai Van Pass|The Pass of Ocean Clouds between Huế and Đà Nẵng|A road in the clouds?|Con đường trên mây hả?
🛶 ⛰️ 🌿|Tràng An|Trang An Landscape Complex|A UNESCO site in Ninh Bình with boat rides through caves|A boat in a cave?|Chiếc thuyền trong hang hả?
🛶 ⛩️ 🌸|Chùa Hương|Perfume Pagoda|A pilgrimage site reached by boat on the Yến River|A fragrant temple?|Ngôi chùa thơm phức hả?
🛍️ 🕰️ 🏪|Chợ Bến Thành|Ben Thanh Market|A famous market with a clock tower|A giant shopping clock?|Cái đồng hồ mua sắm khổng lồ hả?
🌉 🚂 🌅|Cầu Long Biên|Long Bien Bridge|An old iron bridge across the Red River in Hà Nội|A rusty rainbow?|Cầu vồng bị gỉ hả?
🪨 ⛰️ 🌸|Cao nguyên đá Đồng Văn|Dong Van Karst Plateau|A UNESCO Global Geopark in Hà Giang|A garden of rocks?|Khu vườn toàn đá hả?
💨 🌬️ ⚡|Cánh đồng quạt gió Bạc Liêu|Bac Lieu wind farm|Giant wind turbines standing in the sea|Giant fans for the ocean?|Quạt khổng lồ cho đại dương hả?
🏝️ 🐒|Đảo Cát Bà|Cat Ba Island|Home of the rare Cat Ba langur|A monkey vacation?|Kỳ nghỉ của chú khỉ hả?
''')

K('VH', '''
🎶 🪕 👩|Hát ca trù|Ca tru singing|An ancient chamber singing art of the north|A lady with a guitar?|Cô gái cầm đàn ghi-ta hả?
🎭 🥁 👑|Hát tuồng|Tuong classical theater|Traditional theater with bold masks and drums|A drama about a drum?|Vở kịch về cái trống hả?
🎸 🌙 🌾|Đờn ca tài tử|Don ca tai tu music|Amateur music of the south, a UNESCO heritage|A moonlight guitar?|Cây đàn dưới ánh trăng hả?
🧧 🌸 🛍️|Chợ Tết|Tet market|A busy market before the Lunar New Year|A flower shop sale?|Cửa hàng hoa giảm giá hả?
🐟 🔥 🏠|Ông Công ông Táo|Kitchen Gods Day|On the 23rd of the 12th lunar month, carp carry the gods to heaven|A fish fire drill?|Buổi diễn tập cháy của cá hả?
🦵 🪶|Đá cầu|Shuttlecock kicking|A game of keeping a feathered shuttlecock in the air|A foot playing with a feather?|Cái chân chơi với chiếc lông vũ hả?
🛍️ 🦘 🏁|Nhảy bao bố|Sack race|A funny festival game|Kangaroos in sacks?|Chuột túi chui vào bao hả?
🪢 👥 💪|Kéo co|Tug of war|A team game where both sides pull a rope|A rope battle?|Trận chiến của sợi dây hả?
🙈 🐐 🏃|Bịt mắt bắt dê|Blind man's buff|A childhood game of catching a goat while blindfolded|A goat hide and seek?|Dê chơi trốn tìm hả?
🐉 🐍 ☁️|Rồng rắn lên mây|Dragon-snake climbs the clouds|A childhood game with a line of children chasing the tail|A dragon in a line?|Con rồng xếp hàng hả?
☕ 🪑 🛵|Cà phê vỉa hè|Sidewalk coffee|Sitting on little stools and watching the street go by|A tiny chair party?|Bữa tiệc ghế tí hon hả?
🪷 🕯️ 🌊|Thả hoa đăng|Floating flower lanterns|People float lanterns on the water to make wishes|Candles taking a swim?|Những cây nến đi bơi hả?
💃 🥁 ⛰️|Múa xòe Thái|Thai xoe dance|A circle dance of the Thai people, a UNESCO heritage|A mountain disco?|Vũ trường trên núi hả?
🌴 😴|Nằm võng|Lying in a hammock|A cool way to nap on a hot afternoon|Sleeping on a palm tree?|Ngủ trên cây dừa hả?
🧣 🌾|Khăn rằn|Checkered scarf|A scarf worn by people of the Mekong Delta|A farmer's flag?|Lá cờ của bác nông dân hả?
''')

K('GC', '''
🐱 🌲|Mèo rừng|Wildcat|In Vietnamese: a forest cat|A cat on a camping trip?|Chú mèo đi cắm trại hả?
🦋 🌙|Bướm đêm|Moth|In Vietnamese: a night butterfly|A sleepy butterfly?|Con bướm buồn ngủ hả?
🐷 🏺|Heo đất|Piggy bank|In Vietnamese: a clay pig|A pig made of mud?|Chú heo làm từ bùn hả?
🐄 🥛|Bò sữa|Dairy cow|In Vietnamese: a milk cow|A cow who loves milk?|Con bò thích uống sữa hả?
🌧️ 🧊|Mưa đá|Hail|In Vietnamese: ice rain|A cold shower?|Vòi sen lạnh hả?
🚗 ♨️|Xe hơi|Car|In Vietnamese: a steam vehicle|A hot car?|Chiếc xe nóng hổi hả?
''')
