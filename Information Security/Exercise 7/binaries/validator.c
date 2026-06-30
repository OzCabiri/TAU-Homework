#include <stdio.h>
#include <string.h>

#include <openssl/sha.h>

#define LOG(fmt, ...) printf(fmt "\n", ##__VA_ARGS__)

char* invalid_hashes[] = {
    "\x29\x41\x71\xdb\x6b\xce\x62\x7e\x2a\x08\xe8\x2f\x1e\x9e\x86\xa0\x57\x30\x6a\x63",
    "\xa1\x6c\xb2\xde\xcc\x5b\xd4\x10\x50\x70\xbd\xf8\xd4\xf7\xcd\x3a\x3e\x5c\x59\xf2",
    "\x94\x2a\x1a\xc3\x47\xe8\xbb\x5f\xf8\x81\x13\x3d\xd7\x74\x52\x1c\xbe\x00\x91\x02",
    "\x12\x8f\x0f\xad\x71\xbe\x5b\x4f\xbd\x74\x0e\x7f\x8e\x77\xe2\x0c\x5c\x45\xba\x57",
};

char* patch_hashes[] = {
    "\xe2\x48\x50\xe2\x01\x19\x72\x92\xbc\x42\x6e\x20\x91\xbf\x85\xdf\xf2\x57\xfb\x5f"
};

int calc_hash(char* path, char hash[SHA_DIGEST_LENGTH])
{
    FILE* fp;
    int   size;
    char  buff[1024];

    SHA_CTX ctx;
    SHA1_Init(&ctx);

    if ((fp = fopen(path, "r")) == NULL) {
        perror("fopen");
        return 0;
    }

    while ((size = fread(buff, 1, sizeof(buff), fp)) != 0) {
        SHA1_Update(&ctx, buff, size);
    }

    fclose(fp);

    SHA1_Final(hash, &ctx);
    return 1;
}

int check_if_virus(char* path)
{
    int   i;
    char  hash[SHA_DIGEST_LENGTH] = {0};

    LOG("validating %s", path);

    if (!calc_hash(path, hash)) {
        return 0;
    }

    LOG("finalizing hash");

    for (i = 0; i < sizeof(invalid_hashes) / sizeof(invalid_hashes[0]); i++) {
        if (memcmp(hash, invalid_hashes[i], sizeof(hash)) == 0) {
            return 1;
        }
    }

    return 0;
}

int check_if_live_patch(char* path)
{
    int   i;
    char  hash[SHA_DIGEST_LENGTH] = {0};

    if (!calc_hash(path, hash)) {
        return 0;
    }

    for (i = 0; i < sizeof(patch_hashes) / sizeof(patch_hashes[0]); i++) {
        if (memcmp(hash, patch_hashes[i], sizeof(hash)) == 0) {
            return 1;
        }
    }

    return 0;
}
