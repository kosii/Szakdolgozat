#include <windows.h>
#include <detours.h>
#include <stdio.h>

#include <QtCore/QObject>
#include <QtCore/qobjectdefs.h>

static LONG dwSlept = 0;

// Target pointer for the uninstrumented Sleep API.
static VOID (WINAPI * TrueSleep)(DWORD dwMilliseconds) = Sleep;

// QObject::qt_metacall
// int (*QObject::qt)

typedef int (__stdcall QObject::* qt_metacall_signature)(QMetaObject::Call _c, int _id, void **_a);

qt_metacall_signature* original_address = (qt_metacall_signature*)(void*)0x401110;

// QMetaObject::Call qobjectdefs.h ban van definialva
int __stdcall qt_metacall(QMetaObject::Call _c, int _id, void **_a) {
    return original_address(_c, _id, _a);
    printf("LOOOL, id: %d, QMetaObject::Call: %d\n", _id, _c);
    return 0;
}

// Detour function that replaces the Sleep API.
VOID WINAPI TimedSleep(DWORD dwMilliseconds)
{
    // Save the before and after times around calling the Sleep API.
    DWORD dwBeg = GetTickCount();
    TrueSleep(dwMilliseconds);
    DWORD dwEnd = GetTickCount();

    InterlockedExchangeAdd(&dwSlept, dwEnd - dwBeg);
}

// DllMain function attaches and detaches the TimedSleep detour to the
// Sleep target function.  The Sleep target function is referred to
// through the TrueSleep target pointer.
BOOL WINAPI DllMain(HINSTANCE hinst, DWORD dwReason, LPVOID reserved)
{
    LONG errCode;
    if (dwReason == DLL_PROCESS_ATTACH) {
        printf("1\n");
        DetourTransactionBegin();
        DisableThreadLibraryCalls(hinst);
        if (NO_ERROR != (errCode = DetourUpdateThread(GetCurrentThread()))) {
            printf("errorCode %ld\n", errCode);
        } else {
            printf("    updatethread ok\n");
        }
        if (NO_ERROR != (errCode = DetourAttach(&(PVOID&)original_address, &qt_metacall))) {
            printf("errorCode %ld\n", errCode);
        } else {
            printf("    attach OK\n");
        }
        if (NO_ERROR != (errCode = DetourTransactionCommit())) {
            printf("errorCode %ld\n", errCode);
        } else {
            printf("commit ok\n");
        }
    }
    else if (dwReason == DLL_PROCESS_DETACH) {
        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());
        DetourDetach(&(PVOID&)original_address, qt_metacall);
        DetourTransactionCommit();
    }
    return TRUE;
}

