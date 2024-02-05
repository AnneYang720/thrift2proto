# thrift2proto

This is a simple python script to convert thrift files to protobuf files. I made proper handling for some corner instances I met.

## Requirements

This project is based on some great work:
- [proto_schema_parser](https://github.com/recap-build/proto-schema-parser)
- [ptcdt](https://github.com/vtatai/ptcdt)
- [ptsd](https://github.com/wickman/ptsd)

## Usage

```bash
$ python main.py -i your_file_path -o output_file_path
```

## Features
- Only thrift supports **set** type. It's converted to **map** because I'm using this tool to generate Golang code.
```
struct DemoStruct1 {
    1: set<i64> uid
}

message DemoStruct1 {
    map<int64, bool> uid = 1;
}
```

- Except for basic type convertion, the nested list/set/map in thrift struct is supported.
```
struct DemoStruct2 {
    1: list<map<string,set<string>>> result
}

message DemoStruct2 {
    message result_map {
        message result_map_e_set {
            map<string, bool> result_map_e_set_e = 1;
        }
        map<string, result_map_e_set> result_map_e = 1;
    }
    repeated result_map result = 1;
}
```

- Multiple request params are combined to a new message for proto.
```
service DemoService {
    DemoStruct2 GetStruct(1: i64 num, 2: DemoStruct1 struct1)
}

service DemoService {
    rpc GetStruct (GetStructReq) returns (DemoStruct2);
}
message GetStructReq {
    int64 num = 1;
    DemoStruct1 struct1 = 2;
}
```

- The _extend_ of thrift service is ignored because it's not supported in proto3.

- _void_ in thrift service is converted to _google.protobuf.Empty_ in proto3.


## Note
- The generation of proto is **proto3**, so optional and required are not kept.
- _proto_schema_parser_ doesn't support the parser and generator of service type yet, but I already submitted a [PR](https://github.com/recap-build/proto-schema-parser/pull/11).