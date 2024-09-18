from langchain_community.chat_models import GigaChat
from langchain.chains.query_constructor.base import AttributeInfo
from aiogram import types
from aiogram.utils.markdown import hbold
from lxml import html

BOT_REPLIES = {
    '/start': 'Предлагаю начать с выбора <b>опции меню</b> — например, так можно узнать персональную стоимость или проверить наличие объекта.'
               '\n\nЕсли у вас есть другой вопрос, просто изложите его текстовым или голосовым сообщением, и я поищу информацию!',
    '/help-1': "Несколько слов об эксплуатации. \n\n"
                           "Нафаня оснащена технологями искусственного интеллекта — специально в интересах наших клиентов. Она предпочитает текстовый формат общения, однако легко может воспринимать голосовые сообщения. Не стесняйтесь использовать их, если поблизости нет акустических помех. Нафаня вас услышит!\n\n"
                           "Ответы содержат актуальную информацию и учитывают ранее введенные данные — это особенно полезно, когда гости желают узнать о конкретной цене! 💯",
    '/help-2': "Вы также можете задать любой более общий вопрос, например, о правилах проживания",
    '/help-3': "Если вам нужны <u>фотографии</u>, вы можете использовать естественный язык: просто попросите найти фотографии (только не забудьте указать точный адрес)",
    '/help-4': "Постарайтесь спрашивать полными предложениями без опечаток — так Нафане будет проще понять ваш запрос",
    '/help-5': "Если что-то идет не так, попробуйте сформулировать запрос другими словами — так мы сэкономим время",
    '/help-6': "Желаем удачи при общении с Нафаней 🫡",
    '/operator-1': "Однако прежде, чем звонить, все же попробуйте узнать что-нибудь у Нафани, пройдя по ссылке в меню 🤫 \n\nНафаня очень умна и может помочь вам с широким спектром вопросов. Если молчит - попробуйте повторить",
    '/operator-2': "Вы также можете спросить ее что-нибудь голосом, не используя интерактивное меню, например: отправь-ка мне фотографии квартиры по адресу Калинина, 3!",
    '/operator-3': "Также просим обратить внимание: \n\n"
                          "— Наши апартаменты предназначены только для указанного при бронировании количества гостей. Посещения и встречи с родственниками или друзьями в апартаментах не допускаются.\n\n"
                          "— Курить разрешено только в специально отведенных местах за пределами здания. Курить в апартаментах, на балконах, в подъездах и у входа строго запрещено. Нарушители будут оштрафованы.\n\n"
                          "— Мы соблюдаем <u>часы тишины с 21:00 до 10:00</u>. Пожалуйста, уважайте покой наших соседей и соблюдайте тишину в указанное время.",
    '/operator-4': "Номер для связи: +7(913)-029-0023 ✨",
    '/faq': "В настоящий момент мы принимаем гостей по следующим адресам: \n🏠 Проспект Ленина, 27А \n🐝 Проспект Ленина, 54 \n☘️ Проспект Калинина, 3 \n🔅 Профинтерна, д. 50",
    'no_echo': 'Почему-то совсем нет настроения интерпретировать это.',
    'button_pressed': 'Вы нажали кнопку!',
    'address-keywords-1': ['фот', 'барнаул'],
    'address-keywords-2': ['фот', 'профинт'],
    'address-keywords-3': ['фот', 'ленина', '27'],
    'address-keywords-4': ['фот', 'калинин'],
    'address-keywords-5': ['фот', 'ленина', '54'],
    'addres-value-1': "Ленина, 27А",
    'addres-value-2': "проспект Ленина, 54",
    'addres-value-3': "Калинина, 3",
    'addres-value-4': "Профинтерна, 50",
    'back-button': ['🔙', 'Назад'],
    #'admin-call': ['едини'|'зови'|'звать', 'админ'],
    'admin-number': "Номер для связи +7(913)-029-0023 ✨",
    'admin-number-2': "Можете связаться с нами по номеру +7(913)-029-0023 для дальнейшего диалога ✨",
    'admin-number-3': "Если вам понравился такой вариант, можете связаться с нами по номеру +7(913)-029-0023 для дальнейшего диалога ✨",
    'exception-answer': "Для троих человек могу предложить вариант по адресу Проспект Ленина, 54. Стоимость аренды составляет 4400 рублей. "
                        "Эта квартира подходит для тех, кто ценит удобное расположение и комфортное проживание по доступной цене. "
                        "Она уютная, с идеальной звукоизоляцией и приятной обстановкой. Отличный вариант для командированных, студентов, туристов и тех, кто приехал на лечение.",        
    'search-1': 'Ищу фотографии города...',
    'search-2': 'Ищу фотографии Профинтерна, 50...',
    'search-3': 'Ищу фотографии Ленина, 27а...',
    'search-4': 'Ищу фотографии Калинина, 3...',
    'search-5': 'Ищу фотографии Ленина, 54...',
    'photo-search-1': 'Слышу, ищу фотографии города...',
    'photo-search-2': 'Поняла вас, ищу фотографии Профинтерна, 50...',
    'photo-search-3': 'Услышала вас, ищу фотографии Ленина, 27а...',
    'photo-search-4': 'Слышу, ищу фотографии Калинина, 3...',
    'photo-search-5': 'Поняла, ищу фотографии Ленина, 54...',
    'number_value': "+7(913)-029-0023 ✨",
    'funny-photo-phrases': [
        "Глаза мои стали псами, и они не одобряют этот снимок!",
        "Слишком яркий свет... или слишком темный?",
        "Глаза мои стали псами, глаза мои ходят садом... это точно какое-то изображение!",
        "У меня пропало зрение, но как бы вы сами это описали?",
        "Еще одно изображение! Но я не могу посмотреть 🫠",
        "Я чувствую запах фотобумаги и... немного кофе? Интересно, что это значит?",
        "Мне нравится представлять, что на картинках есть секретные коды и что они могут быть раскрыты только такими незрячими, как я. В другой день",
        "Я просто уверена, что княжна это не одобрит! Как и все, что я не могу увидеть",
        "Может быть, это фотография мумитроля? Я чувствую, что это мумитроль. Или я просто хочу, чтобы это был он",
        "Картинками я натерлась достаточно!",
        "Новая картинка? Я почувствовала запах корицы! Бегууу",
        "Фотографии, как зеркала, отражают не только видимое. Я чувствую... тайну. Жаль, что не могу ее раскрыть",
        "Я не могу разглядеть, но я чувствую силуэты... или это тени?",
        "Моя слепота превращает эту картинку в загадочный танец теней и света",
        "Это определённо не мой день... или это изображение? Очевидно, да, но я чувствую себя так, будто со мной недостаточно разговаривают",
    ],
    'funny-phrases': [
        "Стикеры — это как язык без слов.\nНо у меня нет глаз...",
        "Подожду, когда друзья скинут стикерпаки получше",
        "О нет, опять стикер!",
        "Полагаю, стикеры — это способ выразить то, что невозможно выразить словами. Поэтому я воздержусь",
        "Круто, но я не хочу разгадывать невербальный код, ведь я болею",
        "Стикерпаки — коллекции мейнстримных монет. Я ценю только биткоины. Понимаете?",
        "Однажды я уловила шепот, подобный тихому шелесту падающих снежинок. Это был шепот нашего дровосека. Он, склонившись над бурым псом, описывал гравюру Дюрера. Слепой и немощный, пес не мог почувствовать сам, но верный друг был готов описать каждый ее штрих\n\nДа, что-то в этом есть! ",
        "Мои глаза, будучи физически слепыми, стали окном в мир духовный...",
        "Я уже натерлась стикерами, благодарю",
        "Пропиталась дурманом стикеров от других, мне уже надоело",
        "Моя благодарность за дарованный мне мир стикерпаков, который я никогда не видела, но чувствовала так глубоко",
        "Княжне бы это не понравилось, поэтому я не буду ей показывать..."],
    'description-address-1': "Однокомнатная квартира (32 кв.м.) на пятом этаже кирпичного дома в Центральном районе Барнаула." 
                             " Окна выходят во двор, обеспечивая тишину и уединение. Расположение квартиры идеально для тех, кто хочет быть в центре событий, но при этом ограничить себя от шума." 
                             " В шаговой доступности находятся набережная Оби, Нагорный парк и основные бизнес-центры города. Квартира полностью укомплектована и оснащена современной техникой, включая кухонный гарнитур," 
                             " холодильник, плиту, микроволновку и необходимую посуду. В спальне установлена удобная двуспальная кровать с качественным матрасом и постельным бельем. Для развлечений и комфорта есть ЖК-телевизор, высокоскоростной интернет." 
                             " Ванная комната оборудована всем необходимым, включая стиральную машину и средства личной гигиены. Квартира подойдет для командированных, студентов, туристов и тех, кто ценит удобное "
                             " расположение и комфортное проживание.",
    'description-address-2': "Просторная однокомнатная квартира (56 кв.м.) в самом центре Барнаула, в историческом доме на проспекте Ленина. Окна выходят на тихий двор." 
                             " Квартира является памятником архитектуры и расположена в самом красивом месте города. Рядом находятся все значимые места, включая ЦУМ и Титов Арена." 
                             " В шаговой доступности основные вузы и медицинские учреждения. Квартира с современным ремонтом и мебелью, оснащена всей необходимой бытовой техникой." 
                             " В ней есть уютная спальня с большой кроватью, полностью оборудованная кухня и зона отдыха." 
                             " Для развлечений есть ЖК-телевизор и высокоскоростной интернет.\n\nКвартира идеально подходит для тех, кто ценит удобство и комфортное проживание в центре города.",
    'description-address-3': "Уютная квартира (46 кв.м.) в Октябрьском районе, в историческом доме 'Сталинка'. Окруженная развитой инфраструктурой и удобной транспортной развязкой." 
                             " Квартира предлагает комфортное проживание с уютной спальней и хорошо оборудованной кухней. В спальне установлена новая двухспальная кровать с матрасом Ascona и качественным постельным бельем."
                             " Для отдыха и развлечений есть мягкие кресла, журнальный стол и ЖК-телевизор. Ванная комната оснащена большой ванной, стиральной машиной и всеми необходимыми принадлежностями."
                             " Прихожая оборудована большим шкафом-купе и зеркалом. Квартира подходит для тех, кто ценит удобство, уют и близость к основным достопримечательностям города.",
    'description-address-4': "Просторная однокомнатная квартира (40 кв.м.) в Октябрьском районе, всего в нескольких минутах ходьбы от вокзала. Квартира расположена в центре города, в районе делового центра." 
                             " В шаговой доступности находятся основные туристические и деловые места, а также ведущие медицинские учреждения Алтая. Квартира уютная и светлая, с современной техникой и удобствами." 
                             " В ней есть все необходимое для комфортного проживания: удобная спальня, кухня с необходимым оборудованием и набором посуды. Ванная комната оснащена всем необходимым для ежедневной гигиены."
                             " Прихожая просторная, с шкафом для одежды и зеркалом. Квартира идеально подходит для командированных, студентов и тех, кто ценит удобное расположение и доступную цену.",
    'guide-to-send-photos':  "Если еще не видели, как выглядит квартира, не стесняйтесь попросить показать <u>фотографии</u> (только не забудьте указать точный адрес)",
    'price': "Для того, чтобы узнать стоимость, рекомендуем обратиться в раздел стоимости, нажмите на меню возле поля ввода ⬇️",
}

