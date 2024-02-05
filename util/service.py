from proto_schema_parser import ast

from .struct import GenMessageFromStruct


class TmpStruct:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class TmpField:
    def __init__(self, name, type):
        self.name = name
        self.type = type


def GenServiceFromService(struct):
    service = ast.Service(name=struct.name, elements=[])
    elements = []
    gen_import = None
    for func in struct.functions:
        print(func.type)
        if len(func.arguments) > 1:
            tmpstruct = TmpStruct(name=str(func.name) + "Req", fields=[])
            for arg in func.arguments:
                tmpstruct.fields.append(TmpField(name=arg.name, type=arg.type))
            elements.append(GenMessageFromStruct(tmpstruct))
            service.elements.append(
                ast.Method(
                    name=func.name,
                    input_type=ast.MessageType(type=tmpstruct.name),
                    output_type=ast.MessageType(type=func.type),
                )
            )
        else:
            input_type = ast.MessageType(type=func.arguments[0].type)
            if func.type == "void":
                output_type = ast.MessageType(type="google.protobuf.Empty")
                gen_import = ast.Import(name="google/protobuf/empty.proto")
            else:
                output_type = ast.MessageType(type=func.type)
            ele = ast.Method(
                name=func.name, input_type=input_type, output_type=output_type
            )
            service.elements.append(ele)
    return service, elements, gen_import
