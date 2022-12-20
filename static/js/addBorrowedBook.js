$(document).ready(function(){
    var selectBookId = document.getElementById('selectBookId')
    $('#selectBookId').empty()
    var selectBorrowerId = document.getElementById('selectBorrowerId')
    $('#selectBorrowerId').empty()
    $.ajax({
        data : {
            kataKunci : ''
        },
        type : 'POST',
        url : '/ambilKoleksiBukuTersedia'
    }).done(function(hasil){
        hasil.forEach(function(dat){
            var pilihan = document.createElement('option')
            pilihan.setAttribute('value', dat[0])
            pilihan.innerHTML = dat[1]
            selectBookId.appendChild(pilihan)
        })
    })

    $.ajax({
        data : {},
        type : 'POST',
        url : '/muatSemuaPeminjam'
    }).done(function(hasil){
        hasil.forEach(function(dat){
            var pilihan = document.createElement('option')
            pilihan.setAttribute('value', dat[0])
            pilihan.innerHTML = dat[1]
            selectBorrowerId.appendChild(pilihan)
        })
    })
})