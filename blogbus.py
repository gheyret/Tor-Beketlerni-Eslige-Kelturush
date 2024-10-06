import glob
import os
import re
import html
import shutil
import urllib.parse
from datetime import datetime
import requests
import time

#Header ghila qoshqandikin awu Googlening ID sini headerning ichidin izdeymiz
head_google_code = '''
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-143956760-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-143956760-1');
</script>
'''

index_stylesheet="""
@font-face {
	font-family: "UKIJ Tuz";
	font-weight: normal;
	src: local("UKIJ Tuz"), url("/UKIJTuz.ttf") format("TrueType"); /* non-IE */
}
body{
	font-size: 120%;
	font-family: UKIJ Tuz, UKIJ Basma, Boghda Tuz, UKIJ Nasq, Arial Unicode MS,Tahoma;
	text-align: justify;
}
a{
      text-decoration:none;
}
"""


tornami = "ئابىدە"
srcdir   = 'abeda.blogbus.com'
targetdir = 'abeda'

index_header =f'''
<html dir="RTL">
{head_google_code}
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<style type="text/css">
{index_stylesheet}
</style>
<title>{tornami}</title>
</head>
<body>
<h3 align="center">{tornami}(http://{srcdir}) نىڭ ئەسلىگە كەلتۈرۈلگەن مەزمۇنلىرى</h3>
<h3 align="center">($$$$ پارچە يازما)</h3>
<h3 align="center">({datetime.now().year}-يىلى {datetime.now().month}-ئاينىڭ {datetime.now().day}-كۈنى)</h3>
<hr align="middle" width="100%" size="3em" color="#559ee2">
<ul>
'''

index_footer ='''
</ul>
</body>
</html>
'''


index_footer ='''
</ul>
</body>
</html>
'''


tornami = " ئابىدە"
srcdir   = 'abeda.blogbus.com'
targetdir = 'abeda'


del_blk1 =''''''
remove_uls = [f'http://{srcdir}/',f'http://{srcdir}','<script src=http://bizning.blogbus.com/files/12168941251.js>']
remove_title = ['博客大巴',f'{tornami}']

re_title = re.compile('<title>(.*?)</title>', re.DOTALL)

def clean_title(orgTitle):

    strTitle = orgTitle.split('\n')[0]
    for str_r in remove_title:
        strTitle = strTitle.replace(str_r,'')

    ind = strTitle.rfind('-')
    if ind!=-1:
        strTitle=strTitle[:ind]

    strTitle = strTitle.replace('<<<','«').replace('>>>','»')
    strTitle = strTitle.replace('<<','«').replace('>>','»')
    strTitle = strTitle.replace('<','‹').replace('>','›')
    strTitle = strTitle.strip('').strip('-').strip()
    strTitle = re.sub('\\s+',' ',strTitle)    
    strTitle = strTitle.strip().strip('-').strip().strip('-').strip()
    return strTitle.strip()

re_clean_comm = re.compile('<!--.*?-->', re.DOTALL)

re_links =   re.compile("(href|src)[\\s]*=[\\s\"']*([^\"'>]*)[\"'].*?")
# re_links =   re.compile("(href|src)[\\s]*=[\\s\"']*([^\"'>]*)[\"']*?")

logs = set()

def process_links(mg):
    tag = mg.group(1)
    link = mg.group(2)

    # print(link)

    if link.startswith('http://') or link.startswith('https://'):
        pos = link.find('/',9)
        if pos!=-1:
            link = link[(pos+1):]
        else:
            link =""

        if link.find('.css')!=-1:
            link = link.split('/')[-1]
            # if link =='573621.css':
            #     link = '852510.css'

            link = 'blogbus/'+link

        elif link.find('.jpg')!=-1:
            link = 'blogbus/'+link.split('/')[-1]

        if link.endswith('.js'):
            link =""

        # print(link)
        if link.find(f'{targetdir}-logs/')!=-1:
            pos = link.find("#")
            if pos!=-1:
                link = link[:pos]

            link = link.replace(f'{targetdir}-logs/','logs_')
            logs.add(link)
    elif link.startswith('files/'):
        link = link.replace('files/s/','files/')

    else:
        
        if link.startswith('/'):
            link =link[1:]
            
        if link.endswith('/'):
            link = link[:-1]+'_index.html'
        
        if link.find('.html')!=-1:
            link = link.replace('/','_').strip('_')

        else:
            link = 'index.html'

    ret = tag+'="'+link+'"'
    return ret


def ProcessText(alltext):
    rettext = html.unescape(alltext)
    rettext = re_clean_comm.sub('',rettext)
    rettext = rettext.replace('ﯰ','ئۇ').replace('ﯬ','ئە').replace('ﯮ','ئو').replace('ﯪ','ئا')
    pos = rettext.find('</html>')
    if pos!=-1:
        rettext = rettext[:pos+7]

    rettext = re.sub('<!DOCTYPE.*?>','', rettext, flags=re.DOTALL)
    rettext = re.sub('<html.*?>','<html lang="ug">', rettext, flags=re.DOTALL)
    for url in remove_uls:
        rettext = rettext.replace(url,'')

    rettext=rettext.replace(del_blk1,'')
    rettext = re.sub('<iframe.*?</iframe>','', rettext, flags=re.DOTALL)
    rettext = re.sub('GS_googleAddAdSenseService.*?</script>','</script>', rettext, flags=re.DOTALL)
    rettext = re.sub('GA_googleAddSlot.*?</script>','</script>', rettext, flags=re.DOTALL)
    rettext = re.sub('GA_googleFillSlot.*?</script>','</script>', rettext, flags=re.DOTALL)
    rettext = re.sub('<object.*?</object>', '', rettext, flags=re.DOTALL)

    # rettext = re.sub('<script type="text/javascript">//<!\[CDATA\[.*</script></div>','', rettext,count=1,flags=re.DOTALL)

    rettext = re_links.sub(process_links,rettext)
    rettext = rettext.replace('<head>', head_google_code)
    return rettext



