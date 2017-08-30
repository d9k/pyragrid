

pyragrid.blockConstructors['hello_react'] = function(blockArgs){

  let dataUrl = '/test/mobx_fetch';

  // TODO move abstract function to pyragrid.*
  pyragrid.getJsonDataFromServer(dataUrl, (data) => {
    pyragrid.addStoreTypeMixin('HelloReactData', {
      serverTime: withDefault(mobxStateTree.types.string, ''),
      autoSync: withDefault(mobxStateTree.types.boolean, true)
    });

    let element = blockArgs.element;

    if (!element.id){
      throw 'Element id not provided!';
    }

    // pyragrid.addStoreTypeMixin('HelloReactData', {
    //   serverTime: withDefault(mobxStateTree.types.number, ''),
    //   autoSync: withDefault(mobxStateTree.types.boolean, true)
    // });

    if (!data.hasOwnProperty('serverTime')){
      throw "Can't get data from server! URL: " + dataUrl;
    }

    // recreate store: rewrite to run in parallel (?) (is it even possible?)
    pyragrid.recreateStore((snapshot) => {
        snapshot.serverTime = data.serverTime;
    });

    // TODO add react!
    // TODO add react element rerender function to pyragrid.blocks...!
    let appealTo = blockArgs.appeal_to || 'u';
    element.innerHTML  = '<p>Hello, ' + appealTo + '! Server time: ' +  pyragrid.store.serverTime + ' </p>';
  });

};