/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * DS205: Consider reworking code to avoid use of IIFEs
 * DS206: Consider reworking classes to avoid initClass
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
$(document).ready(function() {
  class UI {
    static initClass() {
      this.DEF_MESSAGE_SUCCESS = 'Запрос выполнен успешно';
      this.DEF_MESSAGE_ERROR = 'Ошибка при выполнении запроса';
      this.MASS_MESSAGE_DELAY = 1000;
    }
    constructor() {}
    static messageSuccess(ajaxData) {
      return ajaxData.message || this.DEF_MESSAGE_SUCCESS;
    }

    static messageError(ajaxData) {
      return ajaxData.message || this.DEF_MESSAGE_ERROR;
    }

    static notifyFromSuccessData(ajaxData) {
        return new PNotify({
          title: this.messageSuccess(ajaxData),
          type: 'success'
        });
      }

    static notifyFromErrorData(ajaxData) {
        return new PNotify({
          title: this.messageError(ajaxData),
          type: 'error'
        });
      }

    static notifyFromArray(messages) {
      let counter = 0;
      return (() => {
        const result = [];
        for (let index in messages) {
          const message = messages[index];
          const type = message['type'] || 'success';
          const title = message['title'] || this.defMessage(type);
          const text = message['text'] || '';
          // http://stackoverflow.com/a/10812341/1760643 - do for scope issues fix
          setTimeout((((type, title, text) =>
            () =>
              new PNotify({
                title,
                type,
                text
              })
            
          )
          (type, title, text)), this.MASS_MESSAGE_DELAY * counter);
          counter++;
          result.push(1);
        }
        return result;
      })();
    }


    static defMessage(type) {
        type = type || 'success';
        switch (type) {
          case 'error': return this.DEF_MESSAGE_ERROR;
          case 'success': return this.DEF_MESSAGE_SUCCESS;
          default: return this.DEF_MESSAGE_SUCCESS;
        }
      }

    static renderBool(value) {
        switch (value) {
          case "true": return "да";
          case "false": return "нет";
          case "True": return "Да";
          case "False": return "Нет";
          default: return "?";
        }
      }
  }
  UI.initClass();

  window.UI = UI;
  PNotify.prototype.options.styling = "bootstrap3";
  PNotify.prototype.options.opacity = 0.7;
  PNotify.prototype.options.hide = true;
  return PNotify.prototype.options.delay = 4000;
});