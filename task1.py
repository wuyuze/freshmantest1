import urllib
import re
from sgmllib import SGMLParser
import os
class Getcontent(SGMLParser):
    def __init__(self):
        self.content=[]
        self.ti = False
        self.div = False
        self.getti = False
        self.gettext = False
        self.getimage =False
        self.title=''
        self.layer = 0
        self.mark=0
        SGMLParser.reset(self)

    def start_div(self,attrs):
        if self.div == True:
            self.layer +=1
            return
        for k,v in attrs:
            if k=='class' and v =='show-content':
                self.div = True
        for k,v in attrs:
            if k=='class' and v=='image-package imagebubble' :
                self.getimage = True
                return

    def end_div(self):
        if self.layer == 0:
            self.div = False
            return
        if self.div == True:
            self.layer -=1
            return

    def start_p(self, attrs):
        if self.div == False:
           return
        self.gettext = True

    def end_p(self):
        if self.gettext==True:
            self.gettext = False

    def handle_data(self,text):
        if self.gettext == True :
            self.content.append('        '+text+'\n')
        if self.getti == True:
            self.title=text
            self.content.append('                       '+text+'\n')
            self.content.append('================================================================================'+'\n')

    def start_title(self,attrs):
        self.getti = True
    def end_title(self):
        self.getti = False
    def start_img(self,attrs):
        if self.div ==False:
            return
        alt=[v for k,v in attrs if k=='alt']
        if alt:
            self.content.append('['+str(alt)[1:-1]+']')
        src=[v for k,v in attrs if k=='src']
        if src:
            self.content.append('[id:'+str(src)[1:-1]+']'+'\n')

    def savetomarkdown(self):
        f=open(str(self.title)+'.md','w')
        for i in self.content:
            print i
            f.write(str(i))
url1=[]
j=0
def geturl1(url):
    html = urllib.urlopen(url).read()
    reu=re.compile(r'a href=.*?target')
    html=re.findall(reu,html)
    for i in html:
        url1.append('http://www.jianshu.com'+str(i)[8:-8])
    
url2=[]


def geturl2(url):
    html = urllib.urlopen(url).read()
    reu=re.compile(r'slug=.*?data-pjax')
    reurl=re.findall(reu,html)
    global j
    for i in reurl:
        url2.append('http://www.jianshu.com/p/'+str(i)[6:-11])

#geturl1('http://www.jianshu.com/collection/723de9bac3cd')
url=('http://www.jianshu.com/collection/fcd7a62be697/top','http://www.jianshu.com/collection/NEt52a/top','http://www.jianshu.com/collection/723de9bac3cd')
#for m in url1:
#    geturl2(m)
#os.chdir('/home/wuyuze/python-1/theme1')
for n in range(3):
    geturl1(url[n])
    url11=list(set(url1))
    for m in url11:
        geturl2(str(m))
    os.mkdir('/home/wuyuze/python-1/theme'+str(n+1))
    os.chdir('/home/wuyuze/python-1/theme'+str(n+1))
    url22= list(set(url2))
    for m in range(100):
        print url22[m]
        content=Getcontent()
        content.mark=m+1
        htmlcontent=urllib.urlopen(str(url22[m])).read()
        content.feed(htmlcontent)
        content.savetomarkdown()
