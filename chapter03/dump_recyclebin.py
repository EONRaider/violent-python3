import os
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE


def sid_to_user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
                      "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
                      + '\\' + sid)
        value, _type = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except Exception as e:
        print(f'{"":>3}[-] Exception: {e}')
        return sid


def return_dir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycle_dir in dirs:
        if os.path.isdir(recycle_dir):
            return recycle_dir
    return None


def find_recycled(recycle_dir):
    dir_list = os.listdir(recycle_dir)
    for sid in dir_list:
        files = os.listdir(recycle_dir + sid)
        user = sid_to_user(sid)
        print(f'\n[*] Listing Files For User: {str(user)}')
        for file in files:
            print(f'[+] Found File: {str(file)}')


if __name__ == '__main__':
    recycled_dir = return_dir()
    find_recycled(recycled_dir)
