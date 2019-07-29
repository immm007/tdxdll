// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "stdafx.h"
#include <boost/python/numpy.hpp>

namespace p = boost::python;
namespace np = boost::python::numpy;
p::api::object CHAODUAN;

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
					 )
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		//MessageBoxA(nullptr, "1", "log", MB_OK);
		Py_SetPythonHome(L"E:\\Anaconda3");
		Py_Initialize();
		if (!Py_IsInitialized())
		{
			MessageBoxA(nullptr, "start python fail", "error", MB_OK);
		}
		//MessageBoxA(nullptr, "2", "log", MB_OK);
		np::initialize();
		//MessageBoxA(nullptr, "3", "log", MB_OK);
		CHAODUAN = p::import("chaoduan");
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}

