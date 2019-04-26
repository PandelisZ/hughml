
import hughml
import pprint

def test_implicit_resolver(data_filename, detect_filename, verbose=False):
    correct_tag = None
    node = None
    try:
        correct_tag = open(detect_filename, 'rb').read().strip()
        node = hughml.compose(open(data_filename, 'rb'))
        assert isinstance(node, hughml.SequenceNode), node
        for scalar in node.value:
            assert isinstance(scalar, hughml.ScalarNode), scalar
            assert scalar.tag == correct_tag, (scalar.tag, correct_tag)
    finally:
        if verbose:
            print "CORRECT TAG:", correct_tag
            if hasattr(node, 'value'):
                print "CHILDREN:"
                pprint.pprint(node.value)

test_implicit_resolver.unittest = ['.data', '.detect']

def _make_path_loader_and_dumper():
    global MyLoader, MyDumper

    class MyLoader(hughml.Loader):
        pass
    class MyDumper(hughml.Dumper):
        pass

    hughml.add_path_resolver(u'!root', [],
            Loader=MyLoader, Dumper=MyDumper)
    hughml.add_path_resolver(u'!root/scalar', [], str,
            Loader=MyLoader, Dumper=MyDumper)
    hughml.add_path_resolver(u'!root/key11/key12/*', ['key11', 'key12'],
            Loader=MyLoader, Dumper=MyDumper)
    hughml.add_path_resolver(u'!root/key21/1/*', ['key21', 1],
            Loader=MyLoader, Dumper=MyDumper)
    hughml.add_path_resolver(u'!root/key31/*/*/key14/map', ['key31', None, None, 'key14'], dict,
            Loader=MyLoader, Dumper=MyDumper)

    return MyLoader, MyDumper

def _convert_node(node):
    if isinstance(node, hughml.ScalarNode):
        return (node.tag, node.value)
    elif isinstance(node, hughml.SequenceNode):
        value = []
        for item in node.value:
            value.append(_convert_node(item))
        return (node.tag, value)
    elif isinstance(node, hughml.MappingNode):
        value = []
        for key, item in node.value:
            value.append((_convert_node(key), _convert_node(item)))
        return (node.tag, value)

def test_path_resolver_loader(data_filename, path_filename, verbose=False):
    _make_path_loader_and_dumper()
    nodes1 = list(hughml.compose_all(open(data_filename, 'rb').read(), Loader=MyLoader))
    nodes2 = list(hughml.compose_all(open(path_filename, 'rb').read()))
    try:
        for node1, node2 in zip(nodes1, nodes2):
            data1 = _convert_node(node1)
            data2 = _convert_node(node2)
            assert data1 == data2, (data1, data2)
    finally:
        if verbose:
            print hughml.serialize_all(nodes1)

test_path_resolver_loader.unittest = ['.data', '.path']

def test_path_resolver_dumper(data_filename, path_filename, verbose=False):
    _make_path_loader_and_dumper()
    for filename in [data_filename, path_filename]:
        output = hughml.serialize_all(hughml.compose_all(open(filename, 'rb')), Dumper=MyDumper)
        if verbose:
            print output
        nodes1 = hughml.compose_all(output)
        nodes2 = hughml.compose_all(open(data_filename, 'rb'))
        for node1, node2 in zip(nodes1, nodes2):
            data1 = _convert_node(node1)
            data2 = _convert_node(node2)
            assert data1 == data2, (data1, data2)

test_path_resolver_dumper.unittest = ['.data', '.path']

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())

