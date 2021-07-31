#!env python3


from os.path import basename
from os.path import isdir
from os.path import splitext
from os      import system as cmd
from os      import chdir
from sys     import stdout,argv
from hashlib import sha256,sha1,md5
import requests as rs
import argparse as ar
class Checksum:
    @classmethod
    def sha256(self,fname,compare)->bool:
        if sha256(open(fname,"rb").read()).hexdigest == compare:
            return True
        else:
            return False
    @classmethod
    def sha1(self,fname,compare)->bool:
        if sha1(open(fname,"rb").read()).hexdigest == compare:
            return True
        else:
            return False
    @classmethod
    def md5(self,fname,compare)->bool:
        if md5(open(fname,"rb").read()).hexdigest == compare:
            return True
        else:
            return False
class DManager():
    def __init__(self,link,Output=None,Path=None,checksum=None,hstype=None):
        self.link = link
        self.Output = Output
        self.Path = Path
        self.checksum = checksum
        self.hstype = hstype
    def download(self):
        if not self.Path:
            pass
        elif self.Path and isdir(self.Path):
            chdir(self.Path)
        elif not isdir(self.Path):
            exit("{0} Not directory, or no such file".format(self.Path))
        x = rs.get(self.link,stream=True)
        size = x.headers.get('content-length')
        if self.Output:
            fname = self.Output
        else:
            fname = basename(self.link)
        try:
            with open(fname,'wb') as f:
                cmd("clear")
                print("Downloading {}".format(fname))
                print("Size : {}".format(self.calculate(int(size))))
                print("Type : {}".format(self.Type(basename(self.link))))
                if size is None:
                    f.write(x.content)
                else:
                    a = 0
                    size = int(size)
                    for b in x.iter_content(chunk_size=4096):
                        a += len(b)
                        c = int( 50 * a /size )
                        stdout.write("\r[{}{}] {}/{}".format('=' * c, '.' * (50-c),self.calculate(a),self.calculate(size)))
                        stdout.flush()
                        f.write(b)
                print("")
                if self.hstype == "sha256":
                    if not Checksum.sha256(fname,checksum):
                        print("Archive Corrupt")
                    else:
                        print("Archive isn't Corrupt")
                elif self.hstype == "md5":
                    if not Checksum.md5(fname,checksum):
                        print("Archive Corrupt")
                    else:
                        print("Archive isn't Corrupt")
                elif self.hstype == "sha1":
                    if not Checksum.sha1(fname,checksum):
                        print("Archive Corrupt")
                    else:
                        print("Archive isn't Corrupt")
                else:
                    pass
        except KeyboardInterrupt:
            exit("\nAborted.")
    def calculate(self,filesize=0) -> str:
        ukuran = "bit"
        if (filesize < 1000):
            ukuran = "byte"
            filesize = (filesize/1000)
        elif (filesize < 1000000):
            ukuran = "kB"
            filesize = (filesize/100000)
        elif (filesize >= 1000000):
            ukuran = "MB"
            filesize = (filesize/1000000)
        return "{0:.1f} {1}".format(filesize, ukuran)
    def Type(self,Xfname)->str:
        fname = splitext(Xfname)[1]
        ftype = {
            'codes': [ '.js', '.py', '.c','.sh'],
            'compressed': ['.zip', '.tar', '.rar','.xz','.gz','.lz4','.bz2'],
            'videos': ['.mp4', '.mov', '.avi'],
            'audios': ['.mp3', '.aac', '.opus','.ogg']
        }
        if fname in ftype['codes']:
            return "Script/Text File"
        elif fname in ftype['compressed']:
            return "Compressed File Archive"
        elif fname in ftype['videos']:
            return "Movie/Video File"
        elif fname in ftype['audios']:
            return "Music/Ringtone File"
        else:
            return "Binary/x-octet stream"



if __name__ == '__main__':
    z = ar.ArgumentParser()
    z.add_argument("--link",required=True,type=str,
                   help="Input a downloadable link to be downloaded")
    z.add_argument("--output",metavar='',
                   help="Output file name")
    z.add_argument("--path",metavar='',

                   help="Path to place the file")
    z.add_argument("--checksum",metavar='',
                   help="Verify downloaded file integrity")
    z.add_argument("--hashtype",metavar='',
                   help="required for checksum")
    t = z.parse_args()
    output = t.output
    link = t.link
    path = t.path
    checksum = t.checksum
    hashtype = t.hashtype
    if output and path and checksum and hashtype:
        DManager(link,output,path,checksum,hashtype).download()
    elif output and path:
        DManager(link,output,path).download()
    elif output:
        DManager(link,output).download()
    elif path:
        DManager(link,path).download()
    else:
        DManager(link).download
