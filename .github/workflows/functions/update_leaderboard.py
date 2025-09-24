import json, re, datetime, os, requests, bs4, difflib
from pathlib import Path

TAGS = ['FikFameica','Sheebah','AxeVille','UgandaMusic','EddyKenzo','Vinka','JoshBaraka','Kataleya','BoomplayUganda']

def tiktok_tracks(tag):
    url = f'https://www.tiktok.com/tag/{tag}'
    headers = {'User-Agent':'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
    except:
        return []
    data = []
    for span in soup.select('span[data-e2e="video-desc"]'):
        txt = span.get_text('|', strip=True)
        m = re.search(r'([A-Z][A-Za-z0-9\s]{2,25}-\s?[A-Za-z0-9\s]{2,25})', txt)
        if m:
            title = m.group(1).strip()
            view_tag = span.find_previous('strong')
            views = view_tag.text if view_tag else '0'
            data.append({'title': title, 'views': views, 'url': url})
    return data

def boomplay_trending():
    try:
        r = requests.get('https://mobile.boomplay.com/api/v1/trending', params={'country':'UG','type':'1'}, headers={'User-Agent':'BoomPlay/1200'}, timeout=15)
        return [{'title':item['songName'],'artist':item['artistName'],'url':f"https://boomplay.com/songs/{item['songId']}"} for item in r.json()['data']]
    except:
        return []

def normalise(t):
    return re.sub(r'\W+','',t.lower())

def main():
    old = json.loads(Path('public/leaderboard.json').read_text()) if Path('public/leaderboard.json').exists() else []
    new = []
    for t in TAGS:
        new += tiktok_tracks(t)
    bp = boomplay_trending()
    new += [{'title':f"{x['title']} {x['artist']}", 'source':'boomplay','url':x['url']} for x in bp]
    merged = []
    for n in new:
        for o in old:
            if difflib.SequenceMatcher(None, normalise(n['title']), normalise(o['title'])).ratio() > 0.85:
                n['views'] = o.get('views','0')
                break
        merged.append(n)
    for m in merged:
        v = m.get('views','0')
        num = float(re.sub(r'[^0-9.]','', v.replace('K','e3').replace('M','e6')) or 0)
        m['heatscore'] = int(num)
    merged = sorted(merged, key=lambda x: x['heatscore'], reverse=True)[:50]
    Path('public/leaderboard.json').write_text(json.dumps(merged, indent=2))

if __name__ == '__main__':
    main()
