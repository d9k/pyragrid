(function() {
  $(document).ready(function() {
    var UI;
    UI = (function() {
      function UI() {}

      UI.DEF_MESSAGE_SUCCESS = 'Запрос выполнен успешно';

      UI.DEF_MESSAGE_ERROR = 'Ошибка при выполнении запроса';

      UI.messageSuccess = function(ajaxData) {
        return ajaxData.message || this.DEF_MESSAGE_SUCCESS;
      };

      UI.messageError = function(ajaxData) {
        return ajaxData.message || this.DEF_MESSAGE_ERROR;
      };

      UI.notifyFromSuccessData = function(ajaxData) {
        return new PNotify({
          title: this.messageSuccess(ajaxData),
          type: 'success'
        });
      };

      UI.notifyFromErrorData = function(ajaxData) {
        return new PNotify({
          title: this.messageError(ajaxData),
          type: 'error'
        });
      };

      UI.renderBool = function(value) {
        switch (value) {
          case "true":
            return "да";
          case "false":
            return "нет";
          case "True":
            return "Да";
          case "False":
            return "Нет";
          default:
            return "?";
        }
      };

      return UI;

    })();
    window.UI = UI;
    PNotify.prototype.options.styling = "bootstrap3";
    PNotify.prototype.options.opacity = 0.7;
    PNotify.prototype.options.hide = true;
    return PNotify.prototype.options.delay = 4000;
  });

}).call(this);
