// Navbar scroll effect
(function () {
  const nav = document.getElementById('mainNav');
  if (!nav) return;
  const toggle = () => nav.classList.toggle('scrolled', window.scrollY > 40);
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();
})();

// Auto-dismiss alerts after 5s
document.querySelectorAll('.alert').forEach(function (el) {
  setTimeout(function () {
    const bsAlert = new bootstrap.Alert(el);
    bsAlert.close();
  }, 5000);
});

// Booking form: live total price preview
(function () {
  const checkIn = document.querySelector('[name="check_in_date"]');
  const checkOut = document.querySelector('[name="check_out_date"]');
  const priceEl = document.querySelector('.price-amount-lg');

  if (!checkIn || !checkOut || !priceEl) return;

  const rateText = document.querySelector('.booking-summary-card .fw-semibold:last-of-type');

  function updateTotal() {
    const a = new Date(checkIn.value);
    const b = new Date(checkOut.value);
    if (isNaN(a) || isNaN(b) || b <= a) return;
    const nights = Math.round((b - a) / 86400000);
    const rateMatch = document.body.innerHTML.match(/₦([\d,]+)\s*\/\s*night/);
    if (!rateMatch) return;
    const rate = parseFloat(rateMatch[1].replace(',', ''));
    if (!isNaN(rate)) {
      const total = (rate * nights).toLocaleString('en-NG');
      const preview = document.querySelector('#total-preview');
      if (preview) {
        preview.textContent = `₦${total} (${nights} night${nights > 1 ? 's' : ''})`;
      }
    }
  }
  checkIn.addEventListener('change', updateTotal);
  checkOut.addEventListener('change', updateTotal);
})();
