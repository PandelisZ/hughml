
import _hughml, hughml
import types, pprint

hughml.PyBaseLoader = hughml.BaseLoader
hughml.PySafeLoader = hughml.SafeLoader
hughml.PyLoader = hughml.Loader
hughml.PyBaseDumper = hughml.BaseDumper
hughml.PySafeDumper = hughml.SafeDumper
hughml.PyDumper = hughml.Dumper

old_scan = hughml.scan
def new_scan(stream, Loader=hughml.CLoader):
    return old_scan(stream, Loader)

old_parse = hughml.parse
def new_parse(stream, Loader=hughml.CLoader):
    return old_parse(stream, Loader)

old_compose = hughml.compose
def new_compose(stream, Loader=hughml.CLoader):
    return old_compose(stream, Loader)

old_compose_all = hughml.compose_all
def new_compose_all(stream, Loader=hughml.CLoader):
    return old_compose_all(stream, Loader)

old_load = hughml.load
def new_load(stream, Loader=hughml.CLoader):
    return old_load(stream, Loader)

old_load_all = hughml.load_all
def new_load_all(stream, Loader=hughml.CLoader):
    return old_load_all(stream, Loader)

old_safe_load = hughml.safe_load
def new_safe_load(stream):
    return old_load(stream, hughml.CSafeLoader)

old_safe_load_all = hughml.safe_load_all
def new_safe_load_all(stream):
    return old_load_all(stream, hughml.CSafeLoader)

old_emit = hughml.emit
def new_emit(events, stream=None, Dumper=hughml.CDumper, **kwds):
    return old_emit(events, stream, Dumper, **kwds)

old_serialize = hughml.serialize
def new_serialize(node, stream, Dumper=hughml.CDumper, **kwds):
    return old_serialize(node, stream, Dumper, **kwds)

old_serialize_all = hughml.serialize_all
def new_serialize_all(nodes, stream=None, Dumper=hughml.CDumper, **kwds):
    return old_serialize_all(nodes, stream, Dumper, **kwds)

old_dump = hughml.dump
def new_dump(data, stream=None, Dumper=hughml.CDumper, **kwds):
    return old_dump(data, stream, Dumper, **kwds)

old_dump_all = hughml.dump_all
def new_dump_all(documents, stream=None, Dumper=hughml.CDumper, **kwds):
    return old_dump_all(documents, stream, Dumper, **kwds)

old_safe_dump = hughml.safe_dump
def new_safe_dump(data, stream=None, **kwds):
    return old_dump(data, stream, hughml.CSafeDumper, **kwds)

old_safe_dump_all = hughml.safe_dump_all
def new_safe_dump_all(documents, stream=None, **kwds):
    return old_dump_all(documents, stream, hughml.CSafeDumper, **kwds)

def _set_up():
    hughml.BaseLoader = hughml.CBaseLoader
    hughml.SafeLoader = hughml.CSafeLoader
    hughml.Loader = hughml.CLoader
    hughml.BaseDumper = hughml.CBaseDumper
    hughml.SafeDumper = hughml.CSafeDumper
    hughml.Dumper = hughml.CDumper
    hughml.scan = new_scan
    hughml.parse = new_parse
    hughml.compose = new_compose
    hughml.compose_all = new_compose_all
    hughml.load = new_load
    hughml.load_all = new_load_all
    hughml.safe_load = new_safe_load
    hughml.safe_load_all = new_safe_load_all
    hughml.emit = new_emit
    hughml.serialize = new_serialize
    hughml.serialize_all = new_serialize_all
    hughml.dump = new_dump
    hughml.dump_all = new_dump_all
    hughml.safe_dump = new_safe_dump
    hughml.safe_dump_all = new_safe_dump_all

def _tear_down():
    hughml.BaseLoader = hughml.PyBaseLoader
    hughml.SafeLoader = hughml.PySafeLoader
    hughml.Loader = hughml.PyLoader
    hughml.BaseDumper = hughml.PyBaseDumper
    hughml.SafeDumper = hughml.PySafeDumper
    hughml.Dumper = hughml.PyDumper
    hughml.scan = old_scan
    hughml.parse = old_parse
    hughml.compose = old_compose
    hughml.compose_all = old_compose_all
    hughml.load = old_load
    hughml.load_all = old_load_all
    hughml.safe_load = old_safe_load
    hughml.safe_load_all = old_safe_load_all
    hughml.emit = old_emit
    hughml.serialize = old_serialize
    hughml.serialize_all = old_serialize_all
    hughml.dump = old_dump
    hughml.dump_all = old_dump_all
    hughml.safe_dump = old_safe_dump
    hughml.safe_dump_all = old_safe_dump_all

def test_c_version(verbose=False):
    if verbose:
        print(_hughml.get_version())
        print(_hughml.get_version_string())
    assert ("%s.%s.%s" % _hughml.get_version()) == _hughml.get_version_string(),    \
            (_hughml.get_version(), _hughml.get_version_string())

def _compare_scanners(py_data, c_data, verbose):
    py_tokens = list(hughml.scan(py_data, Loader=hughml.PyLoader))
    c_tokens = []
    try:
        for token in hughml.scan(c_data, Loader=hughml.CLoader):
            c_tokens.append(token)
        assert len(py_tokens) == len(c_tokens), (len(py_tokens), len(c_tokens))
        for py_token, c_token in zip(py_tokens, c_tokens):
            assert py_token.__class__ == c_token.__class__, (py_token, c_token)
            if hasattr(py_token, 'value'):
                assert py_token.value == c_token.value, (py_token, c_token)
            if isinstance(py_token, hughml.StreamEndToken):
                continue
            py_start = (py_token.start_mark.index, py_token.start_mark.line, py_token.start_mark.column)
            py_end = (py_token.end_mark.index, py_token.end_mark.line, py_token.end_mark.column)
            c_start = (c_token.start_mark.index, c_token.start_mark.line, c_token.start_mark.column)
            c_end = (c_token.end_mark.index, c_token.end_mark.line, c_token.end_mark.column)
            assert py_start == c_start, (py_start, c_start)
            assert py_end == c_end, (py_end, c_end)
    finally:
        if verbose:
            print("PY_TOKENS:")
            pprint.pprint(py_tokens)
            print("C_TOKENS:")
            pprint.pprint(c_tokens)

