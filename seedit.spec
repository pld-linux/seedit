Summary:	SELinux Policy Editor (SEEdit)
Summary(pl.UTF-8):	SELinux Policy Editor (SEEdit)
Name:		seedit
Version:	2.1.2
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://downloads.sourceforge.net/seedit/%{name}-%{version}.tar.gz
# Source0-md5:	2c9b44bd9a14b2e60fb1987161c6a797
#Source1:	%{name}-gui.desktop
#Source2:	%{name}-gui.png
URL:		http://seedit.sourceforge.net/
BuildRequires:	byacc
BuildRequires:	desktop-file-utils
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	libselinux-devel >= 1.19
BuildRequires:	libsepol-devel >= 1.1.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
%pyrequires_eq	python-libs
Requires:	audit
Requires:	checkpolicy
Requires:	libselinux >= 1.19
Requires:	libsepol >= 1.1.1
Requires:	m4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SELinux Policy Editor(SEEdit) is a tool to make SELinux easy.
SEEdit is composed of Simplified Policy, command line utils and GUI.
The main feature is Simplified Policy.
Simplified Policy is written in Simplified Policy Description Language(SPDL).
SPDL hides detail of SELinux.

%description -l pl.UTF-8

%package gui
Summary:	GUI for SELinux Policy Editor
Summary(pl.UTF-8):	Interfejs graficzny dla SELinux Policy Editor
Group:		X11/Aplications
Requires:	usermode
Requires:	pygtk2
Requires:	pam >= 0.80-9
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-policy = %{version}-%{release}

%description gui
X based GUI for SELinux Policy Editor.

%package policy
Summary:	SELinux Policy Editor: Sample simplified policy
Group:		-
Requires:	%{name} = %{version}-%{release}

%description policy
Sample simplified policy for SEEdit.

%prep
%setup -q

%build

PYTHON_SITELIB=%{py_sitedir}/
CUSTOMIZABLE_TYPE=y
MODULAR=y
PAM_INCLUDE_SUPPORT=y
AUDIT_OBJ_TYPE_SUPPORT=y
POLICYTYPE=easy
AUDITRULES=%{_sysconfdir}/audit/audit.rules
SELINUXCONFIG=%{_sysconfdir}/selinux
DEVELFLAG=0
SELINUXTYPE=seedit

export PYTHON_SITELIB CUSTOMIZABLE_TYPE MODULAR PAM_INCLUDE_SUPPORT AUDIT_OBJ_TYPE_SUPPORT POLICYTYPE AUDITRULES DEVELFLAG SELINUXTYPE

cd core
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"
cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

cd core
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..
cd gui
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..
cd policy
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install %{SOURCE1} ${RPM_BUILD_ROOT}%{_desktopdir}
#install %{SOURCE2} ${RPM_BUILD_ROOT}%{_pixmapspdir}

touch ${RPM_BUILD_ROOT}%{_datadir}/%{name}/sepolicy/need-rbac-init
touch ${RPM_BUILD_ROOT}%{_datadir}/%{name}/sepolicy/need-init

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post policy
if [ "$1" = "1" ]; then
	#Mark to initialize SELinux Policy Editor, when new install
	touch %{_datadir}/%{name}/sepolicy/need-init
fi

if [ "$1" = "2" ]; then
	#Mark to initialize RBAC config when upgrade
	touch %{_datadir}/%{name}/sepolicy/need-rbac-init
fi

%postun policy
if [ "$1" = "0" ]; then
	sed -i 's/^SELINUXTYPE=.*/SELINUXTYPE=targeted/g' %{_sysconfdir}/selinux/config
	if [ %{selinuxenabled} ]; then
		sed -i 's/^SELINUX=.*/SELINUX=permissive/g' %{_sysconfdir}/selinux/config
	fi
	touch /.autorelabel
fi

%find_lang %{name}

%files
%defattr(644,root,root,755)
%doc README Changelog COPYING AUTHORS NEWS TODO
%attr(755,root,root) %{_bindir}/seedit-converter
%attr(755,root,root) %{_bindir}/audit2spdl
%attr(755,root,root) %{_sbindir}/seedit-rbac
%attr(755,root,root) %{_sbindir}/seedit-load
%attr(755,root,root) %{_sbindir}/seedit-restorecon
%attr(755,root,root) %{_bindir}/seedit-unconfined
%attr(755,root,root) %{_bindir}/seedit-template
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Makefile
%{_datadir}/%{name}/macros
%{_datadir}/%{name}/base_policy
%dir %{_datadir}/%{name}/sepolicy
%{_datadir}/%{name}/seedit-load.conf

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/seedit-gui
%attr(755,root,root) %{_sbindir}/seedit-gui
%attr(755,root,root) %{_sbindir}/seedit-gui-status
%attr(755,root,root) %{_sbindir}/seedit-gui-domain-manager
%attr(755,root,root) %{_sbindir}/seedit-gui-role-manager
%attr(755,root,root) %{_sbindir}/seedit-gui-generate-policy
%attr(755,root,root) %{_sbindir}/seedit-gui-edit
%attr(755,root,root) %{_sbindir}/seedit-gui-load
%{py_sitedir}/%{name}/ui
%{_iconsdir}/%{name}
#%{_desktopdir}/seedit-gui.desktop
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/security/console.apps/seedit-gui
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pam.d/seedit-gui
#{_pixmapsdir}/seedit-gui.png

%files policy
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/policy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/selinux/%{name}
%{_datadir}/%{name}/initialize
%attr(755,root,root) %{_sbindir}/seedit-init
%ghost %{_datadir}/%{name}/sepolicy/need-init
%ghost %{_datadir}/%{name}/sepolicy/need-rbac-init
