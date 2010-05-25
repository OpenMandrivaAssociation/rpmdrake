%define name rpmdrake
%define version 5.26.1
%define release %mkrel 1
%define _requires_exceptions perl(Rpmdrake::widgets)

Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Source0: %name-%version.tar.lzma
Summary: Mandriva Linux graphical front end for sofware installation/removal
Requires: perl-MDK-Common >= 1.1.18-2mdk
Requires: urpmi > 6.18
Requires: perl-URPM >= 3.07-2
Requires: drakxtools >= 12.64
Requires: perl-Gtk2 >= 1.172-2
Requires: perl-Locale-gettext >= 1.05-6
# lazy load modules:
Requires: perl-Gtk2-SourceView2
Requires: perl-File-MimeInfo
# for translations:
Suggests: mdv-rpm-summary
# need the consolehelper basic pam config files
Requires: usermode-consoleonly >= 1.92-4mdv2008.0
# for icons:
Requires: desktop-common-data
BuildRequires: gettext perl-devel intltool
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch
Group: System/Configuration/Packaging
URL: http://wiki.mandriva.com/en/Installing_and_removing_software
Obsoletes: MandrakeUpdate
Provides: MandrakeUpdate
Conflicts: drakconf < 10.1-4mdk

%description
This package contains the Mandriva graphical software manipulation
tools.

Rpmdrake provides a simple interface that makes it easy to install
and remove software.

MandrivaUpdate is a single-purpose application for keeping your system
up to date with the latest official updates.

There is also a tool for configuring package sources (medias), which can
be run independently or accessed from within rpmdrake.

%prep
rm -rf %{buildroot}

%setup -q

%build
make OPTIMIZE="$RPM_OPT_FLAGS -Wall" PREFIX=%{_prefix} INSTALLDIRS=vendor

%install
rm -fr %{buildroot}
%makeinstall_std PREFIX=%buildroot/%{_prefix}

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


%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post 
%update_menus
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%clean_mime_database
%clean_desktop_database
%endif

%files -f rpmdrake.lang
%defattr(-, root, root)
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

