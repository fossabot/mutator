#!/bin/python3
import argparse
import sys
import readline
import code

class ExceptionHandler(object):
    def __init__(self, globals, locals):
        self.variables = globals().copy()
        self.variables.update(locals())
        self.shell = code.InteractiveConsole()
        shell.interact(banner="Object Loader Prototype")

class CLIArgParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--obj", type=str, help="path to the executbale, shared object or object you want to load in bruiser")
        self.args = parser.parse_args()
        if self.args.obj is None:
            raise Exception("no object file provided. please specify an object with --obj.")

def byte2int(value):
    return int.from_bytes(value, byteorder="little", signed=False)

def byte2hex(value):
    return hex(int.from_bytes(value, byteorder="little", signed=False))

def get_section_type_string(number):
    if number == 0x0: return "NULL"
    if number == 0x1: return "PROGBITS"
    if number == 0x2: return "SYMTAB"
    if number == 0x3: return "STRTAB"
    if number == 0x4: return "RELA"
    if number == 0x5: return "HASH"
    if number == 0x6: return "DYNAMIC"
    if number == 0x7: return "NOTE"
    if number == 0x8: return "NOBITS"
    if number == 0x9: return "REL"
    if number == 0xa: return "SHLIB"
    if number == 0xb: return "DYNSYM"
    if number == 0xe: return "INIT_ARRAY"
    if number == 0xf: return "FINI_ARRAY"
    if number == 0x10: return "PREINIT"
    if number == 0x11: return "GROUP"
    if number == 0x12: return "SYMTAB"
    if number == 0x13: return "NUM"
    if number == 0x60000000: return "LOOS"
    if number == 0x6ffffff6: return "GNU_HASH"
    if number == 0x6fffffff: return "VERSYM"
    if number == 0x6ffffffe: return "VERNEED"

class sh_type_e:
    SHT_NULL = 0x0
    SHT_PROGBITS = 0x1
    SHT_SYMTAB = 0x2
    SHT_STRTAB = 0x3
    SHT_RELA = 0x4
    SHT_HASH = 0x5
    SHT_DYNAMIC = 0x6
    SHT_NOTE = 0x7
    SHT_NOBITS = 0x8
    SHT_REL = 0x9
    SHT_SHLIB = 0xa
    SHT_DYNSYM = 0xb
    SHT_INIT_ARRAY = 0xe
    SHT_FINI_ARRAY = 0xf
    SHT_PREINIT = 0x10
    SHT_GROUP = 0x11
    SHT_SYMTAB_SHNDX = 0x12
    SHT_NUM = 0x13
    SHT_LOOS = 0x60000000
    GNU_HASH = 0x6ffffff6
    VERSYM = 0x6fffffff
    VERNEED= 0x6ffffffe

class sh_flags_e:
    SHF_WRITE = 0x1
    SHF_ALLOC = 0x2
    SHF_EXECINSTR = 0x4
    SHF_MERGE = 0x10
    SHF_STRINGS = 0x20
    SHF_INFO_LINK = 0x40
    SHF_LINK_ORDER = 0x80
    SHF_OS_NONCONFORMING = 0x100
    SHF_GROUP = 0x200
    SHF_TLS = 0x400
    SHF_MASKOS = 0x0ff00000
    SHF_MASKPROC = 0xf0000000
    SHF_ORDERED = 0x4000000
    SHF_EXCLUDE = 0x8000000

class p_type_e:
    PT_NULL = 0x0
    PT_LOAD = 0x1
    PT_DYNAMIC = 0x2
    PT_INTERP = 0x3
    PT_NOTE = 0x4
    PT_SHLIB = 0x5
    PT_PHDR = 0x6
    PT_LOOS = 0x60000000
    PT_HIOS = 0x6FFFFFFF
    PT_LOPROC = 0x70000000
    PT_HIPROC = 0x7FFFFFFF
    GNU_EH_FRAME = 0x6474e550
    GNU_STACK = 0x6474e551
    GNU_RELRO = 0x6474e552