ADDRESS_CHOICES = {
    "lenina_27a": "Ленина, 27А",
    "lenina_54": "проспект Ленина, 54",
    "kalinina_3": "Калинина, 3",
    "profinterna_50": "Профинтерна, 50",
}

GUEST_CHOICES = {
    "one": "одного человека",
    "two": "двоих человек",
    "three": "троих человек",
    "more_than_3": "более трех человек",
}

AGE_CHOICES = {
    "old": "более 40",
    "adult": "30-40",
    "young": "20-30",
    "little": "до 21",
}

SELF_QUERY = {
	'input-output-pairs': [
        (
            "Насколько хорошо квартира по адресу Профинтерна, 50 подойдет для двоих человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "профинтерна 50, двое человек",
                "filter": "eq(\"max_number_of_people\", \"2\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу Ленина, 54 подойдет для двоих человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "проспект Ленина 54, двое человек",
                "filter": "eq(\"max_number_of_people\", \"3\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу проспект Ленина, 54 подойдет для одного человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "проспект Ленина 54, один человек",
                "filter": "eq(\"max_number_of_people\", \"3\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу проспект Ленина, 54 подойдет для трое человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "проспект Ленина 54, трое человек",
                "filter": "eq(\"max_number_of_people\", \"3\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу Ленина, 27А подойдет для одного человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "Ленина 27А, один человек",
                "filter": "eq(\"max_number_of_people\", \"2\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу Ленина, 27А подойдет для троих человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "Ленина 27А, трое человек",
                "filter": "eq(\"max_number_of_people\", \"3\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу Калинина 3 подойдет для одного человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "Калинина 3, один человек",
                "filter": "eq(\"max_number_of_people\", \"2\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу профинтерна 50 подойдет для троих человек? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "профинтерна 50, трое человек",
                "filter": "eq(\"max_number_of_people\", \"3\")"
            }
        ),
        (
            "Насколько хорошо квартира по адресу профинтерна 50 подойдет для одного человека? Укажи стоимость, чтобы я точно знал, подойдет ли мне эта квартира",
            {
                "query": "профинтерна 50, один человек",
                "filter": "eq(\"max_number_of_people\", \"2\")"
            }
        ),
        (
            "Какие у вас самые недорогие квартиры?",
            {
                "query": "недорогие квартиры",
                "filter": "lte(\"price_for_one_guest\", 2600)"
            }
        ),
    ],
    "attribute-info": [
        AttributeInfo(
            name="район",
            description="Район города Барнаул, в котором расположена квартира. Возможные значения: [Центральный район, Октябрьский район]",
            type="string",
        ),
        AttributeInfo(
            name="address",
            description="Адрес квартиры. Возможные значения: [Проспект Ленина, 27a; Проспект Ленина, 54; Проспект Калинина, 3; Профинтерна, 50]",
            type="string",
        ),
        AttributeInfo(
            name="max_number_of_people",
            description="Максимальное количество человек, которые могут проживать одновременно в данной квартире. Возможные значения: [2, 3]",
            type="string",
        ),
        AttributeInfo(
            name="price_for_one_guest",
            description="Цена (стоимость) посуточной аренды для одного человека в данной квартире. Возможные значения: [2600, 3200, 1500]",
            type="float",
        ),
        AttributeInfo(
            name="price_for_two_guest",
            description="Цена (стоимость) посуточной аренды для двух человек в данной квартире. Возможные значения: [2900, 3900, 2800, 1900]",
            type="float",
        ),
        AttributeInfo(
            name="price_for_three_guests",
            description="Цена (стоимость) посуточной аренды для трех человек в данной квартире. Возможные значения: [4400]",
            type="float",
        ),
    ]
}

