$(document).ready(function () {
    $('#saveName').hide();
    let resultName = $('.NameResult').text();

    //저장하기
    $('.saveToMyPage').click(function () {
        $('.saveAlert').text(resultName);
        $('#saveName').css('display', 'flex');
    });

    //저장 알림창 닫기
    $('#box .close').click(function () {
        $('#saveName').hide();
        location.reload();
    });

});