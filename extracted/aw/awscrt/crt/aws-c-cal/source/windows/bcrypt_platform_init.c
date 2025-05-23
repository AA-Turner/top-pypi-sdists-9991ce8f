/**
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0.
 */

#include <aws/common/allocator.h>
#if defined(AWS_USE_LIBCRYPTO_TO_SUPPORT_ED25519_EVERYWHERE) && defined(OPENSSL_IS_AWSLC)
#    include <openssl/thread.h>
#    include <windows.h>
#endif

void aws_cal_platform_init(struct aws_allocator *allocator) {
    (void)allocator;
}

void aws_cal_platform_clean_up(void) {
#if defined(AWS_USE_LIBCRYPTO_TO_SUPPORT_ED25519_EVERYWHERE) && defined(OPENSSL_IS_AWSLC)
    AWSLC_thread_local_clear();
#endif
}

void aws_cal_platform_thread_clean_up(void) {
#if defined(AWS_USE_LIBCRYPTO_TO_SUPPORT_ED25519_EVERYWHERE) && defined(OPENSSL_IS_AWSLC)
    AWSLC_thread_local_clear();
#endif
}

#if defined(AWS_USE_LIBCRYPTO_TO_SUPPORT_ED25519_EVERYWHERE) && defined(OPENSSL_IS_AWSLC)
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_DETACH:
            AWSLC_thread_local_shutdown();
            break;
    }
    return TRUE;
}
#endif
