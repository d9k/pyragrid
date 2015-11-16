$(document).ready ->
  class UI
    constructor: () ->
    @DEF_MESSAGE_SUCCESS: 'Запрос выполнен успешно'
    @DEF_MESSAGE_ERROR: 'Ошибка при выполнении запроса'
    @MASS_MESSAGE_DELAY: 1000
    @messageSuccess: (ajaxData) ->
      ajaxData.message || @.DEF_MESSAGE_SUCCESS

    @messageError: (ajaxData) ->
      ajaxData.message || @.DEF_MESSAGE_ERROR

    @notifyFromSuccessData: (ajaxData) ->
        new PNotify(
          title: @.messageSuccess(ajaxData)
          type: 'success'
        )

    @notifyFromErrorData: (ajaxData) ->
        new PNotify(
          title: @.messageError(ajaxData)
          type: 'error'
        )

    @notifyFromArray: (messages) ->
      counter = 0
      for index, message of messages
          type = message['type'] || 'success'
          title = message['title'] || @.defMessage(type)
          text = message['text'] || ''
          # http://stackoverflow.com/a/10812341/1760643 - do for scope issues fix
          setTimeout (do (type, title, text) ->
            () ->
              new PNotify(
                title: title,
                type: type
                text: text
              )
          ), @MASS_MESSAGE_DELAY * counter
          counter++
          1


    @defMessage: (type) ->
        type = type || 'success'
        switch type
          when 'error' then @.DEF_MESSAGE_ERROR
          when 'success' then @.DEF_MESSAGE_SUCCESS
          else @.DEF_MESSAGE_SUCCESS

    @renderBool: (value) ->
        switch value
          when "true" then "да"
          when "false" then "нет"
          when "True" then "Да"
          when "False" then "Нет"
          else "?"

  window.UI = UI
  PNotify.prototype.options.styling = "bootstrap3"
  PNotify.prototype.options.opacity = 0.7
  PNotify.prototype.options.hide = true
  PNotify.prototype.options.delay = 4000