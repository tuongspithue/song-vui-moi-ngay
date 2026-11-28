# Bộ emoji cho trẻ em: (loại, emoji, đáp án Việt, đáp án Anh, câu nói thêm bằng tiếng Anh, Robot đoán sai EN, Robot đoán sai VI)
KID_NEW = []
def K(kind, rows):
    for r in rows.strip().split('\n'):
        em, vi, en, mean, ge, gv = [x.strip() for x in r.split('|')]
        KID_NEW.append((kind, em, vi, en, mean, ge, gv))

K('Con vật', '''
🐱|Con mèo|A cat|Cats say meow!|A tiny fluffy tiger?|Chú hổ con lông xù hả?
🐶|Con chó|A dog|Dogs love to play fetch!|A wolf in pajamas?|Sói mặc đồ ngủ hả?
🐘|Con voi|An elephant|An elephant uses its trunk like a hand!|A mouse with a very long nose?|Con chuột mũi siêu dài hả?
🦒|Hươu cao cổ|A giraffe|Giraffes have super long necks!|A horse standing on tiptoes?|Con ngựa đang kiễng chân hả?
🐒|Con khỉ|A monkey|Monkeys love to climb trees!|A hairy little person?|Một bạn nhỏ đầy lông hả?
🐸|Con ếch|A frog|Frogs can jump very far!|A green tennis ball?|Quả bóng tennis xanh hả?
🐢|Con rùa|A turtle|A turtle carries its house on its back!|A walking rock?|Hòn đá biết đi hả?
🐧|Chim cánh cụt|A penguin|Penguins can swim but cannot fly!|A bird wearing a suit?|Chú chim mặc vest hả?
🦁|Sư tử|A lion|The lion is called the king of the jungle!|A cat with a big hairdo?|Chú mèo có kiểu tóc siêu to hả?
🐙|Bạch tuộc|An octopus|An octopus has eight arms!|A purple balloon with legs?|Quả bóng bay tím có chân hả?
🦋|Con bướm|A butterfly|A caterpillar turns into a butterfly!|A flying flower?|Bông hoa biết bay hả?
🐝|Con ong|A bee|Bees make sweet honey!|A tiny flying tiger?|Hổ con xíu biết bay hả?
🐟|Con cá|A fish|Fish breathe underwater!|A swimming leaf?|Chiếc lá biết bơi hả?
🐓|Gà trống|A rooster|Roosters crow in the morning!|A bird alarm clock?|Chiếc đồng hồ báo thức có lông hả?
🐄|Con bò|A cow|Cows give us milk!|A horse with spots?|Con ngựa có đốm hả?
🐰|Con thỏ|A rabbit|Rabbits love to eat carrots!|A cat with very long ears?|Chú mèo tai siêu dài hả?
🦆|Con vịt|A duck|Ducks can swim and fly!|A yellow bath toy?|Món đồ chơi tắm màu vàng hả?
🐊|Cá sấu|A crocodile|Crocodiles have lots of sharp teeth!|A log with a big smile?|Khúc gỗ đang cười toe hả?
''')

