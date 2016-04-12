/**
 * Created by caojiangtao on 15/3/11.
 */

(function($) {
	var clicknumber = 0;
	var methods = {
		init: function(options) {},
		pop: function(options) { //弹出层
			var _H = $(window).height();
			var _W = $(window).width();
			var jumpstop = 0;
			var stop = 1;
			/*
			 * options.width(number)	弹出层宽度（必选）
			 * options.height(number) 弹出层高度（必选）
			 * options.zIndex(number) 弹出层index轴 ，默认为9999；（可选）
			 * options.poparent(jquery节点) 要插入的父节点,默认为‘body’（可选）
			 * options.opacity(0~1) 背景透明度（可选）
			 * option.popId(jqeury节点 ) 要插入的弹出层ID或者calss,最好为ID，强调唯一性！（必选）
			 * option.popHtml(插入弹出层元素结构) 如“<div id='test'></div>"；（可选）
			 * option.popFunc(function方法) 弹出层回调方法；（可选）
			 * option.closePop(function方法) 关闭回调方法；（可选）
			 * option.time(1~100000)//X秒跳转，X为整数，如：1为1秒（可选）
			 * option.timeId(id)//为一个ID节点，用来储存时间显示（可选）
			 * option.url(URL)//一个链接，倒计时跳转路径。（可选）
			 * 关闭按钮约定名称为 calss = popclose;（可选）
			 * */
			var settings = {
				'width': 100,
				'height': 100,
				'zIndex': 9999,
				'poparent': 'body',
				'opacity': 0.5,
				'popId': null,
				'popHtml': null,
				'popFunc': null,
				'time': null,
				'timeId': null,
				'url': null,
				'closePop': null
			};
			// 如果存在选项，则合并之
			if (options) {
				$.extend(settings, options);
			}
			var popTop;
			var popLeft = (_W - settings.width) / 2;
			if (settings.popHtml === null) {
				return this.each(function() {
					var $this = $(this);
					if (settings.height == 'auto') {
						settings.height = $this.height();
					};
					popTop = (_H - settings.height) / 2;
					$this.show();
					$this.css({
						width: settings.width,
						height: settings.height,
						zIndex: settings.zIndex,
						top: popTop,
						left: popLeft,
						position: 'fixed'
					});
					closebox();
					if (settings.time !== null) {
						jump(settings.time, settings.timeId, settings.url);
					}
				});
			} else if (settings.popHtml !== null) {
				$(settings.poparent).append(settings.popHtml);
				if (settings.height == 'auto') {
					settings.height = $(settings.popId).height();
				};
				popTop = (_H - settings.height) / 2;
				$(settings.popId).css({
					width: settings.width,
					height: settings.height,
					zIndex: settings.zIndex,
					top: popTop,
					left: popLeft,
					position: 'fixed'
				});
				closebox()
			};

			function closebox() {
				if (settings.popFunc !== null) {
					settings.popFunc()
				};
				var backlayer = "<div id='blacklayer'></div>"
				$("body").append(backlayer);
				var dh = $(document).height();

				$('#blacklayer').css({
					zIndex: settings.zIndex - 10,
					background: "#000",
					opacity: settings.opacity,
					position: 'absolute',
					left: 0,
					top: 0,
					width: '100%',
					height: dh
				})
				$('.popclose').bind("click", function() {
					stop = 0;
					$('#blacklayer').remove();
					if (settings.popHtml === null) {
						$(settings.popId).hide();
					} else {
						$(settings.popId).remove();
					}
					if (settings.closePop != null) {
						settings.closePop();
					}
				})
			}

			if (settings.time !== null) {

				jump(settings.time, settings.timeId, settings.url);
			}

			function jump(time, element_id, url) { //X秒跳转
				if (stop === 0) return false
				_jumpfunc = window.setTimeout(function() {
					time--;
					if (time > 0) {
						if (jumpstop == 1) {
							return false;
						} else {

							$(element_id).html(time + "秒");
							jump(time, element_id, url)
						}
					} else {
						if (url == null) {
							$('#blacklayer').remove();
							$(settings.popId).remove();
						} else {
							document.location = url;
						}
					}
				}, 1000);
			}
		},
		tag: function(options) { //标签切换
			var settings = {
				'type': "click",
				'selected': 'on',
				'contentClass': '.content',
				'func': null
			};
			// 如果存在选项，则合并之
			if (options) {
				$.extend(settings, options);
			}
			if (settings.type != 'click' && settings.type != 'mouseover') return false;
			$(this).eq(0).addClass(settings.selected);
			return this.each(function() {
				var $this = $(this);
				$(settings.contentClass).hide();
				$(settings.contentClass).eq(0).show();
				$this.bind(settings.type, contentShow);

				function contentShow() {
					var _index = $this.index();
					$this.siblings().removeClass(settings.selected);
					$this.addClass(settings.selected);
					$(settings.contentClass).hide();
					$(settings.contentClass).eq(_index).show();
					if (settings.func != null) {
						settings.func();
					}
				}
			})
		},
		imgmove: function(options) { //多小图片幻灯
			var settings = {
					oneEle: null,
					oneWidth: null,
					loop: false,
					boxWidth: null,
					prev: null,
					next: null
				}
				// 如果存在选项，则合并之
			if (options) {
				$.extend(settings, options);
			}

			function movefunc() {
				var number = $(settings.oneEle).size();
				var length = number * settings.oneWidth;
				var boxlen = length / settings.boxWidth;
				if (boxlen % settings.boxWidth > 0) {
					boxlen + 1;
				}
				var par = $(settings.oneEle).parent();
				if (settings.loop == true) {
					$(settings.oneEle).parent().width(length).css("left", -settings.oneWidth);
					var par = $(settings.oneEle).parent();
					var li = $(settings.oneEle).last();
					par.prepend(li.clone())
					li.remove();
				} else {
					$(settings.oneEle).parent().width(length);
				}
				$(settings.prev).click(function() {
					if (settings.loop == true) {
						var li = $(settings.oneEle).last();
						TweenMax.to(par, 1, {
							left: 0,
							onComplete: function() {
								par.prepend(li.clone())
								par.css("left", -settings.oneWidth);
								$(settings.oneEle).last().remove();
							},
							ease: Quart.easeOut
						});
					} else {
						if (clicknumber > 0) {
							clicknumber--;
							TweenMax.to(par, 1, {
								left: -settings.boxWidth * clicknumber,
								ease: Quart.easeOut
							});

						};
					}
				});
				$(settings.next).click(function() {
					if (settings.loop == true) {
						TweenMax.to(par, 0.4, {
							left: -settings.oneWidth,
							onComplete: function() {
								par.css("left", "0px");
								var li = $(settings.oneEle).slice(0, 1);
								par.append(li.clone())
								$(settings.oneEle).slice(0, 1).remove();
								console.log("ok")
							},
							ease: Quart.easeOut
						});
					} else {
						if (clicknumber < boxlen - 1) {
							clicknumber++
							TweenMax.to(par, 1, {
								left: -settings.boxWidth * clicknumber,
								ease: Quart.easeOut
							});
						}
					}
				});
			}
			movefunc();
		}
	};
	$.fn.tooltip = function(method) {
		// Method calling logic
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' + method + ' does not exist on jQuery.tooltip');
		}
	};
})(jQuery);
// 获取当前网址的域名
function domain(url){
	var durl=/http:\/\/([^\/]+)\//i;
	var hosts = url.match(durl);
	hosts = hosts[1];
	d_arr = hosts.split('.');
	hosts = d_arr[d_arr.length - 2] + '.' + d_arr[d_arr.length - 1];
	return hosts;
}

