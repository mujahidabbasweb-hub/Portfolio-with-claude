"""Generates every page. Edit the SETTINGS block, then run:  python tools/build.py"""
import json, os, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- SETTINGS (edit these) ----------------
BASE = "https://mujahidabbasweb.netlify.app"
NAME = "Mujahid Abbas"
WA = "923219153891"
EMAIL = ""  # e.g. "you@example.com" (shows on the Contact page when set)
SOCIALS = {"GitHub": "", "LinkedIn": "", "Upwork": "", "Fiverr": "", "Facebook": "", "Instagram": ""}
LIVE = {"casameds": "https://casameds.com"}  # add other live URLs by project key (see PROJ)
ME = "/images/myimage/mujahid-abbas.jpg"  # JPG used for social cards and schema
STEM = "/images/myimage/mujahid-abbas"
DATE = "2026-10-14"
# -------------------------------------------------------

E = html.escape
def pic(stem, alt, w, h, eager=False):
    a = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<picture><source srcset="{stem}.webp" type="image/webp"><img src="{stem}.jpg" alt="{E(alt)}" width="{w}" height="{h}" {a}></picture>'
def fname(p): return "index.html" if p == "/" else p.strip("/").replace("/", "-") + ("" if p.endswith(".html") else ".html")
def clean(p): return "/" if p == "/" else "/" + fname(p)[:-5]
def rel(u):
    b, _, h = u.partition("#")
    b = b[1:] if b.startswith(("/assets", "/images")) else fname(b)
    return b + ("#" + h if h else "")
NAV = [("Home", "/"), ("About", "/about/"), ("Services", "/services/"), ("Projects", "/projects/"), ("Markets", "/markets/"), ("Blog", "/blog/"), ("Contact", "/contact/")]
SOC = {k: v for k, v in SOCIALS.items() if v}
WAURL = f"https://wa.me/{WA}?text=Hi%20Mujahid,%20I%20want%20to%20discuss%20a%20project!"
STACK = ["Laravel", "Flutter", "PHP / PDO", "MySQL", "REST APIs", "WordPress", "WooCommerce", "Firebase", "AI integrations"]

def faq(items):
    h = '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items) + "</div>"
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return h, ld

FAQ_GEN = [
    ("Who is Mujahid Abbas?", "Mujahid Abbas is a freelance AI web and mobile app developer from Pakistan. He builds Laravel web platforms, Flutter mobile apps, custom SaaS products and WordPress or WooCommerce sites for clients worldwide."),
    ("What services does Mujahid Abbas offer?", "He offers custom Laravel and PHP web apps, Flutter apps for Android and iOS, REST API development, AI feature integration, and WordPress and WooCommerce development with speed tuning."),
    ("Is Mujahid Abbas available for clients in the US, UK, UAE and Saudi Arabia?", "Yes. He works remotely with startups, agencies and enterprises in the United States, the United Kingdom, the UAE and Saudi Arabia, and builds Arabic and English interfaces for Gulf clients."),
    ("How do I start a project with Mujahid Abbas?", "Send a short brief through the Hire Me or Contact page. The message opens in WhatsApp, and he replies with questions and a rough plan."),
]
FAQ_SVC = [
    ("What is the difference between a Laravel web app and a WordPress site?", "A Laravel web app is custom-built for specific business logic such as bookings, billing or user roles. WordPress suits content sites and stores where existing plugins cover most needs."),
    ("Can one Flutter app run on both Android and iOS?", "Yes. Flutter uses a single codebase to build for both platforms, which usually reduces build time and maintenance effort compared with two native apps."),
    ("Can you add AI features to an existing product?", "Yes. Typical additions are chat assistants, content or document processing, and smart search, connected to your app through secure APIs."),
    ("Do you fix or speed up an existing website?", "Yes. Speed tuning, bug fixing and security hardening are available for WordPress, WooCommerce and Laravel projects."),
]
FAQ_HIRE = [
    ("How do I hire Mujahid Abbas?", "Fill in the brief on this page. It opens WhatsApp with your message ready to send, and the conversation continues there."),
    ("What should I include in my project brief?", "Describe your goal, who will use the product, the platforms you need (web, Android, iOS) and any deadline. A rough budget helps with planning."),
    ("Do you work on fixed-price projects or ongoing work?", "Both. A fixed scope suits a defined product, and ongoing remote work suits products that keep growing."),
    ("Will I own the code?", "Ownership terms are agreed in writing before work starts, so you know exactly what you receive."),
]

