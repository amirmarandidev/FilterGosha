# pages.py

import base64
from pathlib import Path

_STATIC_IMG = Path(__file__).parent / "app" / "static" / "img" / "fg-logo.jpg"
if _STATIC_IMG.exists():
    try:
        LOGO_B64 = f"data:image/jpeg;base64,{base64.b64encode(_STATIC_IMG.read_bytes()).decode('ascii')}"
    except Exception:
        LOGO_B64 = "/static/img/fg-logo.jpg"
else:
    LOGO_B64 = "/static/img/fg-logo.jpg"

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · FilterGosha</title>
<link rel="icon" type="image/jpeg" href="/static/img/fg-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Vazirmatn',sans-serif !important}
:root{--bg:#060a14;--card:rgba(12,19,38,0.92);--accent:#10b981;--accent2:#059669;--text:#E8F4FF;--dim:#48577A;--mid:#8AA0C4;--border:rgba(16,185,129,0.2)}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--text);font-family:'Vazirmatn',sans-serif !important}
body{display:flex;align-items:center;justify-content:center;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(16,185,129,0.12),transparent 70%),var(--bg);z-index:0}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(16,185,129,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.03) 1px,transparent 1px);background-size:44px 44px;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(90px);z-index:0;animation:fl 9s ease-in-out infinite}
.o1{width:380px;height:380px;background:rgba(16,185,129,0.08);top:-100px;right:-80px}
.o2{width:280px;height:280px;background:rgba(5,150,105,0.05);bottom:-60px;left:-60px;animation-delay:4s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:400px}
.card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:38px 34px 34px;backdrop-filter:blur(24px);box-shadow:0 0 80px rgba(16,185,129,0.08),0 20px 60px rgba(0,0,0,.6)}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.brand-img{width:48px;height:48px;border-radius:50%;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 20px rgba(16,185,129,0.35);flex-shrink:0}
.brand-img img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:16px;font-weight:800;color:var(--text)}
.brand-name a{color:inherit;text-decoration:none}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px}
h1{font-size:21px;font-weight:800;color:var(--text);margin-bottom:5px;letter-spacing:-.02em}
.sub{font-size:12px;color:var(--mid);margin-bottom:24px;line-height:1.6}
.hint{display:flex;align-items:center;gap:10px;background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.18);border-radius:10px;padding:10px 14px;margin-bottom:20px}
.hint-label{font-size:11px;color:var(--mid);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--accent);background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);padding:4px 11px;border-radius:7px;cursor:pointer;transition:.15s;letter-spacing:.08em}
.hint-val:hover{background:rgba(16,185,129,0.24)}
.field{margin-bottom:18px}
.field label{display:block;font-size:10.5px;font-weight:700;color:var(--mid);margin-bottom:7px;text-transform:uppercase;letter-spacing:.06em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:13px 44px 13px 16px;border-radius:11px;border:1px solid var(--border);background:rgba(0,0,0,.35);color:var(--text);font-size:14px;outline:none;transition:.2s}
input[type=password]:focus{border-color:var(--accent);background:rgba(0,0,0,.45);box-shadow:0 0 0 3px rgba(16,185,129,0.15)}
.ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;pointer-events:none;transition:.2s}
input:focus+.ic{color:var(--accent)}
.err{display:none;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#FB8585;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:13px;border-radius:11px;border:none;cursor:pointer;background:linear-gradient(135deg,#10b981,#059669);color:#fff;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(16,185,129,.35);transition:.2s;position:relative;overflow:hidden}
.btn:hover{background:linear-gradient(135deg,#059669,#047857)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:22px;padding-top:18px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--dim)}
.footer a{color:var(--accent);font-weight:700;text-decoration:none;display:flex;align-items:center;gap:4px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg"></div><div class="grid"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-img"><img src="/static/img/fg-logo.jpg" alt="FilterGosha"></div>
      <div><div class="brand-name"><a href="https://t.me/FilterGosha" target="_blank">FilterGosha</a></div><div class="brand-sub">v1.4.13</div></div>
    </div>
    <h1>ورود به پنل مدیریت</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer">پشتیبانی <a href="https://t.me/FilterGosha" target="_blank"><i class="ti ti-brand-telegram"></i>@FilterGosha</a></div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا در ورود');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FilterGosha - مدیریت VLESS</title>
<link rel="icon" type="image/jpeg" href="/static/img/fg-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;font-family:'Vazirmatn',sans-serif !important}
:root{
  --bg:#060a14;--bg2:#0a1020;--bg3:#0d1428;
  --card:#0c1326;--card-b:rgba(16,185,129,0.14);--card-bh:rgba(16,185,129,0.3);
  --accent:#10b981;--accent2:#059669;--accent-d:rgba(16,185,129,0.1);
  --green:#10b981;--green-bg:rgba(16,185,129,0.12);--green-t:#34d399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.12);--red-t:#FB8585;
  --amber:#F2A33D;--amber-bg:rgba(242,163,61,0.12);--amber-t:#F9C988;
  --purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.12);--purple-t:#BCA4F7;
  --t1:#EFF4FF;--t2:#8AA0C4;--t3:#48577A;
  --sidebar-w:248px;--radius:16px;--shadow:0 12px 40px rgba(0,0,0,0.5);
}
/* Custom Scrollbars — تم دارک و نئون زمردی */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:rgba(6,10,20,0.7);border-radius:10px}
::-webkit-scrollbar-thumb{background:rgba(16,185,129,0.28);border-radius:10px;border:1px solid rgba(16,185,129,0.12);transition:all .2s}
::-webkit-scrollbar-thumb:hover{background:rgba(16,185,129,0.6);box-shadow:0 0 10px rgba(16,185,129,0.35)}
::-webkit-scrollbar-thumb:active{background:var(--accent)}
::-webkit-scrollbar-corner{background:transparent}
*{scrollbar-width:thin;scrollbar-color:rgba(16,185,129,0.3) rgba(6,10,20,0.7)}

html,body{min-height:100%;background:var(--bg);color:var(--t1);font-size:13.5px}
body{display:flex;overflow-x:hidden}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1)}
.logo{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:16px 14px;border-bottom:1px solid var(--card-b);position:relative}
.logo-brand{display:flex;align-items:center;gap:10px;min-width:0;flex:1}
.logo-img{width:38px;height:38px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(16,185,129,.35);flex-shrink:0}
.logo-img img{width:100%;height:100%;object-fit:cover;display:block}
.logo-text{min-width:0;flex:1}
.logo-name{font-size:14px;font-weight:800;color:var(--t1);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.logo-name a{color:inherit;text-decoration:none}
.logo-sub{font-size:9.5px;color:var(--accent);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.close-sb-btn{display:none;background:var(--card);border:1px solid var(--card-b);color:var(--t1);width:32px;height:32px;border-radius:9px;align-items:center;justify-content:center;cursor:pointer;font-size:16px;flex-shrink:0;transition:.15s}
.close-sb-btn:hover{background:var(--red-bg);color:var(--red-t);border-color:rgba(239,68,68,.3)}
.nav-wrap{flex:1;padding:12px 8px;overflow-y:auto}
.nav-sec{font-size:9px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.12em;padding:12px 10px 4px}
.nav-it{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:11px;color:var(--t2);cursor:pointer;font-size:12.5px;font-weight:600;transition:.15s;margin-bottom:2px}
.nav-it:hover{background:var(--accent-d);color:var(--accent)}
.nav-it.on{background:var(--accent-d);color:var(--accent);border:1px solid var(--card-b)}
.nav-it i{font-size:17px}
.nav-badge{margin-right:auto;background:var(--accent-d);color:var(--accent);font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:9px;font-size:12px;font-weight:700;border:1px solid rgba(239,68,68,.2);cursor:pointer;width:100%;transition:.15s}
.logout-btn:hover{background:rgba(239,68,68,.25)}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px}
.mob-logo{display:flex;align-items:center;gap:8px;font-weight:800;font-size:14px}
.menu-btn{background:var(--card);border:1px solid var(--card-b);color:var(--t1);width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:20px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:3px}
.tb-right{display:flex;align-items:center;gap:8px}
.badge{font-size:10px;font-weight:700;padding:5px 11px;border-radius:20px;display:inline-flex;align-items:center;gap:6px}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent)}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block}
.dg{background:var(--green)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes spin{to{transform:rotate(360deg)}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px 20px;box-shadow:var(--shadow);transition:.2s;min-width:0}
.metric:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.m-icon{width:36px;height:36px;border-radius:10px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:18px}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:22px;font-weight:800;color:var(--t1);line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:20px;box-shadow:var(--shadow);margin-bottom:16px;min-width:0}
.card-title{font-size:13px;font-weight:800;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 0;border-bottom:1px solid rgba(16,185,129,0.06);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px;min-width:0;flex-shrink:1}
.sr-v{font-weight:700;color:var(--t1);white-space:nowrap;flex-shrink:0}
.pg{display:none}
.pg.on{display:block}
.btn{font-size:12px;font-weight:700;border-radius:10px;padding:8px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:none;transition:all .15s;white-space:nowrap}
.btn-p{background:linear-gradient(135deg,#10b981,#059669);color:#fff;box-shadow:0 3px 14px rgba(16,185,129,.3)}
.btn-p:hover{background:linear-gradient(135deg,#059669,#047857)}
.btn-g{background:var(--accent-d);color:var(--accent);border:1px solid var(--card-b)}
.btn-g:hover{background:rgba(16,185,129,.2)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.2)}
.btn-d:hover{background:rgba(239,68,68,.25)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(242,163,61,.2)}
.btn-sm{padding:5px 11px;font-size:11px;border-radius:8px}
.btn:disabled{opacity:.42;cursor:not-allowed;box-shadow:none}
.inp{background:rgba(0,0,0,.3);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:9px 13px;font-size:12.5px;outline:none;width:100%;transition:.18s}
.inp:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-d)}
select.inp{appearance:none;cursor:pointer}
.form-g{margin-bottom:14px}
.form-g label{display:block;font-size:10.5px;font-weight:700;color:var(--t2);margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(6px);padding:20px}
.modal.open{display:flex}
.modal-box{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;width:100%;max-width:540px;box-shadow:var(--shadow);max-height:90vh;overflow-y:auto;scrollbar-gutter:stable}
.modal-box.modal-box-lg{max-width:760px}
.modal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid var(--card-b)}
.modal-title{font-size:15px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:7px}
.close-btn{background:none;border:none;color:var(--t3);cursor:pointer;font-size:20px}
.close-btn:hover{color:var(--red-t)}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:700;opacity:0;transition:all .25s;z-index:999;pointer-events:none}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.4);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.4);background:var(--red-bg);color:var(--red-t)}
.ch{position:relative;height:210px}
.tbl{width:100%;border-collapse:collapse;font-size:12px}
.tbl th{text-align:right;padding:10px 12px;color:var(--t3);font-size:10px;font-weight:700;text-transform:uppercase;border-bottom:1px solid var(--card-b)}
.tbl td{padding:12px;border-bottom:1px solid rgba(16,185,129,0.05);color:var(--t1)}
.sub-card{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px 20px;margin-bottom:14px;position:relative;overflow:visible;transition:.2s}
.sub-card:hover{border-color:var(--card-bh);box-shadow:var(--shadow)}
.icon-action-btn{width:32px;height:32px;padding:0!important;display:inline-flex;align-items:center;justify-content:center;font-size:15px;border-radius:9px;flex-shrink:0;cursor:pointer}
.action-dropdown{position:relative;display:inline-block}
.action-menu{position:absolute;top:calc(100% + 6px);left:0;min-width:160px;background:#0c1326;border:1px solid var(--card-bh);border-radius:12px;padding:6px;box-shadow:0 12px 32px rgba(0,0,0,0.65),0 0 1px rgba(16,185,129,0.3);z-index:90;display:none;opacity:0;transform:translateY(-6px);transition:opacity .15s ease,transform .15s ease}
.action-menu.open{display:block;opacity:1;transform:translateY(0)}
.action-menu-item{display:flex;align-items:center;gap:9px;width:100%;padding:8px 10px;font-size:11.5px;font-weight:600;color:var(--t1);background:none;border:none;cursor:pointer;text-align:right;border-radius:8px;transition:all .15s;white-space:nowrap}
.action-menu-item:hover{background:var(--accent-d);color:var(--accent)}
.action-menu-item i{font-size:15px;color:var(--accent);flex-shrink:0}
.action-menu-divider{height:1px;background:rgba(16,185,129,0.1);margin:4px 6px}
.sub-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.sub-label{font-size:15px;font-weight:800;color:var(--t1)}
.sub-links-box{background:rgba(0,0,0,.25);border:1px solid var(--card-b);border-radius:12px;padding:10px 12px;margin-top:10px;font-family:ui-monospace,monospace;font-size:10.5px;color:var(--accent);word-break:break-all}
.ubar{height:6px;border-radius:4px;background:rgba(16,185,129,0.1);overflow:hidden;margin-bottom:5px}
.ubar-f{height:100%;border-radius:4px;transition:width .5s ease}
.utxt{font-size:10.5px;color:var(--t3);display:flex;justify-content:space-between}
.cfg-checklist{max-height:160px;overflow-y:auto;border:1px solid var(--card-b);border-radius:10px;padding:8px 12px;background:rgba(0,0,0,.2)}
.cfg-chk-item{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:12px;color:var(--t1);cursor:pointer}
.bulk-bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:11px 16px;margin-bottom:14px;box-shadow:var(--shadow)}
.bulk-all{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:700;color:var(--t2);cursor:pointer;user-select:none}
.bulk-all:hover{color:var(--accent)}
.bulk-count{font-size:11.5px;font-weight:700;color:var(--t3)}
.bulk-count.has-sel{color:var(--accent)}
.bulk-del{margin-inline-start:auto}
.bulk-chk{width:16px;height:16px;accent-color:var(--accent);cursor:pointer;flex-shrink:0}
.bk-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:9px}
.bk-item{display:flex;align-items:flex-start;gap:9px;background:rgba(0,0,0,.22);border:1px solid var(--card-b);border-radius:12px;padding:11px 13px;cursor:pointer;transition:.16s}
.bk-item:hover{border-color:var(--card-bh);background:rgba(16,185,129,.05)}
.bk-item input{margin-top:2px}
.bk-item b{display:block;font-size:12.5px;font-weight:700;color:var(--t1);margin-bottom:3px}
.bk-item i{display:block;font-style:normal;font-size:10.5px;line-height:1.6;color:var(--t3)}
.bk-hint{margin-top:11px;font-size:11px;font-weight:600;color:var(--t2);background:rgba(0,0,0,.22);border:1px solid var(--card-b);border-radius:10px;padding:9px 12px}
.bk-hint.bk-warn{color:var(--red-t);border-color:rgba(239,68,68,.28);background:rgba(239,68,68,.07)}
.github-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:rgba(255,255,255,.06);color:#fff;border-radius:9px;padding:9px;font-size:12px;font-weight:700;border:1px solid rgba(255,255,255,.35);cursor:pointer;width:100%;text-decoration:none;margin-bottom:8px;animation:ghWhite 4.2s ease-in-out infinite;transition:transform .15s}
.github-btn i{font-size:15px}
.github-btn:hover{transform:translateY(-1px);animation-duration:1.5s}
@keyframes ghWhite{
  0%,100%{color:#ffffff;background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.30);box-shadow:0 0 8px rgba(255,255,255,.14),inset 0 0 8px rgba(255,255,255,.03);text-shadow:0 0 6px rgba(255,255,255,.30)}
  20%{color:#f0ffff;background:rgba(240,255,255,.10);border-color:rgba(240,255,255,.62);box-shadow:0 0 18px rgba(240,255,255,.40),inset 0 0 12px rgba(240,255,255,.07);text-shadow:0 0 10px rgba(240,255,255,.60)}
  40%{color:#f5fffa;background:rgba(245,255,250,.13);border-color:rgba(245,255,250,.80);box-shadow:0 0 24px rgba(245,255,250,.52),inset 0 0 14px rgba(245,255,250,.09);text-shadow:0 0 13px rgba(245,255,250,.75)}
  60%{color:#fffff0;background:rgba(255,255,240,.11);border-color:rgba(255,255,240,.66);box-shadow:0 0 20px rgba(255,255,240,.44),inset 0 0 12px rgba(255,255,240,.07);text-shadow:0 0 11px rgba(255,255,240,.62)}
  80%{color:#fff5ee;background:rgba(255,245,238,.08);border-color:rgba(255,245,238,.46);box-shadow:0 0 13px rgba(255,245,238,.26),inset 0 0 10px rgba(255,245,238,.05);text-shadow:0 0 8px rgba(255,245,238,.44)}
}
@media(prefers-reduced-motion:reduce){.github-btn{animation:none;color:#fff;border-color:rgba(255,255,255,.5);box-shadow:0 0 14px rgba(255,255,255,.25)}}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:180}
.overlay.open{display:block}
.dash-charts-grid{display:grid;grid-template-columns:1fr 2fr;gap:14px;margin-bottom:16px}
.dash-bottom-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}
.dash-chart-box{height:200px;position:relative;width:100%}
.dash-donut-box{height:200px;position:relative;display:flex;align-items:center;justify-content:center;width:100%}
.dash-footer{display:flex;justify-content:space-between;align-items:center;padding:16px 0;margin-top:20px;border-top:1px solid var(--card-b);font-size:11px;color:var(--t3);flex-wrap:wrap;gap:10px}

@media(max-width:992px){
  .metrics{grid-template-columns:repeat(2,1fr) !important;gap:12px}
  .dash-charts-grid{grid-template-columns:1fr !important}
  .dash-bottom-grid{grid-template-columns:1fr !important}
  .g2,.g3{grid-template-columns:1fr !important}
}
@media(max-width:900px){
  .main{margin-right:0;padding:68px 16px 40px}
  .sidebar{width:min(280px,85vw);transform:translateX(100%)}
  .sidebar.open{transform:translateX(0)}
  .mob-top{display:flex}
  .close-sb-btn{display:inline-flex}
  .action-menu{left:auto;right:0}
}
@media(max-width:600px){
  .topbar{flex-direction:column;align-items:stretch;gap:10px}
  .tb-right{flex-wrap:wrap;justify-content:flex-start;gap:6px}
  .metrics{gap:10px}
  .metric{padding:14px 15px;border-radius:15px}
  .m-icon{width:32px;height:32px;font-size:16px;margin-bottom:8px}
  .m-val{font-size:18px}
  .m-sub{font-size:9.5px}
  .card{padding:16px;border-radius:16px}
  .card-title{font-size:12.5px;margin-bottom:12px}
  .dash-chart-box{height:190px}
  .dash-donut-box{height:190px}
  .dash-footer{flex-direction:column;align-items:center;text-align:center;gap:6px}
}
@media(max-width:420px){
  .metrics{gap:8px}
  .metric{padding:12px 12px;border-radius:14px}
  .m-val{font-size:17px}
  .sr{font-size:11px;padding:8px 0}
  .dash-chart-box{height:180px}
  .dash-donut-box{height:180px}
}
@media(max-width:380px){
  .metrics{grid-template-columns:1fr !important}
  .main{padding:64px 10px 32px}
  .card{padding:13px;border-radius:14px}
  .tb-title{font-size:18px}
  .badge{padding:4px 8px;font-size:9.5px}
}
@media(max-width:340px){
  .main{padding:60px 8px 24px}
  .sr{font-size:10px;padding:7px 0;gap:4px}
  .sr-k{font-size:10px}
  .tb-right{gap:4px}
  .btn-sm{padding:4px 7px;font-size:10px}
}
</style>
</head>
<body>
<div class="mob-top">
  <div class="mob-logo">
    <div class="logo-img" style="width:28px;height:28px"><img src="/static/img/fg-logo.jpg" alt="FilterGosha"></div>
    <a href="https://t.me/FilterGosha" target="_blank" style="color:inherit;text-decoration:none;">FilterGosha</a>
  </div>
  <button class="menu-btn" id="open-sb" title="باز کردن منو"><i class="ti ti-menu-2"></i></button>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <div class="logo">
    <div class="logo-brand">
      <div class="logo-img"><img src="/static/img/fg-logo.jpg" alt="FilterGosha"></div>
      <div class="logo-text">
        <div class="logo-name"><a href="https://t.me/FilterGosha" target="_blank">FilterGosha</a></div>
        <div class="logo-sub">v1.4.13 · gRPC / WS / XHTTP</div>
      </div>
    </div>
    <button class="menu-btn close-sb-btn" id="close-sb" title="بستن منو"><i class="ti ti-x"></i></button>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">پنل</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-it" data-pg="subs"><i class="ti ti-users-group"></i> اشتراک‌ها <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-sec">سیستم</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-brand-cloudflare"></i> تنظیمات وورکر</div>
    <div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
  </div>
  <div class="sb-foot">
    <a class="github-btn" href="https://github.com/amirmarandidev/FilterGosha" target="_blank" rel="noopener noreferrer"><i class="ti ti-brand-github"></i> صفحه گیت‌هاب پروژه</a>
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج از پنل</button>
  </div>
</aside>

<main class="main">

<!-- PAGE 1: OVERVIEW -->
<section class="pg on" id="pg-overview">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-grid"></i> داشبورد</div><div class="tb-sub" id="last-upd">آخرین بروزرسانی: --:--:--</div></div>
    <div class="tb-right">
      <button class="btn btn-g btn-sm" onclick="fetchStats()"><i class="ti ti-refresh"></i> رفرش</button>
      <span class="badge bg-blue" id="uptime-badge">Railway - 00:00:00</span>
      <span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span>
    </div>
  </div>

  <div class="metrics">
    <div class="metric"><div class="m-icon" style="background:rgba(239,68,68,0.12);color:#EF4444"><i class="ti ti-alert-triangle"></i></div><div class="m-label">خطاها</div><div class="m-val" id="m-errors" style="color:#EF4444">0</div><div class="m-sub">از راه‌اندازی</div></div>
    <div class="metric"><div class="m-icon" style="background:rgba(16,185,129,0.12);color:#34D399"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">0</div><div class="m-sub" id="m-lsub">از 0 کانفیگ</div></div>
    <div class="metric"><div class="m-icon" style="background:rgba(59,130,246,0.12);color:#60A5FA"><i class="ti ti-bolt"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">0.0 MB</div><div class="m-sub">از راه‌اندازی</div></div>
    <div class="metric"><div class="m-icon" style="background:rgba(16,185,129,0.12);color:var(--accent)"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">0</div><div class="m-sub"><span class="dot dg pulse"></span> WebSocket / XHTTP زنده</div></div>
  </div>

  <div class="dash-charts-grid">
    <div class="card" style="display:flex;flex-direction:column;justify-content:space-between">
      <div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div>
      <div class="dash-donut-box">
        <canvas id="ch-donut"></canvas>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-chart-area-line"></i> ترافیک ساعتی (MB)</div>
      <div class="dash-chart-box"><canvas id="ch1"></canvas></div>
    </div>
  </div>

  <div class="dash-bottom-grid">
    <div class="card">
      <div class="card-title"><i class="ti ti-list-details"></i> خلاصه کانفیگ‌ها</div>
      <div id="dash-links-summary" style="display:flex;flex-direction:column;gap:10px;margin-top:8px">
        در حال بارگذاری...
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div>
      <div style="display:flex;flex-direction:column;gap:12px;margin-top:10px">
        <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال - سخت‌گیرانه</span></div>
        <div class="sr"><span class="sr-k"><i class="ti ti-wifi"></i> VLESS / WS Tunnel</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
        <div class="sr"><span class="sr-k"><i class="ti ti-bolt"></i> Siz10a XHTTP Ultra</span><span class="sr-v" style="color:var(--green-t)">mode: auto · ● فعال</span></div>
        <div class="sr"><span class="sr-k"><i class="ti ti-rss"></i> Subscription API</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
        <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline" style="color:var(--t1)">—</span></div>
        <div class="sr"><span class="sr-k"><i class="ti ti-cpu"></i> بار نسبی</span><span class="sr-v" style="color:var(--green-t)">0%</span></div>
      </div>
    </div>
  </div>

  <!-- DASHBOARD FOOTER -->
  <div class="dash-footer">
    <div><a href="https://t.me/FilterGosha" target="_blank" style="color:var(--accent2);text-decoration:none"><i class="ti ti-brand-telegram"></i> t.me/FilterGosha</a></div>
    <div>FilterGosha v1.4.13 · Railway</div>
  </div>
</section>

<!-- PAGE 2: SUBSCRIPTIONS -->
<section class="pg" id="pg-subs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-users-group"></i> مدیریت اشتراک‌ها</div><div class="tb-sub">مدیریت والد برای کانفیگ‌ها، سهمیه حجم، زمان و محدودیت آی‌پی</div></div>
    <div class="tb-right">
      <button class="btn btn-p" onclick="openSubModal()"><i class="ti ti-plus"></i> اشتراک جدید</button>
      <button class="btn btn-g" onclick="loadSubs()"><i class="ti ti-refresh"></i></button>
    </div>
  </div>
  <div class="bulk-bar" id="subs-bulk-bar" style="display:none">
    <label class="bulk-all"><input type="checkbox" class="bulk-chk" id="subs-chk-all" onchange="toggleSelectAll('subs', this.checked)"> انتخاب همه</label>
    <span class="bulk-count" id="subs-bulk-count">هیچ اشتراکی انتخاب نشده</span>
    <button class="btn btn-d btn-sm bulk-del" id="subs-bulk-del" onclick="bulkDelete('subs')" disabled><i class="ti ti-trash"></i> حذف گروهی اشتراک‌ها</button>
  </div>
  <div id="subs-list">
    <div style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:24px"></i><br>در حال بارگذاری اشتراک‌ها...</div>
  </div>
</section>

<!-- PAGE 3: LINKS -->
<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link"></i> مدیریت کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ‌های VLESS (gRPC / WS / XHTTP)</div></div>
    <div class="tb-right">
      <button class="btn btn-p" onclick="openLinkModal()"><i class="ti ti-plus"></i> کانفیگ جدید</button>
      <button class="btn btn-g" onclick="loadLinks()"><i class="ti ti-refresh"></i></button>
    </div>
  </div>
  <div class="bulk-bar" id="links-bulk-bar" style="display:none">
    <label class="bulk-all"><input type="checkbox" class="bulk-chk" id="links-chk-all" onchange="toggleSelectAll('links', this.checked)"> انتخاب همه</label>
    <span class="bulk-count" id="links-bulk-count">هیچ کانفیگی انتخاب نشده</span>
    <button class="btn btn-d btn-sm bulk-del" id="links-bulk-del" onclick="bulkDelete('links')" disabled><i class="ti ti-trash"></i> حذف گروهی کانفیگ‌ها</button>
  </div>
  <div id="links-list">
    <div style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:24px"></i><br>در حال بارگذاری کانفیگ‌ها...</div>
  </div>
</section>

<!-- PAGE 4: CONNECTIONS -->
<section class="pg" id="pg-connections">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات زنده</div><div class="tb-sub">لیست اتصالات فعال کلاینت‌ها</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="loadConns()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="card"><div id="conns-table">در حال بارگذاری...</div></div>
</section>

<!-- PAGE: SETTINGS (CLOUDFLARE WORKER) -->
<section class="pg" id="pg-settings">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-brand-cloudflare"></i> تنظیمات Cloudflare Worker (DPI Bypass)</div><div class="tb-sub">عبور از اختلال اینترنت ایرانسل و رایتل با پروکسی معکوس کلادفلر</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="loadSettings()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>

  <div class="card" style="margin-bottom:16px">
    <div class="card-title"><i class="ti ti-settings"></i> تنظیمات سراسری پنل، دامنه وورکر و پیشوند ریمارک</div>
    <form id="form-settings">
      <div class="form-g">
        <label>پیشوند نام کانفیگ (Remark Prefix)</label>
        <input class="inp" id="st-remark-prefix" placeholder="مثلاً: FilterGosha یا MyBrand (پیش‌فرض: FilterGosha)">
        <div style="font-size:10.5px;color:var(--t3);margin-top:4px">عبارتی که ابتدای ریمارک تمام لینک‌های VLESS قرار می‌گیرد (مثلاً: FilterGosha-VLESS-1).</div>
      </div>
      <div class="form-g">
        <label>دامنه وورکر کلادفلر (WORKER_DOMAIN)</label>
        <input class="inp" id="st-worker-domain" placeholder="مثلاً: worker.mydomain.com یا filtergosha-proxy.sub.workers.dev">
        <div style="font-size:10.5px;color:var(--t3);margin-top:4px">دامنه اختصاصی یا زیردامنه وورکر کلادفلر که کلاینت‌ها به آن متصل می‌شوند.</div>
      </div>
      <div class="form-g">
        <label>آی‌پی تمیز کلادفلر (CLEAN_IP - اختیاری)</label>
        <input class="inp" id="st-clean-ip" placeholder="مثلاً: 104.21.x.x (در صورت خالی بودن، از خود دامنه وورکر استفاده می‌شود)">
        <div style="font-size:10.5px;color:var(--t3);margin-top:4px">آی‌پی تمیز کلادفلر جهت درج در فیلد address لینک‌های VLESS کلاینت.</div>
      </div>
      <button class="btn btn-p" type="submit" style="margin-top:10px"><i class="ti ti-check"></i> ذخیره تنظیمات عمومی</button>
    </form>
  </div>

  <div class="card" style="margin-top:16px">
    <div class="card-title"><i class="ti ti-lock"></i> تغییر رمز عبور مدیریت پنل</div>
    <form id="form-change-pw">
      <div class="form-g">
        <label>رمز عبور فعلی</label>
        <input class="inp" type="password" id="cpw-current" placeholder="رمز فعلی ورود به پنل" required>
      </div>
      <div class="form-row">
        <div class="form-g">
          <label>رمز عبور جدید</label>
          <input class="inp" type="password" id="cpw-new" placeholder="حداقل ۴ کاراکتر" required>
        </div>
        <div class="form-g">
          <label>تکرار رمز عبور جدید</label>
          <input class="inp" type="password" id="cpw-confirm" placeholder="تکرار رمز جدید" required>
        </div>
      </div>
      <button class="btn btn-p" type="submit" style="margin-top:8px"><i class="ti ti-key"></i> بروزرسانی رمز عبور</button>
    </form>
  </div>

  <div class="card" style="margin-top:16px">
    <div class="card-title"><i class="ti ti-database"></i> بک‌آپ و بازیابی دیتابیس (SQLite)</div>
    <div style="font-size:12px;color:var(--t3);margin-bottom:12px">
      بخش‌هایی که می‌خواهید در فایل بک‌آپ باشند را تیک بزنید. فایل <code>.db</code> خروجی <b>تنها</b> شامل موارد انتخاب‌شده است
      و ساختار جداول آن دقیقاً مانند دیتابیس پنل است، پس در هر پنل FilterGosha دیگری بدون خطا قابل بازیابی است.
    </div>
    <div class="bk-list">
      <label class="bk-item">
        <input type="checkbox" class="bulk-chk bk-chk" value="links" checked onchange="syncBackupSelection()">
        <span><b>کانفیگ‌ها</b><i>همه‌ی کانفیگ‌ها با پروتکل، پورت، SNI، محدودیت حجم/سرعت/آی‌پی و تاریخ انقضا</i></span>
      </label>
      <label class="bk-item">
        <input type="checkbox" class="bulk-chk bk-chk" value="subs" checked onchange="syncBackupSelection()">
        <span><b>اشتراک‌ها</b><i>اشتراک‌ها، نام کاربری، محدودیت‌ها و فهرست کانفیگ‌های متصل به هر اشتراک</i></span>
      </label>
      <label class="bk-item">
        <input type="checkbox" class="bulk-chk bk-chk" value="settings" checked onchange="syncBackupSelection()">
        <span><b>تنظیمات عمومی پنل</b><i>دامنه وورکر، آی‌پی تمیز و پیشوند ریمارک</i></span>
      </label>
      <label class="bk-item">
        <input type="checkbox" class="bulk-chk bk-chk" value="usage" checked onchange="syncBackupSelection()">
        <span><b>آمار مصرف کاربران</b><i>مقدار حجم مصرف‌شده؛ در صورت غیرفعال بودن، مصرف همه در فایل صفر ذخیره می‌شود</i></span>
      </label>
      <label class="bk-item">
        <input type="checkbox" class="bulk-chk bk-chk" value="auth" onchange="syncBackupSelection()">
        <span><b>رمز عبور مدیریت پنل</b><i>هش رمز ورود؛ فقط اگر می‌خواهید پنل مقصد با همین رمز باز شود تیک بزنید</i></span>
      </label>
    </div>
    <div class="bk-hint" id="bk-hint"></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">
        <button class="btn btn-p" type="button" id="bk-export-btn" onclick="exportBackup()"><i class="ti ti-download"></i> دانلود بک‌آپ (.db)</button>
        <button class="btn btn-g" type="button" onclick="document.getElementById('import-db-file').click()"><i class="ti ti-upload"></i> آپلود و بازیابی (.db)</button>
        <input type="file" id="import-db-file" accept=".db" style="display:none" onchange="handleImportDB(this.files[0])">
    </div>
  </div>

  <div class="card">
    <div class="card-title" style="display:flex;justify-content:space-between;align-items:center">
      <span><i class="ti ti-code"></i> اسکریپت Cloudflare Worker (Reverse Proxy)</span>
      <button class="btn btn-sm btn-g" onclick="copyWorkerScript()"><i class="ti ti-copy"></i> کپی کد Worker</button>
    </div>
    <div style="font-size:11px;color:var(--t2);margin-bottom:10px">
      این کد را کپی کرده و در پنل کلادفلر (بخش Workers & Pages -> Create Worker) قرار داده و Deploy کنید.
    </div>
    <textarea id="worker-code-box" readonly style="width:100%;height:180px;background:rgba(0,0,0,0.4);border:1px solid var(--card-b);color:var(--accent);font-family:ui-monospace,monospace;font-size:11px;padding:12px;border-radius:10px;outline:none;resize:vertical"></textarea>
  </div>

  <div class="card" style="margin-top:16px">
    <div class="card-title" style="display:flex;justify-content:space-between;align-items:center">
      <span><i class="ti ti-brand-cloudflare"></i> اسکریپت Cloudflare Pages Function (جایگزین pages.dev)</span>
      <button class="btn btn-sm btn-g" onclick="copyPagesScript()"><i class="ti ti-copy"></i> کپی کد Pages</button>
    </div>
    <div style="font-size:11px;color:var(--t2);margin-bottom:10px">
      در صورتی که دامنه <code>workers.dev</code> فیلتر یا مسدود است، یک پروسه Cloudflare Pages بسازید و این کد را در مسیر <code>functions/[[path]].js</code> قرار دهید تا دامنه <code>your-app.pages.dev</code> فعال شود.
    </div>
    <textarea id="pages-code-box" readonly style="width:100%;height:180px;background:rgba(0,0,0,0.4);border:1px solid var(--card-b);color:var(--accent);font-family:ui-monospace,monospace;font-size:11px;padding:12px;border-radius:10px;outline:none;resize:vertical"></textarea>
  </div>
</section>

<!-- PAGE 5: LOGS -->
<section class="pg" id="pg-logs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div><div class="tb-sub">تاریخچه رخدادهای سیستم و پنل</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="loadActivity()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="card"><div id="logs-list">در حال دریافت لاگ‌ها...</div></div>
</section>

<!-- PAGE 6: ERRORS -->
<section class="pg" id="pg-errors">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div><div class="tb-sub">آخرین خطاهای شبکه و اتصالات</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="fetchStats()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="card"><div id="errs-full">هیچ خطایی ثبت نشده است.</div></div>
</section>

</main>

<!-- MODAL: SUBSCRIPTION -->
<div class="modal" id="modal-sub">
  <div class="modal-box">
    <div class="modal-head">
      <div class="modal-title" id="sub-modal-title"><i class="ti ti-users-group"></i> ساخت اشتراک جدید</div>
      <button class="close-btn" onclick="closeModal('modal-sub')"><i class="ti ti-x"></i></button>
    </div>
    <form id="form-sub">
      <div class="form-g"><label>عنوان اشتراک</label><input class="inp" id="sub-label" placeholder="مثلاً: اشتراک VIP کاربر ۱" required></div>
      <div class="form-row">
        <div class="form-g"><label>حجم کل (0 = نامحدود)</label><input class="inp" type="number" step="0.1" id="sub-limit-val" value="0"></div>
        <div class="form-g"><label>واحد حجم</label><select class="inp" id="sub-limit-unit"><option value="GB">گیگابایت (GB)</option><option value="MB">مگابایت (MB)</option></select></div>
      </div>
      <div class="form-row">
        <div class="form-g"><label>محدودیت آی‌پی همزمان (0 = نامحدود)</label><input class="inp" type="number" id="sub-iplimit" value="0"></div>
        <div class="form-g"><label>محدودیت سرعت (0 = نامحدود)</label><input class="inp" type="number" step="0.1" id="sub-speed-val" value="0"></div>
      </div>
      <div class="form-row">
        <div class="form-g">
          <label>محدودیت تعداد دستگاه / HWID (0 = نامحدود)</label>
          <input class="inp" type="number" id="sub-hwidlimit" value="0">
          <div style="font-size:10px;color:var(--t3);margin-top:4px" id="sub-hwid-info">
            اولین دستگاه‌هایی که وصل شوند قفل می‌شوند؛ دستگاه جدید بعد از پر شدن سقف رد می‌شود. شناسه از روی User-Agent کلاینت یا هدر X-HWID ساخته می‌شود (روی WS/gRPC/XHTTP/Trojan؛ SOCKS5 معاف است).
          </div>
        </div>
      </div>
      <div class="form-row">
        <div class="form-g"><label>واحد سرعت</label><select class="inp" id="sub-speed-unit"><option value="MBIT">مگابیت/ثانیه (Mbps)</option><option value="KB">کیلوبایت/ثانیه (KB/s)</option></select></div>
        <div class="form-g"><label>توضیحات / یادداشت</label><input class="inp" id="sub-note" placeholder="توضیحات اختیاری..."></div>
      </div>
      <div class="form-g" style="background:rgba(255,255,255,0.02);border:1px solid var(--card-b);padding:12px;border-radius:12px;margin-bottom:12px">
        <label style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
          <span><i class="ti ti-calendar-time" style="color:var(--accent)"></i> تاریخ و زمان انقضا</span>
          <span id="sub-exp-shamsi" style="font-size:11px;color:var(--accent);font-weight:600">نامحدود (بدون انقضا)</span>
        </label>
        <input class="inp" type="datetime-local" id="sub-exp-date" onchange="updateExpShamsi('sub')" oninput="updateExpShamsi('sub')">
        <div style="display:flex;gap:5px;margin-top:8px;flex-wrap:wrap">
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 0)">نامحدود</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 7)">۷ روزه</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 30)">۱ ماهه (۳۰ روز)</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 60)">۲ ماهه (۶۰ روز)</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 90)">۳ ماهه (۹۰ روز)</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 180)">۶ ماهه</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('sub', 365)">۱ ساله</button>
        </div>
      </div>
      <div class="form-g">
        <label>اتصال کانفیگ‌ها به این اشتراک</label>
        <div class="cfg-checklist" id="sub-links-checklist">در حال بارگذاری لیست کانفیگ‌ها...</div>
      </div>
      <button class="btn btn-p" type="submit" style="width:100%;margin-top:14px;justify-content:center"><i class="ti ti-check"></i> ذخیره اشتراک</button>
    </form>
  </div>
</div>

<!-- MODAL: LINK -->
<div class="modal" id="modal-link">
  <div class="modal-box modal-box-lg" style="max-width:760px">
    <div class="modal-head">
      <div class="modal-title" id="link-modal-title"><i class="ti ti-link"></i> ساخت کانفیگ جدید</div>
      <button class="close-btn" onclick="closeModal('modal-link')"><i class="ti ti-x"></i></button>
    </div>
    <form id="form-link">
      <div class="form-g"><label>عنوان کانفیگ</label><input class="inp" id="nl-label" placeholder="مثلاً: کاربر ۱ - وب‌سوکت" required></div>

      <!-- PROTOCOL SELECTOR CARDS -->
      <div class="form-g">
        <label style="margin-bottom:10px;display:flex;align-items:center;justify-content:space-between">
          <span><i class="ti ti-layers-linked" style="color:var(--accent)"></i> انتخاب پروتکل / ترابرد (Transport)</span>
          <span style="font-size:10.5px;color:var(--t3);font-weight:500">پروتکل مورد نظر را انتخاب کنید</span>
        </label>
        <div class="proto-grid" id="proto-cards">
          <!-- 1. WebSocket -->
          <div class="proto-card active" data-proto="vless-ws" onclick="selectProto('vless-ws')">
            <div class="proto-card-top">
              <div class="proto-icon-wrap"><i class="ti ti-wifi"></i></div>
              <div class="proto-info">
                <div class="proto-title">WebSocket</div>
                <div class="proto-sub">VLESS over WS</div>
              </div>
              <div class="proto-radio"><i class="ti ti-check"></i></div>
            </div>
            <div class="proto-tags">
              <span class="proto-tag">ALPN: http/1.1</span>
              <span class="proto-tag proto-tag-accent">✓ Worker</span>
            </div>
          </div>

          <!-- 2. gRPC -->
          <div class="proto-card" data-proto="vless-grpc" onclick="selectProto('vless-grpc')">
            <div class="proto-card-top">
              <div class="proto-icon-wrap"><i class="ti ti-route"></i></div>
              <div class="proto-info">
                <div class="proto-title">gRPC</div>
                <div class="proto-sub">VLESS over gRPC</div>
              </div>
              <div class="proto-radio"><i class="ti ti-check"></i></div>
            </div>
            <div class="proto-tags">
              <span class="proto-tag">ALPN: h2</span>
              <span class="proto-tag">Multiplexing</span>
            </div>
          </div>

          <!-- 3. XHTTP -->
          <div class="proto-card" data-proto="xhttp" onclick="selectProto('xhttp')">
            <div class="proto-card-top">
              <div class="proto-icon-wrap"><i class="ti ti-bolt"></i></div>
              <div class="proto-info">
                <div class="proto-title">XHTTP</div>
                <div class="proto-sub">SplitHTTP Auto</div>
              </div>
              <div class="proto-radio"><i class="ti ti-check"></i></div>
            </div>
            <div class="proto-tags">
              <span class="proto-tag">ALPN: http/1.1</span>
              <span class="proto-tag proto-tag-accent">✓ Mode: auto</span>
            </div>
          </div>

          <!-- 4. Trojan -->
          <div class="proto-card" data-proto="trojan-ws" onclick="selectProto('trojan-ws')">
            <div class="proto-card-top">
              <div class="proto-icon-wrap"><i class="ti ti-horse"></i></div>
              <div class="proto-info">
                <div class="proto-title">Trojan</div>
                <div class="proto-sub">over WebSocket</div>
              </div>
              <div class="proto-radio"><i class="ti ti-check"></i></div>
            </div>
            <div class="proto-tags">
              <span class="proto-tag">ALPN: http/1.1</span>
              <span class="proto-tag proto-tag-accent">✓ Worker</span>
            </div>
          </div>

          <!-- 5. SOCKS5 -->
          <div class="proto-card" data-proto="socks5" onclick="selectProto('socks5')">
            <div class="proto-card-top">
              <div class="proto-icon-wrap"><i class="ti ti-shield-lock"></i></div>
              <div class="proto-info">
                <div class="proto-title">SOCKS5</div>
                <div class="proto-sub">Direct TCP Proxy</div>
              </div>
              <div class="proto-radio"><i class="ti ti-check"></i></div>
            </div>
            <div class="proto-tags">
              <span class="proto-tag">Direct TCP</span>
              <span class="proto-tag">User / Pass</span>
            </div>
          </div>

          <!-- 6. Custom -->
          <div class="proto-card" data-proto="custom" onclick="selectProto('custom')">
            <div class="proto-card-top">
              <div class="proto-icon-wrap"><i class="ti ti-code"></i></div>
              <div class="proto-info">
                <div class="proto-title">کاستوم</div>
                <div class="proto-sub">SOCKS / Proxy خارجی</div>
              </div>
              <div class="proto-radio"><i class="ti ti-check"></i></div>
            </div>
            <div class="proto-tags">
              <span class="proto-tag">URI اختصاصی</span>
              <span class="proto-tag proto-tag-accent">لینک دلخواه</span>
            </div>
          </div>
        </div>
        <input type="hidden" id="nl-proto" value="vless-ws">
      </div>

      <!-- PROTOCOL INFO BOX -->
      <div id="proto-info-box" style="padding:10px 14px;border-radius:10px;font-size:11px;margin-bottom:12px;border:1px solid var(--card-b);background:rgba(0,0,0,0.15)">
        <div id="proto-info-ws" class="proto-info-item">
          <b><i class="ti ti-info-circle"></i> WebSocket:</b> بهترین گزینه برای عبور از Cloudflare Worker. ترافیک از طریق HTTP/1.1 Upgrade انتقال می‌یابد.<br>
          <span style="color:var(--t3)">• ALPN ثابت: <code>http/1.1</code> • Mux: پشتیبانی نمی‌شود • Fragment: قابل فعال‌سازی</span>
        </div>
        <div id="proto-info-grpc" class="proto-info-item" style="display:none">
          <b><i class="ti ti-info-circle"></i> gRPC:</b> از HTTP/2 استفاده می‌کند و Multiplexing داخلی دارد. نیاز به فعال‌سازی gRPC در Cloudflare.<br>
          <span style="color:var(--t3)">• ALPN ثابت: <code>h2</code> • Mux: داخلی (نیاز به تنظیم ندارد) • Fragment: قابل فعال‌سازی</span>
        </div>
                <div id="proto-info-socks5" class="proto-info-item" style="display:none">
          <b><i class="ti ti-info-circle"></i> SOCKS5:</b> یک پروکسی خام و مستقیم. مناسب برای وارد کردن دستی در تلگرام، نرم‌افزارها و تنظیمات ویندوز.
        </div>
          <div id="proto-info-xhttp" class="proto-info-item" style="display:none">
          <b><i class="ti ti-info-circle"></i> XHTTP:</b> پروتکل پیشرفته با حالت انتقال خودکار (auto mode). سازگار با Worker.<br>
          <span style="color:var(--t3)">• ALPN ثابت: <code>http/1.1</code> • Mux: پشتیبانی نمی‌شود • Fragment: قابل فعال‌سازی</span>
        </div>
        <div id="proto-info-trojan" class="proto-info-item" style="display:none">
          <b><i class="ti ti-info-circle"></i> Trojan:</b> پروتکل Trojan روی WebSocket؛ سازگار با Cloudflare Worker و همان مدل TLS در لبه. رمز عبور برابر نام‌کاربری اشتراک است.<br>
          <span style="color:var(--t3)">• ALPN ثابت: <code>http/1.1</code> • Mux: پشتیبانی نمی‌شود • Fragment: قابل فعال‌سازی</span>
        </div>
        <div id="proto-info-custom" class="proto-info-item" style="display:none">
          <b><i class="ti ti-info-circle"></i> کاستوم / SOCKS5 / پروکسی خارجی:</b> امکان تعریف مستقیم لینک‌های کاستوم (مانند <code>socks://...</code> یا <code>vless://...</code>) جهت اتصال به پروژه‌ها یا سرورهای خارجی و افزودن آن‌ها به اشتراک‌ها.<br>
          <span style="color:var(--t3)">• پشتیبانی از متغيرهای <code>{host}</code> و <code>{uuid}</code></span>
        </div>
      </div>

      <!-- CUSTOM URI FIELD (Visible when custom protocol selected) -->
      <div class="form-g" id="row-custom-uri" style="display:none">
        <label>لینک کاستوم / URI اختصاصی</label>
        <input class="inp" id="nl-custom-uri" placeholder="مثلاً: socks://user:pass@{host}:1081#MyCustomProxy">
        <div style="font-size:10px;color:var(--t3);margin-top:4px">لینک کاملی که کلاینت دریافت خواهد کرد. امکان استفاده از <code>{host}</code> وجود دارد.</div>
      </div>


      <div class="form-row">
        <div class="form-g"><label>حجم (0 = نامحدود)</label><input class="inp" type="number" step="0.1" id="nl-val" value="0"></div>
        <div class="form-g"><label>واحد حجم</label><select class="inp" id="nl-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div>
      </div>
      <div class="form-row">
        <div class="form-g"><label>محدودیت آی‌پی (0 = نامحدود)</label><input class="inp" type="number" id="nl-iplimit" value="0"></div>
        <div class="form-g"><label>توضیحات</label><input class="inp" id="nl-note" placeholder="توضیحات اختیاری..."></div>
      </div>
      <div class="form-g" style="background:rgba(255,255,255,0.02);border:1px solid var(--card-b);padding:12px;border-radius:12px;margin-bottom:12px">
        <label style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
          <span><i class="ti ti-calendar-time" style="color:var(--accent)"></i> تاریخ و زمان انقضا</span>
          <span id="nl-exp-shamsi" style="font-size:11px;color:var(--accent);font-weight:600">نامحدود (بدون انقضا)</span>
        </label>
        <input class="inp" type="datetime-local" id="nl-exp-date" onchange="updateExpShamsi('nl')" oninput="updateExpShamsi('nl')">
        <div style="display:flex;gap:5px;margin-top:8px;flex-wrap:wrap">
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 0)">نامحدود</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 7)">۷ روزه</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 30)">۱ ماهه (۳۰ روز)</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 60)">۲ ماهه (۶۰ روز)</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 90)">۳ ماهه (۹۰ روز)</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 180)">۶ ماهه</button>
          <button type="button" class="btn btn-sm btn-g" onclick="setExpPreset('nl', 365)">۱ ساله</button>
        </div>
      </div>

      <!-- ADVANCED SETTINGS - PROTOCOL AWARE -->
      <div id="adv-settings-wrapper" style="margin-top:14px;border-top:1px dashed var(--card-b);padding-top:10px">
        <button type="button" class="btn btn-sm btn-g" onclick="const b=document.getElementById('adv-settings-box');b.style.display=b.style.display==='none'?'block':'none'" style="width:100%;justify-content:space-between">
          <span><i class="ti ti-adjustments"></i> تنظیمات شبکه و ضد فیلترینگ</span>
          <i class="ti ti-chevron-down"></i>
        </button>
        <div id="adv-settings-box" style="display:none;margin-top:12px;padding:14px;background:rgba(0,0,0,0.25);border:1px solid var(--card-b);border-radius:14px">
          <div style="font-weight:700;font-size:11px;color:var(--accent2);margin-bottom:8px"><i class="ti ti-network"></i> تنظیمات شبکه (اختصاصی این کانفیگ)</div>
          <div class="form-row">
            <div class="form-g"><label>آی‌پی تمیز (Clean IP)</label><input class="inp" id="nl-clean-ip" placeholder="خالی = استفاده از تنظیمات سراسری وورکر"></div>
            <div class="form-g"><label>SNI اختصاصی</label><input class="inp" id="nl-sni" placeholder="خالی = دامین سرور یا وورکر"></div>
          </div>
          <div class="form-row" id="row-host-header">
            <div class="form-g"><label>Host Header اختصاصی</label><input class="inp" id="nl-host" placeholder="خالی = دامین سرور یا وورکر"></div>
            <div class="form-g">
              <label>انتخاب ALPN</label>
              <select class="inp" id="nl-alpn">
                <option value="http/1.1">http/1.1 (پیش‌فرض WebSocket & XHTTP)</option>
                <option value="h2">h2 (پیش‌فرض gRPC / HTTP/2)</option>
                <option value="h2,http/1.1">h2,http/1.1 (ترکیبی gRPC)</option>
                <option value="http/1.1,h2">http/1.1,h2 (ترکیبی HTTP)</option>
              </select>
            </div>
          </div>

          <div style="font-weight:700;font-size:11px;color:var(--accent2);margin:12px 0 6px"><i class="ti ti-scissors"></i> تنظیمات Fragment (ضد فیلترینگ / Anti-DPI)</div>
          <div style="font-size:10px;color:var(--t3);margin-bottom:8px">فعال‌سازی Fragment باعث شکستن بسته‌های TLS Hello و دور زدن فیلترینگ DPI می‌شود.</div>
          <div class="form-row">
            <div class="form-g">
              <label>نوع پکت Fragment</label>
              <select class="inp" id="nl-fg-packets">
                <option value="">غیرفعال (بدون Fragment)</option>
                <option value="tlshello" selected>tlshello (شکستن پکت‌های TLS ClientHello)</option>
                <option value="1-3">1-3 (شکستن پکت‌های اول تا سوم)</option>
                <option value="1-5">1-5 (شکستن پکت‌های اول تا پنجم)</option>
                <option value="tlshello,1-3">tlshello,1-3 (ترکیبی - بیشترین ضد فیلتر)</option>
              </select>
            </div>
            <div class="form-g"><label>طول Fragment (Length)</label><input class="inp" id="nl-fg-len" value="" placeholder="10-20"></div>
          </div>
          <div class="form-g"><label>فاصله زمانی Fragment (Interval)</label><input class="inp" id="nl-fg-interval" value="" placeholder="10-20"></div>

          <!-- MUX SECTION (hidden - not supported) -->
          <input type="hidden" id="nl-mux-enable" value="">
          <input type="hidden" id="nl-mux-concurrency" value="8">
        </div>
      </div>

      <button class="btn btn-p" type="submit" style="width:100%;margin-top:14px;justify-content:center"><i class="ti ti-check"></i> ذخیره کانفیگ</button>
    </form>
  </div>
</div>

<style>
.proto-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 4px;
}
@media (max-width: 680px) {
  .proto-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
}
@media (max-width: 400px) {
  .proto-grid {
    grid-template-columns: 1fr;
    gap: 7px;
  }
}
.proto-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12px 13px;
  border-radius: 14px;
  cursor: pointer;
  transition: all .2s cubic-bezier(.4, 0, .2, 1);
  border: 1.5px solid var(--card-b);
  background: rgba(10, 16, 32, 0.45);
  text-align: right;
  position: relative;
  user-select: none;
  min-height: 84px;
  gap: 10px;
}
.proto-card:hover {
  border-color: rgba(16, 185, 129, 0.4);
  background: rgba(16, 185, 129, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
}
.proto-card.active {
  border-color: var(--accent);
  background: linear-gradient(145deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.04));
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.16), inset 0 0 12px rgba(16, 185, 129, 0.04);
}
.proto-card-top {
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
}
.proto-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--card-b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: var(--accent);
  flex-shrink: 0;
  transition: .2s;
}
.proto-card.active .proto-icon-wrap {
  background: var(--accent-d);
  border-color: rgba(16, 185, 129, 0.35);
  color: #34d399;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
}
.proto-info {
  flex: 1;
  min-width: 0;
}
.proto-title {
  font-size: 13px;
  font-weight: 800;
  color: var(--t1);
  line-height: 1.25;
}
.proto-sub {
  font-size: 9.5px;
  color: var(--t3);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.proto-radio {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1.5px solid var(--card-b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: transparent;
  flex-shrink: 0;
  transition: .2s;
}
.proto-card.active .proto-radio {
  border-color: var(--accent);
  background: var(--accent);
  color: #fff;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
}
.proto-tags {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
}
.proto-tag {
  font-size: 9px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--t2);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.proto-tag-accent {
  background: rgba(16, 185, 129, 0.1);
  color: var(--green-t);
  border-color: rgba(16, 185, 129, 0.2);
}
</style>

<!-- MODAL: QR CODE -->
<div class="modal" id="modal-qr" onclick="this.classList.remove('open')">
  <div style="background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;text-align:center;max-width:320px;width:100%" onclick="event.stopPropagation()">
    <div style="font-size:14px;font-weight:800;margin-bottom:14px" id="qr-title">QR Code</div>
    <div style="background:#fff;padding:12px;border-radius:14px;margin-bottom:14px"><img id="qr-img" src="" alt="QR" style="width:100%;display:block"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="closeModal('modal-qr')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show '+(type||'');
  setTimeout(()=>t.classList.remove('show'),2400);
}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}

