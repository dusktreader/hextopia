import sqlparse


def sql_pretty_print(sql):
    return sqlparse.format(sql, reindent=True, keyword_case='upper')


def query_pretty_print(query, draw_box=True):
    sql = "{}\n\n{}".format(
        sql_pretty_print(str(query.statement)),
        "with bind params: {}".format(query.statement.compile().params),
    )
    if draw_box:
        sql = enboxify(sql, vspace=1, boxchar='.', hspace=2)
    return sql


def enboxify(text, boxchar='*', hspace=1, vspace=0):
    if len(boxchar) > 1:
        raise Exception("boxchar must be a single character")
    if hspace < 0:
        raise Exception("hspace must be 0 or greater")
    if vspace < 0:
        raise Exception("vspace must be 0 or greater")
    lines = [''] * vspace + text.split('\n') + [''] * vspace
    box_width = max([len(l) for l in lines]) + 2 + hspace * 2
    newlines = [boxchar * box_width]
    for line in lines:
        newlines += ["{bc}{bs}{line}{spacer}{bs}{bc}".format(
            bc=boxchar,
            line=line,
            spacer=' ' * (box_width - len(line) - 2 - hspace * 2),
            bs=' ' * hspace,
        )]
    newlines += [boxchar * box_width]
    return '\n'.join(newlines)


class classproperty(property):  # noqa
    """
    This defines a decorator that can be used to describe a read-only property
    that is attached to the class itself instead of an instance.
    """

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
