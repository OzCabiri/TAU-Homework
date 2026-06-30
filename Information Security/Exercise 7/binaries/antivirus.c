#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <dlfcn.h>

#include "validator.h"

#define LOG(fmt, ...) printf(fmt "\n", ##__VA_ARGS__)
#define SLEEP_TIME    10

void load_live_patch(char* path)
{
    void* handle = dlopen(path, RTLD_LAZY);
    if (handle == NULL) {
        LOG("failed loading the live-patch: %s", path);
    }
}

int is_directory(char* path)
{
    struct stat st;

    if (stat(path, &st) == -1) {
        perror("stat");
        return 0;
    }

    return S_ISDIR(st.st_mode);
}

void scan_directory(char* root)
{
    DIR*   dir;
    struct dirent* ent;
    char   path[1024] = {0};

    LOG("scanning %s", root);

    LOG("opening directory");
    if ((dir = opendir(root)) == NULL) {
        perror("opendir");
        goto end;
    }

    LOG("reading directory");
    while ((ent = readdir(dir)) != NULL) {

        if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0) {
            continue;
        }

        snprintf(path, sizeof(path), "%s/%s", root, ent->d_name);
        LOG("got %s", path);

        if (is_directory(path)) {
            scan_directory(path);
        }
        else if (check_if_virus(path)) {
            LOG("\x1b[31mVIRUS DETECTED: %s\x1b[0m", path);
        }
        else if (check_if_live_patch(path)) {
            LOG("found a live-patch: %s", path);
            load_live_patch(path);
        }

    }

close_dir:
    closedir(dir);
end:
    return;
}

int main(int argc, char* argv[])
{
    if (argc < 2) {
        printf("USAGE: %s <directory>\n", argv[0]);
        return -1;
    }

    while (1) {

        scan_directory(argv[1]);

        LOG("sleeping %d seconds", SLEEP_TIME);
        sleep(SLEEP_TIME);

    }

    return 0;
}
