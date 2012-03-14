#include <windows.h>
#include <detours.h>
#include <stdio.h>


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
