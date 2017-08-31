class HelloReactWrapper extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let {store, storeBranchId} = this.props;

    let serverTime = store.serverTime;
    let appealTo = store[storeBranchId].appealTo;

    if (!storeBranchId){
      throw "storeBranchId not defined";
    }

    return (
      <HelloReact appealTo={appealTo} serverTime={serverTime} />
    );
  }
}

let HelloReactWrapperWithObserver = mobxReact.observer(HelloReactWrapper);

let blockType = 'hello_react';

pyragrid.blockConstructors[blockType] = function(blockArgs){

  let element = blockArgs.element;

  if (!element.id){
    throw 'Element id not provided!';
  }

  let dataUrl = '/test/mobx_fetch';
  let appealTo = blockArgs.appeal_to || 'u';

  // TODO move abstract function to pyragrid.*
  pyragrid.getJsonDataFromServer(dataUrl, (data) => {
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

    if (!data.hasOwnProperty('serverTime')){
      throw "Can't get data from server! URL: " + dataUrl;
    }

    setInterval(
      () => {
        if (pyragrid.store.serverTimeAutoSync) {
          pyragrid.getJsonDataFromServer(dataUrl, data => {
            pyragrid.store.serverTime = data.serverTime;
          })
        }
      },
      1000
    );

    pyragrid.blocks[blockType].instances[element.id].rerender = () => {
      ReactDOM.render(
        <HelloReactWrapperWithObserver store={pyragrid.store} storeBranchId={element.id} />,
         document.getElementById(element.id)
      );
    };

    // recreate store: rewrite to run in parallel (?) (is it even possible?)
    pyragrid.storeRecreate((snapshot) => {
        snapshot.serverTime = data.serverTime;
        snapshot[element.id] = {
          appealTo: appealTo
        };
      }
    );

    // pyragrid.blocks[blockType].instances[element.id].rerender();

    // TODO add react element rerender function to pyragrid.blocks...!
  });

};