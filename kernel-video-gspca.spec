# TODO:
#	- rename thiis to gspcav1 ?
#	- use the snapshot dates for %{version}? old versioning seems
#	  discontinued
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		ver	 01.00.20
%define		snap 20071224
%define 	rel	 0.1
Summary:	Linux Generic Software Package for Camera Adapters
Summary(pl.UTF-8):	Generic Software Package for Camera Adapters - pakiet do obsługi kamer pod Linuksem
Name:		gspca
Version:	%{ver}
Release:	1.%{snap}.%{rel}@%{_kernel_ver_str}
Epoch:		0
License:	GPL v2+
Group:		Base/Kernel
Source0:	http://mxhaard.free.fr/spca50x/Download/%{name}v1-%{snap}.tar.gz
# Source0-md5:	14853ba1f4edc1e685039fca56e5ebf2
Patch0:		http://connie.slackware.com/~alien/slackbuilds/gspcav1/build/%{name}_kernel_2.6.27.diff
Patch1:		http://connie.slackware.com/~alien/slackbuilds/gspcav1/build/%{name}v1_nodebug.patch
URL:		http://mxhaard.free.fr/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		module_dir	kernel/drivers/media/video

%description
GSPCA is a Linux Generic Software Package for Camera Adapters. It
supports cameras cameras based on spca5xx, et61xx51, zc030x, sn9c1xx,
cx11646, tv_8532, pac207, vc032x chips.

%description -l pl.UTF-8
GSPCA to ogólny pakiet oprogramowania do obsługi kamer dla Linuksa.
Obsługuje kamery oparte na układach spca5xx, et61xx51, zc030x,
sn9c1xx, cx11646, tv_8532, pac207, vc032x

%package -n kernel%{_alt_kernel}-video-%{name}
Summary:	Generic Software Package for Camera Adapters - Linux kernel module
Summary(pl.UTF-8):	Oprogramowanie do obsługi kamer - moduł jądra Linuksa
Release:	1.%{snap}.%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
%endif

%description -n kernel%{_alt_kernel}-video-%{name}
GSPCA is a Linux Generic Software Package for Camera Adapters. It
supports cameras cameras based on spca5xx, et61xx51, zc030x, sn9c1xx,
cx11646, tv_8532, pac207, vc032x chips.

This package contains Linux kernel module.

%description -n kernel%{_alt_kernel}-video-%{name} -l pl.UTF-8
GSPCA to ogólny pakiet oprogramowania do obsługi kamer dla Linuksa.
Obsługuje kamery oparte na układach spca5xx, et61xx51, zc030x,
sn9c1xx, cx11646, tv_8532, pac207, vc032x.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n %{name}v1-%{snap}
%patch0 -p1
%patch1 -p1

%build
%if %{with kernel}
%build_kernel_modules -m gspca
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m gspca -d %{module_dir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/%{module_dir}/gspca.ko*
%endif
