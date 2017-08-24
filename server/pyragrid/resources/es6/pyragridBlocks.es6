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

pyragrid.blockHandlers = {};
pyragrid.afterTemplateRenderHandlers = {};

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

pyragrid.renderBlocks = function(element) {
    let nunjucksEnv = new nunjucks.Environment();

    nunjucksEnv.addGlobal('render_block', function(blockType, ...blockParams) {
        if (pyragrid.blockHandlers.hasOwnProperty(blockType)){
          return pyragrid.blockHandlers[blockType](blockParams);
        } else {
          console.log('Warning: block type ' + blockType + ' not found!')
        }
    });

    // console.log(nunjucksEnv.renderString(
    //   element.innerHTML
    // ));
    element.innerHTML = nunjucksEnv.renderString(
      element.innerHTML
    );
};

window.withDefault = mobxStateTree.types.optional;

pyragrid.storeTypeMixins = {};
pyragrid.onRecreateStore = {};

pyragrid.storeTypeMixins.TestMixin = mobxStateTree.types.model('TestMixin', {
  testField: withDefault(mobxStateTree.types.string, 'test value')
});

pyragrid.storeTypeMixins.RecreateCountMixin = mobxStateTree.types.model('RecreateCountMixin', {
    storeRecreateCount: withDefault(mobxStateTree.types.number, 0)
});

pyragrid.onRecreateStore.updateRecreateCountMixin = (snapshot) => {
   snapshot.storeRecreateCount += 1;
};

pyragrid.recreateStore = (modifyInputDataCallback) => {
  let snapshot = {};
  if (typeof pyragrid.store !== 'undefined'){
    snapshot = mobxStateTree.getSnapshot(pyragrid.store);
  }

  let onRecreateStore = objectValues(pyragrid.onRecreateStore);

  pyragrid.StoreType = (mobxStateTree.types.compose.apply(null,
      ['Store', ...objectValues(pyragrid.storeTypeMixins)]
  ));
  //   .preProcessSnapshot(snapshot => ({
  //     // auto convert strings to booleans as part of preprocessing
  //     done: snapshot.done === "true" ? true : snapshot.done === "false" ? false : snapshot.done
  // }));
  pyragrid.StoreType.preProcessSnapshot( snapshot => {
  //   // if (typeof modifyInputDataCallback === 'function'){
  //   //   modifyInputDataCallback(snapshot);
  //   // }
  //   //
  //   // onRecreateStore.forEach((recreateStoreCallback) => {
  //   //   recreateStoreCallback(snapshot);
  //   // });
  //
    return snapshot;
  });

  pyragrid.store = pyragrid.StoreType.create(snapshot);
};

pyragrid.recreateStore((snapshot) => {
    snapshot.storeRecreateCount = 0;
});

pyragrid.storeTypeMixins.SC2Mixin = mobxStateTree.types.model('SC2Mixin', {
    SC2Unit: withDefault(mobxStateTree.types.string, 'lurker')
});

pyragrid.recreateStore((snapshot) => {
  //snapshot.SC2Unit = 'marine';
});

pyragrid.blockHandlers['hello_world'] = function(appealToWhom){
  return '<p class="helloWorldBlock">Hello, ' + appealToWhom + '!</p>';
};