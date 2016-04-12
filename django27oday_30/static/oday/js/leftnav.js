var leftnav = leftnav ||{};
leftnav ={
   init:function(){
        this.classify();
    },
    classify:function(){
        $('.lesson-classfiy-nav li').bind("mouseover",changeWidth)
        function changeWidth(){
            var lessonList = $(this).find('.lesson-list-show');
            var a_len =  lessonList.find('div').length;
            var length = 400;
            var number = a_len*400;
            lessonList.width(number);
        };

        $('.lesson-classfiy-nav').bind("mouseover", changeHeight1)
        $('.lesson-classfiy-nav').bind("mouseout", changeHeight2)
        function changeHeight1(){
            var lessonHeight = $(this).height();
            $(this).find('ul').css({'height':'445px','overflow':'visible','borderBottom':'1px solid #e4e4e4'});
            $(this).find('p').removeClass('line');
        }
        function changeHeight2(){
            var lessonHeight = $(this).height();
            $(this).find('ul').css({'height':'298px','overflow':'hidden','borderBottom':'0'});
            $(this).find('p').addClass('line');
        }
        
    }
}

$(function(){
    leftnav.init();
})