K('Trái cây & rau củ', '''
🍎|Quả táo|An apple|An apple is crunchy and sweet!|A red bouncy ball?|Quả bóng nảy màu đỏ hả?
🍌|Quả chuối|A banana|A banana is yellow when it is ripe!|A yellow moon?|Mặt trăng màu vàng hả?
🍇|Chùm nho|Grapes|Grapes grow in bunches!|Purple bubbles?|Bong bóng màu tím hả?
🍓|Quả dâu tây|A strawberry|A strawberry has tiny seeds on the outside!|A red heart with freckles?|Trái tim đỏ có tàn nhang hả?
🍍|Quả dứa|A pineapple|A pineapple has a spiky crown!|A tree wearing a spiky hat?|Cái cây đội mũ gai hả?
🥕|Củ cà rốt|A carrot|Carrots are crunchy and healthy!|An orange rocket?|Tên lửa màu cam hả?
🌽|Bắp ngô|Corn|Corn has lots of yellow kernels!|A yellow ruler?|Cây thước màu vàng hả?
🥦|Súp lơ xanh|Broccoli|Broccoli looks like a tiny tree!|A tiny forest in my bowl?|Cánh rừng bé xíu trong bát hả?
🍊|Quả cam|An orange|Oranges are full of juice!|A small sun?|Mặt trời bé xíu hả?
🥭|Quả xoài|A mango|Mangoes are sweet and juicy!|A yellow rugby ball?|Quả bóng bầu dục vàng hả?
🥥|Quả dừa|A coconut|A coconut has sweet water inside!|A hairy bowling ball?|Quả bowling đầy lông hả?
🍋|Quả chanh|A lemon|A lemon is very sour!|A tiny yellow football?|Quả bóng đá vàng bé xíu hả?
🍑|Quả đào|A peach|A peach is soft and fuzzy!|A baby's cheek?|Má của em bé hả?
🥒|Quả dưa leo|A cucumber|A cucumber is cool and crunchy!|A green submarine?|Tàu ngầm màu xanh hả?
🥔|Củ khoai tây|A potato|Potatoes grow under the ground!|A brown rock?|Hòn đá màu nâu hả?
🍒|Quả anh đào|Cherries|Cherries often grow in pairs!|Two red earrings?|Hai chiếc khuyên tai đỏ hả?
''')

K('Đồ vật', '''
☂️|Cái ô|An umbrella|An umbrella keeps you dry in the rain!|A flying mushroom?|Cây nấm biết bay hả?
🎒|Cặp sách|A school bag|You carry your books in a school bag!|A turtle shell?|Mai rùa hả?
⏰|Đồng hồ báo thức|An alarm clock|An alarm clock wakes you up!|A noisy robot head?|Cái đầu robot ồn ào hả?
🔑|Chìa khóa|A key|A key opens the door!|A metal lollipop?|Cây kẹo mút bằng sắt hả?
📚|Quyển sách|A book|Books are full of stories!|A box of pictures?|Cái hộp đầy hình hả?
✂️|Cái kéo|Scissors|Scissors can cut paper!|A metal crocodile?|Con cá sấu bằng sắt hả?
🪥|Bàn chải đánh răng|A toothbrush|Brush your teeth two times a day!|A tiny broom?|Cây chổi bé xíu hả?
🧦|Đôi tất|Socks|Socks keep your feet warm!|Foot pajamas?|Đồ ngủ cho bàn chân hả?
👟|Đôi giày|Shoes|Shoes protect your feet!|Boats for my toes?|Những chiếc thuyền cho ngón chân hả?
🧢|Chiếc mũ lưỡi trai|A cap|A cap keeps the sun off your face!|A flat bird nest?|Cái tổ chim dẹt hả?
🕶️|Kính râm|Sunglasses|Sunglasses make the sun less bright!|Two black pancakes?|Hai cái bánh kếp đen hả?
🪑|Cái ghế|A chair|You sit on a chair!|A table with a back?|Cái bàn có lưng hả?
🛏️|Cái giường|A bed|You sleep in a bed!|A big soft cookie?|Chiếc bánh quy mềm khổng lồ hả?
🪞|Cái gương|A mirror|A mirror shows your face!|A magic window?|Cửa sổ phép thuật hả?
📱|Điện thoại|A phone|A phone helps us call our family!|A shiny cookie?|Chiếc bánh quy sáng bóng hả?
💡|Bóng đèn|A light bulb|A light bulb makes the room bright!|An upside-down pear?|Quả lê lộn ngược hả?
🥄|Cái thìa|A spoon|We eat soup with a spoon!|A tiny shovel?|Cái xẻng bé xíu hả?
''')

