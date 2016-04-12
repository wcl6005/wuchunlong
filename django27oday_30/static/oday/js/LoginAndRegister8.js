/**
 * 登录注册弹层 js
 * 2015-8-24
 * zhanghaibin
 */



var PASSPORT = PASSPORT || {};


//////////////////////////////////////////////////

// domain
var passportDomain = {


    domain_arr: function(url) {
        var durl = /http:\/\/([^\/]+)\//i;
        var hosts = url.match(durl);
        hosts = hosts[1];
        d_arr = hosts.split('.');
        return d_arr;
    },
    currentUrl: window.location.href
};
var passportHostArr = passportDomain.domain_arr(window.location.href);
var passportBaseUrl = passportHostArr[1] + '.' + passportHostArr[2];
var passportUrl = "http://passport." + passportBaseUrl;
var passportWwwUrl = "http://www." + passportBaseUrl;




 

// 插件
(function($) {
    // 弹出层
    $.fn.passportPopup = function(options) {
        var settings = $.extend({
            'popupId': null, // 弹出层id
            'url': null, // 要插入的HTML的URL, 如果弹层隐藏在页面中, 则不用设置
            'string': null, // html 字符串
            'maskId': 'mask', // 遮罩id,null不显示遮罩
            'position': 'fixed', // 定位类别[fixed|absolute]
            'noscroll': false, // 是否禁止页面滚动[true|false]
            'zindex': null, // z-index值
            'width': null,  // 宽度
            'height': null, // 高度
            'countdown': null,   // 倒计时关闭(正整数,以秒为单位)
            'timer': null,   // 倒计时数字输出位置
            'jump': null,    // 关闭时跳转URL
            'fn': null, // 弹出调用函数
            'callback': null // 关闭回调
        }, options);

        // 如果popupId不存在, 则返回
        if (!settings.popupId) return false;
        // 重命名参数名称
        var _popupId = settings.popupId,
            _url = settings.url,
            _string = settings.string,
            _maskId = settings.maskId,
            _position = settings.position,
            _noscroll = settings.noscroll,
            _zindex = settings.zindex,
            _width = settings.width,
            _height = settings.height,
            _countdown = settings.countdown,
            _timer = settings.timer,
            _jump = settings.jump;

        var $popup = $("#" + _popupId);
        // 倒计时节点
        var $countdown = $('<div class="countdownTxt">');

        // 弹出层显示
        if ($popup.length > 0) {
            // 如果弹层已弹出, 则返回
            if ($popup.is(':visible')) return;
            // 关闭其他已弹出弹层
            closeActive();
            // 判断是否启用遮罩
            if (_maskId !== null) mask();
            // 显示自有弹层并添加属性
            $popup.attr({popup: "show", popmark: "own"}).show();
            // 禁止页面滚动
            if (_noscroll === true) var _scroll = noscroll();
            // 设置宽高
            if (_width !== null) $popup.css("width", _width + 'px');
            if (_height !== null) $popup.css("height", _height + 'px');
            // 设置zIndex值
            if (_zindex !== null) {
                $popup.css({zIndex: Number(_zindex) + 1});
            } else {
                var zIndex = $("#" + _maskId).css('z-index');
                $popup.css({zIndex: Number(zIndex) + 1})
            }
            // 弹层定位
            popupPsotion(_popupId, _position);
            //关闭弹层
            $("#" + _popupId + " .close").bind('click', function() {
                close($(this), _scroll);
                $("#" + _maskId).hide();
            });
            // 弹出调用函数
            if (settings.fn !== null) settings.fn();
            // 倒计时关闭
            if (_countdown !== null) countdown(_countdown, _timer);
        } else if (_string !== null) {
            // 如果弹层已弹出, 则返回
            if ($('body').find("#" + _popupId).length) return;
            // 关闭其他已弹出弹层
            closeActive();
            //判断是否启用遮罩
            if (_maskId !== null) mask();
            // 插入弹层
            $('body').append(_string);

            var $popup = $("#" + _popupId);
            // 添加属性
            $popup.attr("popup", "show").show();
            // 禁止页面滚动
            if (_noscroll === true) var _scroll = noscroll();
            // 设置宽高
            if (_width !== null) $popup.css("width", _width + 'px');
            if (_height !== null) $popup.css("height", _height + 'px');
            // 设置zIndex值
            if (_zindex !== null) {
                $popup.css({zIndex: Number(_zindex) + 1});
            } else {
                var zIndex = $("#" + _maskId).css('z-index');
                $popup.css({zIndex: Number(zIndex) + 1})
            }
            // 弹层定位
            popupPsotion(_popupId, _position);
            //关闭弹层
            $("#" + _popupId + " .close").bind('click', function() {
                close($(this), _scroll);
                $("#" + _maskId).hide();
            });
            // 弹出调用函数
            if (settings.fn !== null) settings.fn();
            // 倒计时关闭
            if (_countdown !== null) countdown(_countdown, _timer);
        } else if (_url !== null) {
            $.ajax({
                type: "GET",
                url: _url,
                success: function(res) {
                    // 如果弹层已弹出, 则返回
                    if ($('body').find("#" + _popupId).length) return;
                    // 关闭其他已弹出弹层
                    closeActive();
                    //判断是否启用遮罩
                    if (_maskId !== null) mask();
                    // 插入弹层
                    $('body').append(res);

                    var $popup = $("#" + _popupId);
                    // 添加属性
                    $popup.attr("popup", "show").show();
                    // 禁止页面滚动
                    if (_noscroll === true) var _scroll = noscroll();
                    // 设置宽高
                    if (_width !== null) $popup.css("width", _width + 'px');
                    if (_height !== null) $popup.css("height", _height + 'px');
                    // 设置zIndex值
                    if (_zindex !== null) {
                        $popup.css({zIndex: Number(_zindex) + 1});
                    } else {
                        var zIndex = $("#" + _maskId).css('z-index');
                        $popup.css({zIndex: Number(zIndex) + 1})
                    }
                    // 弹层定位
                    popupPsotion(_popupId, _position);
                    //关闭弹层
                    $("#" + _popupId + " .close").bind('click', function() {
                        close($(this), _scroll);
                        $("#" + _maskId).hide();
                    });
                    // 弹出调用函数
                    if (settings.fn !== null) settings.fn();
                    // 倒计时关闭
                    if (_countdown !== null) countdown(_countdown, _timer);
                }
            });
        } else {
            return false;
        }
        // 禁止页面滚动
        function noscroll() {
            var $html = $('html');
            var originHtml = $html.attr('style');
            $html.css({overflow: 'hidden'});
            return originHtml;
        }
        // 遮罩
        function mask() {
            var $mask = $("#" + _maskId);
            if ($mask.length > 0) {
                // 如果遮罩以显示, 则返回
                if ($mask.is(":visible")) return;
                $mask.show().css({zIndex: _zindex});
            } else {
                var maskNode = $("<div class='passport-mask' id='" + _maskId + "'>");
                $('body').append(maskNode);
                maskNode.show().css({zIndex: _zindex});
            }
        }
        // 关闭其他已弹出弹层
        function closeActive() {
            $('body').find('[popup="show"]').attr("popup","hide").find('.close').click();
        }
        // 倒计时关闭
        function countdown(time, node) {
            // 参数说明:
            // 1. time是设定的倒计时时间;
            // 2. node是自定义显示倒计时的位置;
            if ((typeof time != 'number') || time <= 1) throw new Error('参数类型错误或小于等于1');
            var _time = Math.ceil(time - 1);
            var _popup = $("#" + _popupId);
            // 显示倒计时
            _timerNum();
            // 清除倒计时
            window.clearTimeout(this._t);
            // 倒计时开始
            this._t = window.setTimeout(function() {
                if (_time > 1) {
                    // 显示倒计时
                    _timerNum();
                   return countdown(_time, node);
                } else {
                    $("#" + _popupId + " .close").click();
                }
            }, 1000);

            function _timerNum() {
                // 如果自定义了时间显示节点名, 则在指定位置显示倒计时
                if (node !== null) {
                    _popup.find(node).text(_time + "秒");
                } else {
                    _popup.find("." + $countdown[0].className).remove();
                    _popup.children('.wrap').append($countdown).find($countdown).text(_time + "秒");
                }
            }
        }
        //关闭按钮
        function close(obj, noscroll) {
            // 清除倒计时
            window.clearTimeout(this._t);
            // 取消禁止页面滚动
            if (_noscroll === true) {
                if (noscroll == undefined) {
                    $('html').removeAttr('style');
                } else {
                    $('html').attr('style', noscroll);
                }
            }
            // 跳转
            if (_jump !== null) document.location = _jump;
            // 设置弹层属性
            var _popup = obj.parents("#" + _popupId);
            var _mark = _popup.attr("popmark");
            _popup.attr("popup", "hide");
            // 如果popmark属性为own则隐藏，否则删除
            if (_mark == "own") {
                _popup.hide();
            } else {
                _popup.remove();
            }
            // 关闭回调
            if (settings.callback !== null) settings.callback();
        }
        //弹层定位
        function popupPsotion(popupId, position) {
            var $popup = $("#" + popupId),
                $win = $(window),
                winW = $win.width(),
                winH = $win.height(),
                popupW = $popup.width(),
                popupH = $popup.height(),
                scrollT = $win.scrollTop(),
                scrollL = $win.scrollLeft();
            if (popupH > winH) {
                // 如果弹层高度大于视窗高度, popupTop为滚动条Top值
                var popupTop = scrollT,
                    popupLeft = (winW - popupW) / 2 + scrollL;

                $popup.css({
                    position: "absolute",
                    top: popupTop,
                    left: popupLeft,
                    margin: 0
                });
            } else if (position == "fixed") {
                var popupTop = (winH - popupH) / 2,
                    popupLeft = (winW - popupW) / 2;

                $popup.css({
                    position: "fixed",
                    top: popupTop,
                    left: popupLeft,
                    margin: 0
                });
            } else if (position == "absolute") {
                var popupTop = (winH - popupH) / 2 + scrollT,
                    popupLeft = (winW - popupW) / 2 + scrollL;

                $popup.css({
                    position: "absolute",
                    top: popupTop,
                    left: popupLeft,
                    margin: 0
                });
            }
        }
        // 窗口调整时重新定位
        $(window).resize(function() {
            popupPsotion(_popupId, _position);
        });
    };
    // 密码强度
    $.fn.passportPasswordStrong = function(elem) {
        var passwordSafe = {
            safe: function(val) {
                if (val == '') return 0;
                var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
                var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
                var enoughRegex = new RegExp("(?=.{6,}).*", "g");
                if (enoughRegex.test(val) == false) {
                    return 1;
                } else if (strongRegex.test(val)) {
                    return 3;
                } else if (mediumRegex.test(val)) {
                    return 2;
                } else {
                    return 1;
                }
                return false;
            },
            state: function(elem, level, stateclass) {
                var $elem = elem;
                var stateClass = stateclass[0] + ' ' + stateclass[1] + ' ' + stateclass[2];
                switch (level) {
                    case 1:
                        $elem.removeClass(stateClass).addClass(stateclass[0]);
                        break;
                    case 2:
                        $elem.removeClass(stateClass).addClass(stateclass[1]);
                        break;
                    case 3:
                        $elem.removeClass(stateClass).addClass(stateclass[2]);
                        break;
                    case 0:
                        $elem.removeClass(stateClass);
                        break;
                }
            }
        };
        var $this = $(this);
        $this.bind('keyup', function() {
            var val = $.trim($this.val());
            var level = passwordSafe.safe(val);
            passwordSafe.state(elem, level, ['safely-danger', 'safely-general', 'safely-safe']);
        });
    };
    // placeholder
    $.fn.passportPlaceholder = function(holderclass) {
        var isIE9 = navigator.userAgent.indexOf('MSIE 9.0') > -1;
        var $this = $(this);
        if (isIE9) {
            $this.each(function() {
                var $this = $(this);
                var holder = $this.attr('placeholder');
                var holderHtml = '<div class="js-placeholder">' + holder + '</div>';
                $this.addClass(holderclass).attr('autocomplete', 'off').before(holderHtml);

                if ($this.val()) {
                    $this.removeClass(holderclass).siblings('.js-placeholder').hide();
                }

                $this.bind('focus', function() {
                    $(this).removeClass(holderclass).siblings('.js-placeholder').hide();
                });
                $this.bind('blur', function() {
                    var $this = $(this);
                    if (!$this.val()) $this.addClass(holderclass).siblings('.js-placeholder').show();
                });
            });
        } else {
            $this.each(function() {
                var $this = $(this);
                $this.removeClass('placeholder').attr({'autocomplete': 'off'});
            });
        }

        return this;
    };
    $.fn.passportSetBtnTimer = function(options) {
        "use strict";
        var settings = $.extend({
            'time': 60,
            'timewhich': null,
            'timetext': null,
            'timerstart': null,
            'timerend': null,
            'callback': null
        }, options);

        var self = this,
            oldv = self.text(),
            lock = 0,
            timer;

        if (settings.timerstart) settings.timerstart(this);
        this.attr("disabled", "disabled");
        // 设置手机号码不可修改
        this.parents('.passport-form').find('input[name="phone"]').attr({'readonly': 'readonly'});

        var text = settings.timetext ? settings.timetext : 's后重新获取';
        var tick = function() {
            settings.time--;
            if (settings.timewhich) {
                settings.timewhich.text(settings.time + text);
            } else {
                self.text(settings.time + text);
            }
            if (settings.time < 1) {
                if (settings.timerend) {
                    settings.timerend(self);
                    self.parents('.passport-form').find('input[name="phone"]').removeAttr('readonly');
                    window.clearInterval(timer);
                } else {
                    self.removeAttr("disabled");
                    self.parents('.passport-form').find('input[name="phone"]').removeAttr('readonly');
                    window.clearInterval(timer);
                    self.text('重新发送');
                }
                if (settings.callback) settings.callback();
            }
        };
        if (lock == 0) {
            settings.time++;
            tick();
            lock == 1;
        }
        return this.each(function() {
            timer = window.setInterval(tick, 1000);
        });
    }
})(jQuery);


