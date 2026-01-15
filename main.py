from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemBytecodeCache

from app.jinja import env
from app.filters import hostname, shortdate, sitename, superscript, truncate
from app.helpers import load_articles
from app.local import DEBUG

app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.bytecode_cache = FileSystemBytecodeCache()
templates.env.filters['hostname'] = hostname
templates.env.filters['sitename'] = sitename
templates.env.filters['shortdate'] = shortdate
templates.env.filters['superscript'] = superscript
templates.env.filters['truncate'] = truncate

if DEBUG:
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def hot_resource():
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    articles_count = len(articles_list)
    domains = set(a['domain'] for a in articles_list)
    sites_count = len(domains)
    limit = sites_count // 2

    # Order by domain, -score, pub to mimic distinct(domain) behavior logic
    # Python sort is stable, so we sort in reverse order of importance:
    # 1. pub (asc)
    # 2. score (desc)
    # 3. domain
    articles_list.sort(key=lambda x: x['pub'])
    articles_list.sort(key=lambda x: x['score'], reverse=True)
    articles_list.sort(key=lambda x: x['domain'])

    distinct_entries = []
    seen_domains = set()
    for a in articles_list:
        if a['domain'] not in seen_domains:
            distinct_entries.append(a)
            seen_domains.add(a['domain'])

    # Now order by -score, pub
    distinct_entries.sort(key=lambda x: x['pub'])
    distinct_entries.sort(key=lambda x: x['score'], reverse=True)

    entries = distinct_entries[:limit]

    template = env.get_template('pages/main.html')
    html_content = template.render(
        entries=entries,
        articles=articles_count, sites=sites_count, view='hottest'
    )
    return HTMLResponse(content=html_content)


@app.get("/cold", response_class=HTMLResponse)
async def cold_resource():
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    articles_count = len(articles_list)
    domains = set(a['domain'] for a in articles_list)
    sites_count = len(domains)
    limit = sites_count // 2

    # Order by domain, -score, pub to mimic distinct(domain) behavior logic
    # Python sort is stable, so we sort in reverse order of importance:
    # 1. pub (asc)
    # 2. score (desc)
    # 3. domain
    articles_list.sort(key=lambda x: x['pub'])
    articles_list.sort(key=lambda x: x['score'])
    articles_list.sort(key=lambda x: x['domain'])

    distinct_entries = []
    seen_domains = set()
    for a in articles_list:
        if a['domain'] not in seen_domains:
            distinct_entries.append(a)
            seen_domains.add(a['domain'])

    # Now order by -score, pub
    distinct_entries.sort(key=lambda x: x['pub'])
    distinct_entries.sort(key=lambda x: x['score'])

    entries = distinct_entries[:limit]

    template = env.get_template('pages/main.html')
    html_content = template.render(
        entries=entries,
        articles=articles_count, sites=sites_count, view='coldest'
    )
    return HTMLResponse(content=html_content)


@app.get("/new", response_class=HTMLResponse)
async def new_resource():
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    articles_count = len(articles_list)
    domains = set(a['domain'] for a in articles_list)
    sites_count = len(domains)
    limit = sites_count // 2

    # Order by domain, -pub to mimic distinct(domain)
    # Sort keys in reverse importance:
    # 1. pub (desc)
    # 2. domain
    articles_list.sort(key=lambda x: x['pub'], reverse=True)
    articles_list.sort(key=lambda x: x['domain'])

    distinct_entries = []
    seen_domains = set()
    for a in articles_list:
        if a['domain'] not in seen_domains:
            distinct_entries.append(a)
            seen_domains.add(a['domain'])

    # Order by -pub
    distinct_entries.sort(key=lambda x: x['pub'], reverse=True)

    entries = distinct_entries[:limit]

    template = env.get_template('pages/main.html')
    html_content = template.render(
        entries=entries,
        articles=articles_count, sites=sites_count, view='newest'
    )
    return HTMLResponse(content=html_content)


@app.get("/read/{base}", response_class=HTMLResponse)
async def read_resource(base: str):
    articles = load_articles()
    entry = articles.get(base)

    if not entry:
        raise HTTPException(status_code=404, detail="Article not found")

    template = env.get_template('pages/read.html')
    html_content = template.render(
        entry=entry, view='read'
    )
    return HTMLResponse(content=html_content)


@app.get("/about", response_class=HTMLResponse)
async def about_resource():
    articles = load_articles()
    count = len(articles)
    sites = sorted(list(set(a['domain'] for a in articles.values())))
    template = env.get_template('pages/about.html')
    html_content = template.render(
        sites=sites, count=count, view='about'
    )
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
