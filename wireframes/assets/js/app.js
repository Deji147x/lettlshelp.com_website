// Mobile navigation + wireframe-notes toggle. No other JavaScript is needed.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  // Navigation dropdowns (About, Services, and the hub's two practice menus).
  // The markup is a real <button aria-expanded> plus a <ul>, so this only has to open and
  // close it. With JavaScript off nothing runs, the CSS leaves the panel in the flow, and
  // every child page stays reachable.
  var subs = document.querySelectorAll('[data-nav-sub]');
  if (subs.length) {
    document.documentElement.classList.add('has-js-nav');
    var openSub = null;
    var pinned = null;   // opened by click: hovering away must not close it again
    var closeTimer = null;

    function canHover() {
      return window.matchMedia('(hover: hover)').matches;
    }

    function close(item, moveFocus) {
      if (!item) return;
      var button = item.querySelector('.nav-sub-toggle');
      item.classList.remove('is-open');
      if (button) {
        button.setAttribute('aria-expanded', 'false');
        if (moveFocus) button.focus();
      }
      if (openSub === item) openSub = null;
      if (pinned === item) pinned = null;
    }

    function open(item) {
      if (openSub && openSub !== item) close(openSub);
      var button = item.querySelector('.nav-sub-toggle');
      item.classList.add('is-open');
      if (button) button.setAttribute('aria-expanded', 'true');
      openSub = item;
    }

    Array.prototype.forEach.call(subs, function (item) {
      var button = item.querySelector('.nav-sub-toggle');
      if (!button) return;

      // Clicking PINS the panel open. Without pinning, hover has already opened it by the
      // time the click lands, so a plain toggle would read the panel as open and shut it
      // again — the menu would flicker closed under the cursor.
      button.addEventListener('click', function () {
        if (pinned === item) { close(item); return; }
        open(item);
        pinned = item;
      });

      // Pointer users get hover, with a short delay on leaving so the cursor can travel
      // from the trigger down into the panel without it snapping shut.
      item.addEventListener('mouseenter', function () {
        if (!canHover()) return;
        window.clearTimeout(closeTimer);
        open(item);
      });
      item.addEventListener('mouseleave', function () {
        if (!canHover() || pinned === item) return;
        closeTimer = window.setTimeout(function () { close(item); }, 220);
      });

      // Leaving the group by keyboard closes it; Escape closes it and returns focus.
      item.addEventListener('focusout', function (event) {
        if (!item.contains(event.relatedTarget)) close(item);
      });
      item.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && item.classList.contains('is-open')) {
          event.stopPropagation();
          close(item, true);
        }
      });
    });

    document.addEventListener('click', function (event) {
      if (openSub && !openSub.contains(event.target)) close(openSub);
    });
  }

  var key = 'tls-wireframe-notes';
  var button = document.querySelector('.wf-toggle');
  function setNotes(on) {
    document.body.classList.toggle('show-notes', on);
    if (button) {
      button.setAttribute('aria-pressed', String(on));
      button.textContent = on ? 'Hide wireframe notes' : 'Show wireframe notes';
    }
    try { localStorage.setItem(key, on ? '1' : '0'); } catch (e) {}
  }
  var saved = false;
  try { saved = localStorage.getItem(key) === '1'; } catch (e) {}
  setNotes(saved);
  if (button) {
    button.addEventListener('click', function () {
      setNotes(!document.body.classList.contains('show-notes'));
    });
  }
})();

// Call-to-action tracking.
// Sends GA4 events when a Measurement ID is configured, and always pushes to dataLayer so
// Google Tag Manager can read the same events. Harmless when neither is installed.
(function () {
  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params);
    window.dataLayer = window.dataLayer || [];
    var payload = { event: name };
    for (var key in params) if (Object.prototype.hasOwnProperty.call(params, key)) payload[key] = params[key];
    window.dataLayer.push(payload);
  }
  window.tlsTrack = track;

  document.addEventListener('click', function (event) {
    var el = event.target.closest ? event.target.closest('[data-cta]') : null;
    if (!el) return;
    var href = el.getAttribute('href') || '';
    var kind = href.indexOf('tel:') === 0 ? 'call' : href.indexOf('mailto:') === 0 ? 'email' : 'navigate';
    track('cta_click', {
      cta_id: el.getAttribute('data-cta'),
      cta_page: el.getAttribute('data-cta-page') || '',
      cta_type: kind,
      link_url: href,
      link_text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 100)
    });
  }, true);
})();

