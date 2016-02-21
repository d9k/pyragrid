if (! window._loadResource_loaded?)

    strEndsWith = (str, suffix) ->
       str.indexOf(suffix, str.length - suffix.length) != -1

    typeIsArray = ( value ) ->
        value and
            typeof value is 'object' and
            value instanceof Array and
            typeof value.length is 'number' and
            typeof value.splice is 'function' and
            not ( value.propertyIsEnumerable 'length' )

    loadCss = (filename)->
        return if !filename
        existingCss = $('link[rel=stylesheet]')
        for cssTag in existingCss
            if cssTag.getAttribute('href') == filename  # or src?
                return
        $('head').append("<link rel='stylesheet' type='text/css' href='#{filename}'>");

    loadJS = (filename) ->
        return if !filename
        existingJs = $('script')
        for jsTag in existingJs
            scriptType = jsTag.typeName
            if scriptType and scriptType != 'text/javascript'
                continue
            if jsTag.getAttribute('src') == filename
                return
        $('head').append("<script type='text/javascript' src='" + filename + "'><" + "/script>")

    loadResource = (fileName) ->
        fileNames = if typeIsArray(fileName) then fileName else [fileName]
        for fileName in fileNames
            if strEndsWith(fileName, '.js')
                loadJS(fileName)
            else if strEndsWith(fileName, '.css')
                loadCss(fileName)

    window.loadResource = loadResource
    window._loadResource_loaded = true;