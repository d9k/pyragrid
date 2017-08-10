/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
$(document).ready(function() {
//    window.ajaxLinksDebugMode = true

    const debugMode = () => window.hasOwnProperty('ajaxLinksDebugMode') && window.ajaxLinksDebugMode;

    const trace = function(s) {
        if (debugMode()) { return console.log(s); }
    };

    trace("bind ajax click events");

//    http://stackoverflow.com/a/728694/1760643
    const cloneObject = function(obj) {
        if ((null === obj) || ("object" !== typeof obj)) {
            return obj;
        }
        const copy = obj.constructor();
        for (let attr in obj) {
            if (obj.hasOwnProperty(attr)) {
                copy[attr] = obj[attr];
            }
        }
        return copy;
    };

    const addToHistory = function(state) {
        trace("add to history");
        if (!!history) {
            history.pushState(state, null, state['url']);
            if (state['returnedUrl'] !== ['url']) {
                const stateRedirected = cloneObject(state);
                stateRedirected['url'] = stateRedirected['returnedUrl'];
                stateRedirected['data'] = '';
                // emulate redirection:
                // TODO check
                return setTimeout((() => history.pushState(state, null, stateRedirected['url'])), 300);
            }
        }
    };

    const domainFromUrl = function(url) {
        if ((url == null)) {
            return null;
        }
        const a = document.createElement('a');
        a.href = url;
        return a.hostname;
    };

    const urlOnThisDomain = function(url) {
        const this_domain = domainFromUrl(window.location.href);
        const url_domain = domainFromUrl(url);
        return this_domain === url_domain;
    };

    const hasDisableAjaxAttr = $el => typeof $el.attr('data-no-ajax-on-click') !== 'undefined';

    const noOptimise = variable => variable;

    addToHistory({url: window.location.href, requestType: 'GET', data: ''});

    const ajaxUpdateContent = function(url, type, data, _addToHistory){
//        _getXhr = jQuery.ajaxSettings.xhr;

        //see http://stackoverflow.com/a/26750780/1760643
//        $.ajaxSettings.xhr = () ->
//          xhr = _getXhr()
//          return xhr

        if (type == null) { type = "GET"; }
        if (data == null) { data = ''; }
        if (_addToHistory == null) { _addToHistory = true; }
        let rawXHR = null;

        return $.ajax({
            url,
            type,
            data,
            xhr() {
                const xhr = jQuery.ajaxSettings.xhr();
                rawXHR = xhr;
                return xhr;
            },
            success(success_data, textStatus, request) {
                trace("ajax link success request");
                $('#content').html(success_data);
                if (_addToHistory) {
                    return addToHistory({
                        url,
                        requestType: type,
                        data,
                        returnedUrl: rawXHR.responseURL
                    });
                }
            },
            error(error_data, textStatus, errorThrown) {
                trace("ajax link error request");
                return UI.notifyFromErrorData(error_data);
            }
        });
    };

    if (!window.hasOwnProperty('popstateBinded')) {
        window.addEventListener('popstate', function(e) {
            trace("back in history");
            const state = $.extend({'requestType': 'GET', 'returnedUrl': '', 'data': ''}, e.state);
            const url = state['url'];
            const requestType = state['requestType'];
            const post = (state['requestType'] !== 'GET');
            const data = state['data'];
            if (!url) {
                return;
            }
            if (post && !confirm('Провести повторную отправку формы?')) {
                return;
            }

            return ajaxUpdateContent(url, requestType, data, false);
        });
        trace('popstate binded');
    }
    window.popstateBinded = true;

// TODO check before event attach, maybe selector "href starts with"
    $('body').on('click', 'a', function(e) {
        trace("ajax link clicked");
        const $this = $(this);
        const url = $this.attr('href');
        if (hasDisableAjaxAttr($this)) {
            return;
        }
        if (urlOnThisDomain(url)) {
            e.preventDefault();
            return ajaxUpdateContent(url);
        }
    });

    return $('body').on('click', 'form button[type=submit]', function(e) {
        const $this = $(this);
        const $form = $(this).closest('form');
        trace("ajax button pressed");
        let url = $form.attr('action');
        if (!url) {
            url = window.location.href;
        }
        if (hasDisableAjaxAttr($this)
        || hasDisableAjaxAttr($form)) {
            return;
        }
        if (urlOnThisDomain(url)) {
            const formEvents = $._data($form.get(0), "events");
            if (formEvents.submit != null) {
                $.each(formEvents.submit, (j, h) =>
                    //TODO fill event object and pass to handler?
//                    console.log(h.handler)
                    h.handler()
                );
            }
            let formData = $form.serialize();
            formData += `&${this.name}=${this.value}`;
            e.preventDefault();
            return ajaxUpdateContent(url, "POST", formData);
        }
     });
});

// TODO  stop event propagating?