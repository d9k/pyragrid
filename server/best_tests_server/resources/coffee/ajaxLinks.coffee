$(document).ready () ->
#    window.ajaxLinksDebugMode = true

    debugMode = () ->
        return window.hasOwnProperty('ajaxLinksDebugMode') && window.ajaxLinksDebugMode

    trace = (s) ->
        console.log(s) if debugMode()

    trace "bind ajax click events"

    addToHistory = (url, state) ->
        trace "add to history"
        if !!history
            history.pushState(state, null, url)

    domainFromUrl = (url) ->
        a = document.createElement('a')
        a.href = url
        return a.hostname

    urlOnThisDomain = (url) ->
        this_domain = domainFromUrl(window.location.href)
        url_domain = domainFromUrl(url)
        return this_domain == url_domain

    ajaxUpdateContent = (url, type="GET", data='', _addToHistory=true)->
        $.ajax(
            url: url,
            type: type,
            data: data,
            success: (success_data) ->
                trace "ajax link success request"
                $('.content').html(success_data)
                if _addToHistory
                    addToHistory(url, {
                        url: url,
                        requestType: type,
                        data: data
                    })
            error: (error_data) ->
                trace "ajax link error request"
                UI.notifyFromErrorData(error_data)
        )

    if !window.hasOwnProperty('popstateBinded')
        window.addEventListener('popstate', (e) ->
            trace "back in history"
            state = e.state
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
        url = $(this).attr('href')
        if urlOnThisDomain(url)
            e.preventDefault()
            ajaxUpdateContent(url)

     $('body').on 'click', 'form button[type=submit]', (e) ->
        $form = $(this).closest('form')
        trace "ajax button pressed"
        url = $form.attr('action')
        if !url
            url = window.location.href
        if urlOnThisDomain(url)
            e.preventDefault()
            ajaxUpdateContent(url, "POST", $form.serialize())

# TODO  stop event propagating?