K('Nghề nghiệp', '''
👩‍🚒|Lính cứu hỏa|A firefighter|Firefighters put out fires and help people!|A lady with a red hat and a water slide?|Cô giáo đội mũ đỏ bên cầu trượt nước hả?
👨‍🍳|Đầu bếp|A chef|A chef cooks yummy food!|A man with a tall marshmallow hat?|Chú đội mũ kẹo dẻo cao hả?
👩‍⚕️|Bác sĩ|A doctor|A doctor helps us get better when we are sick!|A superhero with a stethoscope?|Siêu nhân đeo ống nghe hả?
👨‍🏫|Thầy giáo|A teacher|A teacher helps us learn new things!|A man talking to a green board?|Chú nói chuyện với cái bảng xanh hả?
👮|Chú công an|A police officer|Police officers keep us safe!|A guard of the cookie jar?|Người canh hũ bánh quy hả?
👨‍🌾|Bác nông dân|A farmer|Farmers grow rice and vegetables!|A man with a giant straw hat?|Chú đội cái mũ rơm khổng lồ hả?
👩‍🚀|Phi hành gia|An astronaut|Astronauts travel to space!|A lady with a fishbowl on her head?|Cô đội bể cá lên đầu hả?
👨‍✈️|Phi công|A pilot|A pilot flies the airplane!|A bus driver in the clouds?|Bác lái xe buýt trên mây hả?
🧑‍🎨|Họa sĩ|An artist|An artist paints beautiful pictures!|A person with a rainbow plate?|Người cầm cái đĩa cầu vồng hả?
👩‍🔬|Nhà khoa học|A scientist|Scientists love to explore and ask why!|A wizard with a bottle?|Phù thủy cầm cái chai hả?
🧑‍💻|Lập trình viên|A programmer|A programmer tells computers what to do!|Someone playing with a laptop?|Bạn đang chơi với cái laptop hả?
👷|Công nhân xây dựng|A builder|Builders build houses and bridges!|A man with a yellow bucket on his head?|Chú đội cái xô vàng lên đầu hả?
🧑‍🎤|Ca sĩ|A singer|A singer sings songs for everyone!|A person with colorful hair shouting?|Bạn tóc nhiều màu đang hét hả?
🧑‍🔧|Thợ sửa chữa|A mechanic|A mechanic fixes cars and machines!|A person who tickles engines?|Người cù lét cái máy hả?
''')

K('Phương tiện', '''
🚒|Xe cứu hỏa|A fire truck|A fire truck goes nee-naw to put out fires!|A big red toy?|Món đồ chơi đỏ khổng lồ hả?
🚑|Xe cứu thương|An ambulance|An ambulance takes people to the hospital!|A white van with a siren hat?|Xe tải trắng đội mũ còi hả?
🚌|Xe buýt|A bus|A bus carries many people!|A long yellow caterpillar?|Con sâu vàng siêu dài hả?
🚁|Máy bay trực thăng|A helicopter|A helicopter flies with a spinning blade on top!|A flying fan?|Cái quạt biết bay hả?
⛵|Thuyền buồm|A sailboat|A sailboat moves with the wind!|A floating triangle?|Hình tam giác nổi trên nước hả?
🛵|Xe máy|A motorbike|A motorbike has two wheels and an engine!|A bicycle with a loud voice?|Chiếc xe đạp giọng to hả?
🚜|Máy cày|A tractor|A tractor works on the farm!|A giant tire toy?|Món đồ chơi bánh xe khổng lồ hả?
🚓|Xe cảnh sát|A police car|A police car has flashing lights!|A car with a disco hat?|Chiếc xe đội mũ disco hả?
🛶|Chiếc xuồng|A canoe|You paddle a canoe on the river!|A floating banana?|Quả chuối nổi trên sông hả?
🛴|Xe trượt scooter|A scooter|You push a scooter with one foot!|A skateboard with a steering wheel?|Ván trượt có tay lái hả?
🚕|Xe taxi|A taxi|A taxi takes you where you want to go!|A yellow car for lemons?|Chiếc xe vàng chở chanh hả?
🚛|Xe tải|A truck|A truck carries heavy things!|A very big box with wheels?|Cái hộp khổng lồ có bánh xe hả?
''')

