import inspect


def foo(a, b=0, *c, d, e=1, **f):
    pass

ff = inspect.signature(foo)

print("inspect.signature（fn)是: %s" % ff)
print("inspect.signature（fn)的类型：%s" % (type(ff)))
print("\n")

pp = ff.parameters
print("signature.parameters属性是: %s" % pp)
print("signature.parameters属性的类型是: %s" % type(pp))
print("\n")

for key, value in pp.items():
    print('key: {}, value: {}'.format(key, value))
    print('kind: {}, default: {}'.format(value.kind, value.default))
