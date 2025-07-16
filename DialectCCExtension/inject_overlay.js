(function () {
  const overlay = document.createElement("iframe");
  overlay.src = "https://soft-panda-hides.trycloudflare.com/overlay";  // Replace with new tunnel URL
  overlay.id = "dialect-cc-overlay";
  overlay.style = `
    position: fixed;
    bottom: 5%;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 120px;
    border: none;
    z-index: 999999;
    background: transparent;
    pointer-events: none;
  `;
  document.body.appendChild(overlay);
})();