def MakePages():
    os.makedirs(targetdir,exist_ok=True)
    patstr = os.path.join(srcdir,'**','*.html*')
    files = glob.glob(patstr,recursive=True)
    for afile in files:
        if os.path.isdir(afile): 
            continue
        
        with open(afile,'r',encoding='utf_8_sig',errors='ignore') as fr:
            text = fr.read()

        newfile = os.path.basename(afile)
        dname = os.path.dirname(afile).replace(srcdir,'').strip('\\').replace('\\','_')
        if len(dname)>0:
            dname +='_'
    
        text = ProcessText(text)
        newfile = os.path.join(targetdir, dname+newfile)
        # print(newfile)
        with open(newfile,'w', encoding='utf-8') as nfp:
            nfp.write(text)
    
    return

re_numbers = re.compile(r'(\d+)')
def numericalSort(value): 
    parts = value.replace('-','_')
    parts = re_numbers.split(parts)
    parts[1::2] = map(int, parts[1::2])
    return parts

def getTitles():
    res ={}

    files = glob.glob(os.path.join(targetdir,'logs*.html'))
    # files=sorted(files, key=numericalSort)
    for afile in files:
        with open(afile,'r',encoding='utf-8') as fp:
            content  = fp.read()                        
        
        logs.discard(os.path.basename(afile))

        mawzular = re_title.findall(content.lower())
        if len(mawzular)>0 and len( mawzular[0].strip())>0:
            strTitle = clean_title(mawzular[0].strip())
            if strTitle is None:
                os.remove(afile)
            else:
                afile = afile.replace(targetdir+'\\','')
                if strTitle in res.values():
                    pass
                else:
                    res[afile] = strTitle
        else:
            os.remove(afile)

    sorted_res = sorted(res.items(), key=lambda x:x[1])

    return dict(sorted_res)

def GenerateIndex():
    mezmun=f'<li><a href="{targetdir}/index.html">{tornami}</a></li>\n'
    res = getTitles()
    for k,v in res.items():
        mezmun +='<li><a href="{}">{}</a></li>\n'.format(targetdir+'/'+k.replace('\\','/'),v)
    head = index_header.replace('$$$$',str(len(res)+1))
    mezmun = head + mezmun + index_footer
    indexname = targetdir+'.html'
    with open(indexname,'w', encoding='utf-8') as fp:
        fp.write(mezmun)

    print("Jemiy {} yazma uchun index.html hasil qilindi".format(len(res)))


def to_blogbus(mg):
    url = mg.group(1)
    return 'url('+url.split('/')[-1]+")"

def Downloadcss():
    url = 'https://web.archive.org/web/20140327013306cs_/http://public.blogbus.com/blogbus/skin_css/98/49/624998.css'
    tgt_dir = os.path.join(targetdir,'blogbus')
    os.makedirs(tgt_dir, exist_ok=True)
    tgt_file=os.path.join(tgt_dir,url.split('/')[-1])

    response = requests.get(url)
    response.encoding = 'utf-8'
    css_content = response.text
    response.close()

    re_url = re.compile('url\((.*?)\)', re.DOTALL)
    mathes = re_url.findall(css_content)
    for aurl in mathes:
        try:
            response = requests.get(aurl, allow_redirects=True)
            a_filenm =os.path.join(tgt_dir, aurl.split('/')[-1])
            with open(a_filenm,'wb') as f:                     
                f.write(response.content) 
            response.close()
        except:
            try:
                time.sleep(3)
                response = requests.get(aurl, allow_redirects=True)
                a_filenm =os.path.join(tgt_dir, aurl.split('/')[-1])
                with open(a_filenm,'wb') as f:                     
                    f.write(response.content) 
                response.close()
            except:
                print(f'xataliq: {aurl}')

    css_content = css_content.replace('UKIJ Tuz Tom','UKIJ Tuz').replace('UKIJ TUz Tom','UKIJ Tuz').replace('ukij tuz tom','UKIJ Tuz').replace('Uyghur Ekran','UKIJ Tuz').replace('Alpida Unicode System','UKIJ Tuz')
    
    css_content = re_url.sub(to_blogbus,css_content)

    with open(tgt_file, 'w', encoding='utf-8') as fp:
        fp.write(css_content)

def CopyFiles():

    folders = ['files']
    for fd in folders:
        patstr = os.path.join(srcdir, fd) + "\\**"
        files = glob.glob(patstr,recursive=True)
        for afile in files:
            if os.path.exists(afile)==False or os.path.isdir(afile):
                continue

            newfile = urllib.parse.unquote(afile).replace(srcdir,targetdir)
            ind = newfile.find('_ver=')
            if ind>0:
                newfile = newfile[:ind]
            elif newfile.find('_v=')>0:
                newfile = newfile[:newfile.find('_v=')]

            targetd = os.path.dirname(newfile)
            os.makedirs(targetd,exist_ok=True)
            shutil.copy2(afile, newfile)
            print(afile, '->', newfile)

    return

if __name__ == "__main__":
    CopyFiles()
    MakePages()
    GenerateIndex()
    # Downloadcss()

    with open('qalduq.txt','w',encoding='utf-8') as fp:
        fp.write(f'<li><a href="https://www.uyghur-archive.com/{targetdir}.html">{tornami}({srcdir})</a></li>\n')
        fp.write(f'https://web.archive.org/web/*/http://blogbus.com/{targetdir}-logs/*\n')

