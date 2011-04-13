def xml_tag(tag, contents, header=False):
    return "%s<%s>%s</%s>" % ('<?xml version="1.0" encoding="utf-8"?>' if header else '', tag, contents, tag)