def get_ph_type(value):
    if value == p_type_e.PT_NULL: return "NULL"
    elif value == p_type_e.PT_LOAD: return "LOAD"
    elif value == p_type_e.PT_DYNAMIC: return "DYNAMIC"
    elif value == p_type_e.PT_INTERP: return "INTERP"
    elif value == p_type_e.PT_NOTE: return "NOTE"
    elif value == p_type_e.PT_SHLIB: return "SHLIB"
    elif value == p_type_e.PT_PHDR: return "PHDR"
    elif value == p_type_e.PT_LOOS: return "LOOS"
    elif value == p_type_e.PT_HIOS: return "HIOS"
    elif value == p_type_e.PT_LOPROC: return "LOPROC"
    elif value == p_type_e.PT_HIPROC: return "HIPROC"
    elif value == p_type_e.GNU_EH_FRAME: return "GNU_EH_FRAME"
    elif value == p_type_e.GNU_STACK: return "GNU_STACK"
    elif value == p_type_e.GNU_RELRO: return "GNU_RELRO"
    else: return None

class Colors:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    grey = '\033[1;37m'
    darkgrey = '\033[1;30m'
    cyan = '\033[1;36m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def openSO_r(path):
    so = open(path, "rb")
    return so

def openSO_w(path):
    so = open(path, "wb")
    return so

class ELFHDR():
    def __init__(self, ei_mag, ei_class, ei_data, ei_version, ei_osabi, ei_abiversion,
                 ei_pad, e_type, e_machine, e_version, e_entry, e_phoff,
                 e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize,
                 e_shnum, e_shstrndx):
        self.ei_mag = ei_mag
        self.ei_class = ei_class
        self.ei_data = ei_data
        self.ei_version = ei_version
        self.ei_osabi = ei_osabi
        self.ei_abiversion = ei_abiversion
        self.ei_pad = ei_pad
        self.e_type = e_type
        self.e_machine = e_machine
        self.e_version = e_version
        self.e_entry = e_entry
        self.e_phoff = e_phoff
        self.e_shoff = e_shoff
        self.e_flags = e_flags
        self.e_ehsize = e_ehsize
        self.e_phentsize = e_phentsize
        self.e_phnum = e_phnum
        self.e_shentsize = e_shentsize
        self.e_shnum = e_shnum
        self.e_shstrndx = e_shstrndx

class PHDR():
    def __init__(self, p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz,
                 p_memsz, p_flags2, p_align):
        self.p_type = p_type
        self.p_flags = p_flags
        self.p_offset = p_offset
        self.p_vaddr = p_vaddr
        self.p_paddr = p_paddr
        self.p_filesz = p_filesz
        self.p_memsz = p_memsz
        self.p_flags2 = p_flags2
        self.p_align = p_align

class SHDR():
    def __init__(self, sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size,
                 sh_link, sh_info, sh_addralign, sh_entsize):
        self.sh_name = sh_name
        self.sh_type = sh_type
        self.sh_flags = sh_flags
        self.sh_addr = sh_addr
        self.sh_offset = sh_offset
        self.sh_size = sh_size
        self.sh_link = sh_link
        self.sh_info = sh_info
        self.sh_addralign = sh_addralign
        self.sh_entsize = sh_entsize

class Symbol_Table_Entry64():
    def __init__(self, st_name, st_info, st_other, st_shndx, st_value, st_size):
        self.st_name = st_name
        self.st_info = st_info
        self.st_other = st_other
        self.st_shndx = st_shndx
        self.st_value = st_value
        self.st_size = st_size

