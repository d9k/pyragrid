'use strict';

if (typeof window.pyragrid === 'undefined') {
  window.pyragrid = {};
}

pyragrid.renderBlocks = function (element) {
  var findTextNodes = function findTextNodes(element, onTextNode) {
    if (element.tagName === "SCRIPT") {
      return;
    }

    var childNodes = element.childNodes;
    for (var i = 0; i < childNodes.length; i++) {
      var childNode = childNodes[i];
      if (childNode.nodeType === Node.TEXT_NODE) {
        onTextNode(childNode);
      } else if (childNode.nodeType === Node.ELEMENT_NODE) {
        findTextNodes(childNode, onTextNode);
      } else {
        console.log('nodeType:' + childNode.nodeType);
      }
    }
  };

  findTextNodes(element, function (textNode) {
    console.log(textNode.textContent);
  });
};