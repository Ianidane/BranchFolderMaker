import os, sys, os.path
import datetime as dt 
import ftplib
import platform
import webbrowser
import shutil

OS=platform.system()

if OS == 'Windows':
    temploc = 'C:/Windows/Temp/'
#    print 'Make sure you have Wget.exe in your System32 folder(you can trust me). Do you want to download this now?'
#    yesno = raw_input()
#    if yesno in ('yes','Yes','y','Y'):
#        new = 2
#        url = 'http://nebm.ist.utl.pt/~glopes/wget/'
#        webbrowser.open(url,new=new)
else:
    temploc = '/tmp/'

date = dt.datetime.today().strftime("%y%m%d")

#can hardcode to make process easier
print 'What org?(abv)'
Org =raw_input()
print 'What is your name?'
name = raw_input()
FolderName=Org+'Test'+date+name
print 'Enter Host'
server = raw_input()
print 'User Name?'
username = raw_input()
print 'Password'
password = raw_input()

def download(FolderName, username, password, server, Org):
    if OS == 'Windows':
        os.system('"wget -r -P '+temploc+FolderName+' -nH --cut-dir=1 ftp://'+username+':'+password+'@'+server+'/'+Org+'Test/"')
    else:
        os.system('wget -r -P '+temploc+FolderName+' -nH --cut-dir=1 ftp://'+username+':'+password+'@'+server+'/'+Org+'Test/')

def uploadThis(path):
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            print 'uploading ' + f
	    fh = open(f, 'rb')
            myFTP.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + '/' + f):
            print 'makeing '+ f +' folder'
	    try:
                myFTP.mkd(f)
	    except ftplib.all_errors:
   	        print 'pass'
	        #folder already exists at destination
                pass
	    myFTP.cwd(f)
            uploadThis(path + '/' + f)
    myFTP.cwd('..')
    os.chdir('..')

print 'Downloading files'
download(FolderName, username, password, server, Org)

myFTP = ftplib.FTP(server)
myPath = temploc+FolderName
myFTP.login(username, password)
print 'Logging into server'
try:
    myFTP.mkd('Test'+name+'/'+FolderName)
except ftplib.all_errors:
    print 'pass'
	#folder already exists at destination
    pass

myFTP.cwd('Test'+name+'/'+FolderName)
print 'Uploading to server'
uploadThis(myPath) 
print 'Deleting local file'
shutil.rmtree(myPath)
print 'done'
#sys.exit
