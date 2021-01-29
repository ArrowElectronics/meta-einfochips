inherit pypi setuptools
require python-scipy.inc

do_install_prepend() {
        export OPENBLAS="${STAGING_LIBDIR}"
        mv ${WORKDIR}/build_ext.py ${STAGING_LIBDIR_NATIVE}/python2.7/site-packages/numpy/distutils/command
        mv ${WORKDIR}/exec_command.py ${STAGING_LIBDIR_NATIVE}/python2.7/site-packages/numpy/distutils/
        mv ${WORKDIR}/gnu.py ${STAGING_LIBDIR_NATIVE}/python2.7/site-packages/numpy/distutils/fcompiler
        mv ${WORKDIR}/system_info.py ${STAGING_LIBDIR_NATIVE}/python2.7/site-packages/numpy/distutils/
}