def cta(title="Have a project in mind?", text="Send a short brief and get a reply on WhatsApp with questions and next steps."):
    return f'''<div class="wrap" style="margin-top:clamp(40px,6vw,80px)"><div class="cta"><div><h2>{title}</h2><p style="margin-top:14px">{text}</p></div>
<div class="row"><a class="btn l" href="/hire-me/">Hire me</a><a class="btn g" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.35)" href="{WAURL}" target="_blank" rel="noopener">WhatsApp</a></div></div></div>'''

def bento():
    return '''<div class="bento">
<a class="bx w d" href="/services/#web"><span class="ic">W</span><h3>Custom web apps</h3><p>Laravel and PHP platforms with secure roles, clean data models and APIs your team can rely on.</p><ul class="chips"><li>Laravel</li><li>PHP / PDO</li><li>MySQL</li></ul></a>
<a class="bx" href="/services/#mobile"><span class="ic">F</span><h3>Flutter mobile apps</h3><p>One codebase for Android and iOS.</p></a>
<a class="bx" href="/services/#wp"><span class="ic">WP</span><h3>WordPress and WooCommerce</h3><p>Fast sites and stores built to convert.</p></a>
<a class="bx t" href="/services/#ai"><span class="ic">AI</span><h3>AI features</h3><p>Assistants, smart search and automation added to your product.</p></a>
<a class="bx" href="/services/#api"><span class="ic">API</span><h3>APIs and backends</h3><p>REST APIs that connect web, mobile and third-party tools.</p></a></div>'''

PROJ = [
 ("almalitha", "al-malitha-trading-contracting-website", 1376, 768, "Bilingual corporate website", "Al Malitha Trading & Contracting", "A responsive English and Arabic website for a GRP water tank and construction company, presenting waterproofing, industrial solutions and construction services.", ["English and Arabic versions", "Service sections for each business line", "Responsive on phone, tablet and desktop"], ["Corporate website", "Bilingual", "Responsive"]),
 ("casameds", "casameds-healthcare-website", 1376, 768, "Healthcare website", "Casameds", "A healthcare website for online consultations, prescription delivery and medicine delivery, with a customer account area.", ["Clear service pages for patients", "Customer login and account area", "Responsive on every device"], ["Healthcare", "Customer accounts", "Responsive"]),
 ("nishat", "ar-academy-nishat-learning-portal", 1376, 768, "Education portal", "AR Academy Nishat", "An interactive learning portal for a Cambridge, IGCSE and O-Level academy with faculty profiles, student success stories and online resources.", ["Faculty profile pages", "Student success stories", "Online resources for learners"], ["Education", "Learning portal", "Responsive"]),
 ("icsst", "icsst-safety-training-platform", 1376, 768, "Online training platform", "ICSST Safety Training", "A course platform for the Institute of Civil Safety and Security Training, presenting fire safety and emergency response courses with certification.", ["Course catalogue and dashboard", "Certification-focused content", "Built for professional learners"], ["E-learning", "Dashboard", "Certification"]),
 ("orhan", "orhan-contracting-website", 1536, 1024, "Contracting website", "Orhan Contracting", "A corporate website for a construction company covering residential, industrial and design and build services.", ["Service pages for each sector", "Project-led visual design", "Lead-focused contact flow"], ["Construction", "Corporate website", "Lead generation"]),
 ("gtc", "grand-arab-gtc-corporate-website", 1672, 941, "Corporate website", "Grand Arab (GTC)", "A corporate web presence for a Gulf-based business, with clean branding and a responsive layout.", ["Brand-led corporate design", "Responsive layout", "Built for the Gulf market"], ["Corporate website", "Gulf market", "Branding"]),
]
def case(i, p, flip=False):
    k, s_, w, h, tag, t, d, f, c = p
    live = LIVE.get(k)
    btn = f'<a class="btn p" href="{live}" target="_blank" rel="noopener">View live site</a>' if live else '<a class="btn p" href="/hire-me/">Build something similar</a>'
    return f'''<article class="case{' f' if flip else ''}"><div class="shot">{pic("/images/projects/" + s_, t + " website project by Mujahid Abbas", w, h)}</div>
<div><span class="tag">{tag}</span><h3>{E(t)}</h3><p>{d}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in f)}</ul>
<ul class="chips" style="margin-bottom:22px">{"".join(f"<li>{x}</li>" for x in c)}</ul>{btn}</div></article>'''
def work(n=None):
    return "".join(case(i, p, i % 2 == 1) for i, p in enumerate(PROJ[:n]))

