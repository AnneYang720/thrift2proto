from proto_schema_parser import ast
from ptsd.ast import Map, Set, List  # Container types
from ptsd.ast import I16, I32, I64, Binary, Bool, Byte, Double, String # Basic types


def GenMessageFromStruct(struct):
    message = ast.Message(name=struct.name, elements=[])
    for i, field in enumerate(struct.fields):
        ele = GenElements(i + 1, field.name, field.type)
        message.elements.extend(ele)
    return message


def GenMessageFromType(name, type):
    print("GenMessageFromType ", name, type)
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


def GenElements(i, field_name, field_type) -> [ast.Field]:
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
    print(name, number, type)
    return ast.Field(
        name=name, number=number, type=type, cardinality=ast.FieldCardinality.REPEATED
    )


def GenSetField(name, number, type):
    return ast.MapField(name=name, number=number, key_type=type, value_type="bool")


def isBasicType(input):
    if (
        isinstance(input, I64)
        or isinstance(input, I32)
        or isinstance(input, I16)
        or isinstance(input, Byte)
        or isinstance(input, String)
        or isinstance(input, Bool)
        or isinstance(input, Binary)
        or isinstance(input, Double)
    ):
        return True
    else:
        return False


def basicTypeConverter(input):
    if isinstance(input, I64):
        return "int64"
    elif isinstance(input, I32) or isinstance(input, I16) or isinstance(input, Byte):
        return "int32"
    elif isinstance(input, String):
        return "string"
    elif isinstance(input, Bool):
        return "bool"
    elif isinstance(input, Binary):
        return "bytes"
    elif isinstance(input, Double):
        return "double"
