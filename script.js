const q=(s,r=document)=>r.querySelector(s),qa=(s,r=document)=>[...r.querySelectorAll(s)];
const observer=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("is-visible");observer.unobserve(e.target)}}),{threshold:.12});
qa(".section,.cards article,.arch-node").forEach(el=>{el.classList.add("reveal");observer.observe(el)});
const input=q("#prompt"),run=q("#run"),steps=qa(".trace-step");
const output=["skills: fan.control, timer.schedule","intent: fan.timed_run · confidence: 0.98","policy: allow · risk: low","fan #2: ON · auto-off: 900s"];let timers=[];
function animateTrace(){timers.forEach(clearTimeout);timers=[];steps.forEach((el,i)=>{el.classList.remove("active","done");q("small",el).textContent=i?"等待上一步...":output[0]});run.disabled=true;steps[0].classList.add("active");output.forEach((text,i)=>timers.push(setTimeout(()=>{if(i){steps[i-1].classList.remove("active");steps[i-1].classList.add("done")}steps[i].classList.add("active");q("small",steps[i]).textContent=text;if(i===output.length-1){run.disabled=false;setTimeout(()=>steps[i].classList.add("done"),400)}},i*650)))}
run?.addEventListener("click",animateTrace);input?.addEventListener("keydown",e=>{if(e.key==="Enter")animateTrace()});qa("[data-prompt]").forEach(btn=>btn.addEventListener("click",()=>{input.value=btn.dataset.prompt;animateTrace()}));animateTrace();
