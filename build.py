"""Build the Magimil static design prototype. Python standard library only."""
from pathlib import Path
from html import escape
import json
import argparse
import re
import shutil

ROOT = Path(__file__).resolve().parent
BASE = 'https://magimil.bg'
PRODUCTION = True
# Update only when public content changes, not on every build.
LASTMOD = '2026-10-30'
# Add only verified profiles belonging to МАГИМИЛ, not the hosting account.
FACEBOOK_URL = 'https://www.facebook.com/share/1FMRY89kW6/?mibextid=wwXIfr'
SOCIAL_PROFILES = [FACEBOOK_URL]
PHONE = '0894 336 030'
MAP_URL = 'https://maps.app.goo.gl/57j9Qv3isPY8PgmM8'
BASE_LATITUDE = 42.407070
BASE_LONGITUDE = 25.654342
CITIES = ['Стара Загора', 'Хасково', 'Харманли', 'Пловдив', 'Казанлък', 'Нова Загора', 'Свиленград']
SERVICE_CONTENT = json.loads((ROOT/'seo/service-content.json').read_text(encoding='utf-8'))

ICONS = {
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="m8 3 3 5-3 3c1.2 2.7 2.9 4.4 5.5 5.5l3-3 4.5 3c0 3-1.6 5-4 4C9 18 5 14 3 6 2.5 3.5 5 2 8 3Z"/></svg>',
 'chat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-8 8H8l-5 2 1.5-5A8 8 0 1 1 20 11.5Z"/><path d="M8 9h8M8 13h5" stroke-linecap="round"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 18 18 6M6 6h12v12"/></svg>',
 'menu': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>'
}

def profile(kind):
    shapes = {
      'flash': '<path d="m40 91 54 20V60l53 20v-24l34 13 33-17-34-12-33 16-53-20-54 30Z" fill="currentColor" opacity=".07"/><path d="m40 91 54 20V60l53 20v-24l34 13"/><path d="m40 66 54-30 53 20 33-16 34 12-33 17M94 36v24"/><path class="fold-line" d="m94 111 53-31 34-11"/>',
      'gutter': '<path d="M45 65v18c0 28 48 40 64 12l5-18 80-37v19c0 28-48 43-61 16" fill="currentColor" opacity=".07"/><path d="M45 65v18c0 28 48 40 64 12l5-18 80-37v19c0 28-48 43-61 16M45 65l80-37M114 77l80-37M42 65h7M111 77h7M122 28h7M191 40h7"/><path class="fold-line" d="M45 83c0 28 48 40 64 12"/>',
      'seam': '<path d="m35 100 21 7V71l13 4 21-12 66 25V51l13 4 24-14 15 6"/><path d="m56 71 91-48 13 4v36l9 3M69 75l91-48M90 63l66 25M156 51l39-20 13 5v11M35 100l22-12M156 88l37-20V41"/><path class="fold-line" d="m69 75 21-12 66 25"/>',
      'slat': '<path d="m42 77 19 15 63 16 78-43-18-15-64-16Z" fill="currentColor" opacity=".08"/><path d="m42 77 19 15 63 16 78-43-18-15-64-16ZM42 77l78-43M61 92l78-43 45 1M124 108l78-43"/><path class="fold-line" d="m61 92 63 16"/>',
      'hunter': '<path d="m35 100 17 7 17-12V74l15 6 16-10 14 6 16-10 14 6 16-10 15 6V47l16-10 17 7"/><path d="m52 107 77-44V42l15 6 16-10 14 6 16-10 17 6M69 74l75-43M84 80l76-42M100 70l74-41M175 47l16-10"/><path class="fold-line" d="m69 95 15 6 16-10 14 6 16-10 14 6 16-10 15 6V68"/>',
      'pipe': '<ellipse cx="88" cy="43" rx="24" ry="11"/><path d="M64 43v55c0 6 11 11 24 11s24-5 24-11V43M138 52l18 8v32l30 14 16-9-30-14V52l-18-8Z"/><path d="m156 60 16-8M156 92l16-9"/><path class="fold-line" d="M64 98c0 6 11 11 24 11s24-5 24-11"/>'
    }
    return f'<div class="profile-figure"><svg viewBox="0 0 250 145" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true">{shapes.get(kind,shapes["flash"])}</svg></div>'

