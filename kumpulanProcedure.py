from function import *
def muatKoleksiBuku(kataKunci):
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('searchBook', [kataKunci])
    hasil = []
    for data in cursor.stored_results():
        hasil += data
    return hasil

def loginProcess(username, password):
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('loginPetugas', [username, password])
    hasil = []
    for dat in cursor.stored_results():
        hasil += dat
    if len(hasil) > 0:
        return 1
    else:
        return 0