function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}

function showQR(title, text){
  document.getElementById('qr-title').textContent=title;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(text);
  openModal('modal-qr');
}

function copyConfigLink(linkText){
  if(!linkText) return;
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(linkText).then(()=>{
      toast('لینک کانفیگ با موفقیت کپی شد ✓', 'ok');
    }).catch(()=>{
      _fallbackCopyLink(linkText);
    });
  } else {
    _fallbackCopyLink(linkText);
  }
}
function _fallbackCopyLink(text){
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    toast('لینک کانفیگ با موفقیت کپی شد ✓', 'ok');
  } catch(e) {
    toast('خطا در کپی لینک', 'err');
  }
}

function toggleActionMenu(event, uuid){
  if(event) event.stopPropagation();
  const menu = document.getElementById('menu-' + uuid);
  if(!menu) return;
  const isCurrentlyOpen = menu.classList.contains('open');
  closeActionMenus();
  if(!isCurrentlyOpen){
    menu.classList.add('open');
    const rect = menu.getBoundingClientRect();
    const card = menu.closest('.sub-card');
    const cardRight = card ? card.getBoundingClientRect().right : window.innerWidth;
    const cardLeft = card ? card.getBoundingClientRect().left : 0;
    
    if(rect.right > cardRight - 8 || rect.right > window.innerWidth - 8){
      menu.style.right = '0';
      menu.style.left = 'auto';
    } else if(rect.left < cardLeft + 8 || rect.left < 8){
      menu.style.left = '0';
      menu.style.right = 'auto';
    }
  }
}

