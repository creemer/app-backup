/* customview.js */

require.config({
    paths: {
        // jQuery and contrib plugins
        'jquery': 'contrib/jquery-2.1.0',
        'jquery.fileupload': 'contrib/jquery.fileupload',
        'jquery.iframe-transport': 'contrib/jquery.iframe-transport',

        // jQuery UI plugins
        'jquery.ui.core': 'contrib/jquery-ui-1.10.4/jquery.ui.core',
        'jquery.ui.widget': 'contrib/jquery-ui-1.10.4/jquery.ui.widget'
    },
    shim: {
        'jquery.fileupload': {
            deps: ['jquery']
        },
        'jquery.iframe-transport': {
            deps: ['jquery']
        },
        'jquery.ui.core': {
            deps: ['jquery']
        },
        'jquery.ui.widget': {
            deps: ['jquery.ui.core']
        }
    }
});

require([
    "jquery",
    "underscore",
    "backbone",
    "splunkjs/mvc",
    "splunkjs/mvc/searchmanager",
    "splunkjs/mvc/checkboxview",

    "util/splunkd_utils",

    "splunkjs/splunk",
    "/static/app/api_app/bluebird.js",

    "jquery.ui.widget",
    "jquery.iframe-transport",
    "jquery.fileupload",

    "splunkjs/mvc/simplexml/ready!"
], function(
    $,
    _,
    Backbone,
    mvc,
    SearchManager,
    CheckboxView,
    utilsA,
    customSplunk,
    Promise
) {
    console.log('Begin!!!!');
    var make_request = function(params) {
        var customUrl = Splunk.util.make_full_url('/custom/api_app/api_controller/' + params.method);
        console.log('customUrl:' +  customUrl);
        var options = {
            type: params.type || 'POST', //TODO Уточнить, почему GET не работает
            url: customUrl,
            async: false,
            data: params.data || {}
        };

        return new Promise(function(resolve, reject) {
            $.ajax(options)
                .done(function(answ, status) {
                    console.log('\nINFO_make_request_0', answ, status);
                    resolve(answ);
                })
                .fail(function(err) {
                    console.log('Error_make_request_0', options, err);
                    reject(err);
                });
        });
    };

    var APIs = {
        get_zipped_app: function() {
            console.log('Info_get_zipped_app_0');
            return make_request({
                method: 'get_zipped_app'
            });
        },
        get_apps_list: function(isTest) {
            console.log('Info_get_apps_list_0_0');
            return make_request({
                method: 'get_apps_list'
            });
        },
        deploy_app: function(data) {
            console.log('Info_deploy_app_0_0');
            return make_request({
                method: 'deploy_app',
                data
            });
        }
    };

    var templates = {};
    var fetchTemplate = function(name) {
        console.log('Template name: ', name);
        if (templates[name]) {
            return Promise.resolve(templates[name]);
        }

        return new Promise(function(resolve, reject) {
            $.get('/static/app/api_app/templates/' + name + '.tpl')
                .done(function(contents) {
                    var tmpl = _.template(contents);
                    templates[name] = tmpl;
                    // console.log('----------------------------------');
                    // console.log('contents: ', contents);
                    // console.log('----------------------------------');
                    resolve(tmpl);
                })
                .fail(function(err) {
                    console.log('Error_fetchTemplate_0', err);
                    reject(err);
                });
        });
    };

    APIs.get_apps_list(true)
        .then(function(appsInfos) {
            console.log('appsInfos: ', appsInfos);
            var appListColl = new AppListColl(appsInfos);
            console.log('appListColl: ', appListColl.toJSON());

            var appView = new AppListView({
                model: appListColl
            });

            appView.render();
        })
        .catch(function(err) {
            console.log('Error_get-apps_0', err);
        });

    var MenuView = Backbone.View.extend({
        el: '#menu-wrapper',
        template: 'Menu',
        events: {
            "click li": "changeTab"
        },
        hideAllTabs: function() {
            this.$el
                .find("li")
                .each(function(idx, el) {
                    console.log('El: ' + el + ' idx: ' + idx);
                    var val = $(el).data('tab');
                    console.log('Before hidding tab: ' + val);
                    $('#' + val).hide();
                });
        },
        changeTab: function(e) {
            e.stopPropagation();

            var curEl = $(e.currentTarget);
            var tab2Show = curEl.data('tab');

            console.log('Tab was clicked: ' + curEl + ' ' + tab2Show);

            this.$el.find('li').removeClass('active');
            curEl.addClass('active');

            this.hideAllTabs();
            $('#' + tab2Show).show();

        },
        render: function() {
            var self = this;
            return fetchTemplate(this.template)
                .then(function(tpl) {
                    var compiledForm = tpl({});

                    self.$el.html(compiledForm);

                    return true;
                })
                .catch(function(err) {
                    console.log('Error_get-apps_0', err);
                });
        }
    });

    var menuView = new MenuView({
        model: {}
    });

    menuView.render();

    var AppModel = Backbone.Model.extend({});
    var AppListColl = Backbone.Collection.extend({
        model: AppModel
    });

    var AppListView = Backbone.View.extend({
        template: 'ChooseApp',
        url: Splunk.util.make_full_url('/custom/api_app/api_controller/get_zipped_app'),
        el: '#choose-form-place',
        events: {
            //'click #get-archive-app': 'downloadZip',
            'click .single-app': 'changeLinkHref'
        },
        changeLinkHref: function(event) {
        	var curAppNum = $(event.currentTarget).data('idx');
            console.log('curAppNum: ', curAppNum);
        	var name = this.model.at(curAppNum).get('id');
            console.log('name : ', name);

        	var mainLink = $(this.$el).find("#get-archive-app");
            mainLink.prop('href', this.url + '/?appname=' + name);
            mainLink[0].click();
        },
        render: function() {
            var self = this;
            return fetchTemplate(this.template)
                .then(function(tpl) {
                    var compiledForm = tpl({
                    	url: self.url,
                        appsInfo: self.model
                    });

                    self.$el.html(compiledForm);

                    return true;
                })
                .catch(function(err) {
                    console.log('Error_get-apps_0', err);
                });
        }
    });

    var LoadModel = Backbone.Model.extend({});
    var LoadView = Backbone.View.extend({
        template: 'UploadApp',
        url: Splunk.util.make_full_url('/custom/api_app/api_controller/load_old/?archive_name='),
        el: '#add-new-app',
        loadUrl: Splunk.util.make_full_url('/custom/api_app/api_controller/load_app'),
        events: {
            'click #deploy-btn': 'deployArch',
            'click #upload-handler': 'toggleUpload',
            'change #dist-select' : 'toggleDist'
        },
        initialize: function() {
            let distVariants = [{
                name: 'Deployment server',
                val: 'deployment'
            }, {
                name: 'Deployer',
                val: 'search'
            }];

            this.model.set('distVariants', distVariants);
            this.model.set('dist', distVariants[0].val);
        },
        toggleDist: function() {
            var newVal = this.$el.find('#dist-select').val();
            this.model.set('dist', newVal);
        },
        toggleUpload: function() {
            this.$el.find('#fileupload').click();
        },
        deployArch: function() {
            var self = this;
            var archive_name = this.model.get('archive_name');
            var dist = this.model.get('dist');
            if(!archive_name) {
                this.showPopup('Ошибка!<br/>Выберите приложение');
                return;
            }

            APIs.deploy_app({
                dist,
                archive_name
            })
                .then(function(data) {
                    console.log('data: ', JSON.stringify(data, null, 4));
                    if(data.res === 'ok'){
                        self.model.unset('archive_name');
                        self.$el.find('#progress .bar').css(
                            'width',
                            0 + '%'
                        );
                        let popupText = 'Приложение установлено';
                        if(data.oldAppName){
                            let url = self.url + data.oldAppName;
                            popupText += `<br/><br/><a href='${url}'>Скачать старую версию</a>`;
                        }

                        self.showPopup(popupText);
                    }
                    else {
                        self.showPopup(`Error<br/>${data.descr}`);
                    }
                })
                .catch(function(err) {
                    console.log('Error_deployArch_0', err);
                    self.showPopup(`Error<br/>${err}`);
                });

            document.getElementById('file-name').innerText = '';
        },
        showPopup: function(text) {
            var popupModel = new PopupModel({
                text: text
            });
            popupView = new PopupView({
                model: popupModel
            });
            popupView.render();
        },
        render: function() {
            var self = this;
            return fetchTemplate(this.template)
                .then(function(tpl) {
                    var compiledForm = tpl({
                        url: self.loadUrl,
                        linkData: self.model.get('distVariants')
                    });

                    self.$el.html(compiledForm);
                    self.$el.find('#fileupload').fileupload({
                        process_request_body: true,
                        type: 'POST',
                        progressall: function (e, data) {
                            var progress = parseInt(data.loaded / data.total * 100, 10);
                            self.$el.find('#progress .bar').css(
                                'width',
                                progress + '%'
                            );
                        },
                        dataType: 'json',
                        done: function (e, data) {
                            var response = data._response.result;
                            if(response.res === 'ok'){
	                            document.getElementById('file-name').innerText = response.archive_name;                            		

                            	console.log(response.archive_name);
                                self.model.set('archive_name', response.archive_name);
                            }
                            else{
                                self.showPopup('Ошибка');
                            }
                            
                        }
                    });


                    return true;
                })
                .catch(function(err) {
                    console.log('Error_get-apps_0', err);
                });
        }
    });

    var appView = new LoadView({
        model: new LoadModel({})
    });

    appView.render();

    var PopupModel = Backbone.Model.extend({});

    var PopupView = Backbone.View.extend({
        template: 'Popup',
        el: 'body',
        events: {
            "click .overlay": "removePopup"
        },
        removePopup: function() {
            this.$el.find('.overlay').remove();
            //this.remove();
        },
        render: function() {
            var self = this;
            return fetchTemplate(this.template)
                .then(function(tpl) {
                    var compiledForm = tpl({
                        text: self.model.get('text')
                    });

                    self.$el.append(compiledForm);
                    return true;
                })
                .catch(function(err) {
                    console.log('Error_get-apps_0', err);
                });
        }
    });
});