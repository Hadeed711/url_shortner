document.addEventListener('DOMContentLoaded', ()=>{
  const formBtn = document.getElementById('shorten-btn');
  const input = document.getElementById('url-input');
  const resultEl = document.getElementById('result');
  const toast = document.getElementById('toast');

  function showToast(msg){
    if(!toast) return;
    toast.textContent = msg; toast.style.display = 'block';
    setTimeout(()=>{ toast.style.display = 'none' }, 3000);
  }

  async function shorten(){
    const url = input.value.trim();
    if(!url){ showToast('Please enter a URL'); return }
    try{
      formBtn.disabled = true; formBtn.textContent = 'Shortening...';
      const res = await fetch('/shorten', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url})});
      const data = await res.json();
      if(data.short_url){
        resultEl.innerHTML = `
          <div class="short">
            <div style="flex:1">
              <div class="muted">Short URL</div>
              <a href="${data.short_url}" target="_blank" rel="noopener">${data.short_url}</a>
            </div>
            <div class="actions">
              <button class="btn-ghost" id="copy">Copy</button>
              <a class="btn-ghost" href="${data.short_url}" target="_blank">Open</a>
            </div>
          </div>
        `;
        const copyBtn = document.getElementById('copy');
        copyBtn.addEventListener('click', async ()=>{
          try{ await navigator.clipboard.writeText(data.short_url); showToast('Copied to clipboard') }catch(e){ showToast('Copy failed') }
        });
      } else {
        showToast(data.error || 'Unexpected error');
        resultEl.textContent = '';
      }
    }catch(e){ showToast('Network error'); }
    finally{ formBtn.disabled = false; formBtn.textContent = 'Shorten' }
  }

  document.getElementById('shorten-form').addEventListener('submit', (e)=>{ e.preventDefault(); shorten(); });
  input.addEventListener('keydown',(e)=>{ if(e.key==='Enter'){ e.preventDefault(); shorten(); } });
});
