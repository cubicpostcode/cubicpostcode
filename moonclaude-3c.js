  /* ---------------- Keyboard controls ---------------- */
  function isFormControl(node){
    if(!node) return false;
    const tag = node.tagName;
    return tag==='INPUT' || tag==='SELECT' || tag==='TEXTAREA' || node.isContentEditable;
  }

  function wireKeyboard(){
    window.addEventListener('keydown', (e)=>{
      if(isFormControl(document.activeElement)) return;
      const fast = e.shiftKey ? 3 : 1;
      const rotStep = deg2rad(2*fast);
      const tiltStep = deg2rad(1.5*fast);
      switch(e.key){
        case 'ArrowLeft':  Scene3D.rotateWorld(-rotStep); e.preventDefault(); break;
        case 'ArrowRight': Scene3D.rotateWorld(rotStep);  e.preventDefault(); break;
        case 'ArrowUp':    Scene3D.tiltCamera(tiltStep);  e.preventDefault(); break;
        case 'ArrowDown':  Scene3D.tiltCamera(-tiltStep); e.preventDefault(); break;
        default: return;
      }
      syncFacingSliderFromCamera();
    });
  }

  function syncFacingSliderFromCamera(){
    const heading = Scene3D.currentCompassFacingDeg();
    el.facingSlider.value = Math.round(heading);
    el.facingValue.textContent = compassDirection(heading);
    updateCompassStrip(heading);
  }
