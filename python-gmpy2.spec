%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_py3 1
%endif

%global srcname gmpy2

Name:           python-%{srcname}
Version:        2.0.8
Release:        4%{?dist}
Summary:        Python interface to GMP, MPFR, and MPC

# All source files are LGPLv3+ except:
# - src/py3intcompat.c is Python
# - src/mpz_pylong.c is LGPLv2+
License:        LGPLv3+ and Python
URL:            https://pypi.python.org/pypi/gmpy2
Source0:        https://files.pythonhosted.org/packages/source/g/%{srcname}/%{srcname}-%{version}.zip

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  libmpc-devel
BuildRequires:  mpfr-devel
BuildRequires:  python2-devel
BuildRequires:  python2-sphinx

%if 0%{?with_py3}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
%endif

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

%package -n python2-%{srcname}
Summary:        Python 2 interface to GMP, MPFR, and MPC

Provides:       bundled(jquery)
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{common_desc}

%if 0%{?with_py3}
%package -n python3-%{srcname}
Summary:        Python 3 interface to GMP, MPFR, and MPC

Provides:       bundled(jquery)
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{common_desc}
%endif

%prep
%setup -q -c

pushd %{srcname}-%{version}

# Fix file encodings.  First the easy one.
iconv -f ISO8859-1 -t UTF-8 src/gmpy2.c > src/gmpy2.c.utf8
touch -r src/gmpy2.c src/gmpy2.c.utf8
mv -f src/gmpy2.c.utf8 src/gmpy2.c

# Now the hard one.  What weird encoding is this, anyway?
sed -i.orig 's/i\xad/\xc3\xad/' src/mpz_pylong.c
touch -r src/mpz_pylong.c.orig src/mpz_pylong.c
rm src/mpz_pylong.c.orig
popd

%if 0%{?fedora} >= 24
# Update the sphinx theme name
sed -i 's/default/alabaster/' %{srcname}-%{version}/docs/conf.py
%endif

%if 0%{?with_py3}
# Prepare for a python3 build
cp -a %{srcname}-%{version} python3-%{srcname}-%{version}
sed -i 's/sphinx-build/&-3/' python3-%{srcname}-%{version}/docs/Makefile
%endif

%build
# Adapt to 64-bit systems
%if "%{_libdir}" == "%{_prefix}/lib64"
%global py_setup_args "--lib64"
%endif

# Python 2 build
pushd %{srcname}-%{version}
%py2_build
make -C docs html
popd

%if 0%{?with_py3}
# Python 3 build
pushd python3-%{srcname}-%{version}
%py3_build
make -C docs html
popd
%endif

%install
# Python 2 install
pushd %{srcname}-%{version}
%py2_install
chmod 0755 %{buildroot}%{python2_sitearch}/*.so
popd
 
%if 0%{?with_py3}
# Python 3 install
pushd python3-%{srcname}-%{version}
%py3_install
chmod 0755 %{buildroot}%{python3_sitearch}/*.so
popd
%endif

%check
# Python 2 tests
pushd %{srcname}-%{version}
PYTHONPATH=%{buildroot}%{python2_sitearch} %{__python2} test/runtests.py
popd

%if 0%{?with_py3}
# Python 3 tests
pushd python3-%{srcname}-%{version}
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} test/runtests.py
popd
%endif

%files -n python2-%{srcname}
%license %{srcname}-%{version}/COPYING %{srcname}-%{version}/COPYING.LESSER
%doc %{srcname}-%{version}/docs/_build/html/*
%{python2_sitearch}/%{srcname}*

%if 0%{?with_py3}
%files -n python3-%{srcname}
%license %{srcname}-%{version}/COPYING %{srcname}-%{version}/COPYING.LESSER
%doc python3-%{srcname}-%{version}/docs/_build/html/*
%{python3_sitearch}/%{srcname}*
%endif

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.8-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Jerry James <loganjerry@gmail.com> - 2.0.8-1
- New upstream release
- Drop upstreamed -decref patch

* Fri Mar 25 2016 Jerry James <loganjerry@gmail.com> - 2.0.7-4
- Add -decref patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Jerry James <loganjerry@gmail.com> - 2.0.7-2
- Comply with latest python packaging guidelines

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Aug 22 2015 Jerry James <loganjerry@gmail.com> - 2.0.7-1
- New upstream release

* Mon Jul  6 2015 Jerry James <loganjerry@gmail.com> - 2.0.6-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

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
