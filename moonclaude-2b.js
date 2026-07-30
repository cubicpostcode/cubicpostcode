  /* ---------------- National Gallery (north side) ---------------- */
  function buildColonnade(count, spacing, colH, colR, mat){
    const g = new THREE.Group();
    for(let i=0;i<count;i++){
      const col = new THREE.Mesh(new THREE.CylinderGeometry(colR,colR*1.08,colH,10), mat);
      col.position.x = (i-(count-1)/2)*spacing;
      col.position.y = colH/2;
      col.castShadow = true; col.receiveShadow = true;
      g.add(col);
    }
    return g;
  }

  function buildTriangularPediment(width, height, depth, mat){
    const shape = new THREE.Shape();
    shape.moveTo(-width/2, 0);
    shape.lineTo(width/2, 0);
    shape.lineTo(0, height);
    shape.lineTo(-width/2, 0);
    const geo = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled:false });
    geo.translate(0,0,-depth/2);
    const mesh = new THREE.Mesh(geo, mat);
    mesh.castShadow = true; mesh.receiveShadow = true;
    return mesh;
  }

  function buildNationalGallery(group, terraceTopY){
    const g = new THREE.Group();
    const stoneMat = stoneMaterial(0xd7cba8, 0.85);
    const darkStoneMat = stoneMaterial(0xb9ad8b, 0.85);

    // main block
    const mainW = 120, mainH = 16, mainD = 16;
    const main = new THREE.Mesh(new THREE.BoxGeometry(mainW, mainH, mainD), stoneMat);
    main.position.set(0, terraceTopY + mainH/2, 60);
    main.castShadow = true; main.receiveShadow = true;
    g.add(main);

    // portico projecting toward the square
    const porticoDepth = 8, porticoH = 13, porticoW = 34;
    const porticoRoof = new THREE.Mesh(new THREE.BoxGeometry(porticoW, 1.2, porticoDepth), darkStoneMat);
    porticoRoof.position.set(0, terraceTopY + porticoH, 60 - mainD/2 - porticoDepth/2 + 0.5);
    g.add(porticoRoof);
    const columns = buildColonnade(8, porticoW/7.2, porticoH, 0.85, stoneMat);
    columns.position.set(0, terraceTopY, 60 - mainD/2 - porticoDepth + 1);
    g.add(columns);
    const pediment = buildTriangularPediment(porticoW+2, 5.5, porticoDepth+1, darkStoneMat);
    pediment.position.set(0, terraceTopY + porticoH + 1.2, 60 - mainD/2 - porticoDepth/2 + 0.5);
    g.add(pediment);

    // central dome
    const drum = new THREE.Mesh(new THREE.CylinderGeometry(6.2,6.2,4.5,20), stoneMat);
    drum.position.set(0, terraceTopY + mainH + 2.25, 60);
    g.add(drum);
    const dome = new THREE.Mesh(new THREE.SphereGeometry(6.4, 20, 14, 0, Math.PI*2, 0, Math.PI/2), darkStoneMat);
    dome.position.set(0, terraceTopY + mainH + 4.5, 60);
    g.add(dome);
    const lantern = new THREE.Mesh(new THREE.CylinderGeometry(1.1,1.1,2.4,12), stoneMat);
    lantern.position.set(0, terraceTopY + mainH + 4.5 + 6.4 + 1.2, 60);
    g.add(lantern);

    // long flanking colonnade suggestion (flat pilasters via thin boxes)
    for(let side of [-1,1]){
      const wing = buildColonnade(10, 3.6, 10, 0.5, stoneMat);
      wing.position.set(side*44, terraceTopY, 60-mainD/2+1);
      g.add(wing);
    }

    // windows texture band (simple representative row via emissive-off canvas)
    const winTex = makeCanvasTexture(256,64,(ctx,w,h)=>{
      ctx.fillStyle='#00000000'; ctx.clearRect(0,0,w,h);
      ctx.fillStyle='rgba(60,70,90,0.5)';
      for(let x=6;x<w;x+=22){ ctx.fillRect(x,10,12,h-20); }
    });
    winTex.repeat.set(4,1);
    const winMat = trackedMat(new THREE.MeshStandardMaterial({ map:winTex, transparent:true, roughness:0.6 }));
    const winBand = new THREE.Mesh(new THREE.PlaneGeometry(mainW-6, 5), winMat);
    winBand.position.set(0, terraceTopY+9, 60+mainD/2+0.05);
    g.add(winBand);

    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    group.add(g);
    return { frontZ: 60 - mainD/2 - porticoDepth };
  }

  /* ---------------- St Martin-in-the-Fields (north-east) ---------------- */
  function buildStMartins(group, terraceTopY){
    const g = new THREE.Group();
    const mat = stoneMaterial(0xd9cfae, 0.85);
    const darkMat = stoneMaterial(0xb7ab88, 0.85);

    const bodyW = 20, bodyH = 12, bodyD = 34;
    const body = new THREE.Mesh(new THREE.BoxGeometry(bodyW,bodyH,bodyD), mat);
    body.position.set(78, terraceTopY+bodyH/2, 40);
    g.add(body);

    const porticoCols = buildColonnade(6, 3.0, 9, 0.6, mat);
    porticoCols.position.set(78, terraceTopY, 40-bodyD/2-3);
    g.add(porticoCols);
    const pediment = buildTriangularPediment(20, 4, 6, darkMat);
    pediment.position.set(78, terraceTopY+9+0.7, 40-bodyD/2-3);
    g.add(pediment);

    // steeple: tower + spire stack
    const towerH = 14;
    const tower = new THREE.Mesh(new THREE.BoxGeometry(6,towerH,6), mat);
    tower.position.set(78, terraceTopY+bodyH+towerH/2, 40-bodyD/2-3);
    g.add(tower);
    const spireBase = new THREE.Mesh(new THREE.CylinderGeometry(3.6,3.6,3,10), darkMat);
    spireBase.position.set(78, terraceTopY+bodyH+towerH+1.5, 40-bodyD/2-3);
    g.add(spireBase);
    const spire = new THREE.Mesh(new THREE.ConeGeometry(3.2,12,10), darkMat);
    spire.position.set(78, terraceTopY+bodyH+towerH+3+6, 40-bodyD/2-3);
    g.add(spire);
    const finial = new THREE.Mesh(new THREE.SphereGeometry(0.4,8,8), trackedMat(new THREE.MeshStandardMaterial({color:0x7a6a3a, metalness:0.7, roughness:0.3})));
    finial.position.set(78, terraceTopY+bodyH+towerH+3+12+0.4, 40-bodyD/2-3);
    g.add(finial);

    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    group.add(g);
  }

  /* ---------------- Admiralty Arch (south side, toward the Mall) ---------------- */
  function buildAdmiraltyArch(group){
    const g = new THREE.Group();
    const mat = stoneMaterial(0xcabf9f, 0.85);
    const archH = 11, archW = 46, archD = 9;
    const lintelH = 3.2;
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(archW, lintelH, archD), mat);
    lintel.position.set(0, archH+lintelH/2, -58);
    g.add(lintel);
    // three openings via piers
    const piers = [-archW/2+3, -archW/6, archW/6, archW/2-3];
    for(let i=0;i<piers.length;i++){
      const pierW = i===0||i===piers.length-1 ? 6 : 3.4;
      const pier = new THREE.Mesh(new THREE.BoxGeometry(pierW, archH, archD), mat);
      pier.position.set(piers[i], archH/2, -58);
      g.add(pier);
    }
    const attic = new THREE.Mesh(new THREE.BoxGeometry(archW, 4, archD), mat);
    attic.position.set(0, archH+lintelH+2, -58);
    g.add(attic);
    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    group.add(g);
  }

  /* ---------------- Trees, lamps, representative surrounding buildings ---------------- */
  function buildTree(){
    const g = new THREE.Group();
    const trunkMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x5b4632, roughness:1 }));
    const leafMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x3c6b3f, roughness:0.95 }));
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.22,0.3,2.6,6), trunkMat);
    trunk.position.y = 1.3; g.add(trunk);
    const leaves = new THREE.Mesh(new THREE.SphereGeometry(1.8,8,7), leafMat);
    leaves.position.y = 3.4; leaves.scale.set(1,1.15,1); g.add(leaves);
    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    return g;
  }

  function buildLamp(){
    const g = new THREE.Group();
    const metalMat = trackedMat(new THREE.MeshStandardMaterial({ color:0x2c2c2c, roughness:0.5, metalness:0.7 }));
    const glassMat = trackedMat(new THREE.MeshStandardMaterial({ color:0xfff3cf, emissive:0xffdd88, emissiveIntensity:0, roughness:0.4 }));
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.09,4.6,8), metalMat);
    pole.position.y = 2.3; g.add(pole);
    const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.22,8,8), glassMat);
    lamp.position.y = 4.7; g.add(lamp);
    g.userData.lampMat = glassMat;
    g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; } });
    return g;
  }

  function buildSurroundingBuildings(group){
    const facadeTex = makeCanvasTexture(256,256,(ctx,w,h)=>{
      ctx.fillStyle = '#3a3630'; ctx.fillRect(0,0,w,h);
      ctx.fillStyle = 'rgba(120,130,150,0.55)';
      for(let y=14;y<h;y+=34){ for(let x=10;x<w;x+=26){ ctx.fillRect(x,y,14,20); } }
    });
    const facadeMat = trackedMat(new THREE.MeshStandardMaterial({ map:facadeTex, roughness:0.9 }));
    const rects = [
      { x:-95, z:-10, w:26, d:26, h:22 },
      { x:-95, z:35,  w:26, d:26, h:26 },
      { x:95,  z:-10, w:26, d:26, h:24 },
      { x:95,  z:35,  w:26, d:26, h:20 },
      { x:-95, z:-55, w:26, d:26, h:18 },
      { x:95,  z:-55, w:26, d:26, h:18 },
      { x:0,   z:-100,w:60, d:20, h:16 },
    ];
    rects.forEach(r=>{
      const b = new THREE.Mesh(new THREE.BoxGeometry(r.w,r.h,r.d), facadeMat);
      b.position.set(r.x, r.h/2, r.z);
      b.castShadow = true; b.receiveShadow = true;
      group.add(b);
    });
  }

  function buildTreesAndLamps(group){
    const treePositions = [ [-55,-30],[-58,-38],[55,-30],[58,-38],[-50,20],[52,20] ];
    treePositions.forEach(([x,z])=>{ const t = buildTree(); t.position.set(x,0,z); group.add(t); });

    const lampPositions = [
      [-30,25],[30,25],[-18,-25],[18,-25],[-40,-40],[40,-40],
      [-30,0],[30,0]
    ];
    const lamps = [];
    lampPositions.forEach(([x,z])=>{ const l = buildLamp(); l.position.set(x,0,z); group.add(l); lamps.push(l); });
    return lamps;
  }
