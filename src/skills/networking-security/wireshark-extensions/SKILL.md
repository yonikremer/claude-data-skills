---
name: wireshark-extensions
description: Use when developing custom Wireshark protocol dissectors using Lua. Ideal for reverse engineering custom protocols, network debugging, and packet analysis automation.
---

# Wireshark Extensions (Lua Dissectors)

Wireshark can be extended using Lua to parse custom or proprietary network protocols. These extensions are called "
dissectors."

## Core Concepts

- **Proto**: The object representing your custom protocol.
- **ProtoField**: Definitions for individual fields within the protocol (e.g., ID, length, data).
- **Dissector**: The core function that receives a raw byte buffer and maps it to fields.
- **DissectorTable**: A way to register your protocol on specific ports (e.g., UDP port 12345).

## Workflow: Building a Dissector

1. **Define Protocol**: Create a new `Proto` object.
2. **Define Fields**: Identify each piece of data in the packet and create `ProtoField` objects.
3. **Implement Dissector**: Write a function that uses the `buffer` to populate fields in the protocol tree.
4. **Register**: Tell Wireshark which traffic should be handled by your dissector.

## Quick Start: The "Hello World" Dissector

```lua
local my_proto = Proto("hello", "Hello Protocol")
local f_id = ProtoField.uint16("hello.id", "ID", base.HEX)

my_proto.fields = { f_id }

function my_proto.dissector(buffer, pinfo, tree)
    pinfo.cols.protocol = "HELLO"
    local subtree = tree:add(my_proto, buffer(), "Hello Protocol Data")
    subtree:add(f_id, buffer(0, 2))
end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(9999, my_proto)
```

## Reference Materials

- **Boilerplate Template**: See [lua-dissector-template.lua](references/lua-dissector-template.lua) for a complete
  starting point.
- **Field Types & Displays**: See [proto-field-types.md](references/proto-field-types.md) for a list of all available
  data types (uint, string, ipv4, etc.).

## Strict Idioms

- **Tvb Range**: Always use `buffer(offset, length)` to access data safely.
- **Column Updates**: Always set `pinfo.cols.protocol` so the packet list shows your protocol name.
- **Guard Lengths**: Check `buffer:len()` before dissecting to avoid "Short Header" errors.

## Common Pitfalls

- **Incorrect Bit Order**: Lua dissectors default to big-endian. Use `le_uint16()` or similar if your protocol is
  little-endian.
- **Global Pollution**: Always use `local` for variables within your dissector to avoid conflicts.
- **Missing Registration**: If your dissector isn't showing up, ensure it's registered in a `DissectorTable`.
