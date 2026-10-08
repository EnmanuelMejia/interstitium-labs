/* Mount the immersive Noah slot. External so CSP script-src 'self' allows it. */
(function () {
  var slot = document.querySelector("[data-imm-muse]");
  if (!slot) return;
  try {
    if (window.ILNoahAvatar && ILNoahAvatar.mount) {
      var ninst = ILNoahAvatar.mount(slot, {});
      if (ninst && ninst.setStatus) ninst.setStatus("idle");
    } else if (window.ILMuse3D && ILMuse3D.mount) {
      var inst = ILMuse3D.mount(slot, { avatarId: "dee" });
      if (inst && inst.setStatus) inst.setStatus("idle");
    }
  } catch (eMuse) {}
})();
