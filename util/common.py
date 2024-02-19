from proto_schema_parser import ast
from ptsd.ast import Map, Set, List  # Container types
from ptsd.ast import I16, I32, I64, Binary, Bool, Byte, Double, String  # Basic types


def GenEnum(enum):
    enumvalue = ast.Enum(name=enum.name)
    for value in enum.values:
        ele = ast.EnumValue(name=value.name, number=value.tag)
        enumvalue.elements.append(ele)
    return enumvalue


def GenConst(name, const):
    return ast.Enum(
        name=name, elements=[ast.EnumValue(name=const.name, number=const.value)]
    )


def GenPackageFromNamespace(namespace):
    return ast.Package(name=namespace.name)


def GenOptionFromNamespace(namespace):
    if namespace.language_id not in ["go", "java", "php"]:
        raise NotImplementedError(
            f"Unsupported namespace language {namespace.language_id}"
        )

    if namespace.language_id == "py":
        return

    return ast.Option(name=namespace.language_id + "_package", value=namespace.name)


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


def isContainerType(input):
    if isinstance(input, Map) or isinstance(input, Set) or isinstance(input, List):
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
