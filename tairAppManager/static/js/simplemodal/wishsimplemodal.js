var paperidstr;

$(document).ready(function () {
	$('.obss a.wishbutton').click(function (e) {
		e.preventDefault();
		$('#temp_dialog').modal();
		//从a.wishbutton的name分离出想要读的论文的paper_id
		var str = $(this).attr("name");
		var start = str.indexOf("-");
		var end = str.lastIndexOf("-");
		paperidstr = str.substring(++start, end);
	//	alert(str+"&&"+start+"$$"+end +"&&"+paperidstr);
		queryURL = "../../../paper/" + paperidstr +  "/loadtag";
		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert("loadtag error: "+a.statusText);
		//	},
			success:function(data, textStatus){
				if(data.length == 0){
					$.modal.close();
    				$('#basic-modal-content_wish').modal();
				}
				else{
	 				$.each(data,function(i){
    					$("div #basic-modal-content_wish .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
    					$.modal.close();
    					$('#basic-modal-content_wish').modal();
   					});
   				}
			}
		});
		
	});
	$('.obss a.dobutton').click(function (e) {
		e.preventDefault();
		$('#temp_dialog').modal();
		//从a.wishbutton的name分离出想要读的论文的paper_id
		var str = $(this).attr("name");
		var start = str.indexOf("-");
		var end = str.lastIndexOf("-");
		paperidstr = str.substring(++start, end);		
		queryURL = "../../../paper/" + paperidstr +  "/loadtag";
		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
	 			if(data.length == 0){
					$.modal.close();
					alert('haha');
    				$('#basic-modal-content_do').modal();
					$('#simplemodal-container').css({height:"380px", width:"550px"});
				}
				else{
	 				$.each(data,function(i){
    					$("div #basic-modal-content_do .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
    					$.modal.close();
						alert('haha');
    					$('#basic-modal-content_do').modal();
						$('#simplemodal-container').css({height:"380", width:"550"});
   					});
   				}
			}
		});
	});
	$('.obss a.collectionbutton').click(function (e) {
		e.preventDefault();
		$('#temp_dialog').modal();
		//从a.wishbutton的name分离出想要读的论文的paper_id
		var str = $(this).attr("name");
		var start = str.indexOf("-");
		var end = str.lastIndexOf("-");
		paperidstr = str.substring(++start, end);
		
		queryURL = "../../../paper/" + paperidstr +  "/loadtag";
		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
	 			if(data.length == 0){
					$.modal.close();
					alert('haha');
    				$('#basic-modal-content_collection').modal();
				}
				else{
	 				$.each(data,function(i){
    					$("div #basic-modal-content_collection .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
    					$.modal.close();
    					$('#basic-modal-content_collection').modal();
   					});
   				}
			}
		});
	});
	$('a#user_select, a#user_select2, a#user_select3, a#user_select4').click(function (e){
		e.preventDefault();
		$('#basic-modal-content_choose').modal({scroll:true});
		$('#simplemodal-container').css({height:"310", width:"450"});

		$.ajax({
			type: "POST",
			url: "/mine/friend_list",
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
	 			$.each(data,function(i){
					if(data[i].name.length > 8) {
						var name=data[i].name.substring(0,8)+'..'
					}
					else {
						var name=data[i].name
					}
    				$("div#users").append(' <dl class="obu"> <dt> <a class="ngb" href="/people/'+data[i].id+'"> <img alt="'+data[i].name+'" class="m_sub_img" src="/static/icon_s/'+data[i].headshot+'"/> </a> </dt> <dd style="height:30px"> <a href="/people/'+data[i].id+'/">'+name+'</a></dd> <dd style="height:30px"><input class="allowuser" type="checkbox" name="fri" value="' +data[i].id+'" '+data[i].readinglist_flag+'></dd> </dl>');
					//if (i%5==0){
						//newheight=parseInt($('#simplemodal-container').css("height"))+100;
						//$('#simplemodal-container').height(newheight);
					//}
   				});
    			//$("div#users").append('<a style="margin:360" href="javascript:void(0)" target="_blank">&nbsp</a>');
			}
		});
	});
	
	$('a#changeacl').click(function (e){
		paperidstr = $(this).attr("name");
		e.preventDefault();
		$('#basic-modal-content_chgacl').modal();
		$('#simplemodal-container').css({height:"110", width:"450"});

		$.ajax({
			type: "POST",
			url: "/mine/friend_list",
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert("change acl error: "+a.statusText);
		//	},
			success:function(data, textStatus){
	 			$.each(data,function(i){
    				$("div#users").append(' <dl class="obu"> <dt> <a class="ngb" href="/people/'+data[i].id+'"> <img alt="'+data[i].name+'" class="m_sub_img" src="/static/icon_s/'+data[i].headshot+'"/> </a> </dt> <dd> <a href="/people/{{member.id}}/">'+data[i].name+'</a> <br/><input class="allowuser" type="checkbox" name="fri" id="fri'+data[i].id+'" value="' +data[i].id+'" ></dd> </dl>');
					if (i%6==0){
						newheight=parseInt($('#simplemodal-container').css("height"))+100;
						$('#simplemodal-container').height(newheight);
					}
   				});
    			$("div#users").append('<a style="margin:360" href="javascript:void(0)" target="_blank">&nbsp</a>');
			}
		});
		query={"type":"chk"};
		$.ajax({
			type: "POST",
			url: "/paper/acl/"+paperidstr,
			data: query,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		//alert("loadacl "+a.statusText);
		//	},
			success:function(data, textStatus){
				//alert("#fri"+data[0].id);
	 			$.each(data,function(i){
					box="#fri"+data[i].id;
					$(box).attr("checked","true");
   				});
			}
		});
	});

	$('a#newver').click(function (e){
		paperidstr = $(this).attr("name");
		e.preventDefault();
		$('#basic-modal-content_newver').modal();
		$('#simplemodal-container').css({height:"150", width:"450"});
	});
	//function loadfriends(){
	//}
	//function

	$('a.addtoreadinglist').click(function (e){
		e.preventDefault();
		$('#basic-modal-content_add').modal();
		$('#simplemodal-container').css({height:"110", width:"450"});
		//$('#basic-modal-content_add').css({height:"200", width:"520"});
		paperidstr = $(this).attr("name");
		var qstr="type=checkbox"
		$.ajax({
			type: "POST",
			url: "/paper/readinglist/mine",
			data: qstr,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert("addtorl error"+a.statusText);
		//	},
			success:function(data, textStatus){
				if(data.length==0){
    				$("div#readinglists").append('您还没有创建阅读列表（<a href="/paper/newreadinglist" target="_blank">新建</a>） <br/>');
				}else{
	 				$.each(data,function(i){
    					$("div#readinglists").append(' <li class="line'+ i%2 +'"> <input class="rli" type="checkbox" name="rl" value="' +data[i].id+'" >'+data[i].title +'<br> </li>');
						newheight=parseInt($('#simplemodal-container').css("height"))+20;
						$('#simplemodal-container').height(newheight);
   					});
    				$("div#readinglists").append('<a style="margin: 0 0 0 340;"href="/paper/newreadinglist" target="_blank">新建阅读列表</a>');
				}
			}
		});
	});
	$('a.deletefromreadinglist').click(function (e){
		e.preventDefault();
		$('#basic-modal-content_del').modal();
		$('#basic-modal-content_del').css({height:"50",width:"300"});
		$('#simplemodal-container').css({height:"60", width:"310"});
		paperidstr = $(this).attr("name");
	});
	$('a.deletemysub').click(function (e){
		e.preventDefault();
		$('#basic-modal-content_delmysub').modal();
		$('#basic-modal-content_delmysub').css({height:"50",width:"300"});
		$('#simplemodal-container').css({height:"60", width:"310"});
		paperidstr = $(this).attr("name");
	});

	$('a.add_link').click(function (e){
		e.preventDefault();
		$('#basic-modal-content_addlink').modal();
		$('#simplemodal-container').css({height:"160", width:"410"});
		paperidstr = $(this).attr("name");
	});
		
	$('.indent a.colbutt_wish').click(function (e){
		e.preventDefault();
		$('#temp_dialog').modal();
		thisURL = document.URL; 
		thisURL = thisURL.replace(/(\s*$)/g, ""); 
		thisURL = thisURL.replace(/(\/$)/g, "");
		//alert(thisURL);
		var start = thisURL.lastIndexOf("/");
		var end = thisURL.length;
		queryURL = thisURL.substring(++start, end);
		queryURL ="/paper/"+queryURL+ "/loadtag";

		//alert(queryURL);
		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
				if(data.length == 0){
					$.modal.close();
    				$('#basic-modal-content1_wish').modal();
				}
				else{
	 				$.each(data,function(i){
    					$("div #basic-modal-content1_wish .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
    					$.modal.close();
    					$('#basic-modal-content1_wish').modal();
   					});
   				}
			}
		});
	});
	$('.indent a.colbutt_do').click(function (e){
		e.preventDefault();
		$('#temp_dialog').modal();
		thisURL = document.URL; 
		var start = thisURL.lastIndexOf("/");
		var end = thisURL.length;
		queryURL = thisURL.substring(++start, end);
	//	queryURL += "/loadtag";
	    queryURL ="/paper/"+queryURL+ "/loadtag";

		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
				if(data.length == 0){
					$.modal.close();
    				$('#basic-modal-content1_do').modal();
					$('#simplemodal-container').css({height:"340", width:"550"});
				}
				else{
	 				$.each(data,function(i){
    					$("div #basic-modal-content1_do .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
    					$.modal.close();
    					$('#basic-modal-content1_do').modal();
						$('#simplemodal-container').css({height:"340", width:"550"});
   					});
   				}
			}
		});
	});
	$('.indent a.colbutt_col').click(function (e){
		e.preventDefault();
		$('#temp_dialog').modal();
		thisURL = document.URL;
		thisURL = thisURL.replace(/(\s*$)/g, ""); 
		thisURL = thisURL.replace(/(\/$)/g, ""); 
		var start = thisURL.lastIndexOf("/");
		var end = thisURL.length;
		queryURL = thisURL.substring(++start, end);
		//queryURL += "/loadtag";
		 queryURL ="/paper/"+queryURL+ "/loadtag";
		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
				if(data.length == 0){
					$.modal.close();
    				$('#basic-modal-content1_col').modal();
					$('#simplemodal-container').css({height:"340", width:"550"});
				}
				else{
	 				$.each(data,function(i){
    					$("div #basic-modal-content1_col .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
    					$.modal.close();
    					$('#basic-modal-content1_col').modal();
						$('#simplemodal-container').css({height:"340", width:"550"});
   					});
   				}
			}
		});
	});
	$('.indent a.interest_change').click(function(e){
		e.preventDefault();
		$('#temp_dialog').modal();
		thisURL = document.URL;
		thisURL = thisURL.replace(/(\s*$)/g, ""); 
		thisURL = thisURL.replace(/(\/$)/g, ""); 
		var start = thisURL.lastIndexOf("/");
		var end = thisURL.length;
		queryURL = thisURL.substring(++start, end);
		//queryURL += "/loadtag";
		 queryURL ="/paper/"+queryURL+ "/loadtag";
		$.ajax({
			type: "POST",
			url: queryURL,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
	 			$.each(data,function(i){
    				$("div #basic-modal-content1_chg .clearfix dd").append('<span class="tagbtn gract">' + data[i].tag + '</span>');
   				});
			}
		});
		var chg_wishdoco = $('#chg_wishdoco').val();
		qstr = "chg_wishdoco=" + chg_wishdoco;
		thisURL = document.URL;
		thisURL = thisURL.replace(/(\s*$)/g, ""); 
		thisURL = thisURL.replace(/(\/$)/g, ""); 
		var start = thisURL.lastIndexOf("/");
		var end = thisURL.length;
		queryURL = thisURL.substring(++start, end);
		//queryURL += "/change_rate";
		 queryURL ="/paper/"+queryURL+ "/change_rate";
		$.ajax({
			type: "POST",
			url: queryURL,
			data: qstr,
			dataType: "json",
			error: ajaxError,
		//	error:function(a, textStatus, errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(data, textStatus){
				$.modal.close();
				$('#basic-modal-content1_chg').modal();
					$('#simplemodal-container').css({height:"360px", width:"550px"});
				if(chg_wishdoco == '0'){
					document.all("id_wishdoco")[0].checked=true;
					var shortcom = data.shortcom;
					var secrete = data.secrete;
					var tag = data.tag;
					if (secrete == '1'){
						$("#private_chg").attr("checked", true);
					}
					$(".tags_text").attr("value", tag);
					$("#shortcom_chg").attr("value", shortcom);
					$('#rating_chg #stars_chg').rater(
						null,
						{maxvalue:5, title:{1:'搓', 2:'较差', 3:'还行', 4:'好', 5:'很好'}},
						function(el, value){
							document.chg_form.rating_score_chg.value = value;
						}							
					);
				}
				if(chg_wishdoco == '1'){
					document.all("id_wishdoco")[1].checked=true;
					var score = data.score;
					var shortcom = data.shortcom;
					var secrete = data.secrete;
					var tag = data.tag
					if (secrete == '1'){
						$("#private_chg").attr("checked", true);
					}
					$(".tags_text").attr("value", tag);
					$("#shortcom_chg").attr("value", shortcom);
					document.chg_form.rating_score_chg.value = score;
					$('#rating_chg #stars_chg').rater(
						null,
						{maxvalue:5, curvalue:score, title:{1:'搓', 2:'较差', 3:'还行', 4:'好', 5:'很好'}},
						function(el, value){
							document.chg_form.rating_score_chg.value = value;
						}							
					);				
				}
				if(chg_wishdoco =='2'){
					document.all("id_wishdoco")[2].checked=true;
					var score = data.score;
					var shortcom = data.shortcom;
					var secrete = data.secrete;
					var tag = data.tag;
					if (secrete == '1'){
						$("#private_chg").attr("checked", true);
					}
					$(".tags_text").attr("value", tag);
					$("#shortcom_chg").attr("value", shortcom);
					document.chg_form.rating_score_chg.value = score;
					$('#rating_chg #stars_chg').rater(
						null,
						{maxvalue:5, curvalue:score, title:{1:'搓', 2:'较差', 3:'还行', 4:'好', 5:'很好'}},
						function(el, value){
							document.chg_form.rating_score_chg.value = value;
						}							
					);
				}			
			}	
		});
	});
	
	$('.indent a.interest_del').click(function(e){
		e.preventDefault();
		var r = confirm("真的要删除这个收藏吗？");
		if(r){
			thisURL = document.URL;
			thisURL = thisURL.replace(/(\s*$)/g, ""); 
			thisURL = thisURL.replace(/(\/$)/g, ""); 
			var start = thisURL.lastIndexOf("/");
			var end = thisURL.length;
			queryURL = thisURL.substring(++start, end);
		//	queryURL += "/delete_rate";
             queryURL ="/paper/"+queryURL+ "/delete_rate";
			$.ajax({
				type: "POST",
				url: queryURL,
				error: ajaxError,
			//	error:function(a,textStatus,errorThrown){
			//		alert(a.statusText);
			//	},
				success:function(textStatus){
					alert("该收藏已删除");
					location.replace(location);
				}
			});   			
		}
		else
			;
	});
	
	//simplemodal tags
	$('.tagbtn').live("click", function(e){
		e.preventDefault();
		var tag = $(this).text();
		$.ajax({
			error: ajaxError,
		//	error:function(a,textStatus,errorThrown){
		//		alert(a.statusText);
		//	},
			success:function(textStatus){
				var tag_pre = $('.tags_text').val();
				if(tag_pre == '')
					tag_new = tag;
				else
					tag_new = tag_pre + ' ' + tag;
				$('.tags_text').attr("value", tag_new);
			}
		});   	
	});

	$(".addlinkrl input#save").click(function (){   
	    var rid=$(".addlinkrl").attr("name");
		var paid="";
		//alert("a");
		$(".addlinktolist_list li input").each(function(){
			var $link=$(this).val();
			if($link!=""){
				var start=$link.indexOf("/paper/");
				if(start>=0 && $link.substring(start+7)!="" ){
					id=$link.substring(start+7);
					paid+=id+":";
				}
			}
		});
		//alert(paid);
		//var querystr={"type":"add2", "paperid":paid, "readinglistid":rid};
	    var querystr = "type=" + "add2" + "&paperid=" + paid + "&readinglistid=" + rid;
		//alert(querystr);
		$.ajax({
			type:"POST",
			url:"/paper/readinglist/change",
			data:querystr,
			error: ajaxError,
		//	error:function(a,textStatus,errorThrown){
		//		alert("add2 save error"+a.statusText);
		//	},
			success:function(textStatus){
				$.modal.close();
			}
		});   
		window.location.reload();
	});

	function ajaxError(a){
		if (a.status == 200 && a.statusText == "OK") { 
			alert("ok");
		} 
		else { 
		  //alert(" FAILED : " + a.status + ' ' + a.statusText); 
		} 
	}
});


