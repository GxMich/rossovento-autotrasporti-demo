"""Genera il sito dimostrativo di Rossovento Autotrasporti (azienda di fantasia).
Solo libreria standard di Python."""
from pathlib import Path
from html import escape
from urllib.parse import urlencode
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://gxmich.github.io/rossovento-autotrasporti-demo'
BASE_PATH = '/rossovento-autotrasporti-demo/'
PHONE = '+39 000 000 0000'
TEL = 'tel:+390000000000'
EMAIL = 'info@rossovento-autotrasporti.example'
CAREER_EMAIL = 'lavoro@rossovento-autotrasporti.example'
ADDRESS_HTML = 'Via dei Trasporti&nbsp;22, San&nbsp;Ferlino (Piemonte)'
COMPANY_IDS = 'Azienda di fantasia&nbsp;· dati inventati'
DEMO_NOTE = 'Attività di fantasia: nomi, recapiti, prezzi e recensioni sono inventati. Sito dimostrativo realizzato da <a href="https://www.modicamichele.it">Michele Modica</a>.'
ASSET_URLS = {ext: f'assets/site.{ext}?v=' + hashlib.sha256((ROOT / 'assets' / f'site.{ext}').read_bytes()).hexdigest()[:10] for ext in ('css', 'js')}
OG_VERSION = hashlib.sha256((ROOT / 'assets' / 'og.jpg').read_bytes()).hexdigest()[:8]

SERVICES = [
    dict(slug='nazionali', name='Trasporti nazionali', short='Nazionali', icon='truck', image='camion-nuvole',
         alt='Autoarticolato in bianco e nero su una strada ai piedi delle montagne',
         intro_image='autostrada-aerea', intro_alt='Autostrada vista dall’alto con un autoarticolato in viaggio',
         line='Da nord a sud, con un solo referente.',
         summary='Ritiri e consegne in tutta Italia, seguiti da una persona sola.',
         lead='Carichi e consegne in tutta Italia, organizzati sugli orari di chi spedisce e di chi riceve.',
         intro='Che sia una consegna sola o un collegamento fisso, prima di partire mettiamo per iscritto tratta, merce e orari di carico e scarico. Durante il viaggio l’ufficio traffico segue il mezzo e il tuo referente risponde al telefono e per email.',
         points=[('Viaggio pianificato', 'Tratta, merce e finestre di carico decise prima della partenza.'), ('Mezzo seguito', 'L’ufficio traffico controlla la posizione del camion durante il viaggio.'), ('Una persona di riferimento', 'Lo stesso contatto dalla richiesta alla consegna.'), ('Sosta in magazzino', 'Se la merce deve fermarsi, la teniamo noi e la facciamo ripartire.')],
         faqs=[('Fate anche trasporti fissi ogni settimana?', 'Sì. Scrivi nella richiesta ogni quanto parti: la proposta tiene conto della tratta e della cadenza.'), ('Posso abbinare viaggio e deposito?', 'Sì. Se la merce deve aspettare prima o dopo il viaggio, la teniamo nel nostro magazzino e la facciamo ripartire.'), ('Come so dov’è la mia merce?', 'L’ufficio traffico segue i mezzi durante il viaggio. Per aggiornamenti chiami o scrivi al tuo referente.')]),
    dict(slug='internazionali', name='Trasporti internazionali', short='Internazionali', icon='globe', image='galleria',
         alt='Mezzi pesanti in viaggio in una galleria autostradale',
         line='Oltre il confine, con le carte in ordine.',
         summary='Trasporti su strada da e verso l’estero, con documenti preparati prima.',
         lead='Trasporti su strada da e verso l’Europa, con tratta, documenti e consegna decisi prima di partire.',
         intro='Quando si passa un confine i dettagli contano di più: documenti, orari di scarico, condizioni di consegna. L’ufficio traffico li sistema con te prima del viaggio e segue il mezzo fino a destinazione.',
         points=[('Tratta chiara', 'Paesi, località, tempi e condizioni chiariti prima di partire.'), ('Documenti pronti', 'Le carte che servono alla merce concordate in anticipo con l’ufficio traffico.'), ('Mezzo seguito', 'Controlliamo la posizione del camion lungo tutto il percorso.'), ('Una persona di riferimento', 'Un contatto che risponde anche quando il camion è lontano.')],
         faqs=[('Andate anche nel mio paese di destinazione?', 'Scrivi nel modulo partenza e destinazione: ti diciamo se la tratta è fattibile e con quali tempi.'), ('Quali documenti servono?', 'Dipende da merce e destinazione. Segnala cosa spedisci: li definiamo insieme prima del viaggio.'), ('Gestite anche i rientri?', 'Sì. Se hai merce da riportare in Italia la inseriamo nella stessa pianificazione.')]),
    dict(slug='container', name='Trasporti container', short='Container', icon='container', image='container-nave',
         alt='Nave portacontainer in mare sotto un cielo rosa al tramonto',
         line='Dal porto fino al tuo cancello.',
         summary='Container tra porti, interporti e aziende, dal terminal alla consegna.',
         lead='Ritiriamo il container al porto o all’interporto e lo portiamo dove serve, coordinando ogni passaggio.',
         intro='Un container passa per molte mani: terminal, dogana, autista, magazzino. Mettiamo in fila i passaggi, prenotiamo il ritiro e ti avvisiamo quando il mezzo è in strada.',
         points=[('Passaggi in fila', 'Ritiro, viaggio e consegna organizzati con un’unica richiesta.'), ('Prenotazione al terminal', 'Ci occupiamo degli slot di ritiro e riconsegna del vuoto.'), ('Mezzo seguito', 'Sai sempre a che punto è il container.'), ('Una persona di riferimento', 'Un contatto per date, riferimenti e cambi di programma.')],
         faqs=[('Posso indicare il terminal nel modulo?', 'Sì. Il modulo container ha i campi per porto o terminal, destinazione, tipo di container e operazione.'), ('Non ho ancora tutti i riferimenti. Posso chiedere?', 'Sì. Scrivi quello che hai e cosa manca: partiamo lo stesso e completiamo dopo.'), ('Il container può sostare da voi?', 'Sì. Descrivi l’esigenza nella stessa richiesta: organizziamo sosta e consegna insieme.')]),
    dict(slug='logistica', name='Logistica e magazzino', short='Logistica', icon='warehouse', image='logistica-aerea',
         alt='Vista dall’alto di un piazzale con camion e auto parcheggiati',
         line='Il posto giusto tra un viaggio e l’altro.',
         summary='Magazzino, movimentazione e trasporti gestiti dalla stessa squadra.',
         lead='Spazio a magazzino, movimentazione e trasporti coordinati dalla stessa squadra, senza passaggi di consegne.',
         intro='La merce non viaggia sempre: a volte aspetta. In magazzino la riceviamo, la registriamo e la teniamo pronta per il viaggio successivo. Chi organizza i trasporti vede anche le scorte, così non si perde tempo.',
         points=[('Spazio quando serve', 'Deposito prima, dopo o tra due viaggi, anche per periodi brevi.'), ('Una squadra sola', 'Magazzino e trasporti organizzati dalle stesse persone.'), ('Scorte sotto controllo', 'Entrate e uscite registrate, con un riepilogo quando lo chiedi.')],
         faqs=[('Posso chiedere solo il magazzino?', 'Sì. Descrivi merce, quantità e periodo: ti rispondiamo su spazio e condizioni.'), ('Per quanto tempo potete tenere la merce?', 'Da pochi giorni a mesi. Indica il periodo nella richiesta e ti diciamo cosa possiamo fare.'), ('Magazzino e camion lavorano insieme?', 'Sì. La stessa squadra organizza le uscite dal magazzino e i viaggi.')]),
]
NAV = [('servizi.html', 'Servizi'), ('azienda.html', 'Azienda'), ('lavora-con-noi.html', 'Lavora con noi'), ('contatti.html', 'Contatti')]
IMAGE_SIZES = {'camion-strada': (2000, 1333), 'camion-nuvole': (2000, 1333), 'logistica-aerea': (2000, 1332), 'tramonto': (2000, 1320), 'porto-notte': (2000, 1064), 'container-nave': (2000, 1125), 'autostrada-aerea': (2000, 796), 'galleria': (2000, 1336)}
IMAGE_POSITION = {'camion-nuvole': '35% 60%'}
INTRO_SIZES = '(max-width: 1000px) 145vw, 1100px'


