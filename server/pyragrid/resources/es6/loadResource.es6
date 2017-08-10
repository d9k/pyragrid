/*
 * decaffeinate suggestions:
 * DS101: Remove unnecessary use of Array.from
 * DS102: Remove unnecessary code created because of implicit returns
 * DS205: Consider reworking code to avoid use of IIFEs
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
if ((window._loadResource_loaded == null)) {

    const strEndsWith = (str, suffix) => str.indexOf(suffix, str.length - suffix.length) !== -1;

    const typeIsArray =  value  =>
        value &&
            (typeof value === 'object') &&
            value instanceof Array &&
            (typeof value.length === 'number') &&
            (typeof value.splice === 'function') &&
            !( value.propertyIsEnumerable('length') )
    ;

    const loadCss = function(filename){
        if (!filename) { return; }
        const existingCss = $('link[rel=stylesheet]');
        for (let cssTag of Array.from(existingCss)) {
            if (cssTag.getAttribute('href') === filename) {  // or src?
                return;
            }
        }
        return $('head').append(`<link rel='stylesheet' type='text/css' href='${filename}'>`);
    };

    const loadJS = function(filename) {
        if (!filename) { return; }
        const existingJs = $('script');
        for (let jsTag of Array.from(existingJs)) {
            const scriptType = jsTag.typeName;
            if (scriptType && (scriptType !== 'text/javascript')) {
                continue;
            }
            if (jsTag.getAttribute('src') === filename) {
                return;
            }
        }
        return $('head').append(`<script type='text/javascript' src='${filename}'></script>`);
    };

    const loadResource = function(fileName) {
        const fileNames = typeIsArray(fileName) ? fileName : [fileName];
        return (() => {
            const result = [];
            for (fileName of Array.from(fileNames)) {
                if (strEndsWith(fileName, '.js')) {
                    result.push(loadJS(fileName));
                } else if (strEndsWith(fileName, '.css')) {
                    result.push(loadCss(fileName));
                } else {
                    result.push(undefined);
                }
            }
            return result;
        })();
    };

    window.loadResource = loadResource;
    window._loadResource_loaded = true;
}