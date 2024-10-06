import glob
import os
import re
import html
import shutil
import urllib.parse
from datetime import datetime

#Her bir torbeketni eslige kelturgende bu yerni ozgerting -->
srcdir   = 'www.alimkerim.com'
BASEURL = 'alimkerim.com'

targetdir = 'alimkerimtori'
tornami = "ئالىم كېرىم پەننى ئومۇملاشتۇرۇش بلوگى"
del_blk1 =''''''
remove_uls = [f'http://www.{BASEURL}/',f'http://www.{BASEURL}',f'http://{BASEURL}/',f'http://{BASEURL}','https://www.{BASEURL}/','https://www.{BASEURL}']
#<--Bu yergiche, bashqa yerlerni zoruryet tepilghanda ozgertse bolidu

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

remove_title = [f'{tornami}','']

re_title = re.compile('<title>(.*?)</title>', re.DOTALL)

# re_title = re.compile('<h1>(.*?)</h1>', re.DOTALL)

def clean_title(orgTitle):

    strTitle = orgTitle.split('\n')[0]
    strTitle = re.sub('\\s+',' ',strTitle).strip()

    if strTitle.rfind('|')!=-1:
        strTitle = strTitle[:strTitle.rfind('|')]

    for str_r in remove_title:
        strTitle = strTitle.replace(str_r,'').strip()


    strTitle = strTitle.strip('»').strip().strip('»')
    strTitle = strTitle.replace('<<<','«').replace('>>>','»')
    strTitle = strTitle.replace('<<','«').replace('>>','»').replace('‹‹','«').replace('››','»')
    strTitle = strTitle.replace('<','‹').replace('>','›')
    # strTitle = strTitle.strip('-').replace('___便利民博客 » blog archive » ','').replace('___便利民博客 »','').strip()
    strTitle = strTitle.strip('-').strip()

    if len(strTitle)==0:
        strTitle = None

    return strTitle


re_clean_comm = re.compile('<!--.*?-->', re.DOTALL)
re_links =   re.compile("(src|href)[\\s]*=[\\s]*[\"']([^\"'>]*?)[\"']")

def getID(strname, isfName=False):
    newname = urllib.parse.unquote(strname)
    ind = newname.find('#')
    if ind >= 0:
        newname = newname[:ind]

    if newname.startswith('index.php_'):
        newname = newname.replace('index.php','')
    
    if len(newname) == 0:
        return newname

    if newname[0] == '?':
        newname = '_'+ newname[1:]

    if newname == '_':
        newname = 'bash.html'

    elif newname.startswith('_'):
        newname = newname.replace('\\','')
        qr = urllib.parse.parse_qs(newname)
        if '_author' in qr:
            newname = 'aptor'+qr['_author'][0]
            if 'paged' in qr:
                newname = newname+'_bet'+qr['paged'][0]
            newname = newname + '.html'
        elif '_cat' in qr:
            newname = 'kat'+qr['_cat'][0]
            if 'paged' in qr:
                newname = newname+'_bet'+qr['paged'][0]
            newname = newname + '.html'
        elif '_category_name' in qr:
            newname = 'kat'+qr['_category_name'][0]
            if 'paged' in qr:
                newname = newname+'_bet'+qr['paged'][0]
            newname = newname + '.html'

        elif '_m' in qr:
            newname = 'waqit'+qr['_m'][0]
            if 'paged' in qr:
                newname = newname+'_bet'+qr['paged'][0]
            newname = newname + '.html'

        elif '_p' in qr:
            newname = 'yazma'+qr['_p'][0]
            if 'cpage' in qr:
                newname = newname+'_kat'+qr['cpage'][0]
            newname = newname + '.html'
        
        elif '_page_id' in qr:
            newname = 'yazmabet'+qr['_page_id'][0]
            newname = newname + '.html'

        elif '_paged' in qr:
            newname = 'bet'+qr['_paged'][0]
            newname = newname + '.html'

        elif '_tag' in qr:
            newname = qr['_tag'][0]
            newname = newname + '.html'
        else:
            newname = ''

    else:
        newname = newname.replace('\\','/').strip()
        if newname.find('replytocom=')!=-1:
            newname = newname[:newname.find('replytocom=')]
            newname = newname.strip('&').strip('_').strip('?')
    
        if newname.find('feed')!=-1 or newname.find('://')!=-1 or newname.find('.php')!=-1 or newname.find('.xml')!=-1:
            newname =''
        elif newname.endswith('.html'):
            newname = 'yazma'+newname[:-5]+'.html'
        elif newname.startswith('_p='):
            newname ='yazma'+newname[newname.find('_p=')+3:]+'.html'

        # elif newname.find('replytocom=')!=-1:
        #     # newname ='yazma'+newname.replace('replytocom=','_').replace('.html','')+'.html'
        #     ind = newname.find('.html')
        #     if ind!=-1:
        #         newname ='yazma'+newname[:ind]+'.html'
        #     else:
        #         print(newname)

        elif newname.startswith('date/'):
            newname ='waqit'+newname[newname.find('date/')+5:].replace('/','')+'.html'
        elif newname.startswith('201'):
            itms = newname.strip('/').split('/')
            if len(itms)>3:
                newname ='yazma'+itms[-1]+'.html'
            else:
                newname ='waqit'+newname.replace('/','')+'.html'
        elif newname.startswith('tag/'):
            newname = newname[newname.find('tag/')+4:].replace('/','')+'.html'
            
        elif newname.startswith('_tag='):
            newname = newname[newname.find('_tag=')+5:]+'.html'

        elif newname.startswith('_page_id='):
            newname = 'yazmabet'+newname[newname.find('_page_id=')+9:]+'.html'

        elif newname.startswith('page/'):
            newname = 'bet'+newname[newname.find('page/')+5:]+'.html'

        elif newname.startswith('_cat='):
            newname = 'kat'+newname[newname.find('_cat=')+5:]+'.html'
        elif newname.startswith('category/'):
            newname = 'kat'+newname[newname.find('category/')+9:]+'.html'

        elif newname.endswith('/'):
           newname = 'yazma'+newname[:-1]+'.html'

        elif newname.lower().endswith('.jpg') or newname.lower().endswith('.png') or newname.lower().endswith('.gif') or newname.lower().endswith('.ico'):
            pass
        else:
            itms = newname.split('/')
            if len(itms)>1:
                newname = 'yazma_'+itms[-1]+'.html'
            else:
                newname = 'yazma_'+itms[0]+'.html'

        newname = newname.replace('/','').replace('__','')
    return newname