def icon(name, cls=''):
    source = (ROOT / 'assets' / 'icons' / f'{name}.svg').read_text(encoding='utf-8')
    source = source[source.index('<svg'):]
    source = re.sub(r'\sclass="[^"]*"', '', source, count=1)
    source = re.sub(r'\s+', ' ', source).strip()
    classes = f'icon icon-{name} {cls}'.strip()
    return re.sub(r'<svg\b', f'<svg aria-hidden="true" focusable="false" class="{classes}"', source, count=1)


def picture(name, alt='', cls='', eager=False, sizes='(max-width: 760px) 100vw, 55vw'):
    w, h = IMAGE_SIZES.get(name, (1600, 900))
    srcset = f' srcset="img/{name}-900.webp 900w, img/{name}.webp {w}w" sizes="{sizes}"' if (ROOT / 'img' / f'{name}-900.webp').exists() else ''
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    cls_attr = f' class="{cls}"' if cls else ''
    position = f' style="object-position: {IMAGE_POSITION[name]}"' if name in IMAGE_POSITION else ''
    return f'<img{cls_attr} src="img/{name}.webp"{srcset} width="{w}" height="{h}" alt="{escape(alt)}" {loading} decoding="async"{position}>'


def button(text, href, kind='primary', symbol=None):
    external = href.startswith('http')
    symbol = symbol or ('arrow-up-right' if external else 'arrow-right')
    target = ' target="_blank" rel="noopener"' if external else ''
    return f'<a class="btn btn-{kind}" href="{escape(href, quote=True)}"{target}><span>{text}</span>{icon(symbol)}</a>'


def kicker(text):
    return f'<p class="kicker">{text}</p>'