def test_c_scanner(data_filename, canonical_filename, verbose=False):
    _compare_scanners(open(data_filename, 'rb'),
            open(data_filename, 'rb'), verbose)
    _compare_scanners(open(data_filename, 'rb').read(),
            open(data_filename, 'rb').read(), verbose)
    _compare_scanners(open(canonical_filename, 'rb'),
            open(canonical_filename, 'rb'), verbose)
    _compare_scanners(open(canonical_filename, 'rb').read(),
            open(canonical_filename, 'rb').read(), verbose)

test_c_scanner.unittest = ['.data', '.canonical']
test_c_scanner.skip = ['.skip-ext']

def _compare_parsers(py_data, c_data, verbose):
    py_events = list(hughml.parse(py_data, Loader=hughml.PyLoader))
    c_events = []
    try:
        for event in hughml.parse(c_data, Loader=hughml.CLoader):
            c_events.append(event)
        assert len(py_events) == len(c_events), (len(py_events), len(c_events))
        for py_event, c_event in zip(py_events, c_events):
            for attribute in ['__class__', 'anchor', 'tag', 'implicit',
                                'value', 'explicit', 'version', 'tags']:
                py_value = getattr(py_event, attribute, None)
                c_value = getattr(c_event, attribute, None)
                assert py_value == c_value, (py_event, c_event, attribute)
    finally:
        if verbose:
            print("PY_EVENTS:")
            pprint.pprint(py_events)
            print("C_EVENTS:")
            pprint.pprint(c_events)

def test_c_parser(data_filename, canonical_filename, verbose=False):
    _compare_parsers(open(data_filename, 'rb'),
            open(data_filename, 'rb'), verbose)
    _compare_parsers(open(data_filename, 'rb').read(),
            open(data_filename, 'rb').read(), verbose)
    _compare_parsers(open(canonical_filename, 'rb'),
            open(canonical_filename, 'rb'), verbose)
    _compare_parsers(open(canonical_filename, 'rb').read(),
            open(canonical_filename, 'rb').read(), verbose)

test_c_parser.unittest = ['.data', '.canonical']
test_c_parser.skip = ['.skip-ext']

def _compare_emitters(data, verbose):
    events = list(hughml.parse(data, Loader=hughml.PyLoader))
    c_data = hughml.emit(events, Dumper=hughml.CDumper)
    if verbose:
        print(c_data)
    py_events = list(hughml.parse(c_data, Loader=hughml.PyLoader))
    c_events = list(hughml.parse(c_data, Loader=hughml.CLoader))
    try:
        assert len(events) == len(py_events), (len(events), len(py_events))
        assert len(events) == len(c_events), (len(events), len(c_events))
        for event, py_event, c_event in zip(events, py_events, c_events):
            for attribute in ['__class__', 'anchor', 'tag', 'implicit',
                                'value', 'explicit', 'version', 'tags']:
                value = getattr(event, attribute, None)
                py_value = getattr(py_event, attribute, None)
                c_value = getattr(c_event, attribute, None)
                if attribute == 'tag' and value in [None, '!'] \
                        and py_value in [None, '!'] and c_value in [None, '!']:
                    continue
                if attribute == 'explicit' and (py_value or c_value):
                    continue
                assert value == py_value, (event, py_event, attribute)
                assert value == c_value, (event, c_event, attribute)
    finally:
        if verbose:
            print("EVENTS:")
            pprint.pprint(events)
            print("PY_EVENTS:")
            pprint.pprint(py_events)
            print("C_EVENTS:")
            pprint.pprint(c_events)

def test_c_emitter(data_filename, canonical_filename, verbose=False):
    _compare_emitters(open(data_filename, 'rb').read(), verbose)
    _compare_emitters(open(canonical_filename, 'rb').read(), verbose)

test_c_emitter.unittest = ['.data', '.canonical']
test_c_emitter.skip = ['.skip-ext']

def wrap_ext_function(function):
    def wrapper(*args, **kwds):
        _set_up()
        try:
            function(*args, **kwds)
        finally:
            _tear_down()
    wrapper.__name__ = '%s_ext' % function.__name__
    wrapper.unittest = function.unittest
    wrapper.skip = getattr(function, 'skip', [])+['.skip-ext']
    return wrapper

def wrap_ext(collections):
    functions = []
    if not isinstance(collections, list):
        collections = [collections]
    for collection in collections:
        if not isinstance(collection, dict):
            collection = vars(collection)
        for key in sorted(collection):
            value = collection[key]
            if isinstance(value, types.FunctionType) and hasattr(value, 'unittest'):
                functions.append(wrap_ext_function(value))
    for function in functions:
        assert function.__name__ not in globals()
        globals()[function.__name__] = function

import test_tokens, test_structure, test_errors, test_resolver, test_constructor,   \
        test_emitter, test_representer, test_recursive, test_input_output
wrap_ext([test_tokens, test_structure, test_errors, test_resolver, test_constructor,
        test_emitter, test_representer, test_recursive, test_input_output])

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())

