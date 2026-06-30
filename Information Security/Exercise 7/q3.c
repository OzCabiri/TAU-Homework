#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid = 0x1234567a;
void* got_address = (void*)0x1234567b;
void* alt_address = (void*)0x1234567c;

int main() {
    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {
        perror("attach");
        return 1;
    }
    
    int status;
    waitpid(pid, &status, 0);
    if (WIFEXITED(status)) {return 1;}
    
    if (ptrace(PTRACE_POKEDATA, pid, got_address, alt_address) == -1) {
        perror("poke");
        ptrace(PTRACE_DETACH, pid, NULL, NULL);
        return 1;
    }
    
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {
        perror("detach");
        return 1;
    }
    
    return 0;
}
