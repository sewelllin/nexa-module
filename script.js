const revealTargets = document.querySelectorAll(
  ".section-heading, .value-grid article, .feature, .security-grid div, .timeline article, .use-list p, .terminal"
);

revealTargets.forEach((target) => target.classList.add("reveal"));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 }
);

revealTargets.forEach((target) => observer.observe(target));
