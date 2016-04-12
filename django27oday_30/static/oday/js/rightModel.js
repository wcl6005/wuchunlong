$(function() {
	$('.help-guide a').click(function () {
		$(this).popupshow({
			popupId: 'video-pop',
			zindex: 1000,
			width: 760,
			height: 420,
		});
	});
});