//	function ajaxError(a){
//		if (a.status == 200 && a.statusText == "OK") { 
//			alert("ok");
//		} 
//		else { 
//		  alert(" FAILED : " + a.status + ' ' + a.statusText); 
//		} 
//	}

function closeModal(){
	$.modal.close();
	$('.tags_text').attr("value", "");
}	

function wishsave()
{   
    var wishdoco = $(".wishdoco_wish").val();
    var paperid = paperidstr;
    var tags = $('.tags_wish').val();
    var shortcom = $('#shortcom_wish').val();
    var secrete;
    if($('#private_wish')[0].checked){
    	secrete = true;
    }
    else{
    	secrete = false;
    }
    var querystr = "wishdoco=" + wishdoco + "&paperid=" + paperid + "&tags=" + tags + "&shortcom=" + shortcom + "&secrete=" + secrete;
	$.ajax({
		type:"POST",
		url:"../wishdocosave",
		data:querystr,
		error: ajaxError,
	//	error:function(a,textStatus,errorThrown){
	//		alert(a.statusText);
	//	},
		success:function(textStatus){
			$.modal.close();
		}
	});    
}

function dosave()
{    
    var wishdoco = $(".wishdoco_do").val();
    var paperid = paperidstr;
    var tags = $('.tags_do').val();
    var shortcom = $("#shortcom_do").val();
    var score = $("#rating_score_do").val();
    var secrete;
    if($("#private_do")[0].checked){
    	secrete = true;
    }
    else{
    	secrete = false;
    }
    var querystr = "wishdoco=" + wishdoco + "&paperid=" + paperid + "&tags=" + tags + "&score=" +　score + "&shortcom=" + shortcom + "&secrete=" + secrete;
	$.ajax({
		type:"POST",
		url:"../wishdocosave",
		data:querystr,
		dataType:'html',
		error: ajaxError,
	//	error:function(a,textStatus,errorThrown){
	//		alert(a.statusText);
	//	},
		success:function(textStatus){
			$.modal.close();
		}
	});     
}

