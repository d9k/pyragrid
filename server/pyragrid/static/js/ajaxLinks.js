"use strict";

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
$(document).ready(function () {
    //    window.ajaxLinksDebugMode = true

    var debugMode = function debugMode() {
        return window.hasOwnProperty('ajaxLinksDebugMode') && window.ajaxLinksDebugMode;
    };

    var trace = function trace(s) {
        if (debugMode()) {
            return console.log(s);
        }
    };

    trace("bind ajax click events");

    //    http://stackoverflow.com/a/728694/1760643
    var cloneObject = function cloneObject(obj) {
        if (null === obj || "object" !== (typeof obj === "undefined" ? "undefined" : _typeof(obj))) {
            return obj;
        }
        var copy = obj.constructor();
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) {
                copy[attr] = obj[attr];
            }
        }
        return copy;
    };

    var addToHistory = function addToHistory(state) {
        trace("add to history");
        if (!!history) {
            history.pushState(state, null, state['url']);
            if (state['returnedUrl'] !== ['url']) {
                var stateRedirected = cloneObject(state);
                stateRedirected['url'] = stateRedirected['returnedUrl'];
                stateRedirected['data'] = '';
                // emulate redirection:
                // TODO check
                return setTimeout(function () {
                    return history.pushState(state, null, stateRedirected['url']);
                }, 300);
            }
        }
    };

    var domainFromUrl = function domainFromUrl(url) {
        if (url == null) {
            return null;
        }
        var a = document.createElement('a');
        a.href = url;
        return a.hostname;
    };

    var urlOnThisDomain = function urlOnThisDomain(url) {
        var this_domain = domainFromUrl(window.location.href);
        var url_domain = domainFromUrl(url);
        return this_domain === url_domain;
    };

    var hasDisableAjaxAttr = function hasDisableAjaxAttr($el) {
        return typeof $el.attr('data-no-ajax-on-click') !== 'undefined';
    };

    var noOptimise = function noOptimise(variable) {
        return variable;
    };

    addToHistory({ url: window.location.href, requestType: 'GET', data: '' });

    var ajaxUpdateContent = function ajaxUpdateContent(url, type, data, _addToHistory) {
        //        _getXhr = jQuery.ajaxSettings.xhr;

        //see http://stackoverflow.com/a/26750780/1760643
        //        $.ajaxSettings.xhr = () ->
        //          xhr = _getXhr()
        //          return xhr

        if (type == null) {
            type = "GET";
        }
        if (data == null) {
            data = '';
        }
        if (_addToHistory == null) {
            _addToHistory = true;
        }
        var rawXHR = null;

        return $.ajax({
            url: url,
            type: type,
            data: data,
            xhr: function xhr() {
                var xhr = jQuery.ajaxSettings.xhr();
                rawXHR = xhr;
                return xhr;
            },
            success: function success(success_data, textStatus, request) {
                trace("ajax link success request");
                $('#content').html(success_data);
                if (_addToHistory) {
                    return addToHistory({
                        url: url,
                        requestType: type,
                        data: data,
                        returnedUrl: rawXHR.responseURL
                    });
                }
            },
            error: function error(error_data, textStatus, errorThrown) {
                trace("ajax link error request");
                return UI.notifyFromErrorData(error_data);
            }
        });
    };

    if (!window.hasOwnProperty('popstateBinded')) {
        window.addEventListener('popstate', function (e) {
            trace("back in history");
            var state = $.extend({ 'requestType': 'GET', 'returnedUrl': '', 'data': '' }, e.state);
            var url = state['url'];
            var requestType = state['requestType'];
            var post = state['requestType'] !== 'GET';
            var data = state['data'];
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
    $('body').on('click', 'a', function (e) {
        trace("ajax link clicked");
        var $this = $(this);
        var url = $this.attr('href');
        if (hasDisableAjaxAttr($this)) {
            return;
        }
        if (urlOnThisDomain(url)) {
            e.preventDefault();
            return ajaxUpdateContent(url);
        }
    });

    return $('body').on('click', 'form button[type=submit]', function (e) {
        var $this = $(this);
        var $form = $(this).closest('form');
        trace("ajax button pressed");
        var url = $form.attr('action');
        if (!url) {
            url = window.location.href;
        }
        if (hasDisableAjaxAttr($this) || hasDisableAjaxAttr($form)) {
            return;
        }
        if (urlOnThisDomain(url)) {
            var formEvents = $._data($form.get(0), "events");
            if (formEvents.submit != null) {
                $.each(formEvents.submit, function (j, h) {
                    return (
                        //TODO fill event object and pass to handler?
                        //                    console.log(h.handler)
                        h.handler()
                    );
                });
            }
            var formData = $form.serialize();
            formData += "&" + this.name + "=" + this.value;
            e.preventDefault();
            return ajaxUpdateContent(url, "POST", formData);
        }
    });
});

// TODO  stop event propagating?