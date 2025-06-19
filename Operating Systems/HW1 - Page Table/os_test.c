#define _GNU_SOURCE

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#include <sys/mman.h>

#include "os.h"

/* 2^20 pages ought to be enough for anybody */
#define NPAGES (1024 * 1024)
#define PAGE_SIZE 4096

static char* pages[NPAGES];

uint64_t alloc_page_frame(void)
{
	static uint64_t nalloc;
	uint64_t ppn;
	void* va;

	if (nalloc == NPAGES)
		errx(1, "out of physical memory");

	/* OS memory management isn't really this simple */
	ppn = nalloc;
	nalloc++;

	va = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
	if (va == MAP_FAILED)
		err(1, "mmap failed");

	pages[ppn] = va;	
	return ppn;
}

void* phys_to_virt(uint64_t phys_addr)
{
	uint64_t ppn = (phys_addr >> 12) - 0xbaaaaaad;
	uint64_t off = phys_addr & 0xfff;
	char* va = NULL;

	if (ppn < NPAGES)
		va = pages[ppn] + off;

	return va;
}

// Test function
void test_page_table_query() {

    // Step 1: Allocate some physical pages.
    uint64_t pt = alloc_page_frame();  // Just simulate a page table base address.
    uint64_t ppn1 = alloc_page_frame();  // Allocate physical page 1.
    uint64_t ppn2 = alloc_page_frame();  // Allocate physical page 2.

    // Step 2: Test case 1 - Query unmapped vpn.
    uint64_t vpn1 = 3;  // Virtual page number 3 (unmapped).
    uint64_t result = page_table_query(pt, vpn1);
    assert(result == NO_MAPPING);  // Should return NO_MAPPING (NULL) as it is not mapped.

    // Step 3: Test case 2 - Map vpn1 to ppn1 and query.
    page_table_update(pt, vpn1, ppn1);  // Map vpn1 to ppn1
    result = page_table_query(pt, vpn1);
    assert(result == ppn1);   // Should return ppn1 as vpn1 is now mapped.

    // Step 4: Test case 3 - Query another unmapped vpn (vpn2).
    uint64_t vpn2 = 5;  // Virtual page number 5 (unmapped).
    result = page_table_query(pt, vpn2);
    assert(result == NO_MAPPING);  // Should return NO_MAPPING (NULL) as vpn2 is not mapped.

    // Step 5: Test case 4 - Map vpn2 to ppn2 and query.
    page_table_update(pt, vpn2, ppn2);  // Map vpn2 to ppn2
    result = page_table_query(pt, vpn2);
    assert(result == ppn2);   // Should return ppn2 as vpn2 is now mapped.

    // Step 6: Test case 5 - Query an unmapped vpn after unmapping it.
    page_table_update(pt, vpn1, NO_MAPPING);  // Unmap vpn1
    result = page_table_query(pt, vpn1);
    assert(result == NO_MAPPING);  // Should return NO_MAPPING (NULL) as vpn1 is unmapped.

    // Step 7: Test case 6 - Query a vpn after re-mapping.
    uint64_t ppn3 = alloc_page_frame();  // Allocate new physical page 3
    page_table_update(pt, vpn1, ppn3);  // Re-map vpn1 to ppn3
    result = page_table_query(pt, vpn1);
    assert(result == ppn3);   // Should return ppn3 as vpn1 is re-mapped.

    // Step 8: Test case 7 - Query at the upper limit of the page table size.
    uint64_t vpn_max = NPAGES - 1;  // Maximum virtual page number (last entry in the page table)
    uint64_t ppn_max = alloc_page_frame();  // Allocate a physical page for the max vpn
    page_table_update(pt, vpn_max, ppn_max);  // Map the last vpn to the max ppn
    result = page_table_query(pt, vpn_max);
    assert(result == ppn_max);  // Should return ppn_max as vpn_max is mapped.

    // Step 9: Test case 8 - Test phys_to_virt for the physical pages.
    void* virt_addr1 = phys_to_virt(ppn1 * PAGE_SIZE);  // Convert physical page 1 to virtual
    void* virt_addr2 = phys_to_virt(ppn2 * PAGE_SIZE);  // Convert physical page 2 to virtual
    void* virt_addr3 = phys_to_virt(ppn3 * PAGE_SIZE);  // Convert physical page 3 to virtual
    
    // Verify that physical addresses correctly map to some virtual addresses.
    assert(virt_addr1 != NULL);  // Should return a non-NULL pointer for valid physical page.
    assert(virt_addr2 != NULL);  // Should return a non-NULL pointer for valid physical page.
    assert(virt_addr3 != NULL);  // Should return a non-NULL pointer for valid physical page.

    printf("All test cases passed!\n");
}

int main() {
    // Run the tests
    test_page_table_query();
    return 0;
}