function colsave()
{   
    var wishdoco = $(".wishdoco_col").val();
    var paperid = paperidstr;
    var tags = $(".tags_col").val();
    var shortcom = $("#shortcom_col").val();
    var score = $("#rating_score_col").val();
    var secrete;
    if($("#private_col")[0].checked){
    	secrete = true;
    }
    else{
    	secrete = false;
    }
    var querystr = "wishdoco=" + wishdoco + "&paperid=" + paperid + "&tags=" + tags + "&score=" + score + "&shortcom=" + shortcom + "&secrete=" + secrete;
	$.ajax({
		type:"POST",
		url:"../wishdocosave",
		data:querystr,
		error: ajaxError,
	//	error:function(a,textStatus,errorThrown){
	//		alert(a.statusText);
	//	},
		success:function(textStatus){
			$.modal.close();
		}
	});   
}

function choosesave(){
    var uids=""
	$(".allowuser").each(function(){
		if($(this).attr("checked")){
		 	uids+=$(this).attr("value")+":";
		}
	});
	//alert(uids);
	$("input#user").val(uids);
	$("input#user2").val(uids);
	$("input#user3").val(uids);
	//$.ajax({
	//	type:"POST",
	//	url:"../wishdocosave",
	//	data:querystr,
	//	error:function(a,textStatus,errorThrown){
	//		alert(a.statusText);
	//	},
	//	success:function(textStatus){
	//		$.modal.close();
	//	}
	//});   
	$.modal.close();
}

