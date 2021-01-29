SUMMARY = "SciPy (pronounced “Sigh Pie”) is open-source software for mathematics, science, and engineering"
HOMEPAGE = "https://www.scipy.org/"
LICENSE = "CLOSED"

SRC_URI += "file://build_ext.py;md5=dbeda8d8aa81df8647349a5b01414e03 \
		file://exec_command.py;md5=c7d4dc1042bb169fb00bf3877c0b55dd \
		file://gnu.py;md5=594731942b5d346d249c7447f8cc6cea \
		file://system_info.py;md5=a19ca37110dd01200ed27aa0aac09ca3"

SRC_URI[md5sum] = "aa6bcc85276b6f25e17bcfc4dede8718"
SRC_URI[sha256sum] = "878352408424dffaa695ffedf2f9f92844e116686923ed9aa8626fc30d32cfd1"

CLEANBROKEN = "1"

DEPENDS = " \
		libgfortran \
		openblas \
		openblas-dev \
		${PYTHON_PN}-numpy \
		${PYTHON_PN}-numpy-native \
"

RDEPENDS_${PN} = " \
		openblas \
		libgfortran \
		${PYTHON_PN}-matplotlib \
		${PYTHON_PN}-ipython \
		${PYTHON_PN}-jupyter \
		${PYTHON_PN}-pandas \
		${PYTHON_PN}-sympy \
		${PYTHON_PN}-nose \
"

PYPI_PACKAGE = "scipy"

#BUILD_CFLAGS_append = " -L${STAGING_LIBDIR}/python3.5/site-packages/numpy/core/lib"
#BUILD_LDFLAGS_append = " -L${STAGING_LIBDIR}/python3.5/site-packages/numpy/core/lib"
LDSHARED_append = " -L${STAGING_LIBDIR}/python3.5/site-packages/numpy/core/lib"
CFLAGS_append = " -L${STAGING_LIBDIR}/python3.5/site-packages/numpy/core/lib"
LDFLAGS_append = " -L${STAGING_LIBDIR}/python3.5/site-packages/numpy/core/lib"

do_compile[noexec] = "1"
