(function() {
  $(document).ready(function() {
    var addToHistory, ajaxUpdateContent, debugMode, domainFromUrl, trace, urlOnThisDomain;
    debugMode = function() {
      return window.hasOwnProperty('ajaxLinksDebugMode') && window.ajaxLinksDebugMode;
    };
    trace = function(s) {
      if (debugMode()) {
        return console.log(s);
      }
    };
    trace("bind ajax click events");
    addToHistory = function(url, state) {
      trace("add to history");
      if (!!history) {
        return history.pushState(state, null, url);
      }
    };
    domainFromUrl = function(url) {
      var a;
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
    ajaxUpdateContent = function(url, type, data, _addToHistory) {
      if (type == null) {
        type = "GET";
      }
      if (data == null) {
        data = '';
      }
      if (_addToHistory == null) {
        _addToHistory = true;
      }
      return $.ajax({
        url: url,
        type: type,
        data: data,
        success: function(success_data) {
          trace("ajax link success request");
          $('.content').html(success_data);
          if (_addToHistory) {
            return addToHistory(url, {
              url: url,
              requestType: type,
              data: data
            });
          }
        },
        error: function(error_data) {
          trace("ajax link error request");
          return UI.notifyFromErrorData(error_data);
        }
      });
    };
    if (!window.hasOwnProperty('popstateBinded')) {
      window.addEventListener('popstate', function(e) {
        var data, post, requestType, state, url;
        trace("back in history");
        state = e.state;
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
      var url;
      trace("ajax link clicked");
      url = $(this).attr('href');
      if (urlOnThisDomain(url)) {
        e.preventDefault();
        return ajaxUpdateContent(url);
      }
    });
    return $('body').on('click', 'form button[type=submit]', function(e) {
      var $form, url;
      $form = $(this).closest('form');
      trace("ajax button pressed");
      url = $form.attr('action');
      if (!url) {
        url = window.location.href;
      }
      if (urlOnThisDomain(url)) {
        e.preventDefault();
        return ajaxUpdateContent(url, "POST", $form.serialize());
      }
    });
  });

}).call(this);
