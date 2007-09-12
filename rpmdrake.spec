##################################################################
#
#
# !!!!!!!! WARNING => THIS HAS TO BE EDITED IN THE CVS !!!!!!!!!!!
#
#
##################################################################

%define name rpmdrake
%define version 3.93
%define release %mkrel 2
%define _requires_exceptions perl(Rpmdrake::widgets)

Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Source0: %name-%version.tar.bz2
Summary: Mandriva Linux graphical front end for sofware installation/removal
Requires: perl-MDK-Common >= 1.1.18-2mdk
Requires: urpmi >= 4.10.2
Requires: perl-URPM >= 1.58
Requires: drakxtools >= 10.4.112-1mdv2007.1
Requires: rpmtools >= 5.0.5
Requires: packdrake >= 5.0.5
Requires: perl-Gtk2 >= 1.054-1mdk
Requires: perl-Locale-gettext >= 1.01-7mdk
Requires: mdv-rpm-summary
# need the consolehelper basic pam config files
Requires: usermode-consoleonly >= 1.92-4mdv
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

# for consolehelper config (#29696)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/rpmdrake
cp -af $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/{rpmdrake,mandrivaupdate}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/rpmdrake <<EOF
USER=root
PROGRAM=/usr/sbin/rpmdrake
FALLBACK=false
SESSION=true
EOF
# Rights Delegation spec for MDV2008 says MandrivaUpdate should ask for
# user password, not root password
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/MandrivaUpdate <<EOF
USER=<user>
PROGRAM=/usr/sbin/MandrivaUpdate
FALLBACK=false
SESSION=true
EOF

# delete packages
cp -af $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/{rpmdrake,rpmdrake-remove}
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/rpmdrake-remove <<EOF
USER=root
PROGRAM=/usr/sbin/rpmdrake-remove
FALLBACK=false
SESSION=true
EOF
ln -sf %{_bindir}/consolehelper $RPM_BUILD_ROOT%{_bindir}/rpmdrake-remove
# drakrpm-remove vs rpmdrake-remove mess
ln -sf %{_bindir}/rpmdrake-remove $RPM_BUILD_ROOT%{_bindir}/drakrpm-remove
ln -sf %{_sysconfdir}/pam.d/rpmdrake-remove $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/drakrpm-remove
ln -sf %{_sysconfdir}/security/console.apps/rpmdrake-remove \
        $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/drakrpm-remove

# edit media
cp -af $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/{rpmdrake,drakrpm-edit-media}
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/drakrpm-edit-media <<EOF
USER=root
PROGRAM=/usr/sbin/drakrpm-edit-media
FALLBACK=false
SESSION=true
EOF
ln -sf %{_bindir}/consolehelper $RPM_BUILD_ROOT%{_bindir}/drakrpm-edit-media
# XXX - should be changed upstream
sed -i -e "s,%{_sbindir}/edit-urpm-sources.pl,%{_bindir}/drakrpm-edit-media," \
        %{buildroot}%{_datadir}/applications/rpmdrake-sources.desktop

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
%config(noreplace) %{_sysconfdir}/pam.d/rpmdrake-remove
%config(noreplace) %{_sysconfdir}/pam.d/drakrpm-edit-media
%config(noreplace) %{_sysconfdir}/security/console.apps/rpmdrake
%config(noreplace) %{_sysconfdir}/security/console.apps/MandrivaUpdate
%config(noreplace) %{_sysconfdir}/security/console.apps/rpmdrake-remove
%config(noreplace) %{_sysconfdir}/security/console.apps/drakrpm-edit-media
# all these in sysconfdir are symlinks
%{_sysconfdir}/pam.d/drakrpm
%{_sysconfdir}/pam.d/drakrpm-remove
%{_sysconfdir}/security/console.apps/drakrpm
%{_sysconfdir}/security/console.apps/mandrivaupdate
%{_sysconfdir}/security/console.apps/drakrpm-remove
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
%{_datadir}/applications/*.desktop
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


