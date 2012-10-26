$(document).ready(function(){ 
  
  $("#apply img").hover(function(){
     var label=$(this).siblings("label");
     label.show(); 
  });
  $("#apply input").focus(function(){
     var label=$(this).siblings("label");
     label.show(); 
  });
  $("#apply input").blur(function(){
     var label=$(this).siblings("label");
     label.hide(); 
     //TODO :js表单验证
  });
  $("#apply textarea").focus(function(){
     $("#tip_describe").show();
  });
  $("#apply textarea").blur(function(){
     $("#tip_describe").hide();
  });

  /*
   * 审批页面，选择集群时自动填充namespace，
   * 填充的namespace为选择当前集群的最大值+1
   */
  $("#id_group").change(function(){
    group_id=this.value;
    //url="/cluster/"+group_id+"/ns"
    //$("#id_namespace").attr("title", group_id);     
    //$.ajax({
    //  type:"GET",
    //  url:url,
    //  dataType: "json",
    //  error:function(a,textStatus,errorThrown){
    //    //alert(a.statusText+a.responseXML);
    //  },
    //  success:function(data, textStatus){
    //    if (data.error){
    //      //alert(data.error);         
    //      $("#id_namespace").val("");     
    //    } else {
    //      $("#id_namespace").val(data.namespace);     
    //      $("#id_namespace").attr("title", group_id);     
    //    }
    //  }
    //});
    $("#id_namespace").attr("title", group_id);     
  });

  /*
   * 审批页面，焦点离开文本框时，检查namespace是否被使用
   */
  $("#id_namespace").blur(function(){
    namespace = $(this).val();
    group_id = $(this).attr("title");
    url="/cluster/"+group_id+"/nscheck"
    $.ajax({
      type:"GET",
      url:url,
      data:{"namespace":namespace},
      dataType: "json",
      error:function(a,textStatus,errorThrown){
        //alert(a.statusText+a.responseXML);
      },
      success:function(data, textStatus){
        if (data.error){
          //alert(data.error);         
        } else {
          if(data.exist){
            $("#tip_namespace").show();
            alert("对不起，该Namespace已被使用");
          } else {
            $("#tip_namespace").hide();
          }
        }
      }
    });
  });

  //修改重要级别
  $("a.change_important").click(function(e){
    apply_id=$(this).attr("name");
    e.preventDefault();
    $('#change_important_modal').modal("");
    $('.important_submit').attr('name',apply_id)
  });

  //更新剪切板
  $("#update_clipboard").click(function(e){
    reviewer=$(this).attr("name");
    text=$("#id_clipboard").val();
    url = "/app/savecb";
    alert(text);
    $.ajax({
      type:"POST",
      url:url,
      data:{"text":text, "username":reviewer},
      dataType: "json",
      error:function(a,textStatus,errorThrown){
        //alert(a.statusText+a.responseXML);
      },
      success:function(data, textStatus){
        alert("ok");
      }
    });
  });

  $("#decline").click(function(e){
    id=$(this).attr("name");
    url = "/app/"+id+"/decline";
    $.ajax({
      type:"POST",
      url:url,
      data:{"decline":true},
      dataType: "json",
      error:function(a,textStatus,errorThrown){
        //alert('error! '+a.statusText+a.responseXML);
        window.location.href="/";
      },
      success:function(data, textStatus){
        //alert("ok");
        window.location.href="/";
      }
    });
  });

  $("#rereview").click(function(e){
    id=$(this).attr("name");
    url = "/app/"+id+"/rereview/";
    $.ajax({
      type:"POST",
      url:url,
      data:{"rereview":true},
      dataType: "json",
      error:function(data,textStatus,errorThrown){
        alert(data.errror);
        alert('对不起，您没有修改审批的权限!');
      },
      success:function(data, textStatus){
        //alert("ok");
        window.location.href="/app/"+id+"/review";
      }
    });
  });
  //修改area的quota
  $("#modify").click(function(e){
    area = $("#testarea").val();
    quota = $("#testquota").val();
    url="/openapi/area/"+area;
    data= "quota=" + quota +"&type=modify";
    alert(data);
    $.ajax({
      type:"POST",
      url:url,
      data:data,
      dataType: "json",
      error:function(a,textStatus,errorThrown){
          alert('error! '+a.statusText+a.responseXML);
      },
      success:function(data, textStatus){
          alert("OK");
      }
    });
  });

  //分配新的area
  $("#alloc").click(function(e){
    area = $("#testarea").val();
    quota = $("#testquota").val();
    url="/openapi/area/"+area;
    data= "quota=" + quota +"&type=alloc1";
    alert(data);
    $.ajax({
      type:"POST",
      url:url,
      data:data,
      dataType: "json",
      error:function(a,textStatus,errorThrown){
          alert('error! '+a.statusText+a.responseXML);
      },
      success:function(data, textStatus){
        alert(data.clusters[0].areanum);
        alert(data.clusters[0].address.group);
        location.reload();
      }
    });
  });

  /*
   * 异步提交对important的修改
   */
  $(".important_submit").click(function(){
    app_id=$(this).attr("name");
    ivalue = $("input:[name=important_radio]:radio:checked").val();
    url="/app/"+app_id+"/setimportant/"
    type= "i=" + ivalue;
    $.ajax({
      type:"POST",
      url:url,
      data:type,
      //error: ajaxError,
      error:function(a,textStatus,errorThrown){
          alert(a.statusText+a.responseXML);
      },
      success:function(textStatus){
        $.modal.close();
        location.reload();
      }
    });
  });

  oTableSettings = {
    "bProcessing": true,
    "bServerSide": true,
    "bDestroy": true,
    //"sAjaxSource": "/app/json",
    "sPaginationType" : "full_numbers",
    "bAutoWidth" : false,
    "bScrollCollapse": true,
    //"bJQueryUI": true,
    //"bStateSave" : true, 
    //"bJQueryUI": false,
    //"sScrollX": "100%",
    "aaSorting": [[ 0, "desc"]],
    "aoColumnDefs" : [{ 
      "sType": "numeric", 
      "aTargets": [0]
    }, {
      "bSearchable" : false, 
      "aTargets" : [1,2,3,4,5,6,7] 
    }, {
//      "sWidth": "60px",
//      "aTargets": [0,1,3,4,5,6,7]
//    }, {
//      "sWidth": "430px",
//      "aTargets": [2]
//    }, { 
      "asSorting" : ["asc", "desc"], 
      "aTargets" : [0, 1, 2, 5] 
    }, { 
      "bSortable" : false, 
      "aTargets" : [2, 3, 4, 5, 6, 7] 
    }], 
    "aLengthMenu" : [[10, 50, 100], ["10", "50", "100"]], 
    "oLanguage" : { 
      "sProcessing" : "数据读取中...",
      "sLengthMenu" : "显示_MENU_条 ",
      "sZeroRecords" : "没有您要搜索的内容",
      "sInfo" : "从_START_ 到 _END_ 条记录 - 查询到的记录数为 _TOTAL_ 条",
      "sInfoEmpty" : "记录数为0",
      "sInfoFiltered" : "(全部记录数 _MAX_  条)",
      "sInfoPostFix" : "",
      "sSearch" : "搜索",
      "sUrl" : "",
      "oPaginate" : { 
          "sFirst" : "第一页",
          "sPrevious" : " 上一页 ", 
          "sNext" : " 下一页 ", 
          "sLast" : "最后一页" 
      },
    },
    //"fnServerParams": function ( aoData ) {
    //  aoData.push( { "name": "type", "value": "all" } );
    //},
  }
  paramall = {
    "sAjaxSource": "/app/json",
  }
  paramdone = {
    "sAjaxSource": "/app/json?type=done",
  }
  paramtodo = {
    "sAjaxSource": "/app/json?type=todo",
  }
  $.mergeJsonObject = function(jsonbject1, jsonbject2)  
    {  
      var resultJsonObject={};  
      for(var attr in jsonbject1){  
          resultJsonObject[attr]=jsonbject1[attr];  
      }  
      for(var attr in jsonbject2){  
          resultJsonObject[attr]=jsonbject2[attr];  
      }  
      return resultJsonObject;  
    };  
    //oTableSettings["fnServerParams"]=function(aoData, value){
    //  //aoData.push( { "name": "type", "value": "all" } );
    //  for (data in aoData){
    //    if(aoData[data]["name"] == "type"){
    //      alert(aoData[data]["value"] );
    //      aoData[data]["value"] = value;
    //    }
    //  }
    //};
  var oTable = $('#app_table').dataTable($.mergeJsonObject(oTableSettings,paramall)); 
  var oTable = $('#app_table_todo').dataTable($.mergeJsonObject(oTableSettings,paramtodo)); 
  var oTable = $('#app_table_done').dataTable($.mergeJsonObject(oTableSettings,paramdone)); 
  //$("#todo_nav").click(function(){
  //  for (p in params[0]){
  //    alert(params[0][p]); 
  //  }
  //  //c=$.mergeJsonObject(oTableSettings,{"fnServerParams" : function(aoData){aoData.push({"name":"type","value":"todo"})}} );
  //  //oTableSettings["fnServerParams"]=function(aoData){aoData};

  //  oTable.fnDraw();
  //});
//  oTable.css({'width':"950px"});
//  $('tbody tr td(1)').css({'width':'50px'});
//  $('tbody tr td(2)').css({'width':'150px'});
//  $('tbody tr td(3)').css({'width':'300px'});
//  $('tbody tr td(4)').css({'width':'100px'});
//  $('tbody tr td(5)').css({'width':'50px'});
//  $('tbody tr td(6)').css({'width':'100px'});
//  $('tbody tr td(7)').css({'width':'50px'});
//  $('tbody tr td(8)').css({'width':'150px'});
  var cTable = $('#cluster_table').dataTable({
    "sPaginationType" : "full_numbers",
    "bDestroy": true,
    //打开排序功能
    "bSort" : true,  
    "bStateSave" : true, 
    "bJQueryUI": true,
    "aLengthMenu" : [[10, 30, 100], ["10", "30", "100"]], 
    "oLanguage" : { 
      "sProcessing" : "数据读取中...",
      "sLengthMenu" : "显示_MENU_条 ",
      "sZeroRecords" : "没有您要搜索的内容",
      "sInfo" : "从_START_ 到 _END_ 条记录 - 查询到的记录数为 _TOTAL_ 条",
      "sInfoEmpty" : "记录数为0",
      "sInfoFiltered" : "(全部记录数 _MAX_  条)",
      "sInfoPostFix" : "",
      "sSearch" : "搜索",
      "sUrl" : "",
      "oPaginate" : { 
          "sFirst" : "第一页",
          "sPrevious" : "上一页", 
          "sNext" : "下一页", 
          "sLast" : "最后一页" 
      },
    } 
  });
  
});