var passportLoginhtml = '<div class="passport-popup" id="login-popup"><div class="layout-inner"><div class="hd"><i class="close"></i></div><div class="bd"><div class="passport-sign"><div class="main-form main-form-sign"><div class="passport-tab" id="login-tabs"><div class="tabs"><ul><li class="active" data-tab="login" jktag="0001|0.1|91031">登录</li><li data-tab="fastlogin" jktag="0001|0.1|91028">免注册登录</li></ul></div><div class="tabbed"><div class="tab-group" style="display: block;"><form class="passport-form passport-form-sign" id="login-form-popup" action="' + passportUrl + '/submit/login" method="post"><div class="form-item"><div class="form-cont"><input type="text" name="uname" class="passport-txt xl w-full" tabindex="1" placeholder="手机 / 用户名 / 邮箱"/></div></div><div class="form-item"><div class="form-cont"><input type="password" name="password" class="passport-txt xl w-full" tabindex="2" placeholder="输入6~32位密码"/></div></div><div class="form-item form-imgcode mb-25"><div class="form-cont"><div class="layout-inner"><input type="text" name="verify" class="passport-txt xl w-lg" tabindex="3" placeholder="验证码" /></div><div class="imgcode"><img src="" alt="" class="verifyCode" jktag="0001|0.1|91029" /><i class="passport-icon icon-refresh refreshCode" jktag="0001|0.1|91029"></i></div></div></div><div class="form-item form-sevenday"><div class="form-cont clearfix"><label><input type="checkbox" class="passport-sevenday" />7天内免登录</label><a href="' + passportUrl + '/sso/forget" class="forget-link" jktag="0001|0.1|91030">忘记密码</a></div></div><div class="form-item"><div class="form-cont"><input type="button" id="login-pop-submit" class="passport-btn passport-btn-def xl w-full" tabindex="4" value="登录" jktag="0001|0.1|91038" /></div></div></form></div><div class="tab-group"><form class="passport-form passport-form-sign" id="fastlogin-form-popup" action="' + passportUrl + '/submit/login_phone" method="post"><div class="form-item"><div class="form-cont"><input type="text" name="phone" class="passport-txt xl w-full" tabindex="1" placeholder="请输入手机号" /></div></div><div class="form-item form-imgcode"><div class="form-cont"><div class="layout-inner"><input type="text" name="verify" class="passport-txt xl w-lg " tabindex="2" placeholder="验证码" /></div><div class="imgcode"><img src="" alt="" class="verifyCode" jktag="0001|0.1|91029" /><i class="passport-icon icon-refresh refreshCode" jktag="0001|0.1|91029"></i></div></div></div><div class="form-item form-mcode mb-25"><div class="form-cont"><input type="text" name="verify_code" class="passport-txt xl w-full" tabindex="3" placeholder="动态码" /><div class="btn-getcode"><button type="button" class="passport-btn js-getcode" jktag="0001|0.1|91039">获取动态码</button></div><div class="passport-sms getVoice" style="display: none;">未收到短信？使用<a href="javascript:;" class="js-getvoice" jktag="0001|0.1|91045">语音动态码</a></div><div class="passport-sms reVoice" style="display: none;"><span class="js-revoice"></span>，请注意接听来电</div></div></div><div class="form-item form-rememb"><div class="form-cont"><label><input type="checkbox" id="remember" class="rememb" />记住手机号</label></div></div><div class="form-item"><div class="form-cont"><input type="button" id="fastlogin-pop-submit" class="passport-btn passport-btn-def xl w-full" tabindex="4" value="登录" jktag="0001|0.1|91043" /></div></div></form></div></div></div></div><div class="aside"><div class="passport-goto">没有账号?<a href="javascript:;" tabindex="5" class="diaRegBtnTab" jktag="0001|0.1|91032">免费注册</a></div><div class="passport-third"><header class="hd"><div class="layout-inner"><h3>合作方帐号登录</h3></div></header><div class="links"><a href="' + passportUrl + '/connect/qq" jktag="0001|0.1|91061" data-pl="qq"><i class="passport-icon icon-tencent"></i></a><a href="' + passportUrl + '/connect/weibo" jktag="0001|0.1|91058" data-pl="weibo"><i class="passport-icon icon-weibo"></i></a><a href="' + passportUrl + '/connect/weixin" jktag="0001|0.1|91059" data-pl="weixin"><i class="passport-icon icon-weixin"></i></a><a href="' + passportUrl + '/connect/eoe" jktag="0001|0.1|91060" data-pl="eoe"><i class="passport-icon icon-eoe"></i></a></div></div></div></div></div></div></div>';