K('Tiếng kêu', '''
🐶 🔊|Gâu gâu|Woof woof|A dog says woof woof!|A cat clearing its throat?|Con mèo đang hắng giọng hả?
🐱 🔊|Meo meo|Meow meow|A cat says meow meow!|A barking mouse?|Con chuột biết sủa hả?
🐮 🔊|Ùm bò|Moo moo|A cow says moo!|A very low flute?|Cây sáo trầm hả?
🐷 🔊|Ụt ịt|Oink oink|A pig says oink oink!|A rusty door?|Cánh cửa bị gỉ hả?
🐔 🔊|Cục tác|Cluck cluck|A hen says cluck cluck!|A tiny drum?|Cái trống bé xíu hả?
🐓 🔊|Ò ó o o|Cock-a-doodle-doo|A rooster says cock-a-doodle-doo in the morning!|A rooster singing opera?|Gà trống hát nhạc opera hả?
🦆 🔊|Quạc quạc|Quack quack|A duck says quack quack!|A squeaky shoe?|Chiếc giày kêu cót két hả?
🐸 🔊|Ộp ộp|Ribbit ribbit|A frog says ribbit ribbit!|A tiny tractor?|Cái máy cày bé xíu hả?
🐑 🔊|Be be|Baa baa|A sheep says baa baa!|A wobbly singer?|Ca sĩ hát run run hả?
🐴 🔊|Hí hí|Neigh neigh|A horse says neigh neigh!|A laughing robot?|Con robot đang cười hả?
🐝 🔊|Vo ve|Buzz buzz|A bee says buzz buzz!|A tiny motorbike?|Chiếc xe máy xíu xiu hả?
🦁 🔊|Gầm gừ|Roar|A lion says roar!|A big kitten sneezing?|Chú mèo to đang hắt xì hả?
🐭 🔊|Chít chít|Squeak squeak|A mouse says squeak squeak!|A rubber duck?|Chú vịt cao su hả?
''')

K('Màu sắc', '''
🔴|Màu đỏ|Red|Apples and strawberries can be red!|The color of a tomato soup?|Màu của món súp cà chua hả?
🟡|Màu vàng|Yellow|The sun and bananas are yellow!|The color of a lemon moon?|Màu của mặt trăng chanh hả?
🔵|Màu xanh dương|Blue|The sky and the sea are blue!|The color of a sleepy ocean?|Màu của đại dương đang buồn ngủ hả?
⚫|Màu đen|Black|The night sky is black!|The color of a cat's pajamas?|Màu đồ ngủ của mèo hả?
⚪|Màu trắng|White|Snow and milk are white!|The color of a cloud's pillow?|Màu cái gối của đám mây hả?
🟤|Màu nâu|Brown|Chocolate and tree trunks are brown!|The color of a muddy puddle?|Màu vũng nước bùn hả?
''')

K('Pha màu', '''
🔴 🟡|Màu cam|Orange|Red and yellow make orange!|Red and yellow make a banana?|Đỏ với vàng ra quả chuối hả?
🔵 🟡|Màu xanh lá|Green|Blue and yellow make green!|Blue and yellow make a frog?|Xanh với vàng ra con ếch hả?
🔴 🔵|Màu tím|Purple|Red and blue make purple!|Red and blue make a grape?|Đỏ với xanh ra quả nho hả?
🔴 ⚪|Màu hồng|Pink|Red and white make pink!|Red and white make a strawberry milk?|Đỏ với trắng ra sữa dâu hả?
''')

