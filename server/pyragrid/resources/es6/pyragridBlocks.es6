if (typeof window.pyragrid === 'undefined'){
  window.pyragrid = {};
}

pyragrid.renderBlocks = function(element) {
  let findTextNodes = function(element, onTextNode){
    if (element.tagName === "SCRIPT"){
      return;
    }

    let childNodes = element.childNodes;
    for (let i = 0; i < childNodes.length; i++){
      let childNode = childNodes[i];
      if (childNode.nodeType === Node.TEXT_NODE){
        onTextNode(childNode);
      } else if (childNode.nodeType === Node.ELEMENT_NODE){
        findTextNodes(childNode, onTextNode);
      } else {
        console.log('nodeType:' + childNode.nodeType);
      }
    }
  };

  findTextNodes(element, function (textNode) {
    console.log(textNode.textContent);
  })
};
