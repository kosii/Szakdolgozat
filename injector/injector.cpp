#include <windows.h>
#include <detours.h>
#include <stdio.h>

BOOL DumpProcess(HANDLE hp);

static BYTE buffer[65536];

typedef union
{
    struct
    {
        DWORD Signature;
        IMAGE_FILE_HEADER FileHeader;
    } ih;

    IMAGE_NT_HEADERS32 ih32;
    IMAGE_NT_HEADERS64 ih64;
} IMAGE_NT_HEADER;

struct SECTIONS
{
    PBYTE   pbBeg;
    PBYTE   pbEnd;
    CHAR    szName[16];
} Sections[256];
DWORD SectionCount = 0;
DWORD Bitness = 0;

PCHAR FindSectionName(PBYTE pbBase, PBYTE& pbEnd)
{
    for (DWORD n = 0; n < SectionCount; n++) {
        if (Sections[n].pbBeg == pbBase) {
            pbEnd = Sections[n].pbEnd;
            return Sections[n].szName;
        }
    }
    pbEnd = NULL;
    return NULL;
}

ULONG PadToPage(ULONG Size)
{
    return (Size & 0xfff)
        ? Size + 0x1000 - (Size & 0xfff)
        : Size;
}

int CDECL main(int argc, char **argv){
	//LPCTSTR lpApplicationName = "C:\\Users\\kosi\\Documents\\Projects\\Szakdolgozat\\HoneyPot\\HoneyPot.exe";
	TCHAR lpApplicationName[] = "C:\\Users\\kosi\\AppData\\Local\\Amazon\\Kindle\\application\\Kindle.exe";
	LPTSTR lpCommandLine = NULL;
	STARTUPINFO si = {sizeof(si)};
    PROCESS_INFORMATION pi;
    // ZeroMemory(&si, sizeof(si));
    // ZeroMemory(&pi, sizeof(pi));
    // si.cb = sizeof(si);
	DWORD dwFlags = CREATE_DEFAULT_ERROR_MODE | CREATE_SUSPENDED;
	printf("csa\n");
	SetLastError(0);
	printf("y0 -> %s\n", lpApplicationName);
	// if (!DetourCreateProcessWithDll(lpApplicationName, NULL,
	//     NULL, NULL, TRUE, dwFlags, NULL, NULL, &si, &pi, "C:\\Users\\kosi\\Documents\\Projects\\Szakdolgozat\\injector\\injected.dll", NULL)) {
	if (!DetourCreateProcessWithDll(NULL, lpApplicationName,
	     NULL, NULL, TRUE, dwFlags, NULL, NULL, &si, &pi,
         "injected.dll", NULL)) {
    	printf("kurva\n");
        DWORD dwError = GetLastError();
        printf("withdll.exe: DetourCreateProcessWithDll failed: %d\n", dwError);
        HLOCAL hlocal = NULL;
        DWORD systemLocale = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL);
        FormatMessage(
        	FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_ALLOCATE_BUFFER,
        	NULL, dwError, systemLocale,
        	(PSTR) &hlocal, 0, NULL);
        printf((const char*)hlocal);
        LocalFree(hlocal);
        ExitProcess(9009);
    } else {
        printf("szar\n");
        //DumpProcess(pi.hProcess);
        if (ResumeThread(pi.hThread) == -1) {
            printf("ResumeThread failed\n");
            DWORD dwError = GetLastError();
            HLOCAL hlocal = NULL;
            DWORD systemLocale = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL);
            FormatMessage(
                FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_ALLOCATE_BUFFER,
                NULL, dwError, systemLocale,
                (PSTR) &hlocal, 0, NULL);
            printf((const char*)hlocal);
            LocalFree(hlocal);
            ExitProcess(9010);
        }

        // Wait until child process exits.
        if (WaitForSingleObject( pi.hProcess, INFINITE ) == 0xFFFFFFFF) {
            printf("WaitForSingleObject failed\n");
            DWORD dwError = GetLastError();
            HLOCAL hlocal = NULL;
            DWORD systemLocale = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL);
            FormatMessage(
                FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_ALLOCATE_BUFFER,
                NULL, dwError, systemLocale,
                (PSTR) &hlocal, 0, NULL);
            printf((const char*)hlocal);
            LocalFree(hlocal);
            ExitProcess(9011);
        }

        // Close process and thread handles. 
        CloseHandle( pi.hProcess );
        CloseHandle( pi.hThread );
    	printf("buzivagy!\n");
    }
    printf("szar\n");
	return 0;
}


