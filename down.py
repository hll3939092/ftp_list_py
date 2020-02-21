from ftplib import FTP

address = "ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/"
ftp = FTP("ftp.ncbi.nlm.nih.gov")
ftp.login('anonymous', '')
basePath = "/gene/DATA"
ftp.cwd("/gene/DATA")
file = open("EntrzeGene.txt", "w")

def is_bottom(thisdir):
    res = ftp.nlst(thisdir)
    for i in res:
        if ftp.dir(thisdir+'/'+i):
            return False
    return True


def get_all_files(next):
    paths = []
    for i in next:
        nn = ftp.nlst(i)
        if len(nn) > 1:
            paths.extend(get_all_files(nn))
        else:
            file.write(address+i+"\n")
            print(address+i)
            paths.append(nn)

    return paths



def is_dir(name):
    if ftp.dir(name) is not None:
        return True
    else:
        return False


if __name__ == '__main__':
    test = []
    res = ftp.nlst()
    for i in res:
        next = ftp.nlst(i)
        if len(next) > 1:
            test.extend(get_all_files(next))
        else:
            test.append(i)
    file.flush()
