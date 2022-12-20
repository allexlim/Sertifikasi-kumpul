from function import *

def muatKoleksiBuku(kataKunci, status = 2): # Untuk mengqueri koleksi buku
    mySqlConnection = connectionData.newConnection() # Membuka koneksi
    cursor = mySqlConnection.cursor() # Untuk tempat queri
    cursor.callproc('searchBook', [kataKunci, status]) # memanggil prosedur
    hasil = [] # deklarasi tempat simpen hasil data nantinya
    for data in cursor.stored_results(): # .stored_results() PENTING untuk menampilkan hasil queri di database
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

def muatSemuaEtalase():
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('muatDataEtalase', [])
    hasil = []
    for dat in cursor.stored_results():
        hasil += dat
    return hasil

def muatSemuaBorrower():
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.execute("select * from tabelPeminjam")
    hasil = cursor.fetchall()
    return hasil