#include "stdafx.h"
#include "TCalcFuncSets.h"
#include <boost/python/numpy.hpp>

namespace p = boost::python;
namespace np = boost::python::numpy;
//生成的dll及相关依赖dll请拷贝到通达信安装目录的T0002/dlls/下面,再在公式管理器进行绑定

extern p::api::object CHAODUAN;

void prepare(int len,float* outs,float* codes,float* dates,float* zt_types)
{
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_zt_types = np::from_data(zt_types, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("prepare")(p::object(codes[0]), p_dates, p_zt_types);
}

void get_scsb(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_scsb")(p_outs,p::object(codes[0]), p_dates);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_ycfs(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_ycfs")(p_outs, p::object(codes[0]), p_dates);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_sckb(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_sckb")(p_outs, p::object(codes[0]), p_dates);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_zhhf(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_zhhf")(p_outs, p::object(codes[0]), p_dates);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_gwcj(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_gwcj")(p_outs, p::object(codes[0]), p_dates);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_lbcs(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_zt_types = np::from_data(zt_types, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_lbcs")(p_outs, p::object(codes[0]), p_dates, p_zt_types);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_jzc(int len, float* outs, float* codes, float* dates, float* zt_types)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_jzc")(p_outs, p::object(codes[0]), p_dates);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

void get_sz(int len, float* outs, float* codes, float* dates, float* zfs)
{
	//MessageBoxA(nullptr, "1", "log", MB_OK);
	np::ndarray p_dates = np::from_data(dates, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_outs = np::from_data(outs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	np::ndarray p_zfs = np::from_data(zfs, np::dtype::get_builtin<float>(),
		p::make_tuple(len),
		p::make_tuple(sizeof(float)),
		p::object());
	CHAODUAN.attr("get_sz")(p_outs, p::object(codes[0]), p_dates, p_zfs);
	//MessageBoxA(nullptr, "2", "log", MB_OK);
}

//加载的函数
PluginTCalcFuncInfo g_CalcFuncSets[] = 
{
	{ 1,(pPluginFUNC)&prepare },
	{ 2,(pPluginFUNC)&get_scsb },
	{ 3,(pPluginFUNC)&get_ycfs },
	{ 4,(pPluginFUNC)&get_sckb },
	{ 5,(pPluginFUNC)&get_zhhf },
	{ 6,(pPluginFUNC)&get_gwcj },
	{ 7,(pPluginFUNC)&get_lbcs },
	{ 8,(pPluginFUNC)&get_jzc },
	{ 9,(pPluginFUNC)&get_sz },
	{0,NULL},
};

//导出给TCalc的注册函数
BOOL RegisterTdxFunc(PluginTCalcFuncInfo** pFun)
{
	if(*pFun==NULL)
	{
		(*pFun)=g_CalcFuncSets;
		return TRUE;
	}
	return FALSE;
}
