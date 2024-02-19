from proto_schema_parser import ast

from .common import isBasicType, isContainerType
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
        input_type = None
        output_type = None

        if len(func.arguments) > 1:
            tmpstruct = TmpStruct(name=str(func.name) + "Req", fields=[])
            for arg in func.arguments:
                tmpstruct.fields.append(TmpField(name=arg.name, type=arg.type))
            elements.append(GenMessageFromStruct(tmpstruct))
            input_type = ast.MessageType(type=tmpstruct.name)
        else:
            if len(func.arguments) == 0:
                input_type = ast.MessageType(type="google.protobuf.Empty")
                gen_import = ast.Import(name="google/protobuf/empty.proto")
            else:
                input = func.arguments[0].type
                if isContainerType(input) or isBasicType(input):
                    tmpstruct = TmpStruct(name=str(func.name) + "Req", fields=[])
                    for arg in func.arguments:
                        tmpstruct.fields.append(TmpField(name=arg.name, type=arg.type))
                    elements.append(GenMessageFromStruct(tmpstruct))
                    input_type = ast.MessageType(type=tmpstruct.name)
                else:
                    input_type = ast.MessageType(type=func.arguments[0].type)

        if func.type == "void":
            output_type = ast.MessageType(type="google.protobuf.Empty")
            gen_import = ast.Import(name="google/protobuf/empty.proto")
        else:
            output = func.type
            if isContainerType(output) or isBasicType(output):
                tmpstruct = TmpStruct(name=str(func.name) + "Resp", fields=[])
                tmpstruct.fields.append(TmpField(name="response", type=func.type))
                elements.append(GenMessageFromStruct(tmpstruct))
                output_type = ast.MessageType(type=tmpstruct.name)
            else:
                output_type = ast.MessageType(type=func.type)

        ele = ast.Method(name=func.name, input_type=input_type, output_type=output_type)
        service.elements.append(ele)
    return service, elements, gen_import
