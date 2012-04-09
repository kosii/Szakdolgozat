#include <windows.h>
#include <detours.h>
#include <stdio.h>
#include <iostream>

int CDECL main(int argc, char **argv){
	//LPCTSTR lpApplicationName = "C:\\Users\\kosi\\Documents\\Projects\\Szakdolgozat\\HoneyPot\\HoneyPot.exe";
	TCHAR lpApplicationName[] = "C:\\Users\\kosi\\AppData\\Local\\Amazon\\Kindle\\application\\Kindle.exe";
    //TCHAR lpApplicationName[] = "C:\\Program Files (x86)\\Full Tilt Poker.Fr\\FullTiltPokerFr.exe";
    //TCHAR lpApplicationName[] = "C:\\Users\\kosi\\Documents\\Projects\\Szakdolgozat\\HoneyPot\\HoneyPot.exe";
	
    LPTSTR lpCommandLine = NULL;
	STARTUPINFO si = {sizeof(si)};
    PROCESS_INFORMATION pi;
	DWORD dwFlags = CREATE_DEFAULT_ERROR_MODE | CREATE_SUSPENDED;
	SetLastError(0);
	if (!DetourCreateProcessWithDll(NULL, lpApplicationName,
	     NULL, NULL, TRUE, dwFlags, NULL, NULL, &si, &pi,
         "injected.dll", NULL)) {
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
        // LPCTSTR pipename = "\\\\.\\pipe\\pipename";
        // HANDLE ph = CreateNamedPipe(
        //     pipename, PIPE_ACCESS_INBOUND,
        //     PIPE_TYPE_MESSAGE, 255, 0, 0, 0, NULL);
        // if (ph == INVALID_HANDLE_VALUE)
        //     printf("BUDOSKURVA\n");
        // else printf("OKOKOK\n");

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
        } else {
            printf("resumethread ok\n");
        }

        // varunk beerkezo uzire a pipe-on 1seces timeouttal, ha van, kiirjuk, ha timeout, akkor ellenorizzuk hogy el-e meg a child process
        // ha nem el, kilepunk, ha el, akkor ujbol varunk
        // ConnectNamedPipe(ph, NULL);
        // if (WaitNamedPipe(pipename, NMPWAIT_WAIT_FOREVER)) {
        //     // read
        //     printf("kaka\n");
        // } else {
        //     printf("pisi\n");
        //     // wtf
        // }
        // Wait until child process exits.
        if (WaitForSingleObject(pi.hProcess, INFINITE) == 0xFFFFFFFF) {
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
        } else {
            printf("waitforsingleobject OK\n");
        }

        // Close process and thread handles. 
        CloseHandle( pi.hProcess );
        CloseHandle( pi.hThread );
    }
	return 0;
}
