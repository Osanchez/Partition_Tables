"""
Data structures for the DOS partition table.

Byte range		Description                     Essential
0-445			Boot Code                       No
446-461			Partition Table Entry #1        Yes
462-477			Partition Table Enrty #2        Yes
478-493			Partition Table Enrty #3        Yes
494-509			Partition Table Enrty #4        Yes
510-511			Signature value (0xAA55)        No


Data structure for DOS partition entries.

Byte Range      Description                     Essential
0-0             Bootable Flag                   No
1-3             Starting CHS Address            Yes
4-4             Partition Type (see table 5.3)  No
5-7             Ending CHS Address              Yes
8-11            Starting LBA Address            Yes
12-15           Size in Sectors                 Yes
"""

import struct
import uuid

import binascii

DOS_PARTITIONS = {
    0x00: "Empty",
    0x01: "FAT12, CHS",
    0x04: "FAT16, 16-32 MB, CHS",
    0x05: "Microsoft Extended, CHS",
    0x06: "FAT16, 32 MB-2GB, CHS",
    0x07: "NTFS",
    0x0b: "FAT32, CHS",
    0x0c: "FAT32, LBA",
    0x0e: "FAT16, 32 MB-2GB, LBA",
    0x0f: "Microsoft Extended, LBA",
    0x11: "Hidden Fat12, CHS",
    0x14: "Hidden FAT16, 16-32 MB, CHS",
    0x16: "Hidden FAT16, 32 MB-2GB, CHS",
    0x1b: "Hidden FAT32, CHS",
    0x1c: "Hidden FAT32, LBA",
    0x1e: "Hidden FAT16, 32 MB-2GB, LBA",
    0x42: "Microsoft MBR, Dynamic Disk",
    0x82: "Solaris x86 -or- Linux Swap",
    0x83: "Linux",
    0x84: "Hibernation",
    0x85: "Linux Extended",
    0x86: "NTFS Volume Set",
    0x87: "NTFS Volume SET",
    0xa0: "Hibernation",
    0xa1: "Hibernation",
    0xa5: "FreeBSD",
    0xa6: "OpenBSD",
    0xa8: "Mac OSX",
    0xa9: "NetBSD",
    0xab: "Mac OSX Boot",
    0xb7: "BSDI",
    0xb8: "BSDI swap",
    0xdb: "Recovery Partition",
    0xde: "Dell Diagnostic Partition",
    0xee: "EFI GPT Disk",
    0xef: "EFI System Partition",
    0xfb: "Vmware File System",
    0xfc: "Vmware swap",
}


def parse_mbr(mbr_bytes):
    parsed_data = []
    start_byte = 446
    data = mbr_bytes[start_byte:]
    number_sectors = 4

    for x in range(number_sectors):
        partition_entries = {}
        sector = data

        partition_type = struct.unpack('<B', sector[4:5])[0]
        partition_entries["type"] = hex(partition_type)

        lba_first = struct.unpack("<I", sector[8:12])[0]
        partition_entries["start"] = lba_first

        number_partitions = struct.unpack("<I", sector[12:16])[0]
        partition_entries["end"] = lba_first + number_partitions - 1

        partition_number = x
        partition_entries["number"] = partition_number

        if partition_type != 0:
            parsed_data.append(partition_entries)

        start_byte += 16
        data = mbr_bytes[start_byte:]

    return parsed_data


def parse_gpt(gpt_file, sector_size=512):

    gpt_entries = []
    gpt_file.seek(sector_size)
    gpt_header = gpt_file.read(sector_size)

    table_start = struct.unpack('<Q', gpt_header[72:80])[0]
    number_entries = struct.unpack('<I', gpt_header[80:84])[0]
    entry_size = struct.unpack('<I', gpt_header[84:88])[0]

    gpt_file.seek(table_start * sector_size)
    partitions = gpt_file.read(number_entries * entry_size)

    for x in range(number_entries):
        entry = {}
        entry_offset = x * entry_size
        uuid_type = uuid.UUID(bytes_le=partitions[entry_offset:entry_offset + 16])

        if uuid_type != uuid.UUID(int=0):
            entry['start'] = struct.unpack('<Q', partitions[entry_offset + 32:entry_offset + 40])[0]
            entry['end'] = struct.unpack('<Q', partitions[entry_offset + 40:entry_offset + 48])[0]
            entry['number'] = x
            entry['name'] = partitions[entry_offset + 56:entry_offset + 128].decode('utf-16-le').split('\x00')[0]
            entry['type'] = uuid_type
            gpt_entries.append(entry)

    return gpt_entries


def main():
    with open("usb-mbr.dd", 'rb') as f:
        read_bytes = f.read()
    print(parse_mbr(read_bytes))

    with open("disk-image.dd", 'rb') as f:
        print(parse_gpt(f, 512))

if __name__ == "__main__":
    main()