function closeActionMenus(){
  document.querySelectorAll('.action-menu.open').forEach(m=>{
    m.classList.remove('open');
    m.style.left = '';
    m.style.right = '';
  });
}

document.addEventListener('click', e => {
  if(!e.target.closest('.action-dropdown')){
    closeActionMenus();
  }
});

document.addEventListener('keydown', e => {
  if(e.key === 'Escape') closeActionMenus();
});

// Navigation & Tab Switching
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('open')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('open')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);

function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={overview:fetchStats,subs:loadSubs,links:loadLinks,connections:loadConns,settings:loadSettings,logs:loadActivity,errors:fetchStats};
  if(loaders[name])loaders[name]();
  if(name==='overview'){try{if(ch1)ch1.resize();if(chDonut)chDonut.resize();}catch(e){}}
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));

document.getElementById('logout-btn').addEventListener('click',async()=>{
  await fetch('/api/logout',{method:'POST'});
  location.href='/login';
});

const WORKER_SCRIPT_TEMPLATE = `/**
 * FilterGosha Panel - Cloudflare Worker Reverse Proxy (Anti-DPI / WebSocket Bypass)
 * 
 * Instructions:
 * 1. Go to Cloudflare Dashboard -> Workers & Pages -> Create Worker.
 * 2. Paste this code into the editor.
 * 3. Replace 'RAILWAY_BACKEND' with your actual Railway domain (e.g., 'kouroshnet.vazirigoldgallery.ir').
 * 4. Save and Deploy.
 * 5. Add Custom Domain (e.g., 'gold.vazirigoldgallery.ir') under Worker Settings -> Triggers.
 */

const RAILWAY_BACKEND = "kouroshnet.vazirigoldgallery.ir";

export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      
      // Rewrite destination hostname to Railway server
      url.hostname = RAILWAY_BACKEND;
      url.protocol = "https:";
      url.port = "443";

      // Duplicate headers and set appropriate Host and X-Forwarded headers
      const newHeaders = new Headers(request.headers);
      newHeaders.set("Host", RAILWAY_BACKEND);
      newHeaders.set("X-Forwarded-Host", request.headers.get("Host") || url.hostname);
      newHeaders.set("X-Forwarded-Proto", "https");

      const clientIp = request.headers.get("CF-Connecting-IP");
      if (clientIp) {
        newHeaders.set("X-Real-IP", clientIp);
        const existingFwd = request.headers.get("X-Forwarded-For");
        newHeaders.set("X-Forwarded-For", existingFwd ? \`\${existingFwd}, \${clientIp}\` : clientIp);
      }

      // Check if WebSocket upgrade request
      const isWebSocket = request.headers.get("Upgrade")?.toLowerCase() === "websocket";

      if (isWebSocket) {
        return fetch(url.toString(), {
          method: request.method,
          headers: newHeaders,
          body: request.body,
          redirect: "manual"
        });
      }

      // Standard HTTP fetch
      const response = await fetch(url.toString(), {
        method: request.method,
        headers: newHeaders,
        body: request.method !== "GET" && request.method !== "HEAD" ? request.body : null,
        redirect: "manual"
      });

      // Wrap response headers for CORS compatibility
      const responseHeaders = new Headers(response.headers);
      responseHeaders.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders
      });
    } catch (err) {
      return new Response(\`FilterGosha Worker Proxy Error: \${err.message}\`, { status: 502 });
    }
  }
};`;