function changeacl(){
    var uids="";
	$(".allowuser").each(function(){
		if($(this).attr("checked")){
		 	uids+=$(this).attr("value")+":";
		}
	});
	//alert(uids);

	query={"type":"chg","u":uids};
	$.ajax({
		type: "POST",
		url: "/paper/acl/"+paperidstr,
		data: query,
		error: ajaxError,
	//	error:function(a, textStatus, errorThrown){
	//		alert("chgacl "+a.statusText);
	//	},
		success:function(data, textStatus){
			//alert("#fri"+data[0].id);
			$.each(data,function(i){
				box="#fri"+data[i].id;
				$(box).attr("checked","true");
   			});
		}
	});

	$.modal.close();
}

function addsave()
{   
    var paperid = paperidstr;
    var rid="";
	$(".rli").each(function(){
		if($(this).attr("checked")){
		 	rid+=$(this).attr("value")+":";
		}
	});
	//var querystr={"type":"add", "paperid":paid, "readinglistid":rid};
    var querystr = "type=" + "add" + "&paperid=" + paperid + "&readinglistid=" + rid;
	//alert(querystr);
	$.ajax({
		type:"POST",
		url:"/paper/readinglist/change",
		data:querystr,
		dataType:'html',
		//error: ajaxError,
	   error:function(a,textStatus,errorThrown){
	    alert("addsave "+a.statusText);
		},
		success:function(textStatus){
			$.modal.close();
			alert(textStatus)
		}
	});   
	//window.location.reload();
}



