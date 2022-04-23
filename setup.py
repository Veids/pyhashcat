# Pyhashcat setup module

from setuptools import setup, Extension
import sys
import os

DEFAULT_EXT_NAME = "pyhashcat"
DEFAULT_EXT_VERS = "4.0"
DEFAULT_EXT_DESC = "Python bindings for hashcat"
ENV_DIR_MY_SOURCES = "MY_SOURCES"
ENV_DIR_HC_SOURCES_DIR = "HC_SOURCES_DIR"
ENV_DIR_HC_LIB_DIR = "HC_LIB_DIR"
DEFAULT_MY_SOURCES_DIR = "./"
DEFAULT_HC_SOURCES_DIR = "./hashcat"
DEFAULT_HC_LIB_DIR = "/usr/local/lib"
DEFAULT_HC_ADD_CFLAGS = ["-DWITH_BRAIN", "-DWITH_CUBIN", "-DWITH_HWMON"]
NAMEHINT_HC_LIB = "libhashcat."
MY_SOURCES_FILES = [
	"pyhashcat.c",
]
HC_REL_INCLUDES = [
	"include",
	"OpenCL",
	"deps/OpenCL-Headers",
	"deps/zlib",
	"deps/zlib/contrib",
	"deps/LZMA-SDK/C",
	"deps/xxHash",
	"deps/unrar"
]

def buildmyfiles(my_sources_dir, relfiles):
	ret = None
	if os.path.isdir(my_sources_dir):
		relslen = len(relfiles)
		absfiles = []
		for relfile in relfiles:
			absfile = os.path.join(my_sources_dir, relfile)
			if os.path.isfile(absfile):
				if absfile not in absfiles:
					absfiles.append(absfile)
			else:
				break
		if relslen == len(absfiles):
			ret = absfiles
	return ret

def findhclib(hc_lib_dir, libhint):
	ret = None
	libfiles = os.listdir(hc_lib_dir)
	for f in libfiles:
		if f and f.startswith(libhint):
			#ret = os.path.join(hc_lib_dir, f)
			ret = f
			break
	return ret

def buildincludes(hc_sources_dir, relincludes):
	ret = None
	if os.path.isdir(hc_sources_dir):
		relslen = len(relincludes)
		absincludes = []
		for relinclude in relincludes:
			absinclude = os.path.join(hc_sources_dir, relinclude)
			if os.path.isdir(absinclude):
				if absinclude not in absincludes:
					absincludes.append(absinclude)
			else:
				break
		if relslen == len(absincludes):
			ret = absincludes
	return ret

my_sources_dir = os.environ.get(ENV_DIR_MY_SOURCES, DEFAULT_MY_SOURCES_DIR)
hc_sources_dir = os.environ.get(ENV_DIR_HC_SOURCES_DIR, DEFAULT_HC_SOURCES_DIR)
hc_lib_dir = os.environ.get(ENV_DIR_HC_LIB_DIR, DEFAULT_HC_LIB_DIR)

my_files = buildmyfiles(my_sources_dir, MY_SOURCES_FILES)
if my_files is None:
	print(f"My own sources files could not be found in '{my_sources_dir}', please define '{ENV_DIR_MY_SOURCES}' environment variable", file=sys.stderr)
	sys.exit(10)
hc_includes = buildincludes(hc_sources_dir, HC_REL_INCLUDES)
if hc_includes is None:
	print(f"Hashcat required sources files could not be found in '{hc_sources_dir}', please define '{ENV_DIR_HC_SOURCES_DIR}' environment variable", file=sys.stderr)
	sys.exit(11)
hc_lib = findhclib(hc_lib_dir, NAMEHINT_HC_LIB)
if hc_lib is None:
	print(f"Hashcat shared library could not be found in '{hc_lib_dir}', please define '{ENV_DIR_HC_LIB_DIR}' environment variable", file=sys.stderr)
	sys.exit(12)

print("My sources files:")
for i in my_files:
	print(f"\t{i}")
print("Hashcat shared library:", os.path.join(hc_lib_dir, hc_lib))
print("Hashcat sources dirs:")
for i in hc_includes:
	print(f"\t{i}")

hc_libs_linkinc = None
hc_extra_linkargs = None
if sys.platform == "linux":
	hc_libs_linkinc = ["stdc++", "pthread", "dl", "rt", "m", f":{hc_lib}"]
	hc_extra_linkargs = ["-shared"]
elif sys.platform == "darwin":
	hc_libs_linkinc = ["stdc++", "pthread", "iconv", os.path.splitext(hc_lib)[0].lstrip("lib")]
	hc_extra_linkargs = ["-framework", "CoreFoundation", "-framework", "Foundation", "-framework", "IOKit", "-framework", "CoreGraphics", "-framework", "Metal"]
else:
	print("pyhashcat building is currently only supported on Linux and macOS", file=sys.stderr)
	sys.exit(20)

print(f"Building on '{sys.platform}'")

pyhashcat_module = 	Extension(
						DEFAULT_EXT_NAME,
						sources = my_files,
						include_dirs = hc_includes,
						extra_compile_args = DEFAULT_HC_ADD_CFLAGS,
						library_dirs = [hc_lib_dir],
						libraries = hc_libs_linkinc,
						extra_link_args = hc_extra_linkargs,
					)

setup(
	name = DEFAULT_EXT_NAME,
	version = DEFAULT_EXT_VERS,
	description = DEFAULT_EXT_DESC,
	ext_modules = [pyhashcat_module]
)