BOOL GetSections(HANDLE hp, PBYTE pbBase)
{
    DWORD beg = 0;
    DWORD cnt = 0;
    SIZE_T done;
    IMAGE_DOS_HEADER idh;

    if (!ReadProcessMemory(hp, pbBase, &idh, sizeof(idh), &done) || done != sizeof(idh)) {
        return FALSE;
    }

    if (idh.e_magic != IMAGE_DOS_SIGNATURE) {
        return FALSE;
    }

    IMAGE_NT_HEADER inh;
    if (!ReadProcessMemory(hp, pbBase + idh.e_lfanew, &inh, sizeof(inh), &done) || done != sizeof(inh)) {
        printf("No Read\n");
        return FALSE;
    }

    if (inh.ih.Signature != IMAGE_NT_SIGNATURE) {
        printf("No NT\n");
        return FALSE;
    }

    beg = idh.e_lfanew
        + FIELD_OFFSET( IMAGE_NT_HEADERS, OptionalHeader )
        + inh.ih.FileHeader.SizeOfOptionalHeader;
    cnt = inh.ih.FileHeader.NumberOfSections;
    Bitness = (inh.ih32.OptionalHeader.Magic == IMAGE_NT_OPTIONAL_HDR32_MAGIC) ? 32 : 64;
#if 0
    printf("%d %d count=%d\n", beg, Bitness, cnt);
#endif

    IMAGE_SECTION_HEADER ish;
    for (DWORD n = 0; n < cnt; n++) {
        if (!ReadProcessMemory(hp, pbBase + beg + n * sizeof(ish), &ish, sizeof(ish), &done) || done != sizeof(ish)) {
            printf("No Read\n");
            return FALSE;
        }
        Sections[n].pbBeg = pbBase + ish.VirtualAddress;
        Sections[n].pbEnd = pbBase + ish.VirtualAddress + PadToPage(ish.Misc.VirtualSize);
        memcpy(Sections[n].szName, ish.Name, sizeof(ish.Name));
        Sections[n].szName[sizeof(ish.Name)] = '\0';
#if 0
        printf("--- %p %s\n", Sections[n].pbBeg, Sections[n].szName);
#endif
    }
    SectionCount = cnt;

    return TRUE;
}


void TypeToString(DWORD Type, char *pszBuffer, size_t cBuffer)
{
    if (Type == MEM_IMAGE) {
        sprintf_s(pszBuffer, cBuffer, "img");
    }
    else if (Type == MEM_MAPPED) {
        sprintf_s(pszBuffer, cBuffer, "map");
    }
    else if (Type == MEM_PRIVATE) {
        sprintf_s(pszBuffer, cBuffer, "pri");
    }
    else {
        sprintf_s(pszBuffer, cBuffer, "%x", Type);
    }
}

void StateToString(DWORD State, char *pszBuffer, size_t cBuffer)
{
    if (State == MEM_COMMIT) {
        sprintf_s(pszBuffer, cBuffer, "com");
    }
    else if (State == MEM_FREE) {
        sprintf_s(pszBuffer, cBuffer, "fre");
    }
    else if (State == MEM_RESERVE) {
        sprintf_s(pszBuffer, cBuffer, "res");
    }
    else {
        sprintf_s(pszBuffer, cBuffer, "%x", State);
    }
}

void ProtectToString(DWORD Protect, char *pszBuffer, size_t cBuffer)
{
    if (Protect == 0) {
        sprintf_s(pszBuffer, cBuffer, "");
    }
    else if (Protect == PAGE_EXECUTE) {
        sprintf_s(pszBuffer, cBuffer, "--x");
    }
    else if (Protect == PAGE_EXECUTE_READ) {
        sprintf_s(pszBuffer, cBuffer, "r-x");
    }
    else if (Protect == PAGE_EXECUTE_READWRITE) {
        sprintf_s(pszBuffer, cBuffer, "rwx");
    }
    else if (Protect == PAGE_EXECUTE_WRITECOPY) {
        sprintf_s(pszBuffer, cBuffer, "rcx");
    }
    else if (Protect == PAGE_NOACCESS) {
        sprintf_s(pszBuffer, cBuffer, "---");
    }
    else if (Protect == PAGE_READONLY) {
        sprintf_s(pszBuffer, cBuffer, "r--");
    }
    else if (Protect == PAGE_READWRITE) {
        sprintf_s(pszBuffer, cBuffer, "rw-");
    }
    else if (Protect == PAGE_WRITECOPY) {
        sprintf_s(pszBuffer, cBuffer, "rc-");
    }
    else if (Protect == (PAGE_GUARD | PAGE_EXECUTE)) {
        sprintf_s(pszBuffer, cBuffer, "g--x");
    }
    else if (Protect == (PAGE_GUARD | PAGE_EXECUTE_READ)) {
        sprintf_s(pszBuffer, cBuffer, "gr-x");
    }
    else if (Protect == (PAGE_GUARD | PAGE_EXECUTE_READWRITE)) {
        sprintf_s(pszBuffer, cBuffer, "grwx");
    }
    else if (Protect == (PAGE_GUARD | PAGE_EXECUTE_WRITECOPY)) {
        sprintf_s(pszBuffer, cBuffer, "grcx");
    }
    else if (Protect == (PAGE_GUARD | PAGE_NOACCESS)) {
        sprintf_s(pszBuffer, cBuffer, "g---");
    }
    else if (Protect == (PAGE_GUARD | PAGE_READONLY)) {
        sprintf_s(pszBuffer, cBuffer, "gr--");
    }
    else if (Protect == (PAGE_GUARD | PAGE_READWRITE)) {
        sprintf_s(pszBuffer, cBuffer, "grw-");
    }
    else if (Protect == (PAGE_GUARD | PAGE_WRITECOPY)) {
        sprintf_s(pszBuffer, cBuffer, "grc-");
    }
    else {
        sprintf_s(pszBuffer, cBuffer, "%x", Protect);
    }
}


