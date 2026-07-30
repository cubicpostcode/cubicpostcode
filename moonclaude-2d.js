  /* ---------------- Camera presets ---------------- */
  const MIN_CAMERA_HEIGHT = 1.2; // metres above the plaza — keeps the camera from sinking underground

  /** Limits how far phi (polar angle, measured from +Y) can increase before the
      camera would sink below MIN_CAMERA_HEIGHT, without capping how far it can
      tilt upward otherwise (unlike a flat maxPolarAngle, which would also block
      steep upward tilting from a low target). */
  function clampPhiForGround(radius, phi, targetY){
    if(radius <= 0) return phi;
    const cosLimit = (MIN_CAMERA_HEIGHT - targetY) / radius;
    if(cosLimit <= -1) return phi; // whole range is safely above ground
    const phiLimit = Math.acos(clamp(cosLimit, -1, 1));
    return Math.min(phi, phiLimit);
  }

  function setSpherical(radius, azimuthRad, polarRad){
    const target = controls.target;
    polarRad = clampPhiForGround(radius, polarRad, target.y);
    const x = target.x + radius*Math.sin(polarRad)*Math.sin(azimuthRad);
    const z = target.z + radius*Math.sin(polarRad)*Math.cos(azimuthRad);
    const y = target.y + radius*Math.cos(polarRad);
    camera.position.set(x,y,z);
    controls.update();
  }

  function resetView(){
    controls.target.set(0,10,0);
    setSpherical(115, deg2rad(200), deg2rad(62));
  }
  function aerialView(){
    controls.target.set(0,0,10);
    setSpherical(210, deg2rad(200), deg2rad(12));
  }
  function groundView(){
    controls.target.set(0,3,0);
    setSpherical(55, deg2rad(190), deg2rad(84));
  }
  function centreOn(dirGetter){
    if(!currentAstro) return;
    const d = dirGetter(currentAstro);
    const r = clamp(controls.target.distanceTo(camera.position), 20, 120);
    // Place the camera back along the opposite of the target direction, so
    // looking at the target looks straight toward the Sun/Moon's sky position.
    camera.position.copy(controls.target).addScaledVector(d, -r);
    if(camera.position.y < MIN_CAMERA_HEIGHT) camera.position.y = MIN_CAMERA_HEIGHT;
    camera.lookAt(controls.target);
    controls.update();
  }

  function rotateWorld(deltaAzimuthRad){
    const target = controls.target;
    const offset = new THREE.Vector3().subVectors(camera.position, target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    spherical.theta += deltaAzimuthRad;
    offset.setFromSpherical(spherical);
    camera.position.copy(target).add(offset);
    camera.lookAt(target);
    controls.update();
  }
  function tiltCamera(deltaPolarRad){
    const target = controls.target;
    const offset = new THREE.Vector3().subVectors(camera.position, target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    let phi = clamp(spherical.phi + deltaPolarRad, 0.01, Math.PI-0.01);
    phi = clampPhiForGround(spherical.radius, phi, target.y);
    spherical.phi = phi;
    offset.setFromSpherical(spherical);
    camera.position.copy(target).add(offset);
    camera.lookAt(target);
    controls.update();
  }
  function setCompassFacing(headingDeg){
    const target = controls.target;
    const offset = new THREE.Vector3().subVectors(camera.position, target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    // azimuth 0 = looking from north toward origin i.e. camera placed north; align theta with heading
    spherical.theta = deg2rad(headingDeg);
    offset.setFromSpherical(spherical);
    camera.position.copy(target).add(offset);
    camera.lookAt(target);
    controls.update();
  }
  function currentCompassFacingDeg(){
    const target = controls.target;
    const offset = new THREE.Vector3().subVectors(camera.position, target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    return ((rad2deg(spherical.theta) % 360) + 360) % 360;
  }

  let lamps = [];

  /* ---------------- Init ---------------- */
  function init(canvasEl){
    canvas = canvasEl;
    renderer = new THREE.WebGLRenderer({ canvas, antialias:true, powerPreference:'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputEncoding = THREE.sRGBEncoding;

    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x1c2440, 260, 950);

    camera = new THREE.PerspectiveCamera(55, 1, 0.5, 2000);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.minDistance = 8;
    controls.maxDistance = 420;
    controls.minPolarAngle = 0.01;
    controls.maxPolarAngle = Math.PI - 0.01; // full tilt range; ground clamp below handles the floor
    controls.target.set(0,10,0);
    controls.addEventListener('change', ()=>{
      if(camera.position.y < MIN_CAMERA_HEIGHT) camera.position.y = MIN_CAMERA_HEIGHT;
    });

    hemiLight = new THREE.HemisphereLight(0x9db4d8, 0x36302a, 0.6);
    scene.add(hemiLight);
    ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
    scene.add(ambientLight);

    worldGroup = new THREE.Group();
    scene.add(worldGroup);

    buildGround(worldGroup);
    const colInfo = buildNelsonColumn(worldGroup);
    buildLions(worldGroup, colInfo.baseTopY);
    buildFountains(worldGroup);
    buildNationalGallery(worldGroup, 3.2);
    buildStMartins(worldGroup, 3.2);
    buildAdmiraltyArch(worldGroup);
    buildSurroundingBuildings(worldGroup);
    lamps = buildTreesAndLamps(worldGroup);

    buildSunMoon(scene);
    buildStars(scene);

    resetView();
    handleResize();
  }

  function handleResize(){
    const w = canvas.clientWidth || canvas.parentElement.clientWidth;
    const h = canvas.clientHeight || canvas.parentElement.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w/h;
    camera.updateProjectionMatrix();
  }

  function updateAstro(astro){
    currentAstro = astro;
    updateSunMoonPlacement(astro);
    const phase = updateLighting(astro);
    return phase;
  }

  function render(){
    controls.update();
    renderer.render(scene, camera);
  }

const Scene3D = {
    init, handleResize, render, updateAstro,
    setSunSize:(v)=>{ sunSizeMultiplier=v; applySizeMultipliers(); },
    setMoonSize:(v)=>{ moonSizeMultiplier=v; applySizeMultipliers(); },
    setLightingMode:(m)=>{ lightingMode=m; if(currentAstro) updateLighting(currentAstro); },
    setWorldOpacity:(v)=>{ worldOpacity=v; applyWorldVisibility(); },
    setWorldHidden:(b)=>{ worldHidden=b; applyWorldVisibility(); },
    setFOV:(deg)=>{ camera.fov = deg; camera.updateProjectionMatrix(); },
    resetView, aerialView, groundView,
    centreOnSun:()=> centreOn(a=>azAltToDirection(a.sun.azimuth, Math.max(a.sun.altitude,2))),
    centreOnMoon:()=> centreOn(a=>azAltToDirection(a.moon.azimuth, Math.max(a.moon.altitude,2))),
    rotateWorld, tiltCamera, setCompassFacing, currentCompassFacingDeg,
    get camera(){ return camera; }, get controls(){ return controls; },
  };
