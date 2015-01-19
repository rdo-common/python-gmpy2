%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_py3 1
%endif

%global pkgname gmpy2

Name:           python-%{pkgname}
Version:        2.0.5
Release:        1%{?dist}
Summary:        Python 2 interface to GMP, MPFR, and MPC

# All source files are LGPLv3+ except:
# - src/py3intcompat.c is Python
# - src/mpz_pylong.c is LGPLv2+
License:        LGPLv3+ and Python
URL:            https://pypi.python.org/pypi/gmpy2
Source0:        https://pypi.python.org/packages/source/g/%{pkgname}/%{pkgname}-%{version}.zip

BuildRequires:  gmp-devel
BuildRequires:  libmpc-devel
BuildRequires:  mpfr-devel
BuildRequires:  python2-devel
BuildRequires:  python-sphinx

%if 0%{?with_py3}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
%endif

Provides:       bundled(jquery)

%global common_desc \
This package contains a C-coded Python extension module that supports \
multiple-precision arithmetic.  It is the successor to the original \
gmpy module.  The gmpy module only supported the GMP multiple-precision \
library.  Gmpy2 adds support for the MPFR (correctly rounded real \
floating-point arithmetic) and MPC (correctly rounded complex \
floating-point arithmetic) libraries.  It also updates the API and \
naming conventions to be more consistent and support the additional \
functionality.

%description
%{common_desc}

%if 0%{?with_py3}
%package -n python3-%{pkgname}
Summary:        Python 3 interface to GMP, MPFR, and MPC
Provides:       bundled(jquery)

%description -n python3-%{pkgname}
%{common_desc}
%endif

%prep
%setup -q -c

# Fix file encodings.  First the easy one.
pushd %{pkgname}-%{version}
iconv -f ISO8859-1 -t UTF-8 src/gmpy2.c > src/gmpy2.c.utf8
touch -r src/gmpy2.c src/gmpy2.c.utf8
mv -f src/gmpy2.c.utf8 src/gmpy2.c

# Now the hard one.  What weird encoding is this, anyway?
sed -i.orig 's/i\xad/\xc3\xad/' src/mpz_pylong.c
touch -r src/mpz_pylong.c.orig src/mpz_pylong.c
rm src/mpz_pylong.c.orig
popd

%if 0%{?with_py3}
# Prepare for a python3 build
cp -a %{pkgname}-%{version} python3-%{pkgname}-%{version}
sed -i 's/sphinx-build/&-3/' python3-%{pkgname}-%{version}/docs/Makefile
%endif

%build
# Adapt to 64-bit systems
if [ "%{_libdir}" = "%{_prefix}/lib64" ]; then
  ARGS=--lib64
else
  ARGS=
fi

# Python 2 build
pushd %{pkgname}-%{version}
%{__python2} setup.py $ARGS build
make -C docs html
popd

%if 0%{?with_py3}
# Python 3 build
pushd python3-%{pkgname}-%{version}
%{__python3} setup.py $ARGS build
make -C docs html
popd
%endif

%install
# Python 2 install
pushd %{pkgname}-%{version}
%{__python2} setup.py $ARGS install -O1 --skip-build --root %{buildroot}
chmod 0755 %{buildroot}%{python2_sitearch}/*.so
popd
 
%if 0%{?with_py3}
# Python 3 install
pushd python3-%{pkgname}-%{version}
%{__python3} setup.py $ARGS install -O1 --skip-build --root %{buildroot}
chmod 0755 %{buildroot}%{python3_sitearch}/*.so
popd
%endif

%check
# Python 2 tests
pushd %{pkgname}-%{version}
PYTHONPATH=%{buildroot}%{python2_sitearch} %{__python2} test/runtests.py
popd

%if 0%{?with_py3}
# Python 3 tests
pushd python3-%{pkgname}-%{version}
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} test/runtests.py
popd
%endif

%files
%license %{pkgname}-%{version}/COPYING %{pkgname}-%{version}/COPYING.LESSER
%doc %{pkgname}-%{version}/docs/_build/html/*
%{python2_sitearch}/%{pkgname}*

%if 0%{?with_py3}
%files -n python3-%{pkgname}
%license %{pkgname}-%{version}/COPYING %{pkgname}-%{version}/COPYING.LESSER
%doc python3-%{pkgname}-%{version}/docs/_build/html/*
%{python3_sitearch}/%{pkgname}*
%endif

%changelog
* Mon Jan 19 2015 Jerry James <loganjerry@gmail.com> - 2.0.5-1
- New upstream release
- Drop patch for 32-bit systems, fixed upstream

* Mon Oct 13 2014 Jerry James <loganjerry@gmail.com> - 2.0.4-1
- New upstream release

* Fri Sep 12 2014 Jerry James <loganjerry@gmail.com> - 2.0.3-2
- BR python2-devel instead of python-devel
- Provide bundled(jquery)

* Fri Sep  5 2014 Jerry James <loganjerry@gmail.com> - 2.0.3-1
- Initial RPM
