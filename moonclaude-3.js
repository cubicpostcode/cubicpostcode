/* =====================================================================
   7. MOON PHASE PANEL (2D canvas illustration)
   Draws the correct illuminated fraction and terminator shape, rotated so
   the bright limb points in the correct direction as seen from the
   observer's local zenith (an illustrative companion to the physically
   lit 3D Moon, which is the primary accurate representation).
   ===================================================================== */
function drawMoonPhasePanel(canvasEl, phaseInfo){
  const ctx = canvasEl.getContext('2d');
  const w = canvasEl.width, h = canvasEl.height;
  const cx = w/2, cy = h/2, R = Math.min(w,h)/2 - 6;
  ctx.clearRect(0,0,w,h);

  // dark base disc (unlit portion / earthshine)
  ctx.save();
  ctx.beginPath(); ctx.arc(cx,cy,R,0,Math.PI*2);
  ctx.fillStyle = 'rgba(60,68,84,0.55)';
  ctx.fill();
  ctx.restore();

  // illuminated silhouette, canonical "bulge to +X", then rotated to the
  // correct sky orientation
  ctx.save();
  ctx.translate(cx,cy);
  ctx.rotate(phaseInfo.brightLimbAngleFromZenith - Math.PI/2);

  const k = clamp(phaseInfo.illuminatedFraction, 0, 1);
  if(k > 0.003){
    ctx.beginPath();
    ctx.arc(0,0,R, -Math.PI/2, Math.PI/2, false); // right half-circle boundary
    const rx = R * Math.abs(1 - 2*k);
    if(k < 0.5){
      ctx.ellipse(0,0, rx, R, 0, Math.PI/2, -Math.PI/2, true);
    } else {
      ctx.ellipse(0,0, rx, R, 0, Math.PI/2, -Math.PI/2, false);
    }
    ctx.closePath();
    ctx.fillStyle = '#f2ecd8';
    ctx.fill();
  }
  ctx.restore();

  // rim
  ctx.beginPath(); ctx.arc(cx,cy,R,0,Math.PI*2);
  ctx.strokeStyle = 'rgba(238,231,216,0.25)'; ctx.lineWidth = 1;
  ctx.stroke();
}