// Screening + contact forms.
// Each dropdown answer can reveal guidance and a follow-up box; the answers that make a
// matter ineligible show the "we cannot assist" notice. Submitting opens the visitor's email
// app addressed to the site's address — WordPress replaces this with a real form handler.
(function () {
  var forms = document.querySelectorAll('.intake-form, .mailto-form');
  if (!forms.length) return;

  function labelText(el) {
    var lab = el.id ? document.querySelector('label[for="' + el.id.replace(/"/g, '\\"') + '"]') : null;
    if (!lab) lab = el.closest('label');
    return lab ? lab.textContent.replace(/\s+/g, ' ').trim() : el.name;
  }

  function setUpQuestion(select) {
    var question = select.closest('.q');
    var note = question.querySelector('.q-note');
    var detail = question.querySelector('.q-detail');
    var box = detail ? detail.querySelector('textarea') : null;
    var label = detail ? detail.querySelector('label') : null;

    select.addEventListener('change', function () {
      var opt = select.options[select.selectedIndex];
      var data = opt ? opt.dataset : {};

      if (note) {
        note.textContent = data.note || '';
        note.hidden = !data.note;
      }
      if (detail && box && label) {
        if (data.detail) {
          label.textContent = data.detail;
          detail.hidden = false;
          box.required = data.required === '1';
        } else {
          detail.hidden = true;
          box.required = false;
          box.value = '';
        }
      }
      question.classList.toggle('is-stop', data.stop === '1');
      updateStopState(select.form);
    });
  }

  function updateStopState(form) {
    var banner = form.querySelector('.stop-banner');
    if (!banner) return;
    var blocked = !!form.querySelector('.q.is-stop');
    var changed = banner.hidden === blocked;
    banner.hidden = !blocked;
    if (blocked && changed && window.tlsTrack) {
      window.tlsTrack('screening_ineligible', {
        form_id: 'screening',
        question: (form.querySelector('.q.is-stop h3') || {}).textContent || ''
      });
    }
  }

  function collect(form) {
    var lines = [];
    var lastGroup = null;
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.type === 'submit' || el.disabled) return;
      var hiddenWrap = el.closest('.q-detail');
      if (hiddenWrap && hiddenWrap.hidden) return;

      var group = el.closest('fieldset');
      var legend = group ? group.querySelector('legend') : null;
      var groupName = legend ? legend.textContent.replace(/\s+/g, ' ').trim() : null;
      if (groupName && groupName !== lastGroup) {
        lines.push('', groupName.toUpperCase());
        lastGroup = groupName;
      }

      if (el.type === 'checkbox') {
        lines.push('Confirmed: ' + (el.checked ? 'Yes' : 'No'));
        return;
      }
      var value = (el.value || '').trim();
      if (!value || value === 'Select a role') return;

      var question = el.closest('.q');
      if (question && el.tagName === 'SELECT') {
        var heading = question.querySelector('h3');
        lines.push('', question.dataset.q + '. ' + heading.textContent.replace(/\s+/g, ' ').trim(),
                   'Answer: ' + value);
      } else if (question) {
        lines.push(labelText(el) + ': ' + value);
      } else {
        lines.push(labelText(el).replace(/\s*\(optional\)$/i, '') + ': ' + value);
      }
    });
    return lines.join('\r\n').replace(/^\s+/, '');
  }

  function firstInvalid(form) {
    return Array.prototype.filter.call(form.elements, function (el) {
      if (!el.name || el.disabled) return false;
      var wrap = el.closest('.q-detail');
      if (wrap && wrap.hidden) return false;
      if (el.type === 'checkbox') return el.required && !el.checked;
      if (!el.required) return false;
      if (!el.value.trim()) return true;
      return el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim());
    })[0];
  }

  Array.prototype.forEach.call(forms, function (form) {
    Array.prototype.forEach.call(form.querySelectorAll('.q select'), setUpQuestion);
    var error = form.querySelector('.form-error');

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var bad = firstInvalid(form);
      if (bad) {
        if (error) {
          error.textContent = 'Please complete "' + labelText(bad).replace(/\s*\(optional\)$/i, '') +
                              '" before sending.';
          error.hidden = false;
        }
        bad.focus();
        if (bad.scrollIntoView) bad.scrollIntoView({ block: 'center' });
        return;
      }
      if (error) error.hidden = true;

      var formId = form.classList.contains('intake-form') ? 'screening' : 'contact';
      if (window.tlsTrack) {
        // generate_lead is a GA4 recommended event, so it can be marked as a conversion.
        window.tlsTrack('generate_lead', { form_id: formId, method: 'email' });
        window.tlsTrack('form_submit', { form_id: formId });
      }

      var body = collect(form);
      try { if (navigator.clipboard) navigator.clipboard.writeText(body); } catch (e) {}

      // Keep the mailto short enough for email clients; the clipboard copy holds the full text.
      var trimmed = body.length > 1500
        ? body.slice(0, 1500) + '\r\n\r\n[Truncated for email. The full response is on your clipboard — paste it here.]'
        : body;
      window.location.href = 'mailto:' + form.dataset.email +
        '?subject=' + encodeURIComponent(form.dataset.subject || 'Website enquiry') +
        '&body=' + encodeURIComponent(trimmed);
    });
  });
})();
