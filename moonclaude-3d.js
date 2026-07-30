  /* ---------------- Main animation loop ---------------- */
  function frame(nowMs){
    if(state.lastFrameMs == null) state.lastFrameMs = nowMs;
    const dtMs = nowMs - state.lastFrameMs;
    state.lastFrameMs = nowMs;

    if(state.playing){
      const mult = SPEED_STEPS[state.speedIndex].mult;
      state.simTime = new Date(state.simTime.getTime() + dtMs*mult);
      // Recompute astronomy at most ~10x/sec to stay smooth at high playback speeds;
      // the 3D render itself still runs every frame via Scene3D.render().
      if(nowMs - state.lastComputeMs > 100){
        state.lastComputeMs = nowMs;
        recomputeAndRender();
      }
    }

    Scene3D.render();
    requestAnimationFrame(frame);
  }

  function wireResize(){
    window.addEventListener('resize', ()=>{
      Scene3D.handleResize();
      el.compassBezelWidth = document.getElementById('compassBezel').clientWidth;
      syncFacingSliderFromCamera();
    });
    window.addEventListener('orientationchange', ()=> setTimeout(()=>Scene3D.handleResize(),200));
  }

  /* ---------------- Self-tests (see checklist in the project brief) ---------------- */
  function runSelfTests(){
    const results = [];
    const test = (name, fn)=>{
      try{ const ok = fn(); results.push([name, !!ok]); }
      catch(e){ results.push([name, false]); console.error(`[self-test] ${name} threw:`, e); }
    };
    test('Astronomy Engine loaded', ()=> !!window.Astronomy);
    test('Astronomy module ready', ()=> Astro.ready);
    test('Three.js loaded', ()=> !!window.THREE);
    test('OrbitControls available', ()=> !!(window.THREE && THREE.OrbitControls));
    test('Scene renderer created', ()=> !!Scene3D.camera);
    test('Sun/Moon compute for "now"', ()=>{
      const a = Astro.compute(new Date());
      return isFinite(a.sun.azimuth) && isFinite(a.moon.altitude) && a.phase.illuminatedFraction>=0;
    });
    test('Culmination search works', ()=>{
      const a = Astro.compute(new Date());
      return a.sunEvents.culm !== undefined; // may legitimately be null in edge cases, but must not throw
    });
    console.table ? console.table(results.map(([n,ok])=>({ test:n, passed:ok }))) : console.log(results);
    const failed = results.filter(r=>!r[1]);
    if(failed.length){
      showError(`${failed.length} self-test(s) failed — see console. The app may still be partly usable.`);
    }
    return failed.length === 0;
  }

  /* ---------------- Bootstrap ---------------- */
  function init(){
    cacheEls();
    el.compassBezelWidth = document.getElementById('compassBezel').clientWidth;

    if(!Astro.init()){
      showError('Astronomy Engine failed to load — check your internet connection and reload. Sun/Moon positions cannot be calculated.');
    }

    try{
      Scene3D.init(document.getElementById('scene-canvas'));
    }catch(e){
      showError('The 3D scene failed to initialise (WebGL may be unavailable in this browser).');
      console.error(e);
    }

    buildCompassStrip();
    wireTimeControls();
    wireViewControls();
    wireKeyboard();
    wirePanelToggles();
    wireResize();

    el.dateTimeInput.value = formatForDateTimeInput(state.simTime, state.useLondon);
    recomputeAndRender();
    syncFacingSliderFromCamera();

    const allPassed = runSelfTests();
    console.log(allPassed ? '%cTrafalgar Sky: all self-tests passed.' : '%cTrafalgar Sky: some self-tests failed — see table above.',
      `color:${allPassed?'#5a9c90':'#e0765f'};font-weight:bold;`);

    requestAnimationFrame(frame);

    const loadingEl = document.getElementById('viewportLoading');
    setTimeout(()=> loadingEl.classList.add('hidden'), 350);
  }

const App = { init };

window.addEventListener('DOMContentLoaded', ()=>{
  try{
    App.init();
  }catch(e){
    console.error('Fatal error starting Trafalgar Sky:', e);
    const banner = document.getElementById('errorBanner');
    if(banner){ banner.textContent = 'A fatal error occurred while starting the app. See the browser console for details.'; banner.style.display='block'; }
    const loadingEl = document.getElementById('viewportLoading');
    if(loadingEl) loadingEl.classList.add('hidden');
  }
});