const PAGES_SCRIPT_TEMPLATE = `/**
 * FilterGosha Panel - Cloudflare Pages Function Reverse Proxy (pages.dev Anti-DPI / WebSocket Bypass)
 * File: functions/[[path]].js
 * 
 * Instructions:
 * 1. Go to Cloudflare Dashboard -> Workers & Pages -> Create -> Pages -> Upload Assets.
 * 2. Upload a folder containing a 'functions' directory with this [[path]].js file inside it.
 * 3. Replace 'RAILWAY_BACKEND' with your actual Railway domain (e.g., 'kouroshnet.vazirigoldgallery.ir').
 * 4. Your project will be deployed at 'your-project.pages.dev'.
 */

const RAILWAY_BACKEND = "kouroshnet.vazirigoldgallery.ir";

export async function onRequest(context) {
  const { request } = context;
  try {
    const url = new URL(request.url);
    
    // Rewrite destination hostname to Railway server
    url.hostname = RAILWAY_BACKEND;
    url.protocol = "https:";
    url.port = "443";

    // Duplicate headers and set appropriate Host and X-Forwarded headers
    const newHeaders = new Headers(request.headers);
    newHeaders.set("Host", RAILWAY_BACKEND);
    newHeaders.set("X-Forwarded-Host", request.headers.get("Host") || url.hostname);
    newHeaders.set("X-Forwarded-Proto", "https");

    const clientIp = request.headers.get("CF-Connecting-IP");
    if (clientIp) {
      newHeaders.set("X-Real-IP", clientIp);
      const existingFwd = request.headers.get("X-Forwarded-For");
      newHeaders.set("X-Forwarded-For", existingFwd ? \`\${existingFwd}, \${clientIp}\` : clientIp);
    }

    // Check if WebSocket upgrade request
    const isWebSocket = request.headers.get("Upgrade")?.toLowerCase() === "websocket";

    if (isWebSocket) {
      return fetch(url.toString(), {
        method: request.method,
        headers: newHeaders,
        body: request.body,
        redirect: "manual"
      });
    }

    // Standard HTTP fetch
    const response = await fetch(url.toString(), {
      method: request.method,
      headers: newHeaders,
      body: request.method !== "GET" && request.method !== "HEAD" ? request.body : null,
      redirect: "manual"
    });

    const responseHeaders = new Headers(response.headers);
    responseHeaders.set("Access-Control-Allow-Origin", "*");

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders
    });
  } catch (err) {
    return new Response(\`FilterGosha Pages Proxy Error: \${err.message}\`, { status: 502 });
  }
}
`;

