import os
import patoolib
import psutil
import hashlib


def get_md5(path):
    with open(path, 'rb') as f:
        md5obj = hashlib.md5()
        while True:
            data = f.read(4096)
            if len(data) == 0:
                break
            md5obj.update(data)
    return md5obj.hexdigest()


def get_all_file(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        #root 当前目录路径、dirs 当前路径下所有子目录、 file 当前路径下所有非目录子文
        for file in files:
            file_list.append(f"{root}/{file}")
    return file_list


_magic_dict = (
    b'\x1f\x8b\x08',                #"gz",
    b'\x42\x5a\x68',                #"bz2"
    b'\x50\x4b\x03\x04',            #"zip"
    b'\x37\x7A\xBC\xAF\x27\x1C ',   #"7z",
    b'\x52\x61\x72\x21'             #"rar"
)

_max_len = max(len(x) for x in _magic_dict)


def _is_compress(filename: str):
    with open(filename, mode="rb") as f:
        file_start = f.read(_max_len)
    for magic in _magic_dict:
        if file_start.startswith(magic):
            return True
    return False


def test_compress(filename: str):
    patoolib.test_archive(filename, verbosity=1)


def uncompress(filename:str, dpath):
    patoolib.extract_archive(filename, outdir=dpath)


def find_and_uncompress(srcpath: str, dpath: str = None):
    file_list = []
    if os.path.isdir(srcpath):
        file_list += get_all_file(srcpath)
    elif os.path.isfile(srcpath):
        file_list.append(srcpath)

    dpath = dpath[0:len(dpath)-1] if dpath[len(dpath)-1] == "/" else dpath
    if not os.path.isdir(dpath):
        os.mkdir(dpath)

    for file in file_list:
        if _is_compress(file):
            fbname = os.path.basename(file)
            unfbname = os.path.splitext(fbname)[0]
            uncompress(file, f"{dpath}/{unfbname}")


