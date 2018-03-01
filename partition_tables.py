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
    # FIXME: I'm pretty sure 0xdb is a recovery partition
    0xdb: "Recovery Partition",
    0xde: "Dell Diagnostic Partition",
    0xee: "EFI GPT Disk",
    0xef: "EFI System Partition",
    0xfb: "Vmware File System",
    0xfc: "Vmware swap",
    # FIXME Add flag for VirtualBox Partitions
}


def parse_mbr(mbr_bytes):
    data = mbr_bytes
    bootable_flag = struct.unpack("<B", data[0:1])[0]
    print(bootable_flag)
    start_chs_address = struct.unpack("<BH", data[1:4])[0]
    print(start_chs_address)
    partition_type = struct.unpack("<B", data[4:5])[0]
    print(partition_type)
    end_chs_address = struct.unpack("<BH", data[5:8])[0]
    print(end_chs_address)
    return data


def parse_gpt(gpt_file, sector_size=512):
    return []


def main():
    with open("usb-mbr.dd", 'rb') as f:
        read_bytes = f.read()
    parse_mbr(read_bytes)

if __name__ == "__main__":
    main()