async function loadSettings(){
  try{
    const r=await fetch('/api/settings'),d=await r.json();
    document.getElementById('st-remark-prefix').value = d.remark_prefix !== undefined ? d.remark_prefix : 'FilterGosha';
    document.getElementById('st-worker-domain').value = d.worker_domain||'';
    document.getElementById('st-clean-ip').value = d.clean_ip||'';
    document.getElementById('worker-code-box').value = WORKER_SCRIPT_TEMPLATE;
    document.getElementById('pages-code-box').value = PAGES_SCRIPT_TEMPLATE;
    syncBackupSelection();
  }catch(e){toast('خطا در دریافت تنظیمات','err')}
}

document.addEventListener('submit',async e=>{
  if(e.target && e.target.id==='form-change-pw'){
    e.preventDefault();
    const cur = document.getElementById('cpw-current').value;
    const newPw = document.getElementById('cpw-new').value;
    const conf = document.getElementById('cpw-confirm').value;
    if(newPw !== conf){
      toast('رمز عبور جدید و تکرار آن یکسان نیستند','err');
      return;
    }
    if(newPw.length < 4){
      toast('رمز عبور جدید باید حداقل ۴ کاراکتر باشد','err');
      return;
    }
    try{
      const r = await fetch('/api/change-password',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ current_password: cur, new_password: newPw })
      });
      const d = await r.json();
      if(r.ok){
        toast('رمز عبور با موفقیت تغییر یافت ✓','ok');
        document.getElementById('form-change-pw').reset();
      } else {
        toast(d.detail || 'خطا در تغییر رمز عبور','err');
      }
    }catch(err){
      toast('خطا در ارتباط با سرور','err');
    }
  }
  if(e.target && e.target.id==='form-settings'){
    e.preventDefault();
    const payload = {
      remark_prefix: document.getElementById('st-remark-prefix').value.trim(),
      worker_domain: document.getElementById('st-worker-domain').value.trim(),
      clean_ip: document.getElementById('st-clean-ip').value.trim(),
    };
    try{
      const r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      if(r.ok){
        toast('تنظیمات عمومی پنل ذخیره شد ✓','ok');
        loadSettings();
      }else{
        toast('خطا در ذخیره تنظیمات','err');
      }
    }catch(err){toast('خطا در ارتباط با سرور','err')}
  }
});

function copyWorkerScript(){
  const code = document.getElementById('worker-code-box').value;
  navigator.clipboard.writeText(code).then(()=>toast('کد Cloudflare Worker کپی شد ✓','ok'));
}

function copyPagesScript(){
  const code = document.getElementById('pages-code-box').value;
  navigator.clipboard.writeText(code).then(()=>toast('کد Cloudflare Pages Function کپی شد ✓','ok'));
}

// GRANULAR BACKUP / RESTORE
const BACKUP_LABELS = {
  links: 'کانفیگ‌ها',
  subs: 'اشتراک‌ها',
  settings: 'تنظیمات عمومی پنل',
  auth: 'رمز عبور پنل',
  usage: 'آمار مصرف',
};

function backupSelection(){
  return Array.from(document.querySelectorAll('#pg-settings input.bk-chk:checked')).map(b=>b.value);
}

function syncBackupSelection(){
  const sel = backupSelection();
  const dataParts = sel.filter(v=>v!=='usage');
  const btn = document.getElementById('bk-export-btn');
  const hint = document.getElementById('bk-hint');
  if(btn) btn.disabled = dataParts.length === 0;
  if(!hint) return;
  if(!dataParts.length){
    hint.classList.add('bk-warn');
    hint.innerHTML = '<i class="ti ti-alert-triangle"></i> حداقل یکی از بخش‌های داده (کانفیگ‌ها، اشتراک‌ها، تنظیمات یا رمز عبور) را انتخاب کنید.';
    return;
  }
  hint.classList.remove('bk-warn');
  const notes = [];
  if(sel.includes('subs') && !sel.includes('links'))
    notes.push('اشتراک‌ها بدون کانفیگ ذخیره می‌شوند، پس فهرست کانفیگ‌های هر اشتراک در فایل خالی خواهد بود.');
  if(!sel.includes('usage'))
    notes.push('مصرف تمام کانفیگ‌ها و اشتراک‌ها در فایل صفر ذخیره می‌شود.');
  if(sel.includes('auth'))
    notes.push('رمز عبور پنل هم در فایل قرار می‌گیرد؛ فایل را در جای امن نگه دارید.');
  hint.innerHTML = '<i class="ti ti-file-check"></i> محتوای فایل: ' +
    dataParts.map(v=>BACKUP_LABELS[v]||v).join(' + ') +
    (notes.length ? '<div style="margin-top:6px;color:var(--t3);font-weight:500">• ' + notes.join('<br>• ') + '</div>' : '');
}

function exportBackup(){
  const sel = backupSelection();
  if(!sel.filter(v=>v!=='usage').length) return toast('حداقل یک بخش داده را برای بک‌آپ انتخاب کنید','err');
  window.location.href = '/api/export_db?components=' + encodeURIComponent(sel.join(','));
  toast('در حال ساخت فایل بک‌آپ...','ok');
}

async function handleImportDB(file) {
  if(!file) return;
  const input = document.getElementById('import-db-file');
  try {
    const fd = new FormData();
    fd.append('file', file);
    const r = await fetch('/api/import_db_analyze', {method:'POST', body:fd});
    const d = await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail || 'خطا در آنالیز فایل بک‌آپ');

    const present = d.components || [];
    const lines = [
      'محتوای فایل بک‌آپ:',
      '• ' + (d.links_count || 0) + ' کانفیگ',
      '• ' + (d.subs_count || 0) + ' اشتراک',
      '• بخش‌های موجود: ' + present.map(k=>BACKUP_LABELS[k]||k).join('، '),
      '',
      'بازیابی این فایل انجام شود؟'
    ];
    if(!confirm(lines.join('\n'))){ input.value=''; return; }

    const restore = present.filter(k=>k!=='auth');
    if(present.includes('auth') && confirm('این فایل شامل رمز عبور مدیریت پنل است.\nآیا رمز فعلی پنل با رمز داخل فایل جایگزین شود؟\n\n- [OK] = بله، رمز را هم بازیابی کن\n- [Cancel] = خیر، رمز فعلی حفظ شود'))
      restore.push('auth');

    let mode = 'skip';
    if(d.conflicts > 0){
      mode = confirm(d.conflicts + ' کانفیگ/اشتراک تکراری در فایل بک‌آپ یافت شد.\nآیا اطلاعات موجود در پنل با اطلاعات بک‌آپ جایگزین (Overwrite) شود؟\n\n- [OK] = بله جایگزین کن\n- [Cancel] = خیر، نادیده بگیر و رد شو') ? 'overwrite' : 'skip';
    }

    const fd2 = new FormData();
    fd2.append('file', file);
    fd2.append('mode', mode);
    fd2.append('components', restore.join(','));
    const r2 = await fetch('/api/import_db', {method:'POST', body:fd2});
    const d2 = await r2.json().catch(()=>({}));
    if(!r2.ok) throw new Error(d2.detail || 'خطا در بازگردانی دیتابیس');

    const added = (d2.added_links||0) + (d2.added_subs||0);
    const updated = (d2.updated_links||0) + (d2.updated_subs||0);
    toast(`بازیابی انجام شد ✓ (${added} مورد جدید، ${updated} مورد جایگزین)`,'ok');
    setTimeout(()=>window.location.reload(), 1500);
  } catch(e) {
    toast(e.message || 'خطا در ارتباط با سرور','err');
  } finally {
    if(input) input.value = '';
  }
}


// STATS & DASHBOARD OVERVIEW
let ch1, chDonut;
async function fetchStats(){
  try{
    const r=await fetch('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections||0;
    document.getElementById('m-traffic').textContent=(d.total_traffic_mb||0).toFixed(1)+' MB';
    document.getElementById('m-alinks').textContent=d.active_links??0;
    document.getElementById('m-lsub').textContent='از '+(d.links_count||0)+' کانفیگ';
    document.getElementById('m-errors').textContent=d.total_errors||0;
    document.getElementById('uptime-inline').textContent=d.uptime||'--:--:--';
    document.getElementById('uptime-badge').textContent='Railway - '+(d.uptime||'00:00:00');
    document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    document.getElementById('subs-nb').textContent=d.subs_count||0;
    document.getElementById('links-nb').textContent=d.links_count||0;
    document.getElementById('conns-nb').textContent=d.active_connections||0;
    
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      if(ch1){ch1.data.labels=labels;ch1.data.datasets[0].data=vals;ch1.update()}
    }

    if(d.proto_dist && chDonut){
      const pd = d.proto_dist;
      const ws = pd.vless_ws || 0;
      const xh = pd.xhttp || 0;
      const gr = (pd.vless_grpc || 0) + (pd.custom || 0);
      chDonut.data.datasets[0].data = [ws || 1, xh || 1, gr || 1];
      chDonut.update();
    }

    loadDashLinksSummary();
  }catch(e){console.error(e)}
}

async function loadDashLinksSummary(){
  try{
    const r=await fetch('/api/links'),d=await r.json();
    const el=document.getElementById('dash-links-summary');
    if(!el) return;
    if(!d.links||!d.links.length){
      el.innerHTML='<div style="font-size:12px;color:var(--t3);text-align:center;padding:10px">هیچ کانفیگی ثبت نشده است</div>';
      return;
    }
    el.innerHTML = d.links.slice(0, 5).map(l=>{
      const lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
      const used = fmtB(l.used_bytes);
      const stColor = l.active ? 'var(--green-t)' : 'var(--red-t)';
      return `
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 12px;background:rgba(0,0,0,0.2);border:1px solid var(--card-b);border-radius:10px;font-size:11.5px">
          <div style="display:flex;align-items:center;gap:6px;min-width:0;flex:1">
            <span style="color:${stColor};flex-shrink:0">●</span>
            <strong style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="${esc(l.label)}">${esc(l.label)}</strong>
          </div>
          <div style="font-size:11px;color:var(--t2);white-space:nowrap;flex-shrink:0">
            <span style="color:var(--t1)">${used}</span> / <span style="color:var(--t3)">${lim}</span>
          </div>
        </div>
      `;
    }).join('');
  }catch(e){}
}