/* =====================================================================
   8–10. APP CONTROLLER — state, UI wiring, keyboard controls, main loop
   ===================================================================== */
  const SPEED_STEPS = [
    { mult: 1,      label: 'Real time' },
    { mult: 60,     label: '60× (1 min/s)' },
    { mult: 600,    label: '600× (10 min/s)' },
    { mult: 3600,   label: '1 hr/s' },
    { mult: 14400,  label: '4 hr/s' },
    { mult: 43200,  label: '12 hr/s' },
    { mult: 86400,  label: '1 day/s' },
  ];

  const state = {
    simTime: new Date(),      // authoritative UTC instant being displayed
    useLondon: true,
    playing: false,
    speedIndex: 1,
    lastFrameMs: null,
    lastComputeMs: 0,
    dataStripOpen: true,
  };

  const el = {}; // cached DOM refs, filled in cacheEls()

  function cacheEls(){
    const ids = ['dateTimeInput','dtInputZoneLabel','btnNow','stepDayBack','stepHourBack','stepMinBack',
      'stepMinFwd','stepHourFwd','stepDayFwd','btnPlay','btnPause','speedSlider','speedLabel','todSlider',
      'btnLondonTime','btnUtcTime','chronoDate','chronoTime','chronoSecs','chronoZone',
      'viewReset','viewAerial','viewGround','viewCentreSun','viewCentreMoon','fovSlider','fovValue',
      'facingSlider','facingValue','sunSizeSlider','sunSizeValue','moonSizeSlider','moonSizeValue',
      'lightAuto','lightDay','lightNight','btnHideWorld','worldOpacitySlider','worldOpacityValue',
      'sunData','moonData','moonPhaseCanvas','moonPhaseCaption','twilightPhase','lightPhaseTag',
      'sunQuick','moonQuick','errorBanner','viewportLoading','viewportLoadingText','toggleDataStrip',
      'dataStrip','menuToggle','menuToggleRight','leftPanel','rightPanel','overlayBackdrop',
      'compassStrip','scene-canvas'];
    ids.forEach(id=>{ el[id] = document.getElementById(id); });
  }

  function showError(msg){
    el.errorBanner.textContent = msg;
    el.errorBanner.style.display = 'block';
    console.error('[Trafalgar Sky]', msg);
  }

  /* ---------------- Compass bezel ---------------- */
  function buildCompassStrip(){
    const strip = el.compassStrip;
    strip.innerHTML = '';
    // three loops of the compass so it scrolls seamlessly for any camera heading
    for(let loop=0; loop<3; loop++){
      for(let d=0; d<360; d+=10){
        const t = document.createElement('div');
        t.className = 'compass-tick' + (d%90===0 ? ' card' : '');
        t.textContent = d%90===0 ? compassDirection(d) : (d%30===0 ? String(d) : '');
        strip.appendChild(t);
      }
    }
  }
  function updateCompassStrip(headingDeg){
    const tickWidth = 40;
    const ticksPerLoop = 36;
    const loopWidth = tickWidth*ticksPerLoop;
    const offset = (headingDeg/360)*loopWidth;
    el.compassStrip.style.transform = `translateX(${(-loopWidth + el.compassBezelWidth/2) - offset}px)`;
  }

  /* ---------------- Data panel rendering ---------------- */
  function renderDataPanels(astro){
    const s = astro.sun, m = astro.moon, useL = state.useLondon;
    el.sunData.innerHTML = [
      dataItem('Azimuth', fmtAzimuth(s.azimuth)),
      dataItem('Refracted altitude', fmtAltitude(s.altitude)),
      dataItem('RA (of date)', fmtRA(s.raOfDate)),
      dataItem('Dec (of date)', fmtDec(s.decOfDate)),
      dataItem('RA (J2000)', fmtRA(s.raJ2000)),
      dataItem('Dec (J2000)', fmtDec(s.decJ2000)),
      dataItem('Distance', fmtDistanceAU(s.distAU,false)),
      dataItem('Angular diameter', fmtAngularDiameter(s.angularDiameterDeg)),
      dataItem('Above horizon', s.trueAltitude>0 ? 'Yes' : 'No'),
      dataItem('Next rise', fmtEventTime(astro.sunEvents.rise, useL), true),
      dataItem('Next set', fmtEventTime(astro.sunEvents.set, useL), true),
    ].join('');
    const sc = fmtCulmination(astro.sunEvents.culm, useL);
    el.sunData.innerHTML += dataItem('Next culmination', `${sc.time} — ${sc.alt}, ${sc.dir}`, true);

    el.moonData.innerHTML = [
      dataItem('Azimuth', fmtAzimuth(m.azimuth)),
      dataItem('Refracted altitude', fmtAltitude(m.altitude)),
      dataItem('RA (of date)', fmtRA(m.raOfDate)),
      dataItem('Dec (of date)', fmtDec(m.decOfDate)),
      dataItem('RA (J2000)', fmtRA(m.raJ2000)),
      dataItem('Dec (J2000)', fmtDec(m.decJ2000)),
      dataItem('Distance', fmtDistanceAU(m.distAU,true)),
      dataItem('Angular diameter', fmtAngularDiameter(m.angularDiameterDeg)),
      dataItem('Phase', astro.phase.phaseName),
      dataItem('Illuminated fraction', `${(astro.phase.illuminatedFraction*100).toFixed(1)}%`),
      dataItem('Above horizon', m.trueAltitude>0 ? 'Yes' : 'No'),
      dataItem('Next rise', fmtEventTime(astro.moonEvents.rise, useL), true),
      dataItem('Next set', fmtEventTime(astro.moonEvents.set, useL), true),
    ].join('');
    const mc = fmtCulmination(astro.moonEvents.culm, useL);
    el.moonData.innerHTML += dataItem('Next culmination', `${mc.time} — ${mc.alt}, ${mc.dir}`, true);

    el.sunQuick.textContent = `${fmtAltitude(s.altitude)} ${compassDirection(s.azimuth)}`;
    el.moonQuick.textContent = `${fmtAltitude(m.altitude)} ${compassDirection(m.azimuth)} (${(astro.phase.illuminatedFraction*100).toFixed(0)}%)`;

    drawMoonPhasePanel(el.moonPhaseCanvas, astro.phase);
    el.moonPhaseCaption.textContent = `${astro.phase.phaseName} · ${(astro.phase.illuminatedFraction*100).toFixed(1)}% illuminated`;
  }

  function renderChronometer(astro){
    const d = state.simTime;
    if(state.useLondon){
      const p = londonParts(d);
      el.chronoDate.textContent = formatLondonDateLong(d);
      el.chronoTime.textContent = `${pad2(p.hour)}:${pad2(p.minute)}`;
      el.chronoSecs.textContent = pad2(p.second);
      el.chronoZone.textContent = isBST(d) ? 'British Summer Time (BST, UTC+1)' : 'Greenwich Mean Time (GMT, UTC+0)';
    } else {
      el.chronoDate.textContent = formatUtcDateLong(d);
      el.chronoTime.textContent = `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`;
      el.chronoSecs.textContent = pad2(d.getUTCSeconds());
      el.chronoZone.textContent = 'Coordinated Universal Time (UTC)';
    }
    // keep the datetime-local input and time-of-day slider in sync without fighting user edits mid-drag
    if(!inputIsFocused()){
      el.dateTimeInput.value = formatForDateTimeInput(d, state.useLondon);
    }
    if(!todSliderDragging){
      const p2 = state.useLondon ? londonParts(d) : { hour:d.getUTCHours(), minute:d.getUTCMinutes(), second:d.getUTCSeconds() };
      el.todSlider.value = p2.hour*3600 + p2.minute*60 + p2.second;
    }
  }

  function inputIsFocused(){ return document.activeElement === el.dateTimeInput; }
  let todSliderDragging = false;

  /* ---------------- Core recompute + render ---------------- */
  function recomputeAndRender(){
    if(!Astro.ready) return;
    const astro = Astro.compute(state.simTime);
    const phase = Scene3D.updateAstro(astro);
    el.lightPhaseTag.textContent = phase;
    el.twilightPhase.textContent = phase;
    renderDataPanels(astro);
    renderChronometer(astro);
  }
