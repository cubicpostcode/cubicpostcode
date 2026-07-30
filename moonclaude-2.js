/* =====================================================================
   5. SCENE MODULE — Three.js construction of Trafalgar Square
   All geometry is procedural (no external model assets). Materials used
   by "the world" (everything except Sun, Moon, stars) are collected in
   `worldMaterials` so the World Opacity slider / Hide World button can
   affect them uniformly, and `worldGroup` so the whole set can be hidden.
   Scene axes: +X = east, +Z = north, +Y = up. 1 unit = 1 metre.
   ===================================================================== */
  let renderer, scene, camera, controls, canvas;
  let worldGroup, worldMaterials = [];
  let sunMesh, sunGlow, moonMesh, moonGroup, sunLight, moonLight, hemiLight, ambientLight;
  let starPoints;
  let clock;
  let sunSizeMultiplier = 1, moonSizeMultiplier = 1;
  let baseSunRadius = 6, baseMoonRadius = 4.2; // illustrative base radii at celestialDistance
  let currentAstro = null;
  let lightingMode = 'auto'; // 'auto' | 'day' | 'night'
  let worldOpacity = 1;
  let worldHidden = false;

  function makeCanvasTexture(w, h, draw){
    const c = document.createElement('canvas'); c.width=w; c.height=h;
    const ctx = c.getContext('2d');
    draw(ctx, w, h);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    return tex;
  }

  function trackedMat(mat){ worldMaterials.push(mat); return mat; }

  function stoneMaterial(colorHex, roughness=0.9){
    return trackedMat(new THREE.MeshStandardMaterial({ color: colorHex, roughness, metalness:0.02 }));
  }

  /* ---------------- Ground, roads, plaza ---------------- */
  function buildGround(group){
    // Broad dark asphalt base (roads/surrounding city extent)
    const roadTex = makeCanvasTexture(512,512,(ctx,w,h)=>{
      ctx.fillStyle = '#26262b'; ctx.fillRect(0,0,w,h);
      ctx.strokeStyle = 'rgba(255,255,255,0.55)'; ctx.lineWidth=4; ctx.setLineDash([26,20]);
      ctx.beginPath(); ctx.moveTo(w/2,0); ctx.lineTo(w/2,h); ctx.stroke();
    });
    roadTex.repeat.set(20,20);
    const roadMat = trackedMat(new THREE.MeshStandardMaterial({ map: roadTex, roughness:1 }));
    const road = new THREE.Mesh(new THREE.PlaneGeometry(900,900), roadMat);
    road.rotation.x = -Math.PI/2; road.position.y = -0.03; road.receiveShadow = true;
    group.add(road);

    // Plaza — Portland stone paving with a subtle grid of paving joints
    const paveTex = makeCanvasTexture(512,512,(ctx,w,h)=>{
      ctx.fillStyle = '#cdc2a6'; ctx.fillRect(0,0,w,h);
      ctx.strokeStyle = 'rgba(90,80,60,0.35)'; ctx.lineWidth=2;
      const cell = 32;
      for(let x=0;x<=w;x+=cell){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
      for(let y=0;y<=h;y+=cell){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
    });
    paveTex.repeat.set(8,6);
    const paveMat = trackedMat(new THREE.MeshStandardMaterial({ map: paveTex, roughness:0.95 }));
    const plaza = new THREE.Mesh(new THREE.PlaneGeometry(150,110), paveMat);
    plaza.rotation.x = -Math.PI/2; plaza.receiveShadow = true;
    group.add(plaza);

    // Raised northern terrace in front of the National Gallery
    const terraceMat = stoneMaterial(0xc8bd9e, 0.9);
    const terrace = new THREE.Mesh(new THREE.BoxGeometry(140, 3.2, 26), terraceMat);
    terrace.position.set(0, 1.6, 46);
    terrace.castShadow = true; terrace.receiveShadow = true;
    group.add(terrace);

    // Steps down from the terrace toward the square (a stepped block stack)
    const stepMat = stoneMaterial(0xc2b795, 0.9);
    const stepCount = 6;
    for(let i=0;i<stepCount;i++){
      const stepDepth = 1.4, stepHeight = 3.2/stepCount;
      const s = new THREE.Mesh(new THREE.BoxGeometry(140 - i*1.2, stepHeight, stepDepth), stepMat);
      s.position.set(0, stepHeight*(i+0.5), 46-13-1 + i*stepDepth*0.001 - i*stepDepth);
      s.receiveShadow = true; s.castShadow = true;
      group.add(s);
    }

    return { plazaY: 0 };
  }

  /* ---------------- Nelson's Column + statue ---------------- */
  function buildNelsonColumn(group){
    const g = new THREE.Group();
    const graniteMat = stoneMaterial(0x8d867c, 0.85);
    const bronzeMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x4a5b4f, roughness:0.5, metalness:0.6 }));

    // Stepped granite base
    const base1 = new THREE.Mesh(new THREE.BoxGeometry(16,1.2,16), graniteMat);
    base1.position.y = 0.6; g.add(base1);
    const base2 = new THREE.Mesh(new THREE.BoxGeometry(12,1.6,12), graniteMat);
    base2.position.y = 1.2+0.8; g.add(base2);

    // Pedestal with bronze relief panels (flat colour blocks, stylised)
    const pedestal = new THREE.Mesh(new THREE.BoxGeometry(7.5,9,7.5), graniteMat);
    pedestal.position.y = 2.0+4.5; g.add(pedestal);
    const reliefMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x5b6b58, roughness:0.6, metalness:0.4 }));
    [[0,3.76],[Math.PI/2,3.76],[Math.PI,3.76],[-Math.PI/2,3.76]].forEach(([ry,r])=>{
      const panel = new THREE.Mesh(new THREE.PlaneGeometry(4.2,5.2), reliefMat);
      panel.position.set(Math.sin(ry)*r, 6.5, Math.cos(ry)*r);
      panel.rotation.y = ry;
      g.add(panel);
    });

    // Fluted column shaft (cylinder with slight taper, radial segments give flute look)
    const shaftBottomY = 2.0+9;
    const shaftHeight = 34;
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(1.55,1.85, shaftHeight, 20, 1, false), graniteMat);
    shaft.position.y = shaftBottomY + shaftHeight/2;
    shaft.castShadow = true;
    g.add(shaft);

    // Corinthian-ish capital (bronze)
    const capitalY = shaftBottomY + shaftHeight;
    const capital = new THREE.Mesh(new THREE.CylinderGeometry(2.5,1.6,2.6,16), bronzeMat);
    capital.position.y = capitalY + 1.3; g.add(capital);
    const abacus = new THREE.Mesh(new THREE.BoxGeometry(5.6,0.7,5.6), bronzeMat);
    abacus.position.y = capitalY + 2.6+0.35; g.add(abacus);

    // Statue of Nelson — stylised low-poly figure atop the abacus
    const statueY = capitalY + 2.6 + 0.7;
    const statue = new THREE.Group();
    const coat = new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.85,3.0,10), bronzeMat);
    coat.position.y = 1.5; statue.add(coat);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.42,10,8), bronzeMat);
    head.position.y = 3.25; statue.add(head);
    const hat = new THREE.Mesh(new THREE.ConeGeometry(0.55,0.28,3), bronzeMat);
    hat.rotation.y = Math.PI/2; hat.position.y = 3.5; statue.add(hat);
    const armL = new THREE.Mesh(new THREE.CylinderGeometry(0.11,0.11,1.5,6), bronzeMat);
    armL.position.set(-0.55,2.2,0); armL.rotation.z = 0.5; statue.add(armL);
    statue.position.y = statueY;
    statue.castShadow = true;
    g.add(statue);

    g.traverse(o=>{ if(o.isMesh){ o.castShadow = true; o.receiveShadow = true; } });
    group.add(g);
    return { topY: statueY + 3.6, baseTopY: 2.0+9 };
  }

  /* ---------------- Four lions ---------------- */
  function buildLion(){
    const g = new THREE.Group();
    const bronzeMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x46524a, roughness:0.55, metalness:0.55 }));
    const body = new THREE.Mesh(new THREE.BoxGeometry(2.6,1.1,1.15), bronzeMat);
    body.position.y = 0.75; g.add(body);
    const chest = new THREE.Mesh(new THREE.SphereGeometry(0.62,8,8), bronzeMat);
    chest.position.set(1.15,0.85,0); g.add(chest);
    const mane = new THREE.Mesh(new THREE.SphereGeometry(0.62,8,8), bronzeMat);
    mane.scale.set(1,1.15,1.1); mane.position.set(1.45,1.05,0); g.add(mane);
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.55,0.5,0.55), bronzeMat);
    head.position.set(1.85,1.0,0); g.add(head);
    const legGeo = new THREE.CylinderGeometry(0.16,0.18,0.75,6);
    [[0.9,0.55],[0.9,-0.55],[-0.9,0.55],[-0.9,-0.55]].forEach(([x,z])=>{
      const leg = new THREE.Mesh(legGeo, bronzeMat);
      leg.position.set(x,0.38,z); g.add(leg);
    });
    const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.1,1.2,5), bronzeMat);
    tail.position.set(-1.35,0.9,0); tail.rotation.z = Math.PI/2.6; g.add(tail);
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(3.2,0.5,1.8), stoneMaterial(0x8d867c,0.85));
    plinth.position.y = -0.15; g.add(plinth);
    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    return g;
  }

  function buildLions(group, baseTopY){
    const positions = [
      { x: 8.6, z: 8.6, ry: -Math.PI/4 },
      { x: -8.6, z: 8.6, ry: Math.PI/4 },
      { x: 8.6, z: -8.6, ry: -3*Math.PI/4 },
      { x: -8.6, z: -8.6, ry: 3*Math.PI/4 },
    ];
    positions.forEach(p=>{
      const lion = buildLion();
      lion.position.set(p.x, 0.4, p.z);
      lion.rotation.y = p.ry;
      group.add(lion);
    });
  }

  /* ---------------- Fountains ---------------- */
  function buildFountain(){
    const g = new THREE.Group();
    const basinMat = stoneMaterial(0x9aa199, 0.7);
    const waterMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x2e5b6e, roughness:0.15, metalness:0.15, transparent:true, opacity:0.85 }));
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(7.2,7.6,0.9,28), basinMat);
    basin.position.y = 0.45; g.add(basin);
    const water = new THREE.Mesh(new THREE.CylinderGeometry(6.7,6.7,0.12,28), waterMat);
    water.position.y = 0.95; g.add(water);
    const pedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.6,0.9,1.6,12), basinMat);
    pedestal.position.y = 1.2; g.add(pedestal);
    const upperBasin = new THREE.Mesh(new THREE.CylinderGeometry(2.3,2.6,0.5,20), basinMat);
    upperBasin.position.y = 2.1; g.add(upperBasin);
    const spout = new THREE.Mesh(new THREE.CylinderGeometry(0.12,0.18,1.6,8), basinMat);
    spout.position.y = 2.7; g.add(spout);
    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    return g;
  }

  function buildFountains(group){
    const f1 = buildFountain(); f1.position.set(-24, 0, 12); group.add(f1);
    const f2 = buildFountain(); f2.position.set(24, 0, 12); group.add(f2);
  }
