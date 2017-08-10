'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * DS205: Consider reworking code to avoid use of IIFEs
 * DS206: Consider reworking classes to avoid initClass
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
$(document).ready(function () {
  var UI = function () {
    _createClass(UI, null, [{
      key: 'initClass',
      value: function initClass() {
        this.DEF_MESSAGE_SUCCESS = 'Запрос выполнен успешно';
        this.DEF_MESSAGE_ERROR = 'Ошибка при выполнении запроса';
        this.MASS_MESSAGE_DELAY = 1000;
      }
    }]);

    function UI() {
      _classCallCheck(this, UI);
    }

    _createClass(UI, null, [{
      key: 'messageSuccess',
      value: function messageSuccess(ajaxData) {
        return ajaxData.message || this.DEF_MESSAGE_SUCCESS;
      }
    }, {
      key: 'messageError',
      value: function messageError(ajaxData) {
        return ajaxData.message || this.DEF_MESSAGE_ERROR;
      }
    }, {
      key: 'notifyFromSuccessData',
      value: function notifyFromSuccessData(ajaxData) {
        return new PNotify({
          title: this.messageSuccess(ajaxData),
          type: 'success'
        });
      }
    }, {
      key: 'notifyFromErrorData',
      value: function notifyFromErrorData(ajaxData) {
        return new PNotify({
          title: this.messageError(ajaxData),
          type: 'error'
        });
      }
    }, {
      key: 'notifyFromArray',
      value: function notifyFromArray(messages) {
        var _this = this;

        var counter = 0;
        return function () {
          var result = [];
          for (var index in messages) {
            var message = messages[index];
            var type = message['type'] || 'success';
            var title = message['title'] || _this.defMessage(type);
            var text = message['text'] || '';
            // http://stackoverflow.com/a/10812341/1760643 - do for scope issues fix
            setTimeout(function (type, title, text) {
              return function () {
                return new PNotify({
                  title: title,
                  type: type,
                  text: text
                });
              };
            }(type, title, text), _this.MASS_MESSAGE_DELAY * counter);
            counter++;
            result.push(1);
          }
          return result;
        }();
      }
    }, {
      key: 'defMessage',
      value: function defMessage(type) {
        type = type || 'success';
        switch (type) {
          case 'error':
            return this.DEF_MESSAGE_ERROR;
          case 'success':
            return this.DEF_MESSAGE_SUCCESS;
          default:
            return this.DEF_MESSAGE_SUCCESS;
        }
      }
    }, {
      key: 'renderBool',
      value: function renderBool(value) {
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
      }
    }]);

    return UI;
  }();

  UI.initClass();

  window.UI = UI;
  PNotify.prototype.options.styling = "bootstrap3";
  PNotify.prototype.options.opacity = 0.7;
  PNotify.prototype.options.hide = true;
  return PNotify.prototype.options.delay = 4000;
});