# Copyright (C) 2021 Tejas Patel <tejas.patel1@einfochips.com>
# Released under the MIT license (see COPYING.MIT for the terms)

SUMMARY = "A toolkit for making real world machine learning and data analysis applications"
HOMEPAGE = "http://dlib.net/"
SECTION = "devel/python"
LICENSE = "BSL-1.0"
LIC_FILES_CHKSUM = "file://dlib/LICENSE.txt;md5=2c7a3fa82e66676005cd4ee2608fd7d2"              

DEPENDS = "sqlite3"

SRC_URI = "git://github.com/davisking/dlib"
SRCREV = "9117bd784328d9ac40ffa1f9cf487633a8a715d7"

S = "${WORKDIR}/git"

DISTUTILS_BUILD_ARGS_append = " \
      --set CMAKE_INSTALL_PREFIX:PATH=${prefix} \
      --set CMAKE_INSTALL_BINDIR:PATH=${@os.path.relpath(d.getVar('bindir'), d.getVar('prefix') + '/')} \
      --set CMAKE_INSTALL_SBINDIR:PATH=${@os.path.relpath(d.getVar('sbindir'), d.getVar('prefix') + '/')} \
      --set CMAKE_INSTALL_LIBEXECDIR:PATH=${@os.path.relpath(d.getVar('libexecdir'), d.getVar('prefix') + '/')} \
      --set CMAKE_INSTALL_SYSCONFDIR:PATH=${sysconfdir} \
      --set CMAKE_INSTALL_SHAREDSTATEDIR:PATH=${@os.path.relpath(d.getVar('sharedstatedir'), d.  getVar('prefix') + '/')} \
      --set CMAKE_INSTALL_LOCALSTATEDIR:PATH=${localstatedir} \
      --set CMAKE_INSTALL_LIBDIR:PATH=${@os.path.relpath(d.getVar('libdir'), d.getVar('prefix') + '/')} \
      --set CMAKE_INSTALL_INCLUDEDIR:PATH=${@os.path.relpath(d.getVar('includedir'), d.getVar('prefix') + '/')} \
      --set CMAKE_INSTALL_DATAROOTDIR:PATH=${@os.path.relpath(d.getVar('datadir'), d.getVar('prefix') + '/')} \
      --set PYTHON_EXECUTABLE:PATH=${PYTHON} \
      --set Python_EXECUTABLE:PATH=${PYTHON} \
      --set Python3_EXECUTABLE:PATH=${PYTHON} \
      --set LIB_SUFFIX=${@d.getVar('baselib').replace('lib', '')} \
      --set CMAKE_INSTALL_SO_NO_EXE=0 \
      --set CMAKE_TOOLCHAIN_FILE=${WORKDIR}/toolchain.cmake \
      --set CMAKE_NO_SYSTEM_FROM_IMPORTED=1 \
      --set CMAKE_LIBRARY_OUTPUT_DIRECTORY=${B} \
"

do_configure() {
    distutils3_do_configure
}

do_compile() {
    distutils3_do_compile
}

do_install() {
    distutils3_do_install
}

inherit cmake setuptools3 python3native

INSANE_SKIP_${PN} = "already-stripped"
RDEPENDS_${PN} += "python3-core"