MK = [
 ("usa", "Flutter and AI app developer for US startups", "Founders in New York, San Francisco, Austin and across the USA hire me to build Flutter mobile apps, Laravel SaaS platforms and AI features that ship fast and scale cleanly.", ["Flutter mobile app developer USA", "Laravel SaaS developer", "AI app developer for startups"]),
 ("uk", "AI app developer for London and UK businesses", "UK startups and agencies in London, Manchester and beyond use me for secure Laravel back ends, polished Flutter apps and AI integrations that fit real workflows.", ["AI app developer London", "Full-stack developer UK", "Flutter app developer UK"]),
 ("uae", "Laravel SaaS developer for Dubai and UAE companies", "I build bilingual Arabic and English web platforms and mobile apps for businesses in Dubai, Abu Dhabi and across the UAE, from SaaS dashboards to customer apps.", ["Laravel SaaS developer Dubai", "Flutter app developer UAE", "Bilingual website developer"]),
 ("ksa", "Full-stack developer for Saudi Arabia", "Companies in Riyadh, Jeddah and the Eastern Province can hire a remote full-stack developer for corporate websites, portals and mobile apps with Arabic and English support.", ["Web developer Saudi Arabia", "Mobile app developer Riyadh", "Arabic and English websites"]),
]
FAQ_MKT = [
 ("Can I hire a Laravel SaaS developer in Dubai remotely?", "Yes. Mujahid Abbas works remotely with companies in Dubai and across the UAE, and builds Arabic and English interfaces when your users need both."),
 ("Is there an AI app developer available for London startups?", "Yes. He adds AI features such as assistants and smart search to web and mobile products for UK startups, working remotely and coordinating over WhatsApp."),
 ("Do you build Flutter apps for US startups?", "Yes. Flutter apps for Android and iOS, with a Laravel or API backend, for startups and agencies in New York, San Francisco and across the USA."),
 ("Do you work with clients in Saudi Arabia?", "Yes. He builds corporate websites, portals and mobile apps for businesses in Riyadh, Jeddah and the wider Kingdom, with Arabic and English support."),
]
def teaser():
    c = "".join(f'<a class="bx" href="/markets/#{k}"><h3>{n}</h3><p>{t}</p></a>' for (k, t, _, _), n in zip(MK, ["USA", "United Kingdom", "UAE", "Saudi Arabia"]))
    return f'<div class="mkts">{c}</div>'


STEPS = '''<ol class="steps"><li><h3>Scope</h3><p>We agree on goals, users and what ships first.</p></li><li><h3>Design</h3><p>Screens and data model are planned before any code.</p></li><li><h3>Build</h3><p>Laravel or Flutter, tested on real devices as it grows.</p></li><li><h3>Launch</h3><p>Deployment, handover and fixes after go-live.</p></li></ol>'''

def form(budget=False):
    b = '<div class="fld"><label for="bd">Budget range</label><select id="bd" name="budget"><option value="">Not sure yet</option><option>Under $500</option><option>$500 to $2,000</option><option>$2,000 to $5,000</option><option>Above $5,000</option></select></div>' if budget else ""
    return f'''<div class="formbox" data-wa-form><div class="fld"><label for="nm">Your name</label><input id="nm" name="name" autocomplete="name" placeholder="Ayesha Khan"></div>
<div class="fld"><label for="ty">Project type</label><select id="ty" name="type"><option>Custom web app</option><option>Flutter mobile app</option><option>WordPress or WooCommerce site</option><option>AI feature</option><option>Something else</option></select></div>{b}
<div class="fld"><label for="ms">What do you need?</label><textarea id="ms" name="msg" placeholder="A booking system for my clinics, with an admin dashboard."></textarea></div>
<a class="btn l" data-wa-send href="{WAURL}" target="_blank" rel="noopener">Send on WhatsApp</a><p class="hint">Opens WhatsApp with your message filled in. Nothing is stored on this site.</p></div>'''

