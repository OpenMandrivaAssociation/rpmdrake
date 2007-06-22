##################################################################
#
#
# !!!!!!!! WARNING => THIS HAS TO BE EDITED IN THE CVS !!!!!!!!!!!
#
#
##################################################################

%define name rpmdrake
%define version 3.70
%define release %mkrel 1
%define _requires_exceptions perl(Rpmdrake::widgets)

Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Source0: %name-%version.tar.bz2
Summary: Mandriva Linux graphical front end for sofware installation/removal
Requires: perl-MDK-Common >= 1.1.18-2mdk
Requires: urpmi >= 4.9.14
Requires: perl-URPM >= 1.58
Requires: drakxtools >= 10.4.112-1mdv2007.1
Requires: rpmtools >= 5.0.5
Requires: packdrake >= 5.0.5
Requires: perl-Gtk2 >= 1.054-1mdk
Requires: perl-Locale-gettext >= 1.01-7mdk
Requires: mdv-rpm-summary
# for icons:
Requires: desktop-common-data
# for now, packdrake (5.0.9) works better with this
Requires: perl-Compress-Zlib >= 1.33
BuildRequires: curl-devel >= 7.12.1-1mdk gettext openssl-devel perl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Group: System/Configuration/Packaging
URL: http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/rpmdrake/
Obsoletes: MandrakeUpdate
Provides: MandrakeUpdate
Conflicts: drakconf < 10.1-4mdk

%description
rpmdrake is a simple graphical frontend to manage software packages on a
Mandriva Linux system; it has 3 different modes:
- software packages installation;
- software packages removal;
- MandrivaUpdate (software packages updates).

A fourth program manages the media (add, remove, edit).

%package -n park-rpmdrake
Summary: Configure and update rpms on a park
Group: System/Configuration/Packaging
Requires: rsync scanssh perl-Expect rpmdrake

%description -n park-rpmdrake
Configure and update rpms on a park of hosts. The backend is parallel urpmi.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build
make OPTIMIZE="$RPM_OPT_FLAGS -Wall" PREFIX=%{_prefix} INSTALLDIRS=vendor

%install
%makeinstall_std PREFIX=%buildroot/%{_prefix}

%find_lang rpmdrake

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cp %{name}.menu $RPM_BUILD_ROOT%{_menudir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-rpmdrake.desktop << EOF
[Desktop Entry]
Name=Browse Available Software
Comment=A graphical front end for installing, removing and updating packages
Exec=/usr/sbin/rpmdrake
Icon=rpmdrake
Type=Application
Categories=GTK;X-MandrivaLinux-System-Configuration-Packaging;Settings;PackageManager;
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-rpmdrake-root.desktop << EOF
[Desktop Entry]
Name=Install, Remove & Update Software
Comment=A graphical front end for installing, removing and updating packages
Exec=/usr/bin/rpmdrake
Icon=rpmdrake
Type=Application
Categories=GTK;X-MandrivaLinux-System-Configuration-Packaging;Settings;PackageManager;
EOF

# for consolehelper config (#29696)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/rpmdrake <<EOF
#%PAM-1.0
auth       sufficient   pam_rootok.so
auth       required     pam_console.so
auth       include      system-auth
account    required     pam_permit.so
session    optional     pam_xauth.so
EOF
cp -af $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/{rpmdrake,mandrivaupdate}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/rpmdrake <<EOF
USER=root
PROGRAM=/usr/sbin/rpmdrake
FALLBACK=false
SESSION=true
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/MandrivaUpdate <<EOF
USER=root
PROGRAM=/usr/sbin/MandrivaUpdate
FALLBACK=false
SESSION=true
EOF
mkdir -p $RPM_BUILD_ROOT{%{_miconsdir},%{_liconsdir},%{_iconsdir}/hicolor,%{_iconsdir}/hicolor/{16x16,32x32,48x48},%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps}
for i in rpmdrake rpmdrake-remove mandrivaupdate edit-urpm-sources; do
  cp pixmaps/${i}16.png $RPM_BUILD_ROOT%{_miconsdir}/${i}.png
  cp pixmaps/${i}32.png $RPM_BUILD_ROOT%{_iconsdir}/${i}.png
  cp pixmaps/${i}48.png $RPM_BUILD_ROOT%{_liconsdir}/${i}.png
  cp pixmaps/${i}16.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/${i}.png
  cp pixmaps/${i}32.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/${i}.png
  cp pixmaps/${i}48.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/${i}.png
done
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/rpmdrake
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/MandrivaUpdate
ln -sf %{_bindir}/rpmdrake %{buildroot}%{_bindir}/drakrpm
ln -sf %{_sysconfdir}/security/console.apps/MandrivaUpdate %{buildroot}%{_sysconfdir}/security/console.apps/mandrivaupdate
ln -sf %{_sysconfdir}/pam.d/rpmdrake %{buildroot}%{_sysconfdir}/pam.d/drakrpm
ln -sf %{_sysconfdir}/security/console.apps/rpmdrake %{buildroot}%{_sysconfdir}/security/console.apps/drakrpm

# bloody RPM..
mkdir -p $RPM_BUILD_ROOT/var/lib/urpmi
touch $RPM_BUILD_ROOT/var/lib/urpmi/compssUsers.flat

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%files -f rpmdrake.lang
%defattr(-, root, root)
%doc COPYING AUTHORS README 
%config(noreplace) %{_sysconfdir}/pam.d/rpmdrake
%config(noreplace) %{_sysconfdir}/pam.d/mandrivaupdate
%config(noreplace) %{_sysconfdir}/security/console.apps/rpmdrake
%config(noreplace) %{_sysconfdir}/security/console.apps/MandrivaUpdate
# all three are symlinks
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
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-*.desktop
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/hicolor/16x16/apps/*.png
%{_iconsdir}/hicolor/32x32/apps/*.png
%{_iconsdir}/hicolor/48x48/apps/*.png
%ghost %{_var}/lib/urpmi/compssUsers.flat
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/*.pm

%files -n park-rpmdrake
%defattr(-,root,root)
%{_sbindir}/park-rpmdrake


