function showLoading() {
    // 1. Show the entire container (Spinner + Text)
    document.getElementById('loading-spinner').style.display = 'block';
    
    // 2. Disable the button so they can't click it twice
    const btn = document.getElementById('organize-btn');
    btn.disabled = true;
    btn.innerText = 'Working...';
    btn.style.opacity = '0.5';
}