#include <windows.h>
#include <detours.h>
#include <stdio.h>
#include <iostream>

int CDECL main(int argc, char **argv){
	//LPCTSTR lpApplicationName = "C:\\Users\\kosi\\Documents\\Projects\\Szakdolgozat\\HoneyPot\\HoneyPot.exe";
	// TCHAR lpApplicationName[] = "C:\\Users\\kosi\\AppData\\Local\\Amazon\\Kindle\\application\\Kindle.exe";
    //TCHAR lpApplicationName[] = "C:\\Program Files (x86)\\Full Tilt Poker.Fr\\FullTiltPokerFr.exe";
    //TCHAR lpApplicationName[] = "C:\\Users\\kosi\\Documents\\Projects\\Szakdolgozat\\HoneyPot\\HoneyPot.exe";
    if (argc != 2) {
        printf("Wrong number of arguments. Usage: ./injector input_file\n");
        return -1;
    } else {
        TCHAR *lpApplicationName = (TCHAR *)malloc((strlen(argv[1]) + 1)* sizeof(TCHAR));
        strncpy(lpApplicationName, argv[1], (strlen(argv[1]) + 1));
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
            free(lpApplicationName);
            LocalFree(hlocal);
            ExitProcess(9009);
        } else {
            printf("FOOS\n");
            if (ResumeThread(pi.hThread) == -1) {
                DWORD dwError = GetLastError();
                HLOCAL hlocal = NULL;
                DWORD systemLocale = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL);
                FormatMessage(
                    FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_ALLOCATE_BUFFER,
                    NULL, dwError, systemLocale,
                    (PSTR) &hlocal, 0, NULL);
                // print error message
                printf((const char*)hlocal);
                LocalFree(hlocal);
                free(lpApplicationName);
                getc(stdin);
                ExitProcess(9010);
            }
            // Wait until child process exits.
            if (WaitForSingleObject(pi.hProcess, INFINITE) == 0xFFFFFFFF) {
                DWORD dwError = GetLastError();
                HLOCAL hlocal = NULL;
                DWORD systemLocale = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL);
                FormatMessage(
                    FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_ALLOCATE_BUFFER,
                    NULL, dwError, systemLocale,
                    (PSTR) &hlocal, 0, NULL);
                //print error message
                printf((const char*)hlocal);
                LocalFree(hlocal);
                free(lpApplicationName);
                ExitProcess(9011);
            }

            CloseHandle( pi.hProcess );
            CloseHandle( pi.hThread );
        }
        return 0;
    }
}