K('Đếm số', '''
🐟 🐟|Hai con cá|Two fish|One, two! Two fish!|Twenty fish?|Hai mươi con cá hả?
⭐ ⭐ ⭐ ⭐ ⭐|Năm ngôi sao|Five stars|One, two, three, four, five! Five stars!|A hundred stars?|Một trăm ngôi sao hả?
🎈 🎈 🎈|Ba quả bóng bay|Three balloons|One, two, three! Three balloons!|Ten balloons?|Mười quả bóng bay hả?
🍓 🍓 🍓 🍓|Bốn quả dâu|Four strawberries|One, two, three, four! Four strawberries!|Seven strawberries?|Bảy quả dâu hả?
🐥 🐥 🐥|Ba chú gà con|Three chicks|One, two, three! Three little chicks!|Two and a half chicks?|Hai chú gà rưỡi hả?
🚗 🚗|Hai chiếc xe|Two cars|One, two! Two cars!|A whole car parade?|Cả đoàn diễu hành xe hả?
🌸 🌸 🌸 🌸 🌸|Năm bông hoa|Five flowers|One, two, three, four, five! Five flowers!|A garden of one thousand flowers?|Khu vườn một nghìn bông hoa hả?
🍪 🍪 🍪 🍪|Bốn chiếc bánh quy|Four cookies|One, two, three, four! Four cookies!|Zero cookies? I ate them!|Không có chiếc nào? Robot ăn hết rồi!
🦋 🦋|Hai con bướm|Two butterflies|One, two! Two butterflies!|Three and a half butterflies?|Ba con bướm rưỡi hả?
🐞 🐞 🐞 🐞 🐞|Năm con bọ rùa|Five ladybugs|One, two, three, four, five! Five ladybugs!|Nine ladybugs?|Chín con bọ rùa hả?
🍦 🍦 🍦|Ba cây kem|Three ice creams|One, two, three! Three ice creams!|Eleven ice creams?|Mười một cây kem hả?
🎁 🎁 🎁 🎁|Bốn hộp quà|Four gifts|One, two, three, four! Four gifts!|A million gifts?|Một triệu hộp quà hả?
''')

K('Cảm xúc', '''
😀|Vui vẻ|Happy|A smile shows we are happy!|Eating a banana?|Đang ăn chuối hả?
😢|Buồn bã|Sad|When we are sad, a hug can help!|Lost a sock?|Bị mất một chiếc tất hả?
😡|Tức giận|Angry|Take a deep breath when you feel angry!|The soup is too hot?|Súp nóng quá hả?
😴|Buồn ngủ|Sleepy|When we are sleepy, it is time to rest!|Practicing being a statue?|Đang tập làm bức tượng hả?
😮|Ngạc nhiên|Surprised|We feel surprised when something new happens!|Seeing a flying pig?|Thấy con heo bay hả?
😨|Sợ hãi|Scared|It is okay to feel scared. Tell a grown-up!|Seeing a spider cookie?|Thấy chiếc bánh quy hình nhện hả?
🥰|Yêu thương|Loving|We show love with hugs and kind words!|Looking at pizza?|Đang nhìn cái pizza hả?
🤒|Bị ốm|Sick|When we are sick, we rest and see a doctor!|Wearing a hot water bottle hat?|Đội mũ túi sưởi hả?
😋|Thèm ăn|Hungry|We feel hungry when our tummy wants food!|Tasting the moon?|Đang nếm mặt trăng hả?
🥱|Mệt mỏi|Tired|When we are tired, we need sleep!|Catching a fly with my mouth?|Đang bắt ruồi bằng miệng hả?
''')

