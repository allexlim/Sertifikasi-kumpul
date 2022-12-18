
var koleksiBuku = []
function muatUlangKoleksiData(){
    koleksiBuku = []
    var kontenKoleksiBuku = document.getElementById('kontenKoleksiBuku')
    $('#kontenKoleksiBuku').empty();
    $.ajax({
        data : {
            kataKunci : ""
        },
        type : "POST",
        url : '/ambilKoleksiBuku'

    }).done(function(data){
        //console.log(data)
        data.forEach(function(dat){
            var theWholeContent = document.createElement('a')
            theWholeContent.setAttribute('href', '/' + dat[0])
            
            var divKontenBuku = document.createElement('div')
            divKontenBuku.setAttribute('class', 'divKontenBuku')
            theWholeContent.appendChild(divKontenBuku)
            var theImage = document.createElement('img')
            theImage.setAttribute('class', 'gambarKonten')
            theImage.setAttribute('src', "/static/images/defaultBuku.png")
            divKontenBuku.appendChild(theImage)
            kontenKoleksiBuku.appendChild(theWholeContent)
            var theTitle = document.createElement('p')
            theTitle.innerHTML = dat[1]
            divKontenBuku.appendChild(theTitle)
        })
    })
}

$(document).ready(function() {
    muatUlangKoleksiData()
});