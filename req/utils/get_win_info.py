# -*- coding:utf-8 -*-
# 使用utf-8编码
import wmi

c = wmi.WMI()

def sys_version():
    # 获取操作系统版本
    for sys in c.Win32_OperatingSystem():
        print "Version: %s" % sys.Caption.encode("UTF"), "Vernum:%s" % sys.BuildNumber, "%s" % sys.OSArchitecture.encode(
            "UTF")

def cpu_mem():
    # CPU类型和内存
    for processor in c.Win32_Processor():
        print "CPU Name: %s" % processor.Name.strip()
    for cobj in c.Win32_ComputerSystem():
        print "CPU size: %s" % cobj.TotalPhysicalMemory.strip()
    for Memory in c.Win32_PhysicalMemory():
        print "Memory Capacity: %.fMB" % (int(Memory.Capacity) / 1048576)

def gpu_mem():
    # GPU类型和内存
    for gpu in c.Win32_VideoController():
        print "GPU Name: %s" % gpu.Name.strip()
        print "GPU size: %d" % abs(gpu.AdapterRAM)


sys_version()
gpu_mem()
cpu_mem()
# for gpu in c.Win32_VideoController():
#     print gpu