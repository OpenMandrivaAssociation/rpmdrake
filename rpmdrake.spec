%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Rpmdrake::widgets\\)'
%else
%define _requires_exceptions perl(Rpmdrake::widgets)
%endif

Name:		rpmdrake
Version:	5.46
Release:	9

Summary:	%{distribution} graphical front end for sofware installation/removal
License:	GPLv2+
Group:		System/Configuration/Packaging
URL:		http://wiki.mandriva.com/en/Installing_and_removing_software

Source0:	%{name}-%{version}.tar.xz
Patch1:		rpmdrake-5.46-fix_info_progressbar.patch
Patch2:     rpmdrake-5.46-official.patch
Patch3:	    rpmdrake-5.46-mirrorsite.patch
Patch4:     rpmdrake-5.26.12.update_all_repos.patch
# Fix display of old version if newer one exists
Patch5:     rpmdrake-5.46-installable-versions.patch
# Fix viewing details of gpgkeys
Patch6:     rpmdrake-5.46-gpgkey-details.patch

BuildRequires:	gettext 
BuildRequires:	perl-devel
BuildRequires:	intltool
BuildRequires:	perl_checker
BuildRequires:	perl-JSON-PP
BuildArch:	noarch

Requires:	perl-MDK-Common
Requires:	urpmi > 6.18
Requires:	perl-URPM >= 3.07-2
Requires:	drakxtools >= 12.64
Requires:	perl-Gtk2 >= 1.172-2
Requires:	perl-Locale-gettext >= 1.05-6
# lazy load modules:
Requires:	perl-Gtk2-SourceView2
Requires:	perl-File-MimeInfo
# for translations:
Suggests:	mdv-rpm-summary
# need the consolehelper basic pam config files
Requires:	usermode-consoleonly
# for icons:
Requires:	desktop-common-data
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


