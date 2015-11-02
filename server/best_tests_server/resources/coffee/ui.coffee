$(document).ready ->
  class UI
    constructor: () ->
    @DEF_MESSAGE_SUCCESS: 'Изменение прошло успешно'
    @DEF_MESSAGE_ERROR: 'Ошибка при изменении'
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