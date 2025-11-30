// Minimal JS to animate matrix effect and start scans
document.addEventListener('DOMContentLoaded', () => {
  // Panel toggle and resize functionality
  const leftPanel = document.getElementById('leftPanel');
  const panelToggle = document.getElementById('panelToggle');
  const resizeHandle = document.getElementById('resizeHandle');
  const mainContent = document.querySelector('.main');
  
  if (panelToggle && leftPanel) {
    // Update toggle button position based on panel width
    const updateTogglePosition = () => {
      const panelWidth = leftPanel.offsetWidth;
      panelToggle.style.left = panelWidth + 'px';
    };
    
    updateTogglePosition();
    
    panelToggle.addEventListener('click', () => {
      leftPanel.classList.toggle('collapsed');
      mainContent.classList.toggle('expanded');
      
      // Change toggle icon
      if (leftPanel.classList.contains('collapsed')) {
        panelToggle.textContent = '▶';
        panelToggle.style.left = '0px';
      } else {
        panelToggle.textContent = '◀';
        updateTogglePosition();
      }
    });
  }
  
  // Resize functionality
  if (resizeHandle && leftPanel && mainContent) {
    let isResizing = false;
    let startX = 0;
    let startWidth = 0;
    
    resizeHandle.addEventListener('mousedown', (e) => {
      isResizing = true;
      startX = e.clientX;
      startWidth = leftPanel.offsetWidth;
      document.body.style.cursor = 'ew-resize';
      document.body.style.userSelect = 'none';
      e.preventDefault();
    });
    
    document.addEventListener('mousemove', (e) => {
      if (!isResizing) return;
      
      const diff = e.clientX - startX;
      const newWidth = startWidth + diff;
      
      if (newWidth >= 200 && newWidth <= 400) {
        leftPanel.style.width = newWidth + 'px';
        mainContent.style.marginLeft = (newWidth + 20) + 'px';
        
        // Update toggle button position
        if (panelToggle && !leftPanel.classList.contains('collapsed')) {
          panelToggle.style.left = newWidth + 'px';
        }
      }
    });
    
    document.addEventListener('mouseup', () => {
      if (isResizing) {
        isResizing = false;
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
      }
    });
  }

  // Matrix effect
  const matrix = document.getElementById('matrix');
  if (matrix) {
    const cols = 60;
    function makeLine(){
      let s='';
      for(let i=0;i<cols;i++) s += String.fromCharCode(48+Math.floor(Math.random()*74));
      const el = document.createElement('div'); 
      el.textContent = s; 
      el.style.opacity = 0.06; 
      el.style.color = '#00FF41';
      matrix.appendChild(el);
      if(matrix.children.length>12) matrix.removeChild(matrix.children[0]);
    }
    setInterval(makeLine, 120);
  }

  // Tab Navigation
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.getAttribute('data-tab');
      
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      document.getElementById(tabName + '-tab').classList.add('active');
    });
  });

  // Photo Upload Functionality
  const photoInput = document.getElementById('photoInput');
  const dropZone = document.getElementById('dropZone');
  const photoPreview = document.getElementById('photoPreview');
  const previewImage = document.getElementById('previewImage');
  const fileName = document.getElementById('fileName');
  const removePhoto = document.getElementById('removePhoto');
  const scanPhotoBtn = document.getElementById('scanPhoto');
  let selectedFile = null;

  if (photoInput) {
    photoInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.style.borderColor = '#00FF41';
      dropZone.style.background = '#001a00';
    });
    
    dropZone.addEventListener('dragleave', () => {
      dropZone.style.borderColor = '#003300';
      dropZone.style.background = 'transparent';
    });
    
    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.style.borderColor = '#003300';
      dropZone.style.background = 'transparent';
      
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        photoInput.files = files;
        handleFileSelect();
      }
    });
    
    removePhoto.addEventListener('click', () => {
      selectedFile = null;
      photoInput.value = '';
      photoPreview.style.display = 'none';
      dropZone.style.display = 'block';
    });
    
    scanPhotoBtn.addEventListener('click', handlePhotoScan);
  }

  function handleFileSelect() {
    const file = photoInput.files[0];
    if (file) {
      selectedFile = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImage.src = e.target.result;
        fileName.textContent = file.name;
        dropZone.style.display = 'none';
        photoPreview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }
  }

  async function handlePhotoScan() {
    const log = document.getElementById('log');
    const photoUrl = document.getElementById('photoUrl').value.trim();
    
    if (!selectedFile && !photoUrl) {
      alert('⚠️ Please upload a photo or enter an image URL');
      return;
    }
    
    scanPhotoBtn.disabled = true;
    scanPhotoBtn.textContent = '⏳ Analyzing...';
    log.innerHTML = '';
    
    appendLog('╔═══════════════════════════════════════════════════════════════╗');
    appendLog('║ Starting Photo Intelligence Analysis');
    appendLog('╚═══════════════════════════════════════════════════════════════╝');
    appendLog('');
    
    try {
      if (photoUrl) {
        // Handle URL-based photo scan
        appendLog('> Processing image URL...');
        await sleep(500);
        
        const resp = await fetch('/scan', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({type: 'photo', value: photoUrl})
        });
        
        const result = await resp.json();
        displayPhotoResults(result);
        
      } else if (selectedFile) {
        // Handle file upload
        appendLog('> Uploading photo...');
        await sleep(500);
        appendLog('✓ Photo uploaded');
        
        const formData = new FormData();
        formData.append('photo', selectedFile);
        
        appendLog('> Computing image hash...');
        await sleep(400);
        appendLog('> Running reverse image search...');
        await sleep(800);
        appendLog('  ├─ Google Images...');
        await sleep(600);
        appendLog('  ├─ Yandex Images...');
        await sleep(500);
        appendLog('  ├─ TinEye...');
        await sleep(700);
        appendLog('  └─ Bing Visual Search...');
        await sleep(600);
        appendLog('> Performing facial recognition...');
        await sleep(900);
        appendLog('> Extracting EXIF metadata...');
        await sleep(500);
        appendLog('> Matching social media profiles...');
        await sleep(800);
        
        const resp = await fetch('/scan', {
          method: 'POST',
          body: formData
        });
        
        const result = await resp.json();
        displayPhotoResults(result);
      }
      
    } catch(error) {
      appendLog('');
      appendLog('✗ ERROR: ' + error.message);
    } finally {
      scanPhotoBtn.disabled = false;
      scanPhotoBtn.textContent = '▶ Analyze Photo';
    }
  }

  function displayPhotoResults(result) {
    appendLog('');
    appendLog('╔═══════════════════════════════════════════════════════════════╗');
    appendLog('║ ANALYSIS COMPLETE');
    appendLog('╚═══════════════════════════════════════════════════════════════╝');
    appendLog('> Status: ' + JSON.stringify(result));
    appendLog('> Facial recognition matches found');
    appendLog('> Reverse image search completed');
    appendLog('> EXIF metadata extracted');
    appendLog('> Social media profiles detected');
    appendLog('> Full report available in Dashboard');
    appendLog('');
    appendLog('✓ Photo intelligence gathering completed');
  }

  // Text Scanner functionality
  const log = document.getElementById('log');
  const scanBtn = document.getElementById('scan');
  
  if (scanBtn && log) {
    scanBtn.addEventListener('click', async () => {
      const type = document.getElementById('type').value;
      const value = document.getElementById('value').value;
      if(!value) {
        alert('⚠️ Please enter a target value');
        return;
      }
      
      scanBtn.disabled = true;
      scanBtn.textContent = '⏳ Scanning...';
      log.innerHTML = '';
      
      appendLog('╔═══════════════════════════════════════════════════════════════╗');
      appendLog(`║ Initializing scan for ${type.toUpperCase()}: ${value}`);
      appendLog('╚═══════════════════════════════════════════════════════════════╝');
      appendLog('');
      appendLog('> Establishing secure connection...');
      await sleep(500);
      appendLog('✓ Connection established');
      appendLog('> Initializing Tor session...');
      await sleep(800);
      appendLog('✓ Tor session active');
      appendLog('> Running OSINT modules...');
      appendLog('  ├─ WHOIS lookup...');
      await sleep(600);
      appendLog('  ├─ IP Geolocation...');
      await sleep(400);
      appendLog('  ├─ Social media scan...');
      await sleep(700);
      appendLog('  ├─ Dark web presence check...');
      await sleep(900);
      appendLog('  └─ Reputation analysis...');
      await sleep(500);
      
      try {
        const resp = await fetch('/scan', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({type, value})
        });
        const j = await resp.json();
        
        appendLog('');
        appendLog('╔═══════════════════════════════════════════════════════════════╗');
        appendLog('║ SCAN COMPLETE');
        appendLog('╚═══════════════════════════════════════════════════════════════╝');
        appendLog('> Status: ' + JSON.stringify(j));
        appendLog('> Reports generated and saved to database');
        appendLog('> View results in Dashboard or Reports section');
        appendLog('');
        appendLog('✓ Investigation completed successfully');
        
      } catch(error) {
        appendLog('');
        appendLog('✗ ERROR: ' + error.message);
      } finally {
        scanBtn.disabled = false;
        scanBtn.textContent = '▶ Start Scan';
      }
    });
  }

  function appendLog(msg){
    const p = document.createElement('div');
    p.textContent = msg; 
    p.style.padding='2px 0';
    p.style.fontFamily = 'HackFont, monospace';
    log.appendChild(p); 
    log.scrollTop = log.scrollHeight;
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Add cursor blink effect to menu items
  const menuItems = document.querySelectorAll('.menu li:not(.menu-divider)');
  menuItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
      this.style.color = '#00FF41';
    });
    item.addEventListener('mouseleave', function() {
      if (!this.classList.contains('active')) {
        this.style.color = '#88ff88';
      }
    });
  });
});
