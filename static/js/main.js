$(document).ready(function(){

    //assign option
    let wordOption = $('.wordOption p');

    $(wordOption).click(function(){

        if($(this).hasClass('off')){
            $(this).removeClass('off').addClass('on');
            $(this).siblings('p').addClass('off').removeClass('on');
            
        }
        let word = $(this).text();
        if(word == '완전랜덤'){
            let labelText = `완전랜덤으로 내 이름을 정해줘!`;
            $("label[for='ex_input']").text(labelText);
            $('#ex_input').attr('readonly',true);
        }else{
            let labelText = `${word}를 원해!`;
            $("label[for='ex_input']").text(labelText);
            $('#ex_input').removeaAttr('readonly');
            $('#ex_input').attr('readonly',false);
        }
    });

    //input
    let input = $(' .textInput input')

    //focus on
    input.on('focus',function(){
        if($(this).siblings('label') != null && $('.wordOption p:last-child').hasClass('off')){$(this).siblings('label').css('opacity',0);}
        if($('.wordOption p:last-child').hasClass('off')){
            $(this).siblings('.textClear').css('display','block');
        }
    });

    //focus out
    input.on('focusout',function(){
        if($(this).val() == '' && $(this).siblings('label') != null){
            $(this).siblings('label').css('opacity','80%');
            $(this).siblings('.textClear').css('display','none');
        }
    });

    //input text clear
    $(' .textClear').click(function(){
        $(this).siblings('input').val('');
        $(this).siblings('label').click();
    });

    $('.checks input').click(function(){

        if($(this).hasClass('on')){
            $(this).removeClass('on');
        }else{
            $(this).addClass('on');
        }

    });


    

});