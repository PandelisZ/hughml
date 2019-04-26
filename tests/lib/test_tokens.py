
import hughml
import pprint

# Tokens mnemonic:
# directive:            %
# document_start:       ---
# document_end:         ...
# alias:                *
# anchor:               &
# tag:                  !
# scalar                _
# block_sequence_start: [[
# block_mapping_start:  {{
# block_end:            ]}
# flow_sequence_start:  [
# flow_sequence_end:    ]
# flow_mapping_start:   {
# flow_mapping_end:     }
# entry:                ,
# key:                  ?
# value:                :

_replaces = {
    hughml.DirectiveToken: '%',
    hughml.DocumentStartToken: '---',
    hughml.DocumentEndToken: '...',
    hughml.AliasToken: '*',
    hughml.AnchorToken: '&',
    hughml.TagToken: '!',
    hughml.ScalarToken: '_',
    hughml.BlockSequenceStartToken: '[[',
    hughml.BlockMappingStartToken: '{{',
    hughml.BlockEndToken: ']}',
    hughml.FlowSequenceStartToken: '[',
    hughml.FlowSequenceEndToken: ']',
    hughml.FlowMappingStartToken: '{',
    hughml.FlowMappingEndToken: '}',
    hughml.BlockEntryToken: ',',
    hughml.FlowEntryToken: ',',
    hughml.KeyToken: '?',
    hughml.ValueToken: ':',
}

def test_tokens(data_filename, tokens_filename, verbose=False):
    tokens1 = []
    tokens2 = open(tokens_filename, 'rb').read().split()
    try:
        for token in hughml.scan(open(data_filename, 'rb')):
            if not isinstance(token, (hughml.StreamStartToken, hughml.StreamEndToken)):
                tokens1.append(_replaces[token.__class__])
    finally:
        if verbose:
            print "TOKENS1:", ' '.join(tokens1)
            print "TOKENS2:", ' '.join(tokens2)
    assert len(tokens1) == len(tokens2), (tokens1, tokens2)
    for token1, token2 in zip(tokens1, tokens2):
        assert token1 == token2, (token1, token2)

test_tokens.unittest = ['.data', '.tokens']

def test_scanner(data_filename, canonical_filename, verbose=False):
    for filename in [data_filename, canonical_filename]:
        tokens = []
        try:
            for token in hughml.scan(open(filename, 'rb')):
                tokens.append(token.__class__.__name__)
        finally:
            if verbose:
                pprint.pprint(tokens)

test_scanner.unittest = ['.data', '.canonical']

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())

