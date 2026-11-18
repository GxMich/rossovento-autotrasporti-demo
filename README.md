# Rossovento Autotrasporti — sito dimostrativo

> **Azienda di fantasia.** Rossovento Autotrasporti e il paese di San Ferlino non esistono. Nomi, recapiti, indirizzo e testi sono inventati. Il sito è una demo realizzata da [Michele Modica](https://www.modicamichele.it) per mostrare come potrebbe presentarsi online un'impresa di autotrasporti e logistica.

**Online:** https://gxmich.github.io/rossovento-autotrasporti-demo/

## Cosa mostra la demo

- **Home cinematografica**: titolo a tre righe, foto a tutta pagina con taglio obliquo e **preventivo rapido** (servizio, partenza, destinazione) che apre la pagina contatti con i dati già inseriti.
- **Servizi** con foto che cambia al passaggio del mouse, quattro **pagine servizio** (nazionali, internazionali, container, logistica) con punti chiave, domande frequenti e servizi collegati.
- **Camion illustrato che avanza allo scorrimento** lungo una strada tratteggiata.
- **Richiesta di preventivo** con campi diversi per trasporto, container e magazzino, validazione e riepilogo scaricabile in testo. **Lavora con noi** con candidatura spontanea. Entrambi i moduli sono simulati: nessun dato viene inviato o salvato.
- Menu mobile, azioni rapide su telefono e rispetto dell'impostazione «riduci movimento».

Tutte le pagine hanno `noindex, nofollow` e `robots.txt` blocca l'indicizzazione: un'azienda inventata non deve comparire nelle ricerche.

## Tecnologie

HTML, CSS e JavaScript senza framework né dipendenze esterne. Font Barlow e Barlow Condensed e icone Lucide ospitati in locale. Le pagine si generano con `scripts/build.py` (solo libreria standard di Python); `scripts/check.py` controlla link, ancore, JSON-LD e `noindex`.

## Avviarla in locale

```bash
python scripts/build.py      # rigenera le pagine, sitemap e robots.txt
python scripts/check.py      # controlli automatici
python -m http.server 4173   # poi apri http://localhost:4173
```

Crediti delle foto in [CREDITI-FOTO.md](CREDITI-FOTO.md). Il sito è pubblicato con GitHub Pages dal ramo `main`.
