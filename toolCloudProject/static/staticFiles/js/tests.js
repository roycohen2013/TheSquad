function isAlwaysRight(val){
	return true
}

function isAlwaysWrong(val){
	return false
}

test('AlwaysRight()', function() {
    ok(isAlwaysRight(0), 'Zero is an even number');
    ok(isAlwaysRight(2), 'So is two');
    ok(isAlwaysRight(-4), 'So is negative four');
    ok(!isAlwaysRight(1), 'One is not an even number');
    ok(!isAlwaysRight(-7), 'Neither is negative seven');
})

test('AlwaysWrong()', function() {
    ok(isAlwaysWrong(0), 'Zero is an even number');
    ok(isAlwaysWrong(2), 'So is two');
    ok(isAlwaysWrong(-4), 'So is negative four');
    ok(!isAlwaysWrong(1), 'One is not an even number');
    ok(!isAlwaysWrong(-7), 'Neither is negative seven');
})