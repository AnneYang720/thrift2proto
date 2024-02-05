from proto_schema_parser import ast


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
