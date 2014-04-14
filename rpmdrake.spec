%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Rpmdrake::widgets\\)'
%else
%define _requires_exceptions perl(Rpmdrake::widgets)
%endif

Summary:	%{distribution} graphical front end for sofware installation/removal
Name:		rpmdrake
Version:	5.46
Release:	17
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://wiki.mandriva.com/en/Installing_and_removing_software
Source0:	%{name}-%{version}.tar.xz
Patch1:		rpmdrake-5.46-fix_info_progressbar.patch
Patch2:		rpmdrake-5.46-official.patch
Patch3:		rpmdrake-5.46-mirrorsite.patch
Patch4:		rpmdrake-5.26.12.update_all_repos.patch
# Fix display of old version if newer one exists
Patch5:		rpmdrake-5.46-installable-versions.patch
# Fix viewing details of gpgkeys
Patch6:     rpmdrake-5.46-gpgkey-details.patch
Patch7:	    rpmdrake-5.46-about.patch
Patch8:     rpmdrake-5.46-update_req.patch
Patch9:	    rpmdrake-5.46-locale.patch
BuildArch:	noarch

BuildRequires:	gettext 
BuildRequires:	intltool
BuildRequires:	perl_checker
BuildRequires:	perl-JSON-PP
BuildRequires:	perl-devel
# for icons:
Requires:	desktop-common-data
Requires:	drakxtools >= 12.64
Requires:	perl-MDK-Common
Requires:	perl-Gtk2 >= 1.172-2
Requires:	perl-Locale-gettext >= 1.05-6
Requires:	perl-URPM >= 3.07-2
# lazy load modules:
Requires:	perl-Gtk2-SourceView2
Requires:	perl-File-MimeInfo
Requires:	urpmi > 6.18
# need the consolehelper basic pam config files
Requires:	usermode-consoleonly
# for translations:
Suggests:	mdv-rpm-summary
Provides:	MandrakeUpdate

%description
This package contains the %{distribution} graphical software manipulation
tools.

Rpmdrake provides a simple interface that makes it easy to install
and remove software.

MandrivaUpdate is a single-purpose application for keeping your system
up to date with the latest official updates.

There is also a tool for configuring package sources (medias), which can
be run independently or accessed from within rpmdrake.

%prep
%setup -q
%apply_patches

%build
make OPTIMIZE="%{optflags} -Wall" PREFIX=%{_prefix} INSTALLDIRS=vendor

%install
%makeinstall_std PREFIX=%{buildroot}/%{_prefix}

%find_lang rpmdrake

# for consolehelper config (#29696)
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/rpmdrake
cp -af %{buildroot}%{_sysconfdir}/pam.d/{rpmdrake,mandrivaupdate}
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/rpmdrake <<EOF
USER=root
PROGRAM=/usr/sbin/rpmdrake
FALLBACK=false
SESSION=true
EOF
# Rights Delegation spec for MDV2008 says MandrivaUpdate should ask for
# user password, not root password
cat > %{buildroot}%{_sysconfdir}/security/console.apps/MandrivaUpdate <<EOF
USER=<user>
PROGRAM=/usr/sbin/MandrivaUpdate
FALLBACK=false
SESSION=true
EOF

# edit media
cp -af %{buildroot}%{_sysconfdir}/pam.d/{rpmdrake,drakrpm-edit-media}
cat > %{buildroot}%{_sysconfdir}/security/console.apps/drakrpm-edit-media <<EOF
USER=root
PROGRAM=/usr/sbin/drakrpm-edit-media
FALLBACK=false
SESSION=true
EOF
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/drakrpm-edit-media
# XXX - should be changed upstream
sed -i -e "s,%{_sbindir}/edit-urpm-sources.pl,%{_bindir}/drakrpm-edit-media," \
        %{buildroot}%{_datadir}/applications/rpmdrake-sources.desktop

mkdir -p %{buildroot}{%{_miconsdir},%{_liconsdir},%{_iconsdir}/hicolor,%{_iconsdir}/hicolor/{16x16,32x32,48x48},%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps}
for i in rpmdrake mandrivaupdate edit-urpm-sources; do
  cp pixmaps/${i}16.png %{buildroot}%{_miconsdir}/${i}.png
  cp pixmaps/${i}32.png %{buildroot}%{_iconsdir}/${i}.png
  cp pixmaps/${i}48.png %{buildroot}%{_liconsdir}/${i}.png
  cp pixmaps/${i}16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/${i}.png
  cp pixmaps/${i}32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/${i}.png
  cp pixmaps/${i}48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/${i}.png
done
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/rpmdrake
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/MandrivaUpdate
ln -sf %{_bindir}/rpmdrake %{buildroot}%{_bindir}/drakrpm
ln -sf %{_sysconfdir}/security/console.apps/MandrivaUpdate %{buildroot}%{_sysconfdir}/security/console.apps/mandrivaupdate
ln -sf %{_sysconfdir}/pam.d/rpmdrake %{buildroot}%{_sysconfdir}/pam.d/drakrpm
ln -sf %{_sysconfdir}/security/console.apps/rpmdrake %{buildroot}%{_sysconfdir}/security/console.apps/drakrpm

%check
%make check

%files -f rpmdrake.lang
%doc AUTHORS COPYING NEWS README 
%config(noreplace) %{_sysconfdir}/pam.d/rpmdrake
%config(noreplace) %{_sysconfdir}/pam.d/mandrivaupdate
%config(noreplace) %{_sysconfdir}/pam.d/drakrpm-edit-media
%config(noreplace) %{_sysconfdir}/security/console.apps/rpmdrake
%config(noreplace) %{_sysconfdir}/security/console.apps/MandrivaUpdate
%config(noreplace) %{_sysconfdir}/security/console.apps/drakrpm-edit-media
# all these in sysconfdir are symlinks
%{_sysconfdir}/pam.d/drakrpm
%{_sysconfdir}/security/console.apps/drakrpm
%{_sysconfdir}/security/console.apps/mandrivaupdate
%{_sbindir}/rpmdrake*
%{_sbindir}/MandrivaUpdate
%{_sbindir}/edit-urpm-*
%{_sbindir}/drakrpm-edit-media
%{_sbindir}/drakrpm-update
%{_sbindir}/gurpmi.addmedia
%{_bindir}/*
%{_datadir}/%{name}
%{perl_vendorlib}/*.pm
%{perl_vendorlib}/Rpmdrake
%{_datadir}/mimelnk/application/x-urpmi-media.desktop
%{_datadir}/mime/packages/urpmi-media.xml
%{_datadir}/applications/*.desktop
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/hicolor/16x16/apps/*.png
%{_iconsdir}/hicolor/32x32/apps/*.png
%{_iconsdir}/hicolor/48x48/apps/*.png