function delsave()
{   
    var paperid = paperidstr;

	rid=$(".delrl").attr("name");
	//var querystr={"type":"del", "paperid":paid, "readinglistid":rid};
    var querystr = "type=" + "del" + "&paperid=" + paperid + "&readinglistid=" + rid;
	//alert(querystr);
	$.ajax({
		type:"POST",
		url:"/paper/readinglist/change",
		data:querystr,
		dataType:'html',
		error: ajaxError,
//	   error:function(a,textStatus,errorThrown){
//			alert("delrl error: "+a.statusText);
//		},
		success:function(textStatus){
			$.modal.close();
		}
	});  
	table="table.table_"+paperid;
	$(table).remove();
}

function delete_mysub() {
	paperid = $(".delmysub").attr("name");
	userid = $("#delmysubuser").attr("name");
    var querystr = "userid=" + userid + "&paperid=" + paperid;
    $.ajax({
        type:"POST",
        url:"/mine/mysub/delete",
        data:querystr,
        dataType:'html',
        error:ajaxError,
        success:function(textStatus) {
            $.modal.close();
        }
    });
    ulremove="#ul"+paperid;
    $(ulremove).remove();
}

function ajaxError(a){
        if (a.status == 200 && a.statusText == "OK") {
            alert("ok");
        }
        else {
          alert(" FAILED : " + a.status + ' ' + a.statusText);
        }
    }
function savenewversion(){
	
}