def person():
    p = {"@type": "Person", "@id": BASE + "/#person", "name": NAME, "url": BASE + "/", "image": BASE + ME, "jobTitle": "AI Web and Mobile App Developer",
         "description": "Freelance developer building Laravel web platforms, Flutter mobile apps, SaaS products and WordPress sites.",
         "address": {"@type": "PostalAddress", "addressCountry": "PK"},
         "knowsAbout": ["Laravel", "Flutter", "PHP", "MySQL", "REST APIs", "WordPress", "WooCommerce", "SaaS development", "AI applications"]}
    p["hasCredential"] = {"@type": "EducationalOccupationalCredential", "name": "Certificate of Professional Excellence in Web Development", "recognizedBy": {"@type": "Organization", "name": "NPXSOFT Engineering Group"}}
    if SOC: p["sameAs"] = list(SOC.values())
    return p

PAGES = []
def page(path, title, desc, body, ld=None, crumbs=None, og=None, ptype="website", is_home=False, nonindex=False):
    graph = [person()]
    if is_home:
        graph += [{"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": NAME + " Portfolio", "publisher": {"@id": BASE + "/#person"}, "inLanguage": "en"},
                  {"@type": "ProfessionalService", "name": NAME + ", Web and Mobile App Development", "url": BASE + "/", "image": BASE + ME, "areaServed": [{"@type": "Country", "name": c} for c in ["United States", "United Kingdom", "United Arab Emirates", "Saudi Arabia"]], "founder": {"@id": BASE + "/#person"},
                   "serviceType": ["Custom web application development", "Flutter mobile app development", "WordPress and WooCommerce development", "AI feature integration"]}]
    if crumbs:
        items = [("Home", "/")] + crumbs
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + clean(u)} for i, (n, u) in enumerate(items)]})
    if ld: graph += ld if isinstance(ld, list) else [ld]
    url = BASE + clean(path)
    og = og or ME
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if (u == path or (u != "/" and path.startswith(u))) else ""}>{n}</a>' for n, u in NAV)
    socials = "".join(f'<li><a href="{u}" target="_blank" rel="noopener me">{n}</a></li>' for n, u in SOC.items())
    mail = f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>' if EMAIL else ""
    robots = "noindex, follow" if nonindex else "index, follow, max-image-preview:large, max-snippet:-1"
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / ' + " / ".join(f'<a href="{u}">{E(n)}</a>' if i < len(crumbs) - 1 else E(n) for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("<!--CRUMBS-->", crumb_html)
    out = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="author" content="{NAME}"><meta name="robots" content="{robots}">
<link rel="canonical" href="{url}"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23C6F432'/%3E%3Ctext x='32' y='42' font-size='28' font-weight='800' text-anchor='middle' fill='%231D3306' font-family='sans-serif'%3EMA%3C/text%3E%3C/svg%3E">
<meta name="theme-color" content="#F5F7FB"><meta property="og:type" content="{ptype}"><meta property="og:site_name" content="{NAME} Portfolio"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE + og}"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE + og}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<script>try{{var t=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');document.documentElement.setAttribute('data-theme',t)}}catch(e){{document.documentElement.setAttribute('data-theme','dark')}}document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script></head>
<body data-wa="{WA}"><a class="skip" href="#main">Skip to content</a><div class="aura" aria-hidden="true"><i></i><i></i><i></i></div><canvas id="fx" aria-hidden="true"></canvas>
<header class="site"><div class="wrap bar"><a class="brand" href="/" aria-label="{NAME}, home"><b>MA</b>{NAME}</a>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn p" href="/hire-me/">Hire me</a></nav>
<button class="tt" id="tt" type="button" aria-label="Toggle dark mode"></button><button class="menu" id="menu" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">&#9776;</button></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="fg"><div><a class="brand" href="/"><b>MA</b>{NAME}</a><p class="muted" style="margin-top:14px;max-width:38ch">AI web and mobile app developer building Laravel platforms, Flutter apps and SaaS products. Available for freelance and remote work.</p></div>
<div><h3>Pages</h3><ul>{"".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV[1:] + [("Hire me", "/hire-me/")])}</ul></div>
<div><h3>Connect</h3><ul><li><a href="{WAURL}" target="_blank" rel="noopener">WhatsApp</a></li>{mail}{socials}</ul></div></div>
<div class="copy"><span>&copy; 2026 {NAME}. All rights reserved.</span><span>Web and mobile app developer, Pakistan</span></div></div></footer>
<script src="/assets/js/site.js" defer></script></body></html>'''
    f404 = lambda u: u if u.startswith(("/assets", "/images")) else (lambda b, h: clean(b) + (("#" + h) if h else ""))(*u.partition("#")[::2])
    out = re.sub(r'(href|src|srcset)="(/[^"]*)"', lambda m: f'{m.group(1)}="{(f404 if path == "/404.html" else rel)(m.group(2))}"', out)
    open(os.path.join(ROOT, fname(path)), "w", encoding="utf-8").write(out)
    if not nonindex: PAGES.append(path)

def ph(h1, lede):
    return f'<div class="wrap page-h"><!--CRUMBS--><h1>{h1}</h1><p class="lede">{lede}</p></div>'

# ---------------- HOME ----------------
fh, fl = faq(FAQ_GEN)
mq = "".join(f"<span>{s}</span>" for s in STACK)
page("/", "Mujahid Abbas | AI, Laravel & Flutter App Developer for US, UK & Gulf",
 "Hire Mujahid Abbas, a remote AI app, Laravel SaaS and Flutter mobile developer serving startups and enterprises in the USA, UK, UAE and Saudi Arabia.",
 f'''<div class="hero"><div class="wrap hg"><div><span class="pill"><i aria-hidden="true"></i>Open for freelance and remote work</span>
