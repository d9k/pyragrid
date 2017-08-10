"use strict";

/*
 * decaffeinate suggestions:
 * DS101: Remove unnecessary use of Array.from
 * DS102: Remove unnecessary code created because of implicit returns
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
// Assignment:
var number = 42;
var opposite = true;

// Conditions:
if (opposite) {
  number = -42;
}

// Functions:
var square = function square(x) {
  return x * x;
};

// Arrays:
var list = [1, 2, 3, 4, 5];

// Objects:
var math = {
  root: Math.sqrt,
  square: square,
  cube: function cube(x) {
    return x * square(x);
  }
};

// Splats:
var race = function race(winner) {
  for (var _len = arguments.length, runners = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
    runners[_key - 1] = arguments[_key];
  }

  return print(winner, runners);
};

// Existence:
if (typeof elvis !== 'undefined' && elvis !== null) {
  alert("I knew it!");
}

// Array comprehensions:
var cubes = Array.from(list).map(function (num) {
  return math.cube(num);
});