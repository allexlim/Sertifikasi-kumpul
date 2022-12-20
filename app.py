from flask import Flask, request, jsonify 
from flask import session, redirect, url_for 
from flask import render_template as rt 
from kumpulanProcedure import * 
from kumpulanClass import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SERTIFIKASI' #untuk mendukung pembuatan session

@app.route('/')
def main():
    return redirect(url_for("home"))

@app.route('/login', methods=['POST', 'GET']) 
def login():
    if session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if loginProcess(username, password) == 1:
                session['userId'] = username
                return redirect(url_for('menuPilihan'))
            else:
                return rt("login.html", error = 'username / password incorrect')
        else:
            return rt("login.html")

@app.route('/logout', methods = ['POST'])
def logout():
    if session:
        session.pop("userId", None)
    return redirect(url_for('login'))

@app.route('/addBorrowedBook')
def addBorrowedBook():
    todayDate = datetime.date.today()
    returnDate = datetime.date.today() + timedelta(days=7)
    return rt("addBorrowedBook.html", todayDate = todayDate, returnDate = returnDate)

@app.route('/daftarBorrowedBook', methods = ['POST'])
def daftarBorrowedBook():
    siPetugas = petugas(id=session['userId'])
    bukuId = request.form['selectBookId']
    borrowerId = request.form['selectBorrowerId']
    siBuku = buku(id=bukuId)
    siBuku.muatData()
    pp = peminjam(id=borrowerId)
    pp.muatData()
    siPetugas.muatData()
    siPetugas.catatPinjam(siBuku=siBuku, siPeminjam=pp)
    return redirect(url_for("addBorrowedBook"))
    

@app.route('/menuPilihan')
def menuPilihan():
    if session:
        return rt("pilihan.html")
    else:
        return redirect(url_for('login'))

@app.route('/home', methods=['POST', 'GET'])
def home():
    return rt("home.html")

@app.route('/ambilKoleksiBuku', methods=['POST'])
def ambilKoleksiBuku():
    kataKunci = request.form['kataKunci']
    kumpulanBuku = muatKoleksiBuku(kataKunci)
    return jsonify(kumpulanBuku)

@app.route('/ambilKoleksiBukuTersedia', methods=['POST'])
def ambilKoleksiBukuTersedia():
    kataKunci = request.form['kataKunci']
    kumpulanBuku = muatKoleksiBuku(kataKunci, status=1)
    return jsonify(kumpulanBuku)

@app.route('/<bukuId>')
def bukuPage(bukuId):
    bukuTerpilih = buku(id=bukuId)
    bukuTerpilih.muatData()
    return rt("previewBook.html", id = bukuTerpilih.id, judul = bukuTerpilih.judul, sinopsis = bukuTerpilih.sinopsis, penulis = bukuTerpilih.penulis, tahun = bukuTerpilih.tahunTerbit , status = bukuTerpilih.statusKetersediaan)

@app.route('/tambahBukuPage')
def tambahBukuPage():
    return rt('addBook.html')

@app.route('/tambahkanBuku', methods=['POST'])
def tambahkanBuku():
    judul = request.form['newJudul']
    penulis = request.form['newPenulis']
    tahunTerbit = request.form['newTahunTerbit']
    pilihanEtalase = request.form['pilihanEtalase']
    sinopsis = request.form['sinopsis']
    newBuku = buku(judul=judul,penulis=penulis,tahunTerbit=tahunTerbit,etalase=pilihanEtalase,sinopsis=sinopsis)
    newBuku.daftarDatabase()
    return redirect(url_for('tambahBukuPage'))

@app.route('/muatSemuaEtalasee', methods=['POST'])
def muatSemuaEtalasee():
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('muatDataEtalase', [])
    hasil = []
    for dat in cursor.stored_results():
        hasil += dat
    return jsonify(hasil)

@app.route('/muatSemuaPeminjam', methods=["POST"])
def muatSemuaPeminjam():
    hasil = muatSemuaBorrower()
    return jsonify(hasil)

@app.route('/editBuku-<idBuku>')
def editBuku(idBuku):
    con = connectionData.newConnection()
    cursor = con.cursor()
    cursor.execute(f"select id, judul, penulis, tahun_terbit, sinopsis, etalase from tabelBuku where id = '{idBuku}'")
    hasil = cursor.fetchall()
    etalaseSemua = muatSemuaEtalase()
    return rt("editBuku.html", theData = hasil[0], DataEtalase = etalaseSemua)

@app.route('/mulaiEditBuku', methods = ["POST"])
def mulaiEditBuku():
    idBukuu = request.form['idBuku']
    newJudul = request.form['newJudul']
    newPenulis = request.form['newPenulis']
    newTahunTerbit = request.form['newTahunTerbit']
    newSinopsis = request.form['newSinopsis']
    newEtalase = request.form['pilihanEtalase']
    con = connectionData.newConnection()
    cursor = con.cursor()
    cursor.callproc('updateBuku', [idBukuu, newJudul, newPenulis,newTahunTerbit,newSinopsis,newEtalase])
    con.commit()
    return redirect(url_for('editBuku', idBuku = idBukuu))

@app.route('/tampilkanPeminjamDenganBuku')
def tampilkanPeminjamDenganBuku():
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('borrowerWithBorrow', [''])
    hasil = []
    for data in cursor.stored_results():
        hasil += data
    return rt("borrower.html", theData = hasil)

@app.route('/tampilkanTabelBukuPinjam')
def tampilkanTabelBukuPinjam():
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('showTabelBukuPinjam', [])
    hasil = []
    for data in cursor.stored_results():
        hasil += data
    return rt("tabelBukuPinjam.html", theData = hasil)

@app.route('/kembalikanTabelBukuPinjam-<idPinjam>')
def kembalikanTabelBukuPinjam(idPinjam):
    mySqlConnection = connectionData.newConnection()
    cursor = mySqlConnection.cursor()
    cursor.callproc('bukuKembali', [idPinjam])
    mySqlConnection.commit()
    mySqlConnection.close()
    return redirect(url_for('tampilkanTabelBukuPinjam'))

if __name__ == "__main__":
  app.run(debug=True)