(function() {
  var loadCss, loadJS, loadResource, strEndsWith, typeIsArray;

  if (window._loadResource_loaded == null) {
    strEndsWith = function(str, suffix) {
      return str.indexOf(suffix, str.length - suffix.length) !== -1;
    };
    typeIsArray = function(value) {
      return value && typeof value === 'object' && value instanceof Array && typeof value.length === 'number' && typeof value.splice === 'function' && !(value.propertyIsEnumerable('length'));
    };
    loadCss = function(filename) {
      var cssTag, existingCss, i, len;
      if (!filename) {
        return;
      }
      existingCss = $('link[rel=stylesheet]');
      for (i = 0, len = existingCss.length; i < len; i++) {
        cssTag = existingCss[i];
        if (cssTag.getAttribute('href') === filename) {
          return;
        }
      }
      return $('head').append("<link rel='stylesheet' type='text/css' href='" + filename + "'>");
    };
    loadJS = function(filename) {
      var existingJs, i, jsTag, len, scriptType;
      if (!filename) {
        return;
      }
      existingJs = $('script');
      for (i = 0, len = existingJs.length; i < len; i++) {
        jsTag = existingJs[i];
        scriptType = jsTag.typeName;
        if (scriptType && scriptType !== 'text/javascript') {
          continue;
        }
        if (jsTag.getAttribute('src') === filename) {
          return;
        }
      }
      return $('head').append("<script type='text/javascript' src='" + filename + "'><" + "/script>");
    };
    loadResource = function(fileName) {
      var fileNames, i, len, results;
      fileNames = typeIsArray(fileName) ? fileName : [fileName];
      results = [];
      for (i = 0, len = fileNames.length; i < len; i++) {
        fileName = fileNames[i];
        if (strEndsWith(fileName, '.js')) {
          results.push(loadJS(fileName));
        } else if (strEndsWith(fileName, '.css')) {
          results.push(loadCss(fileName));
        } else {
          results.push(void 0);
        }
      }
      return results;
    };
    window.loadResource = loadResource;
    window._loadResource_loaded = true;
  }

}).call(this);
