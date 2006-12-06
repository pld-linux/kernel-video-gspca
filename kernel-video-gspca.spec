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
Summary:	Linux driver for spca5xx
Summary(pl):	Sterownik dla Linuksa do spca5xx
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
This is version %{_ver} of the spca5xx Video for Linux (v4l) driver,
providing support for webcams and digital cameras based on the spca5xx
range of chips manufactured by SunPlus Sonix Z-star Vimicro Conexant
Etoms and Transvision.

This package contains Linux module.

%package -n kernel%{_alt_kernel}-video-%{name}
Summary:	Linux driver for Philips USB webcams
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-video-%{name}
This is driver for Philips USB webcams for Linux.

This package contains Linux module. File is called
%{_module_file_name}.

%description -n kernel%{_alt_kernel}-video-%{name} -l pl
Sterownik dla Linuksa do kamer internetowych Philipsa.

Ten pakiet zawiera modu³ j±dra Linuksa. Plik nazywa siê
%{_module_file_name}.

%package -n kernel%{_alt_kernel}-smp-video-%{name}
Summary:	Linux SMP driver for spca
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-video-%{name}
This is version %{_ver} the spca5xx video for linux (v4l) driver,
providing support for webcams and digital cameras based on the spca5xx
range of chips manufactured by SunPlus Sonix Z-star Vimicro Conexant
Etoms and Transvision.

This is driver for spca5xx for Linux.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-video-%{name} -l pl
To jest wersja %{_ver} sterownika Video for Linux (v4l) spca5xx
dodaj±cego obs³ugê dla kamer i aparatów opartych na uk³adach spca5xx
produkowanych przez SunPlus Sonix Z-star Vimicro Conexant Etoms and
Transvision.

Sterownik dla Linuksa do spca5xx.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

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
