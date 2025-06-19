#include "os.h"

int isValid(uint64_t entry)
{
    return entry & 1;
}

void page_table_update(uint64_t pt, uint64_t vpn, uint64_t ppn)
{
    uint64_t* ptable = (uint64_t*)phys_to_virt(pt << 12);
    int entryIdx;

    for(int i=4; i>0; i--) {
        entryIdx = (vpn >> (i*9)) & 0x1FF;
        if(!isValid(ptable[entryIdx])) {
            ptable[entryIdx] = (alloc_page_frame() << 12) + 1;
        }
        ptable = (uint64_t*)phys_to_virt(ptable[entryIdx] - 1);
    }

    entryIdx = vpn & 0x1FF;
    if(ppn == NO_MAPPING) {
        ptable[entryIdx] = 0;
    } else {
        ptable[entryIdx] = (ppn << 12) + 1;
    }
    return;
}

uint64_t page_table_query(uint64_t pt, uint64_t vpn)
{
    uint64_t* ptable = (uint64_t*)phys_to_virt(pt << 12);
    int entryIdx;

    for(int i=4; i>0; i--) {
        entryIdx = (vpn >> (i*9)) & 0x1FF;
        if(!isValid(ptable[entryIdx])) {
            return NO_MAPPING;
        }
        ptable = (uint64_t*)phys_to_virt(ptable[entryIdx] - 1);
    }

    entryIdx = vpn & 0x1FF;
    if(!isValid(ptable[entryIdx])) {
        return NO_MAPPING;
    }
    else {
        return ptable[entryIdx] >> 12;
    }
}

/*
Resources:
Course lectures and slides - Virtual Memory (Hardware)
https://www.rapidtables.com/convert/number/binary-to-hex.html

Collaborations:
Answered a few questions about vpn and indexing for: Tal Dotan, Merav Gilboa, Nadav Fuchs(https://moodle.tau.ac.il/mod/forum/discuss.php?d=14808).
*/