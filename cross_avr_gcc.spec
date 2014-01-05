Summary:	Cross GNU Compiler Collection for the x86_64 architecture
Name:		cross_avr_gcc
Version:	4.8.2
Release:	3
License:	GPL v3+
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	a3d7d63b9cb6b6ea049469a0c4a43c9d
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	cloog-devel
BuildRequires:	coreutils
BuildRequires:	cross_avr_binutils
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	isl-devel
BuildRequires:	mpc-devel
BuildRequires:	mpfr-devel
BuildRequires:	texinfo
Requires:	cross_avr_binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}
%define		_slibdir	%{_libdir}

%define         target          avr
%define         arch            %{_prefix}/%{target}
%define         gccarch         %{_libdir}/gcc/%{target}
%define         gcclib          %{gccarch}/%{version}

%define         _noautostrip    .*/lib.*\\.a

%define		debug_package	%{nil}

%description
Cross GNU Compiler Collection for the x86_64 architecture.

%prep
%setup -qn gcc-%{version}

%if 0
# undefined reference to `__stack_chk_guard'
sed -i '/k prot/agcc_cv_libc_provides_ssp=yes' gcc/configure
%endif

# override snapshot version.
echo %{version} > gcc/BASE-VER
echo "release" > gcc/DEV-PHASE

%build
install -d obj-%{target}
cd obj-%{target}

TEXCONFIG=false				\
CFLAGS="%{rpmcflags}"			\
CXXFLAGS="%{rpmcxxflags}"	\
LDFLAGS="%{rpmldflags}"			\
../configure				\
	--build=%{_build}		\
	--host=%{_host}			\
	--target=%{target}		\
	--bindir=%{_bindir}		\
	--infodir=%{_infodir} 		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--mandir=%{_mandir}		\
	--prefix=%{_prefix}		\
	--sbindir=%{_sbindir}		\
	--disable-cloog-version-check	\
	--disable-install-libiberty	\
	--disable-libssp		\
	--disable-libstdcxx-pch		\
	--disable-libunwind-exceptions	\
	--disable-linker-build-id	\
	--disable-nls			\
	--enable-__cxa_atexit		\
	--enable-clocale=gnu		\
	--enable-cloog-backend=isl	\
	--enable-gnu-unique-object	\
	--enable-languages=c,c++	\
	--enable-lto			\
	--enable-plugin			\
	--enable-shared			\
	--with-pkgversion="Freddix"
cd ..

%{__make} -C obj-%{target} \
	CFLAGS_FOR_TARGET="-O2"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}}

%{__make} -C obj-%{target} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install obj-%{target}/gcc/specs $RPM_BUILD_ROOT%{gcclib}

gccdir=$RPM_BUILD_ROOT%{gcclib}
mv $gccdir/include-fixed/*.h $gccdir/include
%{__rm} -r $gccdir/include-fixed
%{__rm} -r $gccdir/install-tools
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{gccarch}
%dir %{gcclib}
%dir %{gcclib}/include
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-gcov
%attr(755,root,root) %{gcclib}/*.a
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%attr(755,root,root) %{gcclib}/lto-wrapper
%attr(755,root,root) %{gcclib}/liblto_plugin.so*
%attr(755,root,root) %{gcclib}/lto1
%{gcclib}/%{target}*
%{gcclib}/tiny-stack
%{gcclib}/include/*.h
%{gcclib}/plugin
%{gcclib}/specs

%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*

%attr(755,root,root) %{_bindir}/%{target}-c++
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{gcclib}/cc1plus
%{_mandir}/man1/%{target}-g++.1*

