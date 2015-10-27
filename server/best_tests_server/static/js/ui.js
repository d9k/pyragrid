(function() {
  $(document).ready(function() {
    var UI;
    UI = (function() {
      function UI() {}

      UI.DEF_MESSAGE_SUCCESS = 'Изменение прошло успешно';

      UI.DEF_MESSAGE_ERROR = 'Ошибка при изменении';

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
          title: this.messageSuccess(ajaxData),
          type: 'error'
        });
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
