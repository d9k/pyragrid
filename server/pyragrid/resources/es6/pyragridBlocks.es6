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

pyragrid.renderBlocks = function(element) {
    let nunjucksEnv = new nunjucks.Environment();

    nunjucksEnv.addGlobal('render_block', function(blockType, ...blockParams) {
        if (pyragrid.blockHandlers.hasOwnProperty(blockType)){
          return pyragrid.blockHandlers[blockType](blockParams);
        } else {
          console.log('Warning: block type ' + blockType + ' not found!')
        }
    });

    console.log(nunjucksEnv.renderString(
      element.innerHTML
    ));
    element.innerHTML = nunjucksEnv.renderString(
      element.innerHTML
    );
};

window.withDefault = mobxStateTree.types.optional;

pyragrid.storeTypeMixins = [];

pyragrid.recreateStore = (modifyInputDataCallback) => {
  let snapshot = {};
  if (typeof pyragrid.store !== 'undefined'){
    snapshot = mobxStateTree.getSnapshot(pyragrid.store);
  }

  if (typeof modifyInputDataCallback === 'function'){
    modifyInputDataCallback(snapshot);
  }

  pyragrid.StoreType = mobxStateTree.types.compose.apply(null, ['Store', ...pyragrid.storeTypeMixins]);

  pyragrid.store = pyragrid.StoreType.create(snapshot);
};

pyragrid.storeTypeMixins.push( mobxStateTree.types.model(
  'TestMixin',
  {
    testString: withDefault(mobxStateTree.types.string, 'Test string')
  }
));

pyragrid.recreateStore((snapshot) => {
  snapshot.testString = 'Test string 2';
});

pyragrid.storeTypeMixins.push( mobxStateTree.types.model(
  'SC2Mixin',
  {
    SC2Unit: withDefault(mobxStateTree.types.string, 'lurker')
  }
));

pyragrid.recreateStore((snapshot) => {
  //snapshot.SC2Unit = 'marine';
});

pyragrid.blockHandlers['hello_world'] = function(appealToWhom){
  return '<p class="helloWorldBlock">Hello, ' + appealToWhom + '!</p>';
};