def process_links(mg):
    tag = mg.group(1)
    link = mg.group(2)

    link = link.replace('index.php?','?').replace('/?','?')
    link = link.replace('index.php','/')

    ind = link.find('?ver=')
    if ind >0:
        link = link[:ind]
    if link.startswith('/'):
        link = link[1:]

    if len(link)==0 or link == '/':
        link = 'index.html'
    elif link.startswith('wp-content/'):
        if link.find('.php_src=')>0:
            link = link[link.find('.php_src=')+9:]
            if link.find('&')!=-1:
                link = link[:link.find('&')]

        elif link.find('src=wp-content/')!=-1:
            link = link[link.find('src=wp-content/')+4:]
            if link.find('&')!=-1:
                link = link[:link.find('&')]
    elif link.find('://')!=-1:
        link = ''

    elif link.startswith('wp-includes/') or link.startswith('images/') or link.find('.css')!=-1 or link.find('.js')!=-1  or link.find('.jpg')!=-1  or link.find('.png')!=-1 or link.find('.gif')!=-1 or link.find('.ico')!=-1:
        link = link.replace('themes/truemag/','themes/adapt/')
        pass
    
    elif link.startswith('wp-admin/') or link.find('wp-login.php')!=-1 or link.find('xmlrpc')!=-1:
        link = ""
    else:
        link = getID(link)

    ret = tag+'="'+link+'"'
    return ret

def ProcessText(alltext):
    rettext = html.unescape(alltext)
    rettext = re_clean_comm.sub('',rettext)
    rettext = re.sub('<!DOCTYPE html PUBLIC.*?>','', rettext, flags=re.DOTALL)
    rettext = re.sub('<html.*?>','<html lang="ug" dir="rtl">', rettext, flags=re.DOTALL)
    rettext = rettext.replace('charset=ISO-8859-1',' charset=UTF-8')

    rettext = re.sub('<!\[CDATA\[.*?\]\]>','', rettext, flags=re.DOTALL)

    pos = rettext.find('</html>')
    if pos!=-1:
        rettext = rettext[:pos+7]

    for url in remove_uls:
        rettext = rettext.replace(url,'')

    rettext=rettext.replace(del_blk1,'')

    # rettext = rettext.replace('wp-content/themes/thunder','wp-content/themes/prestansimple2.0.0').replace('//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js','')
    rettext = rettext.replace('//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js','')
    # rettext = rettext.replace('wp-content/themes//HotNewsPro/','wp-content/themes/muellimpro/') #.replace('wp-content/themes/checkerize/','wp-content/themes/prestansimple2.0.0/')
    # rettext = re.sub('(wp-content/themes/)(.*?/)','\\1muellimpro/', rettext, flags=re.DOTALL) #.replace('wp-content/themes/checkerize/','wp-content/themes/prestansimple2.0.0/')

    rettext = re_links.sub(process_links,rettext)
    rettext = rettext.replace('<head>', head_google_code)
    return rettext