%changelog
* Fri Aug 12 2011 Joao Victor Duarte Martins <jvdm@mandriva.com.br> 5.26.11-0
+ Revision: 694268
- Bugfix release
- Fix access to package information (#63445)
- Fix selection of package do remove (fix #63222).
- Update translations.

* Wed Jun 22 2011 Eugeni Dodonov <eugeni@mandriva.com> 5.26.9-2
+ Revision: 686709
- Rebuild

* Thu May 05 2011 Joao Victor Duarte Martins <jvdm@mandriva.com.br> 5.26.9-1
+ Revision: 669501
- Fix list of matching packages when warning for packages not in list (bug #62308)

* Thu May 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.26.8-1
+ Revision: 669391
- clean out legacy stuff
- update license tag
- follow URPM API change for using the correct tag names 'providename' & 'basenames'

* Tue Mar 01 2011 Joao Victor Duarte Martins <jvdm@mandriva.com.br> 5.26.7-1
+ Revision: 641147
- Bugfix release 2.26.7:
- Fix offering of updates from media not configured as update (#60891).

* Fri Jan 07 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.26.6-1mdv2011.0
+ Revision: 629717
- fix display of name, version, release, arch etc. with rpm5 (#61702)
- don't clean buildroot in %%prep

* Sun Oct 24 2010 Thierry Vignaud <tv@mandriva.org> 5.26.5-1mdv2011.0
+ Revision: 587847
- BuildRequires perl_checker
- add a minimal "testsuite" in order to prevent syntax errors such as #60901

* Tue Aug 24 2010 Joao Victor Martins <jvictor@mandriva.com> 5.26.4-1mdv2011.0
+ Revision: 572521
- fix wrong notice message for updates (#60629)

* Thu Jul 22 2010 Funda Wang <fwang@mandriva.org> 5.26.3-2mdv2011.0
+ Revision: 556964
- rebuild

* Fri Jul 16 2010 Thierry Vignaud <tv@mandriva.org> 5.26.3-1mdv2011.0
+ Revision: 554267
- fix crashing when looking at update details (#60153)
  (bug introduced in rpmdrake 5.25)

* Sat Jun 05 2010 Thierry Vignaud <tv@mandriva.org> 5.26.2-1mdv2010.1
+ Revision: 547136
- rpmdrake:
  o fix displaying version numer in about dialog (#59665)

* Tue May 25 2010 Joao Victor Martins <jvictor@mandriva.com> 5.26.1-1mdv2010.1
+ Revision: 545936
- update to bugfix release 5.26.1
  o uninstalled package shows files list (bug #58871)
  o added auto_select and clean_cache options to conf file (bug #48552)

* Tue Apr 06 2010 Joao Victor Martins <jvictor@mandriva.com> 5.26-1mdv2010.1
+ Revision: 532326
- Bugfix update version 5.26 (bug #40556)

* Wed Mar 03 2010 Thierry Vignaud <tv@mandriva.org> 5.25-1mdv2010.1
+ Revision: 514033
- do not show file list if empty
- explain what are official, backports ... packages
- edit-urpm-sources:
  o fix crashing when deleting media with UTF-8 characters (#57644)

* Wed Feb 24 2010 Thierry Vignaud <tv@mandriva.org> 5.24-3mdv2010.1
+ Revision: 510478
- relax require on gtksourceview2 binding

* Tue Feb 23 2010 Thierry Vignaud <tv@mandriva.org> 5.24-2mdv2010.1
+ Revision: 510383
- fix require on gtksourceview2 binding (#57746)

* Thu Dec 03 2009 Thierry Vignaud <tv@mandriva.org> 5.24-1mdv2010.1
+ Revision: 473047
- remove --root option that was deprecated since August 2007
- use gtksourceview-2 instead of gtksourceview-1
- rpmdrake:
  o fix crashing when running as user (#55009)

* Tue Oct 27 2009 Thierry Vignaud <tv@mandriva.org> 5.23-1mdv2010.0
+ Revision: 459464
- rename 'dependancies' as 'new dependancies' and tell there's no new
  dependancy when list is empty (#54697)
- use a scrolling window if needed when displaying list of orphan
  packages after removing some packages (#54713)

* Fri Oct 16 2009 Thierry Vignaud <tv@mandriva.org> 5.22-1mdv2010.0
+ Revision: 457949
- rpmdrake
  o display a graphical warning when trying more than one instance
    instead of silently exiting
  o match urpmi behavior when registering requested package
- MandrivaUpdate:
  o do not display the banner when height <= 480 instead of just < 480
    (#54550)

* Mon Oct 12 2009 Thierry Vignaud <tv@mandriva.org> 5.21.1-1mdv2010.0
+ Revision: 456902
- try harder to display help, bug wizards, ... as user

* Mon Oct 12 2009 Thierry Vignaud <tv@mandriva.org> 5.21-2mdv2010.0
+ Revision: 456815
- bump require on drakxtools (#54336)

* Fri Oct 09 2009 Thierry Vignaud <tv@mandriva.org> 5.21-1mdv2010.0
+ Revision: 456393
- edit-urpm-sources:
  o fix enabling for the first time a medium that never was enabled
    before (#52636)
  o ignore rpmdrake's option regarding ignoring debug media
  o prevent crashing if one click on a media checkbox while another
    one is being processed (gtk+ was reentering the callback when we
    were processing refreshing events...) (#46727)
- rpmdrake
  o fix searching on just names (#54339)

* Fri Oct 02 2009 Thierry Vignaud <tv@mandriva.org> 5.20-1mdv2010.0
+ Revision: 452559
- rpmdrake
  o display orphan packages after removing some packages
  o fix registering orphan package (#51229)

* Thu Oct 01 2009 Thierry Vignaud <tv@mandriva.org> 5.19-1mdv2010.0
+ Revision: 452243
- gurpmi.addmedia
  o fix message when adding distrib media (#49566)
- rpmdrake
  o fix encoding of diff output (#52994)
  o fix for unreproductable crash (#49273)
  o fix rare crash when medium is unknown (#49901)
  o fix rare crash with packages without any URPM objects (#52751)
  o update GUI package list

* Thu Oct 01 2009 Thierry Vignaud <tv@mandriva.org> 5.18-1mdv2010.0
+ Revision: 452126
- edit-urpm-sources:
  o use proper stock icons for arrows
- rpmdrake
  o added dependencies section in package details panel (#39491)
  o enable to apply priority updates without trying to select any
    package
  o search
    * clear search results too when cleaing searched text (#49239)
    * default to OR like searches for searches among package names (#37643)
    * enable to disable use of regular expression (default is: disabled)
    * enable to search in full or short package names (#46473)
    * fix searching for summary on startup (#49293)
    * rerun search after reloading package list (#49834)
  o show rpmdrake version in about dialog instead of distribution
    version (#49467)
  o warn on exit if some packages are selected (#45404)

* Mon Jun 01 2009 Thierry Vignaud <tv@mandriva.org> 5.17-1mdv2010.0
+ Revision: 381906
- consider chrooted /etc/product.id when detecting whether installed
  distro is stable or cooker
- do not restart if we didn't install any package (when having
  priority packages)
- fix not displaying importance and reasons of updates (#51118)
  (regression introduced by #50276 fix in 5.16.2)
- make 'urpmi-root' implying rpm-root so that the proper chrooted db
  got opened
- rpmdrake:
  o update GUI package list

* Wed May 13 2009 Thierry Vignaud <tv@mandriva.org> 5.16.4-1mdv2010.0
+ Revision: 375062
- rpmdrake:
  o do not crash when running as root (#50473)

* Wed May 06 2009 Thierry Vignaud <tv@mandriva.org> 5.16.3-1mdv2010.0
+ Revision: 372458
- rpmdrake:
  o save "Compute updates on startup" setting
  o when searching in descriptions, do not search among packages not
    in current view (#50638)

* Mon May 04 2009 Thierry Vignaud <tv@mandriva.org> 5.16.2-1mdv2010.0
+ Revision: 371499
- rpmdrake:
  o fix listing _one_ non installed package as installed (#50276)
  o fix swedish translation that broke menu structure (#49989)
  o default "Compute updates on startup" to yes
    (fix "MandrivaUpdate and urpmi show updated rpm, while rpmdrake
    doesn't", #47305)
  o manually list cedega, picasa, VariCAD, VariCAD_View &
    VMware-Player as GUI packages (#50379)
  o update GUI package list
- bump drakxtools require (#50404)

* Wed Apr 15 2009 Thierry Vignaud <tv@mandriva.org> 5.16.1-1mdv2009.1
+ Revision: 367395
- ignore /etc/fstab for *.rpmnew (#49887)
- rpmdrake:
  o update GUI package list

* Fri Apr 03 2009 Thierry Vignaud <tv@mandriva.org> 5.16-1mdv2009.1
+ Revision: 363801
- revert using installer hack that prevents having gray wait message dialogs on
  dialog popup in favor of old rgs hack, else (when not on displayed desktop),
  it uses too much CPU and waits until it got the focus (#48912)
- rpmdrake:
  o update GUI package list

* Wed Apr 01 2009 Thierry Vignaud <tv@mandriva.org> 5.15-1mdv2009.1
+ Revision: 363391
- kill --no-splash option (useless since 4.17 (do not display a splash
  text anymore)), thus fixing #49035)
- rpmdrake:
  o add a sensible tooltip for the "find" entry (#39454)
  o suggest to switch to the 'all' view if there's no search results (#38461)

* Mon Mar 30 2009 Thierry Vignaud <tv@mandriva.org> 5.14-1mdv2009.1
+ Revision: 362357
- prevent dialog to enlarge too much when displaying downloads of
  media meta_data (eg: adding or updating media)
- gurpmi.addmedia:
  o fix success message when adding mirrorlist (#48112)
- rpmdrake:
  o update GUI package list

* Wed Mar 25 2009 Thierry Vignaud <tv@mandriva.org> 5.13-1mdv2009.1
+ Revision: 361041
- rpmdrake:
  o do not use Gtk2::Sexy anymore (sligthly reduce memory usage)
  o update GUI package list (#49086)

* Fri Mar 20 2009 Thierry Vignaud <tv@mandriva.org> 5.12-1mdv2009.1
+ Revision: 359117
- MandrivaUpdate:
  o select updates from all media on cooker instead of only from update media

* Thu Mar 19 2009 Thierry Vignaud <tv@mandriva.org> 5.11.1-1mdv2009.1
+ Revision: 357817
- export a function for mdkapplet

* Thu Mar 19 2009 Thierry Vignaud <tv@mandriva.org> 5.11-1mdv2009.1
+ Revision: 357811
- MandrivaUpdate:
  o fix width of title by workarounding Gtk+ (#48259)
  o update all media on cooker instead of only update media
- rpmdrake:
  o do not try to update & parse inactive sources backports media

* Wed Mar 18 2009 Thierry Vignaud <tv@mandriva.org> 5.10-1mdv2009.1
+ Revision: 357372
- MandrivaUpdate:
  o fix ignoring selected/unselected packages (embarassing bug #29835)
    (regression introduced in 4.10 on 24 June 2008: "show type of
    update in mandrivaupdate (fix, security, ...)")

* Mon Feb 23 2009 Thierry Vignaud <tv@mandriva.org> 5.9-1mdv2009.1
+ Revision: 344200
- patch 0: fix build due to broken pt_BR translation
- rpmdrake:
  o add 'compute_updates' option that enable super fast startup by
    skipping computing updates on startup (#42848)
  o do not try to update & parse inactive debug backports media
  o prevent running more than one instance (#47755)
  o reduce memory usage
  o update GUI package list
  o use right icon

* Sun Feb 15 2009 Thierry Vignaud <tv@mandriva.org> 5.8-1mdv2009.1
+ Revision: 340370
- fix crashing on uninstalling packages (#47751)
- icons (#44671):
  o update banner icons from mcc ones
  o use mcc icon for banners if availlable
- prevent crashing in URPM when using --env with relative paths
- edit-urpm-sources:
  o do not use the same shortcut for "Add a specific "media mirror"
    and "_Add a custom medium" menu entries (#46027)
  o honnor canceling when the user closed the "updates/full_sources"
    dialog (#47125)
  o honnor canceling when the user refused to access the network when
    adding a specific mirror from the menubar (#46027)
  o use same icon as in mcc instead of rpmdarke one (#44671)
- bump drakxtools require (#45653)

* Wed Feb 11 2009 Thierry Vignaud <tv@mandriva.org> 5.7-1mdv2009.1
+ Revision: 339528
- fix using --justdb option
- MandrivaUpdate:
  o warn when rebooting is needed after installing packages
- rpmdrake:
  o add C-F accelerator in order to focus on search entry (#46404)

* Mon Feb 09 2009 Thierry Vignaud <tv@mandriva.org> 5.6-1mdv2009.1
+ Revision: 338777
- edit-urpm-sources:
  o add media even if one failed instead of rollbacking all of them
    (regression introduced in urpmi-6.19)
  o fix displayling big list of media to remove (#46773)
  o fix media selection dialog layout so that dialog behaves smoothly
    on resizing (#47271)
- MandrivaUpdate:
  o use new proper API to select media, thus fixing not updating media
    (side effect of urpmi API changes, #47209)
- rpmdrake:
  o update GUI package list

* Tue Dec 09 2008 Thierry Vignaud <tv@mandriva.org> 5.5-1mdv2009.1
+ Revision: 312341
- rpmdrake:
  o searching:
    * fix a rare crash on searching (#46225)
    * only look at name, not at full name (n-e-v-r) when performing
      search in names (#45410)
    * scroll group list to search category
  o update GUI package list

* Mon Nov 24 2008 Thierry Vignaud <tv@mandriva.org> 5.4-1mdv2009.1
+ Revision: 306386
- edit-urpm-sources:
  o do not drop 'ignore' flag when updating a medium (#44930)
  o fix displaying type of altered mirrorlist media (#44930)
- rpmdrake:
  o list plasma applets in GUI package list too (#45835)
  o update GUI package list
- bump require on urpmi for new API

* Mon Nov 17 2008 Thierry Vignaud <tv@mandriva.org> 5.3-1mdv2009.1
+ Revision: 304017
- drop diagnostics, strict, vars and warnings pragmas (should help #45361)
- edit_urpm_sources:
  o make clearer than DVD, CD-ROM are removable devices (#30842)
  o prevent enabling one to tag media as update media when adding
    whole distro media
- rpmdrake:
  o update GUI package list

* Thu Nov 06 2008 Thierry Vignaud <tv@mandriva.org> 5.2.1-1mdv2009.1
+ Revision: 300283
- fix displaying big list of conflicting packages
- fix loading options from chrooted config file
- rpmdrake:
  o update GUI package list

* Mon Nov 03 2008 Thierry Vignaud <tv@mandriva.org> 5.2-1mdv2009.1
+ Revision: 299347
- better looking messages when downloading files
- do not read big debug media if 'ignore_debug_media' option is set
- try harder not to have gray wait message dialogs
  (needs drakxtools > 11.67)
- when using --env:
  o do not write chrooted .rpmdrake config file on exit
  o open the chrooted .rpmdrake config file
- gurpmi.addmedia:
  o fix return value when canceling
- rpmdrake:
  o enable to set 'noclean' option (#13522)

* Sat Oct 11 2008 Thierry Vignaud <tv@mandriva.org> 5.1-2mdv2009.1
+ Revision: 291786
- do not ask sources on startup
- open help & bug report as user instead of as root (#44497)
- edit_urpm_sources:
  o fix displayed version in 'About' dialog
  o move "add media" menu entries from the "Options" menu into the
    "File" menu (#44601)
- gurpmi.addmedia:
  o handle --urpmi-root
- MandrivaUpdate:
  o make bug importance icons be transparent (#44745)
- rpmdrake:
  o fix too big "media to update" window (#44518)
  o update GUI package list

* Wed Oct 01 2008 Thierry Vignaud <tv@mandriva.org> 5-1mdv2009.0
+ Revision: 290357
- rpmdrake:
  o use radio buttons in order to show current search mode
- edit_urpm_sources:
  o add an "Add media" menu item in order to still able to manually
    choose mirror
  o default to use mirrorlist (#39898)
  o enable to edit mirrorlist media

* Tue Sep 30 2008 Thierry Vignaud <tv@mandriva.org> 4.21-1mdv2009.0
+ Revision: 290028
- fix modality/transient hints
  (regression introduced in drakxtools-11.10.2 on 18 August 2008 while
  fixing focus issues)
- workaround crashing when tree selection wasn't realized yet (#41010)
- rpmdrake:
  o only warn once per session when media XML metadata are newer than
    synthesis (#42737)
    (meaning package list & metadata are not syncrhonised and that
    media need updates)

* Thu Sep 25 2008 Thierry Vignaud <tv@mandriva.org> 4.20.3-2mdv2009.0
+ Revision: 288162
- bump drakxtools require
- fix URL

* Wed Sep 24 2008 Olivier Blin <blino@mandriva.org> 4.20.3-1mdv2009.0
+ Revision: 287760
- 4.20.3
- gurpmi.addmedia:
  o set dialog hint if drakx-matchbox-window-manager is used
    (for installer)

* Mon Sep 22 2008 Thierry Vignaud <tv@mandriva.org> 4.20.1-1mdv2009.0
+ Revision: 287025
- translation updates

* Sat Sep 20 2008 Thierry Vignaud <tv@mandriva.org> 4.20-1mdv2009.0
+ Revision: 286128
- basic managment of orphan packages (#43723):
  o display them
  o handle --auto_orphans option
- rpmdrake:
  o remove short lived wait message when changing selected view to
    some 'update' view (security/bugfix/...) since it's too fast
  o remove short lived wait message when reloading the packages list
    (#43955)

* Wed Sep 17 2008 Thierry Vignaud <tv@mandriva.org> 4.19-1mdv2009.0
+ Revision: 285419
- do display conflicting packages instead of silently removing them
  (needs urpmi 6.11) (#43501)
- do not display any (truncated) banner when embedded while updating
  media (like non-embedded case) (#43815)
- do not display any banner when embedded while adding media
- rpmdrake:
  o fix listing updates per importance (#41331)
    (regression introduced in 3.95 on 2007-09-14)
- bump require on urpmi for new needed API

* Wed Sep 10 2008 Thierry Vignaud <tv@mandriva.org> 4.18.2-1mdv2009.0
+ Revision: 283449
- fix opening the right RPM DB with --env
- workaround looping in URPM->traverse_tag when using --env

* Tue Sep 09 2008 Thierry Vignaud <tv@mandriva.org> 4.18.1-1mdv2009.0
+ Revision: 283298
- rpmdrake:
  o fix crashing when selecting all packages (#40025)

* Tue Sep 09 2008 Thierry Vignaud <tv@mandriva.org> 4.18-1mdv2009.0
+ Revision: 283190
- all:
  o adapt to urpmi-6.6+ new API (which workaround urpmi API breakage
    #43639)
  o do not ignore some options
  o handle --debug, --env, -q, --quiet, -v & --verbose options
- rpmdrake:
  o display a busy cursor while fetching package list on startup
  o update GUI package list
  o remove short lived wait message when changing selected package
    group (#43320) since it's too fast
- require a recent enough urpmi

* Thu Sep 04 2008 Thierry Vignaud <tv@mandriva.org> 4.17-1mdv2009.0
+ Revision: 280812
- all
  o be able to handle --expert
  o do not display a splash text anymore
- edit-urpm-sources:
  o by default do not enable to alter the 'update' flag (unless
    --expert is given)
- gurpmi.addmedia
  o instead of discarding --update when using --distrib, give it a meaning:
    only add media flagged "update"
- rpmdrake:
  o update GUI package list

* Tue Aug 26 2008 Thierry Vignaud <tv@mandriva.org> 4.16-1mdv2009.0
+ Revision: 276213
- MandrivaUpdate:
  o fix sorting by type of update
- rpmdrake:
  o make --mode option work again
  o workaround crashing when media's MD5SUM are garbaged (#41352)

* Mon Aug 25 2008 Thierry Vignaud <tv@mandriva.org> 4.15-1mdv2009.0
+ Revision: 275695
- rpmdrake:
  o fix a rare crash when canceling (#41970)
  o list meta tasks in GUI package list too (#43114)
  o update GUI package list

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 4.14-1mdv2009.0
+ Revision: 266587
- gurpmi.addmedia:
  o fix displaying --help
  o fix --urpmi-root option
- rpmdrake:
  o update GUI package list

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 4.13-1mdv2009.0
+ Revision: 264274
- rpmdrake:
  o behaves like urpmi, allow to continue, thus skipping the bogus
    transaction instead of short-circuiting urpm::main_loop
  o fix some error dialogs not being modal
  o update GUI package list

* Wed Jul 02 2008 Thierry Vignaud <tv@mandriva.org> 4.12-1mdv2009.0
+ Revision: 230720
- MandrivaUpdate, rpmdrake:
  o save & restore window size (#25932)
- rpmdrake:
  o make sure searches with no results clear package list (#34898)
  o show 'Group' in details (usefull for search results, #39244)
  o stop packaging rpmdrake-remove (#39485)
  o update GUI package list

* Tue Jul 01 2008 Thierry Vignaud <tv@mandriva.org> 4.11-1mdv2009.0
+ Revision: 230533
- rpmdrake:
  o always create a search category in tree (#29164)
  o open the search results category once searching is done

* Tue Jun 24 2008 Thierry Vignaud <tv@mandriva.org> 4.10-1mdv2009.0
+ Revision: 228561
- MandrivaUpdate: show type of update in mandrivaupdate (fix,
  security, ...) [spec 216]
- rpmdrake:
  o update GUI package list

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 4.9.16-1mdv2009.0
+ Revision: 219915
- rpmdrake:
  o fix crash in URPM with non standard package names (#41002)
- MandrivaUpdate (#40235):
  o laptop mode (height not bigger than 480): fix test

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri May 23 2008 Thierry Vignaud <tv@mandriva.org> 4.9.15-1mdv2009.0
+ Revision: 210387
- rpmdrake:
  o list basesystem-* as meta-task too
- MandrivaUpdate (#40235):
  o laptop mode (height not bigger than 480):
    * do not display banner
    * reduce Trees' height

* Thu May 08 2008 Thierry Vignaud <tv@mandriva.org> 4.9.14-1mdv2009.0
+ Revision: 204461
- display URLs of packages (#40571)
- handle gracefully locked RPM DB when trying to install some packages
  (#40244)
- warn only once about priority upgrades (#39737)
- MandrivaUpdate:
  o provide --no-splash option in order to skip splash screen when run
    from mdkapplet (#40366)
- rpmdrake:
  o GUI packages view:
    * adapt to KDE3 moving into /opt
    * include KDE applets into GUI packages view (#40073)
    * update list
  o do not list backports as unselected updates media in rpmdrake, not
    just in MandrivaUpdate (#35009, #40556)
  o fix a crash when default view is unknown (#40025)
  o fix searching when numeric pad's return key is pressed

* Thu Apr 03 2008 Thierry Vignaud <tv@mandriva.org> 4.9.13-1mdv2008.1
+ Revision: 192105
- updated translations

* Tue Apr 01 2008 Thierry Vignaud <tv@mandriva.org> 4.9.12-1mdv2008.1
+ Revision: 191478
- better error message while downloading mirror list (#39675)
- rpmdrake:
  o fix view tooltip (#39694)
  o really make "by update availability" view usable (#39461)
  o split out installed packages if any in "by update availability" view

* Tue Apr 01 2008 Thierry Vignaud <tv@mandriva.org> 4.9.11-1mdv2008.1
+ Revision: 191338
- rpmdrake:
  o really remove "--emmbedded <id>" from ARGV when restarting after
    priority upgrades, thus fixing displaying it when run from mcc
    (#39262)
- softenize requires on mdv-rpm-summary (aka put a Suggests)

* Mon Mar 31 2008 Thierry Vignaud <tv@mandriva.org> 4.9.10-1mdv2008.1
+ Revision: 191263
- rpmdrake:
  o do not crash if package is unknow (#39608)
  o do not crash if config file set empty values for some variables
    (eg: after old buggy gurpmi.addmedia garbaged it) (#39511)
  o fix priority upgrades:
    * do not preselect updates
    * do not recompute them when checking selection consistency just
      before actually installing

* Fri Mar 28 2008 Thierry Vignaud <tv@mandriva.org> 4.9.9-1mdv2008.1
+ Revision: 190866
- gurpmi.addmedia:
  o handle --mirrorlist (Anssi)
  o drop 'with' parameter, it didn't work properly anymore (Anssi)
  o do not garbage ~/.rpmdrake
  o fix --distrib
  o fix --distrib --mirrorlist
- rpmdrake:
  o make "by update availability" view usable (#39461)

* Tue Mar 25 2008 Thierry Vignaud <tv@mandriva.org> 4.9.8-1mdv2008.1
+ Revision: 189953
- ensure we always restart if needed
- fix displaying garbaged UTF-8 descriptions (eg: cgoban1)
  (instead of displaying "none")
- remove "--emmbedded <id>" from ARGV when restarting after priority
  upgrades, thus fixing displaying it when run from mcc (#39262)
- workaround crashing while performing medium name lookup (#38793)

* Fri Mar 21 2008 Thierry Vignaud <tv@mandriva.org> 4.9.7-1mdv2008.1
+ Revision: 189436
- make the focus default on "yes" in yes/no dialogs
  (Emmanuel Blindauer, #39123)

* Thu Mar 20 2008 Thierry Vignaud <tv@mandriva.org> 4.9.6-1mdv2008.1
+ Revision: 189143
- rpmdrake:
  o actually restrict "by_leaves" view to current mode (#39090)
  o fix sorting in "by_source" view

* Wed Mar 19 2008 Thierry Vignaud <tv@mandriva.org> 4.9.5-1mdv2008.1
+ Revision: 188966
- rpmdrake:
  o readd by_source view (removed on 2006-07-09)

* Wed Mar 19 2008 Thierry Vignaud <tv@mandriva.org> 4.9.4-1mdv2008.1
+ Revision: 188920
- rpmdrake:
  o handle migrating config file from rpmdrake <= 4.9
  o restore sorting packages in 'by_group' view
    (regression introduced in 4.8 while restoring flat mode)

* Wed Mar 19 2008 Thierry Vignaud <tv@mandriva.org> 4.9.3-1mdv2008.1
+ Revision: 188855
- rpmdrake:
  o fix crash with cs, cy, eu, hu, nl, pl & zh_CN locales (#39052)
    (regression introduced in 4.9: "move view pull down menu as a real
    menu")

* Wed Mar 19 2008 Thierry Vignaud <tv@mandriva.org> 4.9.2-1mdv2008.1
+ Revision: 188742
- restore translation of "Find:"

* Tue Mar 18 2008 Thierry Vignaud <tv@mandriva.org> 4.9.1-1mdv2008.1
+ Revision: 188725
- rpmdrake:
  o add "search:" label again (was removed in 4.8 on 17 March 2008)

* Tue Mar 18 2008 Thierry Vignaud <tv@mandriva.org> 4.9-1mdv2008.1
+ Revision: 188719
- fix displaying data about packages when choosing one while resolving
  dependancies (#39042)
  (regression introduced in "display in bold that priority updates
  require restarting" in 4.6 on 10 March 2008)
- rpmdrake:
  o be nice with UMPC screens:
    * enable to shrink package groups tree (#38762)
    * hide banner if screen height is small than 600 px (#38943)
  o move view pull down menu as a real menu
- bump requires on drakxtools due to needed API

* Mon Mar 17 2008 Thierry Vignaud <tv@mandriva.org> 4.8-1mdv2008.1
+ Revision: 188417
- tell the user to "restart system" when needed (needs urpmi-5.14)
- rpmdrake:
  o add tooltips to pull down menus & to search entry
  o allow to sort packages by size (#25417)
  o make find box larger and left-aligned (#38298)
  o restore flat mode (#25770)

* Mon Mar 17 2008 Thierry Vignaud <tv@mandriva.org> 4.7-1mdv2008.1
+ Revision: 188247
- consider rpm-summary-non-free when fetching package summaries
- rpmdrake:
  o split filters (all, installed, non installed) from views (GUI,
    meta packages, updates, ...)
  o update GUI package list

* Fri Mar 14 2008 Thierry Vignaud <tv@mandriva.org> 4.6.2-1mdv2008.1
+ Revision: 187905
- write configuration before restarting after priority upgrades so
  that we don't ask questions again
- rpmdrake:
  o kill "Mandriva choices"
  o only list priority upgrades if there're
  o warn there're priority upgrades when selecting other packages (#38885)

* Mon Mar 10 2008 Thierry Vignaud <tv@mandriva.org> 4.6.1-1mdv2008.1
+ Revision: 183948
- rpmdrake:
  o do not update media unlike MandrivaUpdate
    (regression introduced in 4.4: "remember latest view mode
    (#38138)")
- bump require on binary perl packages in order to ensure a working perl-5.10
  modules set

* Mon Mar 10 2008 Thierry Vignaud <tv@mandriva.org> 4.6-1mdv2008.1
+ Revision: 183603
- display in bold that priority updates require restarting
- MandrivaUpdate:
  o faster startup if there're priority updates
  o only list priority updates if existing
- rpmdrake:
  o fix listing twice updates from media tagged as update
    (regression introduced in 4.4.2)

* Fri Mar 07 2008 Thierry Vignaud <tv@mandriva.org> 4.5-1mdv2008.1
+ Revision: 181417
- reimplement priority upgrade support through urpmi-5.9's
  infrastructure
- when restarting after priority upgrade, free memory used by previous
  rpmdrake instance

* Thu Mar 06 2008 Thierry Vignaud <tv@mandriva.org> 4.4.2.3-1mdv2008.1
+ Revision: 181054
- fix error introduced in 4.4.2.1
- fix error introduced in 4.4.2.1

* Thu Mar 06 2008 Thierry Vignaud <tv@mandriva.org> 4.4.2.1-1mdv2008.1
+ Revision: 180968
- fix error introduced in 4.4.2

* Thu Mar 06 2008 Thierry Vignaud <tv@mandriva.org> 4.4.2-1mdv2008.1
+ Revision: 180964
- MandrivaUpdate:
  o fix not listing all updates (#*38595)
    (regression introduced in 4.4 with 'remember state of "Show
    automatically selected packages" (#38138)'
- rpmdrake:
  o don't select all updates by default in rpmdrake (#38611)
    (regression introduced in 4.3.2 with "handle priority upgrade list")

* Wed Mar 05 2008 Thierry Vignaud <tv@mandriva.org> 4.4.1-1mdv2008.1
+ Revision: 180035
- fix crash (#38514) due to not having commited all bits of 'remember
  state of "Show automatically selected packages" (#38138)'
- rpmdrake:
  o do not reset search field

* Wed Mar 05 2008 Thierry Vignaud <tv@mandriva.org> 4.4-1mdv2008.1
+ Revision: 179344
- do not warn about empty package names (#38480)
- rpmdrake:
  o make search box larger (#38298)
  o remember latest view mode (#38138)
  o remember state of "Show automatically selected packages" (#38138)

* Wed Mar 05 2008 Thierry Vignaud <tv@mandriva.org> 4.3.2-1mdv2008.1
+ Revision: 179307
- adapt to urpmi-5.7 API:
  o don't want to force a device anymore
  o handle new "cdrom://" type
- handle --test
- handle priority upgrade list
- reuse more urpmi code
- bump require on urpmi
- better description (adam)

* Wed Feb 27 2008 Thierry Vignaud <tv@mandriva.org> 4.3.1-1mdv2008.1
+ Revision: 175767
- rpmdrake's package list:
  o make select checkbox not activatable for base packages instead of
    popup an explanation
  o update icon set
- package NEWS

* Tue Feb 26 2008 Thierry Vignaud <tv@mandriva.org> 4.3-1mdv2008.1
+ Revision: 175447
- display size of data to downloaded (#32154)
- make clearer why there's no medium (#37033) (maybe should we just
  not display the medium for installed packages like old_rpmdrake
  did?)
- rpmdrake:
  o remove leading/trailing spacing in searched word when pasting (#23249)
  o package list:
    * hide architecture column on non biarch systems
    * shrink some column headers
    * statut column:
      + add a label to its header
      + move it at end
      + no icon for uninstalled packages

* Tue Feb 26 2008 Thierry Vignaud <tv@mandriva.org> 4.2.6-1mdv2008.1
+ Revision: 175202
- rpmdrake:
  o adapt to urpmi-5.6 API
  o show KDE4 apps in 'GUI packages' view too
- edit-urpm-sources:
  o display proper type for mirror lists

* Mon Feb 25 2008 Thierry Vignaud <tv@mandriva.org> 4.2.5-2mdv2008.1
+ Revision: 174812
- add require on perl-File-MimeInfo since we lazy load it since rpmdrake-4.2
- add require on perl-Gtk2-SourceView since we lazy load it now (#37958)
  (regression introduced in rpmdrake-3.127)

* Sat Feb 23 2008 Thierry Vignaud <tv@mandriva.org> 4.2.5-1mdv2008.1
+ Revision: 174081
- edit-urpm-sources:
  o fix crashing on clicking on "Create media for a whole
    distribution" (regression introduced in rpmdrake-4.2)
- MandrivaUpdate:
  o adjust default layout repartition (#36069)

* Fri Feb 22 2008 Thierry Vignaud <tv@mandriva.org> 4.2.3-1mdv2008.1
+ Revision: 174015
- edit-urpm-sources:
  o add a progress bar while downloading mirrors list & enable to
    cancel it (#34630)
  o fix crashing when adding a custom medium (regression introduced in
    4.2)
  o set 'ftp_proxy' with the same value as 'http_proxy' (#31026)

* Fri Feb 22 2008 Thierry Vignaud <tv@mandriva.org> 4.2.2-1mdv2008.1
+ Revision: 173898
- rpmdrake:
  o 'GUI packages' view now include graphical packages from all media

* Thu Feb 21 2008 Thierry Vignaud <tv@mandriva.org> 4.2.1-1mdv2008.1
+ Revision: 173721
- edit-urpm-sources
  o drop architecture choice
  o only ask api.mdv.com for 'distrib' style URLs
  o rename "Quit" as "Close" (more consistent when run whithin
    rpmdrake)

* Thu Feb 21 2008 Thierry Vignaud <tv@mandriva.org> 4.2-1mdv2008.1
+ Revision: 173635
- rpmdrake:
  o fix a bug in unused/unsupported parallel mode
  o fix calling help
- edit-urpm-sources
  o display better formatted list when confirming removing media
  o drop support for "Relative path to synthesis/hdlist"
  o factorize some code
  o fix altering XML info policy on cancel
  o make all global options use combo boxes & simplify code
  o reorder 'File' menu ('Quit' is now last)
- explain a require
- fix URL
- kill now useless requires on packdrake, perl-Compress-Zlib & rpmtools
- bump require on drakxtools for needed API
- bump require on perl-URPM due to API changes

* Tue Feb 19 2008 Thierry Vignaud <tv@mandriva.org> 4.1-1mdv2008.1
+ Revision: 173043
- rpmdrake:
  o default to 'GUI packages' view
- edit-urpm-sources
  o allow user to specify how rpmdrake handles .xml.lzma files (#37390)
  o fix menu entries in br locale
  o prevent rpmdrake to ask adding sources if already done through the
    media manager (#37360)

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 4.0-1mdv2008.1
+ Revision: 168609
- rpmdrake:
  o also list as GUI packages those having menu entries into
    /usr/share/applications/kde/ & old /usr/share/applnk/
  o do not quit rpmdrake if urpmi db is locked when running media
    manager

* Wed Feb 13 2008 Thierry Vignaud <tv@mandriva.org> 3.144-1mdv2008.1
+ Revision: 167064
- fix garbaged accents in changelogs when they containing UTF-8 &
  ISO-8859-1 lines) ;
  only remaining ones are when rpm mixes strftime(localtime()) with
  mixed UTF-8/ISO-8859-1 changelogs (eg: 7.0-8mdv2007.0 in vim) ;
  not much we can do w/o fixing all /log in SVN
- rpmdrake:
  o do not crash when a icon is missing (#37700)
  o fix a crash on searching (#37626)
  o revert ignoring disabled backport media in rpmdrake too, not just
    in MandrivaUpdate (#35009) since it's broken

* Wed Feb 13 2008 Thierry Vignaud <tv@mandriva.org> 3.143-1mdv2008.1
+ Revision: 167021
- rpmdrake:
  o skip non existing packages (#36529)
    (eg: when rpmdrake download info.xml.lzma on demand when searching
    or browsing whereas the package was updated in the mean time, the
    info file references the newer package whereas urpmi database only
    know the older version)

* Wed Feb 13 2008 Thierry Vignaud <tv@mandriva.org> 3.142-1mdv2008.1
+ Revision: 166945
- ignore disabled backport media in rpmdrake too, not just in MandrivaUpdate
  (#35009)

* Tue Feb 12 2008 Thierry Vignaud <tv@mandriva.org> 3.141-1mdv2008.1
+ Revision: 165727
- rpmdrake:
  o add list of programs with GUI view (#36486)
  o align search fields to right
  o ensure we never crash on garbaged UTF-8 while querying local files
    (which results in garbaged names in eg vim changelog instead of crashes)
  o move search types menu into Entry
  o only flush X11 queue every 100 packages (seems enough on medium
    machines)
  o really flush X11 queue only every 10 package

* Mon Feb 11 2008 Thierry Vignaud <tv@mandriva.org> 3.140-1mdv2008.1
+ Revision: 165442
- fix no-cleaning-of-buildroot
- rpmdrake:
  o add spacing between search & view widgets
  o simplify GUI using Gtk2::Sexy::IconEntry
- bum require on drakxtools for Gtk2::Sexy::IconEntry support

* Mon Feb 11 2008 Thierry Vignaud <tv@mandriva.org> 3.139-1mdv2008.1
+ Revision: 165284
- rpmdrake:
  o download XML meta-data if needed while searching

* Mon Feb 11 2008 Thierry Vignaud <tv@mandriva.org> 3.138-1mdv2008.1
+ Revision: 165191
- rpmdrake:
  o fix canceling search in file lists or in descriptions
  o flush X queue only every 10 packages while searching

* Fri Feb 08 2008 Thierry Vignaud <tv@mandriva.org> 3.137-1mdv2008.1
+ Revision: 164263
- fix querying file list of installed packages (regression introduced
  in 3.134: "fix formating of file list of installed packages")
- highlight relevant parts of the changelog as italic (#37208)
- render update fields as italic (type & reason of update)
- separate version and release by '-' in details
- use the same format for changelogs from XML metadata as for those
  coming from old hdlists and from queries on local packages

* Thu Feb 07 2008 Thierry Vignaud <tv@mandriva.org> 3.136-1mdv2008.1
+ Revision: 163683
- adapt to new urpmi API for searching in XML meta-data, thus stopping
  from downloading hdlists, side effect of urpmi-5.x (#37411)
- drop old style menu (#37556)

* Wed Feb 06 2008 Thierry Vignaud <tv@mandriva.org> 3.135-1mdv2008.1
+ Revision: 163114
- fix formating of file list of non installed packages

* Wed Feb 06 2008 Thierry Vignaud <tv@mandriva.org> 3.134-1mdv2008.1
+ Revision: 163049
- add a meta packages view (#34510)
- display a message in statusbar while extracting metada from a local
  package
- display size of selection (#34123)
- do not display the download progress dialog when not downloading,
  only a statusbar message
- download & parse the needed XML meta data on demand (aka only
  download & parse the needed ones and not all of them) ;
  always update & fetch 'info' metada on click for descriptions
- fallback to get XML metada when RPM is missing from local medium
- fix extracting info from packages from local media (#37354)
- fix formating of file list of installed packages
- fix setting UTF-8 locale when running rpm for query
- make progres dialogs not be grayed on initial display
- make sure we destroy the XML download progress dialog on error
- stop downloading & parsing the XML meta data on selecting a package (side
  effect of urpmi-5.x)

* Mon Feb 04 2008 Thierry Vignaud <tv@mandriva.org> 3.133-1mdv2008.1
+ Revision: 162389
- fix MandrivaUpdate not ignoring backport media tagged as update (#36654)

* Mon Feb 04 2008 Thierry Vignaud <tv@mandriva.org> 3.132-1mdv2008.1
+ Revision: 162251
- display a progress bar while fetching XML metadata (#37264) (needs
  urpmi-5.3)
- do not include architecture in SRPM names, thus fixing extracting
  info for SRPMS and RPM GPG keys
- fix a breakage in unused/unmaintained parralel mode
- fix encoding of rpm error message "package contains no file" (#37428)

* Wed Jan 30 2008 Thierry Vignaud <tv@mandriva.org> 3.131-1mdv2008.1
+ Revision: 160268
- gracefully handle "could not find foobar in <xml_info_file>" (#37211)
- bump urpmi requires due to API changes

* Wed Jan 30 2008 Thierry Vignaud <tv@mandriva.org> 3.130-1mdv2008.1
+ Revision: 160109
- use urpmi downloader in order to retrieve mirror list from
  api.mandriva.com, instead of forcing curl (thus using urpmi's proxy
    settings)
- drop now useless curl XS binding
- remove hard require on curl (now relying on urpmi requiring webfetch)
- rpmdrake is now a noarch package

* Fri Jan 25 2008 Thierry Vignaud <tv@mandriva.org> 3.129-1mdv2008.1
+ Revision: 158069
- do not show "backports" in the list of filters if there's no
  inactive backport medium (#37088)
- make sure a wait dialog always got killed (might fix #36921)

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 3.128-2mdv2008.1
+ Revision: 157189
- rebuild for fixed changelog

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 3.128-1mdv2008.1
+ Revision: 157175
- fix a crash on extracting package header (#37122)
- prevent selecting basesystem packages earlier (#36367)

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 3.127-1mdv2008.1
+ Revision: 157147
- fix a crash when using empty inactive backport media (#36720)

* Tue Jan 22 2008 Thierry Vignaud <tv@mandriva.org> 3.126-1mdv2008.1
+ Revision: 156800
- adapt to new urpmi-5.x API and use XML info instead of hdlist when
  possible
- typo fix (Shlomi Fish, #36365)

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 3.125-2mdv2008.1
+ Revision: 152149
- rebuild for new perl

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 3.125-1mdv2008.1
+ Revision: 134674
- fix reading urpmi options with new urpmi (#36681)
- renamed Uzbek translations to follow the libc standard (#35090)
- kill re-definition of %%buildroot on Pixel's request

* Thu Dec 06 2007 Thierry Vignaud <tv@mandriva.org> 3.124-1mdv2008.1
+ Revision: 115911
- fix sorting by using RPM version sorting logic (#35209)

* Wed Dec 05 2007 Thierry Vignaud <tv@mandriva.org> 3.123-1mdv2008.1
+ Revision: 115591
- ensure message is displayed in status bar instaneously
- explain long operations in status bar
- MandrivaUpdate: fix fetching updates from non update media (#35009)

* Thu Nov 29 2007 Thierry Vignaud <tv@mandriva.org> 3.122-1mdv2008.1
+ Revision: 113939
- edit_urpm_sources: update button labels & message in order to make
  the clearer and more up to date concerning current media structure
  (#35834)
- rpmdrake:
  o drop --pkg-sel and --pkg-nosel broken options (introduced in
    rpmdrake-2.1.2-8mdk on Feb 26 2004 for MandrakeOnline which didn't
    use them since 2007.0)
  o use urpmi default values for 'split-level' and 'split-length' options
- bump require on urpmi for default split values

* Mon Nov 26 2007 Thierry Vignaud <tv@mandriva.org> 3.121-1mdv2008.1
+ Revision: 112200
- add support for --wait-lock option

* Tue Oct 23 2007 Thierry Vignaud <tv@mandriva.org> 3.120-1mdv2008.1
+ Revision: 101491
- MandrivaUpdate, rpmdrake: split "release" column from "version"
  column

* Tue Oct 23 2007 Thierry Vignaud <tv@mandriva.org> 3.119-1mdv2008.1
+ Revision: 101397
- factorize some code
- edit_urpm_sources:
  o display nicer media with non ASCII characters in names (#34906)
- MandrivaUpdate:
  o ensure mirror list got centered on MandrivaUpdate
  o explain the actual issue when there's no configured update medium
  o nicer names for update media

* Mon Oct 08 2007 Thierry Vignaud <tv@mandriva.org> 3.118-1mdv2008.0
+ Revision: 95713
- MandrivaUpdate: do not add shadow 'in' around Gtk2::SimpleList since mygtk2
  already do it now
- split park-rpmdrake out of rpmdrake

* Thu Oct 04 2007 Thierry Vignaud <tv@mandriva.org> 3.117-1mdv2008.0
+ Revision: 95454
- really report distro release in about dialog

* Thu Oct 04 2007 Thierry Vignaud <tv@mandriva.org> 3.116-1mdv2008.0
+ Revision: 95414
- MandrivaUpdate, edit-urpm-sources:
  o install all update media (Main, restricted, Non-Free, ...)
    (needs urpmi-4.10.14)

* Wed Oct 03 2007 Thierry Vignaud <tv@mandriva.org> 3.115-1mdv2008.0
+ Revision: 95032
- updated translation

* Wed Oct 03 2007 Thierry Vignaud <tv@mandriva.org> 3.114-1mdv2008.0
+ Revision: 94852
- fix 2 untranslated strings in MandrivaUpdate

* Fri Sep 28 2007 Thierry Vignaud <tv@mandriva.org> 3.113-1mdv2008.0
+ Revision: 93651
- do refresh package list after updating media (#34241)

* Thu Sep 27 2007 Thierry Vignaud <tv@mandriva.org> 3.112-1mdv2008.0
+ Revision: 93347
- workaround canceled selection still selected (#34218);
  side effect: no more explanations for (un)selectioned dependencies

* Wed Sep 26 2007 Thierry Vignaud <tv@mandriva.org> 3.111-1mdv2008.0
+ Revision: 93149
- fix sorting

* Wed Sep 26 2007 Thierry Vignaud <tv@mandriva.org> 3.110-1mdv2008.0
+ Revision: 93148
- MandrivaUpdate:
  o display package name, version & arch as 3 separate columns rather
    than raw urpm fullname (for consistency with rpmdrake)
  o enable to sort these columns
  o show columns headers in package list

* Wed Sep 26 2007 Thierry Vignaud <tv@mandriva.org> 3.109-1mdv2008.0
+ Revision: 93121
- prevent not-on-open errors to exec edit-urpmi-sources on next DB open

* Tue Sep 25 2007 Thierry Vignaud <tv@mandriva.org> 3.108-1mdv2008.0
+ Revision: 92793
- remove a now useless hack
- updated translations

* Mon Sep 24 2007 Thierry Vignaud <tv@mandriva.org> 3.107-1mdv2008.0
+ Revision: 92458
- fix crashing while reporting db is locked (#33963)

* Mon Sep 24 2007 Thierry Vignaud <tv@mandriva.org> 3.106-1mdv2008.0
+ Revision: 92453
- properly account size of update packages (#33851)
- use field code %%f for Exec field of gurpmi.addmedia as only local
  files are accepted (anssi)

* Fri Sep 21 2007 Thierry Vignaud <tv@mandriva.org> 3.105-1mdv2008.0
+ Revision: 91917
- make "Reset the selection" work if no group is selected in tree
- properly account size of update packages (#33851)

* Fri Sep 21 2007 Thierry Vignaud <tv@mandriva.org> 3.104-1mdv2008.0
+ Revision: 91831
- searches in summaries in rpmdrake:
  o make them an order of magniture faster
  o make them case insensitive like searches in package names

* Thu Sep 20 2007 Thierry Vignaud <tv@mandriva.org> 3.103-1mdv2008.0
+ Revision: 91533
- revert a change that introduced a regression in MandrivaUpdate (no
  more selecting updates)

* Thu Sep 20 2007 Thierry Vignaud <tv@mandriva.org> 3.102-1mdv2008.0
+ Revision: 91436
- buildrequires intltool
- fix build
- enable to copy/paste transaction errors
- fix a crash on removing packages
- fix counting size of selected package (#32506)
- installing/removing confirmation dialog box:
  o always display "Is it ok to continue?"
  o better formatting
  o display added/removed size
  o make to be installed package & to be removed package lists look
    consistent
- make sure some progress dialogs disapear

* Wed Sep 19 2007 Thierry Vignaud <tv@mandriva.org> 3.100-1mdv2008.0
+ Revision: 90854
- reports staring the browser in status bar rather than with an
  annoying popup
- rpmdrake:
  o do not show banner in media manager
  o enable to sort by state

* Wed Sep 19 2007 Thierry Vignaud <tv@mandriva.org> 3.99-1mdv2008.0
+ Revision: 90591
- edit-urpm-sources: put menubar above banner
- ensure perl-URPM returns UTF-8
- make sure MandrivaUpdate & rpmdrake hits the same code paths

  + Anssi Hannula <anssi@mandriva.org>
    - call clean_desktop_database on postun

* Tue Sep 18 2007 Thierry Vignaud <tv@mandriva.org> 3.98-1mdv2008.0
+ Revision: 89768
- better looking message for bad signatures
- register application/x-urpmi-media MIME type again (#33436)
- rpmdrake:
  o enable to sort by selected status (#27338)
- make package list be sortable

* Mon Sep 17 2007 Thierry Vignaud <tv@mandriva.org> 3.96-1mdv2008.0
+ Revision: 89268
- hide all but main menu entries
- MandrivaUpdate, rpmdrake:
  o make package names appear in bold
- rpmdrake:
  o force align "name - summary" to the right with RTL languages (#33603)
  o indent expanders' contents (details, file list, changelog)

* Fri Sep 14 2007 Thierry Vignaud <tv@mandriva.org> 3.95-1mdv2008.0
+ Revision: 85586
- display update description for both the ia32 and the x86_64 packages
  (needs urpmi-4.10.10)
- fix reading descriptions from update media (got broken in 3.76 when
  switching ro urpmi for parsing "descriptions" files)
- gurpmi.addmedia:
  o display the URL when bogus
  o enable to use --urpmi-root & co options
  o handle --distrib (#33435)

* Fri Sep 14 2007 Thierry Vignaud <tv@mandriva.org> 3.94-1mdv2008.0
+ Revision: 85413
- force sizing of Labels in order to prevent garbaged wrapping with
  hebrew (#32882)
- run the regular user browser (#31021)
- bump require on drakxtools for setuid support

* Wed Sep 12 2007 Andreas Hasenack <andreas@mandriva.com> 3.93-2mdv2008.0
+ Revision: 84828
- use new common pam config files for usermode/consolehelper

* Wed Sep 12 2007 Thierry Vignaud <tv@mandriva.org> 3.93-1mdv2008.0
+ Revision: 84680
- make sure we reread the db if we added a new repository on startup
- further improve startup time by killing a costly
  urpm::media::configure that is only needed in some cases (#33334)

* Tue Sep 11 2007 Thierry Vignaud <tv@mandriva.org> 3.92-1mdv2008.0
+ Revision: 84446
- startup time (#33334):
  o reduce package enumeration by 10%
  o shrink opening urpmi DB time by 30%
- edit-urpm-sources:
  o enable --urpmi-root options and the like
- rpmdrake:
  o make "Package" column use all available space
  o rephrasing (#33188)

* Mon Sep 10 2007 Thierry Vignaud <tv@mandriva.org> 3.91-1mdv2008.0
+ Revision: 84154
- rpmdrake:
  o do not try to convert into UTF-8, thus fixing a SIGV loop while inserting
    file list of "balazar" package
  o fix a crash (#33283)
  o fix order of columns
  o simplify (since perl-URPM-1.56, perl knows that strings from rpm headers
    are UTF-8)

* Mon Sep 10 2007 Thierry Vignaud <tv@mandriva.org> 3.90-1mdv2008.0
+ Revision: 84097
- edit-urpm-sources:
  o display a banner now that we don't display mcc's banner & menubar
    while embedded (side effect of #33316's fix)
- updated translations

* Thu Sep 06 2007 Thierry Vignaud <tv@mandriva.org> 3.89-1mdv2008.0
+ Revision: 81032
- fix not displaying summaries when already translated and encoded in
  UTF-8 in rpm
- rpmdrake:
  o list media from all backport media (needs urpmi' SVN)
  o package list:
    * add margins in package list's columns
    * add margins to columns titles

* Thu Sep 06 2007 Thierry Vignaud <tv@mandriva.org> 3.88-1mdv2008.0
+ Revision: 80674
- gurpmi.addmedia: do not always adds repository as update medium (#30440)
- rpmdrake:
  o package list:
    * disable fixed mode
    * display package name, version & arch as 3 separate columns rather
      than raw urpm name; autosize them
    * display summary too
    * ellipsize package name column & make it resizable
    * show columns headers

* Mon Sep 03 2007 Thierry Vignaud <tv@mandriva.org> 3.87-1mdv2008.0
+ Revision: 78656
- MandrivaUpdate:
  o make "Select all" button working (#29892)
- rpmdrake:
  o kill "help" button in button bar (which was there because we
    didn't have any menubar when embedded) (#29883)

* Mon Sep 03 2007 Thierry Vignaud <tv@mandriva.org> 3.86-1mdv2008.0
+ Revision: 78626
- edit-urpm-sources:
  o swap "add custom" and "add sources" between menubar and buttons bar
- rpmdrake:
  o fix erasing all existing media when adding new media on first
    startup of rpmdrake (#30883)

* Mon Sep 03 2007 Thierry Vignaud <tv@mandriva.org> 3.85-1mdv2008.0
+ Revision: 78528
- fix a regression introduce in 3.84

* Mon Sep 03 2007 Thierry Vignaud <tv@mandriva.org> 3.84-1mdv2008.0
+ Revision: 78517
- really fix --no-verify-rpm option
- edit-urpm-sources: display media type in media list (#25043)
- rpmdrake: enable to select a package listed in urpmi's skip.list (#31548)

* Fri Aug 31 2007 Andreas Hasenack <andreas@mandriva.com> 3.83-3mdv2008.0
+ Revision: 77150
- point edit media menu entry to bindir dir instead of sbindir

* Fri Aug 31 2007 Andreas Hasenack <andreas@mandriva.com> 3.83-2mdv2008.0
+ Revision: 77074
- drakrpm-edit-media: ask console user for root password
- {drakrpm,rpmdrake}-remove: ask console user for root password
- MandrivaUpdate, per Rights Delegation spec, should ask for user password, not root password

* Thu Aug 30 2007 Thierry Vignaud <tv@mandriva.org> 3.83-1mdv2008.0
+ Revision: 75284
- add --run-as-root option as equivalent to --root
- always enable scrolling when asking question in order to be able to
  copy/paste error messages
- deprecate --root option
- do not disable no-verify-rpm option if set in urpmi.cfg but not
  passed to rpmdrake through command line
- fix --no-verify-rpm option (got broken when introducing
  urpm::main_loop)
- temporary workaround gtk+ regression that mess up when shrinking a
  window (#32613)
- use X-MandrivaLinux-CrossDesktop category in menu entries

* Tue Aug 28 2007 Thierry Vignaud <tv@mandriva.org> 3.82-1mdv2008.0
+ Revision: 72788
- merge old desktop entries for g-c-c with menu ones:
  o make them translated
  o add mandrivaupdate & edit-urpm-sources icons
- shrink rpmdrake menu entry
- new desktop entries are no more prefixed
- kill desktop entries inlined in spec file since they're now within sources

* Mon Aug 27 2007 Thierry Vignaud <tv@mandriva.org> 3.81-1mdv2008.0
+ Revision: 72015
- refresh packages tree when edit-urpm-sources performed something
  thus fixing crash when removing source then selecting a package that
  is no more know to urpmi (#32832)

* Mon Aug 27 2007 Thierry Vignaud <tv@mandriva.org> 3.80-1mdv2008.0
+ Revision: 71826
- all:
  o add a "Do not ask me next time" checkbox when asking about media
    update (#17697)
  o ensure we respect 'auto' option in /etc/urpmi.cfg
  o make clearer how to use --rpm-root
  o warn if misusing --rpm-root option
- edit-urpm-source:
  o ensure update progress dialog is centered upon main window
  o fix moving altered medium at end of media list (#32489)
  o make all buttons look consistent regarding "..."
  o move all buttons not directely related to media list in a new menu
    bar (#14439)
  o show a standard "help" menu
  o rework some strings
- MandrivaUpdate:
  o do not update again media after installing/removing some packages (#32586)
  o restore rpmdrake-2.x behaviour (which is inconsistant with urpmi
    one) by only computing updates on media flagged as update (#30546)
- rpmdrake:
  o enable to search only in summaries (previously "in descriptions"
    used to search in both in descriptions and in summaries
  o make search progress dialog appears immediately rather than after
    a few seconds delay
  o make non basic searches faster (saving 25%% of time spent when
    searching in packages' files)
  o remove not found messages from status bar after 5 seconds (#32332)

* Fri Aug 24 2007 Thierry Vignaud <tv@mandriva.org> 3.79-1mdv2008.0
+ Revision: 71060
- fix crash if no backport medium is configured (aka no std configuration, #32815)

* Fri Aug 24 2007 Thierry Vignaud <tv@mandriva.org> 3.78-1mdv2008.0
+ Revision: 71021
- first attempt to provide a "Backports" view (it only looks at first disabled
  backport medium)

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 3.77-1mdv2008.0
+ Revision: 70040
- add new "System/Printing" group
- fix error if urpm::install stoped early (#32504)
- fix running as a user (#32496)
- new option --justdb (new perl-URPM 1.76 & urpmi 4.10.6)
- prevent some gtk+ warnings

* Mon Aug 13 2007 Thierry Vignaud <tv@mandriva.org> 3.76-1mdv2008.0
+ Revision: 62438
- add support for --rpm-root and --urpmi-root (equivalent to urpmi
  --root and --urpmi-root options)
- display again removed packages (wasn't working since urpmi-4.9.24)
- display again removed packages when actually being removing and not
  before
- display already installed & not installable packages on errors
- do not create multiple useless N("Search results (none)") subtrees
  but display a message in status bar instead (#32332)
- do not unconditionnally enable 'allow-force' & 'allow-nodeps'
  options since we do no want end users to shoot themselves in the
  foot
- use urpmi for parsing "descriptions" files
- bump require on urpmi for new API
- bump require on urpmi for reading descriptions

* Sat Aug 11 2007 Thierry Vignaud <tv@mandriva.org> 3.75-1mdv2008.0
+ Revision: 61889
- implement --auto option (#16093)
- add a menu entry for --auto option (#16093)
- display which package failed, and from which hdlist (#32349)

* Fri Aug 10 2007 Thierry Vignaud <tv@mandriva.org> 3.74-1mdv2008.0
+ Revision: 61544
- add a warning: suggest to keep the current file if unsure while
  inspecting *.rpmnew
- better rendering of package lists
- factorize code through new urpm::main_loo module (100 lines killed
  while supporting new features)
- fix bad wrapping in "additional packages are needed" dialog
- handle 'allow-force' and 'allow-nodeps' options
- bump require on urpmi for new API

* Fri Aug 03 2007 Thierry Vignaud <tv@mandriva.org> 3.73-1mdv2008.0
+ Revision: 58595
- progress dialog:
  o align text to top
  o prevent vertical resizing
- remove workaround for buggy GNOME now that it has been fixed
- reduce duplication of code with urpmi
- handle README.<version>.upgrade.urpmi and
  README.<version>-<release>.upgrade.urpmi: the content is displayed when
  upgrading from rpm older than <version> (#30187)
- bump require on urpmi for READMEs list export

* Thu Aug 02 2007 Thierry Vignaud <tv@mandriva.org> 3.72-1mdv2008.0
+ Revision: 58318
- disable notifications (#18965)
- display again README.urpmi*
- do not list identical packages several times when existing in
  several medium since urpmi only consider the first one anyway (same
  behavior as old rpmdrake-2.x) (#31810)
- ensure list of update/install instructions is centered on main window
- open rpm database less often
- some internal refactoring
- rephrase (#30072)
- disable notifications (#18965)

* Tue Jul 03 2007 Thierry Vignaud <tv@mandriva.org> 3.71-1mdv2008.0
+ Revision: 47513
- prevent alarm() to mess up system(), thus making DVD being ejected
  and printing wrong error messages (#30463)

* Fri Jun 22 2007 Thierry Vignaud <tv@mandriva.org> 3.70-1mdv2008.0
+ Revision: 43249
- add "Development/X11" rpm group
- deprecate "Cluster/Message Passing", "Cluster/Queueing Services",
  "System/Deploiement" & "System/Deployment" groups in favor of new
  "System/Cluster" group
- set an icon for "System/X11" group

* Thu Jun 21 2007 Thierry Vignaud <tv@mandriva.org> 3.69-1mdv2008.0
+ Revision: 42330
- do hide again the progress window when install is completed but
  we've errors to display
- also hide it before displaying rpmnew/rpmsave files

* Wed Jun 13 2007 Thierry Vignaud <tv@mandriva.org> 3.68-1mdv2008.0
+ Revision: 38644
- rpmdrake:
  o do not display bogus medium for already installed packages (#30556)
  o fix crash when trying to save non set variables (#31367)
  o fix freezing the GNOME desktop when xterm is installed(#30867)
  o read config before warning if running as user in order to fix
    error when trying to save config (#31367)
- MandrivaUpdate: do handle skip.list if update media were updated (#31092)

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 3.67-2mdv2008.0
+ Revision: 36199
- rebuild with correct optflags

  + Thierry Vignaud <tv@mandriva.org>
    - ensure "initialization" dialog got destroyed if an error happens very early
      (ie if no package was ever installed)
    - rpmdrake: limit the number of results to 2000, else gtk+ takes quite
      a lot of time in order to render the lsit (#30355)

* Tue May 29 2007 Thierry Vignaud <tv@mandriva.org> 3.66-1mdv2008.0
+ Revision: 32446
- MandrivaUpdate: fix crash due to UTF-8 issue
- workaround crash due to option abuse (#30817)

* Wed May 02 2007 Thierry Vignaud <tv@mandriva.org> 3.65-1mdv2008.0
+ Revision: 20709
- fix crashing on invalid UTF8 package summaries (#30409)

* Mon Apr 30 2007 Thierry Vignaud <tv@mandriva.org> 3.64-1mdv2008.0
+ Revision: 19519
- readd back files lost after SVN crash (#30466)

* Wed Apr 25 2007 Thierry Vignaud <tv@mandriva.org> 3.63-1mdv2008.0
+ Revision: 18258
- MandrivaUpdate: escape characters, thus fixing duplicated names (#28970)
- rpmdrake: fix not refreshing a subcategory if old & new
  subcategories have the same name (#30421)
- when asking to choose a package among several ones, fix selecting
  first choice, thus preventing asking again the same question if
  choosing the first one


* Fri Apr 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.62-1mdv2007.1
+ Revision: 150872
- display a progress bar while removing packages
- display which package is beging removed
- do display some data if only one field is not UTF-8 valid
- ensure version as reported by rpmdrake --version is uptodate (#29840)
- reload the database if we removed some packages but didn't installed
  anything if an error happened or if first install transaction was canceled
- edit-urpm-sources: handle --help immediatly (#29971)
- rpmdrake:
  o fix one remaining Gtk+ warning
  o fix "rpmdrake --merge-all-rpmnew" (#29993)
  o only search in package listed in current mode (#29708

* Wed Apr 04 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.61-5mdv2007.1
+ Revision: 150580
- patch 1: fix adding official media on ia32 (#30059)

* Wed Apr 04 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.61-4mdv2007.1
+ Revision: 150576
- patch 0: fix error message when looking at a package when there's no medium (eg: one)

* Fri Mar 23 2007 Andreas Hasenack <andreas@mandriva.com> 3.61-3mdv2007.1
+ Revision: 148581
- go back to asking root password instead of user's password
  (#29833)

* Fri Mar 23 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.61-2mdv2007.1
+ Revision: 148328
- do not crash if selectable package list is empty

* Fri Mar 23 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.60-1mdv2007.1
+ Revision: 148318
- try harder to prevent progress dialog from resizing
- MandrivaUpdate:
  o check dependancies when toggling a package
  o drop "automatically_update_kernels" option now that kernel*-latest
    are handled at urpmi level
  o list again updates matching /etc/urpmi/skip.list (eg:
    kernel*-latest) now that we handle skip.list, but do not select
    them by default
  o fix installing more than selection

* Fri Mar 23 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.59-1mdv2007.1
+ Revision: 148209
- make it closable again in mcc (#26069)
- rpmdrake:
  o fix gtk+ warnings (#26798)
  o fix "unable to remove package" errors messages (#29823)
    (#29291's fix wasn't enough for updates packages)

* Thu Mar 22 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.58-1mdv2007.1
+ Revision: 148039
- do not show "cancel" button when listing alternatives to select
  (it's still possible to cancel later)
- edit_urpm_sources: enable to select ia32 for adding media (#28409)
- MandrivaUpdate:
  o do not refresh the list twice after installing some updates
  o once we updated some packages, refresh the list _after_ updating
    the package list
- rpmdrake: workaround cannot selecting a selected then unselected
  package witth deps (#28613)

  + Adam Williamson <awilliamson@mandriva.com>
    - install fd.o-compliant icons as well as old-style ones

* Wed Mar 21 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.57-2mdv2007.1
+ Revision: 147393
- bump release

* Wed Mar 21 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.57-1mdv2007.1
+ Revision: 147351
- ask confirmation _before_ actually removing packages
- config file management:
  o always read config file in root directory if EUID is 0
  o handle root directory not being /root
- fix bogus "unable to remove package" warnings (#29291)
- restore the main window sensivity if an exception occured

* Wed Mar 21 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.56-1mdv2007.1
+ Revision: 147182
- do not reload package databases when canceling installing
- fix error reporting with --parallel
- prevent mcc from complaining that we exited abnormally when
  canceling confirm dialiog (#29573)

* Tue Mar 20 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.55-2mdv2007.1
+ Revision: 147031
- bump release

  + Andreas Hasenack <andreas@mandriva.com>
    - place MandrivaUpdate under same consolehelper rules

* Tue Mar 20 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.55-1mdv2007.1
+ Revision: 147010
- rpmdrake: fix crash when looking at bugfix or security bugs (#29707)
- rpmdrake:
  o adjust somewhat the margins around the checkboxes
  o bump copyright years in about dialog

  + Andreas Hasenack <andreas@mandriva.com>
    - call rpmdrake directly when it's supposed to be run as root, consolehelper takes care of things

* Mon Mar 19 2007 Andreas Hasenack <andreas@mandriva.com> 3.53-2mdv2007.1
+ Revision: 146809
- allow a regular user to run rpmdrake as root (#29696) provided that:
  - the user types his/her password
  - the user is the console user

  + Thierry Vignaud <tvignaud@mandriva.com>
    - do not package big ChangeLog

* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.53-1mdv2007.1
+ Revision: 146495
- do display if it's a base package (broken since 2007.0)
- do not do anything on key press on the list (which conflicts/blocks
  such signals for Toggles) and this make rpmdrake behaving like other
  regular Gtk+ applications
- do refresh the list if something was installed even if a transaction
  failed (#29384)
- handle more gracefully crashes while installing
- split selection column into a toggle one and a status one, thus
  enabling to use a true (themable) ToggleButton instead of a manually
  randered one
- MandrivaUpdate: make it fit in 800x600
- rpmdrake: fix 'unable to update in "installed" view' (#27629)

* Fri Mar 16 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.52-1mdv2007.1
+ Revision: 144842
- display global count as well as transaction count while installing
- use fixed mode

* Thu Mar 15 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.51-1mdv2007.1
+ Revision: 144603
- bump require on drakxtools for saner mirror API
- don't report cryptic "undefined value as array" error message (#27429)

* Thu Mar 15 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.50-1mdv2007.1
+ Revision: 144506
- fix a crash introduced in 3.48
- use the "busy" cursor on the whole window when filling the package list

* Thu Mar 15 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.49-1mdv2007.1
+ Revision: 144404
- fix some transient hints
- prevent resizing in progress dialogs

* Thu Mar 15 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.48-1mdv2007.1
+ Revision: 144312
- save configuration on exit so that we "remember" we've offered to
  add media on first run
- MandrivaUpdate:
  o do not ask again to update media after installing some updates (#27427)
  o reduce default width
  o set a 3:2 ratio between the package list and the package description

* Wed Mar 14 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.47-1mdv2007.1
+ Revision: 143439
- edit_urpm_sources: refresh button states after moving a row (so that
  eg "up" button is disabled once top of list is reached)

* Tue Mar 13 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.46-1mdv2007.1
+ Revision: 142456
- MandrivaUpdate: fix a crash

* Fri Mar 09 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.45-1mdv2007.1
+ Revision: 139525
- edit_urpm_sources.pm: adapt "up" & "down" buttons to multiple
  selection mode (#29186)

* Thu Mar 08 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.44-1mdv2007.1
+ Revision: 137652
- make TreeViews non editable by default
- MandrivaUpdate:
  o make "update" button insensitive if no updates
  o warn when there're no updates

* Wed Mar 07 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.43-1mdv2007.1
+ Revision: 134579
- fix crash when adding sources on startup (#29252)

* Wed Mar 07 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.42-1mdv2007.1
+ Revision: 134446
- fix wrong count number while dowloading packages and sync messages
  with urpmi/gurpmi ones (#29237)
- skip broken require (b/c of my laziness)

* Wed Mar 07 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.41-1mdv2007.1
+ Revision: 134276
- edit_urpm_sources.pm: improved layout for keys management
- MandrivaUpdate:
  o display extended info about currently selected package (#28862, #28971)
  o reload package list after performing updades
- rpmdrake: show again version, currently installed version (#26946),
  source medium (#23153), size and architecture (#26410)

* Tue Mar 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.40-1mdv2007.1
+ Revision: 133942
- MandrivaUpdate: handle /etc/urpmi/skip.list

* Tue Mar 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.39-1mdv2007.1
+ Revision: 133851
- display version number if --version is given (#28858)
- edit_urpm_sources.pm:
  o fix editing a medium (#29204)
  o fix removing several medium (#29203)

* Tue Mar 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.38-1mdv2007.1
+ Revision: 133601
- missing packages:
  o display them at end of install
  o nicer display
- on first run, offer to set up the packages sources (#28050)
- edit-urpm-sources: set down/edit/remove/up buttons insensitive by default
- MandrivaUpdate: fix a crash
- rpmdrake:
  o display a wait message while removing packages
  o do not reread the urpm database if media manager didn't perform anything
  o fix installing packages (#29068)
  o fix removing packages by performing a removal pass before other transactions (#29070)

* Fri Mar 02 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.37-1mdv2007.1
+ Revision: 131218
- fix allow-nodeps handling
- MandrivaUpdate: automatically select kernels if /root/.rpmdrake
  contains "automatically_update_kernels 1"

* Fri Mar 02 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.36-1mdv2007.1
+ Revision: 131114
- add support for urpmi transactions:
  o display errors at end of installation
  o download only the transaction's packages at once (#16397)
  o fix canceling all installationss when one transaction failled (#26867)
- add support for preforming installation w/o deps & for forcing installation
- don't lock the urpmi db when displaying success/error messages at end
- fix emptying the cache (#26222)
- edit_urpm_sources: enable to delete several medium at once (#21532)
- MandrivaUpdate:
  o don't preselect kernel packages required by kernel*-latest too
  o refresh updates list at end of install

* Thu Mar 01 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.35-1mdv2007.1
+ Revision: 130369
- MandrivaUpdate: fix a crash
- rpmdrake:
  o use same updates enumeration as MandrivaUpdate here
  o stop selecting updates by default in rpmdrake

* Wed Feb 28 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.34-1mdv2007.1
+ Revision: 130190
- fix encoding in rpm summaries' translations
- add requires on mdv-rpm-summary

* Wed Feb 28 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.33-1mdv2007.1
+ Revision: 128546
- fix searching in description (#28943)

* Wed Feb 28 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.32-1mdv2007.1
+ Revision: 127317
- MandrivaUpdate:
  o don't ignore /etc/urpmi/skip.list (#28390)
  o don't select kernel*-latest by default
  o fix not listing all updates (#20294)
  o fix upgrading biarch machines (#15906, #27698)

* Wed Feb 28 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.31-1mdv2007.1
+ Revision: 126999
- fix unrefreshed dialogs while reading the package database or
  installing/removing packages (#15408)
- bump require on drakxtools for #15408 fix

* Tue Feb 27 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.30-1mdv2007.1
+ Revision: 126601
- fix crash after (un)installing package (#28896)

* Mon Feb 26 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.29-1mdv2007.1
+ Revision: 125829
- edit_urpm_sources.pm: make "edit" button insensitive if no selection
- rpmdrake: don't preselect anymore the updates when not started as
  MandrivaUpdate (#27500)
- rpmdrake, MandrivaUpdate:
  o --merge-all-rpmnew option: use Gtk2::SourceView in order to
    source highlight file contents and patches
  o display translated summaries if availlable

* Thu Feb 22 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.28-1mdv2007.1
+ Revision: 124472
- updated tarball in order to fix an install issue
- use standard macro, kill useless make variables
- more refactoring
- display again the full usage on --help
- rpmdrake:
  o do not fork edit-urpm-sources.pl in background
  o reload the package db after editing sources (#27483)
  o rename "apply" button as "update"
- edit-urpm-sources.pl
  o make "remove" button insensitive if no selection
  o remove question mark from column headers
- enable --merge-all-rpmnew in MandrivaUpdate
- move install stuff from spec file into Makefile

* Wed Feb 21 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.27-1mdv2007.1
+ Revision: 124047
- fix being unable to install packages when started as rpmdrake-remove
  (#26364)
- fix crash introduce in 3.26 when started as rpmdrake-remove
- fix crash if there's no source (#28846)

* Wed Feb 21 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.26-1mdv2007.1
+ Revision: 123821
- edit-urpm-sources:
  o have better sub dialogs behaviour (WM hints)
- rpmdrake:
  o add some transient & modal hints
  o fix "cannot see uninstalled packages" bug (#25991)
  o fix crash when performing a search while loading the package list (#27577)
  o fix a bug in listing updates
  o handle singular/plural (#27533)
  o refactoring
- MandrivaUpdate:
  o faster startup
  o new simplified interface
- install new modules
- bump require on perl-URPM for faster db traversing
- bump require on urpmi for encoding fixes
- bump require on drakxtools for plural handling

* Mon Dec 04 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.25-1mdv2007.1
+ Revision: 90411
- edit-urpm-sources.pl: keys managment:
  o better HIG button label
  o better looking (key column now wraps)
- rpmdrake:
  o don't try to show .rpmnew differences for
    /etc/sysconfig/harddrake2/previous_hw (#27426)
  o first attempt of displaying a (for now nonlinear) progress bar (#20494)
  o only show description for real updates, not also for packages with
    the same base name

* Fri Dec 01 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.24-1mdv2007.1
+ Revision: 89812
- fix explaining why package isn't selectable
- when displaying upgrade information, don't display the filename in
  title but just the package name

* Thu Nov 30 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.23-1mdv2007.1
+ Revision: 89404
- rpmdrake:
  o add missing transient hint when updating a media
  o basic port from ugtk2 upon mygtk2
  o don't ellipsize lost of packages since we have a scrolled window
  o dynamically switch the selection label
  o explain why packages are removed
  o handle spurious Gtk+ signals (#27381)
  o really fix not able to select only one update (#26135)
  o show the main window way earlier for faster startup experience
  o update information:
    * better formatting of update data
    * better title for update data
    * better title for README.urpmi dialog
    * better labels
- edit-urpm-sources.pl:
  o fix bad looking error messages (#26971)
- bump require on drakxtools due to API changes

* Mon Nov 27 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.22-1mdv2007.1
+ Revision: 87638
- APIs:
  o edit-urpm-sources.pl, MandrivaUpdate: further adapt to new urpmi APIs
  o use more modern API (MDV::Packdrakeng instead of packdrake)
- edit-urpm-sources.pl: when canceling removal of a medium, don't
  reset the selection
- rpmdrake:
  o add a line between description and file list expander (#27022)
  o allow using regexp in searches (Vincent Panel, #27198)
  o don't crash on UTF-8 issues (#26099)
  o fix displaying list of removed packages
  o lock rpm & urpmi DB whenever needed
  o optimize --pkg-sel
  o reload urpmi db if removing some packages
  o restore --help output
  o when reseting the selection, refresh the package list instead of
    clearing it (#26796)
- MandrivaUpdate:
  o add a "select all" button (reall "toggle") (#25271)
  o default to "all updates" rather than "security updates" in
    MandrivaUpdate mode
  o fix not able to select only one update (#26135)
  o preselect updates by default (#25271)
  o really show all security, bugfix & normal updates in "all updates"
    mode (#27268)

* Sat Nov 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.21-2mdv2007.1
+ Revision: 87152
- bump require on urpmi for API changes

* Fri Nov 24 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.21-1mdv2007.1
+ Revision: 87128
- further adapt to new urpmi APIs
- fix transieness/modality for "more info" dialogs
- if nothing got installed (eg: because some packages are missing),
  do not bother reread the whole hdlists
- really show all security, bugfix & normal updates in "all updates"
  mode (#27268)
- use more modern API (MDV::Packdrakeng instead of packdrake)

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.20-1mdv2007.1
+ Revision: 86716
- edit-urpm-sources.pl: use new lock API for locking the urpmi
  database while running
- rpmdrake: fix signature error dialog not being modal
- require a new urpmi for new APIs

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.19-1mdv2007.1
+ Revision: 86672
- new release (adapt to new urpm)

* Mon Nov 13 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.18-1mdv2007.1
+ Revision: 83785
- regenerated with correct permissions
- fix messed up reasons for removal (#25130)
- fix forever all encoding issues of urpmi (#18629, #25130)
- really fix crash by behaving like urpmi & gurpmi (#26742)

* Sat Oct 28 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.17-1mdv2007.1
+ Revision: 73578
- add support of hdlists for update media (#26788)
 better confirmation string when only removing packages (#26789)

* Fri Oct 27 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.16-1mdv2007.1
+ Revision: 72989
- enable "File/_Update media" whatever is the starting mode
- fix not installing packages when invoked as -remove (#26364)
- if one package cannot be removed, do not alter "selected" status for
  other packages in the loop
- fix uninstalling the last package deselected for removal when
  installing others packages (#26108)
- "/_File/_Reset the selection" menu item:
  o fix displaying again the three after clicking on it
  o behave faster after clicking on it
- requires desktop-common-data for icons

* Thu Oct 26 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.15-1mdv2007.1
+ Revision: 72903
- rpmdrake: fix crash by behaving like urpmi & gurpmi (#26742)
- park-rpmdrake:
  o center dialogs on parent windows
  o set some sensitive dialog titles

* Thu Oct 26 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.14-1mdv2007.1
+ Revision: 72752
- do not show "importance" & "reason for update" fields for non update
  packages when there's an(other package) update for it
- if we cannot create a temp directory, just don't display any data
  rather than exiting

* Wed Oct 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.13-1mdv2007.1
+ Revision: 72480
- check if any sensitive mount point is mounted read-only (#12967)
- fix inverted status icon (#26743)
- fix mis encoded strings returned by urpmi on download errors (#25130)
- show nice icons in "mandriva choice" mode

* Sun Oct 22 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.12-1mdv2007.1
+ Revision: 71619
- enable to see all updates too when not started as MandrivaUpdate
- fix empty list after updating media from "File" menu (#26290)
- if /etc/urpmi/urpmi.cfg doesn't exists, prevent urpmi to kill
  rpmdrake, create an empty config file and run edit-urpm-sources
  instead (#26533)
- show non installed updates in "non installed" list too (#26656)
- Import rpmdrake

* Wed Sep 27 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.11-1mdv2007.0
- fix icon state on unselecting (#26126)
- in "all updates" mode, list again packages without an importance
  field (aka those coming from non update media) (#25267)

* Wed Sep 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.10-1mdv2007.0
- new icons
- fix unselecting an update
- fix displayed status for selected updates (#25964)
- merge-all-rpmnew option:
  o center main window
  o display a wait message
  o do not silently do nothing when there's no changes but show it to
    the user and enable him to delete bogus .rpmnew files (#22744)
  o fix it (#24930)
  o increase default width

* Wed Sep 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.9-1mdv2007.0
- rpmdrake:
  o fix crash
  o force displaying of group on mode switching (#25955)

* Wed Sep 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.8-1mdv2007.0
- for official releases, use new mirror API to ask for only update or
  distrib media
- keep internal state untranslated (#25774)
- prevent blank screen after reloading db from menu
- MandrivaUpdate:
  o fix crash
  o fix listing updates
  o offer to add an update media in on startup if needed (#25708)

* Tue Sep 19 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.7-1mdv2007.0
- edit-urpm-sources: fix canceling "Add"
- rpmdrake:
  o fix crash when searching after clicking "Clear" button (#25926)
  o fix only listing first line of changelog/files list (#25925)

* Tue Sep 19 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.6-1mdv2007.0
- display a link on security advisory
- fix looping on resizing (side effect of #25533's fix)
- prevent dummy "unable to remove package" error dialog (#25680)
- really reload the package list after installing some packages (#25910)

* Mon Sep 18 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.5-1mdv2007.0
- do not needlessly reread urpmi database when canceling
  (un)installation (#25673)
- do not reload the urpmi db when switching list mode
- further speedup mode switching (50%% less time)
- fix bogus portuguese tranlation of a menu item
- fix lost selection on mode switch (#25248)
- fix displaying update data for updates
- fix encoding when querying rpm (#25670, #25716)
- fix listing not all updates (aka only security, bugfixes or normal updates)
- fix title (#25666)
- fix unselecting packages to remove (#25653)
- make "files" and "changelog" embedded widgets be properly sized (#25533)
- scroll textview to its top when selecting a new package
- when launched in remove mode, default to this mode (#25551)

* Sun Sep 17 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.4-1mdv2007.0
- center "Please wait, reading packages database..." dialog on main
  window
- edit-urpm-sources:
  o center some dialogs on main window
  o don't display oversmall error dialogs
  o use new mirror API (#25400)
- fix crash on "Reload the _packages list" in "File" menu (#25652)
- fix double "About About rpmdrake" (#25667)

* Thu Sep 14 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.3-1mdv2007.0
- ask confirmation for packages to be installed too (#25451, #25548)
- better formating: one package per line (#16079)
- fix dialogs not centered on parent window
- fix extracting info for installed packages
- fix uninstalling several packages (#25027)
- prevent some not good looking horizontal scrollbars

* Tue Sep 12 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.2-1mdv2007.0
- add a menu entry for superuser mode (#25302)
- rpmdrake: 
  o display changelog & file list using expanders
  o fix corrupted images after the CVS to SVN switch due to missing
    -kb (#24790)
  o fix crash (#24870)
  o fix dialog title when removing packages (#25046)
  o fix "preparing" message when there's no package to install
    (#25272)
  o misc other fixes
- edit-urpm-sources.pl: HIG
- MandrivaUpdate: fix dying upon startup (#23686)

* Tue Aug 29 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.1.1-1mdv2007.0
- add a "Media Manager" entry
- display a busy cursor when:
  o selecting "Reload the packages list"
  o switching mode
- do not embed wait message on startup
- fix some crashes
- group tree:
  o no more pijama style
  o use smaller icons for subgroups

* Thu Aug 24 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.1-1mdv2007.0
- make GUI working
- many GUI improvements
- somewhat faster startup (more to come...)

* Tue Jul 11 2006 Olivier Blin <oblin@mandriva.com> 3.0-2mdv2007.0
- add 2.27-2mdk changes that weren't in CVS

* Tue Jul 04 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.0-1mdv2007.0
- make some windows transcient
- fix garbaged error messages while accessing mirrors
- edit-urpm-sources:
  o improve layout by using nicer alignment (#17716)
  o improve layout by using a combo box (#17733)
  o let's be more user-friendly by showing one cannot move an item
    when it's the first or the last one
  o prevent some Gtk+ critic warnings
- rpmdrake (WIP):
  o unify all interfaces (#21877)
  o add a "report bug" menu entry (since mcc's menu is hidden)
  o enable one to cancel selecting packages
  o fix encoding of urpmi error

* Fri Mar 17 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.27-2mdk
- Rebuild, require new perl-URPM

* Wed Mar 01 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.27-1mdk
- Add Development/PHP to the rpm group list
- A couple of gurpmi.addmedia bug fixes by Thierry Vignaud
- Fix for mirror and version-guessing heuristic
- Clean cache after downloads
- Update config file when not run as root

* Mon Jan 02 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.26-1mdk
- Add a button to clear the search text field and to redraw the package tree
- Bump requires on drakxtools (for Locale::gettext)

* Fri Dec 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.25-1mdk
- Fix another bug with rpm names containing regex metacharacters
- Use Locale::gettext (Pixel)

* Thu Dec 08 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.24-1mdk
- Support rsync sources (Javier Martínez)
- Require urpmi 4.8.4 for fixes

* Mon Nov 28 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.23-2mdk
- Message updates
- Restore embedding of Software Media Manager in MCC

* Fri Nov 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.23-1mdk
- Display locks before basesystem packages in rpmdrake-remove
- Honor the "prohibit-remove" option

* Wed Nov 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.22-1mdk
- Restore embedding in MCC
- Display README.urpmi only once

* Mon Oct 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.21-1mdk
- Fix sort under some locales (bugs #18617 and #19356)
- Ask the user if one should update unignored invalid media
- Remove context menu in the software media manager
- Make some popups prettier in the software media manager
- Fix busy loop in gtk display (bug #15985)
- Misc. cleanups
- Message updates

* Tue Sep 13 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.20-3mdk
- Avoid double encoding for bad signature message
- Message updates

* Wed Aug 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.20-2mdk
- Message updates
- Install drakrpm-update in /usr/bin also

* Fri Aug 26 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.20-1mdk
- Message updates
- Avoid some forms of utf8 double-encoding

* Fri Aug 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.19-2mdk
- Message updates
- Rename files named mandrake*
- Display sensible wait cursor

* Sat Jul 30 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.19-1mdk
- Add a status bar, remove lots of popup messages
- Fix --pkg-sel= option
- Message updates

* Tue Jul 26 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.18-1mdk
- Make long error windows scrollable
- Translations / strings nits
- Use i18n functions from drakxtools

* Thu Jul 21 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.17-1mdk
- Fix more display bugs

* Wed Jul 20 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.16-2mdk
- Message updates
- Fix display bug 16676

* Tue Jun 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.16-1mdk
- Keep descriptions even when alternate synthesis media
- Always display banners in MCC

* Thu May 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.15-1mdk
- Software media manager: add a column to mark media as update sources,
  and add an "update" checkbox to mark added media as "updates".
- MandrivaUpdate: Always show reason for upgrades even if no media was updated

* Sat May 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.14-1mdk
- Fix rpmdrake in non-update modes

* Fri May 13 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.13-1mdk
- Rework the algorithm to compute upgrades to be more similar to urpmi
- Display architecture in information panel

* Fri Apr 29 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.12-1mdk
- Prompt for proxy credentials if configured so
- Require newest urpmi
- Don't display rsync mirrors if rsync isn't installed
- Recognize the "Limited" distro brand
- Handle virtual media correctly

* Sat Apr 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.11-1mdk
- Rename MandrakeUpdate to MandrivaUpdate

* Thu Mar 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.10-4mdk
- po updates
- make gurpmi.addmedia more robust (bug #15028)

* Mon Mar 21 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.10-3mdk
- Change window title, doesn't include internal version name
- po updates

* Wed Mar 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.10-2mdk
- Install drakrpm-edit-media as a symlink to edit-urpm-sources.pl

* Wed Mar 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.10-1mdk
- Don't install drakrpm-edit-media
- rpmdrake --help works again
- Notes for installed packages are not displayed several times across different
  installs

* Mon Mar 07 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.9-1mdk
- Don't install edit-urpm-media as a copy of edit-urpm-sources.pl anymore
- rpmdrake: restore Quit button, add ctrl-Q as shortcut (Titi)
- add a vertical scrollbar in the software media manager

* Wed Feb 23 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.8-1mdk
- Don't hardcode mirror list url, use /etc/urpmi/mirror.config like
  urpmi.addmedia does

* Mon Feb 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.7-1mdk
- Don't show diffs for rpmnew files that haven't changed
- Make the software media manager cope with variables in media (M. Scherer)

* Fri Feb 11 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.6-1mdk
- Fix utf-8 changelog display in rpmdrake-remove
- Fix view by group

* Thu Feb 10 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.5-5mdk
- Fix crash when displaying changelog

* Wed Feb 09 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.5-4mdk
- Add a new command-line option, --search=pkg, to launch search for "pkg" at
  startup
- Now requires Compress::Zlib, to fix obscure packdrake forking issues
- Language updates, and fix some encoding issues

* Thu Jan 20 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.5-3mdk
- When displaying rpms by medium, display media in the order they appear in
  urpmi.cfg
- Restore view of selected size in rpmdrake
- Remove the view menu (for later)

* Tue Jan 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.5-2mdk
- Quick fix for a crash on some popup windows
- Regenerate po files

* Mon Jan 17 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.5-1mdk
- Software media manager: the "Add..." dialog allows to add updates as well
  as official sources (for Official distros), whereas the "security updates"
  option from the "Add custom..." dialog has been made redundant.
- Language updates
- Fix requires of park-rpmdrake (Pixel)

* Wed Jan 12 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4-5mdk
- rpmdrake now has a menu bar (supported in mcc thanks to Titi)
- Fix crash with new mygtk2 (Titi)
- Move the 'Quit', 'Update media' and 'Help' buttons to it, as well as the
  right-click popup menu.
- Software media manager: requalify the "Add..." button to add the sources for
  the current distribution, and rename the old "Add..." button to "Add
  custom...". (The implementation is not complete yet)

* Fri Jan 07 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4-4mdk
- New command-line option --no-media-update to Mandrakeupdate, to avoid
  updating media at startup
- A few optimisations
- Fix the display of the number of RPMs to be retrieved in rpmdrake

* Fri Dec 17 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4-3mdk
- Add the ability to reorder the media in the software media manager

* Wed Dec 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4-2mdk
- Remove dependency on gurpmi
- Only load packdrake when needed
- Translation updates

* Thu Dec 02 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4-1mdk
- Software media manager:
  - New option setting window, for the downloader and verify-rpm options.
  - Possibility to add all media for a distribution at once (like
    urpmi.addmedia --distrib)
- Add a cancel button in the download progress window
- Don't show the help button in rpmdrake when embedded in the mcc

* Thu Nov 25 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.3-1mdk
- edit-urpm-sources: setting per-media proxies should now work.
- Fix save and restore of package tree display mode in rpmdrake.
- Take into account limit-rate, compress and resume options from urpmi.cfg.

* Thu Nov 18 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.2-4mdk
- edit-urpm-sources: When modifying a media has failed, restore it (don't die,
  and don't keep it in the intermediate state of being ignored)

* Tue Nov 16 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.2-3mdk
- Fix adding an update media in the software media manager.
- Fix sort by country in the mirror list.

* Mon Nov 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.2-2mdk
- Rebuild for new perl

* Tue Nov 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.2-1mdk
- Make the changelog-first option configurable in ~/.rpmdrake (cf bug 11888)
- Less unnecessary package tree rebuilding
- Can search packages whose names contain a '+'
- Allow branding via an OEM file

* Wed Oct 06 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-13mdk
- Language updates
- Adaptation to the new update mirror architecture

* Fri Oct 01 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-12mdk
- Presentation and translation nits
- Upgrade dependencies

* Fri Sep 24 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-11mdk
- The "Update media" button wasn't active when it should

* Thu Sep 23 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-10mdk
- fix parsing of scanssh output in park-rpmdrake (Pixel)

* Wed Sep 22 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-9mdk
- Display the path of the README.urpmi file
- Language updates
- Change menu entry to 'Mandrakelinux Update'

* Wed Sep 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-8mdk
- Language updates
- Disable the "update media" button in removal mode

* Fri Sep 10 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-7mdk
- Language updates
- Change menu entry to 'Mandrakeupdate'

* Thu Sep 02 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-6mdk
- Fix position of "quit" button (Titi)
- Fix display of localized dates in the changelog (Pablo)

* Tue Aug 31 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-5mdk
- Small cleanups in GUI

* Wed Aug 25 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-4mdk
- Add an "update media" button

* Tue Aug 24 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-3mdk
- fix some error popups too large
- fix a crash when trying to remove base packages
- fix download bars for packages (displayed wrong info) and for hdlists (wasn't
  properly updated)
- button reordering
- message updates

* Fri Aug 20 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-2mdk
- Message updates
- Don't ask for selections in browse mode (read-only)
- Reenable selection of all packages

* Thu Aug 19 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.5-1mdk
- Add a checkbox "Show automatically selected packages"

* Wed Aug 18 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.4-2mdk
- Message updates
- Fix a bug on display of fatal errors

* Thu Aug 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.4-1mdk
- rpmdrake uses localized dates in changelog
- edit-urpm-sources.pl requires confirmation when removing media
  (Fabrice Facorat)
- Update messages

* Thu Aug 05 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-14mdk
- Update messages
- Fix some utf-8 handling in error messages
- Fix display of rpmdrake's help
- Refuse to select more than 2000 packages at once

* Thu Jul 29 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-13mdk
- Recognize README.update.urpmi, in addition to README.upgrade.urpmi
- Update requires.
- Allow selection of subtrees, except when the whole tree would be selected.

* Wed Jul 21 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-12mdk
- Display fixes
- Message updates
- Prevent to select an entire subtree by mistake. (work around for bug #9941)

* Fri Jul 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-11mdk
- After installation or upgrade of an rpm, display the contents of a file
  README{,.install,.upgrade}.urpmi
- Presentation nits

* Thu Jul 08 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-10mdk
- Rebuild and fix for new perl

* Tue Jul 06 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-9mdk
- MandrakeUpdate: list packages even when not found in the description file
- Software media manager: allow to set a proxy for only one media

* Thu Jul 01 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-8mdk
- Don't display the "update media" button when not used as root
- use urpm::download
- rebuild for new curl

* Thu Jun 24 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-7mdk
- Message changes and interface cosmetics
- Software media manager: only update explicitly selected sources
- rpmdrake: checks whether the update media added by the installer corresponds
  to the current MDK release

* Tue May 25 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-6mdk
- Message changes
- Replace deprecated OptionMenu widget by ComboBox

* Wed May 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-5mdk
- Avoid selecting all packages when choosing a view sorted by update
  availability
- Remove spurious error messages in the Software Media Manager

* Wed May 05 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-4mdk
- Make the package list pane resizable (Robert Vojta) (#8925)

* Tue May 04 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-3mdk
- Fix reset of the wait cursor when run embedded in drakconf

* Wed Apr 28 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-2mdk
- Language updates

* Tue Apr 27 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1.3-1mdk
- MandrakeUpdate: didn't notify the user when it failed to retrieve
  the hdlist or synthesis file from a mirror. As a consequence no
  update was ever appearing.

