  /* ---------------- Panel toggles (mobile) ---------------- */
  function wirePanelToggles(){
    function openPanel(panel){
      panel.classList.add('open');
      el.overlayBackdrop.classList.add('show');
    }
    function closePanels(){
      el.leftPanel.classList.remove('open');
      el.rightPanel.classList.remove('open');
      el.overlayBackdrop.classList.remove('show');
    }
    el.menuToggle.addEventListener('click', ()=> openPanel(el.leftPanel));
    el.menuToggleRight.addEventListener('click', ()=> openPanel(el.rightPanel));
    el.overlayBackdrop.addEventListener('click', closePanels);

    el.toggleDataStrip.addEventListener('click', ()=>{
      state.dataStripOpen = !state.dataStripOpen;
      el.dataStrip.classList.toggle('collapsed', !state.dataStripOpen);
      el.toggleDataStrip.textContent = state.dataStripOpen ? '▾' : '▴';
      el.toggleDataStrip.setAttribute('aria-expanded', String(state.dataStripOpen));
    });
  }
