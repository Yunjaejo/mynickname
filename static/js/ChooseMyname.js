$(document).ready(function () {

    $("input[id=ex_input]").keyup(function (event) {
        regexp = /[a-z0-9]|[ \[\]{}()<>?|`~!@#$%^&*-_+=,.;:\"'\\]/g;
        v = $(this).val();
        if (regexp.test(v)) {
            alert("한글만 해줄거야!");
            $(this).val(v.replace(regexp, ''));
        }
    });

//귀여운거^^
    $('#enter').mouseover(function () {
        $('#character img').attr('src', '../static/img/cuteCHAR.svg');
        $(this).addClass('buttonGradientAni');
    });
    $('#enter').mouseout(function () {
        $('#character img').attr('src', '../static/img/CHAR.svg');
        $(this).removeClass('buttonGradientAni');
    });

//고정단어 옵션
    let wordOption = $('.wordOption p');
    $(wordOption).click(function () {
        
        if ($(this).hasClass('off')) {
            $(this)
                .removeClass('off')
                .addClass('on');
            $(this)
                .siblings('p')
                .addClass('off')
                .removeClass('on');
        }
        if($('#optionCheck').hasClass('on')){
            $('.nounOption').removeClass('clickNoun');
        }else{$('.nounOption').addClass('clickNoun');}

        $('#ex_input').val('');
        $('#ex_input').focus();
        $('#ex_input').focusout();

        let word = $(this).text();
        if (word == '완전랜덤') {
            let labelText = `완전랜덤으로 내 이름을 정해줘!`;
            $("label[for='ex_input']").text(labelText);
            $('#ex_input').attr('readonly', true);
        } else {
            let labelText = `${word}를 원해!`;
            $("label[for='ex_input']").text(labelText);
            $('#ex_input').attr('readonly', false);
        }
        
        
    });

    

        



    
//고정단어 input 설정
    let input = $(' .textInput input')
    //focus on
    input.on('focus', function () {
        if ($(this).siblings('label') != null && $('.wordOption p:last-child').hasClass('off')) {
            $(this)
                .siblings('label')
                .css('opacity', 0);
        }
        if ($('.wordOption p:last-child').hasClass('off')) {
            $(this)
                .siblings('.textClear')
                .css('display', 'block');
        }
    });

    //focus out
    input.on('focusout', function () {
        if ($(this).val() == '' && $(this).siblings('label') != null) {
            $(this)
                .siblings('label')
                .css('opacity', '80%');
            $(this)
                .siblings('.textClear')
                .css('display', 'none');
        }
    });

    //input text clear
    $(' .textClear').click(function () {
        $(this)
            .siblings('input')
            .val('');
        $(this)
            .siblings('label')
            .click();
    });

//체크박스 클래스 추가+제거
    $('.checks input').click(function () {

        if ($(this).hasClass('on')) {
            $(this).removeClass('on');
            $(this).addClass('off');
        } else {
            $(this).removeClass('off');
            $(this).addClass('on');
        }
    });


 //Result Page
    $('#saveName').hide();
    let resultName = $('.NameResult').text();

    //저장하기
    $('.saveToMyPage').click(function () {
        $('#saveName').css('display', 'flex');
    });

    //저장 알림창 닫기
    $('#box .close').click(function () {
        $('#saveName').fadeOut();
        $('#saveName').hide();
        
    });

    //복사
    $('.Clip').click(function () {
        //클릭한 버튼의 형제 위치에 있는 p태그 안의 텍스트를 가져옵니다.
        // var copyText = $('.NameResult').text();

        // if (!navigator.clipboard) {
        //     fallbackCopyTextToClipboard(copyText);
        //     return
        // }
        // navigator
        //     .clipboard
        //     .writeText(copyText)
        //     .then(function () {
        //         // $('.ClipAlert').css('display','block');
        //         $('.ClipAlert').fadeIn(300).delay(400).fadeOut(400);
        //         console.log("success");
        //     }, function (err) {
        //         //복사 실패시
        //         console.error("fail", err);
        //     });
        var text = $('.NameResult').text();
navigator.clipboard.writeText(text).then(function() {
    $('.ClipAlert').css('display','block');
                 $('.ClipAlert').fadeIn(300).delay(400).fadeOut(400);
  console.log('Async: Copying to clipboard was successful!');
}, function(err) {
  console.error('Async: Could not copy text: ', err);
});
        
        
    });

    $('.Reset').click(function () {
        location.reload();
    });

});