<h1>Mujahid Abbas: <span class="tw" data-words='["AI app developer","Laravel SaaS developer","Flutter app developer","full-stack developer"]'>AI app developer</span> for US, UK and Gulf businesses</h1>
<p class="lede">I design and build secure SaaS platforms, Flutter mobile apps and AI-powered products for startups and enterprises in the USA, UK, UAE and Saudi Arabia, delivered remotely with clear communication.</p>
<div class="row"><a class="btn p" href="/projects/">See my work</a><a class="btn g" href="{WAURL}" target="_blank" rel="noopener">Message on WhatsApp</a></div>
<ul class="facts"><li>Laravel and Flutter specialist</li><li>Secure by default</li><li>Fast delivery</li></ul></div>
<div class="por">{pic(STEM, "Portrait of Mujahid Abbas, AI web and mobile app developer", 1121, 1403, True)}<span class="chip a">Laravel</span><span class="chip b">Flutter</span><span class="chip c">Available now</span></div></div></div>
<div class="mq" aria-hidden="true"><div>{mq}{mq}</div></div>
<section><div class="wrap"><div class="head"><h2>What I build</h2><p>Websites, web apps, mobile apps and the APIs behind them, handled by one developer from database to launch.</p></div>{bento()}</div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>Featured projects</h2><p>Client websites and platforms built for construction, healthcare and education brands.</p></div>{work(3)}<a class="btn g" href="/projects/">All projects</a></div></section>
<section><div class="wrap"><div class="head"><h2>Serving clients worldwide</h2><p>Remote delivery for teams in four key markets.</p></div>{teaser()}</div></section>
<section><div class="wrap"><div class="head"><h2>How a project runs</h2><p>A simple path from first message to a live product.</p></div>{STEPS}</div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>What you can count on</h2></div><div class="trio"><div><h3>Fast, lean code</h3><p>Efficient implementations that keep pages quick and apps responsive.</p></div><div><h3>Secure by default</h3><p>Role-based access, sanitized inputs and safe API patterns protect your operations.</p></div><div><h3>Looks right everywhere</h3><p>Interfaces that stay clear on phones, tablets and desktops.</p></div></div></div></section>
<section><div class="wrap"><div class="head"><h2>Quick answers</h2></div>{fh}</div></section>{cta()}''',
 ld=[fl], is_home=True)

# ---------------- ABOUT ----------------
page("/about/", "About Mujahid Abbas | Laravel and Flutter Developer", "Learn how Mujahid Abbas, a Laravel and Flutter developer from Pakistan, builds secure, fast web and mobile products for freelance and remote clients.",
 f'''{ph("About Mujahid Abbas", "A developer focused on products that work reliably, look clear and keep growing.")}
