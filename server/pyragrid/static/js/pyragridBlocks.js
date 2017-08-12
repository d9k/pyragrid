'use strict';

if (typeof window.pyragrid === 'undefined') {
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

pyragrid.renderBlocks = function (element) {
  var nunjucksEnv = new nunjucks.Environment();

  nunjucksEnv.addGlobal('render_block', function (blockType) {
    if (pyragrid.blockHandlers.hasOwnProperty(blockType)) {
      for (var _len = arguments.length, blockParams = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
        blockParams[_key - 1] = arguments[_key];
      }
      var renderedBlock = pyragrid.blockHandlers[blockType](blockParams)
      return new nunjucks.runtime.SafeString(renderedBlock);
    } else {
      console.log('Warning: block type ' + blockType + ' not found!');
    }
  });

  element.innerHTML = nunjucksEnv.renderString(element.innerHTML);
};

pyragrid.blockHandlers['hello_world'] = function (appealToWhom) {
  return '<p class="helloWorldBlock">Hello, ' + appealToWhom + '!</p>';
};