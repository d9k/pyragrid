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
          title: @.messageSuccess(ajaxData)
          type: 'error'
        )

  window.UI = UI
  PNotify.prototype.options.styling = "bootstrap3"
  PNotify.prototype.options.opacity = 0.7
  PNotify.prototype.options.hide = true
  PNotify.prototype.options.delay = 4000