<section style="padding-top:20px"><div class="wrap ab">{pic(STEM, "Mujahid Abbas at his desk, AI web and mobile app developer", 1121, 1403)}
<div><p class="ans"><strong>Mujahid Abbas</strong> is a freelance AI web and mobile app developer from Pakistan. He builds Laravel web platforms, Flutter mobile apps and custom SaaS products for clients worldwide.</p>
<p>I work with businesses that have a clear idea and need it built properly. That usually means a secure backend, a clean interface and an app that stays fast as more people use it.</p>
<p>My main tools are Laravel, PHP and MySQL for the web, Flutter for Android and iOS, and WordPress or WooCommerce when a content site or store is the better fit. I also add AI features such as assistants and smart search when they solve a real problem.</p>
<p>Every project starts with a short conversation about goals and users, so we build the right thing first.</p>
<div class="row"><a class="btn p" href="/hire-me/">Hire me</a><a class="btn g" href="/projects/">See my work</a></div></div></div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>How I work</h2></div><div class="trio"><div><h3>Clean code</h3><p>Readable structure that another developer can pick up without guessing.</p></div><div><h3>Secure build</h3><p>Role-based access, sanitized inputs and protected APIs from day one.</p></div><div><h3>Fast delivery</h3><p>A clear scope and regular updates keep projects moving.</p></div></div></div></section>
<section><div class="wrap"><div class="head"><h2>Technology I use</h2></div><ul class="stk">{"".join(f"<li>{s}</li>" for s in STACK)}</ul></div></section>
<section class="alt"><div class="wrap two"><div class="shot">{pic("/images/myimage/web-development-certificate", "Certificate of Professional Excellence in Web Development awarded to Mujahid Abbas by NPXSOFT Engineering Group, January 2026", 1600, 1131)}</div><div><h2>Credentials</h2><p class="muted" style="margin-top:14px">Certificate of Professional Excellence in Web Development, awarded by NPXSOFT Engineering Group in January 2026.</p></div></div></section>{cta()}''', crumbs=[("About", "/about/")],
 ld={"@type": "ProfilePage", "mainEntity": {"@id": BASE + "/#person"}})

# ---------------- SERVICES ----------------
sh, sl = faq(FAQ_SVC)
def sr(i, t, p, chips):
    return f'<article class="sr" id="{i}"><h3>{t}</h3><div><p>{p}</p><ul class="chips">{"".join(f"<li>{c}</li>" for c in chips)}</ul></div></article>'
page("/services/", "Services | Laravel SaaS, Flutter & AI App Development (US, UK, Gulf)", "Laravel SaaS platforms, Flutter mobile apps, AI features, REST APIs and WordPress or WooCommerce sites by Mujahid Abbas for clients in the USA, UK, UAE and Saudi Arabia.",
 f'''{ph("Web and mobile development services", "Everything from the database to the screen, handled by one developer.")}
<section style="padding-top:20px"><div class="wrap"><div class="svc">
{sr("web", "Custom web apps", "Laravel and PHP platforms with role-based access, clean data models, dashboards and reporting. Arabic and English bilingual builds are available for Gulf clients.", ["Laravel", "PHP / PDO", "MySQL", "SaaS"])}
{sr("mobile", "Flutter mobile apps", "One codebase for Android and iOS, with a polished interface and a solid backend. Built for real users on real phones.", ["Flutter", "Firebase", "REST API integration"])}
{sr("wp", "WordPress and WooCommerce", "Fast landing pages, custom themes, speed tuning and online stores set up to turn visitors into customers.", ["WordPress", "WooCommerce", "Speed tuning"])}
{sr("ai", "AI features", "Chat assistants, smart search and workflow automation added to your web or mobile product through secure APIs.", ["AI integrations", "Automation"])}
{sr("api", "APIs and backends", "Secure REST APIs that connect your web app, mobile app and third-party tools with consistent data.", ["REST APIs", "Authentication", "MySQL"])}
</div></div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>How a project runs</h2></div>{STEPS}</div></section>
<section><div class="wrap"><div class="head"><h2>Service questions</h2></div>{sh}</div></section>{cta()}''', crumbs=[("Services", "/services/")], ld=[sl])

# ---------------- PROJECTS ----------------
page("/projects/", "Projects | Corporate, Healthcare & E-learning Website Portfolio", "Client work by Mujahid Abbas: bilingual corporate sites, a healthcare platform, an e-learning portal and contracting websites for Gulf and international brands.",
 f'''{ph("Projects", "Selected products built end to end, from database design to the screens people use every day.")}
