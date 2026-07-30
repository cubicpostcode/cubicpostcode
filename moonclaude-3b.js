  /* ---------------- Time control wiring ---------------- */
  function setSimTime(newDate, opts){
    state.simTime = newDate;
    recomputeAndRender();
  }

  function stepBy(ms){ setSimTime(new Date(state.simTime.getTime()+ms)); }

  function wireTimeControls(){
    el.dateTimeInput.addEventListener('change', ()=>{
      const parsed = parseDateTimeInput(el.dateTimeInput.value, state.useLondon);
      if(parsed) setSimTime(parsed);
    });
    el.btnNow.addEventListener('click', ()=> setSimTime(new Date()));
    el.stepDayBack.addEventListener('click', ()=> stepBy(-86400000));
    el.stepHourBack.addEventListener('click', ()=> stepBy(-3600000));
    el.stepMinBack.addEventListener('click', ()=> stepBy(-60000));
    el.stepMinFwd.addEventListener('click', ()=> stepBy(60000));
    el.stepHourFwd.addEventListener('click', ()=> stepBy(3600000));
    el.stepDayFwd.addEventListener('click', ()=> stepBy(86400000));

    el.btnPlay.addEventListener('click', ()=>{
      state.playing = true; el.btnPlay.disabled = true; el.btnPause.disabled = false;
    });
    el.btnPause.addEventListener('click', ()=>{
      state.playing = false; el.btnPlay.disabled = false; el.btnPause.disabled = true;
    });

    el.speedSlider.addEventListener('input', ()=>{
      state.speedIndex = parseInt(el.speedSlider.value,10);
      el.speedLabel.textContent = SPEED_STEPS[state.speedIndex].label;
    });
    el.speedLabel.textContent = SPEED_STEPS[state.speedIndex].label;

    el.todSlider.addEventListener('pointerdown', ()=>{ todSliderDragging = true; });
    window.addEventListener('pointerup', ()=>{ todSliderDragging = false; });
    el.todSlider.addEventListener('input', ()=>{
      const secs = parseInt(el.todSlider.value,10);
      const hh = Math.floor(secs/3600), mm = Math.floor((secs%3600)/60), ss = secs%60;
      if(state.useLondon){
        const p = londonParts(state.simTime);
        setSimTime(londonWallClockToUTC(p.year,p.month,p.day,hh,mm,ss));
      } else {
        const d = state.simTime;
        setSimTime(new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), hh, mm, ss)));
      }
    });

    function setZone(useLondon){
      state.useLondon = useLondon;
      el.btnLondonTime.classList.toggle('active', useLondon);
      el.btnUtcTime.classList.toggle('active', !useLondon);
      el.btnLondonTime.setAttribute('aria-pressed', String(useLondon));
      el.btnUtcTime.setAttribute('aria-pressed', String(!useLondon));
      el.dtInputZoneLabel.textContent = useLondon ? 'London civil time' : 'UTC';
      el.dateTimeInput.value = formatForDateTimeInput(state.simTime, useLondon);
      recomputeAndRender();
    }
    el.btnLondonTime.addEventListener('click', ()=> setZone(true));
    el.btnUtcTime.addEventListener('click', ()=> setZone(false));
  }

  /* ---------------- Camera / view control wiring ---------------- */
  function wireViewControls(){
    el.viewReset.addEventListener('click', ()=> Scene3D.resetView());
    el.viewAerial.addEventListener('click', ()=> Scene3D.aerialView());
    el.viewGround.addEventListener('click', ()=> Scene3D.groundView());
    el.viewCentreSun.addEventListener('click', ()=> Scene3D.centreOnSun());
    el.viewCentreMoon.addEventListener('click', ()=> Scene3D.centreOnMoon());

    el.fovSlider.addEventListener('input', ()=>{
      const v = parseInt(el.fovSlider.value,10);
      el.fovValue.textContent = `${v}°`;
      Scene3D.setFOV(v);
    });

    el.facingSlider.addEventListener('input', ()=>{
      const v = parseInt(el.facingSlider.value,10);
      el.facingValue.textContent = compassDirection(v);
      Scene3D.setCompassFacing(v);
    });

    el.sunSizeSlider.addEventListener('input', ()=>{
      const v = parseFloat(el.sunSizeSlider.value);
      el.sunSizeValue.textContent = `${v.toFixed(1)}×`;
      Scene3D.setSunSize(v);
    });
    el.moonSizeSlider.addEventListener('input', ()=>{
      const v = parseFloat(el.moonSizeSlider.value);
      el.moonSizeValue.textContent = `${v.toFixed(1)}×`;
      Scene3D.setMoonSize(v);
    });

    function setLightMode(mode){
      Scene3D.setLightingMode(mode);
      [['lightAuto','auto'],['lightDay','day'],['lightNight','night']].forEach(([id,m])=>{
        el[id].setAttribute('aria-pressed', String(m===mode));
      });
    }
    el.lightAuto.addEventListener('click', ()=> setLightMode('auto'));
    el.lightDay.addEventListener('click', ()=> setLightMode('day'));
    el.lightNight.addEventListener('click', ()=> setLightMode('night'));

    let worldHidden = false;
    el.btnHideWorld.addEventListener('click', ()=>{
      worldHidden = !worldHidden;
      Scene3D.setWorldHidden(worldHidden);
      el.btnHideWorld.textContent = worldHidden ? 'Show world' : 'Hide world';
      el.btnHideWorld.setAttribute('aria-pressed', String(worldHidden));
    });
    el.worldOpacitySlider.addEventListener('input', ()=>{
      const v = parseInt(el.worldOpacitySlider.value,10);
      el.worldOpacityValue.textContent = `${v}%`;
      Scene3D.setWorldOpacity(v/100);
    });
  }