SERVICES = [
 {'slug':'zagotovki-ot-lamarina','name':'Заготовки от ламарина','kind':'flash','category':'roof industrial','tag':'По размер и чертеж','short':'Обшивки, челни дъски и нестандартни детайли за покриви и халета.',
  'title':'Заготовки от ламарина по размер и чертеж | МАГИМИЛ',
  'description':'Заготовки от ламарина по размер, обшивки за челни дъски и детайли за халета. МАГИМИЛ — Стара Загора, Хасково, Пловдив и региона. Запитвания по Viber.',
  'lead':'Изработваме заготовки от ламарина за майстори, строителни фирми и собственици. Изпратете скица или чертеж с размерите по Viber, за да обсъдим детайла за вашия обект.',
  'sections': [('Детайлът започва с вашия размер','При покривните обшивки и довършителните елементи формата е свързана с конкретния обект. В МАГИМИЛ изработваме детайли по подадени размери и чертеж. Преди производството уточняваме сечението, дължините, количеството и избрания материал.'),('Какви заготовки изработваме',['Покривни обшивки и челни дъски от ламарина.','Огънати детайли за халета и метални конструкции.','Заготовки по нестандартно сечение и скица.','Детайли за водоотвеждане — улуци, водосточни тръби, кривки и казанчета.']),('Какво да изпратите за запитване','Приложете чертеж или четлива скица, размерите на всяка страна, дължина и брой детайли. Ако знаете материала, дебелината и цвета, посочете ги. За уточняване на подходящата изработка изпратете и снимка на мястото за монтаж. Възможността за конкретен материал и размер се потвърждава при запитването.')]
 },
 {'slug':'ogavane-na-lamarina-abkant','name':'Огъване на ламарина на абкант','kind':'flash','category':'industrial','tag':'Абкант 8 метра','short':'Огъване на дълги детайли с електронен абкант на осем метра.',
  'title':'Огъване на ламарина на абкант 8 метра по размер | МАГИМИЛ',
  'description':'Огъване на ламарина с електронен абкант 8 метра. Заготовки по чертеж от МАГИМИЛ за Стара Загора, Хасково, Пловдив и региона. Запитвания по Viber.',
  'lead':'Разполагаме с електронен абкант на осем метра за огъване на ламаринени детайли. Уточняваме всяко сечение по вашата скица и изискванията на обекта.',
  'sections':[('Осемметров абкант за вашите детайли','Оборудването ни включва абкант с работна дължина осем метра и цепачка за ламарина. Използваме ги при подготовката и огъването на заготовки за покриви, фасадни и довършителни елементи и детайли за халета.'),('За какви поръчки е подходящо',['Обшивки и челни дъски за покриви.','Ламаринени детайли за халета.','Огъване по чертеж и нестандартно сечение.','Ламели за огради и метален хънтър.']),('Материалът и сечението се уточняват предварително','Дължината на машината сама по себе си не определя всички възможни детайли. За да потвърдим изработката, изпратете дължина, сечение, количество и, ако са избрани, материал и дебелина. Конкретните допустими размери и срокът се уточняват за всяка поръчка.')]
 },
 {'slug':'bezshevni-uluci','name':'Безшевни улуци','kind':'gutter','category':'roof','tag':'Изтегляне на място','short':'Улуци 5 и 6 инча, изтеглени на място според вашия обект.',
  'title':'Безшевни улуци 5 и 6 инча на място и монтаж | МАГИМИЛ',
  'description':'Американски безшевни улуци 5 и 6 инча — изтегляне на място и монтаж от МАГИМИЛ. Стара Загора, Хасково, Пловдив и региона. Запитвания по Viber.',
  'lead':'Изтегляме безшевни улуци на място с машина за улуци на 5 и 6 инча. Предлагаме също монтаж и детайли за водоотвеждането на вашия покрив.',
  'sections':[('Улуци според дължината на обекта','При изтегляне на място улукът се подготвя според уточнените дължини за конкретния покрив. Преди работа обсъждаме размерите, достъпа до обекта и необходимите допълнителни елементи.'),('Изработка и монтаж',['Изтегляне на улуци на място — 5 и 6 инча.','Монтаж на улуци.','Водосточни тръби и кривки.','Казанчета за улуци и свързващи детайли.']),('Подгответе информация за покрива','Изпратете снимки на стрехите и фасадата, приблизителните дължини и населеното място. Ако вече има водосточни тръби, посочете къде са разположени. Конкретният размер на системата и организацията на монтажа се уточняват за обекта.')]
 },
 {'slug':'shlebah','name':'Шлебах','kind':'seam','category':'roof','tag':'Изработка и монтаж','short':'Подготовка на шлебах с машина и монтаж на покривни елементи.',
  'title':'Шлебах — изработка и монтаж за метални покриви | МАГИМИЛ',
  'description':'Шлебах — изработка и монтаж на метални покривни елементи със стоящ фалц от МАГИМИЛ. Стара Загора, Хасково, Пловдив и региона. Запитвания по Viber.',
  'lead':'Разполагаме с машина за шлебах и предлагаме изработка и монтаж. Подготвяме поръчката според размерите и детайлите на конкретния покрив.',
  'sections':[('Подготовка за конкретния покрив','За изработката на шлебах са важни геометрията на покрива, дължините и връзките с останалите елементи. Изпратете план, скица или снимки, за да уточним какво е необходимо за вашия обект.'),('Свързани услуги',['Изработка на шлебах с машина.','Монтаж на шлебах.','Покривни обшивки по размер.','Челни дъски, улуци и водосточни елементи.']),('Преди производството','Уточняваме размерите, материала, количеството и начина на изпълнение. Наличните цветове, допустимите размери и срокът се потвърждават при запитване; не публикуваме технически стойности без потвърждение.')]
 },
 {'slug':'metalen-hantar','name':'Метален хънтър','kind':'hunter','category':'roof','tag':'Огъване и монтаж','short':'Огъване на метален хънтър и челни детайли за завършен покрив.',
  'title':'Метален хънтър — огъване по размер и монтаж | МАГИМИЛ',
  'description':'Метален хънтър — огъване и монтаж от МАГИМИЛ. Челни дъски и ламаринени обшивки за Стара Загора, Хасково, Пловдив и региона. Запитвания по Viber.',
  'lead':'Огъваме метален хънтър и предлагаме монтаж. Изработваме и свързаните ламаринени обшивки и челни детайли според нуждите на покрива.',
  'sections':[('Изработка по размер','При довършителните елементи размерите и връзките с покрива се уточняват предварително. Подготвяме металния хънтър по конкретно запитване, като обсъждаме сечението, дължините и количеството.'),('Какво можем да обсъдим заедно',['Огъване на метален хънтър.','Монтаж на метален хънтър.','Огъване на челна дъска.','Обшивки и детайли около улука.']),('Какво е необходимо за запитване','Изпратете снимки на мястото, размери или чертеж и приблизително количество. Уточнете дали търсите само заготовки, или изработка с монтаж, и в кое населено място е обектът.')]
 },
 {'slug':'lameli-za-ograda','name':'Ламели за ограда','kind':'slat','category':'industrial','tag':'Огъване от ламарина','short':'Ламаринени ламели за ограда, огънати по зададеното сечение.',
  'title':'Ламели за ограда от ламарина по ваш размер | МАГИМИЛ',
  'description':'Ламели за ограда от ламарина по размер и сечение от МАГИМИЛ. За обекти в Стара Загора, Хасково, Пловдив и региона. Изпратете скица и поискайте оферта.',
  'lead':'Огъваме ламели за ограда от ламарина по зададено сечение. Услугата е за майстори, строителни фирми и собственици, които подготвят своята ограда.',
  'sections':[('Ламелите следват вашия проект','При запитването уточняваме сечението на ламела, дължината на отделните елементи и общото количество. Ако имате мостра или скица, изпратете я по Viber заедно с основните размери.'),('Каква информация да подготвите',['Чертеж или скица на сечението.','Дължина и брой ламели.','Материал, дебелина и цвят, ако вече са избрани.','Населено място и желания срок.']),('Изработка на заготовки','Тази услуга е за огъване на ламели. Доставката, възможността за конкретен материал и организацията на получаване се уточняват отделно. За работата по самата ограда обсъдете с вашия изпълнител необходимите размери и бройки.')]
 },
 {'slug':'vodostochni-trabi-i-detayli','name':'Водосточни тръби и детайли','kind':'pipe','category':'roof','tag':'За водоотвеждането','short':'Водосточни тръби, кривки и казанчета за улуци.',
  'title':'Водосточни тръби, кривки и казанчета за улуци | МАГИМИЛ',
  'description':'Водосточни тръби, кривки и казанчета за улуци от МАГИМИЛ. Стара Загора, Хасково, Пловдив и региона. Изпратете размери и снимки по Viber за оферта.',
  'lead':'Предлагаме водосточни тръби, кривки и казанчета за улуци, както и ламаринени детайли за водоотвеждането. Уточняваме необходимите елементи според вашия обект.',
  'sections':[('Елементите на водоотвеждането','Улукът, тръбите, кривките и казанчетата трябва да се съобразят с конкретния покрив и фасада. За запитване изпратете снимки, размери и броя на необходимите детайли.'),('Какво предлагаме',['Водосточни тръби.','Кривки за водосточни тръби.','Казанчета за улуци.','Изтегляне на улуци на място и монтаж.']),('Съобразяване с наличната система','Ако допълвате съществуващо водоотвеждане, посочете размерите на наличните улуци и тръби и приложете снимки на връзките. Размерите, материалът и цветът се потвърждават преди поръчка.')]
 },
 {'slug':'montazh','name':'Монтаж на покривни елементи','kind':'seam','category':'roof','tag':'За вашия обект','short':'Монтаж на улуци, обшивки, метален хънтър и шлебах.',
  'title':'Монтаж на улуци, обшивки, хънтър и шлебах | МАГИМИЛ',
  'description':'Монтаж на улуци, обшивки, метален хънтър и шлебах от МАГИМИЛ в Стара Загора, Хасково, Харманли, Пловдив и региона. Изпратете снимки за запитване.',
  'lead':'Освен заготовки, предлагаме монтаж на улуци, обшивки от ламарина, метален хънтър и шлебах. Работим със собственици и строителни фирми в обслужвания от нас район.',
  'sections':[('Изработка и изпълнение на обекта','Можете да се обърнете към нас както за отделни ламаринени детайли, така и за монтаж на покривни елементи. При разговора уточнете дали искате само заготовки, монтаж, или и двете.'),('Монтажни услуги',['Монтаж на улуци и водосточни елементи.','Монтаж на обшивки от ламарина.','Монтаж на метален хънтър.','Монтаж на шлебах.']),('Къде работим','Обслужваме района на Стара Загора, Хасково, Харманли, Пловдив, Казанлък, Нова Загора и Свиленград, както и близките населени места. За конкретен адрес и организация на работа се свържете с нас по телефона или Viber.'),('Как да започнем','Изпратете снимки на покрива, ориентировъчни размери, населено място и кратко описание на работата. След уточняване на информацията обсъждаме нужните детайли, организацията и следващите стъпки.')]
 }
]

