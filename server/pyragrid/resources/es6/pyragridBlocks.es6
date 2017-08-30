if (typeof window.pyragrid === 'undefined'){
  window.pyragrid = {};
}

//// manual parsing is too hard. switched to nunjucks
// pyragrid.renderBlocks = function(element) {
//   let findTextNodes = function(element, onTextNode){
//     if (element.tagName === "SCRIPT"){
//       return;
//     }
//
//     let childNodes = element.childNodes;
//     for (let i = 0; i < childNodes.length; i++){
//       let childNode = childNodes[i];
//       if (childNode.nodeType === Node.TEXT_NODE){
//         onTextNode(childNode);
//       } else if (childNode.nodeType === Node.ELEMENT_NODE){
//         findTextNodes(childNode, onTextNode);
//       } else {
//         console.log('nodeType:' + childNode.nodeType);
//       }
//     }
//   };
//
//   findTextNodes(element, function (textNode) {
//     console.log(textNode.textContent);
//   })
// };

pyragrid.blockConstructors = {};
pyragrid.afterTemplateRenderHandlers = {};

// define global function: get list of values without keys from object
window.objectValues = function(obj) {
  let values = [];
  for (let key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      values.push(obj[key]);
      // use val
    }
  }
  return values;
};

pyragrid.blocks = {};

pyragrid.renderBlocks = function(element) {
    let nunjucksEnv = new nunjucks.Environment();

    nunjucksEnv.addGlobal('render_block', function(blockArgs) {
      if (!blockArgs.hasOwnProperty('type')) {
        throw "Block type was not set";
      }
      let blockType = blockArgs.type;

      if (pyragrid.blockConstructors.hasOwnProperty(blockType)){
        if (!pyragrid.blocks.hasOwnProperty(blockType)){
          pyragrid.blocks[blockType] = {
            instances: [],
            maxId: 0
          };
        }

        pyragrid.blocks[blockType].maxId += 1;
        let newBlockId = 'block_' + blockType + '_' + pyragrid.blocks[blockType].maxId;
        pyragrid.blocks[blockType].instances.push(newBlockId);

        // first step: convert block call to html div
        // next step would be actually render block
        let dummyElement = document.createElement('div');
        dummyElement.id = newBlockId;
        dummyElement.className = 'pyragrid_block pyragrid_block_' + blockType;
        dummyElement.setAttribute('data-block-args', JSON.stringify(blockArgs));
        return new nunjucks.runtime.SafeString(dummyElement.outerHTML);
      } else {
        console.log('Warning: Block type ' + blockType + ' handler function was not set!')
      }
    });

    let renderedString = nunjucksEnv.renderString(element.innerHTML);
    element.innerHTML = renderedString;

    let blockDummyElements = document.getElementsByClassName('pyragrid_block');
    for (let dummyElement of blockDummyElements) {
      let blockArgs = dummyElement.getAttribute('data-block-args');
      if (typeof blockArgs !== 'string'){
        console.log('Warning: block dummy (div with id ' + dummyElement.id + ') has no data-block-args argument');
        return;
      }
      // TODO JSON parse error handling?
      blockArgs = JSON.parse(blockArgs);
      // blockArgs.id = currentElement.id;
      blockArgs.element = dummyElement;

      // run in parallel
      setTimeout(() => {
        pyragrid.blockConstructors[blockArgs.type](blockArgs);
      }, 0);
    }

    //TODO pyragrid.blockConstructors[blockType](blockParams);
};

window.withDefault = mobxStateTree.types.optional;

pyragrid.storeTypeMixins = {};
pyragrid.onRecreateStore = {};

pyragrid.addStoreTypeMixin = (mixinName, structure) => {
  if (!pyragrid.storeTypeMixins.hasOwnProperty(mixinName)){
    pyragrid.storeTypeMixins[mixinName] = mobxStateTree.types.model(mixinName, structure);
  }
};

pyragrid.addStoreTypeMixin('TestMixin', {
  testField: withDefault(mobxStateTree.types.string, 'test value')
});

pyragrid.addStoreTypeMixin('RecreateCountMixin', {
  storeRecreateCount: withDefault(mobxStateTree.types.number, 0)
});

pyragrid.onRecreateStore.updateRecreateCountMixin = (snapshot) => {
   snapshot.storeRecreateCount += 1;
};

pyragrid.recreateStore = (modifySnapshotCallback) => {

  pyragrid.StoreType = (mobxStateTree.types.compose.apply(null,
      ['Store', ...objectValues(pyragrid.storeTypeMixins)]
  ));

  let snapshot = {};
  if (typeof pyragrid.store !== 'undefined'){
    snapshot = mobxStateTree.getSnapshot(pyragrid.store);
  }
  // snapshot is read only, need create writeable clone
  let snapshotCopy = _.cloneDeep(snapshot);

  if (typeof modifySnapshotCallback === 'function'){
    modifySnapshotCallback(snapshotCopy);
  }

  objectValues(pyragrid.onRecreateStore).forEach((onRecreateStoreCallback) => {
    onRecreateStoreCallback(snapshotCopy);
  });

  pyragrid.store = pyragrid.StoreType.create(snapshotCopy);
  mobxStateTree.unprotect(pyragrid.store);
};

pyragrid.recreateStore((snapshot) => {
    snapshot.storeRecreateCount = 0;
});

// pyragrid.storeTypeMixins.SC2Mixin = mobxStateTree.types.model('SC2Mixin', {
//     SC2Unit: withDefault(mobxStateTree.types.string, 'lurker')
// });
//
// pyragrid.recreateStore((snapshot) => {
//   //snapshot.SC2Unit = 'marine';
// });

pyragrid.getJsonDataFromServer = (url, callback) => {
    fetch(
      url,
      {
        credentials: "same-origin"
      }
    ).then( response => {
      if (response.status === 200){
        return response.json()
      }
      return {};
    }).then( data => {
      callback(data);
    });
  };

pyragrid.blockConstructors['hello_world'] = function(blockArgs){
  let element = blockArgs.element;
  let appealTo = blockArgs.appeal_to || 'u';
  element.innerHTML  = '<p>Hello, ' + appealTo + '!</p>';
};