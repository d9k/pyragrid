'use strict';

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

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

pyragrid.blockConstructors = {};
pyragrid.afterTemplateRenderHandlers = {};

// define global function: get list of values without keys from object
window.objectValues = function (obj) {
  var values = [];
  for (var key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      values.push(obj[key]);
      // use val
    }
  }
  return values;
};

pyragrid.blocks = {};

pyragrid.renderBlocks = function (element) {
  var nunjucksEnv = new nunjucks.Environment();

  nunjucksEnv.addGlobal('render_block', function (blockArgs) {
    if (!blockArgs.hasOwnProperty('type')) {
      throw "Block type was not set";
    }
    var blockType = blockArgs.type;

    if (pyragrid.blockConstructors.hasOwnProperty(blockType)) {
      if (!pyragrid.blocks.hasOwnProperty(blockType)) {
        pyragrid.blocks[blockType] = {
          instances: [],
          maxId: 0
        };
      }

      pyragrid.blocks[blockType].maxId += 1;
      var newBlockId = 'block_' + blockType + '_' + pyragrid.blocks[blockType].maxId;
      pyragrid.blocks[blockType].instances.push(newBlockId);

      // first step: convert block call to html div
      // next step would be actually render block
      var dummyElement = document.createElement('div');
      dummyElement.id = newBlockId;
      dummyElement.className = 'pyragrid_block pyragrid_block_' + blockType;
      dummyElement.setAttribute('data-block-args', JSON.stringify(blockArgs));
      return new nunjucks.runtime.SafeString(dummyElement.outerHTML);
    } else {
      console.log('Warning: Block type ' + blockType + ' handler function was not set!');
    }
  });

  var renderedString = nunjucksEnv.renderString(element.innerHTML);
  element.innerHTML = renderedString;

  var blockDummyElements = document.getElementsByClassName('pyragrid_block');
  var _iteratorNormalCompletion = true;
  var _didIteratorError = false;
  var _iteratorError = undefined;

  try {
    for (var _iterator = blockDummyElements[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
      var dummyElement = _step.value;

      var blockArgs = dummyElement.getAttribute('data-block-args');
      if (typeof blockArgs !== 'string') {
        console.log('Warning: block dummy (div with id ' + dummyElement.id + ') has no data-block-args argument');
        return;
      }
      // TODO JSON parse error handling?
      blockArgs = JSON.parse(blockArgs);
      // blockArgs.id = currentElement.id;
      blockArgs.element = dummyElement;
      pyragrid.blockConstructors[blockArgs.type](blockArgs);
    }

    //TODO pyragrid.blockConstructors[blockType](blockParams);
  } catch (err) {
    _didIteratorError = true;
    _iteratorError = err;
  } finally {
    try {
      if (!_iteratorNormalCompletion && _iterator.return) {
        _iterator.return();
      }
    } finally {
      if (_didIteratorError) {
        throw _iteratorError;
      }
    }
  }
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

pyragrid.onRecreateStore.updateRecreateCountMixin = function (snapshot) {
  snapshot.storeRecreateCount += 1;
};

pyragrid.recreateStore = function (modifySnapshotCallback) {

  pyragrid.StoreType = mobxStateTree.types.compose.apply(null, ['Store'].concat(_toConsumableArray(objectValues(pyragrid.storeTypeMixins))));

  var snapshot = {};
  if (typeof pyragrid.store !== 'undefined') {
    snapshot = mobxStateTree.getSnapshot(pyragrid.store);
  }
  // snapshot is read only, need create writeable clone
  var snapshotCopy = _.cloneDeep(snapshot);

  if (typeof modifySnapshotCallback === 'function') {
    modifySnapshotCallback(snapshotCopy);
  }

  objectValues(pyragrid.onRecreateStore).forEach(function (onRecreateStoreCallback) {
    onRecreateStoreCallback(snapshotCopy);
  });

  pyragrid.store = pyragrid.StoreType.create(snapshotCopy);
  mobxStateTree.unprotect(pyragrid.store);
};

pyragrid.recreateStore(function (snapshot) {
  snapshot.storeRecreateCount = 0;
});

// pyragrid.storeTypeMixins.SC2Mixin = mobxStateTree.types.model('SC2Mixin', {
//     SC2Unit: withDefault(mobxStateTree.types.string, 'lurker')
// });
//
// pyragrid.recreateStore((snapshot) => {
//   //snapshot.SC2Unit = 'marine';
// });

pyragrid.blockConstructors['hello_world'] = function (blockArgs) {
  var element = blockArgs.element;
  var appealTo = blockArgs.appeal_to || 'u';
  element.innerHTML = '<p class="helloWorldBlock">Hello, ' + appealTo + '!</p>';
};