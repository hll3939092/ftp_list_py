from ftplib import FTP

address = "ftp://ftp.ensembl.org/pub/release-98/genbank/"
ftp = FTP("ftp.ensembl.org")
ftp.login('anonymous', '')
# basePath = "/gene/DATA"
ftp.cwd("/pub/release-98/genbank")
ftp.set_pasv(True)
# file = open("GeneBank.txt", "w")
other_file = open("other_file.txt", "w")


def get_base_folder_list():
    base_list = ftp.nlst()
    for i in base_list:
        for j in ftp.nlst(i):
            print(address + j)
            other_file.write(address + j + "\n")

    other_file.flush()


if __name__ == '__main__':
    get_base_folder_list()
