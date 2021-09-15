$(document).ready(function(){

    //.copySave버튼 클릭시 형제태그인 p태그의 텍스트를 복사합니다.
    $('.copySave').click(function(){
        //클릭한 버튼의 형제 위치에 있는 p태그 안의 텍스트를 가져옵니다.
        var copyText = $(this).siblings('p').text();
        
        if(!navigator.clipboard){
            fallbackCopyTextToClipboard(copyText);
            return
        }
        navigator.clipboard.writeText(copyText).then(
            function(){
                //복사 성공시
                console.log("success");
            },
            function(err){
                //복사 실패시
                console.error("fail",err);
            }
        );
    });
    
});