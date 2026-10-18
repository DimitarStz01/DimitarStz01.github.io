"""Audit generated pages, local links, metadata and publication directives."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,json,re,xml.etree.ElementTree as ET
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.nodes=[];self.ids=set();self.text=[];self.scripts=[];self.stack=[];self.script='';self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.nodes.append((tag,a));self.ids.add(a.get('id'));self.stack.append(tag)
  if tag=='script':self.script=''
 def handle_endtag(self,tag):
  if tag=='script':self.scripts.append(self.script)
  if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
 def handle_data(self,data):
  if self.stack and self.stack[-1]=='script':self.script+=data
  elif 'style' not in self.stack:self.text.append(data)
 def attrs(self,tag,**filters):return [a for t,a in self.nodes if t==tag and all(a.get(k)==v for k,v in filters.items())]
def audit(root,production):
 files=[root/'index.html']+sorted(p for p in root.glob('*/index.html') if p.parent.name not in ['preview','assets','seo'])
 pages={p.resolve():Page(p.read_text()) for p in files};errors=[];titles=[];descriptions=[];canonicals=[];links=0
 def check(ok,msg):
  if not ok:errors.append(msg)
 for path,page in pages.items():
  name=str(path.relative_to(root));text=path.read_text();title=re.search(r'<title>(.*?)</title>',text,re.S);titles.append(title[1] if title else '')
  desc=page.attrs('meta',name='description');descriptions.append(desc[0].get('content','') if desc else '')
  check(len(desc)==1 and bool(descriptions[-1]),name+': description')
  check(len(page.attrs('h1'))==1,name+': H1')
  check(bool(page.attrs('html',lang='bg')),name+': language')
  canonical=page.attrs('link',rel='canonical');value=canonical[0].get('href','') if canonical else '';canonicals.append(value)
  check(len(canonical)==1 and value.startswith('https://magimil.bg/') and value.endswith('/'),name+': canonical')
  robots=page.attrs('meta',name='robots');check(len(robots)==1 and ('noindex' not in robots[0]['content'] if production else 'noindex' in robots[0]['content']),name+': robots')
  for key in ['og:title','og:description','og:url','og:image']:
   check(bool(page.attrs('meta',property=key)),name+': '+key)
  check(page.attrs('meta',property='og:url')[0]['content']==value,name+': OG canonical mismatch')
  for script in page.scripts:
   if script.startswith('{'):
    try:graph=json.loads(script);check(bool(graph.get('@graph')),name+': schema graph')
    except ValueError:errors.append(name+': invalid JSON-LD')
  visible=' '.join(page.text)
  check(not re.search(r'работен шаблон|дизайн концепция|визитк|ил[лю]*юстративен кадър|Контактите се потвърждават преди публикуване',visible,re.I),name+': unwanted visitor note')
  check(not page.attrs('span',**{'class':'photo-badge'}),name+': photo badge')
  for tag,a in page.nodes:
   if tag=='img':
    check('alt' in a,name+': missing image alt');check('width' in a and 'height' in a,name+': image dimensions')
    check(not any(x in a.get('src','') for x in ['magimil-card','magimil-equipment']),name+': reference business card')
   url=a.get('href') if tag in ['a','link'] else a.get('src') if tag in ['img','script'] else None
   if not url:continue
   u=urlsplit(url)
   if u.scheme or u.netloc:continue
   target=(path.parent/unquote(u.path)).resolve() if u.path else path
   if target.is_dir():target=target/'index.html'
   check(target.exists(),name+': missing local resource '+url);links+=1
   if tag=='a' and u.fragment and target in pages:check(unquote(u.fragment) in pages[target].ids,name+': missing anchor '+url)
   if tag=='a':check('index.html' not in u.path,name+': noncanonical internal URL '+url)
 check(len(files)==9,'Expected 9 content pages')
 check(len(set(titles))==len(files) and all(titles),'Unique page titles')
 check(len(set(descriptions))==len(files),'Unique descriptions')
 sitemap=ET.parse(root/'sitemap.xml');urls=[n.text for n in sitemap.findall('.//{*}loc')];check(set(urls)==set(canonicals),'Sitemap/canonical match')
 montage=pages[(root/'montazh/index.html').resolve()];gallery=[a['data-photo-title'] for tag,a in montage.nodes if 'data-photo-title' in a];check(gallery[-1]=='Монтаж на метален хънтър','Metal soffit photo must be last')
 return {'mode':'production' if production else 'local','pages':len(files),'localResourceChecks':links,'sitemapUrls':len(urls),'titles':titles,'passed':not errors,'errors':errors}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--production',action='store_true');args=p.parse_args();result=audit(args.root.resolve(),args.production);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['passed'] else 1)
