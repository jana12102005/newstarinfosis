// NewStar Infosis – Main JS

document.addEventListener('DOMContentLoaded', () => {

  // ── AOS Init ──────────────────────────────────────
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 800, easing: 'ease-out-cubic', once: true, offset: 60 });
  }

  // ── Navbar Scroll ─────────────────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 60);
    });
  }

  // ── Mobile Toggle ─────────────────────────────────
  const toggle = document.getElementById('navToggle');
  const links  = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
      const bars = toggle.querySelectorAll('span');
      bars[0].style.transform = links.classList.contains('open') ? 'rotate(45deg) translate(5px,5px)' : '';
      bars[1].style.opacity   = links.classList.contains('open') ? '0' : '1';
      bars[2].style.transform = links.classList.contains('open') ? 'rotate(-45deg) translate(5px,-5px)' : '';
    });
    // Close on link click
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      links.classList.remove('open');
    }));
  }

  // ── Smooth Scroll ─────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href').slice(1);
      const el = document.getElementById(id);
      if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

  // ── Counter Animation ─────────────────────────────
  const counters = document.querySelectorAll('.stat-number[data-target]');
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el     = entry.target;
        const target = parseInt(el.dataset.target);
        const suffix = el.dataset.suffix || '';
        let current  = 0;
        const step   = Math.ceil(target / 60);
        const timer  = setInterval(() => {
          current = Math.min(current + step, target);
          el.textContent = current + suffix;
          if (current >= target) clearInterval(timer);
        }, 25);
        countObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => countObserver.observe(c));

  // ── OTP Input Auto-focus ──────────────────────────
  const otpInputs = document.querySelectorAll('.otp-inputs input');
  if (otpInputs.length) {
    otpInputs.forEach((input, idx) => {
      input.addEventListener('input', () => {
        if (input.value.length === 1 && idx < otpInputs.length - 1) {
          otpInputs[idx + 1].focus();
        }
        // Auto-submit if all filled
        if ([...otpInputs].every(i => i.value.length === 1)) {
          const hidden = document.getElementById('otpFull');
          if (hidden) hidden.value = [...otpInputs].map(i => i.value).join('');
        }
      });
      input.addEventListener('keydown', e => {
        if (e.key === 'Backspace' && !input.value && idx > 0) {
          otpInputs[idx - 1].focus();
        }
      });
    });
  }

  // ── Flash auto-dismiss ────────────────────────────
  setTimeout(() => {
    document.querySelectorAll('.flash').forEach(f => {
      f.style.transition = 'opacity 0.5s, transform 0.5s';
      f.style.opacity = '0'; f.style.transform = 'translateX(40px)';
      setTimeout(() => f.remove(), 500);
    });
  }, 5000);

  // ── Particle dots (hero bg) ───────────────────────
  const canvas = document.getElementById('heroCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    const dots = Array.from({ length: 60 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.5 + 0.5,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
    }));
    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      dots.forEach(d => {
        d.x += d.vx; d.y += d.vy;
        if (d.x < 0 || d.x > canvas.width)  d.vx *= -1;
        if (d.y < 0 || d.y > canvas.height) d.vy *= -1;
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(212,175,55,0.4)';
        ctx.fill();
      });
      requestAnimationFrame(draw);
    }
    draw();
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    });
  }

  // ── Sidebar active ────────────────────────────────
  const sideLinks = document.querySelectorAll('.sidebar-nav a');
  sideLinks.forEach(a => {
    if (a.href === window.location.href) a.classList.add('active');
  });

});