#Word press ulanmilri boyichi bir terep qilish,
#ulanmilar munderije sheklide zapaslanghanda
def MakePages():
    os.makedirs(targetdir,exist_ok=True)
    patstr = os.path.join(srcdir, '**','*.html')
    files = glob.glob(patstr,recursive=True)

    repfiles = glob.glob(os.path.join(srcdir,'*.html_replytocom=*'))
    files.extend(repfiles)

    repfiles = glob.glob(os.path.join(srcdir,'index.php*'))
    files.extend(repfiles)

    for afile in files:
        if os.path.isdir(afile):
            continue

        newfile = afile.replace(srcdir,'')[1:]
        if newfile.find('=http_')!=-1 or newfile.startswith('search'):
            continue
        
        if newfile!='index.html':
            basedir = os.path.dirname(newfile)
            if len(basedir)>0:
                newfile = getID(basedir,True)
            else:
                bname = os.path.basename(afile)
                if bname.startswith('index.php'):
                    bname = bname.replace('index.php','')
                    newfile = getID(bname,True)
                    # if len(newfile) == 0:
                        # newfile = 'index.html'

                else:
                    newfile = getID(bname,True)

        if len(newfile) == 0:
            print(afile, '-> Yoq')
            continue
        
        with open(afile,'r',encoding='utf_8_sig',errors='ignore') as fr:
            text = fr.read()
                
        text = ProcessText(text)
        if text.find('>ئەخلەتخانا</a>')!=-1:
            print(afile, '-> Exlet')
            continue

        newfile = os.path.join(targetdir,newfile)
        with open(newfile,'w',encoding='utf-8') as fw:
            fw.write(text)

        print(afile, '->', newfile)

    return


def CopyResim():

    folders = ['wp-content','wp-includes','images','avatar','files','imgthm','qrcode','taxwikat']
    for fd in folders:
        patstr = os.path.join(srcdir, fd) + "\\**"
        files = glob.glob(patstr,recursive=True)
        for afile in files:
            if os.path.exists(afile)==False or os.path.isdir(afile):
                # targetd = os.path.join(targetdir,afile)
                # targetd = os.path.dirname(targetd)
                # os.makedirs(targetd,exist_ok=True)
                continue

            newfile = urllib.parse.unquote(afile).replace(srcdir,targetdir)
            ind = newfile.find('_ver=')
            if ind>0:
                newfile = newfile[:ind]
            elif newfile.find('_v=')>0:
                newfile = newfile[:newfile.find('_v=')]

            # targetd = os.path.join(targetdir,newfile)
            ind = newfile.find('timthumb.php_src=http_')
            if ind != -1:
                ind = newfile.rfind('wp-content')
                if ind !=-1:
                    newfile = newfile[ind:]
                    ind = newfile.find('&')
                    if ind !=-1:
                        newfile = newfile[:ind]
                        newfile = os.path.join(targetdir,newfile)

            targetd = os.path.dirname(newfile)
            os.makedirs(targetd,exist_ok=True)
            shutil.copy2(afile, newfile)
            print(afile, '->', newfile)

    return

re_numbers = re.compile(r'(\d+)')
def numericalSort(value): 
    parts = value.replace('-','_')
    parts = re_numbers.split(parts)
    parts[1::2] = map(int, parts[1::2])
    return parts

def getTitles():
    res ={}

    files = glob.glob(os.path.join(targetdir,'yazma*.html'))
    # files=sorted(files, key=numericalSort)
    for afile in files:
        with open(afile,'r',encoding='utf-8') as fp:
            content  = fp.read()

        mawzular = re_title.findall(content.lower())
        if len(mawzular)>0 and len( mawzular[0].strip())>0:
            strTitle = clean_title(mawzular[0].strip())
            if strTitle is None:
                # os.remove(afile)
                pass
            else:
                # afile = afile.replace(targetdir+'\\','')
                afile = os.path.basename(afile)
                if strTitle in res.values():
                    pass
                else:
                    res[afile] = strTitle
        else:
            # os.remove(afile)
            pass

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


if __name__ == "__main__":
    CopyResim()
    MakePages()
    GenerateIndex()
    # with open('qalduq.txt','w',encoding='utf-8') as fp:
    #     fp.write(f'<li><a href="https://www.uyghur-archive.com/{targetdir}.html">{tornami}({srcdir})</a></li>')


