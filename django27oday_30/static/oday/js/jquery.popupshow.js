/* -----------------------------------------/
 * 功能：弹出层显示及居中显示
 * 参数：
 * 返回：
 * 作者：ZhangHaiBin
/ ---------------------------------------- */

(function($) {
    $.fn.popupshow = function(options) {
        var settings = $.extend({
            'popupId': null, // 弹出层id
            'url': null, // 要插入的HTML的URL, 如果弹层隐藏在页面中, 则不用设置
            'maskId': 'mask', // 遮罩id,null不显示遮罩
            'position': 'fixed', // 定位类别(参数fixed和absolute)
            'zindex': null, // z-index值
            'width': null,  // 宽度
            'height': null, // 高度
            'countdown': null,   // 倒计时关闭(正整数,以秒为单位)
            'timer': null,   // 倒计时输出位置
            'jump': null,    // 关闭时跳转URL
            'fn': null, // 弹出调用函数
            'callback': null // 关闭回调
        }, options);

        	// 如果popupId不存在, 则返回
        	if (!settings.popupId) return false;
        // 重命名参数名称
        var _popupId = settings.popupId,
            _url = settings.url,
            _maskId = settings.maskId,
            _position = settings.position,
            _zindex = settings.zindex,
            _width = settings.width,
            _height = settings.height,
            _countdown = settings.countdown,
            _timer = settings.timer,
            _jump = settings.jump;

        var $popup = $("#" + _popupId);
        // 倒计时节点
        var $countdown = $('<div class="countdownTxt">');

        //弹出层显示
        if ($popup.length > 0) {
            // 如果弹层已弹出, 则返回
            if ($popup.is(':visible')) return;
            // 关闭已弹出弹层
            closeActive();
            //判断是否启用遮罩
            if (_maskId !== null) mask();
            // 显示自有弹层并添加属性
            $popup.attr({popup: "show", popmark: "own"}).show();
            // 设置宽高
            if (_width !== null) {
                $popup.css("width", _width + 'px');
            }
            if (_height !== null) {
                $popup.css("height", _height + 'px');
            }
            // 设置zIndex值
            if (_zindex !== null) {
                $popup.css({zIndex: _zindex});
            }
            // 弹层定位
            popupPsotion(_popupId, _position);
            //关闭弹层
            $("#" + _popupId + " .close").bind('click', function() {
                close($(this));
                $("#" + _maskId).hide();
                // location.reload();
            });
            // 弹出回调
            if (settings.fn !== null) settings.fn();
            // 倒计时关闭
            if (_countdown !== null) {
                // 参数类型判断
                if (typeof _countdown == 'number' && _countdown > 0) {
                    countdown(_countdown, _timer, _jump);
                } else {
                    throw new TypeError();
                }
            }
        } else if (_url !== null) {
            $.ajax({
                	type: "GET",
                	url: _url,
                	success: function(res) {
                    // 如果弹层已弹出, 则返回
                    if ($('body').find("#" + _popupId).length) return;
                    // 关闭已弹出弹层
                    closeActive();
                    //判断是否启用遮罩
                    if (_maskId !== null) mask();
                    // 插入弹层
                    $('body').append(res);

                    var $popup = $("#" + _popupId);
                    // 添加属性
                    $popup.attr("popup", "show");
                    // 设置宽高
                    if (_width !== null) {
                        $popup.css("width", _width + 'px');
                    }
                    if (_height !== null) {
                        $popup.css("height", _height + 'px');
                    }
                    // 设置zIndex值
                    if (_zindex !== null) {
                        $popup.css({zIndex: _zindex});
                    }
                    // 弹层定位
                    popupPsotion(_popupId, _position);
                    //关闭弹层
                    $("#" + _popupId + " .close").bind('click', function() {
                        close($(this));
                        $("#" + _maskId).hide();
                    });
                    // 弹出回调
                    if (settings.fn !== null) settings.fn();
                    // 倒计时关闭
                    if (_countdown !== null) {
                        // 参数类型判断
                        if (typeof _countdown == 'number' && _countdown > 0) {
                            countdown(_countdown, _timer, _jump);
                        } else {
                            throw new TypeError();
                        }
                    }
                	}
            });
        } else {
            return false;
        }

        //遮罩
        function mask() {
            var $mask = $("#" + _maskId);
            if ($mask.length > 0) {
                // 如果遮罩以显示, 则返回
                if ($mask.is(":visible")) return;
                $mask.show();
            } else {
                var maskNode = $("<div class='mask' id='" + _maskId + "'>");
                $('body').append(maskNode);
            }
        }
        // 关闭已弹出弹层
        function closeActive() {
            $('body').find('[popup="show"]').attr("popup","hide").find('.close').click();
        }
        // 倒计时关闭
        function countdown(time, node, url) {
            // 参数说明:
            // 1. time是设定的倒计时时间;
            // 2. node是自定义显示倒计时的位置;
            // 3. url是倒计时结束时跳转的url

            var _time = Math.ceil(time) - 1;
            var _popup = $("#" + _popupId);
            if (_time <= 0) return;
            // 如果自定义了时间显示节点名, 则在指定位置显示倒计时
            if (node !== null) {
                _popup.find(node).text(_time + "秒");
            } else {
                _popup.find("." + $countdown[0].className).remove();
                _popup.children('.wrap').append($countdown).find($countdown).text(_time + "秒");
            }
            // 清除倒计时
            window.clearTimeout(this._t);
            this._t = window.setTimeout(function() {
                _time--;
                if (_time > 0) {
                    // 如果自定义了时间显示节点名, 则在指定位置显示倒计时
                    if (node !== null) {
                        _popup.find(node).text(_time + "秒");
                    } else {
                        _popup.children('.wrap').append($countdown).find($countdown).text(_time + "秒");
                    }
                   return countdown(time - 1, node, url);
                } else {
                    $("#" + _popupId + " .close").click();
                    if (url !== null) {
                        document.location = url;
                        window.clearTimeout(this._t);
                    }
                }
            }, 1000);
        }
        //关闭按钮
        function close(obj) {
            // 清除倒计时
            window.clearTimeout(this._t);
            // 关闭回调
            if (settings.callback !== null) settings.callback();
            if (_jump !== null) {
                document.location = _jump;
            }
            var _popup = obj.parents("#" + _popupId);
            var _mark = _popup.attr("popmark");
            // 设置弹层属性
            _popup.attr("popup", "hide");
            // 如果popmark属性为own则隐藏，否则删除
            if (_mark == "own") {
                _popup.hide();
            } else {
                _popup.remove();
            }
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
        // 窗口调整是重新定位
        $(window).resize(function() {
            popupPsotion(_popupId, _position);
        });
    };
})(jQuery);
