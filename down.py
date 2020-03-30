import math
import string
import time
from ftplib import FTP, Error
from random import random

address = "ftp://ftp.ensembl.org/pub/release-98/genbank/"
ftp = FTP("ftp.ensembl.org")
ftp.login('anonymous', '')
# basePath = "/gene/DATA"
ftp.cwd("/pub/release-98/genbank")
ftp.set_pasv(True)
file = open("GeneBank.txt", "w")

gather_file = []


def create_ftp():
    new_ftp = FTP("ftp.ensembl.org")
    new_ftp.login('anonymous', '')
    # basePath = "/gene/DATA"
    new_ftp.cwd("/pub/release-98/genbank")
    new_ftp.set_pasv(True)
    return new_ftp

def is_bottom(thisdir):
    res = ftp.nlst(thisdir)
    for i in res:
        if ftp.dir(thisdir + '/' + i):
            return False
    return True


base_url = "ftp.ensembl.org"
base_path = "/pub/release-98/genbank"

def create_base_ftp_client():
    base_ftp_client = FTP(base_url)
    base_ftp_client.login('anonymous', '')
    base_ftp_client.cwd(base_path)
    base_ftp_client.set_pasv(True)
    return base_ftp_client

def create_ftp_client_with_path(folder_path):
    base_ftp_client = FTP(base_url)
    base_ftp_client.login('anonymous', '')
    base_ftp_client.cwd(base_path+"/"+folder_path)
    base_ftp_client.set_pasv(True)
    return base_ftp_client


def recircuve_get_links(currnet_path, history_path):
    time.sleep(10)
    if history_path == "":
        new_ftp = FTP(base_url)
        new_ftp.login('anonymous', '')
        new_ftp.cwd(base_path + "/" + currnet_path)
        new_ftp.set_pasv(True)

        list = new_ftp.nlst()
        for i in list:

            if str(i).endswith(".gz"):
                # file.write("ftp://"+base_url + new_ftp.pwd() + "/" + i + "\n")
                gather_file.append("ftp://"+base_url + base_path + "/" + currnet_path + "/" + i + "\n")
                print("ftp://"+base_url + base_path + "/" + currnet_path + "/" + i + "\n")
            else:
                if new_ftp.dir(i):
                    recircuve_get_links(i, currnet_path)
                else:
                    # file.write("ftp://" + base_url + new_ftp.pwd() + "/" + i + "\n")
                    gather_file.append("ftp://" + base_url + base_path + "/" + currnet_path + "/" + i + "\n")
                    print("ftp://" + base_url + base_path + "/" + currnet_path + "/" + i + "\n")
        new_ftp.close()

    else:
        new_ftp = FTP(base_url)
        new_ftp.login('anonymous', '')
        new_ftp.cwd(base_path + "/" + history_path + "/" + currnet_path)
        new_ftp.set_pasv(True)

        list = new_ftp.nlst()
        for i in list:
            if str(i).endswith(".gz"):
                # file.write("ftp://"+base_url + new_ftp.pwd() + "/" + i + "\n")
                gather_file.append("ftp://" + base_url + base_path + "/" + history_path + "/" + currnet_path + "/" + i + "\n")
                print("ftp://"+base_url + base_path + "/" + history_path + "/" + currnet_path + "/" + i + "\n")
            else:
                if new_ftp.dir(i):
                    recircuve_get_links(i, history_path + "/" + currnet_path)
                else:
                    # file.write("ftp://" + base_url + new_ftp.pwd() + "/" + i + "\n")
                    gather_file.append("ftp://" + base_url + base_path + "/" + history_path + "/" + currnet_path + "/" + i + "\n")
                    print("ftp://" + base_url + base_path + "/" + history_path + "/" + currnet_path + "/" + i + "\n")
        new_ftp.close()






def get_links_main():
    base_ftp_client = create_base_ftp_client()
    base_list = base_ftp_client.nlst()
    for i in base_list:
        recircuve_get_links(i, "")

    for f in gather_file:
        file.write(f)

    file.flush()
    print("finish")





def get_all_files(next):
    paths = []
    for i in next:
        if str(i).endswith(".gz"):
            file.write(address + i + "\n")
            print(address + i)
            paths.append(address + i)
        else:
            new_ftp = create_ftp()
            nn = new_ftp.nlst(i)
            if len(nn) <= 1:
                file.write(address + i + "\n")
                print(address + i)
                paths.append(address + i)
            else:
                paths.extend(get_all_files(nn))

    return paths


def is_dir(name):
    if ftp.dir(name) is not None:
        return True
    else:
        return False


if __name__ == '__main__':
    get_links_main()


