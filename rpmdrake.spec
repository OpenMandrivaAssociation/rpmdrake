%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Rpmdrake::widgets\\)'
%else
%define _requires_exceptions perl(Rpmdrake::widgets)
%endif

Summary:	%{distribution} graphical front end for sofware installation/removal
Name:		rpmdrake
Version:	6.10
Release:	1
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://wiki.mandriva.com/en/Installing_and_removing_software
Source0:	%{name}-%{version}.tar.xz
BuildRequires:	gettext 
BuildRequires:	intltool
BuildRequires:	perl_checker
BuildRequires:	perl(JSON::PP)
BuildArch:	noarch

Requires:	perl-MDK-Common
Requires:	urpmi >= 7.30
Requires:	drakxtools >= 16.2
# lazy load modules:
Requires:	typelib(GtkSource) = 3.0
Requires:	perl(File::MimeInfo)
Requires:	polkit
# for translations:
Suggests:	mdv-rpm-summary
# for icons:
Requires:	desktop-common-data
Provides:	MandrakeUpdate

%description
This package contains the %{distribution} graphical software manipulation
tools.

Rpmdrake provides a simple interface that makes it easy to install
and remove software.

MoondrakeUpdate is a single-purpose application for keeping your system
up to date with the latest official updates.
  
There is also a tool for configuring package sources (medias), which can
be run independently or accessed from within rpmdrake.

%prep
%setup -q

%build
make OPTIMIZE="%{optflags} -Wall" PREFIX=%{_prefix} INSTALLDIRS=vendor

%install
%makeinstall_std PREFIX=%{buildroot}%{_prefix}

%find_lang rpmdrake

for i in rpmdrake moondrakeupdate edit-urpm-sources; do
  install -m644 pixmaps/${i}16.png -D %{buildroot}%{_miconsdir}/${i}.png
  install -m644 pixmaps/${i}32.png -D %{buildroot}%{_iconsdir}/${i}.png
  install -m644 pixmaps/${i}48.png -D %{buildroot}%{_liconsdir}/${i}.png
  install -m644 pixmaps/${i}16.png -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/${i}.png
  install -m644 pixmaps/${i}32.png -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/${i}.png
  install -m644 pixmaps/${i}48.png -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/${i}.png
done

%check
%make check

%files -f rpmdrake.lang
%doc AUTHORS NEWS README 
%{_bindir}/drakrpm
%{_bindir}/drakrpm-update
%{_bindir}/drakrpm-editmedia
%{_bindir}/drakrpm-addmedia
%{_bindir}/MoondrakeUpdate
%{_bindir}/edit-urpm-sources.pl
%{_bindir}/drakrpm-edit-media
%{_bindir}/gurpmi.addmedia
%{_bindir}/rpmdrake
%{_libexecdir}/drakrpm
%{_libexecdir}/drakrpm-update
%{_libexecdir}/drakrpm-editmedia
%{_libexecdir}/drakrpm-addmedia
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