def enquiry(label='Изпратете чертеж по Viber', subject='', cls='button'):
    return f'<button class="{cls}" type="button" data-enquiry="{escape(subject,quote=True)}">{ICONS["chat"]}{label}</button>'

def head(title, description, prefix='', slug=''):
    if not slug:
        description='Заготовки от ламарина по размер, абкант 8 м и безшевни улуци. МАГИМИЛ — изработка и монтаж в Стара Загора, Хасково и Пловдив.'
    description=description.replace('Запитвания по Viber.', 'Изпратете скица по Viber.')
    canonical=BASE+'/'+(slug+'/' if slug else '')
    image_key=SERVICE_PHOTOS[slug][0] if slug else 'project-lakeside-roof'
    image_url=f'{BASE}/assets/photos/{image_key}-1200.webp'
    robots='index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1' if PRODUCTION else 'noindex,follow'
    graph = [
      {'@type':'Organization','@id':BASE+'/#organization','name':'МАГИМИЛ','alternateName':'MAGIMIL','url':BASE+'/','logo':BASE+'/assets/magimil-logo.png','telephone':'+359894336030','areaServed':[{'@type':'City','name':city} for city in CITIES]},
      {'@type':'WebSite','@id':BASE+'/#website','name':'МАГИМИЛ','url':BASE+'/','inLanguage':'bg','publisher':{'@id':BASE+'/#organization'}}
    ]
    if slug:
      item=next(s for s in SERVICES if s['slug']==slug)
      graph += [{'@type':'Service','name':item['name'],'alternateName':SERVICE_CONTENT[slug]['aliases'],'description':description,'url':f'{BASE}/{slug}/','provider':{'@id':BASE+'/#organization'},'areaServed':[{'@type':'City','name':c} for c in CITIES]}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Начало','item':BASE+'/'},{'@type':'ListItem','position':2,'name':item['name'],'item':f'{BASE}/{slug}/'}]}]
    graph.append({'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'inLanguage':'bg','isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#organization'},'primaryImageOfPage':{'@type':'ImageObject','url':image_url}})
    graph[0].update(description='Заготовки от ламарина по размер, огъване на абкант, безшевни улуци и монтаж от МАГИМИЛ.', image=BASE+'/assets/photos/project-lakeside-roof-1200.webp')
    graph[0]['address']={'@type':'PostalAddress','addressLocality':'Стара Загора','streetAddress':'база Терамис','addressCountry':'BG'}
    graph[0]['location']={'@type':'Place','name':'МАГИМИЛ — база Терамис','hasMap':MAP_URL,'geo':{'@type':'GeoCoordinates','latitude':BASE_LATITUDE,'longitude':BASE_LONGITUDE}}
    graph[1].update(description=graph[0]['description'], image=graph[0]['image'])
    if SOCIAL_PROFILES:
        graph[0]['sameAs']=SOCIAL_PROFILES
    schema=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)
    canonical=BASE+'/'+(slug+'/' if slug else '')
    markup=f'''<!doctype html>
<html lang="bg" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="{robots}"><meta name="theme-color" content="#202124"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:locale" content="bg_BG"><meta property="og:site_name" content="МАГИМИЛ"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image_url}"><meta property="og:image:alt" content="{escape(PHOTOS[image_key][1],quote=True)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title,quote=True)}"><meta name="twitter:description" content="{escape(description,quote=True)}"><meta name="twitter:image" content="{image_url}"><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="preload" href="{prefix}assets/Oswald.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="{prefix}assets/site.css?v=14"><script type="application/ld+json">{schema}</script><script defer src="{prefix}assets/site.js?v=13"></script></head><body>'''

    markup=markup.replace('</head>', f'<link rel="stylesheet" href="{prefix}assets/vendor/leaflet.min.css"><link rel="stylesheet" href="{prefix}assets/location.css?v=5"><script defer src="{prefix}assets/location.js?v=7"></script></head>')
    icons=''.join(f'<link rel="icon" type="image/png" sizes="{size}x{size}" href="{prefix}assets/favicon-{size}.png">' for size in (16,32))
    icons+=f'<link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/apple-touch-icon.png">'
    markup=markup.replace('</head>',icons+'</head>').replace('charset="utf-8"','charset="UTF-8"').replace('initial-scale=1"','initial-scale=1.0"')
    return markup.replace('><','>\n<')

def header(prefix=''):
    home=prefix+'index.html'
    return f'''<a class="skip-link" href="#main">Към съдържанието</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{home}" aria-label="МАГИМИЛ — начална страница"><span class="brand-logo"><img src="{prefix}assets/magimil-logo.webp?v=17" alt="МАГИМИЛ — покривни системи" width="1449" height="712" decoding="async"></span><span class="brand-caption">Заготовки от ламарина<br>и покривни системи</span></a><nav id="main-nav" class="main-nav" aria-label="Основна навигация"><a href="{home}#zagotovki">Заготовки</a><a href="{home}#proizvodstvo">Производство</a><a href="{prefix}montazh/index.html">Монтаж</a><a href="{home}#kontakti">Контакти</a></nav><a class="header-phone" href="tel:+359894336030">{ICONS['phone']}{PHONE}</a><a class="header-location" href="#lokatsia" aria-label="Към секцията с местоположението" title="Местоположение — база Терамис">{ICONS['pin']}<span>Местоположение</span></a><button class="menu-button" aria-label="Отворете менюто" aria-expanded="false" aria-controls="main-nav">{ICONS['menu']}</button></div></header>'''

def location(prefix=''):
    return f'''<section class="base-location" id="lokatsia" aria-labelledby="base-title"><div class="wrap base-location-grid"><div class="base-location-copy"><h2 id="base-title">Как да ни намерите</h2><address>гр. Стара Загора<br><strong>база Терамис</strong></address><p>Вижте точното ни местоположение на картата.</p><a class="text-link" href="{MAP_URL}" target="_blank" rel="noopener">Отвори навигация <span aria-hidden="true">↗</span></a></div><div class="base-map-card"><div id="base-map" class="base-map" role="region" aria-label="Карта на МАГИМИЛ — база Терамис, Стара Загора" data-lat="{BASE_LATITUDE}" data-lng="{BASE_LONGITUDE}" data-library="{prefix}assets/vendor/leaflet.min.js"><p class="base-map-status" role="status">Картата се зарежда. Можете да използвате линка за навигация.</p></div><div class="base-map-caption"><a href="{MAP_URL}" target="_blank" rel="noopener" aria-label="Вижте локацията в Google Maps (нов раздел)">Google Maps <span aria-hidden="true">↗</span></a></div></div></div></section>'''

def contact(prefix=''):
    return location(prefix)+f'''<section class="contact" id="kontakti" aria-labelledby="contact-title"><div class="wrap contact-grid"><div><h2 id="contact-title">Имате чертеж?<br>Да го направим.</h2><p>Изпратете скица, размери и количество по Viber. Ще уточним детайлите за вашата заготовка или монтаж.</p></div><div class="contact-actions"><a class="contact-number" href="tel:+359894336030">{PHONE}</a>{enquiry('Подгответе запитване във Viber')}<div class="contact-secondary"><span>Скица или снимка са добро начало.</span><button class="text-link" data-copy-phone type="button" style="background:none;color:inherit;border-top:0;border-left:0;border-right:0;cursor:pointer">Копирайте номера</button></div></div></div></section>'''

def footer(prefix=''):
    return f'''<footer class="site-footer"><div class="wrap"><div class="footer-top"><a href="{prefix}index.html" class="footer-title" aria-label="МАГИМИЛ — начална страница"><span class="brand-logo footer-logo"><img src="{prefix}assets/magimil-logo.webp?v=17" alt="МАГИМИЛ — покривни системи" width="1449" height="712" loading="lazy" decoding="async"></span></a><div class="footer-links"><a href="{prefix}zagotovki-ot-lamarina/index.html">Заготовки по размер</a><a href="{prefix}bezshevni-uluci/index.html">Улуци по дължина</a><a href="{prefix}montazh/index.html">Монтаж на покривни елементи</a><a href="{prefix}index.html#rayon">Район на работа</a><a href="{escape(FACEBOOK_URL,quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="МАГИМИЛ във Facebook (отваря се в нов раздел)">Facebook ↗</a></div></div><div class="footer-bottom"><p>МАГИМИЛ — заготовки от ламарина и покривни системи.</p><a href="{MAP_URL}" target="_blank" rel="noopener">гр. Стара Загора, база Терамис ↗</a></div></div></footer>
<nav class="mobile-contact" aria-label="Бърза връзка"><a class="button button-outline" href="tel:+359894336030">{ICONS['phone']}Обадете се</a>{enquiry('Чертеж по Viber')}</nav>
<dialog id="viber-dialog" aria-labelledby="dialog-title"><div class="dialog-header"><h2 id="dialog-title">Да уточним детайла.</h2><button class="close-dialog" data-close-dialog aria-label="Затворете запитването">×</button></div><p class="dialog-note">Допълнете текста, копирайте го и го поставете във Viber. Приложете чертежа или снимката директно в разговора. Този сайт не изпраща съобщения и файлове.</p><label for="enquiry-message" class="field-label">Вашето запитване</label><textarea id="enquiry-message">Здравейте, МАГИМИЛ!
Интересувам се от заготовки от ламарина.

Размери / скица: ...
Количество: ...
Материал / цвят, ако са избрани: ...
Населено място на обекта: ...
Желан срок: ...

Ще приложа снимка или чертеж във Viber.</textarea><div class="dialog-actions"><button class="button" data-copy-message>Копирайте запитването</button><a class="button button-outline" href="viber://chat?number=%2B359894336030">Отворете Viber</a></div><p id="dialog-status" class="dialog-status" role="status" aria-live="polite"></p><p class="dialog-note" style="margin:16px 0 0">Ако Viber не се отвори, добавете номера в приложението. Изисква се инсталиран Viber; връзката предстои да се провери с фирмения профил.</p><div class="dialog-phone"><strong>+359 894 336 030</strong><button data-copy-phone>Копирайте номера</button></div></dialog>{photo_dialog()}<div id="toast" class="toast" role="status" aria-live="polite"></div><noscript><div class="noscript-note">Можете да разгледате всички услуги и да се обадите на <a href="tel:+359894336030">0894 336 030</a>. За изпращане на чертеж добавете +359 894 336 030 във Viber.</div></noscript></body></html>'''

PHOTOS = {
 'flashings': ('Обшивки по размер', 'Огънати ламаринени обшивки с различни сечения върху работна маса'),
 'gutters': ('Американски безшевен улук', 'Американски безшевен улук с характерен оформен преден ръб и отворено сечение'),
 'standing-seam': ('Шлебах', 'Детайл на метален покрив с успоредни стоящи фалцове'),
 'metal-soffit': ('Метален хънтър', 'Метален хънтър с широки равни панели и диагонално ъглово съединение по предоставената мостра'),
 'fence-slats': ('Ламели за ограда', 'Мостра на огънати ламели за ограда с наклонена широка лицева част и подгънати ръбове'),
 'downpipes': ('Водосточни тръби и кривки', 'Кръгли ламаринени водосточни тръби, кривки и монтажна скоба'),
 'rain-hopper': ('Американски улук', 'Американски улук в антрацит, монтиран по стрехата на къща'),
 'fascia-flashing': ('Челна дъска от ламарина', 'Ламаринена челна дъска по предоставена мостра, с широка равна повърхност и плитка надлъжна сгъвка'),
 'hall-flashings': ('Детайли за халета', 'Ламаринени обшивки на хале с американски безшевен улук по дясната стреха'),
 'sheet-bending': ('Електронен абкант 8 метра', 'Модерен електронен абкант с дисплей и осемметрова работна дължина'),
 'sheet-slitting': ('Цепачка за ламарина', 'Машина за надлъжен разкрой на ламарина с валове, направляващи и режещи дискове'),
 'finished-roof': ('Покривни елементи в завършен вид', 'Примерен метален покрив с фалцове, улук, челна обшивка и водосточна тръба')
}
PROJECT_PHOTOS = {item['key']: item for item in json.loads((ROOT/'project-photos.json').read_text(encoding='utf-8'))}
PHOTOS.update({key: (item['title'], item['alt']) for key, item in PROJECT_PHOTOS.items()})
SERVICE_PHOTOS = {
 'zagotovki-ot-lamarina': ['flashings', 'fascia-flashing', 'hall-flashings', 'rain-hopper'],
 'ogavane-na-lamarina-abkant': ['sheet-bending', 'sheet-slitting', 'fascia-flashing', 'hall-flashings'],
 'bezshevni-uluci': ['gutters', 'rain-hopper', 'downpipes', 'fascia-flashing'],
 'shlebah': ['standing-seam', 'finished-roof', 'flashings'],
 'metalen-hantar': ['metal-soffit', 'fascia-flashing', 'finished-roof'],
 'lameli-za-ograda': ['fence-slats', 'flashings'],
 'vodostochni-trabi-i-detayli': ['downpipes', 'rain-hopper', 'gutters'],
 'montazh': ['project-lakeside-roof', 'project-gabled-house', 'project-modern-house', 'project-metal-facade', 'project-roof-overview', 'project-roof-renovation', 'project-metal-soffit']
}

def photo(key, prefix='', cls='', eager=False):
    alt=('' if key in PROJECT_PHOTOS else 'Илюстративен кадър: ')+PHOTOS[key][1]
    size=PROJECT_PHOTOS.get(key,{'width':1536,'height':1024})
    return f'<img class="{cls}" src="{prefix}assets/photos/{key}-1200.webp?v=17" srcset="{prefix}assets/photos/{key}-600.webp?v=17 600w, {prefix}assets/photos/{key}-1200.webp?v=17 1200w" sizes="(max-width: 600px) calc(100vw - 40px), (max-width: 850px) 85vw, 45vw" width="{size["width"]}" height="{size["height"]}" alt="{escape(alt,quote=True)}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def photo_dialog():
    return '<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-title"><div class="photo-dialog-top"><h2 id="photo-title">Детайл отблизо</h2><button type="button" class="close-dialog" data-close-photo aria-label="Затворете снимката">×</button></div><img id="photo-large" alt="" width="1536" height="1024"><p class="photo-dialog-caption">Конкретното сечение се уточнява по чертеж.</p></dialog>'

def photo_figure(key, prefix='', cls='', eager=False):
    real=key in PROJECT_PHOTOS
    label=''
    caption='Реална снимка от обект на МАГИМИЛ.' if real else 'Конкретното сечение се уточнява по чертеж.'
    extra=' real-project-photo' if real else ''
    if key=='project-roof-renovation': extra+=' project-collage'
    full=prefix+PROJECT_PHOTOS[key]['original'] if real else f'{prefix}assets/photos/{key}-1200.webp?v=17'
    width=PROJECT_PHOTOS[key]['width'] if real else 1536
    return f'<figure class="photo-figure {cls}{extra}"><button type="button" class="photo-zoom" data-photo="{full}" data-photo-width="{width}" data-photo-real="{str(real).lower()}" data-photo-title="{PHOTOS[key][0]}" data-photo-caption="{caption}" aria-label="Увеличете: {PHOTOS[key][0]}">{photo(key,prefix,eager=eager)}<span class="photo-zoom-hint">Вижте отблизо</span></button><figcaption><strong>{PHOTOS[key][0]}</strong>{label}</figcaption></figure>'

def close_details():
    keys=['fascia-flashing','hall-flashings','rain-hopper','sheet-slitting']
    return f'<section class="section detail-gallery-section" id="detayli" aria-labelledby="close-details-title"><div class="wrap"><div class="section-heading"><h2 id="close-details-title">Детайлът.<br>Погледнат отблизо.</h2><p>Челни обшивки, ъгли, водоотвеждане и разкрой. Разгледайте примерните форми в по-голям размер.</p></div><div class="close-details-grid">{"".join(photo_figure(key) for key in keys)}</div><p class="photo-disclosure">Изображенията са генерирани и показват примерни изделия и процеси. Конкретните сечения, материали и изпълнение уточняваме по вашия чертеж.</p></div></section>'

def service_gallery(item):
    keys=SERVICE_PHOTOS[item['slug']][1:]
    if item['slug']=='montazh':
        return f'<section class="service-gallery real-projects" id="detail-gallery"><h2>Наши обекти</h2><p>Реални кадри от работата на МАГИМИЛ — покриви, обшивки и монтажни детайли.</p><div class="service-gallery-grid">{"".join(photo_figure(key,"../") for key in keys)}</div></section>'
    return f'<section class="service-gallery" id="detail-gallery"><h2>Разгледайте детайлите</h2><div class="service-gallery-grid">{"".join(photo_figure(key,"../") for key in keys)}</div><p class="photo-disclosure">Примерни форми. Не са снимки на изпълнени поръчки на МАГИМИЛ.</p></section>'

def product(item):
    key=SERVICE_PHOTOS[item['slug']][0]
    badge=''
    return f'''<article class="product product-with-photo" data-category="{item['category']}"><div class="product-photo">{photo(key)}{badge}</div><div class="product-info"><div class="product-top"><span>{item['tag']}</span></div><h3><a class="product-link" href="{item['slug']}/index.html">{item['name']}</a></h3><p>{item['short']}</p><div class="product-bottom"><span>Разгледайте услугата</span>{ICONS['arrow']}</div></div></article>'''

ROOF = '''<svg viewBox="0 0 600 360" fill="none" stroke="#38545a" stroke-width="1.4" stroke-linejoin="round" aria-hidden="true"><path d="m65 200 220-125 235 135-220 125Z" fill="#cbd7d9"/><path d="m65 200 220-125 235 135-220 125Z"/><path d="m65 200 115-140 105 15M180 60l235 135 105 15M300 335l115-140M65 200v13l235 135 220-125v-13M300 335v13"/><path d="m86 212 115-140m-88 155 115-140m-88 155 115-140m-88 155 115-140m-88 155 115-140m-88 155 115-140m-88 155 115-140m-88 155 115-140" stroke="#7d9398"/><path d="m180 60 235 135" stroke="#a32e30" stroke-width="4"/><path d="M65 213v58l235 135 220-125v-58" stroke="#8a9ea2"/><path d="M300 348v58" stroke="#8a9ea2"/><path d="m65 213 235 135 220-125" stroke="#a32e30" stroke-width="3"/><path d="M520 223v80l-15 9" stroke="#a32e30" stroke-width="3"/></svg>'''
MAP = '''<svg class="region-map" viewBox="0 0 560 340" role="img" aria-label="Схематичен район на работа: Пловдив, Казанлък, Стара Загора, Нова Загора, Хасково, Харманли и Свиленград. Не обозначава адреси на офиси."><path class="map-outline" d="m35 96 43-12 42-35 52 8 52-16 46 23 33-12 35 21 69-9 37 39 61 14 18 38-29 34-17 52-44 18-30 32-62 1-28-18-60 14-37-27-35 6-35-44-32-8-16-39Z"/><path class="map-road" d="m115 200 138-48 83-17M253 152l28 71 85 20 79 39M197 96l56 56"/><circle cx="115" cy="200" r="6"/><circle cx="197" cy="96" r="6"/><circle cx="253" cy="152" r="7"/><circle cx="336" cy="135" r="6"/><circle cx="281" cy="223" r="6"/><circle cx="366" cy="243" r="6"/><circle cx="445" cy="282" r="6"/><text x="67" y="228">Пловдив</text><text x="159" y="80">Казанлък</text><text x="196" y="179">Стара Загора</text><text x="326" y="116">Нова Загора</text><text x="228" y="250">Хасково</text><text x="343" y="269">Харманли</text><text x="422" y="307">Свиленград</text><text x="43" y="318" class="map-muted">Схематична карта на обслужвания район</text></svg>'''

def home():
    html=head('Заготовки от ламарина по размер | МАГИМИЛ','МАГИМИЛ — заготовки от ламарина по размер, огъване на абкант 8 м, безшевни улуци и монтаж. Работа в района на Стара Загора, Хасково и Пловдив.')+header()
    html+=f'''<main id="main"><section class="hero" aria-labelledby="hero-title"><div class="wrap"><div class="hero-grid"><div class="hero-copy"><p class="hero-intro">За майстори, строителни фирми и собственици</p><h1 id="hero-title"><span>Заготовки </span><span>от ламарина. </span><span>По ваш размер.</span></h1><p class="hero-description">Изработваме заготовки от ламарина по ваш размер и чертеж за покриви, халета и огради. Подготвяме всеки детайл според сечението и размерите, които са необходими за вашия обект.</p><div class="actions">{enquiry()}<a class="text-link" href="#zagotovki">Разгледайте заготовките</a></div></div><figure class="hero-art"><img src="assets/folded-metal-v3.webp?v=17" alt="Илюстративен кадър на челна дъска с плитка сгъвка и американски улук" width="1536" height="1024" fetchpriority="high"><figcaption class="art-note">Илюстративни детайли: челна дъска и американски улук.</figcaption></figure></div><div class="hero-bottom"><p><strong>Изработка на заготовки и монтаж.</strong> Стара Загора, Хасково, Пловдив и региона.</p><div class="capacity"><b>8 м</b><span>работна дължина<br>на абканта</span></div><div class="capacity"><b>5″ / 6″</b><span>безшевни улуци<br>на място</span></div></div></div></section><div class="service-ticker" aria-label="Основни дейности"><span>Заготовки по чертеж</span><span>Огъване на ламарина</span><span>Безшевни улуци</span><span>Изработка и монтаж</span></div>
<section class="section catalogue" id="zagotovki" aria-labelledby="catalogue-title"><div class="wrap"><div class="section-heading"><h2 id="catalogue-title">Всеки детайл<br>си има място.</h2><p>Подготвяме ламаринени детайли според нуждите на вашия обект, от покривните обшивки до ламелите за ограда.</p></div><div class="filter-bar" role="group" aria-label="Филтрирайте категориите заготовки"><button class="filter" data-filter="all" aria-pressed="true">Всички заготовки</button><button class="filter" data-filter="roof" aria-pressed="false">За покрива</button><button class="filter" data-filter="industrial" aria-pressed="false">За халета и огради</button></div><div class="catalogue-grid">{''.join(product(s) for s in SERVICES if s['slug'] not in ['ogavane-na-lamarina-abkant','montazh'])}</div><span id="catalogue-status" role="status" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)"></span><div class="catalogue-foot"><p>Имате нестандартно сечение? Показаните кадри са илюстративни. Изпратете скица, за да обсъдим вашия детайл.</p><a class="text-link" href="zagotovki-ot-lamarina/index.html">Повече за изработката по размер</a></div></div></section>{close_details()}
<section class="section workshop" id="proizvodstvo" aria-labelledby="workshop-title"><div class="wrap workshop-grid"><div class="workshop-copy"><span class="section-kicker">Производството зад детайла</span><h2 id="workshop-title">Голямата машина.<br>Малкият детайл.</h2><p>Собственото ни оборудване позволява да подготвяме ламаринени елементи за различни задачи — от челна дъска до детайли за хале.</p><div class="equipment-list"><div class="equipment-row"><span>Електронен абкант</span><strong>8 метра</strong></div><div class="equipment-row"><span>Машина за безшевни улуци</span><strong>5 и 6 инча</strong></div><div class="equipment-row"><span>Машина за шлебах</span><strong>Изработка на профили</strong></div><div class="equipment-row"><span>Цепачка за ламарина</span><strong>Подготовка на материала</strong></div></div><a class="text-link" href="ogavane-na-lamarina-abkant/index.html">Огъване на ламарина на абкант</a></div><div class="workshop-visual">{photo_figure('sheet-bending',cls='workshop-photo')}</div></div></section>
<section class="section installation" id="montazh" aria-labelledby="installation-title"><div class="wrap installation-grid">{photo_figure('project-lakeside-roof',cls='installation-photo')}<div class="installation-copy"><span class="section-kicker">От работилницата до покрива</span><h2 id="installation-title">Изработваме.<br>И монтираме.</h2><p>За собственици и строителни фирми предлагаме както изработка на заготовки, така и монтаж на улуци, обшивки от ламарина, метален хънтър и шлебах.</p><a class="text-link" href="montazh/index.html">Вижте монтажните услуги</a></div></div><div class="wrap home-projects"><div class="projects-heading"><div><span class="section-kicker">Реални снимки от нашата работа</span><h3>Наши обекти.</h3></div><a class="text-link" href="montazh/index.html#detail-gallery">Всички снимки от обекти</a></div><div class="home-project-grid">{''.join(photo_figure(key) for key in ['project-roof-overview','project-modern-house','project-metal-soffit'])}</div></div></section>
<section class="section process" id="porachka" aria-labelledby="process-title"><div class="wrap process-grid"><div class="process-intro"><h2 id="process-title">От вашата скица.<br>Към вашия обект.</h2><p>Не е необходимо да започвате със сложен проект. Четлива скица с размери или снимка са добра основа за разговор.</p>{enquiry('Подгответе запитване')}</div><ol class="steps"><li><div><h3>Изпратете ни детайла</h3><p>Изпратете снимка, скица или чертеж по Viber, като добавите размерите, необходимото количество и населеното място на обекта.</p></div></li><li><div><h3>Уточняваме изработката</h3><p>Обсъждаме сечението, материала, цвета и срока. Ако ви трябва монтаж, посочете го още в запитването.</p></div></li><li><div><h3>Подготвяме поръчката</h3><p>След потвърждение уточняваме производството и организацията за получаване или работа на обекта.</p></div></li></ol></div></section>
<section class="section regions" id="rayon" aria-labelledby="regions-title"><div class="wrap regions-grid"><div><span class="section-kicker">Близо до вашата работа</span><h2 id="regions-title">В региона.<br>На вашия обект.</h2><p>Работим в района на Стара Загора, Хасково, Харманли, Пловдив, Казанлък, Нова Загора и Свиленград, както и в близките населени места.</p><p>Посочете къде се намира обектът, за да уточним възможностите за изработка на заготовки и монтаж на конкретния адрес.</p><ul class="city-list">{''.join('<li>'+c+'</li>' for c in CITIES)}</ul></div>{MAP}</div></section>
<section class="section faq" aria-labelledby="faq-title"><div class="wrap faq-grid"><div class="faq-intro"><h2 id="faq-title">Преди<br>да започнем.</h2><p>Няколко отговора за изработката и поръчките.</p></div><div class="faq-list"><details><summary>Мога ли да поръчам заготовка по моя скица?</summary><p>Можете да поръчате заготовки от ламарина по ваша скица, като изпратите размерите и необходимото количество по Viber. Уточняваме материала, сечението и възможността за изработка преди потвърждение.</p></details><details><summary>Работите ли с майстори и строителни фирми?</summary><p>Изработваме заготовки за майстори, строителни фирми и собственици, като уточняваме всеки детайл според изискванията на конкретния обект.</p></details><details><summary>Изтегляте ли улуци на място?</summary><p>Разполагаме с машина за безшевни улуци на 5 и 6 инча, които изтегляме на място според дължините на покрива. Организацията за изтегляне и монтаж на конкретния обект се уточнява предварително.</p></details><details><summary>Как се определят цената и срокът?</summary><p>Определяме цената и срока за конкретната поръчка след уточняване на размерите, количеството, материала и необходимата работа. Изпратете тази информация по Viber или се обадете, за да обсъдим детайлите и да потвърдим условията за изработка.</p></details><details><summary>Предлагате ли само заготовки, без монтаж?</summary><p>Можете да поръчате само заготовки по размер, които да монтирате сами или да предоставите на вашия майстор. Предлагаме и монтаж на улуци, обшивки, метален хънтър и шлебах, ако това е необходимо за обекта.</p></details></div></div></section>{contact()}</main>'''
    return html+footer()

def detail(item):
    p='../'
    service_content=SERVICE_CONTENT[item['slug']]
    html=head(item['title'],item['description'],p,item['slug'])+header(p)
    html+=f'''<main id="main"><div class="wrap breadcrumb"><a href="../index.html">Начало</a><span>/</span><a href="../index.html#zagotovki">Услуги</a><span>/</span>{item['name']}</div><section class="detail-hero"><div class="wrap detail-grid"><div><span class="section-kicker">{item['tag']}</span><h1>{item['name']}</h1><p class="detail-lead">{item['lead']}</p><div class="actions">{enquiry('Запитване по Viber',item['name'])}<a class="text-link" href="tel:+359894336030">{PHONE}</a></div></div>{photo_figure(SERVICE_PHOTOS[item['slug']][0],p,cls='detail-feature',eager=True)}</div></section><section class="detail-content"><div class="wrap detail-content-grid"><article class="article">'''
    for heading,content in item['sections']:
        html+=f'<h2>{heading}</h2>'
        html+=('<ul>'+''.join(f'<li>{text}</li>' for text in content)+'</ul>') if isinstance(content,list) else f'<p>{content}</p>'
    html+=f'<h2>{escape(service_content["heading"])}</h2><p>{escape(service_content["text"])}</p>'
    html+='<section aria-labelledby="service-questions"><h2 id="service-questions">Въпроси за '+escape(item['name'].lower())+'</h2>'
    html+=''.join(f'<h3>{escape(question)}</h3><p>{escape(answer)}</p>' for question,answer in service_content['faq'])
    html+='</section>'
    html+=service_gallery(item)
    html+='<h2>Район на работа</h2><p>Обслужваме Стара Загора, Хасково, Харманли, Пловдив, Казанлък, Нова Загора, Свиленград и близките населени места. Посочете местоположението на вашия обект при запитване.</p><h2>Свързани услуги</h2><div class="related-links">'
    related=[next(s for s in SERVICES if s['slug']==slug) for slug in service_content['related']]
    html+=''.join(f'<a href="../{s["slug"]}/index.html">{s["name"]}</a>' for s in related)
    html+=f'''</div></article><aside class="detail-aside"><h2>Вашият детайл<br>започва оттук.</h2><p>Подгответе размери, количество и скица. Материалът и срокът ще уточним заедно.</p>{enquiry('Подгответе запитване',item['name'])}<a class="aside-phone" href="tel:+359894336030">{PHONE}</a></aside></div></section>{contact(p)}</main>'''
    return html+footer(p)

def clean_links(html):
    # Link to the same directory URLs used by canonical tags and the sitemap.
    html=re.sub(r'(<img\b[^>]*loading="eager")', r'\1 fetchpriority="high"', html)
    return re.sub(r'href="([^"?#]*)index\.html([#?][^"]*)?"', lambda m: 'href="'+(m[1] or './')+(m[2] or '')+'"', html)

def main():
    global PRODUCTION
    parser=argparse.ArgumentParser(description='Build the MAGIMIL website locally or prepare a publication folder.')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--production',action='store_true',help='Build indexable public pages (default).')
    mode.add_argument('--preview',action='store_true',help='Build a separate noindex preview.')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    PRODUCTION=not args.preview
    if args.preview and not args.output:
        parser.error('--preview requires a separate --output folder')
    output=args.output.resolve() if args.output else ROOT
    if args.preview and output==ROOT:
        parser.error('Use a separate preview output folder')
    output.mkdir(parents=True,exist_ok=True)
    (output/'index.html').write_text(clean_links(home()),encoding='utf-8')
    for item in SERVICES:
        directory=output/item['slug'];directory.mkdir(exist_ok=True)
        (directory/'index.html').write_text(clean_links(detail(item)),encoding='utf-8')
    urls=[BASE+'/']+[BASE+'/'+item['slug']+'/' for item in SERVICES]
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{url}</loc><lastmod>{LASTMOD}</lastmod><priority>{"1.0" if url==BASE+"/" else "0.8"}</priority></url>\n' for url in urls)+'</urlset>\n'
    (output/'sitemap.xml').write_text(sitemap,encoding='utf-8')
    robots='User-agent: *\nAllow: /\n'+('Sitemap: '+BASE+'/sitemap.xml\n' if PRODUCTION else '# Local preview: HTML pages use noindex,follow.\n')
    (output/'robots.txt').write_text(robots,encoding='utf-8')
    if output!=ROOT:
        shutil.copytree(ROOT/'assets',output/'assets',dirs_exist_ok=True)
    print(f'Built homepage and {len(SERVICES)} service pages ({"production" if PRODUCTION else "local preview"}).')

if __name__=='__main__':main()