var JK_lock = "open";
var checkSubmitFlg = false;

var JKXY = JKXY || {}
JKXY = {
	init: function() {
		this.gotop();
		this.bindElem();
		this.TopSearch();
	},
	bindElem: function() {
		$("#headsearch .search-btn").bind("click", JKXY.TopSearch);
		$('#user-name,.user-center,#user-name p').bind("mouseover", this.userContent);
		
		$(".mod-tips .close").on('click', function() {
			$(this).parents('.mod-tips').remove();
		});
	},
	userContent: function() { //头部用户中心下拉
		$('.user-center').show();
		$('.jiaotou').addClass("rotate");
		JKXY.stopEventBubble();
		$(document).bind("mouseover", function() {
			$('.user-center').hide();
			$('.jiaotou').removeClass("rotate");
		});
	},
	Cookie: {
		cokpre: 'sso_',
		get: function(name) {
			var nameEQ = this.cokpre + name + '=';
			var ca = document.cookie.split(';');
			for (var i = 0; i < ca.length; i++) {
				var c = ca[i];
				while (c.charAt(0) == ' ') c = c.substring(1, c.length);
				if (c.indexOf(nameEQ) == 0) {
					var ret;
					try {
						ret = unescape(c.substring(nameEQ.length, c.length));
					} catch (e) {
						ret = unescape(c.substring(nameEQ.length, c.length));
					}
					return ret;
				}
			}
			return null;
		},
		set: function(name, value, days, path, domain, secure) {
			var expires;
			if (typeof days == "number") {
				if (days > 0) {
					var date = new Date();
					date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
					expires = date.toGMTString();
				}
			} else if (typeof days == "String") {
				expires = days;
			} else {
				expires = false;
			}
			document.cookie = this.cokpre + name + '=' + escape(value) +
				(expires ? (';expires=' + expires) : '') +
				(path ? (';path=' + path) : '') +
				(domain ? (';domain=' + domain) : '') +
				(secure ? ';secure' : '');
		},
		del: function(name, path, domain, secure) {
			JKXY.Cookie.set(name, '', -1, path, domain, secure);
		}
	},
	stopEventBubble: function() { //阻止冒泡事件
		function getEvent() {
			if (window.event) {
				return window.event;
			}
			func = getEvent.caller;
			while (func != null) {
				var arg0 = func.arguments[0];
				if (arg0) {
					if ((arg0.constructor == Event || arg0.constructor == MouseEvent || arg0.constructor == KeyboardEvent) || (typeof(arg0) == "object" && arg0.preventDefault && arg0.stopPropagation)) {
						return arg0;
					}
				}
				func = func.caller;
			}
			return null;
		}


		var e = getEvent();
		if (window.event) {
			//e.returnValue=false;//阻止自身行为
			e.cancelBubble = true; //阻止冒泡
		} else if (e.preventDefault) {
			//e.preventDefault();//阻止自身行为
			e.stopPropagation(); //阻止冒泡
		}
	},


	TopSearch: function() { //头部搜索
		// alert('1');
		$("input[name='q']").bind("focus", function() {
			$('.search-btn').addClass("search-btn2");
			$('.hot-words').hide()
			$(this).css({
				paddingRight: "55px"
			});

		});
		$("input[name='q']").bind("focusout", function() {
			$('.search-btn').removeClass("search-btn2");
			$('.hot-words').show();
		});
		$('#J_keywordList .result-list').delegate('.current', "click", function() {
			var val = $(this).text();
			$("input[name='q']").val(val);

		})
	},
	gotop: function() { 
		var lock = JKXY.Cookie.get("pewm");
		var erwma_none = lock == "none" ? '' : "style='display:none'";
		var html = "<div class='gotop' id='gototop'>";
		var ewmImg = wenda_url + '/home/static/images/erwma.png';
		var ewapImg = wenda_url + '/home/static/images/ewap.jpg';
		var appewm = wenda_url + '/home/static/images/appewm.png';

		html += "<span class='top'></span>";
		html += "<span class='erwma'><img src=" + ewmImg + "> </span>";
		html += "<a href='/app/' alt='极客学院应用' target='_blank'><span class='jk-app'><img src=" + appewm + " class='appewm'/></span></a>"
		
		html+="<a href='http://meiqia.com/chat/7594' target='_blank' class='qq-online qq-online1' rel='nofollow'>";
		html+="<span class='kefu'>在线客服<br/>  工作日9:00-21:00在线<i></i></span></a>";
		if (lock != "none") {
			var pewm_display = $('#bannerbox').length <= 0 ? '' : 'style="display:none;"';
			html += "<img src=" + ewapImg + " class='pewm' id='pewm' />";
		}
		html += "</div>";

		//获取返回顶部元素对象
		// var version=" <div class='text' id='ie-test'>您的浏览器版本太低，为了获得更好的浏览体验！<br/>我们建议您升级浏览器或者使用Chrome、Firefox、Safari浏览器</div>";
		function showPop(id) {
			if ($(window).height() < 490 + 340 && $(window).scrollTop() <= 490) {
				$(id).fadeOut();
			} else {
				$(id).fadeIn();
			}
		}
		var pewmDisplay = function() {
			var lock = JKXY.Cookie.get("pewm");
			if (lock != "none" && $('#bannerbox').length > 0) {
				showPop('#pewm');
			}
		}

		if ($('#gototop').length == 0) {
			$('body').append(html);
			var html = $('#gototop');
			pewmDisplay();
		} else {
			var html = $('#gototop');
		}
		//绑定返回顶部事件

		$('#pewm').on("click", function() {

			$(this).fadeOut();
			JKXY.Cookie.set("pewm", "none", 1, '/', '.' + domain(window.location.href), '');
			$('.erwma').fadeIn();
		});
		if ($(window).scrollTop() <= 0) {
			$('#gototop>.top').hide();
		}
		html.find('.top').bind('click', function() {
			if ($(window).scrollTop() <= 0) return false;
			$('body,html').animate({
				scrollTop: 0
			}, 200);
			return false;
		});
		html.find('.erwma').bind("mouseover", function() {
			$('.erwma>img').fadeIn();
			$('.jk-app img').hide();
			JKXY.stopEventBubble();
		})
		html.find('.jk-app').bind("mouseover", function() {
			$('.jk-app img').fadeIn();
			$('.erwma>img').hide();
			JKXY.stopEventBubble();
		})
		$(document).bind("mouseover", function() {
			$('.erwma>img').stop(true, true)
			$('.jk-app img').stop(true, true)
			$('.jk-app img').fadeOut();
			$('.erwma>img').fadeOut();
		})
		$(window).scroll(function() {
			if ($(window).scrollTop() > 0) {
				$('#gototop>.top').fadeIn();
			} else {
				$('#gototop>.top').fadeOut();
			}
			pewmDisplay();
		})
		html.find('.news').bind("click", function() {
			if (JKXY.Browser.IE) {
				if (JKXY.Browser.IE6 || JKXY.Browser.IE7 || JKXY.Browser.IE8) {
					if ($('#warningpop').has('#ie-test')) {
						return false
					} else {
						$('#warningpop').append(version);
					}

				}
			}
			$('#warningpop').tooltip("pop", {
				width: 540,
				height: 'auto',
				popId: '#warningpop',
				opacity: 0.3
			})
		});
		$('.close-img').bind("click", function() {
			$(this).parent().remove();
		})
	},
	//顶部弹窗功能
	msgBox:function(status, msg, show_time, callBack)
	{
		var msg		= msg ? msg : '此用户已经申请过，不要重复申请';
		var id		= "warning";
		var show_time	= parseInt(show_time) ? parseInt(show_time) : 1500;
		switch (status)
		{
			case 1:
				var color_class	= "waring-success";
				break;
			case 0:
				var color_class	= "waring-failure";
				break;
			case 2:
			default:
				var color_class	= "waring-sub";
				break;
		}
		var html;
		html	= '<div class="web-dia-tip '+color_class+'" id="'+id+'" >';
		html	+= msg;
		html	+= '</div>';
		$('body').append( html );

		var _W	= $('#'+id).width()/2;
		$('#'+id).css("marginLeft", -_W);
		$('#'+id).animate({top:"0px",opacity:1},300,function(){
			$('#'+id).delay(show_time).animate({top:"-50px",opacity:0},500,function(){
				$('#'+id).remove();
				if( typeof(callBack) == 'function' )
				{
					callBack();
				}
			});
		});

	}
}

