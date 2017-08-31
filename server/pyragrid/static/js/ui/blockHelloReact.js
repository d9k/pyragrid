'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var HelloReactWrapper = function (_React$Component) {
  _inherits(HelloReactWrapper, _React$Component);

  function HelloReactWrapper(props) {
    _classCallCheck(this, HelloReactWrapper);

    return _possibleConstructorReturn(this, (HelloReactWrapper.__proto__ || Object.getPrototypeOf(HelloReactWrapper)).call(this, props));
  }

  _createClass(HelloReactWrapper, [{
    key: 'render',
    value: function render() {
      var _props = this.props,
          store = _props.store,
          storeBranchId = _props.storeBranchId;


      var serverTime = store.serverTime;
      var appealTo = store[storeBranchId].appealTo;

      if (!storeBranchId) {
        throw "storeBranchId not defined";
      }

      return React.createElement(HelloReact, { appealTo: appealTo, serverTime: serverTime });
    }
  }]);

  return HelloReactWrapper;
}(React.Component);

var HelloReactWrapperWithObserver = mobxReact.observer(HelloReactWrapper);

var blockType = 'hello_react';

pyragrid.blockConstructors[blockType] = function (blockArgs) {

  var element = blockArgs.element;

  if (!element.id) {
    throw 'Element id not provided!';
  }

  var dataUrl = '/test/mobx_fetch';
  var appealTo = blockArgs.appeal_to || 'u';

  // TODO move abstract function to pyragrid.*
  pyragrid.getJsonDataFromServer(dataUrl, function (data) {
    pyragrid.storeAddTypeMixin('HelloReactData', {
      serverTime: withDefault(mobxStateTree.types.string, ''),
      serverTimeAutoSync: withDefault(mobxStateTree.types.boolean, true)
    });

    pyragrid.storeAddTypeMixinAsBranch(element.id, {
      appealTo: appealTo
    });

    // pyragrid.storeAddTypeMixin('HelloReactData', {
    //   serverTime: withDefault(mobxStateTree.types.number, ''),
    //   autoSync: withDefault(mobxStateTree.types.boolean, true)
    // });

    if (!data.hasOwnProperty('serverTime')) {
      throw "Can't get data from server! URL: " + dataUrl;
    }

    setInterval(function () {
      if (pyragrid.store.serverTimeAutoSync) {
        pyragrid.getJsonDataFromServer(dataUrl, function (data) {
          pyragrid.store.serverTime = data.serverTime;
        });
      }
    }, 1000);

    pyragrid.blocks[blockType].instances[element.id].rerender = function () {
      ReactDOM.render(React.createElement(HelloReactWrapperWithObserver, { store: pyragrid.store, storeBranchId: element.id }), document.getElementById(element.id));
    };

    // recreate store: rewrite to run in parallel (?) (is it even possible?)
    pyragrid.storeRecreate(function (snapshot) {
      snapshot.serverTime = data.serverTime;
      snapshot[element.id] = {
        appealTo: appealTo
      };
    });

    // pyragrid.blocks[blockType].instances[element.id].rerender();

    // TODO add react element rerender function to pyragrid.blocks...!
  });
};