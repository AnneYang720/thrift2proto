from proto_schema_parser import ast
from ptsd.ast import Field
from ptsd.ast import List, Map, Set  # Container types

from .common import basicTypeConverter, isBasicType


def GenMessageFromStruct(struct):
    message = ast.Message(name=struct.name, elements=[])
    for i, field in enumerate(struct.fields):
        ele = GenElements(i + 1, field.name, field.type)
        message.elements.extend(ele)
    return message


def GenMessageFromType(name, type):
    if isinstance(type, Map):
        message_name = str(name) + '_map'
        elements = GenElements(1, message_name + "_e", type)
        message = ast.Message(name=message_name, elements=elements)

    elif isinstance(type, List):
        message_name = str(name) + '_list'
        elements = GenElements(1, message_name + "_e", type)
        message = ast.Message(name=message_name, elements=elements)

    elif isinstance(type, Set):
        message_name = str(name) + '_set'
        elements = GenElements(1, message_name + "_e", type)
        message = ast.Message(name=message_name, elements=elements)

    else:
        return str(type), None

    return message_name, message


def GenElements(i, field_name, field_type) -> [Field]:
    if isBasicType(field_type):
        t = basicTypeConverter(field_type)
        return [GenBasicField(field_name, i, t)]

    if isinstance(field_type, Map):
        if not isBasicType(field_type.key_type):
            raise Exception("map key type must be a basic type")
        if isBasicType(field_type.value_type):
            return [
                GenMapField(
                    field_name,
                    i,
                    basicTypeConverter(field_type.key_type),
                    basicTypeConverter(field_type.value_type),
                )
            ]

        elements = []
        key_type = ""
        value_type = ""
        if not isBasicType(field_type.key_type):
            key_type, message = GenMessageFromType(field_name, field_type.key_type)
            elements.append(message)
        else:
            key_type = basicTypeConverter(field_type.key_type)

        if not isBasicType(field_type.value_type):
            value_type, message = GenMessageFromType(field_name, field_type.value_type)
            elements.append(message)
        else:
            value_type = basicTypeConverter(field_type.value_type)

        elements.append(GenMapField(field_name, i, key_type, value_type))
        return elements

    if isinstance(field_type, List):
        if isBasicType(field_type.value_type):
            return [
                GenListField(field_name, i, basicTypeConverter(field_type.value_type))
            ]

        elements = []
        value_type, message = GenMessageFromType(field_name, field_type.value_type)
        elements.append(message)
        elements.append(GenListField(field_name, i, value_type))
        return elements

    if isinstance(field_type, Set):
        if not isBasicType(field_type.value_type):
            raise Exception("set value type must be a basic type")

        return [GenSetField(field_name, i, basicTypeConverter(field_type.value_type))]

    return [GenBasicField(field_name, i, str(field_type))]


def GenBasicField(name, number, type):
    return ast.Field(name=name, number=number, type=type)


def GenMapField(name, number, key_type, value_type):
    return ast.MapField(
        name=name, number=number, key_type=key_type, value_type=value_type
    )


def GenListField(name, number, type):
    return ast.Field(
        name=name, number=number, type=type, cardinality=ast.FieldCardinality.REPEATED
    )


def GenSetField(name, number, type):
    return ast.MapField(name=name, number=number, key_type=type, value_type="bool")
