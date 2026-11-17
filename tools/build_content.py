"""Tạo data/content_v2.json: câu đố (kèm câu Robot đoán sai) + câu đuổi hình bắt chữ bằng emoji.
Chạy: python tools/build_content.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
old = {r['id']: r for r in json.load(open(os.path.join(ROOT, 'data', 'content.json'), encoding='utf8'))['riddles']}

# Câu cũ tạm tắt (đáp án mơ hồ, trùng ý, kém hấp dẫn hoặc nhắc tên nhân vật có bản quyền)
OFF = 'R032 R037 R044 R045 R061 R071 R078 R083 R085 R087 R117 R120 R123 R129 R130 R131 R170 R171 R179 R192'.split()

# Câu cũ giữ lại: mã | Robot đoán sai (EN) | (VI)
KEEP = """
R001 | Is it... the hospital bill? | Là… hoá đơn viện phí hả?
R002 | Is it... a drum? | Là… cái trống hả?
R004 | Is it... my umbrella? | Là… cái ô của tôi hả?
R005 | Is it... my phone charger? | Là… cục sạc điện thoại hả?
R006 | Is it... a broken table? | Là… cái bàn gãy chân hả?
R008 | My homework calendar? | Lịch nộp bài tập hả?
R009 | The traffic jam? | Chỗ kẹt xe hả?
R010 | My dad's pajamas? | Quần ngủ của bố hả?
R011 | The way home when I'm hungry? | Đường về nhà lúc đói bụng hả?
R015 | Is it... a robot like me? | Là… con robot như tôi hả?
R016 | Is it... a sleepy shark? | Là… cá mập buồn ngủ hả?
R017 | Is it... a giraffe ghost? | Là… con ma hươu cao cổ hả?
R018 | Is it... my little brother? | Là… em trai tôi hả?
R019 | Is it... my pizza delivery? | Là… anh giao pizza hả?
R021 | Is it... my old socks? | Là… đôi tất cũ của tôi hả?
R022 | Is it... my debt? | Là… món nợ của tôi hả?
R023 | Is it... the prices? | Là… giá cả hả?
R024 | Is it me, without my glasses? | Là tôi lúc quên kính hả?
R026 | A locksmith on holiday? | Ông thợ khoá đi nghỉ mát hả?
R027 | Is it... my nose? | Là… cái mũi của tôi hả?
R028 | February! | Tháng Hai!
R031 | Is it... a traffic light? | Là… đèn giao thông hả?
R033 | Is it... my diet plan? | Là… kế hoạch ăn kiêng hả?
R035 | My mom on moving day? | Mẹ tôi hôm chuyển nhà hả?
R036 | A circus duck? | Vịt làm xiếc hả?
R042 | Is it... homework? | Là… bài tập về nhà hả?
R043 | By phone? | Bằng điện thoại hả?
R046 | A lazy fish? | Con cá lười hả?
R047 | Is it... my dog on a leash? | Là… con chó nhà tôi hả?
R048 | Is it... a snake? | Là… con rắn hả?
R049 | Is it... my dad's snoring? | Là… tiếng ngáy của bố hả?
R050 | Is it... a ghost? | Là… con ma hả?
R051 | An airplane? | Máy bay hả?
R053 | My brother when mom calls? | Anh trai tôi lúc mẹ gọi hả?
R054 | A shy parrot? | Con vẹt nhút nhát hả?
R055 | An airplane in the factory? | Máy bay trong xưởng hả?
R060 | In a video game? | Trong trò chơi điện tử hả?
R062 | Is it... a soap bubble? | Là… bong bóng xà phòng hả?
R063 | Because it is hungry? | Vì nó đói bụng hả?
R064 | Is it... a sleeping dog? | Là… con chó đang ngủ hả?
R069 | Is it... a sad airplane? | Là… máy bay đang buồn hả?
R070 | Is it... a security camera? | Là… camera an ninh hả?
R072 | Is it... a fish? | Là… con cá hả?
R080 | The Sahara? | Sa mạc Sahara hả?
R081 | A plastic cake? | Bánh nhựa hả?
R082 | A leaf with superglue? | Chiếc lá dán keo hả?
R089 | Mount Fuji? | Núi Phú Sĩ hả?
R090 | Use a pillow? | Lót cái gối hả?
R092 | Is it... a lazy cat? | Là… con mèo lười hả?
R099 | The frogs? | Mấy con ếch hả?
R101 | My dog chasing its tail? | Con chó đuổi theo đuôi hả?
R102 | It turns purple? | Nó thành màu tím hả?
R104 | Is it... my dog's nose? | Là… mũi con chó nhà tôi hả?
R105 | The police were sleeping? | Cảnh sát ngủ gật hả?
R106 | Buy a bigger fridge? | Mua tủ lạnh to hơn hả?
R113 | A river on the map? | Con sông trên bản đồ hả?
R114 | My sofa and my TV? | Ghế sofa và cái tivi hả?
R115 | Is it... mosquitoes? | Là… muỗi hả?
R116 | Airport water? | Nước suối ở sân bay hả?
R118 | Is it... my cheeks? | Là… hai cái má của tôi hả?
R119 | Is it... my salary? | Là… tiền lương của tôi hả?
R121 | Day one, day two, day three? | Ngày một, ngày hai, ngày ba hả?
R122 | Is it... my glasses? | Là… cặp kính của tôi hả?
R124 | Is it... a paper boat? | Là… thuyền giấy hả?
R125 | Is it... a ghost hand? | Là… bàn tay ma hả?
R126 | A kangaroo! | Con kangaroo!
R133 | A sleeping bat? | Con dơi đang ngủ hả?
R134 | Calling in sick on Monday? | Bệnh xin nghỉ làm thứ Hai hả?
R137 | Is it... a pencil? | Là… cây bút chì hả?
R138 | Is it... a spider? | Là… con nhện hả?
R140 | Because they have GPS? | Vì chúng có GPS hả?
R141 | A hot potato? | Củ khoai nóng hả?
R142 | Winter! | Đông!
R146 | Is it... my phone screen? | Là… màn hình điện thoại hả?
R148 | Five hours! | Năm tiếng!
R162 | Is it... my grandma? | Là… bà của tôi hả?
R163 | Because it is shy? | Vì nó nhút nhát hả?
R166 | A tiny helicopter? | Trực thăng tí hon hả?
R167 | Is it... my patience? | Là… sự kiên nhẫn của tôi hả?
R174 | A snowman without a head? | Người tuyết mất đầu hả?
R175 | Is it... my electricity bill? | Là… hoá đơn tiền điện hả?
R177 | A train? | Tàu hoả hả?
R181 | Is it... a snail? | Là… con ốc sên hả?
R184 | Is it... a ninja? | Là… một ninja hả?
R185 | The inside of my eyelids? | Mặt trong mí mắt hả?
R186 | Is it... an electric fan? | Là… cái quạt điện hả?
R191 | The fridge at midnight? | Tủ lạnh lúc nửa đêm hả?
R195 | The stars? | Mấy ngôi sao hả?
R198 | A square watermelon? | Dưa hấu vuông hả?
R199 | X-ray glasses? | Kính nhìn xuyên thấu hả?
"""
# Sửa lại đáp án / đánh dấu "chỉ tiếng Việt" (chơi chữ, không dịch được)
FIX = {
    'R001': dict(vi_only=1, en_a='A broken arm (pun: "bó tay" = to give up)'),
    'R006': dict(vi_a='Con người', en_a='A human'),
    'R008': dict(vi_only=1, en_a='History ("lịch sử")'), 'R009': dict(vi_only=1, en_a='Society ("xã hội")'),
    'R010': dict(vi_only=1, en_a='An archipelago ("quần đảo")'),
    'R036': dict(vi_a='Tất cả các con vịt', en_a='All ducks'), 'R046': dict(vi_a='Cá khô'),
    'R053': dict(vi_only=1, vi_a='Cái cốc có quai', en_a='A mug ("tai" = handle)'),
    'R081': dict(vi_only=1, en_a='A wheel ("bánh xe")'), 'R082': dict(vi_only=1, en_a='A flag ("lá cờ")'),
    'R099': dict(vi_a='Cái ô'), 'R106': dict(vi_a='Mở tủ, cho voi vào, đóng tủ', en_a='Open it, put it in, close it'),
    'R113': dict(vi_only=1, en_a='The Milky Way ("sông Ngân Hà")'), 'R116': dict(vi_only=1, en_a='Perfume ("nước hoa")'),
    'R126': dict(vi_a='Mọi thứ, vì toà nhà đâu biết nhảy', en_a="Anything. Buildings can't jump"),
    'R133': dict(vi_a='Nhũ băng'), 'R177': dict(vi_only=1, en_a='A cake truck ("bánh" = cake or wheel)'),
    'R191': dict(vi_a='Cái miệng, khi lỡ lời', en_q='What is the easiest thing to open but the hardest to close?', en_a='Your mouth'),
    'R198': dict(vi_only=1, en_a='A dumbbell ("quả tạ")'),
}

# Câu mới: câu đố VI | đáp án VI | riddle EN | answer EN | Robot đoán (EN) | (VI) | V = chỉ tiếng Việt
NEW = """
Cái gì bạn càng bước nhiều thì càng để lại nhiều phía sau? | Dấu chân | The more you take, the more you leave behind. What are they? | Footsteps | Is it... my money? | Là… tiền của tôi hả?
Cái gì có một mắt mà không nhìn thấy gì? | Cây kim | What has one eye but cannot see? | A needle | A sleepy pirate? | Cướp biển buồn ngủ hả?
Cái gì bạn có thể làm vỡ dù chưa hề chạm vào? | Lời hứa | What can you break without ever touching it? | A promise | Is it... the Wi-Fi? | Là… cái Wi-Fi hả?
Cái gì lên xuống suốt ngày mà vẫn đứng yên một chỗ? | Cầu thang | What goes up and down all day but never moves? | The stairs | Is it... my mood? | Là… tâm trạng của tôi hả?
Tôi nói được mọi thứ tiếng dù không có miệng. Tôi là gì? | Tiếng vọng | I can speak every language without a mouth. What am I? | An echo | Google Translate? | Google Dịch hả?
Cái gì có răng mà chỉ ăn toàn gỗ? | Cái cưa | What has teeth and eats only wood? | A saw | A hungry beaver? | Con hải ly đói bụng hả?
Hai người mẹ và hai người con gái đi ăn, chỉ gọi 3 suất mà ai cũng có phần. Vì sao? | Họ là bà, mẹ và con gái | Two mothers and two daughters order only 3 meals, yet each gets one. How? | They are a grandma, a mom and a daughter | One of them is on a diet? | Một người đang ăn kiêng hả?
Một người đi dưới mưa không ô, không mũ mà không ướt sợi tóc nào. Vì sao? | Vì ông ấy hói đầu | A man walks in the rain with no umbrella and no hat, yet not a single hair gets wet. Why? | He is bald | He runs really fast? | Ông ấy chạy siêu nhanh hả?
Gà trống đẻ một quả trứng trên nóc nhà. Trứng sẽ lăn về bên nào? | Gà trống đâu có đẻ trứng | A rooster lays an egg on top of the roof. Which way does it roll? | Roosters don't lay eggs | To the left! | Lăn sang trái!
Một ký sắt và một ký bông, cái nào nặng hơn? | Bằng nhau | Which is heavier: a kilo of iron or a kilo of cotton? | They weigh the same | Iron, of course! | Sắt chứ còn gì nữa!
Trong bể có 10 con cá, 2 con chết đuối. Còn lại mấy con? | Vẫn 10 con, cá đâu có chết đuối | There are 10 fish in a tank and 2 of them drown. How many are left? | Still 10. Fish can't drown | Eight! | Tám con!
Bạn đang thi chạy và vượt qua người đứng thứ hai. Bạn đang đứng thứ mấy? | Thứ hai | You are in a race and you overtake the person in second place. What place are you in? | Second place | First place! | Hạng nhất!
Trên bàn có 3 quả táo, bạn lấy đi 2 quả. Bạn có mấy quả? | 2 quả | There are 3 apples and you take away 2. How many do you have? | Two | One! | Một quả!
Bác nông dân có 5 đống rơm ở ruộng này và 4 đống ở ruộng kia. Gom hết lại thì được mấy đống? | Một đống | A farmer has 5 haystacks in one field and 4 in another. If he puts them all together, how many does he have? | One | Nine! | Chín đống!
Từ nào trong từ điển lúc nào cũng bị viết sai? | Từ "sai" | Which word in the dictionary is always spelled wrong? | The word "wrong" | Is it... my name? | Là… tên của tôi hả?
Nửa đêm điện thoại reo, bạn mở cái gì ra trước tiên? | Mở mắt | The phone rings at midnight. What do you open first? | Your eyes | The fridge? | Cái tủ lạnh hả?
Vào phòng tối có cây nến, đèn dầu và bếp củi, bạn chỉ còn một que diêm. Bạn châm cái gì trước? | Que diêm | You enter a dark room with a candle, an oil lamp and a stove. You have one match. What do you light first? | The match | The candle! | Cây nến!
Bác sĩ đưa 3 viên thuốc, dặn cứ nửa tiếng uống một viên. Bao lâu thì uống hết? | 1 tiếng | A doctor gives you 3 pills and says to take one every half hour. How long until they are all gone? | One hour | An hour and a half! | Một tiếng rưỡi!
Cái gì có 13 trái tim mà không có lá phổi nào? | Bộ bài | What has 13 hearts but no lungs? | A deck of cards | Valentine's Day? | Ngày Valentine hả?
Cái gì khi đem chia sẻ thì lại tăng gấp đôi? | Niềm vui | What doubles when you share it? | Joy | Is it... my pizza? | Là… cái bánh pizza của tôi hả?
Cái gì đen khi sạch và trắng khi bẩn? | Cái bảng đen | What is black when it is clean and white when it is dirty? | A blackboard | Is it... a panda? | Là… con gấu trúc hả?
Con gì đi ngủ mà vẫn mang giày? | Con ngựa | What goes to sleep with its shoes on? | A horse | My dad after work? | Bố tôi lúc đi làm về hả?
Con gì càng to càng nhỏ? | Con cua | | A crab ("càng" = claw) | A shy elephant? | Con voi nhút nhát hả? | V
Con gì đầu dê mình ốc? | Con dốc | | A slope: "d" from dê + "ốc" | A goat in a shell? | Con dê chui vỏ ốc hả? | V
Ở Việt Nam, rồng bay lên ở đâu và đáp xuống ở đâu? | Bay ở Thăng Long, đáp ở Hạ Long | | Thăng Long = rising dragon, Hạ Long = landing dragon | At the airport? | Ở sân bay hả? | V
Tháng nào ngắn nhất trong năm? | Tháng Ba và tháng Tư, chỉ có 2 chữ cái | | "Ba" and "Tư": only two letters | February, I am sure! | Tháng Hai, chắc chắn luôn! | V
Núi nào bị chặt ra từng khúc? | Núi Thái Sơn | | Mount Thái Sơn ("thái" = to slice) | A mountain of cake? | Núi bánh kem hả? | V
Cái gì đánh cha, đánh mẹ, đánh anh, đánh chị, đánh em mà ai cũng cần? | Bàn chải đánh răng | | A toothbrush ("đánh răng" = brush teeth) | A naughty kid? | Đứa trẻ hư hả? | V
Con trai có gì quý nhất? | Ngọc trai | | A pearl ("con trai" = boy or clam) | His phone? | Cái điện thoại hả? | V
Bỏ ngoài, nướng trong, ăn ngoài, bỏ trong. Là cái gì? | Bắp ngô | You throw away the outside and cook the inside. Then you eat the outside and throw away the inside. What is it? | Corn on the cob | A pizza box? | Hộp bánh pizza hả?
Môn thể thao nào càng thắng càng thua? | Đua xe đạp | | Cycling ("thắng" = win or brake) | Arguing with my mom? | Môn cãi nhau với mẹ hả? | V
Xe gì không bao giờ giảm? | Xe tăng | | A tank ("tăng" = increase) | My dad's old bike? | Xe đạp cũ của bố hả? | V
Hoa gì biết ăn, biết nói, biết hát? | Hoa hậu | | A beauty queen ("hoa hậu") | A sunflower with a phone? | Hoa hướng dương cầm điện thoại hả? | V
Sở thú bị cháy, con gì chạy ra đầu tiên? | Con người | The zoo is on fire. Which animal runs out first? | The humans | The cheetah! | Con báo!
Đàn chim đậu trên cành, thợ săn bắn cái rằm. Hỏi chết mấy con? | 15 con | | 15 ("rằm" = the fifteenth) | They all flew away? | Bay hết rồi hả? | V
Vì sao hươu cao cổ có cái cổ dài? | Vì đầu nó ở xa thân quá | Why does a giraffe have such a long neck? | Because its head is so far from its body | To catch the Wi-Fi? | Để bắt sóng Wi-Fi hả?
Tôi cao khi còn trẻ và thấp khi về già. Tôi là gì? | Cây nến | I am tall when I am young and short when I am old. What am I? | A candle | Is it... my grandpa? | Là… ông nội tôi hả?
Con gì mang đầy kim trên lưng mà không biết may vá? | Con nhím | What carries hundreds of needles but cannot sew? | A hedgehog | My grandma on holiday? | Bà tôi lúc đi du lịch hả?
Cái gì có đầu, có chân mà không có thân, tối nào bạn cũng nằm lên? | Cái giường | What has a head and a foot but no body? | A bed | A very short snake? | Con rắn siêu ngắn hả?
Cái gì bạn mua để ăn nhưng không bao giờ ăn nó? | Đôi đũa | What do you buy for eating but never eat? | Chopsticks | Is it... broccoli? | Là… bông cải xanh hả?
Tôi không sống nhưng tôi lớn lên, không có phổi nhưng cần không khí, gặp nước là tôi chết. Tôi là gì? | Ngọn lửa | I am not alive but I grow. I have no lungs but I need air. Water kills me. What am I? | Fire | A cat taking a bath? | Con mèo bị bắt đi tắm hả?
Việc gì mà tất cả mọi người trên thế giới đều đang làm cùng một lúc? | Già đi | What is everyone in the world doing at the same time? | Getting older | Checking their phones? | Bấm điện thoại hả?
Câu hỏi nào bạn không bao giờ trả lời "Rồi" một cách thật thà được? | "Bạn ngủ chưa?" | What question can you never honestly answer "yes" to? | "Are you asleep?" | "Did you do your homework?" | "Con làm bài tập chưa?" hả?
Cái gì có vua, có hậu mà không có vương quốc? | Bàn cờ vua | What has kings and queens but no kingdom? | A chessboard | A costume party? | Tiệc hoá trang hả?
Cái gì mất đầu vào buổi sáng và có lại vào buổi tối? | Cái gối | What loses its head in the morning and gets it back at night? | A pillow | Is it... a zombie? | Là… một con zombie hả?
Ba bác sĩ đều nói Bình là anh em ruột của họ. Bình nói mình không có anh em trai nào. Ai nói dối? | Không ai cả, ba bác sĩ là chị em gái | Three doctors say Binh is their brother. Binh says he has no brothers. Who is lying? | No one. The doctors are his sisters | The doctors! | Mấy ông bác sĩ!
Một cậu bé ngã từ chiếc thang 20 bậc mà không hề đau. Vì sao? | Vì cậu ngã từ bậc đầu tiên | A boy fell off a 20-step ladder but was not hurt. Why? | He fell from the first step | He can fly? | Cậu ấy biết bay hả?
Làm sao một người có thể thức suốt 8 ngày không ngủ? | Ngủ vào ban đêm | How can someone go 8 days without sleep? | They sleep at night | Too much coffee? | Uống quá nhiều cà phê hả?
Trên bàn có 5 con ruồi, bạn đập chết 1 con. Trên bàn còn mấy con? | Còn 1 con, là con đã chết | There are 5 flies on the table and you swat one. How many are left on the table? | One. The others flew away | Four! | Bốn con!
Quả gì có đủ năm châu bốn biển? | Quả địa cầu | | A globe ("quả địa cầu") | A giant watermelon? | Quả dưa hấu khổng lồ hả? | V
Hai lưỡi mà chẳng có răng, cắt gì cũng đứt. Là cái gì? | Cái kéo | Two blades and no teeth, yet it cuts through anything. What is it? | Scissors | A two-headed shark? | Cá mập hai đầu hả?
Da trắng muốt, ruột trắng tinh, bạn với học sinh, thích cọ đầu vào bảng. Là cái gì? | Viên phấn | White skin, white heart, a student's friend that loves rubbing its head on the board. What is it? | A piece of chalk | A polar bear at school? | Gấu Bắc Cực đi học hả?
Chẳng phải trâu bò mà uống nước ao sâu, lên cày ruộng cạn. Là cái gì? | Cây bút mực | It is not a buffalo, yet it drinks from a deep pond and ploughs a dry field. What is it? | A fountain pen | A thirsty buffalo? | Con trâu khát nước hả?
Vừa bằng hạt đỗ, ăn giỗ cả làng. Là con gì? | Con ruồi | As small as a bean, yet it eats at every feast in the village. What is it? | A fly | My little cousin? | Thằng em họ tôi hả?
Sừng sững đứng giữa nhà, ai vào không hỏi, ai ra không chào. Là cái gì? | Cái cột nhà | It stands in the middle of the house and never greets anyone coming or going. What is it? | A pillar | Is it... my cat? | Là… con mèo nhà tôi hả?
Chân đen mình trắng, đứng nắng giữa đồng. Là con gì? | Con cò | Black legs, white body, standing in the sun in the rice field. What is it? | A stork | A snowman wearing boots? | Người tuyết đi ủng hả?
Xưa ở bụi tre, mùa đông xếp lại, mùa hè mở ra. Là cái gì? | Cái quạt giấy | It came from bamboo. It is folded in winter and opened in summer. What is it? | A paper fan | An ice cream shop? | Tiệm kem hả?
Năm anh em ở chung một nhà: bốn anh lên ba, riêng một anh mới lên hai. Là gì? | Bàn tay: ngón cái chỉ có hai đốt | Five brothers live together. Four are three years old, but one is only two. What are they? | Fingers. The thumb has only two joints | A boy band? | Một nhóm nhạc nam hả?
Hai cô nằm nghỉ hai phòng, ngày thì mở cửa ra trông, đêm thì đóng cửa. Là gì? | Đôi mắt | Two sisters live in two rooms. They open the doors by day and close them at night. What are they? | Your eyes | Two shops? | Hai cửa tiệm hả?
Một mẹ có sáu đứa con, yêu thương mẹ sẻ nước non vơi đầy. Là gì? | Bộ ấm chén | A mother has six children and shares her water with every one of them. What is it? | A teapot and cups | A mother duck? | Vịt mẹ hả?
Nhà xanh lại đóng đố xanh, tra đỗ, trồng hành, thả lợn vào trong. Là cái gì? | Bánh chưng | | Bánh chưng, the Tết rice cake | A tiny farm? | Nông trại tí hon hả? | V
Bằng cái vung, vùng xuống ao, đào chẳng thấy, lấy chẳng được. Là cái gì? | Bóng mặt trăng | Round like a pot lid, it drops into the pond. You can't dig it out or pick it up. What is it? | The moon's reflection | My lost phone? | Điện thoại tôi làm rơi hả?
Không sơn mà đỏ, không gõ mà kêu, không khều mà rụng. Là những gì? | Mặt trời, sấm và mưa | Red without paint, loud without a knock, falling without a push. What are they? | The sun, thunder and rain | A tomato, a rooster and me? | Cà chua, gà trống và tôi hả?
Lưng đằng trước, bụng đằng sau, con mắt ở dưới, cái đầu ở trên. Là cái gì? | Cái chân | Its back is in front and its belly is behind. Its eye is at the bottom and its head is at the top. What is it? | Your leg | A shirt worn backwards? | Cái áo mặc ngược hả?
Thứ gì mỗi ngày phải mất đi một tờ thì mới làm tròn nhiệm vụ? | Cuốn lịch xé | What must lose a page every day to do its job? | A tear-off calendar | Is it... my wallet? | Là… cái ví của tôi hả?
Ở đâu thì "hôm nay" đứng trước "hôm qua"? | Trong từ điển | Where does today come before yesterday? | In a dictionary | In a time machine? | Trong cỗ máy thời gian hả?
Cái gì lên núi, xuống đồi, đi khắp nơi mà vẫn nằm im một chỗ? | Con đường | What goes up and down the hills but never moves? | A road | A lazy hiker? | Người leo núi lười hả?
Số nào khi lật ngược lại thì tăng thêm 3? | Số 6 | Which number gets bigger by 3 when you turn it upside down? | The number 6 | My test score? | Điểm kiểm tra của tôi hả?
Một nửa của hai, cộng thêm hai, bằng mấy? | Bằng 3 | What is half of two, plus two? | Three | Two! | Bằng hai!
5 con mèo bắt 5 con chuột trong 5 phút. Vậy 1 con mèo bắt 1 con chuột trong mấy phút? | 5 phút | 5 cats catch 5 mice in 5 minutes. How long does 1 cat need to catch 1 mouse? | 5 minutes | One minute! | Một phút!
Bèo trong ao mỗi ngày tăng gấp đôi, đến ngày thứ 30 thì phủ kín ao. Ngày thứ mấy bèo phủ nửa ao? | Ngày thứ 29 | The lily pads in a pond double every day and cover it on day 30. On which day is the pond half covered? | Day 29 | Day 15! | Ngày 15!
Giỏ có 6 quả trứng, 6 người mỗi người lấy 1 quả mà trong giỏ vẫn còn 1 quả. Vì sao? | Người cuối lấy luôn cả giỏ | There are 6 eggs in a basket. 6 people each take one, yet one egg is still in the basket. How? | The last person took the basket too | A chicken is hiding inside? | Có con gà trốn trong giỏ hả?
Có tôi thì bạn muốn chia sẻ, chia sẻ rồi thì bạn không còn tôi nữa. Tôi là gì? | Bí mật | If you have me, you want to share me. If you share me, you no longer have me. What am I? | A secret | Is it... my sandwich? | Là… cái bánh mì của tôi hả?
Cái gì không bao giờ hỏi nhưng lúc nào cũng được trả lời? | Chuông điện thoại | What never asks a question but always gets answered? | A ringing phone | A text from my boss? | Tin nhắn của sếp hả?
Người nghèo có, người giàu cần, ai ăn nó thì đói lả. Là cái gì? | Không có gì cả | The poor have it, the rich need it, and if you eat it you starve. What is it? | Nothing | Instant noodles? | Mì gói hả?
Một người cạo râu nhiều lần mỗi ngày mà vẫn có râu. Ông ấy là ai? | Thợ cắt tóc | A man shaves several times a day but still has a beard. Who is he? | A barber | A werewolf? | Người sói hả?
Con gì ngủ mà không bao giờ nhắm mắt? | Con cá | Which animal sleeps with its eyes open? | A fish | Me, in math class? | Tôi trong giờ Toán hả?
Con vật nào không thể đi lùi? | Con kangaroo | Which animal cannot walk backwards? | A kangaroo | My stubborn uncle? | Ông chú bướng bỉnh của tôi hả?
Con vật nào có tới ba trái tim? | Con bạch tuộc | Which animal has three hearts? | An octopus | A K-pop fan? | Một fan K-pop hả?
Loài chim nào không biết bay nhưng bơi giỏi như vận động viên? | Chim cánh cụt | Which bird cannot fly but swims like a champion? | A penguin | A wet chicken? | Con gà bị ướt hả?
Quả gì đội vương miện? | Quả dứa | Which fruit wears a crown? | A pineapple | The king's apple? | Quả táo của nhà vua hả?
Hạt gì rơi xuống mà không ai nhặt? | Hạt mưa | | A raindrop ("hạt mưa") | A chili seed? | Hạt ớt cay hả? | V
Nước gì không uống được mà ai cũng yêu? | Đất nước | | Your homeland ("đất nước") | Fish sauce? | Nước mắm hả? | V
Đường gì không ngọt mà ngày nào cũng dùng? | Đường đi | | A road ("đường" = sugar or road) | Sugar-free sugar? | Đường không đường hả? | V
Sữa gì không uống được? | Sữa rửa mặt | | Face wash ("sữa rửa mặt") | Expired milk? | Sữa hết hạn hả? | V
Mắt gì nằm ở dưới chân? | Mắt cá chân | | Your ankle ("mắt cá chân") | A fish that can walk? | Con cá biết đi hả? | V
Cầu gì có bảy màu mà không ai đi qua được? | Cầu vồng | | A rainbow ("cầu vồng") | A bridge in a cartoon? | Cây cầu trong phim hoạt hình hả? | V
Trăng gì không nằm trên trời? | Trăng mật | | A honeymoon ("trăng mật") | The moon in my soup? | Mặt trăng trong bát canh hả? | V
Tiền gì không tiêu được mà rất hay ghi bàn? | Tiền đạo | | A striker in football ("tiền đạo") | Toy money? | Tiền đồ chơi hả? | V
Đồng gì không đúc được mà bát ngát lúa vàng? | Cánh đồng | | A rice field ("cánh đồng") | A gold coin farm? | Nông trại tiền vàng hả? | V
Tay gì không cầm nắm được? | Tay áo | | A sleeve ("tay áo") | A robot arm with no battery? | Tay robot hết pin hả? | V
Chân gì ở tít trên trời? | Chân trời | | The horizon ("chân trời") | A bird's leg? | Chân con chim hả? | V
Miệng gì không ăn mà to hơn cả ngôi nhà? | Miệng núi lửa | | A volcano crater ("miệng núi lửa") | A yawning hippo? | Con hà mã đang ngáp hả? | V
Mũi gì không ngửi được mà bay rất nhanh? | Mũi tên | | An arrow ("mũi tên") | My nose when I have a cold? | Mũi tôi lúc bị cảm hả? | V
Ngôi sao nào không ở trên trời mà nằm dưới biển? | Sao biển | Which star lives in the sea, not in the sky? | A starfish | A movie star on vacation? | Ngôi sao điện ảnh đi nghỉ mát hả?
Con ngựa nào sống dưới biển và không bao giờ ăn cỏ? | Cá ngựa | Which horse lives in the sea and never eats grass? | A seahorse | A horse with a snorkel? | Con ngựa đeo ống thở hả?
Cái gì có bốn chân, một cái lưng mà không có đầu? | Cái ghế | What has four legs and a back but no head? | A chair | An invisible horse? | Con ngựa tàng hình hả?
Cái gì có một lối vào và hai lối ra? | Cái quần | What has one way in and two ways out? | A pair of trousers | A haunted house? | Ngôi nhà ma hả?
Cái gì đi khắp nhà rồi lại đứng yên trong góc? | Cái chổi | What goes all around the house and then stands in the corner? | A broom | My cousin, the robot vacuum? | Anh họ robot hút bụi của tôi hả?
Trước khi lên giường, thứ cuối cùng bạn nhấc ra là gì? | Đôi chân khỏi sàn nhà | What is the last thing you take off before getting into bed? | Your feet off the floor | My socks! | Đôi tất!
Cái gì vào thì dễ mà ra thì khó? | Rắc rối | What is easy to get into but hard to get out of? | Trouble | My bed in the morning? | Cái giường buổi sáng hả?
Ai kiếm tiền bằng cách chở khách của mình đi chỗ khác? | Tài xế taxi | Who gets paid for driving customers away? | A taxi driver | A grumpy waiter? | Anh bồi bàn khó tính hả?
Cái gì làm bạn khóc mà không nói một lời nào? | Củ hành | What can make you cry without saying a word? | An onion | My bank account? | Tài khoản ngân hàng của tôi hả?
Nhà gì lạnh nhất? | Nhà băng | | A bank ("nhà băng": "băng" = ice) | A penguin's house? | Nhà của chim cánh cụt hả? | V
Cây gì không cần trồng, mát lạnh, trẻ con đứa nào cũng mê? | Cây kem | | An ice cream ("cây kem") | A Christmas tree in the freezer? | Cây thông trong tủ đá hả? | V
Bánh gì mới nghe tên đã thấy đau? | Bánh tét | | Bánh tét ("tét" = to spank) | A cake made of bricks? | Bánh làm bằng gạch hả? | V
Bánh gì mới nghe tên đã thấy sướng? | Bánh khoái | | Bánh khoái ("khoái" = delighted) | Free cake? | Bánh miễn phí hả? | V
Thành gì không xây bằng gạch mà ai cũng muốn đạt được? | Thành công | | Success ("thành công") | The Great Wall? | Vạn Lý Trường Thành hả? | V
Chữ gì mất đầu là hỏi, mất đuôi là trả lời? | Chữ "tai": bỏ đầu còn "ai", bỏ đuôi còn "ta" | | The word "tai": "ai" = who, "ta" = me | A broken question mark? | Dấu hỏi bị gãy hả? | V
"""

# Đuổi hình bắt chữ: emoji | loại | đáp án VI | nghĩa đen EN | ý nghĩa EN | Robot đoán (EN) | (VI)
EMOJI = """
🐸 🪑 🕳️ | TN | Ếch ngồi đáy giếng | A frog sitting at the bottom of a well | Meaning: a narrow view of the world | A frog on a chair fell in a hole? | Con ếch ngồi ghế rơi xuống lỗ hả?
🐘 🕳️ 🪡 | TN | Voi chui lỗ kim | An elephant through the eye of a needle | Meaning: something impossible | An elephant doing some sewing? | Con voi đang may vá hả?
🎸 👂 🐃 | TN | Đàn gảy tai trâu | Playing music to a buffalo's ears | Meaning: talking to someone who won't listen | A buffalo rock concert? | Buổi hoà nhạc rock của trâu hả?
🐭 ⬇️ 🍚 | TN | Chuột sa chĩnh gạo | A mouse falls into a jar of rice | Meaning: a sudden stroke of luck | A mouse ordering lunch? | Con chuột gọi cơm trưa hả?
🐱 😭 🐭 | TN | Mèo khóc chuột | A cat crying for a mouse | Meaning: fake sympathy | A sad cat movie? | Phim buồn về con mèo hả?
👴 🐔 👵 🦆 | TN | Ông nói gà bà nói vịt | Grandpa says chicken, grandma says duck | Meaning: two people talking about different things | Grandparents at the zoo? | Ông bà đi sở thú hả?
💧 ➡️ 🪨 | TU | Nước chảy đá mòn | Flowing water wears away stone | Meaning: persistence beats anything | A rock taking a shower? | Hòn đá đi tắm hả?
🔥 🧪 🥇 | TU | Lửa thử vàng | Fire tests gold | Meaning: hardship shows true worth | A gold medal in chemistry? | Huy chương vàng môn Hoá hả?
👂 🧱 🌳 | TN | Tai vách mạch rừng | Walls have ears | Meaning: be careful, secrets spread | An ear stuck in a wall? | Cái tai kẹt trong tường hả?
🐟 🤝 💧 | TN | Như cá gặp nước | Like a fish meeting water | Meaning: being in your element | A fish signing a contract? | Con cá ký hợp đồng hả?
🥚 ⚔️ 🪨 | TN | Trứng chọi đá | An egg fighting a rock | Meaning: a hopeless fight | An egg ninja? | Ninja trứng hả?
🏇 👀 🌸 | TN | Cưỡi ngựa xem hoa | Riding a horse to look at flowers | Meaning: doing things in a rush | A horse on a date? | Con ngựa đi hẹn hò hả?
🐅 ➡️ 🌳 | TN | Thả hổ về rừng | Sending the tiger back to the forest | Meaning: letting a dangerous rival go | A tiger going camping? | Con hổ đi cắm trại hả?
✏️ 🐍 ➕ 🦶 | TN | Vẽ rắn thêm chân | Drawing a snake and adding legs | Meaning: spoiling something by overdoing it | A snake buying shoes? | Con rắn đi mua giày hả?
💧 🍃 🥔 | TN | Nước đổ lá khoai | Water poured on a taro leaf | Meaning: advice that has no effect | Potato soup? | Canh khoai tây hả?
🤿 🪡 🌊 | TN | Mò kim đáy biển | Searching for a needle at the bottom of the sea | Meaning: an almost impossible search | A fish getting a vaccine? | Con cá đi tiêm vắc-xin hả?
🐜 ⏳ 🏠 | TU | Kiến tha lâu đầy tổ | Ants carrying little by little fill the nest | Meaning: small efforts add up | An ant paying rent? | Con kiến trả tiền thuê nhà hả?
🍯 💀 🪰 | TU | Mật ngọt chết ruồi | Sweet honey kills flies | Meaning: beware of sweet words | A haunted honey shop? | Tiệm mật ong ma ám hả?
🦆 👂 ⛈️ | TN | Vịt nghe sấm | A duck listening to thunder | Meaning: hearing without understanding | A duck weather reporter? | Con vịt dự báo thời tiết hả?
🐶 🥱 🪰 | TN | Chó ngáp phải ruồi | A yawning dog catches a fly | Meaning: pure dumb luck | A sleepy dog's breakfast? | Bữa sáng của con chó buồn ngủ hả?
🐓 🍼 👶 | TN | Gà trống nuôi con | A rooster raising the chicks | Meaning: a single father raising his kids | A chicken babysitter? | Con gà trông trẻ hả?
🍎 🧠 🌱 | TU | Ăn quả nhớ kẻ trồng cây | When you eat the fruit, remember who planted the tree | Meaning: be grateful | A very smart apple? | Quả táo thông minh hả?
🥤 🧠 ⛲ | TU | Uống nước nhớ nguồn | When you drink water, remember the spring | Meaning: never forget your roots | Brain freeze? | Uống lạnh buốt óc hả?
🐋 😋 🐟 | TU | Cá lớn nuốt cá bé | Big fish swallow small fish | Meaning: the strong beat the weak | A whale at a sushi bar? | Cá voi đi ăn sushi hả?
🖋️ ⚫ 💡 ✨ | TU | Gần mực thì đen gần đèn thì sáng | Near ink you turn black, near a lamp you shine | Meaning: you become like your friends | A pen fixing a lamp? | Cây bút sửa bóng đèn hả?
🐴 🔁 🛣️ | TN | Ngựa quen đường cũ | The horse goes back to its old road | Meaning: old habits die hard | A horse stuck in traffic? | Con ngựa bị kẹt xe hả?
✋ 🔨 😋 | TU | Tay làm hàm nhai | Hands that work get food to chew | Meaning: you must work to eat | Eating a hammer? | Ăn cái búa hả?
🚶 🛣️ 🎓 | TU | Đi một ngày đàng học một sàng khôn | Travel for a day, learn a basket of wisdom | Meaning: travel makes you wiser | Walking to university? | Đi bộ tới trường đại học hả?
🗣️ 💨 | TU | Lời nói gió bay | Spoken words fly away with the wind | Meaning: spoken promises are easily forgotten | Someone talking too fast? | Ai đó nói quá nhanh hả?
🏃 ⚡ | TN | Nhanh như chớp | As fast as lightning | Meaning: extremely fast | Running from the electricity bill? | Chạy trốn hoá đơn tiền điện hả?
💪 🐘 | TN | Khoẻ như voi | As strong as an elephant | Meaning: very strong | An elephant at the gym? | Con voi đi tập gym hả?
🤐 🦪 | TN | Câm như hến | As silent as a clam | Meaning: saying absolutely nothing | A secret seafood recipe? | Công thức hải sản bí mật hả?
😱 🐰 | TN | Nhát như thỏ | As timid as a rabbit | Meaning: easily scared | A scary bunny movie? | Phim kinh dị về thỏ hả?
🦊 👴 | TN | Cáo già | An old fox | Meaning: a cunning, experienced person | The fox's grandpa? | Ông nội của con cáo hả?
👨 ⛰️ | TU | Công cha như núi Thái Sơn | A father's devotion is as great as a mountain | A line from a beloved folk verse | Dad goes hiking? | Bố đi leo núi hả?
👩 💧 ⛲ | TU | Nghĩa mẹ như nước trong nguồn | A mother's love flows like water from the spring | The next line of the same folk verse | Mom washing the dishes? | Mẹ đang rửa bát hả?
🍃 🤗 🍂 | TU | Lá lành đùm lá rách | Whole leaves wrap torn leaves | Meaning: those who have more help those in need | Leaves at a hug party? | Lá cây mở tiệc ôm nhau hả?
🌲 🌲 🌲 ⛰️ | TU | Ba cây chụm lại nên hòn núi cao | Three trees together make a high mountain | Meaning: unity is strength | A tiny forest? | Khu rừng tí hon hả?
🐴 🤕 🚫 🌾 | TU | Một con ngựa đau cả tàu bỏ cỏ | When one horse is sick, the whole stable stops eating | Meaning: sharing each other's pain | A horse on a diet? | Con ngựa ăn kiêng hả?
⚒️ ⏳ 🪡 | TU | Có công mài sắt có ngày nên kim | Grind iron long enough and it becomes a needle | Meaning: perseverance pays off | A very slow tailor? | Ông thợ may siêu chậm hả?
🐟 🚫 🧂 | TU | Cá không ăn muối cá ươn | A fish without salt goes bad | Meaning: children who don't listen go astray | A fish on a low-salt diet? | Con cá ăn nhạt hả?
🌧️ ⏳ 💦 | TU | Mưa dầm thấm lâu | Steady rain soaks deep | Meaning: slow, steady effort works | Waiting for the bus in the rain? | Đợi xe buýt dưới mưa hả?
⛵ 💨 | TN | Thuận buồm xuôi gió | Smooth sails and a fair wind | Meaning: everything goes smoothly | A boat running late? | Con thuyền đi trễ hả?
💯 👂 🆚 👀 | TU | Trăm nghe không bằng một thấy | Hearing a hundred times is not as good as seeing once | Meaning: seeing is believing | An ear fighting an eye? | Tai đánh nhau với mắt hả?
🐛 😞 🍲 | TU | Con sâu làm rầu nồi canh | One worm spoils the pot of soup | Meaning: one bad member ruins the group | Worm soup? Yuck! | Canh sâu hả? Eo ôi!
⏰ 🥇 | TU | Thời gian là vàng | Time is gold | Meaning: time is precious | A gold medal for waking up early? | Huy chương vàng dậy sớm hả?
📖 🤝 🛠️ | TU | Học đi đôi với hành | Learning goes hand in hand with practice | Meaning: use what you learn | A book fixing a car? | Quyển sách sửa xe hả?
🌱 😊 🐦 | TU | Đất lành chim đậu | Birds settle on good land | Meaning: good places attract good people | A happy bird farmer? | Bác chim nông dân vui vẻ hả?
🐃 👑 | TU | Con trâu là đầu cơ nghiệp | The buffalo is the heart of the farm | An old farming saying | King Buffalo the First? | Vua Trâu đệ nhất hả?
🐱 🕶️ 🐟 🔥 | TN | Mèo mù vớ cá rán | A blind cat stumbles on a fried fish | Meaning: an unexpected stroke of luck | A cool cat having a barbecue? | Mèo ngầu đi ăn đồ nướng hả?
🛢️ 💨 📢 | TN | Thùng rỗng kêu to | Empty barrels make the most noise | Meaning: those who know little talk the most | A barrel giving a speech? | Cái thùng đang phát biểu hả?
📄 ✂️ 📏 | TU | Giấy rách phải giữ lấy lề | Even torn paper must keep its margin | Meaning: keep your dignity in hard times | Arts and crafts class? | Giờ thủ công hả?
🩸 🆚 💧 | TU | Một giọt máu đào hơn ao nước lã | A drop of blood is worth more than a pond of water | Meaning: family comes first | A vampire choosing a drink? | Ma cà rồng chọn đồ uống hả?
👧 🤕 👦 🤝 | TU | Chị ngã em nâng | When the sister falls, the brother lifts her up | Meaning: siblings support each other | A playground accident? | Tai nạn ở sân chơi hả?
🥣 🦶 💥 | TN | Ăn cháo đá bát | Eating the porridge, then kicking the bowl | Meaning: being ungrateful | Football with a bowl? | Đá bóng bằng cái bát hả?
🌉 🚶 🪵 | TN | Qua cầu rút ván | Crossing the bridge, then pulling up the planks | Meaning: abandoning those who helped you | Someone stealing a bridge? | Ai đó trộm cây cầu hả?
🧍 ⛰️ 👀 ⛰️ | TN | Đứng núi này trông núi nọ | Standing on this mountain, looking at that one | Meaning: never happy with what you have | A lost tourist? | Du khách bị lạc hả?
🌊 🦶 🤾 | TN | Nước đến chân mới nhảy | Jumping only when the water reaches your feet | Meaning: leaving things to the last minute | Beach volleyball? | Bóng chuyền bãi biển hả?
🐄 ❓ 🔨 🏚️ | TN | Mất bò mới lo làm chuồng | Building the barn after the cow is lost | Meaning: acting too late | A cow playing hide and seek? | Con bò chơi trốn tìm hả?
🐸 💀 👄 | TN | Ếch chết tại miệng | The frog dies because of its mouth | Meaning: talking too much brings trouble | A frog ate too much chili? | Con ếch ăn quá nhiều ớt hả?
🔥 🏠 🐭 | TN | Cháy nhà ra mặt chuột | When the house burns, the rats show their faces | Meaning: a crisis reveals who people really are | A mouse firefighter? | Chuột lính cứu hoả hả?
🌳 🥇 🌊 🥈 | TN | Rừng vàng biển bạc | Golden forests, silver seas | Meaning: a land rich in resources | The nature Olympics? | Thế vận hội thiên nhiên hả?
⬆️ 🐘 ⬇️ 🐶 | TN | Lên voi xuống chó | Up on an elephant, down on a dog | Meaning: the ups and downs of life | An elevator for animals? | Thang máy cho thú hả?
🐘 ➡️ 🐭 | TN | Đầu voi đuôi chuột | An elephant's head, a mouse's tail | Meaning: a grand start, a weak finish | An elephant shrinking machine? | Máy thu nhỏ con voi hả?
🌧️ 👍 💨 | TN | Mưa thuận gió hoà | Timely rain and gentle wind | Meaning: good weather, a good harvest | A five-star review for a storm? | Chấm 5 sao cho cơn bão hả?
☀️ 🌫️ 🌫️ | TN | Một nắng hai sương | One sun, two dews | Meaning: working hard from dawn to dusk | Today's weather forecast? | Dự báo thời tiết hôm nay hả?
🎋 👴 🌱 | TU | Tre già măng mọc | When the bamboo grows old, young shoots spring up | Meaning: the young follow the old | Grandpa's garden? | Vườn của ông nội hả?
🌳 📏 😎 | TU | Cây ngay không sợ chết đứng | A straight tree fears nothing | Meaning: honest people have nothing to fear | The coolest tree in school? | Cái cây ngầu nhất trường hả?
🐃 🐂 💥 🦟 | TU | Trâu bò húc nhau ruồi muỗi chết | When buffaloes fight, the mosquitoes die | Meaning: the small suffer when the powerful fight | A buffalo wrestling show? | Giải đấu vật của trâu hả?
🤝 💪 | TU | Đoàn kết là sức mạnh | Unity is strength | A motto everyone knows | An arm wrestling deal? | Thoả thuận vật tay hả?
🧧 🧨 🌸 | VH | Tết Nguyên Đán | Lunar New Year | Vietnam's biggest holiday | A red flower explosion? | Vụ nổ hoa đỏ hả?
🌕 🥮 🏮 | VH | Tết Trung thu | The Mid-Autumn Festival | A night of mooncakes and lanterns | Dinner on the moon? | Ăn tối trên mặt trăng hả?
🥁 🦁 🌕 | VH | Múa lân | The lion dance | Performed at Mid-Autumn and Tết | A lion playing the drums? | Sư tử chơi trống hả?
🎋 👒 | VH | Nón lá | The conical leaf hat | A symbol of Vietnam | A bamboo fashion show? | Trình diễn thời trang tre hả?
👗 💃 🌸 | VH | Áo dài | Áo dài, the long dress | Vietnam's traditional dress | A flower dance party? | Tiệc khiêu vũ hoa hả?
👦 🐃 🎵 | VH | Chú bé chăn trâu thổi sáo | A buffalo boy playing the flute | A classic image of the countryside | A buffalo music teacher? | Trâu dạy nhạc hả?
🪁 🌬️ 👦 | VH | Thả diều | Flying a kite | A favorite summer game | A boy chasing the wind? | Cậu bé đuổi theo gió hả?
🚣 🏁 🥁 | VH | Đua thuyền | Boat racing | A festival tradition on the river | A drum on a boat trip? | Cái trống đi du thuyền hả?
🛵 🚗 🚌 😫 | VH | Kẹt xe | A traffic jam | Daily life in the big city | A party for vehicles? | Tiệc của xe cộ hả?
🍜 🐄 | MA | Phở bò | Beef pho | Vietnam's most famous noodle soup | A cow eating noodles? | Con bò ăn mì hả?
🥖 🥩 🥒 | MA | Bánh mì | Bánh mì sandwich | Loved all around the world | A very long hamburger? | Hamburger siêu dài hả?
☕ 🥛 🧊 | MA | Cà phê sữa đá | Iced milk coffee | The taste of a Vietnamese morning | A coffee snowman? | Người tuyết cà phê hả?
🥚 ☕ | MA | Cà phê trứng | Egg coffee | A creamy Hanoi specialty | Breakfast in one cup? | Bữa sáng trong một cái cốc hả?
🍚 🍗 | MA | Cơm gà | Chicken rice | A simple, tasty classic | A chicken sleeping on rice? | Con gà ngủ trên cơm hả?
🦀 🍜 | MA | Bún riêu cua | Crab noodle soup | A tangy tomato and crab broth | A crab's swimming pool? | Hồ bơi của con cua hả?
🥞 🍤 🥬 | MA | Bánh xèo | Sizzling crispy pancake | Named after its sizzling sound | A shrimp sleeping under a blanket? | Con tôm đắp chăn ngủ hả?
🌯 🍤 🥬 | MA | Gỏi cuốn | Fresh spring rolls | Light, fresh and healthy | A salad burrito? | Burrito rau hả?
💧 🐟 | MA | Nước mắm | Fish sauce | The soul of Vietnamese cooking | A crying fish? | Con cá đang khóc hả?
🍵 🥛 ⚫ | MA | Trà sữa trân châu | Bubble milk tea | The favorite drink of students | Tea with a black hole? | Trà có hố đen hả?
🥥 🍬 | MA | Kẹo dừa | Coconut candy | A sweet gift from Bến Tre | A coconut's birthday? | Sinh nhật quả dừa hả?
🍚 🎋 | MA | Cơm lam | Bamboo-tube rice | Rice cooked inside bamboo | A panda's lunch box? | Hộp cơm của gấu trúc hả?
🥭 🧂 🌶️ | MA | Xoài chấm muối ớt | Green mango with chili salt | Sour, salty and spicy: a perfect snack | An angry mango? | Quả xoài nổi giận hả?
🌽 🔥 🧈 | MA | Bắp rang bơ | Popcorn | The best friend of every movie | A corn in the sauna? | Trái bắp đi xông hơi hả?
🐉 ⬇️ 🌊 | DD | Vịnh Hạ Long | Ha Long Bay | Its name means the descending dragon | A dragon learning to swim? | Con rồng tập bơi hả?
🌉 🐉 🔥 | DD | Cầu Rồng Đà Nẵng | The Dragon Bridge in Da Nang | It breathes fire on weekend nights | A dragon barbecue? | Tiệc nướng của rồng hả?
🏮 🏘️ | DD | Phố cổ Hội An | Hoi An Ancient Town | Famous for its colorful lanterns | A street of lamp shops? | Phố bán đèn hả?
🐢 🗡️ 💧 | DD | Hồ Gươm | Sword Lake in Hanoi | A golden turtle took back the king's sword | A turtle knight? | Rùa hiệp sĩ hả?
🌸 🌲 🍓 | DD | Đà Lạt | Da Lat | The city of flowers, pines and strawberries | A strawberry forest? | Rừng dâu tây hả?
🏝️ 💎 | DD | Đảo ngọc Phú Quốc | Phu Quoc, the Pearl Island | Vietnam's largest island | A pirate treasure map? | Bản đồ kho báu cướp biển hả?
🕳️ ⛰️ 🦇 | DD | Hang Sơn Đoòng | Son Doong Cave | The largest cave in the world | A hotel for bats? | Khách sạn của dơi hả?
🌾 🪜 ⛰️ | DD | Ruộng bậc thang | Terraced rice fields | Giant green stairs in the northern mountains | Stairs for a giant? | Cầu thang cho người khổng lồ hả?
🌉 🥇 🖐️ | DD | Cầu Vàng Đà Nẵng | The Golden Bridge in Da Nang | Held up by two giant stone hands | A high five from a bridge? | Cây cầu đập tay hả?
🏯 👑 | DD | Kinh thành Huế | Hue Imperial City | Home of the Nguyễn kings | A king's video game? | Trò chơi điện tử của vua hả?
🛶 🌴 🥥 | DD | Miền Tây sông nước | The Mekong Delta | A land of rivers, boats and coconuts | A coconut delivery boat? | Thuyền giao dừa hả?
🐻 🐱 | GC | Gấu mèo | Raccoon | In Vietnamese: a bear cat | A bear adopting a cat? | Gấu nhận nuôi mèo hả?
🐟 🐷 | GC | Cá heo | Dolphin | In Vietnamese: a pig fish | A pig learning to swim? | Con heo tập bơi hả?
🐟 🗡️ | GC | Cá kiếm | Swordfish | The same idea in both languages | A fish in a sword fight? | Con cá đấu kiếm hả?
🔥 🚗 | GC | Xe lửa | Train | In Vietnamese: a fire vehicle | A car on fire? Call 114! | Xe bị cháy hả? Gọi 114!
⚡ 🗣️ | GC | Điện thoại | Telephone | In Vietnamese: electric talk | Shouting in a storm? | La hét giữa cơn bão hả?
🚪 ❄️ | GC | Tủ lạnh | Refrigerator | In Vietnamese: a cold cabinet | A door to the North Pole? | Cánh cửa tới Bắc Cực hả?
🐭 💻 | GC | Chuột máy tính | Computer mouse | The same idea in both languages | A mouse doing homework? | Con chuột làm bài tập hả?
👕 🌧️ | GC | Áo mưa | Raincoat | In Vietnamese: a rain shirt | A laundry day disaster? | Thảm hoạ ngày giặt đồ hả?
🏹 🔥 | GC | Tên lửa | Rocket | In Vietnamese: a fire arrow | A barbecue with arrows? | Nướng thịt bằng mũi tên hả?
🦁 🌊 | GC | Sư tử biển | Sea lion | The same idea in both languages | A lion on a surfboard? | Sư tử lướt sóng hả?
🌉 🪶 | GC | Cầu lông | Badminton | In Vietnamese: a feather shuttle | A bridge for birds? | Cây cầu cho chim hả?
🚩 👑 | GC | Cờ vua | Chess | In Vietnamese: the king's game | A king waving a flag? | Nhà vua vẫy cờ hả?
🌶️ 🔔 | GC | Ớt chuông | Bell pepper | The same idea in both languages | A spicy doorbell? | Chuông cửa cay xè hả?
🟢 🐉 | GC | Thanh long | Dragon fruit | In Vietnamese: a green dragon | A dragon that ate too much salad? | Con rồng ăn quá nhiều rau hả?
🐉 👁️ | GC | Long nhãn | Longan | Its name means the dragon's eye | A dragon at the eye doctor? | Con rồng đi khám mắt hả?
🌸 ➡️ ☀️ | GC | Hoa hướng dương | Sunflower | In Vietnamese: the flower facing the sun | A flower on a beach trip? | Bông hoa đi biển hả?
"""


# Theo mùa: khoảng ngày (dd/MM-dd/MM) || câu đố VI | đáp án | riddle EN | answer EN | Robot đoán EN | VI | V
SEASON_R = """
19/11-20/11 || Ai dạy bạn bao điều hay, chẳng đòi trả ơn, chỉ mong bạn giỏi hơn mình? | Thầy cô giáo | Who teaches you so much and only hopes you become better than them? | Your teachers | Is it... YouTube? | Là… YouTube hả?
19/11-20/11 || Nghề gì đưa hàng nghìn người sang sông mà không cần thuyền? | Nghề giáo, người lái đò thầm lặng | | Teaching: teachers are called "ferrymen" | A bridge builder? | Thợ xây cầu hả? | V
19/11-20/11 || Cái gì thầy cô cho đi mỗi ngày mà không bao giờ vơi? | Kiến thức | What do teachers give away every day but never run out of? | Knowledge | Is it... homework? | Là… bài tập về nhà hả?
19/11-20/11 || Ngày nào học trò mang hoa tới trường tặng thầy cô? | Ngày 20 tháng 11 | On which day do students in Vietnam bring flowers to their teachers? | November 20th, Vietnamese Teachers' Day | My teacher's birthday? | Sinh nhật cô giáo hả?
24/12-25/12 || Ông già nào không bao giờ già thêm, năm nào cũng mặc đồ đỏ? | Ông già Noel | Which old man never gets older and wears red every year? | Santa Claus | My grandpa in his new pajamas? | Ông tôi mặc đồ ngủ mới hả?
24/12-25/12 || Cây gì không ra quả mà đêm Giáng sinh lại đầy quà bên dưới? | Cây thông Noel | Which tree bears no fruit but has gifts under it on Christmas Eve? | A Christmas tree | A money tree? | Cây tiền hả?
24/12-25/12 || Con gì có sừng, kéo xe trượt tuyết bay trên trời đêm Giáng sinh? | Con tuần lộc | Which animal has antlers and pulls a flying sleigh on Christmas night? | A reindeer | A buffalo with wings? | Con trâu có cánh hả?
24/12-25/12 || Người gì mùa đông mới có, nắng lên là tan? | Người tuyết | Who only appears in winter and melts when the sun comes out? | A snowman | Is it... my motivation? | Là… động lực của tôi hả?
31/12-01/01 || Cái gì mỗi năm chỉ đến một lần lúc nửa đêm, cả thế giới cùng đếm ngược chờ nó? | Năm mới | What arrives once a year at midnight while the whole world counts down? | The New Year | A very late bus? | Chuyến xe buýt siêu trễ hả?
31/12-01/01 || Đêm nào bạn đi ngủ năm nay mà thức dậy vào năm sau? | Đêm giao thừa | On which night do you go to bed this year and wake up next year? | New Year's Eve | A very long nap? | Một giấc ngủ siêu dài hả?
01/02-12/02 || Cái gì màu đỏ, đầu năm trẻ con đứa nào cũng mong được nhận? | Bao lì xì | What is red and makes every child happy at Lunar New Year? | A lucky red envelope | Is it... a tomato? | Là… quả cà chua hả?
01/02-12/02 || Hoa gì miền Bắc nở hồng, hoa gì miền Nam nở vàng mỗi khi Tết đến? | Hoa đào và hoa mai | Which flower blooms pink in the North, and which blooms yellow in the South, at Tết? | Peach blossom and apricot blossom | Plastic flowers? | Hoa nhựa hả?
01/02-12/02 || Thịt mỡ, dưa hành, câu đối đỏ; cây nêu, tràng pháo, bánh chưng xanh. Đó là dịp gì? | Tết Nguyên Đán | | Tết, the Lunar New Year (a famous couplet) | A cooking show? | Chương trình nấu ăn hả? | V
01/02-12/02 || Tiền gì đầu năm cho đi mà ai cũng vui? | Tiền mừng tuổi | | Lucky money ("tiền mừng tuổi") | Tax money? | Tiền thuế hả? | V
"""
SEASON_E = """
19/11-20/11 || 👩 📚 💐 | VH | Ngày Nhà giáo Việt Nam | Vietnamese Teachers' Day | Celebrated on November 20th | A flower shop in a library? | Tiệm hoa trong thư viện hả?
19/11-20/11 || ⛵ 👨 🌊 | VH | Người lái đò | The ferryman | A loving name for teachers in Vietnam | A fisherman on holiday? | Bác ngư dân đi nghỉ hả?
19/11-20/11 || 🙇 👨 📖 | TN | Tôn sư trọng đạo | Respect your teachers and value learning | A proud Vietnamese tradition | Reading a book upside down? | Đọc sách lộn ngược hả?
24/12-25/12 || 🎅 🎁 🌙 | VH | Đêm Giáng sinh | Christmas Eve | The night Santa delivers the gifts | A night shift delivery man? | Anh giao hàng ca đêm hả?
24/12-25/12 || 🎄 ⭐ 🎁 | VH | Cây thông Noel | A Christmas tree | A star on top and gifts below | A tree winning a prize? | Cái cây trúng thưởng hả?
31/12-01/01 || 🎆 🕛 🥳 | VH | Đêm giao thừa | New Year's Eve | Counting down to midnight | A very noisy alarm clock? | Đồng hồ báo thức ồn ào hả?
01/02-12/02 || 🧧 👶 😄 | VH | Lì xì đầu năm | Lucky money | Red envelopes for children at Tết | A baby winning the lottery? | Em bé trúng số hả?
01/02-12/02 || 🌼 🟡 🏠 | VH | Hoa mai ngày Tết | Yellow apricot blossoms | The flower of Tết in the South | A house painted yellow? | Ngôi nhà sơn vàng hả?
01/02-12/02 || 🍌 🍊 🍇 🥭 🍍 | VH | Mâm ngũ quả | The five-fruit tray | A Tết offering to the ancestors | A fruit salad? | Món salad trái cây hả?
"""
# Câu có sẵn nhưng chỉ hợp một mùa (theo đáp án)
SEASON_BY_ANSWER = {'Bánh chưng': '01/02-12/02', 'Bánh tét': '01/02-12/02', 'Tết Nguyên Đán': '01/02-12/02', 'Tết Trung thu': '08/09-16/09', 'Múa lân': '08/09-16/09'}


def rows(block, n):
    out = []
    for ln in block.strip().split('\n'):
        p = [x.strip() for x in ln.split('|')]
        assert len(p) in (n, n + 1), (len(p), ln)
        out.append(p)
    return out


riddles = []
for p in rows(KEEP, 3):
    r = dict(old[p[0]]); r.update(FIX.get(p[0], {}))
    for k in ('vi_a', 'en_a'): r[k] = r[k].rstrip('.!').strip() if not r[k].endswith('!') or True else r[k]
    r.update(g_en=p[1], g_vi=p[2], vi_only=int(r.get('vi_only', 0)))
    if r['vi_only']: r['en_q'] = ''
    riddles.append(r)
kept = {r['id'] for r in riddles}
missing = [i for i in old if i not in kept and i not in OFF]
assert not missing, missing
for i, p in enumerate(rows(NEW, 6), 1):
    v = int(len(p) == 7 and p[6] == 'V')
    assert v or p[2], p
    riddles.append(dict(id=f'N{i:03d}', vi_q=p[0], vi_a=p[1], en_q=p[2], en_a=p[3], g_en=p[4], g_vi=p[5], vi_only=v))
emoji = [dict(id=f'E{i:03d}', emoji=p[0], kind=p[1], vi=p[2], en=p[3], mean=p[4], g_en=p[5], g_vi=p[6]) for i, p in enumerate(rows(EMOJI, 7), 1)]
for r in riddles: r['season'] = SEASON_BY_ANSWER.get(r['vi_a'], '')
for e in emoji: e['season'] = SEASON_BY_ANSWER.get(e['vi'], '')
for i, ln in enumerate(SEASON_R.strip().split('\n'), 1):
    win, rest = [x.strip() for x in ln.split('||')]; p = [x.strip() for x in rest.split('|')]
    v = int(len(p) == 7 and p[6] == 'V'); assert len(p) in (6, 7) and (v or p[2]), ln
    riddles.append(dict(id=f'S{i:03d}', vi_q=p[0], vi_a=p[1], en_q=p[2], en_a=p[3], g_en=p[4], g_vi=p[5], vi_only=v, season=win))
for i, ln in enumerate(SEASON_E.strip().split('\n'), 1):
    win, rest = [x.strip() for x in ln.split('||')]; p = [x.strip() for x in rest.split('|')]; assert len(p) == 7, ln
    emoji.append(dict(id=f'SE{i:02d}', emoji=p[0], kind=p[1], vi=p[2], en=p[3], mean=p[4], g_en=p[5], g_vi=p[6], season=win))
json.dump({'riddles': riddles, 'riddles_off': OFF, 'emoji': emoji}, open(os.path.join(ROOT, 'data', 'content_v2.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('theo mùa:', sum(1 for r in riddles if r['season']), sum(1 for e in emoji if e['season']))
print('câu đố', len(riddles), '(chỉ tiếng Việt:', sum(r['vi_only'] for r in riddles), ') tắt', len(OFF), '| emoji', len(emoji))