<section style="padding-top:20px"><div class="wrap">{work()}</div></section>{cta("Want a product like this?")}''', crumbs=[("Projects", "/projects/")], og="/images/projects/" + PROJ[0][1] + ".jpg",
 ld={"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[5]} for i, p in enumerate(PROJ)]})

# ---------------- BLOG ----------------
POSTS = [
 ("laravel-app-cost", "What affects the cost of a custom Laravel web app?", "The main cost drivers for a Laravel web app, and how to scope a project so the estimate stays realistic.",
  "A custom Laravel web app costs more or less depending on its features, user roles, integrations and design needs. There is no single price, but you can predict the range by listing what the app must do.",
  [("Features and user roles", "Every extra role, such as admin, staff or customer, adds screens, permissions and testing. List the roles first."),
   ("Integrations", "Payments, messaging, maps and AI services each need secure API work. Name the ones you need on day one."),
   ("Design and languages", "Bilingual interfaces and custom dashboards take more time than a single-language standard layout."),
   ("Scope control", "Launch with the core workflow, then add features in phases. This keeps the first release fast and the budget clear.")]),
 ("flutter-vs-native", "Flutter or native: which is right for your app?", "A plain comparison of Flutter and native development to help you choose for your next mobile app.",
  "Flutter is the better choice for most business apps that must run on both Android and iOS, because one codebase serves both. Native fits apps that depend heavily on platform-specific features.",
  [("When Flutter fits", "Business apps, dashboards, booking and school or clinic apps work well. You ship to both stores faster and maintain one codebase."),
   ("When native fits", "Apps built around advanced camera, sensors or platform-only features may need native code for the best result."),
   ("Backend matters equally", "Either way, a secure API and database decide how reliable the app feels. Plan the backend with the app."),
   ("How to decide", "List your must-have features and platforms. If both stores matter and features are standard, start with Flutter.")]),
]
def art(slug, title, desc, lead, secs):
    b = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in secs)
    page(f"/blog/{slug}/", title + " | Mujahid Abbas", desc,
     f'<div class="wrap page-h"><!--CRUMBS--><h1>{title}</h1><p class="meta">By {NAME} &middot; <time datetime="{DATE}">14 October 2026</time></p></div><section style="padding-top:10px"><div class="wrap art"><p class="ans">{lead}</p>{b}<p style="margin-top:34px"><a class="btn p" href="/hire-me/">Discuss your project</a></p></div></section>',
     crumbs=[("Blog", "/blog/"), (title, f"/blog/{slug}/")], ptype="article",
     ld={"@type": "BlogPosting", "headline": title, "description": desc, "datePublished": DATE, "dateModified": DATE, "author": {"@id": BASE + "/#person"}, "mainEntityOfPage": f"{BASE}/blog{slug}/", "image": BASE + ME})
for p in POSTS: art(*p)
cards = "".join(f'<a class="post" href="/blog/{s}/"><small>14 October 2026</small><h3>{t}</h3><p>{d}</p></a>' for s, t, d, _, _ in POSTS)
page("/blog/", "Blog | Web & Mobile App Development Guides", "Practical guides on Laravel, Flutter and web app planning by Mujahid Abbas.",
 f'{ph("Blog", "Practical answers about planning and building web and mobile products.")}<section style="padding-top:20px"><div class="wrap"><div class="posts">{cards}</div></div></section>{cta()}', crumbs=[("Blog", "/blog/")])

# ---------------- HIRE ME ----------------
hh, hl = faq(FAQ_HIRE)
page("/hire-me/", "Hire Mujahid Abbas | Freelance Laravel & Flutter Developer", "Hire Mujahid Abbas for a Laravel web app, Flutter mobile app or WordPress project. Send a brief and get a reply on WhatsApp.",
 f'''{ph("Hire a Laravel and Flutter developer", "Tell me what you want to build. You will get questions, a rough plan and next steps on WhatsApp.")}
<section style="padding-top:20px"><div class="wrap two"><div><div class="opt"><h3>Fixed-scope project</h3><p>A defined product such as a booking system, school app or store, delivered from design to launch.</p></div><div class="opt"><h3>Ongoing remote work</h3><p>A developer who joins your product and keeps shipping features and fixes.</p></div><div class="opt"><h3>Fix or speed up a site</h3><p>Bug fixes, speed tuning and security hardening for WordPress, WooCommerce or Laravel.</p></div></div>{form(True)}</div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>How a project runs</h2></div>{STEPS}</div></section>
<section><div class="wrap"><div class="head"><h2>Hiring questions</h2></div>{hh}</div></section>''', crumbs=[("Hire me", "/hire-me/")], ld=[hl])

# ---------------- CONTACT ----------------
soc = "".join(f'<p><strong>{n}:</strong> <a href="{u}" target="_blank" rel="noopener me">{u}</a></p>' for n, u in SOC.items())
page("/contact/", "Contact Mujahid Abbas | Web & Mobile App Developer", "Contact Mujahid Abbas on WhatsApp to discuss a Laravel, Flutter or WordPress project.",
 f'''{ph("Contact", "The fastest way to reach me is WhatsApp. Send a short message about your project.")}