def header(active):
    def links():
        return ''.join(f'<a href="{url}"{" aria-current=\"page\"" if active == url or active.startswith("servizio-") and url == "servizi.html" else ""}>{text}</a>' for url, text in NAV)
    return f'''<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="header" data-header><div class="header-inner wrap">
  <a class="logo" href="index.html" aria-label="Rossovento Autotrasporti, home"><img src="img/logo.svg" width="250" height="81" alt="Rossovento Autotrasporti"></a>
  <nav class="desktop-nav" aria-label="Navigazione principale">{links()}</nav>
  <a class="header-phone" href="{TEL}" aria-label="Chiama l’ufficio traffico: {PHONE}">{icon('phone')}<span>{PHONE}</span></a>
  {button('Richiedi un preventivo', 'contatti.html#richiesta', 'primary header-quote')}
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-mobile" aria-label="Apri il menu" data-menu-toggle><span></span><span></span></button>
</div></header><noscript><nav class="fallback-nav" aria-label="Navigazione senza JavaScript"><a href="servizi.html">Servizi</a><a href="azienda.html">Azienda</a><a href="contatti.html">Contatti</a><a href="lavora-con-noi.html">Lavora con noi</a></nav></noscript>
<div class="mobile-menu" id="menu-mobile" hidden inert data-menu aria-label="Menu di navigazione">
  <nav aria-label="Navigazione mobile"><a href="index.html">Home</a>{links()}</nav>
  <div class="menu-contact"><p>Ufficio traffico</p><a href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  {button('Richiedi un preventivo', 'contatti.html#richiesta', 'primary menu-quote')}
</div>'''


