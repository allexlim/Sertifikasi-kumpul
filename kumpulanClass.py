from function import *
import datetime
from datetime import timedelta

class buku:
    def __init__(self, id = "", judul = "", penulis = "", tahunTerbit = "", etalase = "", statusKetersediaan = "", sinopsis = ""):
        self.id = id
        self.judul = judul
        self.penulis = penulis
        self.tahunTerbit = tahunTerbit
        self.etalase = etalase
        self.statusKetersediaan = statusKetersediaan
        self.sinopsis = sinopsis
    def muatData(self):
        mySqlConnection = connectionData.newConnection()
        cursor = mySqlConnection.cursor()
        cursor.callproc('getBook', [self.id])
        hasilTemp = []
        for i in cursor.stored_results():
            hasilTemp += i
        if len(hasilTemp) > 0:
            theData = hasilTemp[0]
            self.judul = theData[2]
            self.penulis = theData[3]
            self.tahunTerbit = theData[4]
            self.etalase = theData[1]
            self.statusKetersediaan = theData[6]
            self.sinopsis = theData[5]
        else:
            self.judul = "not found"
            self.penulis = "not found"
            self.tahunTerbit = "not found"
            self.etalase = "not found"
            self.statusKetersediaan = "not found"
            self.sinopsis = "not found"
    def daftarDatabase(self):
        mySqlConnection = connectionData.newConnection()
        cursor = mySqlConnection.cursor()
        cursor.callproc('addBook',[self.judul, self.penulis, self.tahunTerbit, self.sinopsis, self.etalase])
        mySqlConnection.commit()
        cursor.close()
        mySqlConnection.close()
        

class peminjam:
    def __init__(self, id = "", nama = "", listBuku = ""):
        self.id = id
        self.nama = nama
        self.listBuku = listBuku
    def muatDataIdentitas(self):
        mySqlConnection = connectionData.newConnection()
        cursor = mySqlConnection.cursor()
        cursor.callproc('getBorrower', [self.id])
        hasilTemp = []
        for i in cursor.stored_results():
            hasilTemp += i
        theData = hasilTemp[0]
        self.nama = theData[1]
    def muatData(self):
        self.muatDataIdentitas()


class petugas:
    def __init__(self, id = "", nama = ""):
        self.id = id
        self.nama = nama
    def muatData(self):
        mySqlConnection = connectionData.newConnection()
        cursor = mySqlConnection.cursor()
        cursor.callproc('getAdmin', [self.id])
        hasilTemp = []
        for i in cursor.stored_results():
            hasilTemp += i
        theData = hasilTemp[0]
        self.nama = theData[1]
    def catatPinjam(self, siPeminjam = peminjam() , siBuku = buku()):
        mySqlConnection = connectionData.newConnection()
        cursor = mySqlConnection.cursor()
        cursor.callproc('insertBorrowedbook',[siBuku.id, siPeminjam.id, self.id, datetime.date.today(), datetime.date.today() + timedelta(days=7)])
        mySqlConnection.commit()
        mySqlConnection.close()
    def ubahStatus(self):
        mySqlConnection = connectionData.newConnection()
        cursor = mySqlConnection.cursor()
        cursor.callproc('', [])