<section style="padding-top:20px"><div class="wrap two"><div><p><strong>WhatsApp:</strong> <a href="{WAURL}" target="_blank" rel="noopener">+{WA}</a></p>{f'<p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>' if EMAIL else ""}{soc}
<p class="muted">Based in Pakistan. Available for freelance and remote work with clients worldwide.</p></div>{form()}</div></section>''', crumbs=[("Contact", "/contact/")],
 ld={"@type": "ContactPage", "url": BASE + "/contact/"})

# ---------------- MARKETS ----------------
mh, ml = faq(FAQ_MKT)
mk = "".join(f'''<article class="sr" id="{k}"><h2 style="font-size:1.6rem">{t}</h2><div><p>{d}</p><ul class="chips" style="margin-bottom:18px">{"".join(f"<li>{c}</li>" for c in ch)}</ul><a class="btn g" href="/hire-me/">Start a project</a></div></article>''' for k, t, d, ch in MK)
page("/markets/", "Hire a Full-Stack, Flutter & AI Developer | USA, UK, UAE, Saudi Arabia", "Remote Laravel SaaS, Flutter mobile and AI app development for startups and enterprises in the USA, UK, UAE and Saudi Arabia by Mujahid Abbas.",
 f'''{ph("Full-stack, mobile and AI developer for the US, UK and Gulf", "Remote delivery from Pakistan with clear communication on WhatsApp. Choose your market to see how I help.")}
<section style="padding-top:20px"><div class="wrap"><div class="svc">{mk}</div></div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>Questions from international clients</h2></div>{mh}</div></section>{cta()}''', crumbs=[("Markets", "/markets/")],
 ld=[ml, {"@type": "Service", "name": "Remote full-stack, Flutter and AI app development", "provider": {"@id": BASE + "/#person"}, "areaServed": [{"@type": "Country", "name": c} for c in ["United States", "United Kingdom", "United Arab Emirates", "Saudi Arabia"]]}])

# ---------------- 404 ----------------
page("/404.html", "Page not found | Mujahid Abbas", "This page does not exist.",
 '<div class="wrap page-h"><h1>Page not found</h1><p class="lede">The page you want has moved or never existed.</p><div class="row" style="margin-top:20px"><a class="btn p" href="/">Go home</a><a class="btn g" href="/projects/">See projects</a></div></div>', nonindex=True)

# ---------------- SEO / GEO files ----------------
sm = "".join(f"<url><loc>{BASE}{clean(p)}</loc><lastmod>{DATE}</lastmod></url>" for p in PAGES)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}/sitemap.xml\n")
open(os.path.join(ROOT, "llms.txt"), "w").write(f"""# {NAME}

> {NAME} is a freelance AI web and mobile app developer from Pakistan. He builds Laravel web platforms, Flutter mobile apps, custom SaaS products and WordPress/WooCommerce sites for clients worldwide.

## Key facts
- Role: AI web and mobile app developer (freelance, remote)
- Core stack: Laravel, PHP, MySQL, Flutter, REST APIs, WordPress, WooCommerce, Firebase
- Contact: WhatsApp +{WA}

## Pages
- [Home]({BASE}/): overview and quick answers
- [About]({BASE}/about): who he is and how he works
- [Services]({BASE}/services): web apps, Flutter apps, WordPress, AI features, APIs
- [Projects]({BASE}/projects): Al Malitha Trading & Contracting, Casameds, AR Academy Nishat, ICSST, Orhan Contracting, Grand Arab (GTC)
- [Markets]({BASE}/markets): USA, UK, UAE and Saudi Arabia
- [Blog]({BASE}/blog/): guides on Laravel cost and Flutter vs native
- [Hire me]({BASE}/hire-me): how to start a project
- [Contact]({BASE}/contact)
""")
open(os.path.join(ROOT, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/images/*\n  Cache-Control: public, max-age=31536000\n")
print("Built", len(PAGES), "pages")
