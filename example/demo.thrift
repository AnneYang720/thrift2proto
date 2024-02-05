namespace go demo
namespace java demo

include "common.thrift"

struct DemoStruct1 {
    1: set<i64> uid
}

struct DemoStruct2 {
    1: list<map<string,set<string>>> result
}

service DemoService {
    DemoStruct2 GetStruct(1: i64 num, 2: DemoStruct1 struct1)
}
