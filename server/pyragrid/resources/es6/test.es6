/*
 * decaffeinate suggestions:
 * DS101: Remove unnecessary use of Array.from
 * DS102: Remove unnecessary code created because of implicit returns
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
// Assignment:
let number   = 42;
const opposite = true;

// Conditions:
if (opposite) { number = -42; }

// Functions:
const square = x => x * x;

// Arrays:
const list = [1, 2, 3, 4, 5];

// Objects:
const math = {
  root:   Math.sqrt,
  square,
  cube(x) { return x * square(x); }
};

// Splats:
const race = (winner, ...runners) => print(winner, runners);

// Existence:
if (typeof elvis !== 'undefined' && elvis !== null) { alert("I knew it!"); }

// Array comprehensions:
const cubes = (Array.from(list).map((num) => math.cube(num)));