function initChart(){
  const ctx=document.getElementById('ch1').getContext('2d');
  ch1=new Chart(ctx,{
    type:'line',
    data:{labels:[],datasets:[{label:'ترافیک (MB)',data:[],borderColor:'#3B82F6',backgroundColor:'rgba(59,130,246,0.12)',fill:true,tension:.4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true}}}
  });

  const ctx2=document.getElementById('ch-donut').getContext('2d');
  chDonut=new Chart(ctx2,{
    type:'doughnut',
    data:{
      labels:['VLESS/WS', 'XHTTP Ultra', 'HTTP / gRPC'],
      datasets:[{
        data:[1, 1, 1],
        backgroundColor:['#10b981', '#3B82F6', '#9D7BF0'],
        borderWidth: 0
      }]
    },
    options:{
      responsive:true,
      maintainAspectRatio:false,
      plugins:{
        legend:{
          position:'bottom',
          labels:{color:'#8AA0C4', font:{family:'Vazirmatn', size:10}}
        }
      },
      cutout:'70%'
    }
  });
}

// DATEPICKER & EXPIRATION HELPERS
function setExpPreset(prefix, days){
  const inp = document.getElementById(prefix + '-exp-date');
  if(!inp) return;
  if(days <= 0){
    inp.value = '';
  } else {
    const d = new Date();
    d.setDate(d.getDate() + days);
    const pad = n => String(n).padStart(2, '0');
    inp.value = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }
  updateExpShamsi(prefix);
}

function updateExpShamsi(prefix){
  const inp = document.getElementById(prefix + '-exp-date');
  const label = document.getElementById(prefix + '-exp-shamsi');
  if(!inp || !label) return;
  if(!inp.value){
    label.innerHTML = '<span style="color:var(--t3)">نامحدود (بدون انقضا)</span>';
    return;
  }
  const dt = new Date(inp.value);
  if(isNaN(dt.getTime())){
    label.innerHTML = '<span style="color:var(--t3)">نامحدود</span>';
    return;
  }
  const now = new Date();
  const diffDays = Math.ceil((dt - now) / (1000 * 60 * 60 * 24));
  const shamsiStr = dt.toLocaleDateString('fa-IR', { year:'numeric', month:'long', day:'numeric' }) + ' ساعت ' + dt.toLocaleTimeString('fa-IR', { hour:'2-digit', minute:'2-digit' });
  if(dt < now){
    label.innerHTML = `<span style="color:var(--red-t);font-weight:700">⚠️ منقضی شده (${shamsiStr})</span>`;
  } else {
    label.innerHTML = `<span style="color:var(--green-t)">✓ ${shamsiStr} (${diffDays} روز دیگر)</span>`;
  }
}

function formatExpBadge(expStr){
  if(!expStr) return '<span style="color:var(--t3)"><i class="ti ti-infinity"></i> نامحدود</span>';
  const dt = new Date(expStr);
  if(isNaN(dt.getTime())) return '<span style="color:var(--t3)">نامحدود</span>';
  const now = new Date();
  const dateFmt = dt.toLocaleDateString('fa-IR', { year:'numeric', month:'numeric', day:'numeric' });
  if(dt < now){
    return `<span class="badge bg-red" style="background:rgba(239,68,68,0.15);color:#FB8585"><i class="ti ti-clock-off"></i> منقضی شده (${dateFmt})</span>`;
  }
  const diffDays = Math.ceil((dt - now) / (1000 * 60 * 60 * 24));
  return `<span class="badge bg-green" style="background:rgba(16,185,129,0.12);color:var(--accent)"><i class="ti ti-calendar"></i> ${dateFmt} (${diffDays} روز)</span>`;
}

// BULK SELECTION (shared by subscriptions & configs pages)
const BULK_CFG = {
  subs: {
    endpoint: '/api/subs/bulk_delete',
    reload: () => loadSubs(),
    noun: 'اشتراک',
    emptyText: 'هیچ اشتراکی انتخاب نشده',
    confirmText: n => `آیا از حذف ${n} اشتراک انتخاب‌شده اطمینان دارید؟\nکانفیگ‌های مرتبط حذف نمی‌شوند و فقط از این اشتراک‌ها جدا می‌شوند.`,
  },
  links: {
    endpoint: '/api/links/bulk_delete',
    reload: () => loadLinks(),
    noun: 'کانفیگ',
    emptyText: 'هیچ کانفیگی انتخاب نشده',
    confirmText: n => `آیا از حذف ${n} کانفیگ انتخاب‌شده اطمینان دارید؟\nاین کانفیگ‌ها از تمام اشتراک‌های مرتبط نیز حذف خواهند شد.`,
  },
};
const bulkSelected = { subs: new Set(), links: new Set() };

function bulkBoxes(kind){
  return Array.from(document.querySelectorAll(`#${kind}-list input.bulk-item`));
}

function syncBulkUI(kind){
  const boxes = bulkBoxes(kind);
  const sel = bulkSelected[kind];
  const bar = document.getElementById(kind + '-bulk-bar');
  const btn = document.getElementById(kind + '-bulk-del');
  const cnt = document.getElementById(kind + '-bulk-count');
  const all = document.getElementById(kind + '-chk-all');
  if(bar) bar.style.display = boxes.length ? 'flex' : 'none';
  if(btn) btn.disabled = sel.size === 0;
  if(cnt){
    cnt.textContent = sel.size ? `${sel.size} ${BULK_CFG[kind].noun} انتخاب شده` : BULK_CFG[kind].emptyText;
    cnt.classList.toggle('has-sel', sel.size > 0);
  }
  if(all){
    all.checked = boxes.length > 0 && sel.size === boxes.length;
    all.indeterminate = sel.size > 0 && sel.size < boxes.length;
  }
}

function toggleBulkItem(kind, id, checked){
  if(checked) bulkSelected[kind].add(id);
  else bulkSelected[kind].delete(id);
  syncBulkUI(kind);
}

function toggleSelectAll(kind, checked){
  const sel = bulkSelected[kind];
  bulkBoxes(kind).forEach(box=>{
    box.checked = checked;
    if(checked) sel.add(box.value); else sel.delete(box.value);
  });
  syncBulkUI(kind);
}

function restoreBulkSelection(kind, availableIds){
  const sel = bulkSelected[kind];
  const alive = new Set(availableIds);
  Array.from(sel).forEach(id=>{ if(!alive.has(id)) sel.delete(id); });
  bulkBoxes(kind).forEach(box=>{ box.checked = sel.has(box.value); });
  syncBulkUI(kind);
}

async function bulkDelete(kind){
  const cfg = BULK_CFG[kind];
  const ids = Array.from(bulkSelected[kind]);
  if(!ids.length) return toast(cfg.emptyText, 'err');
  if(!confirm(cfg.confirmText(ids.length))) return;

  const btn = document.getElementById(kind + '-bulk-del');
  const original = btn ? btn.innerHTML : '';
  if(btn){
    btn.disabled = true;
    btn.innerHTML = '<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال حذف...';
  }
  try{
    const r = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ ids })
    });
    const d = await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail || 'خطا در حذف گروهی');
    bulkSelected[kind].clear();
    const missing = (d.missing || []).length;
    toast(`${d.deleted_count || 0} ${cfg.noun} حذف شد ✓` + (missing ? ` (${missing} مورد یافت نشد)` : ''), 'ok');
    await cfg.reload();
  }catch(e){
    toast(e.message || 'خطا در ارتباط با سرور', 'err');
  }finally{
    if(btn){ btn.innerHTML = original; }
    syncBulkUI(kind);
  }
}

// SUBSCRIPTION MANAGEMENT
let allAvailableLinks = [];
let currentSubId = '';

async function loadSubs(){
  try{
    const r=await fetch('/api/subs'),d=await r.json();
    if(d.subs) renderSubs(d.subs);
  }catch(e){toast('خطا در بارگذاری اشتراک‌ها','err')}
}

function renderSubs(subs){
  const el=document.getElementById('subs-list');
  if(!subs.length){
    el.innerHTML='<div class="card" style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-users-group" style="font-size:32px;display:block;margin-bottom:10px"></i>هیچ اشتراکی تعریف نشده است. بر روی «اشتراک جدید» کلیک کنید.</div>';
    bulkSelected.subs.clear();
    syncBulkUI('subs');
    return;
  }
  el.innerHTML=subs.map(s=>{
    const pct = s.limit_bytes === 0 ? 0 : Math.min(100, (s.used_bytes / s.limit_bytes) * 100);
    const bc = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
    return `
      <div class="sub-card">
        <div class="sub-head">
          <div style="display:flex;align-items:flex-start;gap:10px">
            <input type="checkbox" class="bulk-chk bulk-item" style="margin-top:4px" value="${esc(s.sub_id)}" title="انتخاب برای حذف گروهی" onchange="toggleBulkItem('subs','${esc(s.sub_id)}',this.checked)">
            <div>
              <div class="sub-label">${esc(s.label)}</div>
              <div style="font-size:10.5px;color:var(--t3);margin-top:4px">
                <span class="badge bg-blue" style="margin-left:6px"><i class="ti ti-link"></i> ${s.links_count} کانفیگ</span>
                <span class="badge bg-green"><i class="ti ti-plug-connected"></i> ${s.connections} اتصال فعال</span>
                <span style="margin-right:8px"><i class="ti ti-calendar"></i> انقضا: ${formatExpBadge(s.expires_at)}</span>
              </div>
            </div>
          </div>
          <div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-g" onclick="resetSubUsage('${s.sub_id}')" title="صفر کردن مصرف"><i class="ti ti-rotate"></i> ریست مصرف</button>
            <button class="btn btn-sm btn-g" onclick="openSubModal('${s.sub_id}')"><i class="ti ti-edit"></i> ویرایش</button>
            <button class="btn btn-sm btn-d" onclick="deleteSub('${s.sub_id}')"><i class="ti ti-trash"></i> حذف</button>
          </div>
        </div>
        <div style="margin-top:10px">
          <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
          <div class="utxt"><span>مصرف: ${esc(s.used_fmt)}</span><span>سهمیه: ${esc(s.limit_fmt)}</span></div>
        </div>
        <div class="sub-links-box">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
            <span style="font-weight:700;color:var(--t1)"><i class="ti ti-link"></i> لینک اشتراک (صفحه وب + کلاینت):</span>
            <div style="display:flex;gap:6px">
              <button class="btn btn-sm btn-p" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک اشتراک کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی لینک</button>
              <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.label)}', '${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i> QR</button>
            </div>
          </div>
          <div style="word-break:break-all;color:var(--accent2);">${esc(s.sub_url)}</div>
        </div>
      </div>
    `;
  }).join('');
  restoreBulkSelection('subs', subs.map(s=>s.sub_id));
}

async function resetSubUsage(sid){
  if(!confirm('آیا از صفر کردن ترافیک مصرفی این اشتراک اطمینان دارید؟')) return;
  try{
    const r = await fetch('/api/subs/' + sid + '/reset_usage', {method:'POST'});
    if(r.ok){ toast('مصرف اشتراک ریست شد ✓', 'ok'); loadSubs(); }
    else { toast('خطا در ریست مصرف', 'err'); }
  }catch(e){ toast('خطا در ارتباط با سرور', 'err'); }
}

async function openSubModal(sid=''){
  currentSubId = sid;
  document.getElementById('sub-modal-title').textContent = sid ? 'ویرایش اشتراک' : 'ساخت اشتراک جدید';
  
  // Load links for checklist
  const lr = await fetch('/api/links'), ld = await lr.json();
  allAvailableLinks = ld.links || [];
  
  let targetSub = null;
  if(sid){
    const sr = await fetch('/api/subs'), sd = await sr.json();
    targetSub = (sd.subs || []).find(s=>s.sub_id===sid);
  }
  
  document.getElementById('sub-label').value = targetSub ? targetSub.label : '';
  document.getElementById('sub-limit-val').value = targetSub ? (targetSub.limit_bytes / (1024**3)).toFixed(1) : 0;
  
  if(targetSub && targetSub.expires_at){
    try{
      const d = new Date(targetSub.expires_at);
      if(!isNaN(d.getTime())){
        const pad = n => String(n).padStart(2,'0');
        document.getElementById('sub-exp-date').value = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
      } else {
        document.getElementById('sub-exp-date').value = '';
      }
    }catch(e){ document.getElementById('sub-exp-date').value = ''; }
  } else {
    document.getElementById('sub-exp-date').value = '';
  }
  updateExpShamsi('sub');

  document.getElementById('sub-iplimit').value = targetSub ? targetSub.ip_limit : 0;
  document.getElementById('sub-speed-val').value = targetSub ? (targetSub.speed_limit_bytes * 8 / 1024 / 1024).toFixed(1) : 0;
  document.getElementById('sub-hwidlimit').value = targetSub ? (targetSub.hwid_limit || 0) : 0;
  const hwidInfoEl = document.getElementById('sub-hwid-info');
  if(hwidInfoEl){
    const regCount = (targetSub && targetSub.hwids) ? Object.keys(targetSub.hwids).length : 0;
    let extra = '';
    if(targetSub){
      extra = ` <b style="color:var(--accent)">دستگاه‌های ثبت‌شده: ${regCount}</b>`;
      if(regCount > 0){
        extra += ` — <a href="#" onclick="resetSubHwids('${esc(currentSubId)}');return false;" style="color:var(--red)">پاک‌کردن دستگاه‌ها</a>`;
      }
    }
    hwidInfoEl.innerHTML = 'اولین دستگاه‌هایی که وصل شوند قفل می‌شوند؛ دستگاه جدید بعد از پر شدن سقف رد می‌شود. شناسه از روی User-Agent کلاینت یا هدر X-HWID ساخته می‌شود (روی WS/gRPC/XHTTP/Trojan؛ SOCKS5 معاف است).' + extra;
  }
  document.getElementById('sub-note').value = targetSub ? targetSub.note : '';
  
  const chkEl = document.getElementById('sub-links-checklist');
  if(!allAvailableLinks.length){
    chkEl.innerHTML = '<span style="color:var(--t3)">هیچ کانفیگی برای انتخاب وجود ندارد.</span>';
  } else {
    chkEl.innerHTML = allAvailableLinks.map(l=>{
      const isChecked = targetSub && targetSub.links && targetSub.links.includes(l.uuid);
      return `
        <label class="cfg-chk-item">
          <input type="checkbox" value="${l.uuid}" ${isChecked?'checked':''}>
          <span>${esc(l.label)} <small style="color:var(--t3)">(:${l.port||443})</small></span>
        </label>
      `;
    }).join('');
  }
  openModal('modal-sub');
}

