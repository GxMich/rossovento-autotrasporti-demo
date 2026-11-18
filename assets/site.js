/* Rossovento (demo). Local, dependency-free interactions; the demo never submits data. */
(() => {
  'use strict';

  const root = document.documentElement;
  root.classList.add('js');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const smallScreen = window.matchMedia('(max-width: 760px)');
  const ease = 'cubic-bezier(.22,1,.36,1)';
  const $ = (selector, context = document) => context.querySelector(selector);
  const $$ = (selector, context = document) => [...context.querySelectorAll(selector)];

  $$('[data-year]').forEach(element => { element.textContent = String(new Date().getFullYear()); });

  /* Menu: focus never moves into the page behind the open navigation. */
  const menu = $('[data-menu]');
  const toggle = $('[data-menu-toggle]');
  let menuOpen = false;
  let menuTimer;
  const background = [$('main'), $('.footer'), $('.mobile-actions')].filter(Boolean);

  function setMenu(open, restoreFocus = true) {
    if (!menu || !toggle || open === menuOpen) return;
    clearTimeout(menuTimer);
    menuOpen = open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
    document.body.classList.toggle('menu-open', open);
    background.forEach(element => { element.inert = open; });
    if (open) {
      menu.hidden = false;
      menu.inert = false;
      requestAnimationFrame(() => {
        if (!menuOpen) return;
        menu.classList.add('is-open');
        if (!motion.matches) {
          $$('nav a', menu).forEach((link, index) => {
            link.getAnimations().forEach(animation => animation.cancel());
            link.animate([{ transform: 'translateX(-18px)', opacity: .6 }, { transform: 'none', opacity: 1 }], { duration: 380, delay: index * 45, easing: ease });
          });
        }
        $('a', menu)?.focus();
      });
    } else {
      menu.classList.remove('is-open');
      menu.inert = true;
      menuTimer = setTimeout(() => { if (!menuOpen) menu.hidden = true; }, motion.matches ? 0 : 260);
      if (restoreFocus) toggle.focus();
    }
  }

  toggle?.addEventListener('click', () => setMenu(!menuOpen));
  menu?.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false, false); });
  document.addEventListener('keydown', event => {
    if (!menuOpen) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      setMenu(false);
      return;
    }
    if (event.key !== 'Tab') return;
    const items = [toggle, ...$$('a[href], button:not(:disabled)', menu)];
    const first = items[0];
    const last = items.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 1000 && menuOpen) setMenu(false, false); }, { passive: true });

  /* A quick logistics enquiry must not require an invented transport route. */
  const quick = $('[data-quick-form]');
  if (quick) {
    const select = $('select', quick);
    const route = $('.quick-route', quick);
    const logistics = $('.quick-logistics', quick);
    const update = () => {
      const isLogistics = select.value === 'Logistica';
      route.hidden = isLogistics;
      $$('input', route).forEach(input => { input.disabled = isLogistics; });
      logistics.hidden = !isLogistics;
    };
    select.addEventListener('change', update);
    update();
  }

  /* Photograph changes follow the service under the pointer or keyboard focus. */
  const feature = $('.service-feature');
  let imageRequest = 0;
  if (feature) {
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
    $$('[data-service-image]').forEach(link => {
      const change = async () => {
        if (!finePointer.matches) return;
        const request = ++imageRequest;
        const image = new Image();
        image.src = link.dataset.serviceImage;
        try { await image.decode(); } catch { return; }
        if (request !== imageRequest) return;
        feature.removeAttribute('srcset');
        feature.removeAttribute('sizes');
        feature.src = image.src;
        feature.alt = link.dataset.serviceAlt;
        feature.style.objectPosition = link.dataset.servicePosition || '';
        feature.getAnimations().forEach(animation => animation.cancel());
        if (!motion.matches) feature.animate([
          { clipPath: 'inset(0 15% 0 0)', transform: 'translateX(-12px) scale(1.04)', opacity: .7 },
          { clipPath: 'inset(0)', transform: 'none', opacity: 1 }
        ], { duration: 420, easing: ease });
      };
      link.addEventListener('pointerenter', change);
      link.addEventListener('focus', change);
    });
  }

  /* Local qualification and review. No fetch, storage, tracking or simulated send. */
  const query = new URLSearchParams(window.location.search);
  const serviceTitles = { Nazionali: 'Trasporti nazionali', Internazionali: 'Trasporti internazionali', Container: 'Trasporti container', Logistica: 'Logistica e magazzino' };
  const serviceNames = Object.keys(serviceTitles);
  const requestedService = serviceNames.find(name => name.toLocaleLowerCase('it') === (query.get('servizio') || '').toLocaleLowerCase('it'));
  const serviceDescriptions = {
    Nazionali: 'Descrivi il trasporto da organizzare in Italia.',
    Internazionali: 'Indica anche i Paesi di partenza e di destinazione.',
    Container: 'Indica porto o terminal, destinazione e operazione richiesta.',
    Logistica: 'Parliamo di magazzino: merce, quantità, periodo e movimenti previsti.'
  };
  const fieldLabels = {
    servizio: 'Servizio', da: 'Partenza', a: 'Destinazione', container_tipo: 'Tipo di container',
    operazione: 'Operazione richiesta', quantita_logistica: 'Quantità da stoccare', periodo: 'Periodo di stoccaggio',
    quantita: 'Quantità e peso', data: 'Data desiderata', merce: 'Merce ed esigenze', nome: 'Nome e cognome',
    azienda: 'Azienda', email: 'Email', telefono: 'Telefono', ruolo: 'Ambito di interesse', esperienza: 'Esperienza e disponibilità'
  };
  const requiredErrors = {
    da: 'Indica la località di partenza.', a: 'Indica la destinazione.', merce: 'Descrivi la merce e la tua esigenza.',
    nome: 'Inserisci il tuo nome e cognome.', email: 'Inserisci un indirizzo email valido, per esempio nome@azienda.it.',
    careerEmail: 'Inserisci un indirizzo email valido, per esempio mario.rossi@gmail.com.', container: 'Indica il porto o terminal di ritiro.',
    privacy: 'Conferma di aver letto l’informativa privacy.', esperienza: 'Raccontaci brevemente la tua esperienza.'
  };

  $$('[data-request-form]').forEach(form => {
    const career = form.dataset.kind === 'career';
    const fields = $('[data-form-fields]', form);
    const summary = $('[data-form-summary]', form);
    const summaryList = $('[data-summary-list]', form);
    const errorSummary = $('[data-error-summary]', form);
    const routeGroup = $('.route-fields', form);
    const routeNote = $('[data-route-note]', form);
    let summaryText = '';
    let routeCollapsed = false;

    function setRouteCollapsed(collapsed) {
      routeCollapsed = collapsed;
      if (!routeGroup || !routeNote) return;
      routeGroup.classList.toggle('is-collapsed', collapsed);
      routeNote.hidden = !collapsed || routeGroup.hidden;
      if (collapsed) $('[data-route-text]', routeNote).textContent = `${$('#f-da', form).value} → ${$('#f-a', form).value}`;
    }

    function errorNode(control) { return document.getElementById(`${control.id}-error`); }
    function clearError(control) {
      control.removeAttribute('aria-invalid');
      const message = errorNode(control);
      if (message) { message.hidden = true; message.textContent = ''; }
    }

    function updateService(announce = true) {
      const selected = $('input[name="servizio"]:checked', form)?.value || 'Nazionali';
      const logistics = selected === 'Logistica';
      $$('[data-fields]', form).forEach(group => {
        const show = group.dataset.fields === 'container' ? selected === 'Container' : group.dataset.fields === 'logistics' ? logistics : !logistics;
        group.hidden = !show;
        $$('input, select, textarea', group).forEach(control => {
          control.disabled = !show;
          if (!show) clearError(control);
        });
      });
      const context = $('[data-service-context]', form);
      const detailHeading = $('[data-detail-heading]', form);
      if (context) context.textContent = serviceDescriptions[selected];
      if (detailHeading) detailHeading.textContent = logistics ? 'Descrivi l’esigenza di magazzino' : 'Descrivi la spedizione';
      const from = $('#f-da', form);
      const fromLabel = $('label[for="f-da"]', form);
      if (from && fromLabel) {
        fromLabel.textContent = selected === 'Container' ? 'Porto o terminal di ritiro *' : 'Partenza *';
        from.placeholder = selected === 'Container' ? 'Porto, terminal o località di ritiro' : selected === 'Internazionali' ? 'Città, CAP e Paese' : 'Città o CAP';
      }
      const to = $('#f-a', form);
      if (to) to.placeholder = selected === 'Internazionali' ? 'Città, CAP e Paese' : selected === 'Container' ? 'Stabilimento o località di consegna' : 'Città o CAP';
      const description = $('#f-merce', form);
      if (description) description.placeholder = logistics ? 'Merce e imballaggio, periodo previsto, movimenti in ingresso e in uscita, eventuale trasporto.' : 'Descrivi la merce, l’imballaggio e le esigenze di carico e scarico.';
      /* A container route starts from a port or terminal: show the fields again. */
      if (routeCollapsed && selected === 'Container') setRouteCollapsed(false);
      else if (routeNote) routeNote.hidden = !routeCollapsed || routeGroup.hidden;
      if (announce) $('[data-service-status]', form).textContent = `Servizio selezionato: ${serviceTitles[selected]}. I campi della richiesta sono stati aggiornati.`;
      if (!$$('[aria-invalid="true"]', form).length) errorSummary.hidden = true;
    }

    if (!career) {
      if (requestedService) $$('input[name="servizio"]', form).forEach(radio => { radio.checked = radio.value === requestedService; });
      for (const name of ['da', 'a']) {
        const value = (query.get(name) || '').trim();
        const control = form.elements.namedItem(name);
        if (value && control) control.value = value.slice(0, 120);
      }
      if ($('#f-da', form)?.value && $('#f-a', form)?.value && requestedService !== 'Container') setRouteCollapsed(true);
      $('[data-route-edit]', form)?.addEventListener('click', () => {
        setRouteCollapsed(false);
        $('#f-da', form).focus();
      });
      $$('input[name="servizio"]', form).forEach(radio => radio.addEventListener('change', () => updateService()));
      const date = $('input[type="date"]', form);
      if (date) {
        const now = new Date();
        date.min = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
      }
      updateService(false);
    }

    const controls = $$('input, textarea, select', form);
    controls.forEach(control => {
      const onInput = () => {
        if (control.getAttribute('aria-invalid') === 'true' && control.checkValidity()) clearError(control);
        if (!$$('[aria-invalid="true"]', form).length) errorSummary.hidden = true;
      };
      control.addEventListener('input', onInput);
      control.addEventListener('change', onInput);
    });

    form.addEventListener('submit', event => {
      event.preventDefault();
      const invalid = [];
      controls.forEach(control => {
        if (control.disabled || control.type === 'radio' || control.type === 'submit') return;
        if (['text', 'email', 'tel', 'textarea'].includes(control.type)) control.value = control.value.trim();
        if (control.checkValidity()) { clearError(control); return; }
        invalid.push(control);
        control.setAttribute('aria-invalid', 'true');
        const message = errorNode(control);
        if (message) {
          const service = $('input[name="servizio"]:checked', form)?.value;
          const key = control.name === 'email' && career ? 'careerEmail' : control.name === 'da' && service === 'Container' ? 'container' : control.name;
          message.textContent = control.validity.rangeUnderflow ? 'Scegli una data da oggi in avanti oppure lascia il campo vuoto.' : requiredErrors[key] || 'Controlla questo campo e completa l’informazione richiesta.';
          message.hidden = false;
        }
      });
      errorSummary.hidden = invalid.length === 0;
      if (invalid.some(control => control.closest('.is-collapsed'))) setRouteCollapsed(false);
      if (invalid.length) {
        errorSummary.textContent = invalid.length === 1 ? 'C’è un campo da controllare. Trovi l’indicazione vicino al campo.' : `Ci sono ${invalid.length} campi da controllare. Trovi le indicazioni vicino ai campi.`;
        invalid[0].focus({ preventScroll: true });
        invalid[0].scrollIntoView({ behavior: motion.matches ? 'auto' : 'smooth', block: 'center' });
        return;
      }

      const data = new FormData(form);
      const fragment = document.createDocumentFragment();
      const pairs = [];
      for (const [name, value] of data.entries()) {
        if (name === 'privacy' || !String(value).trim()) continue;
        let formatted = String(value);
        if (name === 'data' && /^\d{4}-\d{2}-\d{2}$/.test(formatted)) formatted = formatted.split('-').reverse().join('/');
        if (name === 'servizio') formatted = serviceTitles[formatted] || formatted;
        const label = name === 'da' && data.get('servizio') === 'Container' ? 'Porto o terminal di ritiro' : fieldLabels[name] || name;
        const row = document.createElement('div');
        const term = document.createElement('dt');
        const definition = document.createElement('dd');
        term.textContent = label;
        definition.textContent = formatted;
        row.append(term, definition);
        fragment.append(row);
        pairs.push(`${label}: ${formatted}`);
      }
      summaryList.replaceChildren(fragment);
      const subject = career ? `Candidatura spontanea — ${data.get('nome')}` : `Richiesta di preventivo — ${serviceTitles[data.get('servizio')] || data.get('servizio')}`;
      summaryText = `${subject}\n\n${pairs.join('\n\n')}\n\n— Sito dimostrativo Rossovento Autotrasporti (azienda di fantasia): nulla è stato inviato.\n`;
      fields.hidden = true;
      summary.hidden = false;
      const heading = $('h2', summary);
      heading.focus({ preventScroll: true });
      form.scrollIntoView({ behavior: motion.matches ? 'auto' : 'smooth', block: 'start' });
      if (!motion.matches) summary.animate([{ transform: 'translateY(8px)' }, { transform: 'none' }], { duration: 240, easing: ease });
    });

    $('[data-edit-request]', form)?.addEventListener('click', () => {
      summary.hidden = true;
      fields.hidden = false;
      const first = career ? $('input[name="nome"]', form) : $('input[name="servizio"]:checked', form);
      first.focus({ preventScroll: true });
      form.scrollIntoView({ behavior: motion.matches ? 'auto' : 'smooth', block: 'start' });
    });

    $('[data-download-summary]', form)?.addEventListener('click', () => {
      const url = URL.createObjectURL(new Blob([summaryText], { type: 'text/plain;charset=utf-8' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = career ? 'candidatura-demo.txt' : 'richiesta-demo.txt';
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    $$('button[type="submit"]', form).forEach(button => { button.disabled = false; });
  });

  /* Leave space for the native keyboard on a phone. */
  function updateKeyboard() {
    const active = document.activeElement;
    const textEntry = active?.matches('input:not([type="radio"]):not([type="checkbox"]), textarea, select');
    document.body.classList.toggle('keyboard-active', Boolean(smallScreen.matches && textEntry));
  }
  document.addEventListener('focusin', updateKeyboard);
  document.addEventListener('focusout', () => requestAnimationFrame(updateKeyboard));
  smallScreen.addEventListener('change', updateKeyboard);

  /* The road is the visual thread: a depth scene and a truck that approaches.
     Frames are requested only after input, never in a continuous idle loop. */
  const hero = $('.hero');
  const heroPhoto = $('.hero-photo');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const posterLayout = window.matchMedia('(max-width: 1000px)');
  const truckSection = $('[data-truck-section]');
  const truck = $('[data-truck]');
  const road = $('.road-line');
  let roadWidth = road?.clientWidth || 0;
  let heroVisible = Boolean(hero);
  let truckVisible = false;
  let framePending = false;
  let pointerX = 0;
  let pointerY = 0;
  function drawTruck() {
    framePending = false;
    if (motion.matches) {
      if (truck) truck.style.removeProperty('transform');
      return;
    }
    if (document.hidden) return;
    if (heroPhoto && heroVisible) {
      /* Dolly-in: while the visitor scrolls, the truck keeps coming closer. */
      const rect = hero.getBoundingClientRect();
      const progress = Math.max(0, Math.min(1, -rect.top / Math.max(1, rect.height)));
      heroPhoto.style.setProperty('--scene-scroll', `${(progress * (posterLayout.matches ? 8 : 14)).toFixed(2)}px`);
      heroPhoto.style.setProperty('--scene-zoom', (progress * (posterLayout.matches ? .04 : .05)).toFixed(4));
      heroPhoto.style.setProperty('--scene-x', `${pointerX.toFixed(2)}px`);
      heroPhoto.style.setProperty('--scene-y', `${pointerY.toFixed(2)}px`);
    }
    if (!truck || !truckVisible) return;
    /* The cut-out truck approaches along the road: from far and to the left, to full size. */
    const rect = truckSection.getBoundingClientRect();
    const progress = Math.max(0, Math.min(1, (window.innerHeight - rect.top) / (window.innerHeight * .95 + rect.height * .55)));
    const eased = 1 - Math.pow(1 - progress, 2);
    const distance = smallScreen.matches ? 70 : 220;
    const scale = smallScreen.matches ? .78 + eased * .22 : .62 + eased * .4;
    truck.style.transform = `translate3d(${((1 - eased) * -distance).toFixed(2)}px,${((1 - eased) * -14).toFixed(2)}px,0) scale(${scale.toFixed(3)})`;
    if (road) {
      road.style.setProperty('--road-travel', `${(progress * Math.max(0, roadWidth - 96)).toFixed(2)}px`);
      road.style.setProperty('--road-dash', `${(progress * -328).toFixed(2)}px`);
    }
  }
  function scheduleTruck() {
    if (framePending || motion.matches || document.hidden || (!truckVisible && !heroVisible)) return;
    framePending = true;
    requestAnimationFrame(drawTruck);
  }
  if ((hero || truck) && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.target === hero) heroVisible = entry.isIntersecting;
        if (entry.target === truckSection) truckVisible = entry.isIntersecting;
      });
      scheduleTruck();
    });
    if (hero) observer.observe(hero);
    if (truck) observer.observe(truckSection);
    window.addEventListener('scroll', scheduleTruck, { passive: true });
    window.addEventListener('resize', () => { roadWidth = road?.clientWidth || 0; scheduleTruck(); }, { passive: true });
    document.addEventListener('visibilitychange', scheduleTruck);
    hero?.addEventListener('pointermove', event => {
      if (!finePointer.matches || motion.matches || posterLayout.matches) return;
      const rect = hero.getBoundingClientRect();
      pointerX = ((event.clientX - rect.left) / rect.width - .5) * -20;
      pointerY = ((event.clientY - rect.top) / rect.height - .5) * -8;
      scheduleTruck();
    }, { passive: true });
    hero?.addEventListener('pointerleave', () => { pointerX = 0; pointerY = 0; scheduleTruck(); }, { passive: true });
  }

  /* Each sequence has its own job: service choices, the operational process,
     photographs and short internal-page titles. Text is visible by default. */
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        const element = entry.target;
        element.classList.add('is-in-view');
        if (motion.matches) return;
        if (element.matches('[data-enter]')) {
          /* Lateral, slightly oblique entrance: the same slant as the photographs. */
          element.animate([
            { transform: 'translate3d(-42px, 0, 0) skewX(5deg)', opacity: .25 },
            { transform: 'none', opacity: 1 }
          ], { duration: 720, easing: ease });
        } else if (element.matches('.service-rows, .process-list, .control-facts')) {
          [...element.children].forEach((item, index) => {
            const service = element.matches('.service-rows');
            item.animate([
              { transform: service ? 'translateX(-18px)' : 'translateY(23px)', opacity: .65 },
              { transform: 'none', opacity: 1 }
            ], { duration: service ? 480 : 520, delay: Math.min(index * 75, 210), easing: ease });
          });
        } else {
          element.animate([
            { clipPath: 'inset(0 0 10% 0)', transform: 'translateY(20px)' },
            { clipPath: 'inset(0)', transform: 'none' }
          ], { duration: 650, easing: ease });
        }
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    $$('.section-heading > div, .logistics-copy > h2, .control-copy > h2, .faq-grid > div:first-child > h2, .detail-lead > h2, .company-story > div:first-child > h2, .related h2, .company-band p, .contact-band h2, .contact-aside > h2, .directory-row h2').forEach(element => element.setAttribute('data-enter', ''));
    $$('[data-reveal], [data-enter], .service-rows, .process-list, .control-facts, .page-intro h1').forEach(element => observer.observe(element));
  }

  const faqAnimations = new WeakMap();
  $$('.faq-item').forEach(details => {
    details.addEventListener('toggle', () => {
      faqAnimations.get(details)?.cancel();
      if (!details.open || motion.matches) return;
      const answer = $('.faq-answer', details);
      const animation = answer.animate([
        { height: '0px', opacity: .55 },
        { height: `${answer.scrollHeight}px`, opacity: 1 }
      ], { duration: 260, easing: ease });
      faqAnimations.set(details, animation);
    });
  });
  motion.addEventListener('change', () => {
    if (motion.matches) {
      document.getAnimations().forEach(animation => animation.cancel());
      if (truck) truck.style.removeProperty('transform');
      ['--scene-x', '--scene-y', '--scene-scroll', '--scene-zoom'].forEach(property => heroPhoto?.style.removeProperty(property));
      road?.style.removeProperty('--road-travel');
      road?.style.removeProperty('--road-dash');
    } else scheduleTruck();
  });
})();
