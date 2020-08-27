;window.onload=function(){
    jQuery('#load-container').css({'left':(jQuery(window).width()-jQuery('#load-container').outerWidth())/2})
    var timer=setTimeout(function(){
        jQuery('.info').text('')
        clearTimeout(timer)
    },5000)
}

var add_comment=function(){
    jQuery('.comment-reply-link').off().on('click',function(){
        re_that=jQuery(this)
        jQuery(this).parent().parent().find('.comment-respond').slideToggle('fast')
        if (jQuery(this).text()==='REPLY'){
            jQuery(this).text('CANCEL')
        }else{
            jQuery(this).text('REPLY')
        }
        jQuery(this).parent().parent().find('.submit').off().on('click',function(){
            that = jQuery(this)
            if(that.parent().parent().find('.author').val().toUpperCase()==='BLOGGER'||that.parent().parent().find('.author').val()==='博主'){
                that.after('<p style="color:red;">Name不能使用“Blogger”和“博主”</p>')
                that.parent().parent().find('.author').val('')
                var timer=setTimeout(function(){
                    that.next().remove()
                    clearTimeout(timer)
                },5000)
            }
            if(jQuery(this).parent().parent().find('.author').val()!==''&&jQuery(this).parent().parent().find('.email').val()!==''&&jQuery(this).parent().parent().find('.comment').val()!==''){
                jQuery('#load-container').css({'left':(jQuery(window).width()-jQuery('#load-container').outerWidth())/2})
                jQuery('.load-item').show()
                $.ajax({
                    url:'/comment/',
                    type:'POST',
                    data:{
                        id:that.parent().find('.comment_ID').val(),
                        author:that.parent().parent().find('.author').val(),
                        email:that.parent().parent().find('.email').val(),
                        comment:that.parent().parent().find('.comment').val(),
                        csrfmiddlewaretoken:that.parent().parent().find('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success:function(data,status){
                        if(status==='success'){
                            var html='<div class="commentlist-item">'+
                                        '<div class="comment even thread-even depth-1" id="comment-'+data.comment_num+'">'+
                                            '<div class="avatar-holder">'+
                                                '<strong class="text"><span class="icon ico-user"></span></strong>'+
                                            '</div>'+
                                            '<div class="commentlist-holder">'+
                                                '<p class="meta">'+
                                                    '<strong class="name">'+data.author+'</strong>'+
                                                    '<time datetime="'+data.date+'">'+data.time+'</time>'+
                                                '</p>'+
                                                '<p>'+data.content+'</p>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>';
                            that.parent().parent().parent().slideToggle('fast')
                            that.parent().parent().find('.author').val('')
                            that.parent().parent().find('.email').val('')
                            that.parent().parent().find('.comment').val('')
                            that.parent().parent().parent().parent().parent().after(html)
                            jQuery('#comment-number').text(data.comment_num+' comments')
                            jQuery('.comment-count a').last().text(data.comment_num+' comments')
                            jQuery('.load-item').hide()
                            jQuery('.info').text(data.result)
                            var timer=setTimeout(function(){
                                jQuery('.info').text('')
                                clearTimeout(timer)
                            },5000)
                            if (re_that.text()==='REPLY'){
                                re_that.text('CANCEL')
                            }else{
                                re_that.text('REPLY')
                            }
                        }else{
                            jQuery('.load-item').hide()
                            jQuery('.info').text('评论失败,请重试')
                            var timer=setTimeout(function(){
                                jQuery('.info').text('')
                                clearTimeout(timer)
                            },5000)
                        }
                    }
                })
            }
        })
    })
}
add_comment()

response=jQuery('#comment-response')
response.find('#submit').off().on('click',function(){
    if(response.find('.author').val().toUpperCase()==='BLOGGER'||response.find('.author').val()==='博主'){
        response.find('#submit').after('<p style="color:red;">Name不能使用“Blogger”和“博主”</p>')
        response.find('.author').val('')
        var timer=setTimeout(function(){
            response.find('#submit').next().remove()
            clearTimeout(timer)
        },5000)
    }
    if(response.find('.author').val()!==''&&response.find('.email').val()!==''&&response.find('.comment').val()!==''){
        jQuery('#load-container').css({'left':(jQuery(window).width()-jQuery('#load-container').outerWidth())/2})
        jQuery('.load-item').show()
        $.ajax({
            url:'/comment/post/',
            type:'POST',
            data:{
                id:response.find('.post_ID').val(),
                author:response.find('.author').val(),
                email:response.find('.email').val(),
                comment:response.find('.comment').val(),
                csrfmiddlewaretoken:response.find('input[name="csrfmiddlewaretoken"]').val()
            },
            success:function(data,status){
                if(status==='success'){
                    var html='<div class="commentlist-item">'+
                                '<div class="comment even thread-even depth-1" id="comment-'+data.comment_num+'">'+
                                    '<div class="avatar-holder">'+
                                        '<strong class="text"><span class="icon ico-user"></span></strong>'+
                                    '</div>'+
                                    '<div class="commentlist-holder">'+
                                        '<p class="meta">'+
                                            '<strong class="name">'+data.author+'</strong>'+
                                            '<time datetime="'+data.date+'">'+data.time+'</time>'+
                                        '</p>'+
                                        '<p>'+data.content+'</p>'+
                                        '<p><a class="comment-reply-link" style="cursor:pointer;">REPLY</a></p>'+
                                        '<section class="comment-respond" style="display:none;">'+
                                            '<form action="javascript:;" method="post" class="comment-form">'+
                                                '<input type="hidden" name="csrfmiddlewaretoken" value="'+response.find('input[name="csrfmiddlewaretoken"]').val()+'"></input>'+
                                                '<div class="wrap">'+
                                                    '<div class="comment-form-author">'+
                                                        '<label for="author">Your name <span class="required">*</span></label>'+
                                                        '<input type="text" class="author" name="author" size="30" required placeholder="enter your name here">'+
                                                    '</div>'+
                                                    '<div class="comment-form-email">'+
                                                        '<label for="email">Email address <span class="required">*</span></label>'+
                                                        '<input type="text" class="email" name="email" size="30" required placeholder="enter your email address">'+
                                                    '</div>'+
                                                '</div>'+
                                                '<div class="comment-form-comment">'+
                                                    '<label for="comment">Comment <span class="required">*</span></label>'+
                                                    '<textarea class="comment" name="comment" rows="3" cols="72" required placeholder="your comment here"></textarea>'+
                                                '</div>'+
                                                '<div class="form-submit">'+
                                                    '<input type="submit" name="submit" class="submit" value="Reply">'+
                                                    '<input type="hidden" name="comment_ID" value="'+data.comment_id+'" class="comment_ID">'+
                                                '</div>'+
                                            '</form>'+
                                        '</section>'+
                                    '</div>'+
                                '</div>'+
                            '</div>';
                    response.find('.author').val('')
                    response.find('.email').val('')
                    response.find('.comment').val('')
                    jQuery('.commentlist').append(html)
                    jQuery('#comment-number').text(data.comment_num+' comments')
                    jQuery('.comment-count a').last().text(data.comment_num+' comments')
                    add_comment()
                    jQuery('.load-item').hide()
                    response.find('#submit').blur()
                    jQuery('.info').text(data.result)
                    var timer=setTimeout(function(){
                        jQuery('.info').text('')
                        clearTimeout(timer)
                    },5000)
                }else{
                    jQuery('.load-item').hide()
                    response.find('#submit').blur()
                    jQuery('.info').text('评论出错，请重试')
                    var timer=setTimeout(function(){
                        jQuery('.info').text('')
                        clearTimeout(timer)
                    },5000)
                }
            }
        })
    }
})

jQuery('.subscribe-form').find('.ico-send').off().on('click',function(){
    that=jQuery('.subscribe-form')
    if(that.find('.form-control').val()!==''){
        jQuery('#load-container').css({'left':(jQuery(window).width()-jQuery('#load-container').outerWidth())/2})
        jQuery('.load-item').show()
        $.ajax({
            url:'/subscribe/',
            type:'POST',
            data:{
                email:that.find('.form-control').val(),
                csrfmiddlewaretoken:that.find('input[name="csrfmiddlewaretoken"]').val()
            },
            success:function(data,status){
                if(status==='success'){
                    jQuery('.load-item').hide()
                    jQuery('.subscribe-form').find('.ico-send').blur()
                    jQuery('.info').text(data.result)
                    that.find('.form-control').val('')
                    var timer=setTimeout(function(){
                        jQuery('.info').text('')
                        clearTimeout(timer)
                    },5000)
                }else{
                    jQuery('.load-item').hide()
                    jQuery('.subscribe-form').find('.ico-send').blur()
                    jQuery('.info').text('订阅出错，请稍后重试')
                    var timer=setTimeout(function(){
                        jQuery('.info').text('')
                        clearTimeout(timer)
                    },5000)
                }
            }
        })
    }
})

jQuery('.ico-search').off().on('click',function(){
    jQuery('#load-container').css({'left':(jQuery(window).width()-jQuery('#load-container').outerWidth())/2})
    jQuery('.load-item').show()
})






// page init
jQuery(function(){
	"use strict";

	initIsoTop();
	initTabs();
	initFitVid();
	initbackTop();
	initLightbox();
	initAddClass();
	initCountDown();
	initHoverClass();
	new WOW().init();
	initSlickSlider();
//	initStyleChanger();
	initStickyHeader();
});
jQuery(window).on('load', function() {
	"use strict";

	initIsoTop();
});

function initHoverClass() {
	jQuery('.blocks-slider .slide').on( "mouseover", function(){
		if (jQuery(this).siblings().hasClass("active")) {
			jQuery(this).siblings().removeClass('active');
			jQuery(this).addClass("active");
		}else{
			jQuery(this).addClass("active");
		}
	});
}

function initFitVid() {
	jQuery(".videobox").fitVids();
}
// count down init
function initCountDown() {
	var newDate = new Date(2016, 12, 28);
	
	jQuery("#defaultCountdown").countdown({until: newDate});
}



jQuery(window).load(function() {
	jQuery(".loader-holder").hide();
});

function initAddClass() {
	jQuery(".icon-menu, .close").click(function(event) {
		event.preventDefault();
		jQuery("body").toggleClass("sidenav-active");
	});
}

function initSlickSlider() {
	jQuery('.image-slider').slick({
		dots: false,
		autoplay: true,
		arrows: true,
		adaptiveHeight: true
	});
	jQuery('.carousel').slick({
		dots: false,
		autoplay: true,
		arrows: true,
		adaptiveHeight: true
	});
	jQuery('.instagram-slider .mask .slideset').slick({
		dots: false,
		arrows: false,
		autoplay: true,
		slidesToShow: 7,
		responsive: [
			{
				breakpoint: 991,
				settings: {slidesToShow: 5}
			},
			{
				breakpoint: 600,
				settings: {slidesToShow: 3}
			}
		]
	});
	jQuery('.center-slider').slick({
		centerMode: true,
		centerPadding: '0',
		slidesToShow: 3,
		speed: 400,
		adaptiveHeight: true,
		responsive: [
			{
				breakpoint: 767,
				settings: {
					centerMode: true,
					centerPadding: '0',
					adaptiveHeight: false,
					slidesToShow: 1
				}
			}
		]
	}); 
	jQuery('.slideshow').slick({
		fade: true,
		speed: 900,
		dots: false,
		arrows: false,
		infinite: true,
		asNavFor: '.switcher .switcher-mask'
	}); 
	jQuery('.switcher .switcher-mask').slick({
		dots: false,
		slidesToShow: 4,
		slidesToScroll: 1,
		asNavFor: '.slideshow',
		focusOnSelect: true,
		responsive: [
			{
				breakpoint: 1199,
				settings: {slidesToShow: 3}
			},
			{
				breakpoint: 991,
				settings: {slidesToShow: 2}
			},
			{
				breakpoint: 767,
				settings: {slidesToShow: 1}
			}
		]
	});
}

// fancybox modal popup init
function initLightbox() {
	jQuery('a.lightbox, a[rel*="lightbox"]').fancybox({
		padding: 0,
		loop: false,
		helpers: {
			overlay: {
				css: {background: 'rgba(0, 0, 0, 0.35)'}
			}
		},
		afterLoad: function(current, previous) {
			// handle custom close button in inline modal
			if(current.href.indexOf('#') === 0) {
				jQuery(current.href).find('a.close').off('click.fb').on('click.fb', function(e){
					e.preventDefault();
					jQuery.fancybox.close();
				});
			}
		}
	});
}
// content tabs init
function initTabs() {
	jQuery('header.tab-head').tabset({
		tabLinks: 'a',
		defaultTab: false
	});
}

// IsoTop init
function initIsoTop() {
	// Isotope init
	var isotopeHolder = jQuery('#masonry-container'),
		win = jQuery(window);
	jQuery('#masonry-container').isotope({
		itemSelector: '.block',
		transitionDuration: '0.6s'
	});
}

// sticky header init
function initbackTop() {
	var jQuerybackToTop = jQuery("#back-top");
	jQuery(window).on('scroll', function() {
		if (jQuery(this).scrollTop() > 100) {
			jQuerybackToTop.addClass('active');
		} else {
			jQuerybackToTop.removeClass('active');
		}
	});
	jQuerybackToTop.on('click', function(e) {
		jQuery("html, body").animate({scrollTop: 0}, 500);
	});
}


// sticky header init
function initStickyHeader() {
	var win = jQuery(window),
		stickyClass = 'sticky',
		stickyTop = jQuery('#header').offset().top +200;
	

	jQuery(window).on( 'scroll', function(){
		if (jQuery(window).scrollTop() >= stickyTop) {
			jQuery('#header').addClass('movetop');
		} else {
			jQuery('#header').removeClass('movetop');
		}
	});

	jQuery('#header').css({'height': jQuery('#header').innerHeight()});
	jQuery(window).resize( function(){
		jQuery('#header').css({'height': jQuery('#header').innerHeight()});
		jQuery('#load-container').css({'left':(jQuery(window).width()-jQuery('#load-container').outerWidth())/2})
	});

	jQuery('#header').each(function() {
		var header = jQuery(this);
		var headerOffset = header.offset().top +400 || 0;
		var flag = true;

		function scrollHandler() {
			if (win.scrollTop() > headerOffset) {
				if (flag){
					flag = false;
					header.addClass(stickyClass);
				}
			} else {
				if (!flag) {
					flag = true;
					header.removeClass(stickyClass);
				}
			}

			ResponsiveHelper.addRange({
				'..767': {
					on: function() {
						header.removeClass(stickyClass);
					}
				}
			});
		}

		scrollHandler();
		win.on('scroll resize orientationchange', scrollHandler);
	});
}
