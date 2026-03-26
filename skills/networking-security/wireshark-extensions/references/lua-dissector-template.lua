-- Wireshark Lua Dissector Template
-- Documentation: https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm_modules.html

-- 1. Declare the protocol
local myproto = Proto("myproto", "My Protocol Name")

-- 2. Define protocol fields
-- Field types: uint8, uint16, uint32, string, ipv4, etc.
local pf_type = ProtoField.uint8("myproto.type", "Message Type", base.DEC)
local pf_data = ProtoField.string("myproto.data", "Data")

myproto.fields = { pf_type, pf_data }

-- 3. The main dissector function
function myproto.dissector(buffer, pinfo, tree)
    -- Check buffer length
    if buffer:len() == 0 then return end

    -- Update column display
    pinfo.cols.protocol = "MYPROTO"

    -- Add to protocol tree
    local subtree = tree:add(myproto, buffer(), "My Protocol Data")

    -- Add fields
    -- buffer(offset, length)
    subtree:add(pf_type, buffer(0, 1))
    subtree:add(pf_data, buffer(1))
end

-- 4. Register the dissector
-- Common ports: tcp_dissector_table, udp_dissector_table
local udp_port = DissectorTable.get("udp.port")
udp_port:add(12345, myproto)
