'use strict';

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

/*
 * decaffeinate suggestions:
 * DS101: Remove unnecessary use of Array.from
 * DS102: Remove unnecessary code created because of implicit returns
 * DS205: Consider reworking code to avoid use of IIFEs
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
if (window._loadResource_loaded == null) {

    var strEndsWith = function strEndsWith(str, suffix) {
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    };

    var typeIsArray = function typeIsArray(value) {
        return value && (typeof value === 'undefined' ? 'undefined' : _typeof(value)) === 'object' && value instanceof Array && typeof value.length === 'number' && typeof value.splice === 'function' && !value.propertyIsEnumerable('length');
    };

    var loadCss = function loadCss(filename) {
        if (!filename) {
            return;
        }
        var existingCss = $('link[rel=stylesheet]');
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = Array.from(existingCss)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                var cssTag = _step.value;

                if (cssTag.getAttribute('href') === filename) {
                    // or src?
                    return;
                }
            }
        } catch (err) {
            _didIteratorError = true;
            _iteratorError = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion && _iterator.return) {
                    _iterator.return();
                }
            } finally {
                if (_didIteratorError) {
                    throw _iteratorError;
                }
            }
        }

        return $('head').append('<link rel=\'stylesheet\' type=\'text/css\' href=\'' + filename + '\'>');
    };

    var loadJS = function loadJS(filename) {
        if (!filename) {
            return;
        }
        var existingJs = $('script');
        var _iteratorNormalCompletion2 = true;
        var _didIteratorError2 = false;
        var _iteratorError2 = undefined;

        try {
            for (var _iterator2 = Array.from(existingJs)[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                var jsTag = _step2.value;

                var scriptType = jsTag.typeName;
                if (scriptType && scriptType !== 'text/javascript') {
                    continue;
                }
                if (jsTag.getAttribute('src') === filename) {
                    return;
                }
            }
        } catch (err) {
            _didIteratorError2 = true;
            _iteratorError2 = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion2 && _iterator2.return) {
                    _iterator2.return();
                }
            } finally {
                if (_didIteratorError2) {
                    throw _iteratorError2;
                }
            }
        }

        return $('head').append('<script type=\'text/javascript\' src=\'' + filename + '\'></script>');
    };

    var loadResource = function loadResource(fileName) {
        var fileNames = typeIsArray(fileName) ? fileName : [fileName];
        return function () {
            var result = [];
            var _iteratorNormalCompletion3 = true;
            var _didIteratorError3 = false;
            var _iteratorError3 = undefined;

            try {
                for (var _iterator3 = Array.from(fileNames)[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                    fileName = _step3.value;

                    if (strEndsWith(fileName, '.js')) {
                        result.push(loadJS(fileName));
                    } else if (strEndsWith(fileName, '.css')) {
                        result.push(loadCss(fileName));
                    } else {
                        result.push(undefined);
                    }
                }
            } catch (err) {
                _didIteratorError3 = true;
                _iteratorError3 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion3 && _iterator3.return) {
                        _iterator3.return();
                    }
                } finally {
                    if (_didIteratorError3) {
                        throw _iteratorError3;
                    }
                }
            }

            return result;
        }();
    };

    window.loadResource = loadResource;
    window._loadResource_loaded = true;
}