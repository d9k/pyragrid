import colander


def exception_for_schema_field(form, field_name: str, text: str):
    """
    draw exception near specific form field
    """""
    exc = colander.Invalid(form)
    """:type : SchemaNode"""
    # field = form.get(field_name)
    field = None
    field_pos = 0
    for pos, f in enumerate(form.children):
        if f.name == field_name:
            field = f
            field_pos = pos
            break

    exc.add(colander.Invalid(field, text), field_pos)
    return exc