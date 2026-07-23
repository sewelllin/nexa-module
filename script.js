const q = (selector, root = document) => root.querySelector(selector);
const qa = (selector, root = document) => [...root.querySelectorAll(selector)];

const observer = new IntersectionObserver(
  (entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    }
  }),
  { threshold: 0.12 }
);

qa(".section,.cards article,.topo-server,.topo-device,.film-frame").forEach((el) => {
  el.classList.add("reveal");
  observer.observe(el);
});

const input = q("#prompt");
const run = q("#run");
const source = q("#source");
const steps = qa(".trace-step");
const suggestions = qa("[data-scenario]");
let timers = [];
let activeScenario = "fan";

const scenarios = {
  fan: {
    source: "远程应用服务器",
    match: ["风机", "打开"],
    titles: ["接收远程自然语言", "模组理解远程任务", "端侧策略校验", "执行 fan.control"],
    lines: [
      "source: remote_app · skills: fan.control, timer.schedule",
      "intent: fan.timed_run · confidence: 0.98",
      "policy: allow · risk: low · duration: 900s",
      "fan #2: ON · timer: auto-off in 900s"
    ]
  },
  serial: {
    source: "UART 串口",
    match: ["GPIO", "拉高"],
    titles: ["接收串口文本输入", "模组理解串口任务", "端侧策略校验", "执行 gpio.write"],
    lines: [
      "source: uart0 · skills: gpio.write, timer.schedule",
      "intent: gpio.pulse_high · confidence: 0.96",
      "policy: allow · pin: 12 · duration: 10s",
      "GPIO 12: HIGH · scheduled restore LOW"
    ]
  },
  voice: {
    source: "语音转文字",
    match: ["温度", "喷淋"],
    titles: ["接收语音转写输入", "模组理解语音任务", "端侧策略校验", "注册自动化规则"],
    lines: [
      "source: speech_text · skills: sensor.rule, irrigation.control",
      "intent: automation.create · confidence: 0.96",
      "policy: allow · threshold: 30°C · action verified",
      "rule #12: temp > 30°C → irrigation ON"
    ]
  }
};

function inferScenario(value) {
  if (value.includes("GPIO") || value.includes("拉高") || value.includes("串口")) return "serial";
  if (value.includes("温度") || value.includes("喷淋") || value.includes("语音")) return "voice";
  return "fan";
}

function animateTrace(key = inferScenario(input.value)) {
  activeScenario = key;
  const config = scenarios[key];
  timers.forEach(clearTimeout);
  timers = [];

  if (source) source.textContent = config.source;
  suggestions.forEach((btn) => btn.classList.toggle("active", btn.dataset.scenario === key));
  steps.forEach((el, index) => {
    el.classList.remove("active", "done");
    q("b", el).textContent = config.titles[index];
    q("small", el).textContent = index ? "等待上一阶段..." : config.lines[0];
  });

  run.disabled = true;
  steps[0].classList.add("active");
  config.lines.forEach((line, index) => {
    timers.push(setTimeout(() => {
      if (index) {
        steps[index - 1].classList.remove("active");
        steps[index - 1].classList.add("done");
      }
      steps[index].classList.add("active");
      q("small", steps[index]).textContent = line;
      if (index === config.lines.length - 1) {
        run.disabled = false;
        setTimeout(() => steps[index].classList.add("done"), 400);
      }
    }, index * 720));
  });
}

run?.addEventListener("click", () => animateTrace());
input?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") animateTrace();
});

suggestions.forEach((btn) => btn.addEventListener("click", () => {
  input.value = btn.dataset.prompt;
  animateTrace(btn.dataset.scenario);
}));

animateTrace(activeScenario);