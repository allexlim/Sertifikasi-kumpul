$(document).ready(function(){
    var pilihanEtalase = document.getElementById('pilihanEtalase')
    $('#pilihanEtalase').empty()
    $.ajax({
        data : {},
        type : 'POST',
        url : '/muatSemuaEtalasee'
    }).done(function(hasil){
        hasil.forEach(function(dat){
            var pilihan = document.createElement('option')
            pilihan.setAttribute('value', dat[0])
            pilihan.innerHTML = dat[1]
            pilihanEtalase.appendChild(pilihan)
        })
    })
})