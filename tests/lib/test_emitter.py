
import hughml

def _compare_events(events1, events2):
    assert len(events1) == len(events2), (events1, events2)
    for event1, event2 in zip(events1, events2):
        assert event1.__class__ == event2.__class__, (event1, event2)
        if isinstance(event1, hughml.NodeEvent):
            assert event1.anchor == event2.anchor, (event1, event2)
        if isinstance(event1, hughml.CollectionStartEvent):
            assert event1.tag == event2.tag, (event1, event2)
        if isinstance(event1, hughml.ScalarEvent):
            if True not in event1.implicit+event2.implicit:
                assert event1.tag == event2.tag, (event1, event2)
            assert event1.value == event2.value, (event1, event2)

def test_emitter_on_data(data_filename, canonical_filename, verbose=False):
    events = list(hughml.parse(open(data_filename, 'rb')))
    output = hughml.emit(events)
    if verbose:
        print "OUTPUT:"
        print output
    new_events = list(hughml.parse(output))
    _compare_events(events, new_events)

test_emitter_on_data.unittest = ['.data', '.canonical']

def test_emitter_on_canonical(canonical_filename, verbose=False):
    events = list(hughml.parse(open(canonical_filename, 'rb')))
    for canonical in [False, True]:
        output = hughml.emit(events, canonical=canonical)
        if verbose:
            print "OUTPUT (canonical=%s):" % canonical
            print output
        new_events = list(hughml.parse(output))
        _compare_events(events, new_events)

test_emitter_on_canonical.unittest = ['.canonical']

def test_emitter_styles(data_filename, canonical_filename, verbose=False):
    for filename in [data_filename, canonical_filename]:
        events = list(hughml.parse(open(filename, 'rb')))
        for flow_style in [False, True]:
            for style in ['|', '>', '"', '\'', '']:
                styled_events = []
                for event in events:
                    if isinstance(event, hughml.ScalarEvent):
                        event = hughml.ScalarEvent(event.anchor, event.tag,
                                event.implicit, event.value, style=style)
                    elif isinstance(event, hughml.SequenceStartEvent):
                        event = hughml.SequenceStartEvent(event.anchor, event.tag,
                                event.implicit, flow_style=flow_style)
                    elif isinstance(event, hughml.MappingStartEvent):
                        event = hughml.MappingStartEvent(event.anchor, event.tag,
                                event.implicit, flow_style=flow_style)
                    styled_events.append(event)
                output = hughml.emit(styled_events)
                if verbose:
                    print "OUTPUT (filename=%r, flow_style=%r, style=%r)" % (filename, flow_style, style)
                    print output
                new_events = list(hughml.parse(output))
                _compare_events(events, new_events)

test_emitter_styles.unittest = ['.data', '.canonical']

class EventsLoader(hughml.Loader):

    def construct_event(self, node):
        if isinstance(node, hughml.ScalarNode):
            mapping = {}
        else:
            mapping = self.construct_mapping(node)
        class_name = str(node.tag[1:])+'Event'
        if class_name in ['AliasEvent', 'ScalarEvent', 'SequenceStartEvent', 'MappingStartEvent']:
            mapping.setdefault('anchor', None)
        if class_name in ['ScalarEvent', 'SequenceStartEvent', 'MappingStartEvent']:
            mapping.setdefault('tag', None)
        if class_name in ['SequenceStartEvent', 'MappingStartEvent']:
            mapping.setdefault('implicit', True)
        if class_name == 'ScalarEvent':
            mapping.setdefault('implicit', (False, True))
            mapping.setdefault('value', '')
        value = getattr(hughml, class_name)(**mapping)
        return value

EventsLoader.add_constructor(None, EventsLoader.construct_event)

def test_emitter_events(events_filename, verbose=False):
    events = list(hughml.load(open(events_filename, 'rb'), Loader=EventsLoader))
    output = hughml.emit(events)
    if verbose:
        print "OUTPUT:"
        print output
    new_events = list(hughml.parse(output))
    _compare_events(events, new_events)

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())

