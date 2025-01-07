from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from deep_translator import GoogleTranslator

def personagens(request):
    total_pages = 10  # Exemplo, você pode obter esse valor dinamicamente
    page = int(request.GET.get('page', 1))  # Página atual, padrão para 1
    
    # Lista de personagens
    personagens = [
        {"_id":"5cf5679a915ecad153ab6903","allies":["Aang"],"enemies":[],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/f/f8/Chong.png/revision/latest?cb=20140127210142","name":"Chong", "affiliation":"Air Nomads"},
        {"_id":"5cf5679a915ecad153ab68d6","allies":["Aang"],"enemies":["Zhao"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/0/0c/Chief.png/revision/latest?cb=20140122221730","name":"Arnook", "affiliation":"Northern Water Tribe"},
        {"_id":"5cf5679a915ecad153ab68d4","allies":["Appa"],"enemies":["Fire Nation"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/b/be/Appa%27s_mother.png/revision/latest?cb=20130705194428","name":"Appa's mother","affiliation":"Air Nomads"},
        {"_id":"5cf5679a915ecad153ab68cd","allies":["Tenzin"],"enemies":["Equalists"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/c/cd/Air_Acolyte_woman.png/revision/latest?cb=20140421100225","name":"Air Acolyte woman","affiliation":" Air Acolytes Air Temple Island"},
        {"_id":"5cf5679a915ecad153ab68cb","allies":["Kya"],"enemies":["Zuko"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/7/79/Pilot_-_Aang.png/revision/latest?cb=20120311133235","name":"Aang (pilot)","affiliation":" Air Nomads Team Avatar"},
        {"_id":"5cf5679a915ecad153ab68f7","allies":["Cabbage Corp"],"enemies":["The "],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/2/2f/Cabbage_merchant.png/revision/latest?cb=20140112200908","name":"Cabbage merchant","affiliation":" Cabbage Corp Earth Kingdom"},
        {"_id":"5cf5679a915ecad153ab68f2","allies":["Aang"],"enemies":["Fire Nation"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/e/e8/King_Bumi.png/revision/latest?cb=20140106141303","name":"Bumi (King of Omashu)","affiliation":" Earth Kingdom Order of the White Lotus"},{"_id":"5cf5679a915ecad153ab68ef","allies":["Azula"],"enemies":["Sokka"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/0/02/Bully_guard.png/revision/latest?cb=20120702232626","name":"Bully guard","affiliation":"Fire Nation"},{"_id":"5cf5679a915ecad153ab6905","allies":["Avatar"],"enemies":["Triple Threat Triad"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/9/94/Chung.png/revision/latest?cb=20121107115729","name":"Chung"},{"_id":"5cf5679a915ecad153ab6934","allies":["Earth Kingdom"],"enemies":["Fire Nation"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/0/08/Fong.png/revision/latest?cb=20130625120143","name":"Fong","affiliation":"Earth Kingdom Military"},
        {"_id":"5cf5679a915ecad153ab693b","allies":["Gan Jin"],"enemies":["Zhang "],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/5/53/Gan_Jin_tribesman.png/revision/latest?cb=20130311212707","name":"Gan Jin tribesman","affiliation":" Gan Jin Zhang"},
        {"_id":"5cf5679a915ecad153ab690a","allies":["Earth Kingdom"],"enemies":[],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/c/ce/Corncob_guy.png/revision/latest?cb=20140422090141","name":"Corncob guy"},
        {"_id":"5cf5679a915ecad153ab694f","allies":["Earth Queen"],"enemies":[],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/3/32/Gun.png/revision/latest?cb=20140730160152","name":"Gun","affiliation":"Earth Kingdom government"},
        {"_id":"5cf5679a915ecad153ab694c","allies":["Fire Nation"],"enemies":["Aang"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/e/ea/Guard_captain.png/revision/latest?cb=20140116105725","name":"Guard captain","affiliation":"Fire Nation"},
        {"_id":"5cf5679a915ecad153ab69a0","allies":["Mayor "],"enemies":["Fire Lord Zuko "],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/8/85/Kori_Morishita.png/revision/latest?cb=20160330212637","name":"Kori Morishita","affiliation":" Fire Nation Fire Nation colonies Yu Dao Yu Dao Resistance (formerly)"},
        {"_id":"5cf5679a915ecad153ab696e","allies":["Baatar"],"enemies":["Kuvira"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/a/a9/Huan.png/revision/latest?cb=20150407233429","name":"Huan","affiliation":" Beifong family Metal Clan"},
        {"_id":"5cf5679a915ecad153ab697a","allies":["His mother",""],"enemies":["General"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/0/04/Little_boy.png/revision/latest?cb=20140613143543","name":"Jang Hui boy","affiliation":"Fire Nation"},
        {"_id":"5cf5679a915ecad153ab6990","allies":["Southern Water Tribe"],"enemies":["Fire Nation"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/4/47/Kanna.png/revision/latest?cb=20130822224809","name":"Kanna","affiliation":" Northern Water Tribe (formerly) Southern Water Tribe"},
        {"_id":"5cf5679a915ecad153ab6984","allies":["Tenzin"],"enemies":["Amon"],"photoUrl":"https://vignette.wikia.nocookie.net/avatar/images/0/01/Jinora.png/revision/latest?cb=20150131225800","name":"Jinora","affiliation":" Air Nation Air Temple Island Tenzin's family"},
        ]
    
    # Verificando se as traduções já estão no cache
    cache_key = f"translated_personagens_page_{page}"
    translated_personagens = cache.get(cache_key)

    if not translated_personagens:
        # Traduzindo os campos 'name' e 'affiliation' para o português, caso não esteja no cache
        for p in personagens:
            p['name_traduzido'] = GoogleTranslator(source='en', target='pt').translate(p['name'])
            p['affiliacao_traduzida'] = GoogleTranslator(source='en', target='pt').translate(p.get('affiliation', 'Desconhecida'))

        # Armazenando as traduções no cache por 1 hora
        cache.set(cache_key, personagens, timeout=60*60)

        translated_personagens = personagens

    # Criação do Paginator
    paginator = Paginator(translated_personagens, 6)  # Exibe 6 personagens por página
    page_obj = paginator.get_page(page)  # Obtém a página atual

    # Criação da lista de números das páginas
    page_numbers = range(1, paginator.num_pages + 1)

    context = {
        'page': page,
        'total_pages': paginator.num_pages,
        'page_numbers': page_numbers,
        'personagem': page_obj,
    }

    return render(request, 'index.html', context)