var pageloading = pageloading || {};
pageloading = {
    init: function (commonUrl) {
        var _self = this;
        _self.loading();
        // pageloading.def();
        // pageloading.bind();
        //_self.loading(_self.imgList());
    },
    def: function(){
        window.commonSearch = function () {

            $.ajax({
                type: "get",
                url: "/search/headsuggest",
                success: function (data) {
                    if (data.code != 200 || !data.data instanceof Array || data.data.length <= 0) {
                        return;
                    }
                    var ul = $("#J_keywordList ul");
                    $("#J_keywordList").hide();
                    ul.empty();
                    for (var i = 0, k = data.data.length; i < k; i++) {
                        $("#J_keywordList ul").append('<li class="current">\
                      <a href="/search/s/q_' + data.data[i] + '"> ' + data.data[i] + '</a>\
                      </li>');
                    }
                    $("#J_keywordList").show();
                },
                data: {"val": encodeURIComponent(window.searchSuggestEle.target.value)},
                dataType: "jsonp"
            });
        }
    },
    bind: function(){
        var $webSearchHeader = $('#web_search_header');
        var searchSuggestCode;
        $webSearchHeader.on('keyup', function(ele){
            window.searchSuggestEle = ele;
            clearTimeout(searchSuggestCode);
            searchSuggestCode = setTimeout('commonSearch()', 200);
        })
    },

    loading: function () {//头部loadding
        var le = $('.loading-length');
        le.animate({width: $(window).width()}, 300)

    }
}


