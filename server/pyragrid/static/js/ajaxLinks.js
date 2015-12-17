(function() {
  $(document).ready(function() {
    var addToHistory, ajaxUpdateContent, cloneObject, debugMode, domainFromUrl, hasDisableAjaxAttr, noOptimise, trace, urlOnThisDomain;
    debugMode = function() {
      return window.hasOwnProperty('ajaxLinksDebugMode') && window.ajaxLinksDebugMode;
    };
    trace = function(s) {
      if (debugMode()) {
        return console.log(s);
      }
    };
    trace("bind ajax click events");
    cloneObject = function(obj) {
      var attr, copy;
      if (null === obj || "object" !== typeof obj) {
        return obj;
      }
      copy = obj.constructor();
      for (attr in obj) {
        if (obj.hasOwnProperty(attr)) {
          copy[attr] = obj[attr];
        }
      }
      return copy;
    };
    addToHistory = function(state) {
      var stateRedirected;
      trace("add to history");
      if (!!history) {
        history.pushState(state, null, state['url']);
        if (state['returnedUrl'] !== ['url']) {
          stateRedirected = cloneObject(state);
          stateRedirected['url'] = stateRedirected['returnedUrl'];
          stateRedirected['data'] = '';
          return setTimeout((function() {
            return history.pushState(state, null, stateRedirected['url']);
          }), 300);
        }
      }
    };
    domainFromUrl = function(url) {
      var a;
      if (url == null) {
        return null;
      }
      a = document.createElement('a');
      a.href = url;
      return a.hostname;
    };
    urlOnThisDomain = function(url) {
      var this_domain, url_domain;
      this_domain = domainFromUrl(window.location.href);
      url_domain = domainFromUrl(url);
      return this_domain === url_domain;
    };
    hasDisableAjaxAttr = function($el) {
      return typeof $el.attr('data-no-ajax-on-click') !== 'undefined';
    };
    noOptimise = function(variable) {
      return variable;
    };
    addToHistory({
      url: window.location.href,
      requestType: 'GET',
      data: ''
    });
    ajaxUpdateContent = function(url, type, data, _addToHistory) {
      var rawXHR;
      if (type == null) {
        type = "GET";
      }
      if (data == null) {
        data = '';
      }
      if (_addToHistory == null) {
        _addToHistory = true;
      }
      rawXHR = null;
      return $.ajax({
        url: url,
        type: type,
        data: data,
        xhr: function() {
          var xhr;
          xhr = jQuery.ajaxSettings.xhr();
          rawXHR = xhr;
          return xhr;
        },
        success: function(success_data, textStatus, request) {
          trace("ajax link success request");
          $('.content').html(success_data);
          if (_addToHistory) {
            return addToHistory({
              url: url,
              requestType: type,
              data: data,
              returnedUrl: rawXHR.responseURL
            });
          }
        },
        error: function(error_data, textStatus, errorThrown) {
          trace("ajax link error request");
          return UI.notifyFromErrorData(error_data);
        }
      });
    };
    if (!window.hasOwnProperty('popstateBinded')) {
      window.addEventListener('popstate', function(e) {
        var data, post, requestType, state, url;
        trace("back in history");
        state = $.extend({
          'requestType': 'GET',
          'returnedUrl': '',
          'data': ''
        }, e.state);
        url = state['url'];
        requestType = state['requestType'];
        post = state['requestType'] !== 'GET';
        data = state['data'];
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
    $('body').on('click', 'a', function(e) {
      var $this, url;
      trace("ajax link clicked");
      $this = $(this);
      url = $this.attr('href');
      if (hasDisableAjaxAttr($this)) {
        return;
      }
      if (urlOnThisDomain(url)) {
        e.preventDefault();
        return ajaxUpdateContent(url);
      }
    });
    return $('body').on('click', 'form button[type=submit]', function(e) {
      var $form, $this, formData, formEvents, url;
      $this = $(this);
      $form = $(this).closest('form');
      trace("ajax button pressed");
      url = $form.attr('action');
      if (!url) {
        url = window.location.href;
      }
      if (hasDisableAjaxAttr($this) || hasDisableAjaxAttr($form)) {
        return;
      }
      if (urlOnThisDomain(url)) {
        formEvents = $._data($form.get(0), "events");
        if (formEvents.submit != null) {
          $.each(formEvents.submit, function(j, h) {
            return h.handler();
          });
        }
        formData = $form.serialize();
        formData += '&' + this.name + '=' + this.value;
        e.preventDefault();
        return ajaxUpdateContent(url, "POST", formData);
      }
    });
  });

}).call(this);
