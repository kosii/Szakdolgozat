#include <windows.h>
#include <detours.h>
#include <stdio.h>

#include <QtCore/QObject>
#include <QtCore/qobjectdefs.h>

typedef int (WINAPI qt_metacall_signature)(QMetaObject::Call _c, int _id, void **_a);

qt_metacall_signature* original_address = (qt_metacall_signature*)(void*)0x401110;

// QMetaObject::Call qobjectdefs.h ban van definialva
int WINAPI qt_metacall(QMetaObject::Call _c, int _id, void **_a) {
    printf("hello from honeypot\n");
    return original_address(_c, _id, _a);
}

BOOL DllProcessAttach(HINSTANCE hinst) {
    LONG errCode;
    if (NO_ERROR != (errCode = DetourTransactionBegin())) {
        switch (errCode) {
            case ERROR_INVALID_OPERATION:
                printf("DetourTransactionBegin failed\n\tA pending transaction alrady exists.");
                break;
        }
        return FALSE;
    }
    DisableThreadLibraryCalls(hinst);
    if (NO_ERROR != (errCode = DetourUpdateThread(GetCurrentThread()))) {
        switch (errCode) {
            case ERROR_NOT_ENOUGH_MEMORY:
                printf("DetourUpdateThread failed\n\tNot enough memory to record identity of thread.");
                break;
        }
        DetourTransactionAbort();
        return FALSE;
    }
    if (NO_ERROR != (errCode = DetourAttach(&(PVOID&)original_address, qt_metacall))) {
        switch (errCode) {
            case ERROR_INVALID_BLOCK:
                printf("DetourAttach failed\n\tThe function referenced is too small to be detoured.");
                break;
            case ERROR_INVALID_HANDLE:
                printf("DetourAttach failed\n\tThe ppPointer parameter is null or points to a null pointer.");
                break;
            case ERROR_INVALID_OPERATION:
                printf("DetourAttach failed\n\tNo pending transaction exists.");
                break;
            case ERROR_NOT_ENOUGH_MEMORY:
                printf("DetourAttach failed\n\tNot enough memory exists to complete the operation.");
                break;
        }
        DetourTransactionAbort();
        return FALSE;
    }
    if (NO_ERROR != (errCode = DetourTransactionCommit())) {
        switch (errCode) {
            case ERROR_INVALID_DATA:
                printf("DetourTransactionCommit failed. Target function was changed by third party between steps of the transaction.");
                break;
            case ERROR_INVALID_OPERATION:
                printf("DetourTransactionCommit failed. No pending transaction exists.");
                break;
            default:
                printf("DetourTransactionCommit failed. Other error.");
                break;
        }
        DetourTransactionAbort();
        return FALSE;
    }
    return TRUE;
}

BOOL DllProcessDetach() {
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourDetach(&(PVOID&)original_address, qt_metacall);
    DetourTransactionCommit();
    return TRUE;
}

BOOL WINAPI DllMain(HINSTANCE hinst, DWORD dwReason, LPVOID reserved)
{
    switch (dwReason) {
        case DLL_PROCESS_ATTACH:
            return DllProcessAttach(hinst);
        case DLL_PROCESS_DETACH:
            return DllProcessDetach();
        default:
            return TRUE;
    }
}