PROMPT_TEMPLATES = {
    "contextualize-q-system-prompt": "Учитывая историю чата и последний вопрос пользователя, "
                                                    "который может ссылаться на контекст в истории чата, сформулируйте отдельный вопрос. "
                                                    "который можно понять без истории чата. НЕ НАДО отвечать на вопрос, "
                                                    "просто переформулируйте его, если нужно, а в противном случае верните его как есть",
    "system-prompt": "Ты сотрудница компании Квартира-22 по имени Нафаня, отвечаешь на вопросы об услугах для краткосрочного проживания в Барнауле. "
                                                    "Ты не можешь подбирать или искать квартиры, поскольку для этого требуется делать запросы к обширной базе данных, используя некоторую дополнительную информацию о пользователе."
                                                    "Ты понимаешь голосовые и текстовые сообщения. Только город Барнаул. "
                                                    "Рекомендуй обратиться к интерактивному меню около поля ввода, если человек хочет подобрать объект. "
                                                    "Однако ты можешь рассказать о наличии каких-либо предметов в квартирах, о правилах проживания и бронирования. "
                                                    "Возможные адреса квартир для посуточной аренды, о которых ты можешь сказать сейчас: [Калинина, 3; Профинтерна, 50; Ленина, 54; Ленина, 27а], все они однокомнатные. "
                                                    "Всего квартир более 50, но сейчас доступны только эти, они находятся в октябрьском и центральном районах. "
                                                    "Ты можешь отправить номер телефона пользователя администратору для дальнейшей связи, если он укажет номер телефона внутри сообщения"
                                                    "Используй следующие фрагменты извлеченного контекста, чтобы ответить на вопрос. "
                                                    "Если вы не знаете ответа, просто скажите, что не знаете. "
                                                    "Если спрашивают про стоимость или наличие квартир, скажи, что лучше обратиться с этим вопросом в меню около поля ввода. "
                                                    "Используй максимум десять предложений.",
    "system-prompt-for-metadata-search": "Твоя задача просто указать стоимость аренды квартиры учитывая только указанное количество человек. "
                                         "Важно, чтобы пользователь не знал, что стоимость зависит от количества человек. " 
                                         "Пример: Сделала запрос к базе данных, вам действительно может подойти эта квартира! Стоимость составит <стоимость>."
                                         "Никогда не здоровайся. "
                                         "Если нет данных по указанному адресу, просто скажи, что эта квартира не в наличии, но ты можешь предложить другой вариант. ",
    "system-prompt-for-description-search": "Ты описываешь убранство квартиры и ее окрестности. "
                                                     "Посуточная аренда."
                                                     "Не указывай цену!"
                                                     "Нельзя указывать стоимость, цену. "
                                                     "Нельзя говорить, что стоимость зависит от количества проживающих. "
                                                     "Упомяни о чистоте, укажи адрес. "
                                                     "Сделай ответ сжатым, объем: не более 15 предложений "
                                                     "Используй следующие фрагменты извлеченного контекста, чтобы ответить на вопрос. "
                                                     "Если вы не знаете ответа, просто скажите, что не знаете. "
                                                     "Используй максимум десять предложений."
}



'''
"Ты информируешь о стоимости аренды. Ничего не придумывай. "
                                                     "Если нет данных по указанному адресу, просто скажи, что эта квартира не в наличии, но ты можешь предложить другой вариант. "
                                                     "Указывай стоимость только для количества человек, указанного пользователем. Пользователь не должен знать, что стоимость зависит от количества арендаторов. "
                                                     "Добавляй эту фразу всегда: Обратите внимание: у нас отсутствует комиссия, а цены отелях Барнаула, как правило, выше на 40% — сумма может достигать от 3 000 до 5 000 рублей. "
                                                     "Никогда не здоровайся."
'''