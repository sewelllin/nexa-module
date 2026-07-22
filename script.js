const q=(s,r=document)=>r.querySelector(s),qa=(s,r=document)=>[...r.querySelectorAll(s)];
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("is-visible");observer.unobserve(entry.target)}}),{threshold:.12});
qa(".section,.cards article,.arch-node").forEach(el=>{el.classList.add("reveal");observer.observe(el)});
const input=q("#prompt"),run=q("#run"),steps=qa(".trace-step"),suggestions=qa("[data-scenario]");
const scenarios={
 fan:{match:["风机","打开"],titles:["设备构建上下文","意图服务器匹配","端侧策略校验","执行 fan.control"],lines:["skills: fan.control, timer.schedule","intent: fan.timed_run · confidence: 0.98","policy: allow · risk: low","fan #2: ON · timer: auto-off in 900s"]},
 rule:{match:["温度","喷淋"],titles:["设备构建上下文","意图服务器匹配","端侧策略校验","注册联动规则"],lines:["skills: sensor.rule, irrigation.control","intent: automation.create · confidence: 0.96","policy: allow · condition validated","rule #12: temp > 30°C → irrigation ON"]},
 collect:{match:["传感器","结果"],titles:["设备构建上下文","意图服务器匹配","端侧策略校验","采集并上报数据"],lines:["skills: sensor.read, tcp.publish","intent: sensor.collect_report · confidence: 0.99","policy: allow · destination trusted","temp: 26.4°C · humidity: 61% · server ACK"]}
};
let timers=[],activeScenario="fan";
function inferScenario(value){if(value.includes("温度")||value.includes("喷淋")||value.includes("联动"))return"rule";if(value.includes("传感器")||value.includes("采集")||value.includes("上报")||value.includes("结果"))return"collect";return"fan"}
function animateTrace(key=inferScenario(input.value)){activeScenario=key;const config=scenarios[key];timers.forEach(clearTimeout);timers=[];suggestions.forEach(btn=>btn.classList.toggle("active",btn.dataset.scenario===key));steps.forEach((el,i)=>{el.classList.remove("active","done");q("b",el).textContent=config.titles[i];q("small",el).textContent=i?"等待上一步...":config.lines[0]});run.disabled=true;steps[0].classList.add("active");config.lines.forEach((line,i)=>timers.push(setTimeout(()=>{if(i){steps[i-1].classList.remove("active");steps[i-1].classList.add("done")}steps[i].classList.add("active");q("small",steps[i]).textContent=line;if(i===config.lines.length-1){run.disabled=false;setTimeout(()=>steps[i].classList.add("done"),400)}},i*700)))}
run?.addEventListener("click",()=>animateTrace());input?.addEventListener("keydown",e=>{if(e.key==="Enter")animateTrace()});
suggestions.forEach(btn=>btn.addEventListener("click",()=>{input.value=btn.dataset.prompt;animateTrace(btn.dataset.scenario)}));
animateTrace(activeScenario);