document.getElementById('form-sub').addEventListener('submit',async e=>{
  e.preventDefault();
  const checkedUuids = Array.from(document.querySelectorAll('#sub-links-checklist input:checked')).map(i=>i.value);
  const expVal = document.getElementById('sub-exp-date').value;
  const payload = {
    label: document.getElementById('sub-label').value.trim(),
    limit_value: parseFloat(document.getElementById('sub-limit-val').value)||0,
    limit_unit: document.getElementById('sub-limit-unit').value,
    expires_at: expVal ? new Date(expVal).toISOString() : null,
    ip_limit: parseInt(document.getElementById('sub-iplimit').value)||0,
    speed_limit_value: parseFloat(document.getElementById('sub-speed-val').value)||0,
    speed_limit_unit: document.getElementById('sub-speed-unit').value,
    hwid_limit: parseInt(document.getElementById('sub-hwidlimit').value)||0,
    note: document.getElementById('sub-note').value.trim(),
    links: checkedUuids,
  };
  
  const url = currentSubId ? ('/api/subs/' + currentSubId) : '/api/subs';
  const method = currentSubId ? 'PATCH' : 'POST';
  
  try{
    const r=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(r.ok){
      toast('اشتراک با موفقیت ذخیره شد ✓','ok');
      closeModal('modal-sub');
      loadSubs();
    } else {
      toast('خطا در ذخیره اشتراک','err');
    }
  }catch(err){toast('خطا در ارتباط با سرور','err')}
});

async function deleteSub(sid){
  if(!confirm('آیا از حذف این اشتراک اطمینان دارید؟ کانفیگ‌های مرتبط از این اشتراک جدا می‌شوند.')) return;
  try{
    const r=await fetch('/api/subs/'+sid,{method:'DELETE'});
    if(r.ok){toast('اشتراک حذف شد','ok');loadSubs();}
  }catch(e){toast('خطا در حذف','err')}
}

async function resetSubHwids(sid){
  if(!sid) return;
  if(!confirm('همه‌ی دستگاه‌های ثبت‌شده‌ی این اشتراک پاک شوند؟ دفعه‌ی بعد که کاربر وصل شود، دستگاه‌هایش دوباره از نو ثبت می‌شوند.')) return;
  try{
    const r=await fetch('/api/subs/'+sid+'/reset_hwids',{method:'POST'});
    if(r.ok){
      toast('دستگاه‌های ثبت‌شده پاک شد ✓','ok');
      const el=document.getElementById('sub-hwid-info');
      if(el){ const i=el.innerHTML.indexOf('دستگاه‌های ثبت‌شده'); }
      loadSubs();
      closeModal('modal-sub');
    } else { toast('خطا در پاک‌کردن دستگاه‌ها','err'); }
  }catch(e){toast('خطا در ارتباط با سرور','err')}
}

// LINKS MANAGEMENT
async function loadLinks(){
  try{
    const r=await fetch('/api/links'),d=await r.json();
    if(d.links) renderLinks(d.links);
  }catch(e){toast('خطا در بارگذاری کانفیگ‌ها','err')}
}

function protoChipText(proto){
  if(proto==='vless-ws') return '<span class="badge bg-blue"><i class="ti ti-wifi"></i> VLESS WS</span>';
  if(proto==='xhttp') return '<span class="badge bg-green" style="background:var(--purple-bg);color:var(--purple-t)"><i class="ti ti-bolt"></i> XHTTP Auto</span>';
  if(proto==='trojan-ws') return '<span class="badge bg-red" style="background:rgba(239,68,68,0.12);color:#FCA5A5"><i class="ti ti-horse-toy"></i> Trojan WS</span>';
  if(proto==='socks5'||proto==='socks') return '<span class="badge bg-amber" style="background:rgba(242,163,61,0.12);color:#F9C988"><i class="ti ti-shield-lock"></i> SOCKS5</span>';
  if(proto==='custom') return '<span class="badge bg-amber" style="background:rgba(242,163,61,0.12);color:#F9C988"><i class="ti ti-code"></i> کاستوم</span>';
  return '<span class="badge bg-green"><i class="ti ti-route"></i> VLESS gRPC</span>';
}

let currentLinkId = '';

function renderLinks(links){
  const el=document.getElementById('links-list');
  if(!links.length){
    el.innerHTML='<div class="card" style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-link" style="font-size:32px;display:block;margin-bottom:10px"></i>هیچ کانفیگی ساخته نشده است. بر روی «کانفیگ جدید» کلیک کنید.</div>';
    bulkSelected.links.clear();
    syncBulkUI('links');
    return;
  }
  el.innerHTML=links.map(l=>{
    const pct = l.limit_bytes === 0 ? 0 : Math.min(100, ((l.used_bytes || 0) / l.limit_bytes) * 100);
    const bc = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
    const usedFmt = fmtB(l.used_bytes || 0);
    const limitFmt = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
    return `
      <div class="sub-card">
        <div class="sub-head">
          <div style="display:flex;align-items:flex-start;gap:10px">
            <input type="checkbox" class="bulk-chk bulk-item" style="margin-top:4px" value="${esc(l.uuid)}" title="انتخاب برای حذف گروهی" onchange="toggleBulkItem('links','${esc(l.uuid)}',this.checked)">
            <div>
              <div class="sub-label">${esc(l.label)}</div>
              <div style="font-size:10.5px;color:var(--t3);margin-top:4px">
                ${protoChipText(l.protocol)}
                <span class="badge bg-blue" style="margin-right:6px"><i class="ti ti-plug-connected"></i> ${l.connected_ips||0} آی‌پی متصل</span>
                <span style="margin-right:8px"><i class="ti ti-calendar"></i> انقضا: ${formatExpBadge(l.expires_at)}</span>
              </div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:6px">
            <button class="btn btn-sm btn-g icon-action-btn" onclick="copyConfigLink('${esc(l.vless_link)}')" title="کپی لینک کانفیگ"><i class="ti ti-copy"></i></button>
            <div class="action-dropdown">
              <button class="btn btn-sm btn-g icon-action-btn" onclick="toggleActionMenu(event, '${esc(l.uuid)}')" title="عملیات بیشتر"><i class="ti ti-dots-vertical"></i></button>
              <div class="action-menu" id="menu-${esc(l.uuid)}">
                <button type="button" class="action-menu-item" onclick="openLinkModal('${l.uuid}'); closeActionMenus()">
                  <i class="ti ti-edit"></i>
                  <span>ویرایش کانفیگ</span>
                </button>
                <button type="button" class="action-menu-item" onclick="showQR('${esc(l.label)}', '${esc(l.vless_link)}'); closeActionMenus()">
                  <i class="ti ti-qrcode"></i>
                  <span>نمایش QR Code</span>
                </button>
                <div class="action-menu-divider"></div>
                <button type="button" class="action-menu-item" onclick="resetLinkUsage('${l.uuid}'); closeActionMenus()">
                  <i class="ti ti-rotate"></i>
                  <span>ریست مصرف</span>
                </button>
              </div>
            </div>
            <button class="btn btn-sm btn-d icon-action-btn" onclick="deleteLink('${l.uuid}')" title="حذف کانفیگ"><i class="ti ti-trash"></i></button>
          </div>
        </div>
        <div style="margin-top:8px">
          <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
          <div class="utxt"><span>مصرف: ${usedFmt}</span><span>سهمیه: ${limitFmt}</span></div>
        </div>
        <div class="sub-links-box" style="margin-top:8px;font-size:10px">
          ${esc(l.vless_link)}
        </div>
      </div>
    `;
  }).join('');
  restoreBulkSelection('links', links.map(l=>l.uuid));
}

async function resetLinkUsage(uid){
  if(!confirm('آیا از صفر کردن ترافیک مصرفی این کانفیگ اطمینان دارید؟')) return;
  try{
    const r = await fetch('/api/links/' + uid + '/reset_usage', {method:'POST'});
    if(r.ok){ toast('مصرف کانفیگ ریست شد ✓', 'ok'); loadLinks(); }
    else { toast('خطا در ریست مصرف', 'err'); }
  }catch(e){ toast('خطا در ارتباط با سرور', 'err'); }
}

// Protocol selector with rules enforcement
function selectProto(proto){
  document.getElementById('nl-proto').value = proto;
  document.querySelectorAll('.proto-card').forEach(c=>{
    c.classList.toggle('active', c.dataset.proto===proto);
  });
  // Show/hide protocol info
  document.querySelectorAll('.proto-info-item').forEach(el=>el.style.display='none');
  if(proto==='vless-ws') document.getElementById('proto-info-ws').style.display='block';
  else if(proto==='vless-grpc') document.getElementById('proto-info-grpc').style.display='block';
  else if(proto==='xhttp') document.getElementById('proto-info-xhttp').style.display='block';
  else if(proto==='trojan-ws'){ const trEl=document.getElementById('proto-info-trojan'); if(trEl) trEl.style.display='block'; }
  else if(proto==='socks5'||proto==='socks') {
    const s5El = document.getElementById('proto-info-socks5');
    if(s5El) s5El.style.display='block';
  }
  else if(document.getElementById('proto-info-custom')) document.getElementById('proto-info-custom').style.display='block';

  // Toggle custom URI field
  const rowCustom = document.getElementById('row-custom-uri');
  if(rowCustom) rowCustom.style.display = (proto === 'custom') ? 'block' : 'none';

  // Toggle advanced settings (Fragment / TLS / Clean IP / SNI / ALPN)
  const advWrap = document.getElementById('adv-settings-wrapper');
  if(advWrap) {
    advWrap.style.display = (proto === 'socks5' || proto === 'socks' || proto === 'custom') ? 'none' : 'block';
  }

  // Set default ALPN dropdown selection based on transport protocol
  const alpnEl = document.getElementById('nl-alpn');
  if(alpnEl){
    if(proto==='vless-grpc'){ alpnEl.value = 'h2'; }
    else { alpnEl.value = 'http/1.1'; }
  }
}

async function openLinkModal(uid=''){
  currentLinkId = uid;
  document.getElementById('link-modal-title').innerHTML = uid ? '<i class="ti ti-edit"></i> ویرایش کانفیگ' : '<i class="ti ti-link"></i> ساخت کانفیگ جدید';

  let targetLink = null;
  if(uid){
    const lr=await fetch('/api/links'),ld=await lr.json();
    targetLink = (ld.links||[]).find(l=>l.uuid===uid);
  }

  document.getElementById('nl-label').value = targetLink ? targetLink.label : '';
  document.getElementById('nl-val').value = targetLink ? (targetLink.limit_bytes / (1024**3)).toFixed(1) : 0;
  
  if(targetLink && targetLink.expires_at){
    try{
      const d = new Date(targetLink.expires_at);
      if(!isNaN(d.getTime())){
        const pad = n => String(n).padStart(2,'0');
        document.getElementById('nl-exp-date').value = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
      } else {
        document.getElementById('nl-exp-date').value = '';
      }
    }catch(e){ document.getElementById('nl-exp-date').value = ''; }
  } else {
    document.getElementById('nl-exp-date').value = '';
  }
  updateExpShamsi('nl');

  document.getElementById('nl-iplimit').value = targetLink ? targetLink.ip_limit : 0;
  document.getElementById('nl-note').value = targetLink ? (targetLink.note || '') : '';
  document.getElementById('nl-clean-ip').value = targetLink ? (targetLink.clean_ip || '') : '';
  document.getElementById('nl-sni').value = targetLink ? (targetLink.sni || '') : '';
  document.getElementById('nl-host').value = targetLink ? (targetLink.host || '') : '';
  document.getElementById('nl-fg-packets').value = targetLink ? (targetLink.fragment_packets || '') : 'tlshello';
  document.getElementById('nl-fg-len').value = targetLink ? (targetLink.fragment_length || '') : '';
  document.getElementById('nl-fg-interval').value = targetLink ? (targetLink.fragment_interval || '') : '';
  document.getElementById('nl-mux-concurrency').value = 8;
  document.getElementById('nl-custom-uri').value = targetLink ? (targetLink.custom_uri || '') : '';

  // Select protocol card
  selectProto(targetLink ? targetLink.protocol : 'vless-ws');

  // Override ALPN if targetLink has custom alpn
  if(targetLink && targetLink.alpn){
    document.getElementById('nl-alpn').value = targetLink.alpn;
  }

  // Close adv settings box by default
  document.getElementById('adv-settings-box').style.display = 'none';

  openModal('modal-link');
}

document.getElementById('form-link').addEventListener('submit',async e=>{
  e.preventDefault();
  const expVal = document.getElementById('nl-exp-date').value;
  const payload={
    label: document.getElementById('nl-label').value.trim(),
    protocol: document.getElementById('nl-proto').value||'vless-ws',
    clean_ip: document.getElementById('nl-clean-ip').value.trim()||"",
    limit_value: parseFloat(document.getElementById('nl-val').value)||0,
    limit_unit: document.getElementById('nl-unit').value,
    expires_at: expVal ? new Date(expVal).toISOString() : null,
    ip_limit: parseInt(document.getElementById('nl-iplimit').value)||0,
    note: document.getElementById('nl-note').value.trim(),
    clean_ip: document.getElementById('nl-clean-ip').value.trim(),
    sni: document.getElementById('nl-sni').value.trim(),
    host_header: document.getElementById('nl-host').value.trim(),
    alpn: document.getElementById('nl-alpn').value.trim(),
    fragment_packets: document.getElementById('nl-fg-packets').value.trim(),
    fragment_length: document.getElementById('nl-fg-len').value.trim(),
    fragment_interval: document.getElementById('nl-fg-interval').value.trim(),
    mux_enable: false,
    mux_concurrency: parseInt(document.getElementById('nl-mux-concurrency').value)||8,
    custom_uri: document.getElementById('nl-custom-uri').value.trim(),
  };

  const url = currentLinkId ? ('/api/links/' + currentLinkId) : '/api/links';
  const method = currentLinkId ? 'PATCH' : 'POST';

  try{
    const r=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(r.ok){
      toast(currentLinkId ? 'کانفیگ ویرایش شد ✓' : 'کانفیگ جدید ساخته شد ✓','ok');
      closeModal('modal-link');
      loadLinks();
    } else {
      toast('خطا در ذخیره کانفیگ','err');
    }
  }catch(e){toast('خطا در ارتباط با سرور','err')}
});

async function deleteLink(uid){
  if(!confirm('آیا از حذف این کانفیگ اطمینان دارید؟')) return;
  try{
    const r=await fetch('/api/links/'+uid,{method:'DELETE'});
    if(r.ok){toast('کانفیگ حذف شد','ok');loadLinks();}
  }catch(e){toast('خطا در حذف','err')}
}

