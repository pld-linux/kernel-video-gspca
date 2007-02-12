#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_ver 01.00.10
%define		_rel	0.1
Summary:	Linux Generic Software Package for Camera Adapters
Summary(pl.UTF-8):   Generic Software Package for Camera Adapters - pakiet do obsługi kamer pod Linuksem
Name:		gspca
Version:	%{_ver}
Release:	%{_rel}@%{_kernel_ver_str}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://mxhaard.free.fr/spca50x/Investigation/Gspca/%{name}v1-%{version}.tar.gz
# Source0-md5:	39e4fb7fe47c2ef489b1f10b3b482253
URL:		http://mxhaard.free.fr/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_module_dir	kernel/drivers/media/video

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
Summary(pl.UTF-8):   Oprogramowanie do obsługi kamer - moduł jądra Linuksa
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
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

%package -n kernel%{_alt_kernel}-smp-video-%{name}
Summary:	Generic Software Package for Camera Adapters - Linux SMP kernel module
Summary(pl.UTF-8):   Oprogramowanie do obsługi kamer - moduł jądra Linuksa SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-video-%{name}
GSPCA is a Linux Generic Software Package for Camera Adapters. It
supports cameras cameras based on spca5xx, et61xx51, zc030x, sn9c1xx,
cx11646, tv_8532, pac207, vc032x chips.

This package contains Linux SMP kernel module.

%description -n kernel%{_alt_kernel}-smp-video-%{name} -l pl.UTF-8
GSPCA to ogólny pakiet oprogramowania do obsługi kamer dla Linuksa.
Obsługuje kamery oparte na układach spca5xx, et61xx51, zc030x,
sn9c1xx, cx11646, tv_8532, pac207, vc032x.

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -n %{name}v1-%{version}

%build
%if %{with kernel}
%build_kernel_modules -m gspca
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m gspca -d %{_module_dir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-video-%{name}
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-video-%{name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/%{_module_dir}/gspca.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-video-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/%{_module_dir}/gspca.ko*
%endif
%endif
