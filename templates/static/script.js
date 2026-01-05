 function showLoading() {
    // 1. Show the spinner
    document.getElementById('loading-spinner').style.display = 'block';
    
    // 2. Disable the button so they can't click it twice
    document.getElementById('organize-btn').disabled = true;
    document.getElementById('organize-btn').innerText = 'Working...';
    document.getElementById('organize-btn').style.opacity = '0.5';
    }