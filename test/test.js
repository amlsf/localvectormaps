var things = '{"dict": "hello"}';

var jsObject  = JSON.parse(things);

console.log(jsObject);
console.log(jsObject["dict"]);


file = fopen('CAneighborhoods.txt', 0);
str = fread(file);