/**
 * il-cred-capture.js — secure-entry page logic for /account/credentials/.
 * The ONLY place a user types a service password into this platform:
 * a dedicated protected page, form posts straight to the session-gated
 * broker API over HTTPS. The value is never rendered back, never put
 * in a URL, never stored client-side. Mirrors the Proton Pass pattern:
 * the store holds it; agents see names and states only.
 */
(function () {
  'use strict';

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  var svcSel = $('cred-service'), customWrap = $('cred-custom-wrap'), customInp = $('cred-custom');
  var userInp = $('cred-username'), passInp = $('cred-secret');
  var form = $('cred-form'), msg = $('cred-msg'), stateLine = $('cred-state');
  var extBtn = $('cred-external');

  var qs = new URLSearchParams(window.location.search);
  var wanted = (qs.get('service') || '').toLowerCase();

  function currentService() {
    if (svcSel.value === '__custom') return (customInp.value || '').trim().toLowerCase();
    return svcSel.value;
  }

  function fillDirectory() {
    if (!window.ILCredBroker) return;
    var html = '';
    window.ILCredBroker.DIRECTORY.forEach(function (d) {
      html += '<option value="' + d.id + '"' + (d.id === wanted ? ' selected' : '') + '>' +
        esc(d.label) + '</option>';
    });
    html += '<option value="__custom"' + (wanted && !window.ILCredBroker.DIRECTORY.some(function (d) { return d.id === wanted; }) ? ' selected' : '') +
      '>Other service…</option>';
    svcSel.innerHTML = html;
    if (svcSel.value === '__custom') {
      customWrap.style.display = 'block';
      if (wanted) customInp.value = wanted;
    }
    refreshState();
  }

  function refreshState() {
    if (!window.ILCredBroker) return;
    var svc = currentService();
    if (!svc) { stateLine.textContent = ''; return; }
    window.ILCredBroker.status().then(function (st) {
      if (!st.live) { stateLine.textContent = ''; return; }
      if (!st.signedIn) { stateLine.textContent = 'You are signed out — saving needs your account.'; return; }
      var rec = null;
      st.services.forEach(function (s) { if (s.id === svc) rec = s; });
      stateLine.textContent = !rec || rec.state === 'not_saved'
        ? 'No login saved for this service yet.'
        : rec.state === 'saved'
          ? 'A login is already saved in the secure store — saving again replaces it.'
          : 'Marked as kept in Proton Pass — saving here adds an encrypted copy.';
    });
  }

  svcSel.addEventListener('change', function () {
    customWrap.style.display = svcSel.value === '__custom' ? 'block' : 'none';
    refreshState();
  });
  customInp.addEventListener('input', refreshState);

  extBtn.addEventListener('click', function () {
    var svc = currentService();
    if (!svc || !window.ILCredBroker) return;
    extBtn.disabled = true;
    window.ILCredBroker.markExternal(svc).then(function (d) {
      extBtn.disabled = false;
      if (d && d.ok) {
        msg.className = 'il-auth-hint';
        msg.textContent = 'Marked — this login stays in your Proton Pass, and Noah / Genesis will ' +
          'point you to the vault when a task needs it.';
        window.ILCredBroker.invalidate(); refreshState();
      } else {
        msg.className = 'il-auth-error';
        msg.textContent = 'Could not mark it — sign in first, then try again.';
      }
    }).catch(function () {
      extBtn.disabled = false;
      msg.className = 'il-auth-error';
      msg.textContent = 'Could not mark it just now. Try again in a moment.';
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var svc = currentService();
    msg.textContent = '';
    if (!/^[a-z0-9][a-z0-9-]{1,60}$/.test(svc)) {
      msg.className = 'il-auth-error';
      msg.textContent = 'Pick a service, or type a short service name (letters, numbers, dashes).';
      return;
    }
    if (!userInp.value.trim() || !passInp.value) {
      msg.className = 'il-auth-error';
      msg.textContent = 'Enter both the username and the password for this login.';
      return;
    }
    var btn = $('cred-save');
    btn.disabled = true; btn.textContent = 'Saving securely…';
    fetch('/api/credentials/capture', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ service: svc, username: userInp.value.trim(), secret: passInp.value })
    }).then(function (r) {
      return r.json().then(function (d) { return { status: r.status, d: d }; });
    }).then(function (res) {
      btn.disabled = false; btn.textContent = 'Save to the secure store';
      passInp.value = '';
      if (res.status === 401) {
        msg.className = 'il-auth-error';
        msg.innerHTML = 'You are signed out. <a href="/account/">Sign in</a> first, then save this login.';
        return;
      }
      if (res.d && res.d.error === 'cred_store_not_configured') {
        msg.className = 'il-auth-error';
        msg.textContent = 'The secure store is not switched on yet — the site owner still needs to ' +
          'set its encryption key. For now, keep this login in Proton Pass and use the button below.';
        return;
      }
      if (!res.d || !res.d.ok) {
        msg.className = 'il-auth-error';
        msg.textContent = 'Saving failed (' + ((res.d && res.d.error) || 'unknown') + '). Nothing was stored.';
        return;
      }
      msg.className = 'il-auth-hint';
      msg.innerHTML = '✓ Saved securely. Noah and Genesis can now use this login through the ' +
        'secure store — they see that it exists, never the password itself. ' +
        'Manage it any time in <a href="/noah/#settings">Noah Settings → Saved logins</a>.';
      if (window.ILCredBroker) window.ILCredBroker.invalidate();
      refreshState();
    }).catch(function () {
      btn.disabled = false; btn.textContent = 'Save to the secure store';
      msg.className = 'il-auth-error';
      msg.textContent = 'Network trouble — nothing was stored. Try again.';
    });
  });

  fillDirectory();
})();
