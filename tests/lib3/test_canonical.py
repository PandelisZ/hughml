
import hughml, canonical

def test_canonical_scanner(canonical_filename, verbose=False):
    data = open(canonical_filename, 'rb').read()
    tokens = list(hughml.canonical_scan(data))
    assert tokens, tokens
    if verbose:
        for token in tokens:
            print(token)

test_canonical_scanner.unittest = ['.canonical']

def test_canonical_parser(canonical_filename, verbose=False):
    data = open(canonical_filename, 'rb').read()
    events = list(hughml.canonical_parse(data))
    assert events, events
    if verbose:
        for event in events:
            print(event)

test_canonical_parser.unittest = ['.canonical']

def test_canonical_error(data_filename, canonical_filename, verbose=False):
    data = open(data_filename, 'rb').read()
    try:
        output = list(hughml.canonical_load_all(data))
    except hughml.hughmlError as exc:
        if verbose:
            print(exc)
    else:
        raise AssertionError("expected an exception")

test_canonical_error.unittest = ['.data', '.canonical']
test_canonical_error.skip = ['.empty']

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())

