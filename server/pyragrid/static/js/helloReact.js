"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

//TODO move to ui
//TODO envelop with umd

var ShowNumber = function (_React$Component) {
  _inherits(ShowNumber, _React$Component);

  function ShowNumber(props) {
    _classCallCheck(this, ShowNumber);

    return _possibleConstructorReturn(this, (ShowNumber.__proto__ || Object.getPrototypeOf(ShowNumber)).call(this, props));
  }

  _createClass(ShowNumber, [{
    key: "render",
    value: function render() {
      var number = this.props.number;


      return React.createElement(
        "span",
        null,
        number
      );
    }
  }]);

  return ShowNumber;
}(React.Component);

var autoUpdateFromServer = true;

// TODO rewrite
// TODO add hello world line with server time and user name
// TODO refer to component data from store by component id

var HelloReact = function (_React$Component2) {
  _inherits(HelloReact, _React$Component2);

  function HelloReact(props) {
    _classCallCheck(this, HelloReact);

    return _possibleConstructorReturn(this, (HelloReact.__proto__ || Object.getPrototypeOf(HelloReact)).call(this, props));
  }

  _createClass(HelloReact, [{
    key: "render",
    value: function render() {
      var store = this.props.store;


      return React.createElement(
        "div",
        null,
        React.createElement(
          "button",
          { onClick: function onClick(event) {
              store.data.number = store.data.number - 1;
            } },
          "-"
        ),
        "\xA0",
        React.createElement(ShowNumber, { number: store.data.number }),
        "\xA0",
        React.createElement(
          "button",
          { onClick: function onClick(event) {
              store.data.number = store.data.number + 1;
            } },
          "+"
        ),
        "\xA0",
        React.createElement(
          "p",
          null,
          "updates from server: ",
          store.data.serverTime
        ),
        React.createElement(
          "button",
          { onClick: function onClick(event) {
              autoUpdateFromServer = !autoUpdateFromServer;
            } },
          "Toggle autoupdate from server"
        )
      );
    }
  }]);

  return HelloReact;
}(React.Component);