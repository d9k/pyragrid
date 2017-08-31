'use strict';

pyragrid.blockConstructors['hello_react'] = function (blockArgs) {

  var dataUrl = '/test/mobx_fetch';

  // TODO move abstract function to pyragrid.*
  pyragrid.getJsonDataFromServer(dataUrl, function (data) {
    pyragrid.storeAddTypeMixin('HelloReactData', {
      serverTime: withDefault(mobxStateTree.types.string, ''),
      autoSync: withDefault(mobxStateTree.types.boolean, true)
    });

    var element = blockArgs.element;

    if (!element.id) {
      throw 'Element id not provided!';
    }

    // pyragrid.storeAddTypeMixin('HelloReactData', {
    //   serverTime: withDefault(mobxStateTree.types.number, ''),
    //   autoSync: withDefault(mobxStateTree.types.boolean, true)
    // });

    if (!data.hasOwnProperty('serverTime')) {
      throw "Can't get data from server! URL: " + dataUrl;
    }

    // recreate store: rewrite to run in parallel (?) (is it even possible?)
    pyragrid.storeRecreate(function (snapshot) {
      snapshot.serverTime = data.serverTime;
    });

    // TODO add react!
    // TODO add react element rerender function to pyragrid.blocks...!
    var appealTo = blockArgs.appeal_to || 'u';
    element.innerHTML = '<p>Hello, ' + appealTo + '! Server time: ' + pyragrid.store.serverTime + ' </p>';
  });
};