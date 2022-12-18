from flask import Flask, request, jsonify # untuk import flask
from flask import session, redirect, url_for # untuk membuat session petugas dan menavigasi halaman
from flask import render_template as rt # untuk merender template HTML
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
    bukuId = request.form['bukuId']
    borrowerId = request.form['borroweId']
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

@app.route('/<bukuId>')
def bukuPage(bukuId):
    bukuTerpilih = buku(id=bukuId)
    bukuTerpilih.muatData()
    return rt("previewBook.html", id = bukuTerpilih.id, judul = bukuTerpilih.judul, sinopsis = bukuTerpilih.sinopsis, penulis = bukuTerpilih.penulis, tahun = bukuTerpilih.tahunTerbit , status = bukuTerpilih.statusKetersediaan)

if __name__ == "__main__":
  app.run(debug=True)