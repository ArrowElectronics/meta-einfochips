DESCRIPTION = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version." 
SUMMARY = "OpenBLAS : An optimized BLAS library" 
HOMEPAGE = "http://www.openblas.net/" 
SECTION = "libs" 
LICENSE = "BSD-3-Clause" 


DEPENDS = "make" 
DEPENDS += "libgfortran" 


LIC_FILES_CHKSUM = "file://LICENSE;md5=5adf4792c949a00013ce25d476a2abc0" 


SRC_URI = "https://github.com/xianyi/OpenBLAS/archive/v${PV}.tar.gz" 
SRC_URI[md5sum] = "42cde2c1059a8a12227f1e6551c8dbd2" 
SRC_URI[sha256sum] = "cf51543709abe364d8ecfb5c09a2b533d2b725ea1a66f203509b21a8e9d8f1a1" 

S = "${WORKDIR}/OpenBLAS-${PV}" 

do_compile () { 
#    if [ ${DEFAULTTUNE} = "aarch64" ]; then
        oe_runmake TARGET=ARMV8     \
                                HOSTCC="${BUILD_CC}"                                         \ 
								AR="${TARGET_PREFIX}ar"                        \
                                BINARY=64 NOFORTRAN=0 NO_LAPACK=1 USE_THREAD=0
		oe_runmake -C utest TARGET=ARMV8     \
                                HOSTCC="${BUILD_CC}"                                         \ 
                                BINARY=64 NOFORTRAN=0 NO_LAPACK=1 USE_THREAD=0
#	else
#	    oe_runmake TARGET=ARMV7     \
#                                HOSTCC="${BUILD_CC}"                                         \ 
#								AR="${TARGET_PREFIX}ar"                        \
#                               NOFORTRAN=0 NO_LAPACK=1 USE_THREAD=0
#		oe_runmake -C utest TARGET=ARMV7     \
#                               HOSTCC="${BUILD_CC}"                                         \ 
#                                NOFORTRAN=0 NO_LAPACK=1 USE_THREAD=0
#	fi
} 


do_install () {
	    oe_runmake install PREFIX="${D}/opt/${PN}"
		cp ${WORKDIR}/OpenBLAS-${PV}/utest/openblas_utest ${D}/opt/${PN}/bin
	    rm -rf ${D}${libdir}/cmake 
} 


FILES_${PN}     += "/opt/${PN}" 
FILES_${PN}-dev += "/opt/${PN}/lib/lib${PN}.so"
INSANE_SKIP_${PN} += "staticdev"
