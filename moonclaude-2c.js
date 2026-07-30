  /* ---------------- Sun, Moon, and their lights ---------------- */
  function buildSunMoon(scene){
    // Sun: emissive sphere + soft glow sprite (glow scales with the Sun's own size control)
    const sunMat = new THREE.MeshBasicMaterial({ color:0xfff2c8 });
    sunMesh = new THREE.Mesh(new THREE.SphereGeometry(baseSunRadius,20,16), sunMat);
    scene.add(sunMesh);

    const glowTex = makeCanvasTexture(128,128,(ctx,w,h)=>{
      const grad = ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,w/2);
      grad.addColorStop(0,'rgba(255,240,190,0.9)');
      grad.addColorStop(0.4,'rgba(255,210,120,0.35)');
      grad.addColorStop(1,'rgba(255,180,80,0)');
      ctx.fillStyle = grad; ctx.fillRect(0,0,w,h);
    });
    const glowMat = new THREE.SpriteMaterial({ map: glowTex, transparent:true, depthWrite:false, blending: THREE.AdditiveBlending });
    sunGlow = new THREE.Sprite(glowMat);
    sunGlow.scale.set(baseSunRadius*7, baseSunRadius*7, 1);
    scene.add(sunGlow);

    sunLight = new THREE.DirectionalLight(0xfff3de, 1.4);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.set(2048,2048);
    sunLight.shadow.camera.left = -140; sunLight.shadow.camera.right = 140;
    sunLight.shadow.camera.top = 140; sunLight.shadow.camera.bottom = -140;
    sunLight.shadow.camera.near = 10; sunLight.shadow.camera.far = 1400;
    sunLight.shadow.bias = -0.0015;
    scene.add(sunLight); scene.add(sunLight.target);

    // Moon: shaded sphere lit by the sun direction (gives a physically-derived
    // correct terminator and bright-limb orientation "for free"); a faint
    // secondary fill simulates earthshine on the dark limb.
    moonGroup = new THREE.Group();
    const moonMat = new THREE.MeshStandardMaterial({ color:0xcfd3d8, roughness:0.95, metalness:0.0, emissive:0x0b0f18, emissiveIntensity:0.35 });
    moonMesh = new THREE.Mesh(new THREE.SphereGeometry(baseMoonRadius,32,24), moonMat);
    // subtle procedural "craters" via a canvas bump-ish colour texture
    const moonTex = makeCanvasTexture(256,256,(ctx,w,h)=>{
      ctx.fillStyle = '#cfd3d8'; ctx.fillRect(0,0,w,h);
      const rnd = mulberry32(99);
      ctx.fillStyle = 'rgba(120,125,135,0.5)';
      for(let i=0;i<70;i++){
        const x = rnd()*w, y = rnd()*h, r = 2+rnd()*9;
        ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
      }
      ctx.fillStyle = 'rgba(170,175,185,0.35)';
      for(let i=0;i<10;i++){
        const x = rnd()*w, y = rnd()*h, r = 10+rnd()*22;
        ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
      }
    });
    moonMat.map = moonTex;
    moonGroup.add(moonMesh);
    scene.add(moonGroup);

    moonLight = new THREE.DirectionalLight(0x9fb3d8, 0.0);
    scene.add(moonLight); scene.add(moonLight.target);
  }

  function azAltToDirection(azDeg, altDeg){
    const az = deg2rad(azDeg), alt = deg2rad(altDeg);
    return new THREE.Vector3(
      Math.sin(az)*Math.cos(alt),   // east -> +X
      Math.sin(alt),                // up -> +Y
      Math.cos(az)*Math.cos(alt)    // north -> +Z
    );
  }

  function updateSunMoonPlacement(astro){
    const sunDir = azAltToDirection(astro.sun.azimuth, astro.sun.altitude);
    const moonDir = azAltToDirection(astro.moon.azimuth, astro.moon.altitude);
    const D = CONFIG.celestialDistance;

    sunMesh.position.copy(sunDir).multiplyScalar(D);
    sunGlow.position.copy(sunMesh.position);
    // Always visible — including below the horizon — so their position can be
    // seen at any time. (The world's own geometry, when shown, naturally
    // occludes the view toward them from ground level.)
    sunMesh.visible = true;
    sunGlow.visible = true;

    moonGroup.position.copy(moonDir).multiplyScalar(D);
    moonGroup.visible = true;

    // Orient the Moon so it is lit realistically from the Sun's true direction
    // (physically-based shading => correct terminator & bright-limb automatically).
    sunLight.position.copy(sunDir).multiplyScalar(300);
    sunLight.target.position.set(0,0,0);
    moonLight.position.copy(moonDir).multiplyScalar(300);
    moonLight.target.position.set(0,0,0);

    // A dedicated light on the Moon mesh itself, always from the true Sun
    // direction, so the phase is correct even when using "forced daylight"/
    // "night" presets that alter the main scene lighting.
    moonMesh.userData.sunDirWorld = sunDir.clone();

    applySizeMultipliers();
  }

  function applySizeMultipliers(){
    if(sunMesh){
      const s = sunSizeMultiplier;
      sunMesh.scale.setScalar(s);
      sunGlow.scale.set(baseSunRadius*7*s, baseSunRadius*7*s, 1);
    }
    if(moonMesh){ moonMesh.scale.setScalar(moonSizeMultiplier); }
  }

  /* ---------------- Decorative starfield (fixed seed) ---------------- */
  function buildStars(scene){
    const rnd = mulberry32(CONFIG.seed);
    const count = 1400;
    const positions = new Float32Array(count*3);
    for(let i=0;i<count;i++){
      const theta = rnd()*Math.PI*2;
      const phi = Math.acos(1-2*rnd()); // uniform on sphere, but keep upper hemisphere-ish
      const r = CONFIG.starDistance;
      const x = r*Math.sin(phi)*Math.cos(theta);
      const y = Math.abs(r*Math.cos(phi))*0.98 + r*0.02; // bias upward, but allow near-horizon
      const z = r*Math.sin(phi)*Math.sin(theta);
      positions[i*3]=x; positions[i*3+1]=y; positions[i*3+2]=z;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions,3));
    const mat = new THREE.PointsMaterial({ color:0xffffff, size:1.6, sizeAttenuation:false, transparent:true, opacity:0.75 });
    starPoints = new THREE.Points(geo, mat);
    scene.add(starPoints);
  }

  /* ---------------- Lighting modes (auto / forced daylight / enhanced night) ---------------- */
  function twilightPhaseFor(altDeg){
    if(altDeg > -0.83) return 'Daylight';
    if(altDeg > -6) return 'Civil twilight';
    if(altDeg > -12) return 'Nautical twilight';
    if(altDeg > -18) return 'Astronomical twilight';
    return 'Night';
  }

  function updateLighting(astro){
    const alt = astro.sun.trueAltitude;
    let sunIntensity, hemiIntensity, ambient, starOpacity, moonLightIntensity, lampOn;

    if(lightingMode === 'day'){
      sunIntensity = 1.5; hemiIntensity = 0.85; ambient = 0.55; starOpacity = 0; moonLightIntensity = 0.05; lampOn = 0;
    } else if(lightingMode === 'night'){
      sunIntensity = 0.02; hemiIntensity = 0.12; ambient = 0.32; starOpacity = 0.85; moonLightIntensity = 0.35; lampOn = 1;
    } else {
      // auto — driven by true solar altitude
      const t = clamp((alt + 18)/18, 0, 1); // 0 at -18deg (astro night) -> 1 at 0deg (horizon)
      sunIntensity = clamp((alt+2)/14, 0, 1) * 1.5;
      hemiIntensity = 0.08 + t*0.85;
      ambient = 0.06 + t*0.55;
      starOpacity = clamp(1 - t*1.3, 0, 1) * (alt < -0.83 ? 1 : 0);
      moonLightIntensity = clamp((astro.moon.trueAltitude+2)/20,0,1) * 0.3 * (1-t*0.8);
      lampOn = alt < -1 ? 1 : 0;
    }

    sunLight.intensity = sunIntensity;
    hemiLight.intensity = hemiIntensity;
    ambientLight.intensity = ambient;
    moonLight.intensity = moonLightIntensity;
    starPoints.material.opacity = starOpacity * 0.85;

    // sky colour drifts from deep night navy -> twilight indigo -> day blue
    const t2 = clamp((alt+10)/20,0,1);
    const nightCol = new THREE.Color(0x05060c);
    const twilightCol = new THREE.Color(0x1c2440);
    const dayCol = new THREE.Color(0x8fb8e6);
    let sky = nightCol.clone().lerp(twilightCol, clamp(t2*2,0,1)).lerp(dayCol, clamp((t2-0.5)*2,0,1));
    if(lightingMode==='day') sky = dayCol;
    if(lightingMode==='night') sky = nightCol;
    renderer.setClearColor(sky, 1);
    scene.fog.color = sky;

    lamps.forEach(l=>{ l.userData.lampMat.emissiveIntensity = lampOn * 1.4; });

    return twilightPhaseFor(alt);
  }

  /* ---------------- World visibility / opacity ---------------- */
  function applyWorldVisibility(){
    worldGroup.visible = !worldHidden;
    worldMaterials.forEach(m=>{
      m.transparent = worldOpacity < 1;
      m.opacity = worldOpacity;
      m.needsUpdate = true;
    });
  }
