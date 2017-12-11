require([
         "jquery",
         "underscore",
         "backbone",
		 "splunkjs/mvc",
		 "splunkjs/mvc/utils",
         "splunkjs/mvc/simplexml/ready!"
     ], function(
         $,
         _,
         Backbone,
		 mvc,
		 utils
     )
     {
	console.log('The beginning of dashboard.js');

	var prefix = Splunk.util.make_url();

	$('head').append('<link id="link-new-theme" rel="stylesheet" type="text/css">');

	var oldInterval = null;

	//Change themes script
	function changeTheme(value, changeCookie) {
		var themeCss = '';
		if(value !== 'common' && value !== 'default'){
			themeCss = prefix + '/static/app/' + utils.getCurrentApp() + '/css/' + value + '.css';
		}

		if(value === 'default' && defaultVal) {
			themeCss = prefix + '/static/app/' + utils.getCurrentApp() + '/css/' + defaultVal + '.css';
		}

		$('#link-new-theme').attr('href', themeCss);
		changeCookie && $.cookie('theme-color', value, {
			path: '/'
		});

		function changeSvg() {
			if (value === 'dark') {
				$('.row-green-bar[fill=#F5F5F5]').attr('fill', '#444');
				$('.row-green-bar[fill=white]').attr('fill', '#888');
				$('.splunk-timeline text').attr('fill', '#ccc');
			}
			else {
				$('.row-green-bar[fill=#444]').attr('fill', '#F5F5F5');
				$('.row-green-bar[fill=#888]').attr('fill', 'white');
				$('.splunk-timeline text').attr('fill', '#555');
			}
		}

		changeSvg();

		oldInterval && clearInterval(oldInterval);

		oldInterval = setInterval(function() {
			changeSvg();
		}, 5000);

		//Set cookie for continous using
	}

	var submittedTokenModel = mvc.Components.getInstance('submitted', {create: true});
	var tokenName = 'theme-change';

	console.log('prefix: ', prefix);

	//Initial changing of theme colour
	var tokenVal = submittedTokenModel.get(tokenName);
	var cookieVal = $.cookie('theme-color') || tokenVal;// || 'dark';
	console.log('tokenVal: ', tokenVal);
	console.log('cookieVal: ', cookieVal);

	if(tokenVal === 'default' && cookieVal !== tokenVal) {
		var defaultVal = cookieVal;
	}

	//cookieVal is more important
	changeTheme(cookieVal, true);

	if(tokenVal) {
		if(tokenVal !== cookieVal) {
			console.log('Need to set token val');
			submittedTokenModel.set(tokenName, cookieVal);
		}

		submittedTokenModel.on('change:' + tokenName, function(model, value, options) {
			console.log('New theme name: ' + value);
			changeTheme(value, true);
		});
	}
	//----------------------

	// Find the Javascript blocks and run them
	$.each($('div.javascript'), function( index, value ) {
		eval(value.innerText);
	});
     }
);
