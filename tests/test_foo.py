from sharedcontrolpaper.foo import return_foo

def test_foo():
    assert return_foo() == "foo"