def footer(path=''):
    services = ''.join(f'<li><a href="servizio-{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    if path == 'lavora-con-noi.html':
        actions = f'<a href="mailto:{CAREER_EMAIL}">{icon("mail")}Scrivi</a><a href="#candidatura">Candidati {icon("arrow-right")}</a>'
    else:
        actions = f'<a href="{TEL}">{icon("phone")}Chiama il traffico</a><a href="contatti.html#richiesta">Preventivo {icon("arrow-right")}</a>'
    return f'''<footer class="footer"><div class="wrap footer-top">
  <div class="footer-brand"><a class="logo" href="index.html"><img src="img/logo.svg" width="250" height="81" alt="Rossovento Autotrasporti, home"></a><p>Ogni carico ha una strada.<br>La nostra parte da San Ferlino.</p></div>
  <div><h2>Servizi</h2><ul>{services}</ul></div>
  <div><h2>Rossovento</h2><ul><li><a href="azienda.html">L’azienda</a></li><li><a href="lavora-con-noi.html">Lavora con noi</a></li><li><a href="contatti.html">Contatti e preventivi</a></li><li><a href="privacy.html">Privacy e cookie</a></li></ul></div>
  <div class="footer-contact"><h2>Ufficio traffico</h2><a class="footer-tel" href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><p>{ADDRESS_HTML}</p></div>
</div><div class="wrap footer-bottom"><p>© <span data-year>2026</span> Rossovento Autotrasporti&nbsp;· {COMPANY_IDS}</p><p class="footer-preview">{DEMO_NOTE}</p></div></footer>
<nav class="mobile-actions" aria-label="Azioni rapide">{actions}</nav>'''


def cta(title='La prossima partenza<br><em>si decide qui.</em>', text='Un viaggio solo, un collegamento fisso o un magazzino da organizzare: scrivici cosa ti serve.'):
    return f'''<section class="contact-band"><div class="wrap contact-band-inner"><h2>{title}</h2><div><p>{text}</p><div class="button-row">{button('Richiedi un preventivo', 'contatti.html#richiesta', 'light')}<a class="band-phone" href="{TEL}">{icon('phone')}{PHONE}</a></div></div></div></section>'''


def faq(items, title='Prima di partire,<br><em>un po’ di chiarezza.</em>'):
    rows = ''.join(f'<details class="faq-item"><summary>{q}{icon("plus")}</summary><div class="faq-answer"><p>{answer}</p></div></details>' for q, answer in items)
    return f'<section class="faq section"><div class="wrap faq-grid"><div>{kicker("Domande frequenti")}<h2>{title}</h2><p>Hai un caso particolare? Fai prima a chiamare: risponde l’ufficio traffico.</p><a class="text-link" href="{TEL}">{icon("phone")}{PHONE}</a></div><div class="faq-list">{rows}</div></div></section>'


def process(dark=False):
    rows = [('Scrivi cosa ti serve', 'Per un viaggio: merce, tratta e date. Per il magazzino: quantità, periodo e movimenti.'), ('Ricevi la proposta', 'L’ufficio traffico controlla fattibilità e costi e ti manda una proposta scritta.'), ('Si parte', 'Quando confermi fissiamo ritiro, consegna e riferimenti del viaggio.')]
    return f'<section class="process section{" process-dark" if dark else ""}"><div class="wrap"><div class="section-heading"><div>{kicker("Come lavoriamo")}<h2>Dalla richiesta<br><em>al casello.</em></h2></div><p>Tre passi, con le informazioni giuste fin dal primo giorno.</p></div><ol class="process-list">' + ''.join(f'<li><span class="step-number">0{i+1}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(rows)) + '</ol></div></section>'


def service_showcase():
    rows = ''.join(f'<a class="service-row" href="servizio-{s["slug"]}.html" data-service-image="img/{s["image"]}.webp" data-service-alt="{escape(s["alt"])}" data-service-position="{IMAGE_POSITION.get(s["image"], "")}"><span class="service-index" aria-hidden="true">0{i+1}</span><div><h3>{s["name"]}</h3><p>{s["line"]}</p></div>{icon("arrow-right")}</a>' for i, s in enumerate(SERVICES))
    return f'''<section class="services section" id="servizi"><div class="wrap"><div class="section-heading"><div>{kicker('Servizi')}<h2>Strada, porto<br><em>e magazzino.</em></h2></div><p>Camion in Italia e in Europa, container dai porti, spazio a magazzino: una sola squadra segue la merce in ogni tratto.</p></div><div class="service-showcase"><figure class="service-figure" data-reveal>{picture('tramonto', 'Strada che corre verso il tramonto', cls='service-feature', sizes='(max-width: 760px) 125vw, 900px')}</figure><div class="service-rows">{rows}</div></div></div></section>'''


def page(path, title, description, body, active=None, classes='', schema=None):
    body = body.replace('class="btn btn-primary" type="submit"', 'class="btn btn-primary" type="submit" disabled')
    canonical = BASE + ('/' if path == 'index.html' else '/' + path)
    organization = {'@context': 'https://schema.org', '@type': 'Organization', '@id': BASE + '/#organization', 'name': 'Rossovento Autotrasporti (azienda di fantasia)', 'description': 'Sito dimostrativo: azienda e dati inventati.', 'url': BASE + '/'}
    ld = [organization] + ([schema] if schema else [])
    weight = '700' if path == 'index.html' else '600'
    preload = ''.join(f'<link rel="preload" href="assets/fonts/barlow-condensed-{name}.woff2" as="font" type="font/woff2" crossorigin>' for name in (weight, weight + '-italic'))
    not_found = path == '404.html'
    location = '' if not_found else f'<link rel="canonical" href="{canonical}">'
    og_url = '' if not_found else f'<meta property="og:url" content="{canonical}">'
    output = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#151719">
{location}<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:locale" content="it_IT"><meta property="og:site_name" content="Rossovento Autotrasporti (demo)"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:image" content="{BASE}/assets/og.jpg?v={OG_VERSION}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Rossovento Autotrasporti, sito dimostrativo di un’azienda di fantasia">{og_url}<meta name="twitter:card" content="summary_large_image">
{preload}<link rel="stylesheet" href="assets/fonts/fonts.css"><link rel="stylesheet" href="{ASSET_URLS['css']}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script><script src="{ASSET_URLS['js']}" defer></script></head>
<body class="{classes}">{header(active or path)}<main id="contenuto" tabindex="-1">{body}</main>{footer(path)}</body></html>
'''
    if not_found:
        # Servita per qualsiasi percorso inesistente: i riferimenti locali partono dalla base del sito.
        output = re.sub(r'(href|src)="(?!#|https?:|mailto:|tel:|/)', r'\1="' + BASE_PATH, output)
        output = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="' + re.sub(r'(^|, )img/', r'\1' + BASE_PATH + 'img/', m.group(1)) + '"', output)
    (ROOT / path).write_text(output, encoding='utf-8', newline='\n')


def intro(title, lead, current, image=None, alt='', extra='', kick=''):
    media = f'<div class="page-intro-photo"><div class="page-intro-frame">{picture(image, alt, eager=True, sizes=INTRO_SIZES)}</div></div>' if image else ''
    crumb = f'<nav class="breadcrumb" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{current}</span></nav>' if current else ''
    return f'''<section class="page-intro {'with-photo' if image else ''}"><div class="wrap">{crumb}<div class="intro-copy">{kicker(kick) if kick else ''}<h1>{title}</h1><p class="lead">{lead}</p>{extra}</div></div>{media}</section>'''


def home():
    options = ''.join(f'<option value="{s["short"]}">{s["name"]}</option>' for s in SERVICES)
    quick = f'''<div class="wrap hero-quick-wrap"><div class="hero-quick"><div class="quick-head">{kicker('Preventivo rapido')}<h2 id="quick-title">Cosa deve partire?</h2></div><form class="quick-form" action="contatti.html#dettagli" method="get" aria-labelledby="quick-title" data-quick-form><label for="quick-service">Servizio<select id="quick-service" name="servizio">{options}</select></label><div class="quick-route"><label for="quick-from">Partenza<input id="quick-from" name="da" placeholder="Città o CAP" maxlength="120" autocomplete="off"></label><span class="quick-arrow" aria-hidden="true">{icon('arrow-right')}</span><label for="quick-to">Destinazione<input id="quick-to" name="a" placeholder="Città o CAP" maxlength="120" autocomplete="off"></label></div><p class="quick-logistics" hidden>Nel passo successivo descrivi merce, quantità e periodo.</p><button type="submit" class="btn btn-primary"><span>Continua</span>{icon('arrow-right')}</button></form></div></div>'''
    body = f'''<section class="hero" aria-labelledby="hero-title"><div class="hero-photo"><div class="hero-frame">{picture('camion-strada', 'Camion in autostrada verso un tramonto rosso', eager=True, sizes='(max-width: 760px) 130vw, (max-width: 1000px) 110vw, 1400px')}</div></div><div class="wrap hero-content"><div class="hero-copy">{kicker('Autotrasporti · San Ferlino')}<h1 id="hero-title"><span>Trasporti.</span><span>Logistica.</span><span class="brand-word">Rossovento.</span></h1><p class="hero-lead">Camion in Italia e in Europa, container dai porti e spazio a magazzino. Una persona segue la tua spedizione dalla richiesta alla firma sulla bolla.</p><div class="button-row hero-actions">{button('Guarda i servizi', '#servizi', 'ghost')}<a class="hero-phone" href="{TEL}" aria-label="Chiama l’ufficio traffico: {PHONE}">{icon('phone')}<span><small>Traffico</small>{PHONE}</span></a></div></div></div>{quick}</section>
{service_showcase()}
<section class="logistics section"><div class="wrap logistics-grid"><figure class="logistics-figure" data-reveal>{picture('logistica-aerea', 'Vista dall’alto di un piazzale con camion e auto parcheggiati', sizes='(max-width: 760px) 135vw, 1300px')}<figcaption>Piazzale e magazzino · foto illustrativa</figcaption></figure><div class="logistics-copy">{kicker('Logistica')}<h2>Anche la sosta<br><em>fa parte del viaggio.</em></h2><p>Prima del ritiro, tra due consegne, in attesa della nave: la merce ferma va seguita come quella in strada.</p><ul class="fact-list"><li><strong>Magazzino a pochi metri dal piazzale</strong><span>La merce passa dal camion allo scaffale senza giri inutili.</span></li><li><strong>Una squadra sola</strong><span>Chi organizza i viaggi vede anche cosa c’è in magazzino.</span></li><li><strong>Soste brevi o lunghe</strong><span>Da qualche giorno a qualche mese, con un riepilogo quando serve.</span></li></ul>{button('Vedi la logistica', 'servizio-logistica.html', 'outline')}</div></div></section>
<section class="control-section section" data-truck-section><div class="wrap control-layout"><div class="control-copy">{kicker('In viaggio')}<h2>La strada cambia.<br><em>Il riferimento no.</em></h2><p>Pianificazione, controllo del mezzo e una persona che risponde: in ogni momento sai a chi chiedere.</p><a class="text-link" href="azienda.html">Conosci l’azienda {icon('arrow-right')}</a></div><div class="truck-stage"><div class="truck" data-truck><img src="img/camion-sagoma.svg" width="970" height="681" loading="lazy" decoding="async" alt="Illustrazione di un autoarticolato rosso e bianco"></div><div class="road-line" aria-hidden="true"></div></div></div><div class="wrap control-facts"><div><h3>Pianificazione</h3><p>Merce, tratta e orari di carico decisi prima di partire.</p></div><div><h3>Controllo</h3><p>L’ufficio traffico segue la posizione dei mezzi durante il viaggio.</p></div><div><h3>Contatto diretto</h3><p>Un referente al telefono e per email, fino alla consegna.</p></div></div></section>
{process()}
{faq([('Come chiedo un preventivo?', 'Scegli il servizio e scrivi tratta, merce e date: il modulo raccoglie quello che serve. Se preferisci, chiama il +39&nbsp;000&nbsp;000&nbsp;0000.'), ('Devo sapere già peso e misure?', 'No. Scrivi quello che sai e segnala cosa manca. Più dati ci dai, più la proposta sarà precisa.'), ('Posso chiedere viaggio e magazzino insieme?', 'Sì. Descrivi tutte e due le esigenze nella stessa richiesta: le organizziamo insieme.'), ('Seguite la merce durante il viaggio?', 'Sì. L’ufficio traffico controlla i mezzi e il tuo referente risponde fino alla consegna.'), ('Il prezzo si calcola online?', 'No. Ogni proposta dipende da merce, tratta e condizioni di carico, e la prepara l’ufficio traffico.')])}
{cta()}'''
    page('index.html', 'Rossovento Autotrasporti | Trasporti e logistica da San Ferlino', 'Trasporti nazionali e internazionali, container, logistica e magazzino. Sito dimostrativo di un’azienda di fantasia.', body, classes='home-page')


def service_pages():
    body = intro('Trasporti e logistica<br><em>da San Ferlino.</em>', 'Camion in Italia e in Europa, container tra porti, interporti e aziende, spazio a magazzino gestito dalla stessa squadra.', 'Servizi', 'porto-notte', 'Terminal container illuminato di notte')
    body += '<section class="section paper"><div class="wrap service-directory">' + ''.join(f'<article class="directory-row"><a class="directory-image" href="servizio-{s["slug"]}.html" tabindex="-1" aria-hidden="true">{picture(s["image"], "", sizes="(max-width: 760px) 125vw, 900px")}</a><div><span class="directory-index" aria-hidden="true">0{i+1}</span><h2><a href="servizio-{s["slug"]}.html">{s["name"]}</a></h2><p>{s["lead"]}</p>{button("Scopri il servizio", "servizio-"+s["slug"]+".html", "outline")}</div></article>' for i, s in enumerate(SERVICES)) + '</div></section>'
    body += process(dark=True) + cta()
    page('servizi.html', 'Servizi di trasporto e logistica | Rossovento', 'Trasporti nazionali e internazionali, container, logistica e magazzino: i quattro servizi di Rossovento Autotrasporti (azienda di fantasia).', body)
    for s in SERVICES:
        url = 'contatti.html?' + urlencode({'servizio': s['short']}) + '#richiesta'
        first, rest = s['name'].split(' ', 1)
        body = intro(f'{first}<br><em>{rest}</em>', s['lead'], s['name'], s.get('intro_image', s['image']), s.get('intro_alt', s['alt']))
        points = ''.join(f'<div><dt>{t}</dt><dd>{p}</dd></div>' for t, p in s['points'])
        body += f'<section class="section paper"><div class="wrap service-detail"><div class="detail-lead">{kicker("Il servizio")}<h2>{s["line"]}</h2><p>{s["intro"]}</p><div class="button-row">{button("Richiedi un preventivo", url)}<a class="text-link detail-phone" href="{TEL}">{icon("phone")}{PHONE}</a></div></div><div class="detail-benefits"><h3 class="detail-label">Cosa ottieni</h3><dl class="detail-points">{points}</dl></div></div></section>'
        body += faq(s['faqs'], 'Le domande<br><em>più frequenti.</em>')
        cards = ''.join(f'<a class="related-card" href="servizio-{other["slug"]}.html">{icon(other["icon"], "related-icon")}<h3>{other["name"]}</h3><p>{other["summary"]}</p><span class="related-more">Scopri il servizio {icon("arrow-right")}</span></a>' for other in SERVICES if other != s)
        body += f'<section class="related section paper"><div class="wrap"><div class="related-head">{kicker("Altri servizi")}<h2>La stessa merce,<br><em>altre esigenze.</em></h2></div><div class="related-grid">{cards}</div></div></section>'
        body += cta()
        schema = {'@context': 'https://schema.org', '@type': 'Service', 'name': s['name'], 'serviceType': s['name'], 'description': s['lead'], 'provider': {'@id': BASE + '/#organization'}}
        page('servizio-' + s['slug'] + '.html', s['name'] + ' | Rossovento', s['lead'], body, schema=schema)


def company():
    body = intro('Il lavoro è la strada.<br><em>Le persone sono il&nbsp;riferimento.</em>', 'Rossovento Autotrasporti: camion, container e magazzino da un piazzale di San Ferlino, in Piemonte.', 'Azienda', 'camion-strada', 'Camion in autostrada verso un tramonto rosso')
    body += f'''<section class="section paper"><div class="wrap company-story"><div>{kicker('L’azienda')}<h2>Prima di partire,<br><em>ascoltiamo.</em></h2></div><div><p class="large-copy">Una consegna urgente, un magazzino da riempire, una linea fissa da organizzare. Prima di accendere il motore capiamo bene cosa ti serve.</p><p>Trasporti in Italia e in Europa, container e logistica partono tutti dalla stessa sede, dove lavorano insieme ufficio traffico, autisti e magazzino. Per ogni richiesta hai una persona sola da chiamare, al telefono o per email.</p>{button('Guarda i servizi', 'servizi.html', 'outline')}</div></div></section>
<section class="company-band"><div class="company-band-photo">{picture('camion-nuvole', 'Autoarticolato in bianco e nero su una strada ai piedi delle montagne', sizes='(max-width: 760px) 125vw, 1300px')}</div><div class="wrap company-band-copy"><p>In strada tutti i giorni.<br><em>In ufficio quando ci&nbsp;cerchi.</em></p></div></section>
<section class="section paper"><div class="wrap company-story"><div>{kicker('La sede')}<h2>Un punto fermo.<br><em>A San Ferlino.</em></h2><p>I dati dell’azienda. San Ferlino è un paese di fantasia: indirizzo e recapiti sono inventati per questa demo.</p></div><dl class="company-data"><div><dt>Ragione sociale</dt><dd>Rossovento Autotrasporti S.r.l. (di fantasia)</dd></div><div><dt>Sede</dt><dd>{ADDRESS_HTML}</dd></div><div><dt>Telefono</dt><dd><a href="{TEL}">{PHONE}</a></dd></div><div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div><div><dt>Dati societari</dt><dd>{COMPANY_IDS}</dd></div></dl></div></section>{cta()}'''
    page('azienda.html', 'L’azienda | Rossovento Autotrasporti', 'Rossovento Autotrasporti: trasporti e logistica da San Ferlino, con un referente per ogni richiesta. Azienda di fantasia.', body)


def field(name, label, required=False, type='text', placeholder='', autocomplete=None, help=None, textarea=False):
    id = 'f-' + name
    req = ' required' if required else ''
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ''
    hint = f'<small class="field-hint" id="{id}-hint">{help}</small>' if help else ''
    desc = f'{id}-error' + (f' {id}-hint' if help else '')
    attrs = f'id="{id}" name="{name}"{req}{ac} aria-describedby="{desc}" placeholder="{escape(placeholder, quote=True)}"'
    limit = '' if type == 'date' else ' maxlength="180"'
    control = f'<textarea {attrs} rows="4" maxlength="2500"></textarea>' if textarea else f'<input {attrs} type="{type}"{limit}>'
    return f'<div class="field"><label for="{id}">{label}{" <span aria-hidden=\"true\">*</span>" if required else " <span class=\"optional\">(facoltativo)</span>"}</label>{control}{hint}<small class="field-error" id="{id}-error" hidden></small></div>'


def select(name, label, options, help=''):
    opts = ''.join(f'<option value="{escape(v, quote=True)}">{escape(v)}</option>' for v in options)
    return f'<div class="field"><label for="f-{name}">{label}</label><select id="f-{name}" name="{name}">{opts}</select>{"<small class=\"field-hint\">" + help + "</small>" if help else ""}</div>'


def summary(kind):
    career = kind == 'career'
    noun = 'candidatura' if career else 'richiesta'
    return f'''<section class="form-summary" data-form-summary hidden aria-labelledby="summary-title"><div class="summary-check">{icon('check')}</div><h2 id="summary-title" tabindex="-1">Ecco la tua {noun}.</h2><p>Controlla i dati. In un sito vero da qui partirebbe la {noun}; in questa demo nulla viene inviato e puoi solo scaricare il riepilogo.</p><dl data-summary-list></dl><div class="summary-actions"><button class="btn btn-outline" type="button" data-edit-request>Modifica i dati</button><button class="text-link" type="button" data-download-summary>Scarica il riepilogo {icon('download')}</button></div><p class="summary-fallback">Sito dimostrativo: i dati restano nel tuo browser.</p></section>'''


def privacy_field():
    return '<div class="privacy-field"><label for="f-privacy"><input id="f-privacy" type="checkbox" name="privacy" required aria-describedby="f-privacy-error"><span>Ho letto l’<a href="privacy.html" target="_blank" rel="noopener">informativa privacy</a>. <span aria-hidden="true">*</span></span></label><small id="f-privacy-error" class="field-error" hidden></small></div>'


def quote_form():
    radios = ''.join(f'<label class="service-choice"><input type="radio" name="servizio" value="{s["short"]}"{" checked" if i == 0 else ""}>{icon(s["icon"])}<span>{s["short"]}</span></label>' for i, s in enumerate(SERVICES))
    return f'''<form class="request-form" id="richiesta" data-request-form data-kind="quote" novalidate><div data-form-fields>
<div class="form-heading">{kicker('Richiesta di preventivo')}<h2>Raccontaci la spedizione.</h2><p>I&nbsp;campi con&nbsp;* sono obbligatori. Ogni dettaglio in più rende la proposta più precisa.</p></div><p class="form-error-summary" data-error-summary role="alert" hidden></p>
<fieldset><legend><span class="step-tag">01</span> Scegli il servizio</legend><div class="service-choices">{radios}</div><p class="service-context" data-service-context>Descrivi il trasporto da organizzare in Italia.</p><p class="sr-only" role="status" data-service-status></p></fieldset>
<fieldset id="dettagli"><legend><span class="step-tag">02</span> <span data-detail-heading>Descrivi la spedizione</span></legend>
<p class="route-note" data-route-note hidden>Tratta inserita: <strong data-route-text></strong> · <button type="button" class="route-edit" data-route-edit>modifica</button></p>
<div class="route-fields field-grid" data-fields="transport">{field('da', 'Partenza', True, placeholder='Città, CAP e Paese')}{field('a', 'Destinazione', True, placeholder='Città, CAP e Paese')}</div>
<div class="conditional-fields field-grid" data-fields="container" hidden>{select('container_tipo', 'Tipo di container', ['Da definire', '20 piedi', '40 piedi', '40 piedi High Cube', 'Altro'])}{select('operazione', 'Operazione richiesta', ['Da definire', 'Import', 'Export', 'Altro'])}</div>
<div class="conditional-fields field-grid" data-fields="logistics" hidden>{field('quantita_logistica', 'Quantità da tenere in magazzino', False, placeholder='Es. numero di pallet o colli')}{select('periodo', 'Per quanto tempo', ['Da definire', 'Meno di un mese', 'Da uno a tre mesi', 'Più di tre mesi', 'Sempre'])}</div>
<div class="field-grid" data-fields="shipment">{field('quantita', 'Quantità e peso', False, placeholder='Es. pallet, colli e kg')}{field('data', 'Data di partenza', False, type='date')}</div>
{field('merce', 'Merce ed esigenze', True, textarea=True, placeholder='Che merce è, com’è imballata, come si carica e si scarica.', help='Se qualche dato manca ancora, scrivilo&nbsp;qui.')}</fieldset>
<fieldset><legend><span class="step-tag">03</span> Come ricontattarti</legend><div class="field-grid">{field('nome', 'Nome e cognome', True, autocomplete='name')}{field('azienda', 'Azienda', False, autocomplete='organization')}{field('email', 'Email', True, type='email', autocomplete='email')}{field('telefono', 'Telefono', False, type='tel', autocomplete='tel')}</div></fieldset>
{privacy_field()}
<div class="form-submit"><button class="btn btn-primary" type="submit">Rivedi la richiesta {icon('arrow-right')}</button><p>Sito dimostrativo: vedrai solo un riepilogo, non parte nessuna email.</p></div></div>{summary('quote')}<noscript><p class="noscript-note">Per vedere il riepilogo serve JavaScript. In questa demo non è previsto un invio alternativo.</p></noscript></form>'''


def contacts():
    body = intro('Parliamo del tuo<br><em>prossimo carico.</em>', 'Camion, container o magazzino: descrivi cosa ti serve oppure chiama l’ufficio traffico.', 'Contatti', 'autostrada-aerea', 'Autostrada vista dall’alto con un autoarticolato in viaggio')
    body += f'''<section class="contact-section section paper"><div class="wrap contact-layout"><aside class="contact-aside">{kicker('Ufficio traffico')}<h2>Rispondiamo<br><em>direttamente.</em></h2><p>Telefono ed email dell’ufficio traffico, per ogni richiesta di trasporto e magazzino. Recapiti di fantasia.</p><a class="contact-number" href="{TEL}">{PHONE}{icon('phone')}</a><a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a><div class="address-block">{icon('map-pin')}<div><h3>La sede</h3><p>{ADDRESS_HTML}</p></div></div><p class="contact-note">Per ritiri e consegne in sede, concorda prima giorno e orario.</p></aside>{quote_form()}</div></section>'''
    page('contatti.html', 'Contatti e preventivi | Rossovento', 'Prepara una richiesta di trasporto, container o logistica. Modulo dimostrativo: non invia dati.', body, classes='contact-page')


def careers():
    form = f'''<form class="request-form" id="candidatura" data-request-form data-kind="career" novalidate><div data-form-fields><div class="form-heading">{kicker('Candidatura spontanea')}<h2>Presentati.</h2><p>Raccontaci esperienza, patenti e disponibilità. I&nbsp;campi con&nbsp;* sono obbligatori.</p></div><p class="form-error-summary" data-error-summary role="alert" hidden></p><div class="field-grid">{field('nome', 'Nome e cognome', True, autocomplete='name')}{field('email', 'Email', True, type='email', autocomplete='email')}{field('telefono', 'Telefono', False, type='tel', autocomplete='tel')}{select('ruolo', 'Ambito di interesse', ['Autista', 'Magazzino', 'Traffico e logistica', 'Altro'])}</div>{field('esperienza', 'La tua esperienza', True, textarea=True, placeholder='Esperienza, patenti e qualifiche, disponibilità.')}{privacy_field()}<div class="form-submit"><button class="btn btn-primary" type="submit">Rivedi la candidatura {icon('arrow-right')}</button><p>Sito dimostrativo: vedrai solo un riepilogo, non parte nulla.</p></div></div>{summary('career')}<noscript><p>Per vedere il riepilogo serve JavaScript.</p></noscript></form>'''
    body = intro('La prossima strada<br><em>potrebbe essere la&nbsp;tua.</em>', 'Autisti, magazzino, traffico e logistica: presentati con una candidatura spontanea.', 'Lavora con noi', 'tramonto', 'Strada che corre verso il tramonto')
    roles = ''.join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in [('truck', 'Autisti'), ('warehouse', 'Magazzino'), ('globe', 'Traffico e logistica')])
    body += f'<section class="section paper"><div class="wrap contact-layout"><aside class="contact-aside">{kicker("Lavora con noi")}<h2>Il viaggio<br><em>lo fanno le persone.</em></h2><p>Se vuoi lavorare nei trasporti, mandaci il tuo profilo: esperienza, patenti, qualifiche e disponibilità.</p><ul class="role-list">{roles}</ul><p>Una candidatura spontanea non vuol dire che ci sia una posizione aperta.</p><div class="address-block">{icon("mail")}<div><h3>Preferisci scrivere?</h3><a href="mailto:{CAREER_EMAIL}">{CAREER_EMAIL}</a></div></div></aside>{form}</div></section>'
    page('lavora-con-noi.html', 'Lavora con noi | Rossovento', 'Candidatura spontanea per autisti, magazzino, traffico e logistica. Modulo dimostrativo.', body)


def privacy():
    body = intro('Privacy<br><em>e cookie.</em>', 'Come sarebbe trattato chi scrive da questo sito, e quali servizi esterni usa.', 'Privacy e cookie')
    body += f'''<section class="section paper"><article class="wrap legal-content"><p class="draft-note">Esempio di informativa per un’azienda di fantasia.</p><h2>Titolare del trattamento</h2><p>Rossovento Autotrasporti S.r.l. (azienda di fantasia), {ADDRESS_HTML}. Email di esempio: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><h2>Quali dati</h2><p>In un sito reale: nome, azienda, recapiti e dettagli della richiesta di trasporto o di magazzino. Per le candidature, contatti, esperienza e curriculum.</p><h2>Come arrivano</h2><p>In questa demo i moduli mostrano solo un riepilogo nella pagina. Nulla viene trasmesso o salvato.</p><h2>Finalità e base giuridica</h2><p>Rispondere a richieste di preventivo e informazioni e gestire i rapporti che ne derivano (art. 6.1.b GDPR). Valutare le candidature spontanee (art. 6.1.b GDPR e, per eventuali dati particolari, art. 9.2.b).</p><h2>Conservazione e destinatari</h2><p>Il tempo necessario a gestire la richiesta e a rispettare gli obblighi di legge. Accesso limitato al personale incaricato e ai fornitori di posta e hosting.</p><h2>Diritti</h2><p>Accesso, rettifica, cancellazione, limitazione, portabilità e opposizione (artt. 15–22 GDPR), più il reclamo al Garante per la protezione dei dati personali.</p><h2>Cookie e servizi esterni</h2><p>Il sito non usa cookie di profilazione né strumenti di statistica. Font, icone e immagini sono ospitati insieme alle pagine. Non ci sono mappe o contenuti esterni incorporati.</p></article></section>'''
    page('privacy.html', 'Privacy e cookie | Rossovento', 'Esempio di informativa privacy per il sito dimostrativo di un’azienda di fantasia.', body)


def not_found():
    actions = f'<div class="button-row intro-actions">{button("Torna alla home", "index.html")}{button("Scopri i servizi", "servizi.html", "ghost")}<a class="band-phone" href="{TEL}">{icon("phone")}{PHONE}</a></div>'
    body = intro('Strada sbagliata.<br><em>Questa pagina non&nbsp;c’è.</em>', 'L’indirizzo può essere cambiato o non esistere più. Riparti dalla home o chiama l’ufficio traffico.', '', 'porto-notte', '', actions, 'Errore 404')
    page('404.html', 'Pagina non trovata | Rossovento', 'La pagina richiesta non è disponibile.', body, classes='not-found')


def build():
    home()
    service_pages()
    company()
    contacts()
    careers()
    privacy()
    not_found()
    files = sorted(p.name for p in ROOT.glob('*.html'))
    urls = ''.join(f'<url><loc>{BASE}/{"" if name == "index.html" else name}</loc></url>\n' for name in files if name != '404.html')
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text('# Sito dimostrativo di un’azienda di fantasia: escluso dai motori di ricerca.\nUser-agent: *\nDisallow: /\n', encoding='utf-8')
    print(f'Generate {len(files)} pagine in {ROOT}')


if __name__ == '__main__':
    build()