var passportReghtml = '<div class="passport-popup" id="register-popup"><div class="layout-inner"><div class="hd"><i class="close"></i></div><div class="bd"><div class="passport-sign"><div class="main-form"><h2>欢迎注册极客学院</h2><form class="passport-form passport-form-sign" id="register-form-popup" action="' + passportUrl + '/submit/reg_phone"><div class="form-item"><div class="form-cont"><input type="text" name="phone" class="passport-txt xl w-full" tabindex="1" placeholder="请输入手机号" /></div></div><div class="form-item"><div class="form-cont"><input type="password" name="password" class="passport-txt xl w-full" tabindex="2" placeholder="输入6~32位密码"/><ul class="passport-safely" id="safely"><li class="danger">弱</li><li class="general">中</li><li class="safe">高</li></ul></div></div><div class="form-item form-imgcode"><div class="form-cont"><div class="layout-inner"><input type="text" name="verify" class="passport-txt xl w-lg" tabindex="3" placeholder="验证码"></div><div class="imgcode"><img src="" alt="" class="verifyCode" jktag="0001|0.1|91034" /><i class="passport-icon icon-refresh refreshCode" jktag="0001|0.1|91034"></i></div></div></div><div class="form-item form-mcode mb-25"><div class="form-cont"><input type="text" name="verify_code" class="passport-txt xl w-full" tabindex="4" placeholder="动态码"/><div class="btn-getcode"><button type="button" class="passport-btn js-getcode" jktag="0001|0.1|91035">获取动态码</button></div><div class="passport-sms getVoice" style="display: none;">未收到短信？使用<a href="javascript:;" class="js-getvoice" jktag="0001|0.1|91044">语音动态码</a></div><div class="passport-sms reVoice" style="display: none;"><span class="js-revoice"></span>，请注意接听来电</div></div></div><div class="form-item form-treaty"><div class="form-cont"><input type="checkbox" name="treaty" checked="checked" value="treaty" /><a href="' + passportWwwUrl + '/help/service.html" target="_blank" class="treaty">极客学院用户协议</a></div></div><div class="form-item"><div class="form-cont"><input type="button" id="register-pop-submit" class="passport-btn passport-btn-def xl w-full" tabindex="5" value="注册" jktag="0001|0.1|91037" /></div></div></form></div><div class="aside"><div class="passport-goto">已有帐号<a href="javascript:;" tabindex="6" class="diaLoginBtnTab" jktag="0001|0.1|91040">立即登录</a></div><div class="passport-third"><header class="hd"><div class="layout-inner"><h3>合作方帐号登录</h3></div></header><div class="links"><a href="' + passportUrl + '/connect/qq" jktag="0001|0.1|91053" data-pl="qq"><i class="passport-icon icon-tencent"></i></a><a href="' + passportUrl + '/connect/weibo" jktag="0001|0.1|91054" data-pl="weibo"><i class="passport-icon icon-weibo"></i></a><a href="' + passportUrl + '/connect/weixin" jktag="0001|0.1|91055" data-pl="weixin"><i class="passport-icon icon-weixin"></i></a><a href="' + passportUrl + '/connect/eoe" jktag="0001|0.1|91056" data-pl="eoe"><i class="passport-icon icon-eoe"></i></a></div></div><div class="passport-ad" id="reg-ad01"></div></div></div></div></div></div>';