class ELF(object):
    def __init__(self, so):
        self.so = so
        self.so.seek(0, 0)
        self.elfhdr = ELFHDR(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.phdr = []
        self.shhdr = []
        self.size = int()
        self.string_tb_e = []
        self.string_tb_e_dyn = []
        self.symbol_table_e = []
        self.data_section = []
        self.text_section = []

    def init(self, size):
        self.size = size
        self.read_ELF_H(size)
        self.so.seek(int.from_bytes(self.elfhdr.e_phoff, byteorder="little", signed=False))
        phnum = int.from_bytes(self.elfhdr.e_phnum, byteorder="little", signed=False)
        for i in range(0, phnum):
            self.read_PHDR(size)
        self.so.seek(int.from_bytes(self.elfhdr.e_shoff, byteorder="little", signed=False))
        shnum = int.from_bytes(self.elfhdr.e_shnum, byteorder="little", signed=False)
        for i in range(0, shnum):
            self.read_SHDR(size)
        for i in range(0, shnum):
            type = int.from_bytes(self.shhdr[i].sh_type, byteorder="little", signed=False)
            if type == sh_type_e.SHT_SYMTAB:
                self.so.seek(int.from_bytes(self.shhdr[i].sh_offset, byteorder="little", signed=False), 0)
                symbol_tb = self.so.read(int.from_bytes(self.shhdr[i].sh_size, byteorder="little", signed=False))
                offset = 0
                num = int(int.from_bytes(self.shhdr[i].sh_size, byteorder="little") / 24)
                for j in range(0, num):
                    self.read_st_entry(symbol_tb[offset:offset + 24], self.string_tb_e)
                    offset += 8*24
            if type == sh_type_e.SHT_DYNSYM:
                self.so.seek(int.from_bytes(self.shhdr[i].sh_offset, byteorder="little", signed=False), 0)
                symbol_tb = self.so.read(int.from_bytes(self.shhdr[i].sh_size, byteorder="little", signed=False))
                offset = 0
                num = int(int.from_bytes(self.shhdr[i].sh_size, byteorder="little") / 24)
                for j in range(0, num):
                    self.read_st_entry(symbol_tb[offset:offset + 24], self.string_tb_e_dyn)
                    offset += 8*24
        self.pop_data_section()
        self.pop_text_section()

    def read_ELF_H(self, size):
        self.elfhdr.ei_mag = self.so.read(4)
        self.elfhdr.ei_class = self.so.read(1)
        self.elfhdr.ei_data = self.so.read(1)
        self.elfhdr.ei_version = self.so.read(1)
        self.elfhdr.ei_osabi = self.so.read(1)
        self.elfhdr.ei_abiversion = self.so.read(1)
        self.elfhdr.ei_pad = self.so.read(7)
        self.elfhdr.e_type = self.so.read(2)
        self.elfhdr.e_machine = self.so.read(2)
        self.elfhdr.e_version = self.so.read(4)
        if size == 32: self.elfhdr.e_entry = self.so.read(4)
        elif size == 64: self.elfhdr.e_entry = self.so.read(8)
        if size == 32: self.elfhdr.e_phoff = self.so.read(4)
        elif size == 64: self.elfhdr.e_phoff = self.so.read(8)
        if size == 32: self.elfhdr.e_shoff = self.so.read(4)
        elif size == 64: self.elfhdr.e_shoff = self.so.read(8)
        self.elfhdr.e_flags = self.so.read(4)
        self.elfhdr.e_ehsize = self.so.read(2)
        self.elfhdr.e_phentsize = self.so.read(2)
        self.elfhdr.e_phnum = self.so.read(2)
        self.elfhdr.e_shentsize = self.so.read(2)
        self.elfhdr.e_shnum = self.so.read(2)
        self.elfhdr.e_shstrndx = self.so.read(2)

    def read_PHDR(self, size):
        dummy = PHDR(0,0,0,0,0,0,0,0,0)
        dummy.p_type = self.so.read(4)
        if size == 64: dummy.p_flags = self.so.read(4)
        if size == 32: dummy.p_offset = self.so.read(4)
        elif size == 64: dummy.p_offset = self.so.read(8)
        if size == 32: dummy.p_vaddr = self.so.read(4)
        elif size == 64: dummy.p_vaddr = self.so.read(8)
        if size == 32: dummy.p_paddr = self.so.read(4)
        elif size == 64: dummy.p_paddr = self.so.read(8)
        if size == 32: dummy.p_filesz = self.so.read(4)
        elif size == 64: dummy.p_filesz = self.so.read(8)
        if size == 32: dummy.p_memsz = self.so.read(4)
        elif size == 64: dummy.p_memsz = self.so.read(8)
        if size == 32: dummy.p_flags2 = self.so.read(4)
        elif size == 64: pass
        if size == 32: dummy.p_align = self.so.read(4)
        elif size == 64: dummy.p_align = self.so.read(8)
        self.phdr.append(dummy)

    def read_SHDR(self, size):
        dummy = SHDR(0,0,0,0,0,0,0,0,0,0)
        dummy.sh_name = self.so.read(4)
        dummy.sh_type = self.so.read(4)
        if size == 32: dummy.sh_flags = self.so.read(4)
        elif size == 64: dummy.sh_flags = self.so.read(8)
        if size == 32: dummy.sh_addr = self.so.read(4)
        elif size == 64: dummy.sh_addr = self.so.read(8)
        if size == 32: dummy.sh_offset = self.so.read(4)
        elif size == 64: dummy.sh_offset = self.so.read(8)
        if size == 32: dummy.sh_size = self.so.read(4)
        elif size == 64: dummy.sh_size = self.so.read(8)
        dummy.sh_link = self.so.read(4)
        dummy.sh_info = self.so.read(4)
        if size == 32: dummy.sh_addralign = self.so.read(4)
        elif size == 64: dummy.sh_addralign = self.so.read(8)
        if size == 32: dummy.sh_entsize = self.so.read(4)
        elif size == 64: dummy.sh_entsize = self.so.read(8)
        self.shhdr.append(dummy)

    def read_st_entry(self, st, entry_list):
        dummy = Symbol_Table_Entry64(0,0,0,0,0,0)
        dummy.st_name = st[0:4]
        dummy.st_info = st[4:5]
        dummy.st_other = st[5:6]
        dummy.st_shndx = st[6:8]
        dummy.st_value = st[8:16]
        dummy.st_size = st[16:24]
        entry_list.append(dummy)

    def read_section_name(self, index):
        shstrtab_index = byte2int(self.elfhdr.e_shstrndx)
        name = []
        self.so.seek(byte2int(self.shhdr[shstrtab_index].sh_offset), 0)
        strings = self.so.read(byte2int(self.shhdr[shstrtab_index].sh_size))
        char = strings[index]
        while chr(char) != "\0":
            index += 1
            name.append(chr(char))
            char = strings[index]
        return ''.join(name)

    def dump_objs(self):
        ret_list = []
        dummy = []
        ret_list_int = []
        for iter in self.string_tb_e:
            if byte2int(iter.st_size) != 0:
                self.so.seek(int.from_bytes(iter.st_value, byteorder="little"))
                obj = self.so.read(int.from_bytes(iter.st_size, byteorder="little"))
                ret_list.append(obj)
                for byte in obj:
                    dummy.append(int(byte))
                ret_list_int.append(dummy)
                dummy = []
        return ret_list_int

    def dump_symbol_idx(self):
        print(Colors.green + "symbol:" + Colors.ENDC)
        for iter in self.string_tb_e:
            print(Colors.blue + "name: " + Colors.cyan + repr(int.from_bytes(iter.st_name, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "size: " + Colors.cyan + repr(int.from_bytes(iter.st_size, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "value: " + Colors.cyan +  repr(int.from_bytes(iter.st_value, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "info: " + Colors.cyan +  repr(int.from_bytes(iter.st_info, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "other: " + Colors.cyan +  repr(int.from_bytes(iter.st_other, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "shndx: " + Colors.cyan +  repr(int.from_bytes(iter.st_shndx, byteorder="little")) + Colors.ENDC)
        print(Colors.green + "dyn symbol:" + Colors.ENDC)
        for iter in self.string_tb_e_dyn:
            print(Colors.blue + "name: " + Colors.cyan +  repr(int.from_bytes(iter.st_name, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "size: " + Colors.cyan +  repr(int.from_bytes(iter.st_size, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "value: " + Colors.cyan +  repr(int.from_bytes(iter.st_value, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "info: " + Colors.cyan +  repr(int.from_bytes(iter.st_info, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "other: " + Colors.cyan +  repr(int.from_bytes(iter.st_other, byteorder="little")) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "shndx: " + Colors.cyan +  repr(int.from_bytes(iter.st_shndx, byteorder="little")) + Colors.ENDC)

    def dump_header(self):
        print("------------------------------------------------------------------------------")
        print(Colors.green + "elf header:" + Colors.ENDC)
        print(Colors.blue + "ei_mag: " + Colors.cyan + repr(self.elfhdr.ei_mag) + Colors.ENDC)
        print(Colors.blue + "ei_class: " + Colors.cyan + repr(byte2int(self.elfhdr.ei_class)) + Colors.ENDC)
        print(Colors.blue + "ei_data: " + Colors.cyan + repr(byte2int(self.elfhdr.ei_data)) + Colors.ENDC)
        print(Colors.blue + "ei_version: " + Colors.cyan + repr(byte2int(self.elfhdr.ei_version)) + Colors.ENDC)
        print(Colors.blue + "ei_osabi: " + Colors.cyan + repr(byte2int(self.elfhdr.ei_osabi)) + Colors.ENDC)
        print(Colors.blue + "ei_abiversion: " + Colors.cyan + repr(byte2int(self.elfhdr.ei_abiversion)) + Colors.ENDC)
        print(Colors.blue + "ei_pad: " + Colors.cyan + repr(byte2int(self.elfhdr.ei_pad)) + Colors.ENDC)
        print(Colors.blue + "e_type: " + Colors.cyan + repr(byte2int(self.elfhdr.e_type)) + Colors.ENDC)
        print(Colors.blue + "e_machine: " + Colors.cyan + repr(byte2int(self.elfhdr.e_machine)) + Colors.ENDC)
        print(Colors.blue + "e_version: " + Colors.cyan + repr(byte2int(self.elfhdr.e_version)) + Colors.ENDC)
        print(Colors.blue + "e_entry: " + Colors.cyan + repr(byte2int(self.elfhdr.e_entry)) + Colors.ENDC)
        print(Colors.blue + "e_phoff: " + Colors.cyan + repr(byte2int(self.elfhdr.e_phoff)) + Colors.ENDC)
        print(Colors.blue + "e_shoff: " + Colors.cyan + repr(byte2int(self.elfhdr.e_shoff)) + Colors.ENDC)
        print(Colors.blue + "e_flags: " + Colors.cyan + repr(byte2int(self.elfhdr.e_flags)) + Colors.ENDC)
        print(Colors.blue + "e_ehsize: " + Colors.cyan + repr(byte2int(self.elfhdr.e_ehsize)) + Colors.ENDC)
        print(Colors.blue + "e_phentsize: " + Colors.cyan + repr(byte2int(self.elfhdr.e_phentsize)) + Colors.ENDC)
        print(Colors.blue + "e_phnum: " + Colors.cyan + repr(byte2int(self.elfhdr.e_phnum)) + Colors.ENDC)
        print(Colors.blue + "e_shentsize: " + Colors.cyan + repr(byte2int(self.elfhdr.e_shentsize)) + Colors.ENDC)
        print(Colors.blue + "e_shnum: " + Colors.cyan + repr(byte2int(self.elfhdr.e_shnum)) + Colors.ENDC)
        print(Colors.blue + "e_shstrndx: " + Colors.cyan + repr(byte2int(self.elfhdr.e_shstrndx)) + Colors.ENDC)
        print("------------------------------------------------------------------------------")

    def dump_phdrs(self):
        print(Colors.green + Colors.BOLD + "pheaders:" + Colors.ENDC)
        for i in range(0, int.from_bytes(self.elfhdr.e_phnum, byteorder="little", signed=False)):
            type = get_ph_type(byte2int(self.phdr[i].p_type))
            print(Colors.blue + "p_type: " + Colors.cyan + type + Colors.ENDC, end="")
            print(Colors.blue + " p_flags: " + Colors.cyan + repr(byte2int(self.phdr[i].p_flags)) + Colors.ENDC, end="")
            print(Colors.blue + " p_offset: " + Colors.cyan + repr(byte2int(self.phdr[i].p_offset)) + Colors.ENDC, end="")
            print(Colors.blue + " p_vaddr: " + Colors.cyan + repr(byte2int(self.phdr[i].p_vaddr)) + Colors.ENDC, end="")
            print(Colors.blue + " p_paddr: " + Colors.cyan + repr(byte2int(self.phdr[i].p_paddr)) + Colors.ENDC, end="")
            print(Colors.blue + " p_filesz: " + Colors.cyan + repr(byte2int(self.phdr[i].p_filesz)) + Colors.ENDC, end="")
            print(Colors.blue + " p_memsz: " + Colors.cyan + repr(byte2int(self.phdr[i].p_memsz)) + Colors.ENDC, end="")
            print(Colors.blue + " p_flags2: " + Colors.cyan + repr(self.phdr[i].p_flags2) + Colors.ENDC, end="")
            print(Colors.blue + " p_align: " + Colors.cyan + repr(byte2int(self.phdr[i].p_align)) + Colors.ENDC)

    def dump_shdrs(self):
        print(Colors.green + Colors.BOLD + "sheaders:" + Colors.ENDC)
        counter = int()
        for i in range(0, int.from_bytes(self.elfhdr.e_shnum, byteorder="little", signed=False)):
            name = self.read_section_name(byte2int(self.shhdr[i].sh_name))
            print(Colors.green + Colors.BOLD + repr(counter) + Colors.ENDC, end="")
            print("   ", end="")
            print(Colors.blue + "sh_name: " + Colors.cyan + name + Colors.ENDC, end="")
            print("\t", end="")
            type = get_section_type_string(byte2int(self.shhdr[i].sh_type))
            print(Colors.blue + "sh_type: " + Colors.cyan + type + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_flags: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_flags)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_addr: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_addr)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_offset: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_offset)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_size: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_size)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_link: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_link)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_info: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_info)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_addralign: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_addralign)) + Colors.ENDC, end="")
            print("\t", end="")
            print(Colors.blue + "sh_entsize: " + Colors.cyan + repr(byte2int(self.shhdr[i].sh_entsize)) + Colors.ENDC)
            counter += 1

    def dump_symbol_tb(self):
        for i in range(0, int.from_bytes(self.elfhdr.e_shnum, byteorder="little", signed=False)):
            if int.from_bytes(self.shhdr[i].sh_type, byteorder="little", signed=False) == sh_type_e.SHT_STRTAB:
                print(Colors.BOLD + Colors.yellow + "STRING TABLE:" + Colors.ENDC)
                self.so.seek(int.from_bytes(self.shhdr[i].sh_offset, byteorder="little", signed=False), 0)
                symbol_tb = self.so.read(int.from_bytes(self.shhdr[i].sh_size, byteorder="little", signed=False))
                for byte in symbol_tb:
                    print(chr(byte), end='')
                    if chr(byte) == '\0': print()

    def dump_st_entries(self):
        for entry in self.string_tb_e:
            print(Colors.green + "name: " + Colors.ENDC + repr(byte2int(entry.st_name)), end="")
            print(Colors.green + " value: " + Colors.ENDC + repr(byte2int(entry.st_value)), end="")
            print(Colors.green + " size: " + Colors.ENDC + repr(byte2int(entry.st_size)), end="")
            print(Colors.green + " info: " + Colors.ENDC + repr(byte2int(entry.st_info)), end="")
            print(Colors.green + " other: " + Colors.ENDC + repr(byte2int(entry.st_other)), end="")
            print(Colors.green + " shndx: " + Colors.ENDC + repr(byte2int(entry.st_shndx)))

    def get_symbol_string_table(self, offset):
        symbol = []
        for i in range(0, int.from_bytes(self.elfhdr.e_shnum, byteorder="little", signed=False)):
            if int.from_bytes(self.shhdr[i].sh_type, byteorder="little", signed=False) == sh_type_e.SHT_STRTAB:
                self.so.seek(int.from_bytes(self.shhdr[i].sh_offset, byteorder="little", signed=False) + offset - 0, 0)
                byte = self.so.read(1)
                while chr(byte[0]) != "\0":
                    if chr(byte[0]) != "\0": symbol.append(chr(byte[0]))
                    byte = self.so.read(1)
                return symbol

    def dump_inst_sections(self):
        indices= []
        for section in self.shhdr:
            if int.from_bytes(section.sh_flags, byteorder="little", signed=False) & sh_flags_e.SHF_EXECINSTR == sh_flags_e.SHF_EXECINSTR:
                indices.append(int.from_bytes(section.sh_name, byteorder="little"))
        return indices

    def pop_data_section(self):
        for section in self.shhdr:
            name = self.read_section_name(byte2int(section.sh_name))
            if name == ".data":
                self.so.seek(byte2int(section.sh_offset))
                self.data_section = self.so.read(byte2int(section.sh_size))

    def pop_text_section(self):
        for section in self.shhdr:
            name = self.read_section_name(byte2int(section.sh_name))
            if name == ".text":
                self.so.seek(byte2int(section.sh_offset))
                self.text_section = self.so.read(byte2int(section.sh_size))

class obj_loader():
    def __init__(self, bytes):
        self.memory = bytes()

    def load(self, obj):
        for byte in obj:
            self.memory.append(byte)

def ch_so_to_exe(path):
    so = open(path, "r+b")
    so.seek(16)
    so.write(bytes([2]))
    print(Colors.purple + "changed so to exe" + Colors.ENDC)
    so.close

def ch_exe_to_so(path):
    so = open(path, "r+b")
    so.seek(16)
    so.write(bytes([3]))
    print(Colors.purple + "changed exe to so" + Colors.ENDC)
    so.close

def main():
    #argparser = CLIArgParser()
    #if argparser.args.obj is None: so = openSO_r("./test/test.so")
    #else: so = openSO_r(argparser.args.obj)
    so = openSO_r(sys.argv[1])
    elf = ELF(so)
    elf.init(64)
    #elf.dump_header()
    #elf.dump_symbol_tb()
    #elf.dump_phdrs()
    #elf.dump_shdrs()
    #elf.dump_symbol_idx()
    #elf.dump_st_entries()
    #elf.dump_objs()

    return elf.dump_objs()
    #return 0;

if __name__ == "__main__":
    main()