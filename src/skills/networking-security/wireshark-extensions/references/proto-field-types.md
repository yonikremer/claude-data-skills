# Wireshark ProtoField Types

Detailed list of available `ProtoField` types and their usage in Wireshark Lua.

## Common Types

- **uint8**, **uint16**, **uint24**, **uint32**, **uint64**: Unsigned integers (specify bit length).
- **int8**, **int16**, **int32**, **int64**: Signed integers.
- **float**, **double**: Floating-point numbers.
- **string**, **stringz**: Text strings (stringz is null-terminated).
- **ipv4**, **ipv6**: IP addresses.
- **ether**: MAC addresses (Ethernet).
- **bool**: Boolean (true/false).
- **bytes**: Raw byte sequences.

## Base Displays

Use these as the third argument in `ProtoField` to control how values appear in the tree:

- `base.DEC`: Decimal (default for integers).
- `base.HEX`: Hexadecimal.
- `base.OCT`: Octal.
- `base.NONE`: No base (for strings/IPs).

## Examples

```lua
-- Unsigned 16-bit integer, displayed as Hex
local pf_id = ProtoField.uint16("proto.id", "ID", base.HEX)

-- IPv4 address
local pf_addr = ProtoField.ipv4("proto.addr", "Source Address")

-- Null-terminated string
local pf_msg = ProtoField.stringz("proto.msg", "Message")
```
