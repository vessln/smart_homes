const API_BASE_URL = "http://localhost:8000";

// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.getElementById('nav-menu');
if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', !expanded);
    navMenu.classList.toggle('open');
  });
  navToggle.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      navToggle.click();
    }
  });
}

// Testimonials carousel logic
function initTestimonialsCarousel() {
  const carousel = document.querySelector('.testimonials-carousel');
  if (!carousel) return;
  const list = carousel.querySelector('.carousel-list');
  const items = Array.from(list.querySelectorAll('.carousel-item'));
  const prevBtn = carousel.querySelector('.carousel-btn.prev');
  const nextBtn = carousel.querySelector('.carousel-btn.next');
  let current = 0;

  function updateCarousel() {
    items.forEach((item, i) => {
      item.classList.toggle('active', i === current);
    });
    list.style.transform = `translateX(-${current * 100}%)`;
    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === items.length - 1;
    // Focus management for accessibility
    items.forEach((item, i) => {
      item.setAttribute('tabindex', i === current ? '0' : '-1');
    });
    if (document.activeElement.classList.contains('carousel-item')) {
      items[current].focus();
    }
  }

  prevBtn.addEventListener('click', () => {
    if (current > 0) {
      current--;
      updateCarousel();
    }
  });
  nextBtn.addEventListener('click', () => {
    if (current < items.length - 1) {
      current++;
      updateCarousel();
    }
  });
  // Keyboard navigation
  carousel.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
      prevBtn.click();
    } else if (e.key === 'ArrowRight') {
      nextBtn.click();
    }
  });
  // Initial state
  updateCarousel();
}

// Contact form validation and simulated submit
function initContactForm() {
  const form = document.querySelector('form.contact-form');
  if (!form) return;
  const name = form.querySelector('input[name="name"]');
  const email = form.querySelector('input[name="email"]');
  const phone = form.querySelector('input[name="phone"]');
  const message = form.querySelector('textarea[name="message"]');
  const status = form.querySelector('.form-status');

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    let valid = true;
    // Reset errors
    form.querySelectorAll('.error').forEach(el => el.textContent = '');
    if (!name.value.trim()) {
      showError(name, 'Name is required');
      valid = false;
    }
    if (!email.value.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)) {
      showError(email, 'Valid email required');
      valid = false;
    }
    if (message.value.trim().length < 10) {
      showError(message, 'Message must be at least 10 characters');
      valid = false;
    }
    if (!valid) return;
    // Simulate submit
    form.classList.add('submitting');
    status.setAttribute('aria-live', 'polite');
    status.textContent = 'Sending...';
    setTimeout(() => {
      form.classList.remove('submitting');
      status.textContent = 'Thank you! We will contact you soon.';
      form.reset();
    }, 1200);
    /*
    async function postContact(data){ 
      const res = await fetch(`${API_BASE_URL}/api/contact/`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
      const json = await res.json(); 
      // handle json
    }
    */
  });
  function showError(input, msg) {
    let err = input.parentElement.querySelector('.error');
    if (!err) {
      err = document.createElement('div');
      err.className = 'error';
      input.parentElement.appendChild(err);
    }
    err.textContent = msg;
  }
}

// Accordion logic for solutions page
function initAccordions() {
  const headers = Array.from(document.querySelectorAll('.accordion__header'));
  if (!headers.length) return;
  headers.forEach((header, idx) => {
    const panelId = header.getAttribute('aria-controls');
    const panel = document.getElementById(panelId);
    header.addEventListener('click', () => toggleAccordion(header, panel));
    header.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleAccordion(header, panel);
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        headers[(idx + 1) % headers.length].focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        headers[(idx - 1 + headers.length) % headers.length].focus();
      }
    });
  });
  function toggleAccordion(header, panel) {
    const expanded = header.getAttribute('aria-expanded') === 'true';
    header.setAttribute('aria-expanded', !expanded);
    if (!expanded) {
      panel.hidden = false;
      panel.classList.add('open');
    } else {
      panel.hidden = true;
      panel.classList.remove('open');
    }
  }
}

// Profile dropdown logic
function initProfileDropdown() {
  const btn = document.querySelector('.profile-btn');
  const menu = document.getElementById('profile-menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', !expanded);
    menu.hidden = expanded;
    if (!expanded) menu.querySelector('a').focus();
  });
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      btn.click();
    }
  });
  menu.addEventListener('keydown', (e) => {
    const links = Array.from(menu.querySelectorAll('a'));
    let idx = links.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      links[(idx + 1) % links.length].focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      links[(idx - 1 + links.length) % links.length].focus();
    } else if (e.key === 'Escape') {
      btn.setAttribute('aria-expanded', 'false');
      menu.hidden = true;
      btn.focus();
    }
  });
  document.addEventListener('click', (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      btn.setAttribute('aria-expanded', 'false');
      menu.hidden = true;
    }
  });
}

// Profile dropdown delayed close logic
function initProfileDropdownDelay() {
  const dropdown = document.querySelector('.nav-profile-dropdown');
  const menu = dropdown && dropdown.querySelector('.profile-dropdown-menu');
  let hideTimeout;
  if (!dropdown || !menu) return;
  function showMenu() {
    clearTimeout(hideTimeout);
    menu.classList.add('show');
  }
  function hideMenu() {
    hideTimeout = setTimeout(() => menu.classList.remove('show'), 200);
  }
  dropdown.addEventListener('mouseenter', showMenu);
  dropdown.addEventListener('mouseleave', hideMenu);
  dropdown.addEventListener('focusin', showMenu);
  dropdown.addEventListener('focusout', hideMenu);
  // Prevent menu from closing if mouse moves between button and menu
  menu.addEventListener('mouseenter', showMenu);
  menu.addEventListener('mouseleave', hideMenu);
}

document.addEventListener('DOMContentLoaded', () => {
  initContactForm();
  // If carousel exists, initialize
  if (document.querySelector('.testimonials-carousel')) {
    initTestimonialsCarousel();
  }
  // If accordions exist, initialize
  if (document.querySelector('.accordion__header')) {
    initAccordions();
  }
  if (document.querySelector('.profile-btn')) {
    initProfileDropdown();
  }
  if (document.querySelector('.nav-profile-dropdown')) {
    initProfileDropdownDelay();
  }
});
