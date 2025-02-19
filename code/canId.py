from __future__ import annotations

import dataclasses
from dataclasses import dataclass

Field = any
DeviceAddress = int
PgnId = int

def _encode_canid(src: int, pgn: int, dst: int, prio: int) -> int:
    canid = src & 0xFF
    PF = (pgn >> 8) & 0xFF
    if PF < 240:
        # PDU 1
        canid = canid | ((dst & 0xFF) << 8)
        canid = canid | (pgn << 8)
    else:
        # PDU 2
        canid = canid | pgn << 8

    canid = canid | prio << 26
    return canid

@dataclass(eq=True, frozen=True)
class CanId:
    canid: int
    prio: int
    pgn: PgnId
    dst: DeviceAddress
    src: DeviceAddress

    # Ported from https://github.com/canboat/canboatjs/blob/ed28e9ed60df0f89dfdbb2228487c7db2ae80747/lib/canId.js#L4
    @classmethod
    def parse_int(cls, id: int) -> CanId:
        prio = (id >> 26) & 0x7
        src = id & 0xFF

        pdu_format = (id >> 16) & 0xFF
        pdu_specific = (id >> 8) & 0xFF
        data_page = (id >> 24) & 1

        if pdu_format < 240:
            # PDU1 format, the pduSpecific contains the destination address.
            dst = pdu_specific
            pgn = (data_page << 16) + (pdu_format << 8)
        else:
            # PDU2 format, the destination is implied global and the PGN is extended.
            dst = 0xFF
            pgn = (data_page << 16) + (pdu_format << 8) + pdu_specific

        return CanId(
            canid=id,
            prio=prio,
            pgn=pgn,
            dst=dst,
            src=src,
        )

    @classmethod
    def parse_hex(cls, id: str) -> CanId:
        return cls.parse_int(int(id, 16))

    @classmethod
    def parse_dbc_id(cls, dbc_frame_id: int) -> CanId:
        canid = dbc_frame_id & ~(1 << 31)
        return cls.parse_int(canid)

    def get_dbc_id(self) -> int:
        return self.canid | (1 << 31)

    def replace_src(self, src: int) -> CanId:
        return self.replace(src=src)

    def replace_prio(self, prio: int) -> CanId:
        return self.replace(prio=prio)

    def replace_dst(self, dst: int) -> CanId:
        return self.replace(dst=dst)

    def replace(
        self,
        src: int | None = None,
        dst: int | None = None,
        prio: int | None = None,
        pgn: int | None = None,
    ) -> CanId:
        """
        Returns a new CanId instance based on self but with the given new attribute values and a freshly calculated
        can id based on the updated values.
        """
        if src is None:
            src = self.src
        if dst is None:
            dst = self.dst
        if prio is None:
            prio = self.prio
        if pgn is None:
            pgn = self.pgn

        new_canid = _encode_canid(
            src=src,
            pgn=pgn,
            dst=dst,
            prio=prio,
        )
        return CanId(
            canid=new_canid,
            prio=prio,
            pgn=pgn,
            dst=dst,
            src=src,
        )


print("Frame ID in hex eingeben: ")
frame_id_hex = input()
canId = CanId.parse_hex(frame_id_hex)
print(canId)
#replace_src
print("Neue Source eingeben: ")
src = input()
canId = canId.replace_src(int(src))
print(canId)
#print in hex
print(hex(canId.canid))
