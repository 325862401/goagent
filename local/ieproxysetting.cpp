#include "stdio.h"
#include "windows.h"
#include "wininet.h"
#pragma comment(lib, "wininet.lib")
int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   PSTR szCmdLine, int iCmdShow)
{
 //char buff[256] = "http=http://itgproxy:80";http://109.130.10.19:8080/TEST.pac
 char buff[256]= "http://127.0.0.1:8086/proxy.pac";
 int buffSize = MultiByteToWideChar(CP_ACP, 0, buff, -1, NULL, 0);
 LPWSTR proxy = new WCHAR[buffSize];
 MultiByteToWideChar(CP_ACP, 0, buff, -1, proxy, buffSize);
 INTERNET_PER_CONN_OPTION_LIST    List;
 INTERNET_PER_CONN_OPTION         Option[2];
 unsigned long                    nSize = sizeof(INTERNET_PER_CONN_OPTION_LIST);
 
 Option[0].dwOption = INTERNET_PER_CONN_AUTOCONFIG_URL;
 Option[0].Value.pszValue = proxy;
 //Option[0].Value.dwValue = PROXY_TYPE_AUTO_PROXY_URL;
 Option[1].dwOption = INTERNET_PER_CONN_FLAGS;
 Option[1].Value.dwValue = PROXY_TYPE_AUTO_PROXY_URL;
 //Option[1].Value.dwValue |= PROXY_TYPE_DIRECT;
 // This option sets all the possible connection types for the client.
 // This case specifies that the proxy can be used or direct connection is possible.
// Option[2].dwOption = INTERNET_PER_CONN_PROXY_BYPASS;
// Option[2].Value.pszValue = "<local>";
 
 List.dwSize = sizeof(INTERNET_PER_CONN_OPTION_LIST);
 List.pszConnection = NULL;
 List.dwOptionCount = 2;
 List.dwOptionError = 0;
 List.pOptions = Option;
 if(!InternetSetOption(NULL, INTERNET_OPTION_PER_CONNECTION_OPTION, &List, nSize))
  printf("InternetSetOption failed! (%d)\n", GetLastError());
 InternetSetOption(NULL,INTERNET_OPTION_SETTINGS_CHANGED,NULL,NULL);
 InternetSetOption(NULL, INTERNET_OPTION_REFRESH, NULL,NULL);
 //The connection settings for other instances of Internet Explorer.
 return 0;
}