K('Hoạt động', '''
🛁|Đang tắm|Taking a bath|Baths keep us clean and fresh!|A duck pool party?|Tiệc bể bơi của vịt hả?
🪥|Đánh răng|Brushing teeth|Brush your teeth morning and night!|Painting my teeth?|Đang sơn răng hả?
🏃|Chạy bộ|Running|Running makes our legs strong!|Chasing a butterfly?|Đuổi theo con bướm hả?
🏊|Bơi lội|Swimming|Swimming is fun in the water!|Walking in a wet world?|Đi bộ trong thế giới ướt hả?
🚴|Đạp xe|Riding a bike|Pedal, pedal, pedal!|Rolling on two coins?|Lăn trên hai đồng xu hả?
📖|Đọc sách|Reading a book|Reading helps us learn and dream!|Eating a paper sandwich?|Ăn bánh mì kẹp giấy hả?
🎨|Vẽ tranh|Painting a picture|Painting is fun with lots of colors!|Mixing a rainbow soup?|Trộn súp cầu vồng hả?
🎤|Hát|Singing|Singing makes us happy!|Eating a microphone?|Đang ăn cái micro hả?
💃|Nhảy múa|Dancing|Dancing is fun with music!|Shaking off the bees?|Đang rũ đàn ong hả?
🛌|Đi ngủ|Going to bed|A good sleep helps us grow!|Hiding from the sun?|Đang trốn mặt trời hả?
🧹|Quét nhà|Sweeping the floor|Sweeping keeps our home clean!|Riding a witch's broom?|Cưỡi chổi phù thủy hả?
🚿 🌱|Tưới cây|Watering plants|Plants need water to grow!|Giving a plant a bath?|Tắm cho cái cây hả?
''')

K('Thiên nhiên', '''
☔|Trời mưa|Rain|Rain helps plants grow!|The clouds are crying?|Mây đang khóc hả?
🌈|Cầu vồng|A rainbow|A rainbow has seven colors!|A giant colorful slide?|Cầu trượt khổng lồ nhiều màu hả?
⛈️|Giông bão|A thunderstorm|Thunder is a loud sound in the sky!|Clouds playing drums?|Mây đang chơi trống hả?
❄️|Bông tuyết|A snowflake|Every snowflake is different!|A flying lace?|Cái ren biết bay hả?
☀️|Mặt trời|The sun|The sun gives us light and warmth!|A giant lemon lamp?|Cái đèn chanh khổng lồ hả?
🌙|Mặt trăng|The moon|The moon shines at night!|A banana in the sky?|Quả chuối trên trời hả?
🌋|Núi lửa|A volcano|A volcano can erupt with hot lava!|A mountain with a stomach ache?|Ngọn núi bị đau bụng hả?
🌊|Sóng biển|Waves|Waves roll to the beach!|The sea waving hello?|Biển đang vẫy tay chào hả?
🍄|Cây nấm|A mushroom|Some mushrooms grow in the forest!|A tiny umbrella?|Cái ô bé xíu hả?
🌵|Cây xương rồng|A cactus|A cactus lives in the desert and has spikes!|A green hedgehog?|Con nhím xanh hả?
🌪️|Lốc xoáy|A tornado|A tornado spins round and round!|A cloud doing ballet?|Đám mây đang múa ba lê hả?
''')

K('Đồ ăn vặt', '''
🍦|Cây kem|An ice cream|Ice cream is cold and sweet!|A cold hat?|Cái mũ lạnh hả?
🍕|Bánh pizza|A pizza|Pizza is round and cheesy!|A triangle puzzle?|Trò xếp hình tam giác hả?
🍔|Bánh hamburger|A hamburger|A hamburger has many layers!|A bun sandwich tower?|Tòa tháp bánh mì hả?
🍟|Khoai tây chiên|French fries|French fries are crispy!|Yellow sticks?|Những cây gậy vàng hả?
🍩|Bánh vòng|A donut|A donut has a hole in the middle!|A tasty tire?|Cái lốp xe ăn được hả?
🍪|Bánh quy|A cookie|Cookies are crunchy and yummy!|A flat round rock?|Hòn đá dẹt hả?
🧁|Bánh cupcake|A cupcake|A cupcake is a small cake!|A cake with a hat?|Cái bánh đội mũ hả?
🍫|Thanh sô-cô-la|A chocolate bar|Chocolate is made from cocoa beans!|A brown ruler?|Cây thước màu nâu hả?
🍿|Bắp rang|Popcorn|Popcorn pops when it is hot!|Tiny white clouds?|Những đám mây trắng xíu hả?
🥛|Ly sữa|A glass of milk|Milk helps our bones grow strong!|White water?|Nước màu trắng hả?
🍭|Kẹo mút|A lollipop|A lollipop is a sweet candy on a stick!|A candy flower?|Bông hoa kẹo hả?
🧀|Miếng phô mai|A piece of cheese|Cheese has many holes!|A yellow sponge?|Miếng bọt biển vàng hả?
''')

