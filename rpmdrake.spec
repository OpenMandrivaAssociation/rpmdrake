%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Rpmdrake::widgets\\)'
%else
%define _requires_exceptions perl(Rpmdrake::widgets)
%endif

Summary:	%{distribution} graphical front end for sofware installation/removal
Name:		rpmdrake
Version:	6.01
Release:	2
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://wiki.mandriva.com/en/Installing_and_removing_software
Source0:	%{name}-%{version}.tar.xz
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
Requires:	perl-Gtk3
Requires:	perl-Locale-gettext >= 1.05-6
Requires:	perl-URPM >= 3.07-2
# lazy load modules:
Requires:	perl-File-MimeInfo
Requires:	urpmi > 6.18
Requires:	polkit
Requires:	typelib(GtkSource) = 3.0
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

# XXX - should be changed upstream
sed -i -e "s,%{_sbindir}/edit-urpm-sources.pl,%{_bindir}/drakrpm-edit-media," \
        %{buildroot}%{_datadir}/applications/rpmdrake-sources.desktop

mkdir -p %{buildroot}{%{_miconsdir},%{_liconsdir},%{_iconsdir}/hicolor,%{_iconsdir}/hicolor/{16x16,32x32,48x48},%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps}
for i in rpmdrake onlineupdate edit-urpm-sources; do
  cp pixmaps/${i}16.png %{buildroot}%{_miconsdir}/${i}.png
  cp pixmaps/${i}32.png %{buildroot}%{_iconsdir}/${i}.png
  cp pixmaps/${i}48.png %{buildroot}%{_liconsdir}/${i}.png
  cp pixmaps/${i}16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/${i}.png
  cp pixmaps/${i}32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/${i}.png
  cp pixmaps/${i}48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/${i}.png
done

%check
%make check

%files -f rpmdrake.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/OnlineUpdate
%{_bindir}/drakrpm
%{_bindir}/edit-urpm-sources.pl
%{_bindir}/drakrpm-edit-media
%{_bindir}/drakrpm-update
%{_bindir}/drakrpm-editmedia
%{_bindir}/drakrpm-addmedia
%{_bindir}/gurpmi.addmedia
%{_bindir}/rpmdrake
%{_libexecdir}/drakrpm-update
%{_libexecdir}/drakrpm-editmedia
%{_libexecdir}/drakrpm-addmedia
%{_libexecdir}/drakrpm
%{_datadir}/polkit-1/actions/*.policy
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