var ques = ques || {};

ques = {
	init: function(){
		this.numSwitch();
		this.bindElem();
		this.editType();
		this.floorBg();
		// this.setImg('.details');
		// this.setImg('.contEdit');
	},
	bindElem:function(){
        
		// 采纳答案
		$('.adoptOn, .adoptOff').on('click',this.adoptOn);
        // 点赞
        $('.praise').on('click',this.praise);
		// 编辑问题
		$("#editAsk").on('click',this.editAsk);
		// 编辑回答
		$(".editReply").on('click',this.editReply);
		// 回复
		$(".reply").on('click',this.reply);
		// 提交表单
		$("#subBtn").on('click',this.subForm);

	},

	numSwitch:function(){  //数字转换单位
		var aNum = $('.numSwitch');

		aNum.each(function(i){
			iNum = $(this).text();
			if(iNum > 1000){
				iNum = iNum/1000;
				var sNum = iNum.toFixed(1);
				$(this).text(sNum+'k');
			}
		})
		
	},
	// 控制回复内容图片宽度
	setImg:function(obj){
		$(obj).find('img').each(function(){
			var imgw = $(this).width(),
				imgh = $(this).height(),
				scale = 1;
			if(imgw>660){
				scale = 660/imgw;
				$(this).width(scale*imgw);
				$(this).height(scale*imgh);
			}
			
		})
	},
	// 采纳
	adoptOn:function(){	//采纳	待定
		// aid 问题id， rid 回答id
		var aid = $("#ask").attr('aid'),
            rid = $(this).parents('.wrap').attr('rid'),
            isAdopt = $(this).attr('adopt');
            submitStatus = 5,
			data = {'replyId':rid, 'submitStatus':submitStatus, 'isAdopt':isAdopt};
		// console.log(data);
		if(data){
			$.ajax({
				type:"post",
				url :'/question/'+aid+'/',
				data:data,
				success:function(res){
					if(res.code == 200){
						location.reload();
					}else{
			            JKXY.msgBox(0, "出现问题了~，请再试一次~");
					}
				},
				error:function(){
			        JKXY.msgBox(0, "出现问题了~，请再试一次~");
				},
				dataType:'json'
			});
		}else{
			JKXY.msgBox(0, "出现问题了~，请再试一次~");
		}
	},
	// 点赞
	praise:function(){
  
        if (checkSubmitFlg == true) {
            return false;
        }

        checkSubmitFlg = true;

		var aid = $("#ask").attr('aid'),
            rid = $(this).parents('.wrap').attr('rid'),
            submitStatus = 4,
			data = {'replyId':rid, 'submitStatus':submitStatus};
		if(data){
			$.ajax({
				type:"post",
				url :'/question/'+aid+'/',
				data:data,
				success:function(res){
			        if (res.code == 200) {
						location.reload();
                    }
				},
				error:function(){
			        JKXY.msgBox(0, "出现问题了~，请再试一次~");
				},
				dataType:'json'
			});
		}else{
			JKXY.msgBox(0, "出现问题了~，请再试一次~");
		}
	},
	editType:function(){
		if($("#submitStatus").val() == 2){
			$("#askTit").css('display','block');	
		}else{
			$("#askTit").css('display','none').children().val(0);
		}
	},
	floorBg:function(){
		$('.floor').click(function(){
			var id = $(this).attr('href');
				id = id.substr(1);
				// console.log(id);
			$('.replylist>.wrap').removeClass('light');
			$("#"+id).addClass('light');
		})
	},
	// 回复答案
	reply:function(){

		var aid = $("#ask").attr('aid'),
			rid = $(this).parents('.wrap').attr('rid'),
			submitStatus = 1;

		$("#askId").val(aid);
		$("#replyId").val(rid);	
		$("#submitStatus").val(submitStatus);

		ques.editType();
		//tcw
		var nick = $(this).parents('ul').find('.userNick').html(),
			floor = $(this).parents('ul').find('.hint').find('.floor a').html();
			// console.log(floor);

			sNick = floor+' <span>@'+nick+'&nbsp; </span>';
		ques.editor.setValue(sNick);

	},
	// 编辑问题
	editAsk:function(){
		var	submitStatus = 2,
			sTit = $(this).parents('.tit').find('h1').text(),
			sCont = $(this).parents('.wrap').find('.details').html();

		$("#submitStatus").val(submitStatus);

		ques.editType();

		$("#askTit").css('display','block').children().val(sTit);	
		
		
		ques.editor.setValue(sCont);

	},
	// 编辑回复
	editReply:function(){
		var aid = $("#ask").attr('aid'),
			rid = $(this).parents('.wrap').attr('rid'),
			submitStatus = 3;
		$("#askId").val(aid);
		$("#replyId").val(rid);	
		$("#submitStatus").val(submitStatus);
		ques.editType();
		var sCont = $(this).parents('ul').find('.cont').html();
	
		ques.editor.setValue(sCont);
	},
	// 提交回复
	subForm:function(rid){
		var	aid = $("#ask").attr('aid'),
            rid = $("#replyId").val(),
			rid = rid ? rid : 0,
			sTit = $("#askTit input").val(),
			// edit = $('.simditor-body');
			edit = ques.editor.getValue();
						
		// console.log(edit);
		// console.log($.trim(edit).length);
		// console.log($.trim($(edit).text()).length);

		var img = /<img\s+/;
		var flag = img.test(edit);
		// console.log(flag);
		if(edit.length > 5000){
			JKXY.msgBox(0, "回复内容长度不能超过5000字符哦~");
		}else if($.trim($(edit).text()).length == 0 && flag == false){
			JKXY.msgBox(0, "回复内容不能为空哦~");
		}else if(sTit != 0 && sTit.length == 0){	//sTit=0 不需要输入标题
			JKXY.msgBox(0, "标题内容不能为空哦~");
		}else{
            var submitStatus = $("#submitStatus").val();
			var data = {'replyId':rid,'title':sTit,'content':edit, 'submitStatus':submitStatus};
			// console.log(data);
			$.ajax({
				type:"post",
				url:"/question/"+aid+"/",
				data:data,
				success:function(data){
				
                    if(data.code == 200){
                        location.reload();
                    } else {
                        JKXY.msgBox(0, data.msg);
                    }
				},
				error:function(){
					JKXY.msgBox(0, "完了~网络出问题了,刷新下再试试吧！");
				},
				dataType:'json'
			});
		}

		
	}
}



$(function() {
	
	JKXY.init();
	pageloading.init();
	ques.init();
})
