$(document).ready () ->
#    window.ajaxLinksDebugMode = true

    debugMode = () ->
        return window.hasOwnProperty('ajaxLinksDebugMode') && window.ajaxLinksDebugMode

    trace = (s) ->
        console.log(s) if debugMode()

    trace "bind ajax click events"

#    http://stackoverflow.com/a/728694/1760643
    cloneObject = (obj) ->
        if null == obj || "object" != typeof obj
            return obj
        copy = obj.constructor()
        for attr of obj
            if obj.hasOwnProperty(attr)
                copy[attr] = obj[attr]
        return copy

    addToHistory = (state) ->
        trace "add to history"
        if !!history
            history.pushState(state, null, state['url'])
            if state['returnedUrl'] != ['url']
                stateRedirected = cloneObject state
                stateRedirected['url'] = stateRedirected['returnedUrl']
                stateRedirected['data'] = '';
                # emulate redirection:
                # TODO check
                setTimeout (-> history.pushState(state, null, stateRedirected['url'])), 300

    domainFromUrl = (url) ->
        a = document.createElement('a')
        a.href = url
        return a.hostname;

    urlOnThisDomain = (url) ->
        this_domain = domainFromUrl(window.location.href)
        url_domain = domainFromUrl(url)
        return this_domain == url_domain

    hasDisableAjaxAttr = ($el) ->
        return typeof $el.attr('data-no-ajax-on-click') isnt 'undefined'

    noOptimise = (variable) ->
        variable

    addToHistory({url: window.location.href, requestType: 'GET', data: ''})

    ajaxUpdateContent = (url, type="GET", data='', _addToHistory=true)->
#        _getXhr = jQuery.ajaxSettings.xhr;

        #see http://stackoverflow.com/a/26750780/1760643
#        $.ajaxSettings.xhr = () ->
#          xhr = _getXhr()
#          return xhr

        rawXHR = null

        $.ajax(
            url: url,
            type: type,
            data: data,
            xhr: () ->
                xhr = jQuery.ajaxSettings.xhr();
                rawXHR = xhr
                return xhr;
            success: (success_data, textStatus, request) ->
                trace "ajax link success request"
                $('.content').html(success_data)
                if _addToHistory
                    addToHistory({
                        url: url,
                        requestType: type,
                        data: data
                        returnedUrl: rawXHR.responseURL
                    })
            error: (error_data, textStatus, errorThrown) ->
                trace "ajax link error request"
                UI.notifyFromErrorData(error_data)
        )

    if !window.hasOwnProperty('popstateBinded')
        window.addEventListener('popstate', (e) ->
            trace "back in history"
            state = $.extend({'requestType': 'GET', 'returnedUrl': '', 'data': ''}, e.state)
            url = state['url']
            requestType = state['requestType'];
            post = (state['requestType'] != 'GET')
            data = state['data']
            if !url
                return
            if post && !confirm('Провести повторную отправку формы?')
                return

            ajaxUpdateContent(url, requestType, data, false)
        )
        trace 'popstate binded'
    window.popstateBinded = true

# TODO check before event attach, maybe selector "href starts with"
    $('body').on 'click', 'a', (e) ->
        trace "ajax link clicked"
        $this = $(this)
        url = $this.attr('href')
        if hasDisableAjaxAttr($this)
            return
        if urlOnThisDomain(url)
            e.preventDefault()
            ajaxUpdateContent(url)

     $('body').on 'click', 'form button[type=submit]', (e) ->
        $this = $(this)
        $form = $(this).closest('form')
        trace "ajax button pressed"
        url = $form.attr('action')
        if !url
            url = window.location.href
        if hasDisableAjaxAttr($this)\
        or hasDisableAjaxAttr($form)
            return
        formData = $form.serialize()
        formData += '&' + this.name + '=' + this.value;
        if urlOnThisDomain(url)
            e.preventDefault()
            ajaxUpdateContent(url, "POST", formData)

# TODO  stop event propagating?