// 判断域名，特殊设置
if(passportHostArr[0] == "e"){
	var passportCurrPage = passportDomain.currentUrl.match(/\/\w+\.html/);
	passportCurrPage = passportCurrPage[0].replace(/\.html/,'');
	passportCurrPage = passportCurrPage.substr(1);
	// var passportClose = (passportHostArr[0] == "e" && passportCurrPage == "android") ? 'close-event' : 'close';

	if(passportCurrPage == "android"){
		var passportReghtml = '<div class="passport-popup" id="register-popup"><div class="layout-inner"><div class="hd"><i class="close-event"></i><input type="hidden" class="close" /></div><div class="bd"><div class="passport-sign"><div class="main-form"><h2>欢迎注册极客学院</h2><form class="passport-form passport-form-sign" id="register-form-popup" action="' + passportUrl + '/submit/reg_phone"><div class="form-item"><div class="form-cont"><input type="text" name="phone" class="passport-txt xl w-full" tabindex="1" placeholder="请输入手机号" /></div></div><div class="form-item"><div class="form-cont"><input type="password" name="password" class="passport-txt xl w-full" tabindex="2" placeholder="输入6~32位密码"/><ul class="passport-safely" id="safely"><li class="danger">弱</li><li class="general">中</li><li class="safe">高</li></ul></div></div><div class="form-item form-imgcode"><div class="form-cont"><div class="layout-inner"><input type="text" name="verify" class="passport-txt xl w-lg" tabindex="3" placeholder="验证码"></div><div class="imgcode"><img src="" alt="" class="verifyCode" jktag="0001|0.1|91034" /><i class="passport-icon icon-refresh refreshCode" jktag="0001|0.1|91034"></i></div></div></div><div class="form-item form-mcode mb-25"><div class="form-cont"><input type="text" name="verify_code" class="passport-txt xl w-full" tabindex="4" placeholder="动态码"/><div class="btn-getcode"><button type="button" class="passport-btn js-getcode" jktag="0001|0.1|91035">获取动态码</button></div><div class="passport-sms getVoice" style="display: none;">未收到短信？使用<a href="javascript:;" class="js-getvoice" jktag="0001|0.1|91044">语音动态码</a></div><div class="passport-sms reVoice" style="display: none;"><span class="js-revoice"></span>，请注意接听来电</div></div></div><div class="form-item form-treaty"><div class="form-cont"><input type="checkbox" name="treaty" checked="checked" value="treaty" /><a href="' + passportWwwUrl + '/help/service.html" target="_blank" class="treaty">极客学院用户协议</a></div></div><div class="form-item"><div class="form-cont"><input type="button" id="register-pop-submit" class="passport-btn passport-btn-def xl w-full" tabindex="5" value="注册" jktag="0001|0.1|91037" /></div></div></form></div><div class="aside"><div class="passport-goto">已有帐号<a href="javascript:;" tabindex="6" class="diaLoginBtnTab" jktag="0001|0.1|91040">立即登录</a></div><div class="passport-third"><header class="hd"><div class="layout-inner"><h3>合作方帐号登录</h3></div></header><div class="links"><a href="' + passportUrl + '/connect/qq" jktag="0001|0.1|91053" data-pl="qq"><i class="passport-icon icon-tencent"></i></a><a href="' + passportUrl + '/connect/weibo" jktag="0001|0.1|91054" data-pl="weibo"><i class="passport-icon icon-weibo"></i></a><a href="' + passportUrl + '/connect/weixin" jktag="0001|0.1|91055" data-pl="weixin"><i class="passport-icon icon-weixin"></i></a><a href="' + passportUrl + '/connect/eoe" jktag="0001|0.1|91056" data-pl="eoe"><i class="passport-icon icon-eoe"></i></a></div></div><div class="passport-ad" id="reg-ad01"></div></div></div></div></div></div>';
	}
}
// baidu ad
document.write("<script src='http://cbjs.baidu.com/js/m.js'></script>"); 