BOOL DumpProcess(HANDLE hp)
{
    ULONG64 base;
    ULONG64 next;

    MEMORY_BASIC_INFORMATION mbi;

    printf("  %12s %8s %8s: %3s %3s %4s %3s : %8s\n", "Address", "Offset", "Size", "Typ", "Sta", "Prot", "Ini", "Contents");
    printf("  %12s %8s %8s: %3s %3s %4s %3s : %8s\n", "------------", "--------", "--------", "---", "---", "----", "---", "-----------------");

    for (next = 0;;) {
        base = next;
        ZeroMemory(&mbi, sizeof(mbi));
        if (VirtualQueryEx(hp, (PVOID)base, &mbi, sizeof(mbi)) == 0) {
            break;
        }

        next = (ULONG64)mbi.BaseAddress + mbi.RegionSize;

        if (mbi.State == MEM_FREE) {
            continue;
        }

        CHAR szType[16];
        TypeToString(mbi.Type, szType, ARRAYSIZE(szType));
        CHAR szState[16];
        StateToString(mbi.State, szState, ARRAYSIZE(szState));
        CHAR szProtect[16];
        ProtectToString(mbi.Protect, szProtect, ARRAYSIZE(szProtect));
        CHAR szAllocProtect[16];
        ProtectToString(mbi.AllocationProtect, szAllocProtect, ARRAYSIZE(szAllocProtect));

        CHAR szFile[MAX_PATH];
        szFile[0] = '\0';
        DWORD cb = 0;
        PCHAR pszFile = szFile;

        if (base == (ULONG64)mbi.AllocationBase) {
#if 0
            cb = pfGetMappedFileName(hp, (PVOID)mbi.AllocationBase, szFile, ARRAYSIZE(szFile));
#endif
            if (GetSections(hp, (PBYTE)mbi.AllocationBase)) {
                next = base + 0x1000;
                sprintf_s(szFile, ARRAYSIZE(szFile), "%d-bit PE", Bitness);
            }
        }
        if (cb > 0) {
            for (DWORD c = 0; c < cb; c++) {
                szFile[c] = (szFile[c] >= 'a' && szFile[c] <= 'z')
                    ? szFile[c] - 'a' + 'A' : szFile[c];
            }
            szFile[cb] = '\0';
        }

        if ((pszFile = strrchr(szFile, '\\')) == NULL) {
            pszFile = szFile;
        }
        else {
            pszFile++;
        }

        PBYTE pbEnd;
        PCHAR pszSect = FindSectionName((PBYTE)base, pbEnd);
        if (pszSect != NULL) {
            pszFile = pszSect;
            if (next > (ULONG64)pbEnd) {
                next = (ULONG64)pbEnd;
            }
        }

        CHAR szDesc[128];
        ZeroMemory(&szDesc, ARRAYSIZE(szDesc));
        if (base == (ULONG64)mbi.AllocationBase) {
            sprintf_s(szDesc, ARRAYSIZE(szDesc), "  %12I64x %8I64x %8I64x: %3s %3s %4s %3s : %s",
                      (ULONG64)base,
                      (ULONG64)base - (ULONG64)mbi.AllocationBase,
                      (ULONG64)next - (ULONG64)base,
                      szType,
                      szState,
                      szProtect,
                      szAllocProtect,
                      pszFile);


        }
        else {
            sprintf_s(szDesc, ARRAYSIZE(szDesc), "  %12s %8I64x %8I64x: %3s %3s %4s %3s : %s",
                      "-",
                      (ULONG64)base - (ULONG64)mbi.AllocationBase,
                      (ULONG64)next - (ULONG64)base,
                      szType,
                      szState,
                      szProtect,
                      szAllocProtect,
                      pszFile);
        }
        printf("%s\n", szDesc);
    }
    return TRUE;
}