K('Cơ thể', '''
👀|Đôi mắt|Eyes|We see with our eyes!|Two little balls?|Hai quả bóng nhỏ hả?
👂|Cái tai|An ear|We hear with our ears!|A curly shell?|Vỏ ốc cuộn hả?
👃|Cái mũi|A nose|We smell with our nose!|A little hill on my face?|Ngọn đồi nhỏ trên mặt hả?
👄|Cái miệng|A mouth|We eat and talk with our mouth!|A red banana?|Quả chuối đỏ hả?
🦷|Chiếc răng|A tooth|Teeth help us chew our food!|A tiny white rock?|Hòn đá trắng xíu hả?
✋|Bàn tay|A hand|We have five fingers on each hand!|A five-legged spider?|Con nhện năm chân hả?
🦶|Bàn chân|A foot|We walk and run with our feet!|A big toe party?|Bữa tiệc ngón chân hả?
👅|Cái lưỡi|A tongue|We taste food with our tongue!|A pink noodle?|Sợi mì màu hồng hả?
🧠|Bộ não|A brain|The brain helps us think and learn!|A pink cauliflower?|Cây súp lơ hồng hả?
❤️|Trái tim|A heart|The heart pumps blood around our body!|A red balloon?|Quả bóng bay đỏ hả?
''')

K('Đồ chơi', '''
🧸|Gấu bông|A teddy bear|A teddy bear is soft to hug!|A sleepy real bear?|Chú gấu thật đang ngủ hả?
🪁|Cái diều|A kite|A kite flies in the wind!|A flying pillow?|Cái gối biết bay hả?
🎈|Bóng bay|A balloon|A balloon floats when it has helium!|A floating bubble gum?|Kẹo cao su nổi lên hả?
🪀|Con yo-yo|A yo-yo|A yo-yo goes up and down on a string!|A spinning cookie?|Chiếc bánh quy biết xoay hả?
🧩|Trò xếp hình|A puzzle|A puzzle has many pieces to put together!|A broken picture?|Bức tranh bị vỡ hả?
🎲|Con xúc xắc|A dice|A dice has six sides!|A square with freckles?|Hình vuông có tàn nhang hả?
🛝|Cầu trượt|A slide|You go wheee on a slide!|A slippery stairway?|Cầu thang trơn tuột hả?
🎠|Đu quay ngựa gỗ|A carousel|A carousel goes round and round!|Horses on a merry-go-round?|Ngựa chạy vòng vòng hả?
🎮|Máy chơi game|A game controller|A game controller helps us play video games!|A plastic butterfly?|Con bướm nhựa hả?
🥁|Cái trống|A drum|A drum goes boom boom!|A round table for drumsticks?|Cái bàn tròn cho que đánh hả?
🎸|Đàn ghi-ta|A guitar|A guitar has six strings!|A flat violin with a long neck?|Đàn violin dẹt cổ dài hả?
🎺|Cây kèn|A trumpet|A trumpet is loud and shiny!|An elephant's golden nose?|Cái mũi vàng của voi hả?
''')
