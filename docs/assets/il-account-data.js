/* Interstitium Labs — account data rights (2026-10-11).
 * Wires the /account/ "Your data" section: full server-side export is a
 * plain authenticated GET (/api/account/export); deletion posts the
 * confirm-gated /api/account/delete and reports the returned manifest. */
(function () {
  var exportBtn = document.getElementById('il-export-btn');
  var deleteToggle = document.getElementById('il-delete-toggle');
  var deleteForm = document.getElementById('il-delete-form');
  var deleteBtn = document.getElementById('il-delete-btn');
  var emailInput = document.getElementById('il-delete-email');
  var status = document.getElementById('il-data-status');
  if (!exportBtn || !deleteToggle || !status) return;

  function setStatus(t, isErr) {
    status.textContent = t || '';
    status.style.color = isErr ? '#fca5a5' : '';
  }

  fetch('/api/me', { credentials: 'same-origin' })
    .then(function (r) {
      if (!r.ok) {
        exportBtn.removeAttribute('href');
        exportBtn.style.opacity = '.5';
        exportBtn.setAttribute('aria-disabled', 'true');
        deleteToggle.disabled = true;
        setStatus('Sign in above to export or delete your account data.');
      }
    })
    .catch(function () { /* leave buttons as-is; the API will 401 honestly */ });

  deleteToggle.addEventListener('click', function () {
    var open = deleteForm.style.display !== 'none';
    deleteForm.style.display = open ? 'none' : 'block';
    if (!open && emailInput) emailInput.focus();
  });

  deleteBtn.addEventListener('click', function () {
    var email = (emailInput.value || '').trim();
    if (!email) {
      setStatus('Enter your account email to confirm deletion.', true);
      return;
    }
    deleteBtn.disabled = true;
    setStatus('Deleting…');
    fetch('/api/account/delete', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ confirm: 'DELETE', email: email })
    })
      .then(function (r) {
        return r.json().then(function (j) { return { ok: r.ok, j: j }; });
      })
      .then(function (res) {
        if (res.ok && res.j && res.j.ok) {
          var d = res.j.deleted || {};
          setStatus(
            'Account deleted. Removed — account: ' + (d.account || 0) +
            ', progress: ' + (d.progress || 0) +
            ', synced stores: ' + (d.sync_stores || 0) +
            ', goals: ' + (d.goals || 0) +
            ', certificates: ' + (d.certificates || 0) +
            ', sessions: ' + (d.sessions || 0) +
            '. Orders anonymized: ' + (res.j.orders_anonymized || 0) +
            '. Taking you home…'
          );
          setTimeout(function () { window.location.href = '/'; }, 4000);
        } else {
          deleteBtn.disabled = false;
          setStatus(
            'Deletion failed: ' + ((res.j && res.j.error) || 'unknown error') +
            '. The email must match your signed-in account.',
            true
          );
        }
      })
      .catch(function () {
        deleteBtn.disabled = false;
        setStatus('Deletion failed: network error.', true);
      });
  });
})();