// sign javascript
var SIGN = {
    lock: true,
    submitLock: true,
    total: 60,
    oldval: {},
    valid: {},
    invalid: {},
    init: function() {
        var self = this;
        this.bindEle();
        this.signPop();
    },
    bindEle: function() {
        var self = this;
        $('body').delegate('.passport-txt', 'focus', function() {
            PASSPORT.removeHint($(this), self.hintclass());
            PASSPORT.removeInputState($(this), self.inputclass());
        });
        $('body').delegate('#register-form-popup input[name="treaty"]', 'click', function() {
            if ($('#register-form-popup input[name="treaty"]').is(':checked')) {
                PASSPORT.removeHint($(this), self.hintclass());
                PASSPORT.removeInputState($(this), self.inputclass());
            }
        });
    },
    hintclass: function() {
        return PASSPORT.toHintClass('passport-note', ['passport-error-text']);
    },
    inputclass: function() {
        return PASSPORT.toStateClass(['passport-error-input']);
    },
    hintEvent: function(elem, errhint) {
        PASSPORT.insetHint(elem, errhint, this.hintclass());
        PASSPORT.removeInputState(elem, this.inputclass());
        PASSPORT.addInputState(elem, this.inputclass());
    },
    hintArgs: {
        tag: 'div',
        hint: 'passport-note',
        state: 'passport-error-text'
    },
    submit: function(param) {
        var self = this;
        var sets = $.extend({
            'form': null,
            'button': null,
            'text': null,
            'error': null,
            'success': null
        }, param);
        var oldtext = sets.button.val();
        if (!self.submitLock) return false;
        self.submitLock = false;
        sets.button.val(sets.text);
        $.post(sets.form.attr('action') + '?is_ajax=1&jsoncallback=?', sets.form.serialize(), function(res) {
            if (res.status != 1) {
                PASSPORT.msgBox(0, res.msg);
                self.submitLock = true;
                sets.form.find('.verifyCode').click();
                sets.button.val(oldtext);
                if (sets.error) sets.error(res);
            } else {
                if (sets.success) sets.success(res);
                document.location.href = document.location.href;
            }
        }, 'jsonp');
    },
    resetData: function(mode) {
        this.oldval[mode] = {};
        this.valid[mode] = {};
        this.invalid[mode] = {};
    },
    required: function(param) {
        var self = this;
        var sets = $.extend({
            'elem': null,
            'val': null,
            'hint': null,
            'mode': null,
            'error': null,
            'success': null,
            'rules': null,
            'rangelength': null,
        }, param);
        var name = sets.elem.attr('name');
        var type = sets.elem.attr('type');
        var errhint;
        if (type == 'text' || type == 'password' || type == 'textarea') {
            if (!sets.val) {
                self.hintArgs.text = sets.hint;
                errhint = PASSPORT.createHint(self.hintArgs, 'span');
                self.hintEvent(sets.elem, errhint);
                self.oldval[sets.mode][name] = '';
                if (sets.error) sets.error();
                return false;
            } else {
                if (sets.success) sets.success();
            }
        } else if (type == 'checkbox' || type == 'radio') {
            if (!sets.elem.is(':checked')) {
                self.hintArgs.text = sets.hint;
                errhint = PASSPORT.createHint(self.hintArgs, 'span');
                self.hintEvent(sets.elem, errhint);
                self.oldval[sets.mode][name] = '';
                if (sets.error) sets.error();
                return false;
            } else {
                if (sets.success) sets.success();
            }
        }
        if (sets.rules && !self.rules(sets.rules)) return false;
        if (sets.rangelength && !self.rangelength(sets.rangelength)) return false;
        return true;
    },
    rules: function(param) {
        var self = this;
        var sets = $.extend({
            'elem': null,
            'val': null,
            'rules': null,
            'hint': null,
            'error': null,
            'success': null
        }, param);
        var rules = sets.rules.test(sets.val);
        var errhint;
        if (!rules) {
            self.hintArgs.text = sets.hint;
            errhint = PASSPORT.createHint(self.hintArgs, 'span');
            self.hintEvent(sets.elem, errhint);
            if (sets.error) sets.error();
            return false;
        } else {
            if (sets.success) sets.success();
        }
        return true;
    },
    rangelength: function(param) {
        var self = this;
        var sets = $.extend({
            'elem': null,
            'val': null,
            'rangelength': null,
            'hint': null
        }, param);
        var errhint, minlength = sets.rangelength[0], maxlength = sets.rangelength[1];
        if (sets.val.length < minlength || sets.val.length > maxlength) {
            self.hintArgs.text = sets.hint;
            errhint = PASSPORT.createHint(self.hintArgs, 'span');
            self.hintEvent(sets.elem, errhint);
            return false;
        }
        return true;
    },
    remote: function(args, settings) {
        var self = this;
        var sets = $.extend({
            'context': null,
            'mode': null,
            'elem': settings.elem,
            'hint': settings.hint,
            'reverse': false,
            'error': null,
            'success': null
        }, settings);
        var name = sets.elem.attr('name');
        var status, errhint;
        var param = $.extend(true, {
            type: 'post',
            dataType: 'json',
            context: sets.context,
            error: function() {
                PASSPORT.msgBox(0, '远程：网络出错了，过会再试！');
            },
            success: function(res) {
                status = sets.reverse ? 0 : 1;
                if (res.status !== status) {
                    self.hintArgs.text = sets.hint;
                    errhint = PASSPORT.createHint(self.hintArgs, 'span');
                    self.hintEvent(sets.elem, errhint);
                    self.invalid[sets.mode][name] = true;
                    delete self.valid[sets.mode][name];
                    if (sets.error) return sets.error(res);
                } else {
                    self.valid[sets.mode][name] = true;
                    delete self.invalid[sets.mode][name];
                    if (sets.success) return sets.success(res);
                }
            }
        }, args);
        return param;
    },
    getVoice: function(form, param) {
        var self = this;
        self.lock = true;

        var sets = $.extend({
            'restype': 4,
            'phoneError': null,
            'verifyError': null
        }, param);
        // 获取语音动态码
        $(form + ' .js-getvoice').unbind('click');
        $(form + ' .js-getvoice').removeClass('disabled');
        $(form + ' .js-getvoice').bind('click', function() {
            var $this = $(this);
            var $form = $(form);
            var $getBtn = $form.find('.js-getcode');
            var $phone = $form.find('input[name="phone"]');
            var $verify = $form.find('input[name="verify"]');
            var phoneNum = $.trim($phone.val());
            var verifyCode = $.trim($verify.val());
            var $getVoice = $this.parent('.getVoice');
            var $reVoice = $getVoice.siblings('.reVoice');
            var $revoice = $reVoice.find('.js-revoice');
            var data = {
                phone: phoneNum,
                verify: verifyCode,
                type: sets.restype,
            };
            var timestart = function() {
                $getVoice.hide();
                $reVoice.show();
                $getBtn.prop('disabled', true);
            };
            var timeend = function() {
                $getVoice.show();
                $reVoice.hide();
                $getBtn.removeAttr('disabled');
                self.lock = true;
            };
            $.ajax({
                type: 'post',
                url: passportUrl + '/sso/voice?is_ajax=1&jsoncallback=?',
                dataType: 'jsonp',
                data: data,
                error: function() {
                    PASSPORT.msgBox(0, '语音：网络出错了，过会再试！');
                    $revoice.passportSetBtnTimer({
                        time: 0,
                        timerstart: function() {
                            timestart();
                        },
                        timerend: function() {
                            timeend();
                        }
                    });
                },
                success: function(res) {
                    if (res.status == 1) {
                        $revoice.passportSetBtnTimer({
                            time: self.total,
                            timerstart: function() {
                                timestart();
                            },
                            timerend: function() {
                                timeend();
                            }
                        });
                    } else {
                        PASSPORT.msgBox(0, res.msg);
                        $revoice.passportSetBtnTimer({
                            time: 0,
                            timerstart: function() {
                               timestart();
                            },
                            timerend: function() {
                                timeend();
                            }
                        });
                    }
                },
            });
        });
    },
    getMcode: function(form, param) {
        var self = this;
        self.lock = false;
        var sets = $.extend({
            restype: 4,
        }, param);
        var $this = $(this);
        var $form = $(form);
        var $getBtn = $form.find('.js-getcode');
        var $phone = $form.find('input[name="phone"]');
        var $verify = $form.find('input[name="verify"]');
        var phoneNum = $.trim($phone.val());
        var verifyCode = $.trim($verify.val());

        var phoneType = passportReg.phone.test(phoneNum);
        self.hintArgs.text = passportHint.phone.required;
        var errhint = PASSPORT.createHint(self.hintArgs, 'span');

        if (!phoneNum) {
            self.hintEvent($phone, errhint);
            self.lock = true;
        } else {
            self.hintArgs.text = passportHint.phone.rules;
            errhint = PASSPORT.createHint(self.hintArgs, 'span');
            if (!phoneType) {
                self.hintEvent($phone, errhint);
                self.lock = true;
            }
        }
        self.hintArgs.text = passportHint.verify.required;
        errhint = PASSPORT.createHint(self.hintArgs, 'span');
        if (!verifyCode) {
            self.hintEvent($verify, errhint);
        }
        if (!phoneNum || !phoneType || !verifyCode) {
            self.lock = true;
            return false;
        }

        if (sets.restype == 4) {
            $.ajax({
                type: 'post',
                url: passportUrl + '/check/phone?is_ajax=1&jsoncallback=?',
                data: {phone: phoneNum},
                dataType: 'jsonp',
                error: function() {
                    PASSPORT.msgBox(0, '手机：网络出错了，过会再试！');
                    self.lock = true;
                },
                success: function(res) {
                    if (res.status == 1) {
                        $.ajax({
                            type: 'post',
                            url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                            data: {verify: verifyCode},
                            dataType: 'jsonp',
                            error: function() {
                                PASSPORT.msgBox(0, '验证：网络出错，过会再试');
                                $getBtn.passportSetBtnTimer({
                                    time: 0,
                                    callback: function() {
                                        self.lock = true;
                                    }
                                });
                            },
                            success: function(res) {
                                if (res.status == 0) {
                                    // 创建提示
                                    self.hintArgs.text = '验证码错误';
                                    var ajaxhint = PASSPORT.createHint(self.hintArgs, 'span');
                                    self.hintEvent($verify, ajaxhint);
                                    self.lock = true;
                                    if (sets.verifyError) sets.verifyError(res);
                                    return false;
                                }

                                $getBtn.addClass('passport-btn-def').text('短信发送中');

                                var data = {
                                    phone: phoneNum,
                                    verify: verifyCode,
                                    type: 4,
                                };
                                $.ajax({
                                    type: "post",
                                    url: passportUrl + '/sso/sms?is_ajax=1&jsoncallback=?',
                                    data: data,
                                    dataType: 'jsonp',
                                    error: function() {
                                        PASSPORT.msgBox(0, '短信：网络出错，过会再试');
                                        $getBtn.passportSetBtnTimer({
                                            time: 0,
                                            timerstart: function(elem) {
                                                $form.find('.js-getvoice').addClass('disabled').unbind('click');
                                                elem.removeClass('passport-btn-def');
                                            },
                                            callback: function() {
                                                self.lock = true;
                                                // 获取语音动态码
                                                self.getVoice(form, {restype: 4});
                                            }
                                        });
                                    },
                                    success: function(res) {
                                        if (res.status == 1) {
                                            $getBtn.passportSetBtnTimer({
                                                time: self.total,
                                                timerstart: function(elem) {
                                                    $form.find('.js-getvoice').addClass('disabled').unbind('click');
                                                    elem.removeClass('passport-btn-def');
                                                },
                                                callback: function() {
                                                    self.lock = true;
                                                    $form.find('.getVoice').show();
                                                    // 获取语音动态码
                                                    self.getVoice(form, {restype: 4});
                                                },
                                            });
                                        } else {
                                            PASSPORT.msgBox(0, res.msg);
                                            $('.verifyCode').click();
                                            $getBtn.passportSetBtnTimer({
                                                time: 0,
                                                timerstart: function(elem) {
                                                    $form.find('.js-getvoice').addClass('disabled').unbind('click');
                                                    elem.removeClass('passport-btn-def');
                                                },
                                                callback: function() {
                                                    // 获取语音动态码
                                                    self.lock = true;
                                                    self.getVoice(form, {restype: 4});
                                                }
                                            });
                                        }
                                    },
                                });
                            }
                        });
                    } else {
                        self.hintArgs.text = passportHint.phone.remote;
                        errhint = PASSPORT.createHint(self.hintArgs, 'span');
                        self.hintEvent($phone, errhint);
                        if (sets.phoneError) sets.phoneError(res);
                        self.lock = true;
                    }
                }
            });
        } else if (sets.restype == 5) {
            $.ajax({
                type: 'post',
                url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                data: {
                    verify: verifyCode
                },
                dataType: 'jsonp',
                error: function() {
                    PASSPORT.msgBox(0, '验证：网络出错，过会再试');
                    $getBtn.passportSetBtnTimer({
                        time: 0,
                        callback: function() {
                            self.lock = true;
                        }
                    });
                },
                success: function(res) {
                    if (res.status == 0) {
                        // 创建提示
                        self.hintArgs.text = '验证码错误';
                        var ajaxhint = PASSPORT.createHint(self.hintArgs, 'span');
                        self.hintEvent($verify, ajaxhint);
                        self.lock = true;
                        return false;
                    }

                    $getBtn.addClass('passport-btn-def').text('短信发送中');

                    var data = {
                        phone: phoneNum,
                        verify: verifyCode,
                        type: 5,
                    };
                    $.ajax({
                        type: "post",
                        url: passportUrl + '/sso/sms?is_ajax=1&jsoncallback=?',
                        data: data,
                        dataType: 'jsonp',
                        error: function() {
                            PASSPORT.msgBox(0, '短信：网络出错了，请过会再试');
                            $getBtn.passportSetBtnTimer({
                                time: 0,
                                timerstart: function(elem) {
                                    $form.find('.js-getvoice').addClass('disabled').unbind('click');
                                    elem.removeClass('passport-btn-def');
                                },
                                callback: function() {
                                    self.lock = true;
                                    // 获取语音动态码
                                    self.getVoice(form, {restype: 5});
                                }
                            });
                        },
                        success: function(res) {
                            if (res.status == 1) {
                                $getBtn.passportSetBtnTimer({
                                    time: self.total,
                                    timerstart: function(elem) {
                                        $form.find('.js-getvoice').addClass('disabled').unbind('click');
                                        elem.removeClass('passport-btn-def');
                                    },
                                    callback: function() {
                                        self.lock = true;
                                        $form.find('.getVoice').show();
                                        // 获取语音动态码
                                        self.getVoice(form, {restype: 5});
                                    },
                                });
                            } else {
                                PASSPORT.msgBox(0, res.msg);
                                $('.verifyCode').click();
                                $getBtn.passportSetBtnTimer({
                                    time: 0,
                                    timerstart: function(elem) {
                                        $form.find('.js-getvoice').addClass('disabled').unbind('click');
                                        elem.removeClass('passport-btn-def');
                                    },
                                    callback: function() {
                                        // 获取语音动态码
                                        self.lock = true;
                                        self.getVoice(form, {restype: 5});
                                    }
                                });
                            }
                        },
                    });
                }
            });

        }

        if(window.hasSa) sa.track('reg_popup_enter',{name:'receive_TextCode'});
    },
    register: function(form, button) {
        if (!$(form).length) return;
        var self = this;
        var $form = $(form);
        var $phone = $form.find('input[name="phone"]');
        var $pwd = $form.find('input[name="password"]');
        var $verify = $form.find('input[name="verify"]');
        var $mcode = $form.find('input[name="verify_code"]');
        var $treaty = $form.find('input[name="treaty"]');
        var $submit = $form.find(button);
        self.oldval.register = {};
        self.valid.register = {};
        self.invalid.register = {};
        // 密码强度验证
        $pwd.passportPasswordStrong($('#safely'));

        $phone.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem: $this,
                val: val,
                hint: passportHint.phone.required,
                mode: 'register',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91046,posId: 910005});
                },
                rules: {
                    elem: $this,
                    val: val,
                    rules: passportReg.phone,
                    hint: passportHint.phone.rules,
                    error: function() {
                        if (typeof stat != 'undefined') stat.efunc({po: 91047,posId: 910005});
                    }
                }
            });
            if (check) {
                if (self.oldval.register[name] === val && self.valid.register[name]) return false;
                if (self.oldval.register[name] === val && self.invalid.register[name]) {
                    self.hintArgs.text = premote;
                    var errhint = PASSPORT.createHint(self.hintArgs, 'span');
                    self.hintEvent($this, errhint);
                    return false;
                }
                self.oldval.register[name] = val;
                $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/phone?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {phone: val}
                }, {
                    context: $form,
                    mode: 'register',
                    elem: $this,
                    hint: passportHint.phone.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91048,posId: 910005});
                    },
                    success: function () {
                        if(typeof stat != 'undefined') stat.efunc({po:91091,posId: 910005});
                        if(window.hasSa)
							sa.track('reg_popup_enter', {name:'enter_PhoneNumber'});
                    }
                }));
            }
        });
        $pwd.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.pwd.required,
                mode:'register',
                success: function() {
                    var $safely = $form.find('#safely');
                    if ($safely.hasClass('safely-danger')) {
                        if(typeof stat != 'undefined') stat.efunc({po:91049,posId: 910005});
                    } else if ($safely.hasClass('safely-general')) {
                        if(typeof stat != 'undefined') stat.efunc({po:91050,posId: 910005});
                    } else if ($safely.hasClass('safely-safe')) {
                        if(typeof stat != 'undefined') stat.efunc({po:91051,posId: 910005});
                    }
                    if(window.hasSa) sa.track('reg_popup_enter',{name:'enter_password'});
                },
                error: function () {
                    if(typeof stat != 'undefined') stat.efunc({po:91096,posId: 910005});
                },
                rangelength: {
                    elem: $this,
                    val: val,
                    rangelength: [6, 32],
                    hint: passportHint.pwd.rangelength
                }
            });
        });
        $verify.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.verify.required,
                mode:'register',
                error: function () {
                    if(typeof stat != 'undefined') stat.efunc({po:91097,posId: 910005});
                }
            });
            if (check) {
                if (self.oldval.register[name] === val && self.valid.register[name]) return false;
                if (self.oldval.register[name] === val && self.invalid.register[name]) {
                    self.hintArgs.text = passportHint.verify.remote;
                    var errhint = PASSPORT.createHint(self.hintArgs, 'span');
                    self.hintEvent($this, errhint);
                    return false;
                }
                self.oldval.register[name] = val;
                $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {verify: val}
                }, {
                    centext: $form,
                    mode: 'register',
                    elem: $this,
                    hint: passportHint.verify.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91033,posId: 910005});
                        $form.find('.verifyCode').click();
                    },
                    success: function () {
                        if(typeof stat != 'undefined') stat.efunc({po:91094,posId: 910005});
                        if(window.hasSa) sa.track('reg_popup_enter',{name:'enter_GraphCode'});
                    }
                }));
            }
        });
        $mcode.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem: $this,
                val: val,
                hint: passportHint.mobile.required,
                mode: 'register',
                error: function () {
                    if(typeof stat != 'undefined') stat.efunc({po:91098,posId: 910005});
                }
            });
        });
        $treaty.bind('click', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.treaty.required,
                mode:'register'
            });
        });
        $submit.bind('click', function() {
            PASSPORT.efunc({po:91037,posId: 910005});
            var phoneVal = $.trim($phone.val());
            var phoneCheck = self.required({
                elem:$phone,
                val:phoneVal,
                hint:passportHint.phone.required,
                mode:'register',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91046,posId: 910005});
                },
                rules: {
                    elem:$phone,
                    val:phoneVal,
                    rules:passportReg.phone,
                    hint:passportHint.phone.rules,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91047,posId: 910005});
                    }
                }
            });
            var pwdVal = $.trim($pwd.val());
            var pwdCheck = self.required({
                elem:$pwd,
                val:pwdVal,
                hint:passportHint.pwd.required,
                mode:'register',
                rangelength: {
                    elem: $pwd,
                    val: pwdVal,
                    rangelength: [6, 32],
                    hint: passportHint.pwd.rangelength
                }
            });
            var verifyVal = $.trim($verify.val());
            var verifyCheck = self.required({
                elem:$verify,
                val:verifyVal,
                hint:passportHint.verify.required,
                mode:'register'
            });
            var mcodeVal = $.trim($mcode.val());
            var mcodeCheck = self.required({
                elem:$mcode,
                val:mcodeVal,
                hint:passportHint.mobile.required,
                mode:'register'
            });
            var treatyVal = $.trim($treaty.val());
            var treatyCheck = self.required({
                elem:$treaty,
                val:treatyVal,
                hint:passportHint.treaty.required,
                mode:'register'
            });

            if (phoneCheck && pwdCheck && verifyCheck && mcodeCheck && treatyCheck) {
                 $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/phone?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {phone: phoneVal}
                }, {
                    context: $form,
                    mode: 'register',
                    elem: $phone,
                    hint: passportHint.phone.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91048,posId: 910005});
                    },
                    success: function() {
                        $.ajax(self.remote({
                                type: 'post',
                                url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                                dataType: 'jsonp',
                                data: {verify: verifyVal}
                            }, {
                                context: $form,
                                mode: 'register',
                                elem: $verify,
                                hint: passportHint.verify.remote,
                                error: function() {
                                    if(typeof stat != 'undefined') stat.efunc({po:91033,posId: 910005});
                                },
                                success: function() {
                                    self.resetData('register');
                                    self.submit({
                                        form: $form,
                                        button: $submit,
                                        text: '注册中',
                                        error: function(res) {
                                            if (res.msg == '手机验证码错误或过期') {
                                                if(typeof stat != 'undefined') stat.efunc({po:91036,posId: 910005});
                                            }
                                        },
                                        success: function() {
                                            if (typeof stat != 'undefined') stat.efunc({po:91052,posId: 910005});
                                            if(window.hasSa) sa.track('reg_popup_SignUp_success');
                                        }
                                    });
                                }
                            })
                        );
                    }
                }));
            }
        });
    },
    login: function(form, button) {
        if (!$(form).length) return;
        var self = this;
        var $form = $(form);
        var $uname = $form.find('input[name="uname"]');
        var $pwd = $form.find('input[name="password"]');
        var $verify = $form.find('input[name="verify"]');
        var $expire = $form.find('input[name="expire"]');
        var $submit = $form.find(button);
        var day = 7;
        self.oldval.login = {};
        self.valid.login = {};
        self.invalid.login = {};

        $('body').delegate(form + ' input[name="expire"]', 'click', function() {
            if ($expire.prop('checked')) {
                day = 7;
            } else {
                day = 0;
            }
            $('#expire').val(day);
        });

        $uname.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.uname.required,
                mode:'login',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91062,posId: 91095});
                }
            });
        });
        $pwd.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.pwd.required,
                mode:'login',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91063,posId: 91095});
                }
            });
        });
        $verify.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.verify.required,
                mode:'login',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91064,posId: 91095});
                }
            });
            if (check) {
                if (self.oldval.login[name] === val && self.valid.login[name]) return false;
                if (self.oldval.login[name] === val && self.invalid.login[name]) {
                    self.hintArgs.text = passportHint.verify.remote;
                    var errhint = PASSPORT.createHint(self.hintArgs, 'span');
                    self.hintEvent($this, errhint);
                    return false;
                }
                self.oldval.login[name] = val;
                $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {verify: val}
                }, {
                    centext: $form,
                    mode: 'login',
                    elem: $this,
                    hint: passportHint.verify.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91065,posId: 91095});
                        $form.find('.verifyCode').click();
                    },
                    success: function () {
                        if(typeof stat != 'undefined') stat.efunc({po:91093,posId: 91095});
                    }
                }));
            }
        });
        $submit.bind('click', function() {
            PASSPORT.efunc({po:91038,posId: 91095});
            var $this = $(this);
            var unameVal = $.trim($uname.val());
            var unameCheck = self.required({
                elem:$uname,
                val:unameVal,
                hint:passportHint.uname.required,
                mode:'login',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91062,posId: 91095});
                }
            });
            var pwdVal = $.trim($pwd.val());
            var pwdCheck = self.required({
                elem:$pwd,
                val:pwdVal,
                hint:passportHint.pwd.required,
                mode:'login',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91063,posId: 91095});
                }
            });
            var verifyVal = $.trim($verify.val());
            var verifyCheck = self.required({
                elem:$verify,
                val:verifyVal,
                hint:passportHint.verify.required,
                mode:'login',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91064,posId: 91095});
                }
            });

            if (unameCheck && pwdCheck && verifyCheck) {
               $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {verify: verifyVal}
                }, {
                    centext: $form,
                    mode: 'login',
                    elem: $verify,
                    hint: passportHint.verify.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91065,posId: 91095});
                        $form.find('.verifyCode').click();
                    },
                    success: function() {
                        self.resetData('login');
                        self.submit({
                            form: $form,
                            button: $submit,
                            text: '登录中',
                            success: function() {
                                if (typeof stat != 'undefined') stat.efunc({po:91066,posId: 91095});
                            }
                        });
                    }
                }));
            }
        });
    },
    fastlogin: function(form, button) {
        if (!$(form).length) return;
        var self = this;
        var $form = $(form);
        var $phone = $form.find('input[name="phone"]');
        var $verify = $form.find('input[name="verify"]');
        var $mcode = $form.find('input[name="verify_code"]');
        var $hold = $form.find('#remember');
        var $submit = $form.find(button);
        var phone = PASSPORT.getCookie('hold_phone', $phone);
        self.oldval.fastlogin = {};
        self.valid.fastlogin = {};
        self.invalid.fastlogin = {};

        if (phone) $hold.prop('checked', true);

        $phone.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem: $this,
                val: val,
                hint: passportHint.phone.required,
                mode: 'fastlogin',
                error: function() {
                    if (typeof stat != 'undefined') stat.efunc({
                        po: 91083,
                        posId: 91095
                    });
                },
                rules: {
                    elem: $this,
                    val: val,
                    rules: passportReg.phone,
                    hint: passportHint.phone.rules,
                    error: function() {
                        if (typeof stat != 'undefined') stat.efunc({
                            po: 91084,
                            posId: 91095
                        });
                    },
                    success: function () {
                        if (typeof stat != 'undefined') stat.efunc({
                            po: 91092,
                            posId: 91095
                        });
                    }
                }
            });
        });
        $verify.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.verify.required,
                mode:'fastlogin',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91085, posId: 91095});
                }
            });
            if (check) {
                if (self.oldval.fastlogin[name] === val && self.valid.fastlogin[name]) return false;
                if (self.oldval.fastlogin[name] === val && self.invalid.fastlogin[name]) {
                    self.hintArgs.text = passportHint.verify.remote;
                    var errhint = PASSPORT.createHint(self.hintArgs, 'span');
                    self.hintEvent($this, errhint);
                    return false;
                }
                self.oldval.fastlogin[name] = val;
                $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {verify: val}
                }, {
                    centext: $form,
                    mode: 'fastlogin',
                    elem: $this,
                    hint: passportHint.verify.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91086, posId: 91095});
                        $form.find('.verifyCode').click();
                    }
                }));
            }
        });
        $mcode.bind('blur', function() {
            var $this = $(this);
            var name = $this.attr('name');
            var val = $.trim($this.val());
            var check = self.required({
                elem:$this,
                val:val,
                hint:passportHint.mobile.required,
                mode:'fastlogin',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91087, posId: 91095});
                }
            });
        });
        $submit.bind('click', function() {
            PASSPORT.efunc({po:91043, posId: 91095});
            var $this = $(this);
            var phoneVal = $.trim($phone.val());
            var phoneCheck = self.required({
                elem: $phone,
                val: phoneVal,
                hint: passportHint.phone.required,
                mode: 'fastlogin',
                error: function() {
                    if (typeof stat != 'undefined') stat.efunc({
                        po: 91083
                    });
                },
                rules: {
                    elem: $phone,
                    val: phoneVal,
                    rules: passportReg.phone,
                    hint: passportHint.phone.rules,
                    error: function() {
                        if (typeof stat != 'undefined') stat.efunc({
                            po: 91084
                        });
                    }
                }
            });
            var verifyVal = $.trim($verify.val());
            var verifyCheck = self.required({
                elem:$verify,
                val:verifyVal,
                hint:passportHint.verify.required,
                mode:'fastlogin',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91085, posId: 91095});
                }
            });
            var mcodeVal = $.trim($mcode.val());
            var mcodeCheck = self.required({
                elem:$mcode,
                val:mcodeVal,
                hint:passportHint.mobile.required,
                mode:'fastlogin',
                error: function() {
                    if(typeof stat != 'undefined') stat.efunc({po:91087, posId: 91095});
                }
            });

            if (phoneCheck && verifyCheck && mcodeCheck) {
               $.ajax(self.remote({
                    type: 'post',
                    url: passportUrl + '/check/verify?is_ajax=1&jsoncallback=?',
                    dataType: 'jsonp',
                    data: {verify: verifyVal}
                }, {
                    centext: $form,
                    mode: 'fastlogin',
                    elem: $verify,
                    hint: passportHint.verify.remote,
                    error: function() {
                        if(typeof stat != 'undefined') stat.efunc({po:91086, posId: 91095});
                        $form.find('.verifyCode').click();
                    },
                    success: function() {
                        self.resetData('fastlogin');
                        if ($hold.prop('checked')) {
                            PASSPORT.setCookie('hold_phone', $phone.val(), 7);
                        } else {
                            PASSPORT.setCookie('hold_phone', '', 7);
                        }
                        self.submit({
                            form: $form,
                            button: $submit,
                            text: '登录中',
                            success: function() {
                                if (typeof stat != 'undefined') stat.efunc({po:91066, posId: 91095});
                            }
                        });
                    }
                }));
            }
        });
    },
    signPop: function() {
        var self = this;
        var registerPop = function(fn) {
            // 调用注册弹层请使用.diaRegBtn, 不要使用其他 class 或 id
            $(this).passportPopup({
                popupId: 'register-popup',
                string: passportReghtml,
                zindex: 9999,
                fn: function() {
                	// 神策埋点
                	if(window.hasSa) sa.track('reg_popup_visit');
                    // 埋点
                    PASSPORT.efunc({posId:910005});
                    PASSPORT.getImgcode($('#register-form-popup .verifyCode'));
                    // placeholder
                    $('.passport-txt').passportPlaceholder('placeholder');
                    // $('input[name="password"]').passportPasswordStrong($('#safely'));

                    self.register('#register-form-popup', '#register-pop-submit');

                    // 刷新图片验证码
                    $('#register-form-popup .refreshCode, #register-form-popup .verifyCode').bind('click', function() {
                        PASSPORT.efunc({po:91034, posId:910005});
                        PASSPORT.getImgcode($('#register-form-popup .verifyCode'));
                    });
                    $('#register-form-popup .verifyCode').click();

                    // 获取动态码
                    $('#register-form-popup .js-getcode').bind('click', function() {
                        PASSPORT.efunc({po:91035, posId:910005});
                        if (self.lock) self.getMcode('#register-form-popup');
                    });

                    // 第三方登录埋点
                    $('#register-popup [data-pl]').click(function() {
                        var $this = $(this);
                        var val = $this.attr('data-pl');
                        switch(val) {
                            case 'qq':
                                PASSPORT.efunc({po:91053, posId:910005});
                                break;
                            case 'weibo':
                                PASSPORT.efunc({po:91054, posId:910005});
                                break;
                            case 'weixin':
                                PASSPORT.efunc({po:91055, posId:910005});
                                break;
                            case 'eoe':
                                PASSPORT.efunc({po:91056, posId:910005});
                                break;
                        };
                    });

                    $(document).bind('keyup', function(e) {
                        if (e.keyCode == 13) {
                            $('#register-pop-submit').click();
                        }
                    });
                    if (fn) fn();
                    // ad
                    BAIDU_CLB_fillSlotAsync('1170455', 'reg-ad01');
                },
                callback: function() {
                    // 埋点
                    PASSPORT.efunc({po:91088, posId:910005});
                    if(window.hasSa) sa.track('reg_popup_leave');
                    
                }
            });
        };
        var loginPop = function(fn) {
            // 调用登录弹层请使用.diaLoginBtn, 不要使用其他 class 或 id
            $(this).passportPopup({
                popupId: 'login-popup',
                string: passportLoginhtml,
                zindex: 9999,
                fn: function() {
                    // 埋点
                    PASSPORT.efunc({posId:91095});
                    PASSPORT.getImgcode($('#login-popup .verifyCode'));
                    // placeholder
                    $('.passport-txt').passportPlaceholder('placeholder');
                    PASSPORT.tabs($('#login-tabs'), function(event) {
                        var val = event.attr('data-tab');
                        switch (val) {
                            case 'login':
                                PASSPORT.efunc({po: 91031, posId:91095});
                                break;
                            case 'fastlogin':
                                PASSPORT.efunc({po: 91028, posId:91095});
                                break;
                        }
                    });

                    // 刷新图片验证码
                    $('#login-popup .refreshCode, #login-popup .verifyCode').bind('click', function() {
                        PASSPORT.efunc({po:91029, posId:91095});
                        PASSPORT.getImgcode($('#login-popup .verifyCode'));
                    });
                    $('#login-popup .verifyCode').click();

                    // 获取动态码
                    $('#fastlogin-form-popup .js-getcode').bind('click', function() {
                        PASSPORT.efunc({po:91039, posId:91095});
                        if (self.lock) self.getMcode('#fastlogin-form-popup', {
                            restype: 5
                        });
                    });
                    $('#login-popup .forget-link').bind('click', function() {
                        PASSPORT.efunc({po:91030, posId:91095});
                    });
                    // 第三方登录埋点
                    $('#login-popup [data-pl]').bind('click', function() {
                        var $this = $(this);
                        var val = $this.attr('data-pl');
                        switch(val) {
                            case 'qq':
                                PASSPORT.efunc({po:91061, posId:91095});
                                break;
                            case 'weibo':
                                PASSPORT.efunc({po:91058, posId:91095});
                                break;
                            case 'weixin':
                                PASSPORT.efunc({po:91059, posId:91095});
                                break;
                            case 'eoe':
                                PASSPORT.efunc({po:91060, posId:91095});
                                break;
                        };
                    });
                    // 登录
                    self.login('#login-form-popup', '#login-pop-submit');
                    // 免注册登录
                    self.fastlogin('#fastlogin-form-popup', '#fastlogin-pop-submit');

                    $(document).bind('keyup', function(e) {
                        if (e.keyCode == 13) {
                            // 登录
                            if ($('#login-pop-submit').is(':visible')) $('#login-pop-submit').click();
                            // 免注册登录
                            if ($('#fastlogin-pop-submit').is(':visible')) $('#fastlogin-pop-submit').click();
                        }
                    });
                    if (fn) fn();
                },
                callback: function() {
                    // 埋点
                    PASSPORT.efunc({po:91089, posId:91095});
                }
            });
        }
        $('body').delegate('.diaRegBtn, .regnow, #regnow, #diaregBtn', 'click', function() {
            // PASSPORT.efunc({po:91032, posId: 91095});
            registerPop();
            return false;
        });
        $('body').delegate('.diaLoginBtn, .loginnow, #loginnow, #diaLoginBtn', 'click', function() {
            // PASSPORT.efunc({po:91040, posId: 910005});
            loginPop();
            return false;
        });
        $('body').delegate('.diaRegBtnTab', 'click', function() {
            PASSPORT.efunc({po:91032, posId: 91095});
            registerPop();
            return false;
        });
        $('body').delegate('.diaLoginBtnTab', 'click', function() {
            PASSPORT.efunc({po:91040, posId: 910005});
            loginPop();
            return false;
        });
        return {login: loginPop, register: registerPop};
    }
};

$(function() {
    SIGN.init();
})