// CONNECTIONS & LOGS
async function loadConns(){
  try{
    const r=await fetch('/api/connections'),d=await r.json();
    const el=document.getElementById('conns-table');
    if(!d.configs||!d.configs.length){
      el.innerHTML='<div style="text-align:center;padding:20px;color:var(--t3)">هیچ اتصال فعالی وجود ندارد.</div>';
      return;
    }
    el.innerHTML=`
      <table class="tbl">
        <thead><tr><th>کانفیگ</th><th>آی‌پی کلاینت</th><th>مصرف بایت</th><th>آخرین اتصال</th></tr></thead>
        <tbody>
          ${d.configs.map(c=>(c.connections||[]).map(ip=>`
            <tr>
              <td><strong>${esc(c.label)}</strong></td>
              <td><code>${esc(ip.ip)}</code></td>
              <td>${esc(ip.bytes_fmt)}</td>
              <td>${new Date(ip.last_connected_at||Date.now()).toLocaleTimeString('fa-IR')}</td>
            </tr>
          `).join('')).join('')}
        </tbody>
      </table>
    `;
  }catch(e){}
}

async function loadActivity(){
  try{
    const r=await fetch('/api/activity'),d=await r.json();
    const el=document.getElementById('logs-list');
    if(!d.logs||!d.logs.length){el.innerHTML='<div style="padding:20px;color:var(--t3)">لاگی ثبت نشده است.</div>';return}
    el.innerHTML=d.logs.slice().reverse().map(l=>`
      <div style="padding:8px 0;border-bottom:1px solid rgba(16,185,129,0.06);font-size:12px;display:flex;justify-content:space-between">
        <span><strong>[${l.kind}]</strong> ${esc(l.message)}</span>
        <span style="color:var(--t3)">${new Date(l.time).toLocaleTimeString('fa-IR')}</span>
      </div>
    `).join('');
  }catch(e){}
}

document.addEventListener('DOMContentLoaded',()=>{
  initChart();
  fetchStats();
  syncBackupSelection();
  setInterval(fetchStats,5000);
});
</script>
</body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب - سیستم اشتراک‌ها و کانفیگ‌های gRPC توسط FilterGosha با فونت وزیرمتن"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>FilterGosha Sub</title>
<link rel="icon" type="image/jpeg" href="/static/img/fg-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;font-family:'Vazirmatn',sans-serif !important}}
:root{{
  --bg:#060a14;--bg2:#0a1020;--bg3:#0d1428;
  --card:#0c1326;--card-b:rgba(16,185,129,0.14);--card-bh:rgba(16,185,129,0.3);
  --accent:#10b981;--accent2:#059669;--accent-d:rgba(16,185,129,0.1);
  --green:#10b981;--green-bg:rgba(16,185,129,0.12);--green-t:#34d399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.12);--red-t:#FB8585;
  --amber:#F2A33D;--amber-bg:rgba(242,163,61,0.12);--amber-t:#F9C988;
  --purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.12);--purple-t:#BCA4F7;
  --t1:#EFF4FF;--t2:#8AA0C4;--t3:#48577A;
  --radius:18px;--shadow:0 12px 40px rgba(0,0,0,0.45);
}}
html,body{{min-height:100%;background:var(--bg);font-family:'Vazirmatn',sans-serif !important;color:var(--t1);font-size:14px}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(16,185,129,0.14),transparent 62%),var(--bg);z-index:0;pointer-events:none}}
.grid-fx{{position:fixed;inset:0;background-image:linear-gradient(rgba(16,185,129,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.03) 1px,transparent 1px);background-size:46px 46px;z-index:0;pointer-events:none}}
.wrap{{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:24px 16px 64px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:26px;gap:10px}}
.brand{{display:flex;align-items:center;gap:11px}}
.brand-img{{width:40px;height:40px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(16,185,129,.35);flex-shrink:0}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{font-size:15px;font-weight:800;color:var(--t1)}}
.brand-name a{{color:inherit;text-decoration:none}}
.brand-sub{{font-size:9.5px;color:var(--accent);font-weight:600}}

.sub-info{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:24px;margin-bottom:16px;box-shadow:var(--shadow);position:relative;overflow:hidden}}
.sub-name{{font-size:22px;font-weight:800;color:var(--t1);margin-bottom:6px}}
.sub-desc{{font-size:12.5px;color:var(--t2);line-height:1.8;margin-bottom:14px}}
.sub-sub-box{{background:var(--accent-d);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.sub-sub-url{{font-family:ui-monospace,monospace;font-size:10.5px;color:var(--accent);word-break:break-all;flex:1}}

.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}}
.stat-card{{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 17px}}
.stat-label{{font-size:9px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:7px}}
.stat-val{{font-size:22px;font-weight:800;color:var(--t1);line-height:1}}
.stat-sub{{font-size:9.5px;color:var(--t3);margin-top:6px}}

.copy-all-bar{{display:flex;align-items:center;gap:12px;background:linear-gradient(120deg,var(--accent) 0%,#059669 100%);border-radius:18px;padding:16px 19px;margin-bottom:18px;box-shadow:0 10px 30px rgba(16,185,129,.28);flex-wrap:wrap}}
.copy-all-text{{flex:1;min-width:160px}}
.copy-all-title{{font-size:13.5px;font-weight:800;color:#fff;display:flex;align-items:center;gap:6px}}
.copy-all-sub{{font-size:10px;color:rgba(255,255,255,.8);margin-top:3px}}
.copy-all-btn{{background:#fff;color:#047857;border:none;border-radius:12px;padding:10px 19px;font-size:12.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;transition:.18s;white-space:nowrap}}
.copy-all-btn:hover{{transform:translateY(-1px)}}

.cfg-card{{background:var(--card);border:1px solid var(--card-b);border-radius:18px;margin-bottom:14px;overflow:hidden}}
.cfg-top{{padding:17px 19px 15px}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px;flex-wrap:wrap}}
.cfg-label{{font-size:14.5px;font-weight:800;color:var(--t1)}}
.cfg-status{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px}}
.cfg-status.ok{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status.no{{background:var(--red-bg);color:var(--red-t)}}
.ubar{{height:6px;border-radius:4px;background:rgba(16,185,129,0.1);overflow:hidden;margin-bottom:5px}}
.ubar-f{{height:100%;border-radius:4px;transition:width .5s ease}}
.utxt{{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}}
.cfg-bottom{{padding:15px 19px;border-top:1px dashed var(--card-b)}}
.cfg-vless{{background:rgba(0,0,0,.3);border:1px solid var(--card-b);border-radius:10px;padding:11px 13px;font-size:10px;font-family:ui-monospace,monospace;color:var(--accent);word-break:break-all;margin-top:9px}}

.btn{{font-size:11.5px;font-weight:700;border-radius:10px;padding:8px 15px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s}}
.btn-p{{background:linear-gradient(135deg,#10b981,#059669);color:#fff}}
.btn-g{{background:var(--accent-d);color:var(--accent);border:1px solid var(--card-b)}}

.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:700;opacity:0;transition:all .25s;z-index:999;pointer-events:none}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{background:var(--green-bg);color:var(--green-t);border-color:rgba(16,185,129,.4)}}

.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(6px)}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;text-align:center;max-width:320px;width:100%}}

.footer{{text-align:center;padding-top:28px;font-size:11px;color:var(--t3)}}
.footer a{{color:var(--accent);font-weight:700;text-decoration:none}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid-fx"></div>
<div class="toast" id="toast"></div>

<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div style="font-size:14px;font-weight:800;margin-bottom:14px" id="qr-label">QR Code</div>
    <div style="background:#fff;padding:12px;border-radius:14px;margin-bottom:14px"><img id="qr-img" src="" alt="QR" style="width:100%;display:block"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>

<div class="wrap">
  <div class="top">
    <div class="brand">
      <div class="brand-img"><img src="/static/img/fg-logo.jpg" alt="FilterGosha"></div>
      <div><div class="brand-name"><a href="https://t.me/FilterGosha" target="_blank">FilterGosha</a></div><div class="brand-sub">Secure Sub</div></div>
    </div>
  </div>
  <div id="root">
    <div style="text-align:center;padding:80px 20px;color:var(--t3)"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:32px"></i><br><br>در حال بارگذاری اشتراک...</div>
  </div>
  <div class="footer">پشتیبانی: <a href="https://t.me/filtergosha" target="_blank">@FilterGosha</a> · FilterGosha</div>
</div>

<script>
const UUID_KEY='{uuid_key}';

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show '+(type||'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

async function loadData(){{
  const r=await fetch('/api/public/sub/'+UUID_KEY);
  return r.json();
}}

function renderContent(d){{
  const activeCount=d.links.filter(l=>l.active).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub/' + UUID_KEY);

  window._fgSubUrl  = baseSubUrl;
  window._fgSubName = d.name;
  window._fgLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    label : l.label,
  }}));

  document.getElementById('root').innerHTML=`
    <div class="sub-info">
      <div style="font-size:10px;font-weight:700;color:var(--accent);text-transform:uppercase;margin-bottom:8px"><i class="ti ti-users-group"></i> اشتراک اختصاصی VLESS</div>
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div style="display:flex;gap:14px;font-size:10.5px;color:var(--t3);margin-bottom:14px;flex-wrap:wrap">
        <span><i class="ti ti-clock"></i> بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}</span>
        <span><i class="ti ti-calendar"></i> انقضا: <b style="color:var(--accent)">${{d.expires_at ? new Date(d.expires_at).toLocaleDateString('fa-IR', {{year:'numeric',month:'long',day:'numeric'}}) : 'نامحدود'}}</b></span>
      </div>
      
      ${{d.username ? `
      <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:10px 14px; border-radius:12px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
          <div>
              <div style="font-size:10px; color:var(--t3); margin-bottom:2px;">نام کاربری SOCKS5 (برای تنظیم دستی)</div>
              <div style="font-size:14px; font-weight:800; color:var(--t1); font-family:monospace; letter-spacing:1px;">${{esc(d.username)}}</div>
          </div>
          <button class="btn btn-g" style="padding:4px 10px;font-size:10px" onclick="navigator.clipboard.writeText('${{esc(d.username)}}').then(()=>toast('نام کاربری کپی شد ✓', 'ok'))"><i class="ti ti-copy"></i> کپی</button>
      </div>
      ` : ''}}
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(baseSubUrl)}}</span>
        <button class="btn btn-p" style="padding:6px 12px;font-size:10.5px"
          onclick="navigator.clipboard.writeText(window._fgSubUrl).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی لینک ساب
        </button>
        <button class="btn btn-g" style="padding:6px 12px;font-size:10.5px"
          onclick="showQR(window._fgSubName, window._fgSubUrl)">
          <i class="ti ti-qrcode"></i> QR
        </button>
      </div>
    </div>

    <div class="copy-all-bar">
      <div class="copy-all-text">
        <div class="copy-all-title"><i class="ti ti-copy"></i> کپی همه‌ی کانفیگ‌ها</div>
        <div class="copy-all-sub">تمام کانفیگ‌های فعال این اشتراک را یک‌جا کپی کن</div>
      </div>
      <button class="copy-all-btn" onclick="copyAllConfigs()"><i class="ti ti-clipboard-copy"></i> کپی همه (${{activeCount}})</button>
    </div>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">کانفیگ‌های فعال</div>
        <div class="stat-val">${{activeCount}}</div>
        <div class="stat-sub">از ${{d.links.length}} کانفیگ</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">اتصالات زنده</div>
        <div class="stat-val">${{d.active_connections}}</div>
        <div class="stat-sub" style="color:var(--green-t)">● آنلاین</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">کل مصرف / سهمیه</div>
        <div class="stat-val" style="font-size:16px;margin-top:2px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">سهمیه: ${{esc(d.limit_fmt)}}</div>
      </div>
    </div>

    <div style="font-size:12px;font-weight:800;color:var(--t2);margin-bottom:13px;display:flex;align-items:center;gap:6px"><i class="ti ti-link" style="color:var(--accent)"></i> کانفیگ‌های فعال (VLESS / SOCKS)</div>
    <div>
      ${{d.links.map((l, i) => {{
        const hasLimit = l.limit_bytes > 0;
        const pct = hasLimit ? Math.min(100, (l.used_bytes / l.limit_bytes) * 100) : 0;
        const bc  = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
        const lim = hasLimit ? fmtB(l.limit_bytes) : 'نامحدود (سقف اشتراک)';
        return `
          <div class="cfg-card">
            <div class="cfg-top">
              <div class="cfg-head">
                <div>
                  <div class="cfg-label">${{esc(l.label)}}</div>
                  <div style="font-size:10px;color:var(--accent);margin-top:4px"><i class="ti ti-route"></i> ${{esc(l.protocol.toUpperCase())}}</div>
                </div>
                <span class="cfg-status ${{l.active ? 'ok' : 'no'}}">${{l.active ? '● فعال' : '● غیرفعال'}}</span>
              </div>
              <div>
                <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}}"></div></div>
                <div class="utxt"><span>${{esc(l.used_fmt)}} مصرف شده</span><span>سهمیه: ${{lim}}</span></div>
              </div>
            </div>
            <div class="cfg-bottom">
              <div style="display:flex;align-items:center;justify-content:space-between">
                <span style="font-size:11px;font-weight:700;color:var(--t2)"><i class="ti ti-key"></i> لینک کانفیگ:</span>
                <div style="display:flex;gap:6px">
                  <button class="btn btn-p" onclick="navigator.clipboard.writeText(window._fgLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی</button>
                  <button class="btn btn-g" onclick="showQR(window._fgLinks[${{i}}].label, window._fgLinks[${{i}}].vless)"><i class="ti ti-qrcode"></i> QR</button>
                </div>
              </div>
              <div class="cfg-vless">${{esc(l.vless_link)}}</div>
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  setTimeout(() => autoRefresh(), 30000);
}}

function copyAllConfigs(){{
  const links=window._fgLinks||[];
  if(!links.length){{toast('کانفیگی برای کپی نیست','');return}}
  const text=links.map(l=>l.vless).join('\\n');
  navigator.clipboard.writeText(text).then(()=>toast('همه‌ی '+links.length+' کانفیگ کپی شد ✓','ok'));
}}

async function autoRefresh(){{
  try{{
    const data = await loadData();
    renderContent(data);
  }} catch(e) {{}}
}}

async function init(){{
  try{{
    const data = await loadData();
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML = '<div style="text-align:center;padding:40px;color:var(--red-t)"><i class="ti ti-alert-circle"></i> خطا در بارگذاری اطلاعات اشتراک</div>';
  }}
}}

init();
</script>
</body></html>"""
