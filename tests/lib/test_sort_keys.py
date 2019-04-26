import hughml
import pprint
import sys

def test_sort_keys(input_filename, sorted_filename, verbose=False):
    input = open(input_filename, 'rb').read().decode('utf-8')
    sorted = open(sorted_filename, 'rb').read().decode('utf-8')
    data = hughml.load(input, Loader=hughml.FullLoader)
    dump_sorted = hughml.dump(data, default_flow_style=False, sort_keys=True)
    dump_unsorted = hughml.dump(data, default_flow_style=False, sort_keys=False)
    dump_unsorted = hughml.dump(data, default_flow_style=False, sort_keys=False, Dumper=hughml.SafeDumper)
    if verbose:
        print("INPUT:")
        print(input)
        print("DATA:")
        print(data)

    assert dump_sorted == sorted




test_sort_keys.unittest = ['.sort', '.sorted']

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())

