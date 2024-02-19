import argparse

from proto_schema_parser import ast
from proto_schema_parser.generator import Generator
from ptcdt.thrift_parser import MappedAST

from util import common as util_common
from util import service as util_service
from util import struct as util_struct


def Thrift2Proto(input_file, output_file):
    mapped = MappedAST.from_file(input_file)

    output = ast.File()
    output.syntax = "proto3"
    output.file_elements = []

    # const
    if len(mapped.consts) > 0:
        raise NotImplementedError("Consts are not supported in proto3")

    # typedef
    if len(mapped.typedefs) > 0:
        raise NotImplementedError("Typedefs are not supported in proto3")

    # namespace
    if len(mapped.namespaces) == 1:
        file_element = util_common.GenPackageFromNamespace(mapped.namespaces[0])
    else:
        for v in mapped.namespaces:
            file_element = util_common.GenOptionFromNamespace(v)
            if not file_element:
                continue
            output.file_elements.append(file_element)

    # enum
    for _, v in mapped.enums.items():
        file_element = util_common.GenEnum(v)
        output.file_elements.append(file_element)

    # struct
    for _, v in mapped.structs.items():
        file_element = util_struct.GenMessageFromStruct(v)
        output.file_elements.append(file_element)

    # exception
    for _, v in mapped.exceptions.items():
        file_element = util_struct.GenMessageFromStruct(v)
        output.file_elements.append(file_element)

    # service
    for _, v in mapped.services.items():
        file_element, gen_elements, gen_import = util_service.GenServiceFromService(v)
        output.file_elements.append(file_element)
        output.file_elements.extend(gen_elements)
        if gen_import:
            output.file_elements.insert(0, gen_import)

    proto = Generator().generate(output)
    with open(output_file, "w") as f:
        f.write(proto)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", type=str, help="input filename", default="./example/tmp.thrift"
    )
    parser.add_argument(
        "-o", type=str, help="output filename", default="./example/tmp.proto"
    )
    args = parser.parse_args()
    Thrift2Proto(args.i, args.o)
