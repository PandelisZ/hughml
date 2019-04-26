
cdef extern from "_hughml.h":

    void malloc(int l)
    void memcpy(char *d, char *s, int l)
    int strlen(char *s)
    int PyString_CheckExact(object o)
    int PyUnicode_CheckExact(object o)
    char *PyString_AS_STRING(object o)
    int PyString_GET_SIZE(object o)
    object PyString_FromStringAndSize(char *v, int l)
    object PyUnicode_FromString(char *u)
    object PyUnicode_DecodeUTF8(char *u, int s, char *e)
    object PyUnicode_AsUTF8String(object o)
    int PY_MAJOR_VERSION

    ctypedef enum:
        SIZEOF_VOID_P
    ctypedef enum hughml_encoding_t:
        hughml_ANY_ENCODING
        hughml_UTF8_ENCODING
        hughml_UTF16LE_ENCODING
        hughml_UTF16BE_ENCODING
    ctypedef enum hughml_break_t:
        hughml_ANY_BREAK
        hughml_CR_BREAK
        hughml_LN_BREAK
        hughml_CRLN_BREAK
    ctypedef enum hughml_error_type_t:
        hughml_NO_ERROR
        hughml_MEMORY_ERROR
        hughml_READER_ERROR
        hughml_SCANNER_ERROR
        hughml_PARSER_ERROR
        hughml_WRITER_ERROR
        hughml_EMITTER_ERROR
    ctypedef enum hughml_scalar_style_t:
        hughml_ANY_SCALAR_STYLE
        hughml_PLAIN_SCALAR_STYLE
        hughml_SINGLE_QUOTED_SCALAR_STYLE
        hughml_DOUBLE_QUOTED_SCALAR_STYLE
        hughml_LITERAL_SCALAR_STYLE
        hughml_FOLDED_SCALAR_STYLE
    ctypedef enum hughml_sequence_style_t:
        hughml_ANY_SEQUENCE_STYLE
        hughml_BLOCK_SEQUENCE_STYLE
        hughml_FLOW_SEQUENCE_STYLE
    ctypedef enum hughml_mapping_style_t:
        hughml_ANY_MAPPING_STYLE
        hughml_BLOCK_MAPPING_STYLE
        hughml_FLOW_MAPPING_STYLE
    ctypedef enum hughml_token_type_t:
        hughml_NO_TOKEN
        hughml_STREAM_START_TOKEN
        hughml_STREAM_END_TOKEN
        hughml_VERSION_DIRECTIVE_TOKEN
        hughml_TAG_DIRECTIVE_TOKEN
        hughml_DOCUMENT_START_TOKEN
        hughml_DOCUMENT_END_TOKEN
        hughml_BLOCK_SEQUENCE_START_TOKEN
        hughml_BLOCK_MAPPING_START_TOKEN
        hughml_BLOCK_END_TOKEN
        hughml_FLOW_SEQUENCE_START_TOKEN
        hughml_FLOW_SEQUENCE_END_TOKEN
        hughml_FLOW_MAPPING_START_TOKEN
        hughml_FLOW_MAPPING_END_TOKEN
        hughml_BLOCK_ENTRY_TOKEN
        hughml_FLOW_ENTRY_TOKEN
        hughml_KEY_TOKEN
        hughml_VALUE_TOKEN
        hughml_ALIAS_TOKEN
        hughml_ANCHOR_TOKEN
        hughml_TAG_TOKEN
        hughml_SCALAR_TOKEN
    ctypedef enum hughml_event_type_t:
        hughml_NO_EVENT
        hughml_STREAM_START_EVENT
        hughml_STREAM_END_EVENT
        hughml_DOCUMENT_START_EVENT
        hughml_DOCUMENT_END_EVENT
        hughml_ALIAS_EVENT
        hughml_SCALAR_EVENT
        hughml_SEQUENCE_START_EVENT
        hughml_SEQUENCE_END_EVENT
        hughml_MAPPING_START_EVENT
        hughml_MAPPING_END_EVENT

    ctypedef int hughml_read_handler_t(void *data, char *buffer,
            size_t size, size_t *size_read) except 0

    ctypedef int hughml_write_handler_t(void *data, char *buffer,
            size_t size) except 0

    ctypedef struct hughml_mark_t:
        size_t index
        size_t line
        size_t column
    ctypedef struct hughml_version_directive_t:
        int major
        int minor
    ctypedef struct hughml_tag_directive_t:
        char *handle
        char *prefix

    ctypedef struct _hughml_token_stream_start_data_t:
        hughml_encoding_t encoding
    ctypedef struct _hughml_token_alias_data_t:
        char *value
    ctypedef struct _hughml_token_anchor_data_t:
        char *value
    ctypedef struct _hughml_token_tag_data_t:
        char *handle
        char *suffix
    ctypedef struct _hughml_token_scalar_data_t:
        char *value
        size_t length
        hughml_scalar_style_t style
    ctypedef struct _hughml_token_version_directive_data_t:
        int major
        int minor
    ctypedef struct _hughml_token_tag_directive_data_t:
        char *handle
        char *prefix
    ctypedef union _hughml_token_data_t:
        _hughml_token_stream_start_data_t stream_start
        _hughml_token_alias_data_t alias
        _hughml_token_anchor_data_t anchor
        _hughml_token_tag_data_t tag
        _hughml_token_scalar_data_t scalar
        _hughml_token_version_directive_data_t version_directive
        _hughml_token_tag_directive_data_t tag_directive
    ctypedef struct hughml_token_t:
        hughml_token_type_t type
        _hughml_token_data_t data
        hughml_mark_t start_mark
        hughml_mark_t end_mark

    ctypedef struct _hughml_event_stream_start_data_t:
        hughml_encoding_t encoding
    ctypedef struct _hughml_event_document_start_data_tag_directives_t:
        hughml_tag_directive_t *start
        hughml_tag_directive_t *end
    ctypedef struct _hughml_event_document_start_data_t:
        hughml_version_directive_t *version_directive
        _hughml_event_document_start_data_tag_directives_t tag_directives
        int implicit
    ctypedef struct _hughml_event_document_end_data_t:
        int implicit
    ctypedef struct _hughml_event_alias_data_t:
        char *anchor
    ctypedef struct _hughml_event_scalar_data_t:
        char *anchor
        char *tag
        char *value
        size_t length
        int plain_implicit
        int quoted_implicit
        hughml_scalar_style_t style
    ctypedef struct _hughml_event_sequence_start_data_t:
        char *anchor
        char *tag
        int implicit
        hughml_sequence_style_t style
    ctypedef struct _hughml_event_mapping_start_data_t:
        char *anchor
        char *tag
        int implicit
        hughml_mapping_style_t style
    ctypedef union _hughml_event_data_t:
        _hughml_event_stream_start_data_t stream_start
        _hughml_event_document_start_data_t document_start
        _hughml_event_document_end_data_t document_end
        _hughml_event_alias_data_t alias
        _hughml_event_scalar_data_t scalar
        _hughml_event_sequence_start_data_t sequence_start
        _hughml_event_mapping_start_data_t mapping_start
    ctypedef struct hughml_event_t:
        hughml_event_type_t type
        _hughml_event_data_t data
        hughml_mark_t start_mark
        hughml_mark_t end_mark

    ctypedef struct hughml_parser_t:
        hughml_error_type_t error
        char *problem
        size_t problem_offset
        int problem_value
        hughml_mark_t problem_mark
        char *context
        hughml_mark_t context_mark

    ctypedef struct hughml_emitter_t:
        hughml_error_type_t error
        char *problem

    char *hughml_get_version_string()
    void hughml_get_version(int *major, int *minor, int *patch)

    void hughml_token_delete(hughml_token_t *token)

    int hughml_stream_start_event_initialize(hughml_event_t *event,
            hughml_encoding_t encoding)
    int hughml_stream_end_event_initialize(hughml_event_t *event)
    int hughml_document_start_event_initialize(hughml_event_t *event,
            hughml_version_directive_t *version_directive,
            hughml_tag_directive_t *tag_directives_start,
            hughml_tag_directive_t *tag_directives_end,
            int implicit)
    int hughml_document_end_event_initialize(hughml_event_t *event,
            int implicit)
    int hughml_alias_event_initialize(hughml_event_t *event, char *anchor)
    int hughml_scalar_event_initialize(hughml_event_t *event,
            char *anchor, char *tag, char *value, size_t length,
            int plain_implicit, int quoted_implicit,
            hughml_scalar_style_t style)
    int hughml_sequence_start_event_initialize(hughml_event_t *event,
            char *anchor, char *tag, int implicit, hughml_sequence_style_t style)
    int hughml_sequence_end_event_initialize(hughml_event_t *event)
    int hughml_mapping_start_event_initialize(hughml_event_t *event,
            char *anchor, char *tag, int implicit, hughml_mapping_style_t style)
    int hughml_mapping_end_event_initialize(hughml_event_t *event)
    void hughml_event_delete(hughml_event_t *event)

    int hughml_parser_initialize(hughml_parser_t *parser)
    void hughml_parser_delete(hughml_parser_t *parser)
    void hughml_parser_set_input_string(hughml_parser_t *parser,
            char *input, size_t size)
    void hughml_parser_set_input(hughml_parser_t *parser,
            hughml_read_handler_t *handler, void *data)
    void hughml_parser_set_encoding(hughml_parser_t *parser,
            hughml_encoding_t encoding)
    int hughml_parser_scan(hughml_parser_t *parser, hughml_token_t *token) except *
    int hughml_parser_parse(hughml_parser_t *parser, hughml_event_t *event) except *

    int hughml_emitter_initialize(hughml_emitter_t *emitter)
    void hughml_emitter_delete(hughml_emitter_t *emitter)
    void hughml_emitter_set_output_string(hughml_emitter_t *emitter,
            char *output, size_t size, size_t *size_written)
    void hughml_emitter_set_output(hughml_emitter_t *emitter,
            hughml_write_handler_t *handler, void *data)
    void hughml_emitter_set_encoding(hughml_emitter_t *emitter,
            hughml_encoding_t encoding)
    void hughml_emitter_set_canonical(hughml_emitter_t *emitter, int canonical)
    void hughml_emitter_set_indent(hughml_emitter_t *emitter, int indent)
    void hughml_emitter_set_width(hughml_emitter_t *emitter, int width)
    void hughml_emitter_set_unicode(hughml_emitter_t *emitter, int unicode)
    void hughml_emitter_set_break(hughml_emitter_t *emitter,
            hughml_break_t line_break)
    int hughml_emitter_emit(hughml_emitter_t *emitter, hughml_event_t *event) except *
    int hughml_emitter_flush(hughml_emitter_t *emitter)

