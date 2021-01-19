$(function(){
   //初始化数据列表
  function initList(){
      $.ajax({
        type:"get",
        url:"/lists",
        dataType:"json",
        success:function(data){           
            var html = template('indexTpl',{list:data});
            $("#dataList").html(html);          
        }
      });
  };
  initList();      
});

