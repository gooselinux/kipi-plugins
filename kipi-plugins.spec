# Fedora review: http://bugzilla.redhat.com/171504

Name:    kipi-plugins
Summary: Plugins to use with Kipi
Version: 0.8.0
Release: 5%{?dist}

License: GPLv2+
Group:   Applications/Multimedia
Url:	 http://www.kipi-plugins.org/
Source0: http://downloads.sourceforge.net/kipi/kipi-plugins-%{version}-patched.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: desktop-file-utils
BuildRequires: exiv2-devel
BuildRequires: gettext
# Until when/if libksane grows a dep on sane-backends-devel
BuildRequires: kdegraphics4-devel sane-backends-devel 
BuildRequires: kdelibs4-devel >= 4.3.4
Requires: kdelibs4 >= 4.3.4
BuildRequires: kdepimlibs-devel
BuildRequires: libgpod-devel >= 0.7.0 
## acquireimages, jpeglossless and rawconverter plugins
BuildRequires: libtiff-devel
## htmlexport plugin 
BuildRequires: libxslt-devel
## RemoveRedeye
BuildRequires: opencv-devel
## Shwup
BuildRequires: qca2-devel

# when -libs split happened
Obsoletes: kipi-plugins < 0.7.0
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

## jpeglossless plugin
Requires: ImageMagick

%description
This package contains plugins to use with Kipi, the KDE Image Plugin
Interface.  Currently implemented plugins are:
AcquireImages      : acquire images using flat scanner
AdvancedSlideshow  : slide images with 2D and 3D effects using OpenGL
Calendar           : create calendars
FlickrExport       : export images to a remote Flickr web service
GalleryExport      : export images to a remote Gallery server
GPSSync            : geolocalize pictures
HTMLExport         : export images collections into a static XHTML page
ImageViewer        : preview images using OpenGL
JpegLossLess       : rotate/flip images without losing quality
KioExportImport    : export/imports pictures to/from accessible via KIO
MetadataEdit       : edit EXIF, IPTC and XMP metadata
PicasaWebExport    : export images to a remote Picasa web service
RemoveRedEyes      : remove red eyes on image automatically
RawConverter       : convert Raw Image to JPEG/PNG/TIFF
SendImages         : send images by e-mail
SimpleViewerExport : export images to Flash using SimpleViewer
ShwupExport        : export images to a remote Shwup web service
SmugExport         : export images to a remote SmugMug web service
FbExport           : export images to a remote Facebook web service
TimeAdjust         : adjust date and time
PrintWizard        : print images in various format

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.


%prep
%setup -q -n %{name}-%{version}-patched


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --all-name --with-kde

## unpackaged files
rm -f %{buildroot}%{_kde4_libdir}/lib*.so


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/kipiplugins.desktop
%ifnarch s390 s390x 
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/scangui.desktop
%endif

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null  ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen  &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor >& /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen >& /dev/null ||:
fi

%posttrans
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor >& /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen >& /dev/null ||:

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%ifnarch s390 s390x
%{_kde4_bindir}/scangui
%{_kde4_libdir}/kde4/kipiplugin_acquireimages.so
%{_kde4_datadir}/applications/kde4/scangui.desktop
%endif
%{_kde4_libdir}/kde4/kipiplugin_advancedslideshow.so
%{_kde4_libdir}/kde4/kipiplugin_batchprocessimages.so
%{_kde4_libdir}/kde4/kipiplugin_calendar.so
%{_kde4_libdir}/kde4/kipiplugin_facebook.so
%{_kde4_libdir}/kde4/kipiplugin_flickrexport.so
%{_kde4_libdir}/kde4/kipiplugin_flashexport.so
%{_kde4_libdir}/kde4/kipiplugin_galleryexport.so
%{_kde4_libdir}/kde4/kipiplugin_gpssync.so
%{_kde4_libdir}/kde4/kipiplugin_htmlexport.so
%{_kde4_libdir}/kde4/kipiplugin_imageviewer.so
%{_kde4_libdir}/kde4/kipiplugin_ipodexport.so
%{_kde4_libdir}/kde4/kipiplugin_jpeglossless.so
%{_kde4_libdir}/kde4/kipiplugin_kioexportimport.so
%{_kde4_libdir}/kde4/kipiplugin_metadataedit.so
%{_kde4_libdir}/kde4/kipiplugin_picasawebexport.so
%{_kde4_libdir}/kde4/kipiplugin_printimages.so
%{_kde4_libdir}/kde4/kipiplugin_rawconverter.so
%{_kde4_libdir}/kde4/kipiplugin_removeredeyes.so
%{_kde4_libdir}/kde4/kipiplugin_sendimages.so
%{_kde4_libdir}/kde4/kipiplugin_shwup.so
%{_kde4_libdir}/kde4/kipiplugin_smug.so
%{_kde4_libdir}/kde4/kipiplugin_timeadjust.so
%{_kde4_appsdir}/kipiplugin_facebook/
%{_kde4_appsdir}/kipiplugin_flashexport/
%{_kde4_appsdir}/kipiplugin_flickrexport/
%{_kde4_appsdir}/kipiplugin_galleryexport/
%{_kde4_appsdir}/kipiplugin_htmlexport/
%{_kde4_appsdir}/kipiplugin_imageviewer/
%{_kde4_appsdir}/kipiplugin_metadataedit/
%{_kde4_appsdir}/kipiplugin_picasawebexport/
%{_kde4_appsdir}/kipiplugin_printimages/
%{_kde4_appsdir}/kipiplugin_removeredeyes/
%{_kde4_appsdir}/kipiplugin_shwup/
%{_kde4_appsdir}/kipiplugin_smug/
%{_kde4_datadir}/applications/kde4/kipiplugins.desktop
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/libkipiplugins.so.1*


%changelog
* Tue Jun 29 2010 Lukas Tinkl <ltinkl@redhat.com> - 0.8.0-5
- Resolves: #608738 - LEGAL: kipi-plugins-0.8.0-4.el6.src.rpm problematic license terms

* Tue May 18 2010 Lukas Tinkl <ltinkl@redhat.com> - 0.8.0-4
- drop broken BRs on libkdcraw-devel, libkipi-devel, libkexiv2-devel

* Tue May 18 2010 Lukas Tinkl <ltinkl@redhat.com> - 0.8.0-3.1
- Resolves: #587901 - dngconverter does not have a menu icon

* Wed Mar 17 2010 Than Ngo <than@redhat.com> - 0.8.0-3
- rebuild against opencv

* Sun Dec 13 2009 Than Ngo <than@redhat.com> - 0.8.0-2
- cleanup

* Mon Nov 02 2009 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-1
- kipi-plugins-0.8.0

* Mon Sep 28 2009 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-1
- kipi-plugins-0.7.0
- -libs pkg, multilib friendly
- use %%find_lang

* Wed Sep 09 2009 Karsten Hopp <karsten@redhat.com> 0.6.0-2
- add endian info for s390, s390x
- kipiplugin_acquireimages.so is not available as kdegraphics is compiled
  without sane support on s390x

* Sat Aug 29 2009 Rex Dieter <rdieter@fedoraproject.org> 0.6.0-1
- kipi-plugins-0.6.0

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.0-1
- kipi-plugins-0.5.0

* Fri Jul 03 2009 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- kipi-plugins-0.4.0

* Fri May 22 2009 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- optimize scriptlets

* Tue May 12 2009 Lukáš Tinkl <ltinkl@redhat.com> - 0.3.0-1
- latest upstream bugfix release 0.3.0, many fixes 
  (cf http://www.digikam.org/drupal/node/449)

* Tue Mar 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-2
- BR: opencv-devel, include RemoveRedEye plugin 

* Tue Mar 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-1
- kipi-plugins-0.2.0 (final)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.18.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.17.rc2
- qt45 patch
- libgpod06 patch f-10 only

* Fri Feb 20 2009 Todd Zullinger <tmz@pobox.com> - 0.2.0-0.16.rc2
- Revert upstream patch requiring libgpod-0.7.0

* Sat Feb 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.15.rc2
- kipi-plugins-0.2.0-rc2

* Thu Feb 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.14.rc1
- BR: kdelibs4-devel >= 4.2.0

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.13.rc1
- kipi-plugins-0.2.0-rc1

* Wed Jan 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.12.beta6
- update %%description
- License: +Adobe (DNGConverter)

* Mon Jan 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.11.beta6
- kipi-plugins-0.2.0-beta6

* Mon Dec 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.10.beta5
- tighten BR's (libkipi >= 0.3.0 mostly)

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.9.beta5 
- respin (exiv2)

* Mon Dec 15 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-0.8.beta5
- kipi-plugins-0.2.0-beta5
- %%description: reorder (alphabetic), simplify

* Thu Dec 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.2.0-0.7.beta4
- rebuild for fixed kde-filesystem (macros.kde4) (get rid of rpaths)

* Tue Nov 25 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-0.6.beta4
- kipi-plugins-0.2.0-beta4

* Tue Nov 25 2008 Lukáš Tinkl <ltinkl@redhat.com> 0.2.0-0.5.beta3
- #472874 - kipi-plugins package is missing kipiplugin.desktop

* Mon Oct 27 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-0.4.beta3
- kipi-plugins-0.2.0-beta3

* Mon Oct 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.2.0-0.3.beta2
- update to 0.2.0 beta 2
- build against latest kdegraphics
- don't require dcraw, libkdcraw includes its own RAW decoding code

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-0.2.beta1
- respin (against newer kdegraphics)

* Thu Sep 04 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-0.1.beta1
- kipi-plugins-0.2.0-beta1, kde4

* Wed Jun 25 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.6-0.2.beta1
- respin for exiv2

* Mon May 26 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.6-0.1.beta1
- kipi-plugins-0.1.6-beta1

* Tue May 20 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.5-3
- don't BR: kdepim3-devel on F-10+

* Thu May 08 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.5-2
- respin

* Fri Mar 14 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.5-1
- kipi-plugins-0.1.5

* Thu Feb 21 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.5-0.6.rc2
- libXrandr patch

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.5-0.5.rc2
- Autorebuild for GCC 4.3

* Sat Feb 02 2008 Rex Dieter <rdieter@fedoraproject.org> 0.1.5-0.4.rc2
- kipi-plugins-0.1.5-rc2

* Sun Dec 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.5-0.3.rc1
- kipi-plugins-0.1.5-rc1

* Sat Dec 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.5-0.2.beta1
- BR: kdelibs3-devel 

* Wed Nov 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.5-0.1.beta1
- kipi-plugins-0.1.5-beta1
- cleanup %%description

* Wed Nov 21 2007 Todd Zullinger <tmz@pobox.com> 0.1.4-5
- rebuild against libgpod-0.6.0

* Wed Sep 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-4
- rebuild against libkdcraw libkexiv2

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-3
- License: GPLv2+

* Tue Aug 21 2007 Todd Zullinger <tmz@pobox.com> 0.1.4-2
- rebuild against libgpod-0.5.2

* Mon Jul 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-1
- kipi-plugins-0.1.4(final)

* Wed Jun 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-0.5.beta3
- LIB_KIO.patch

* Wed Jun 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-0.4.beta2
- --disable-final

* Tue Jun 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-0.3.beta2
- BR: libkdcraw-devel >= 0.1.1

* Tue Jun 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-0.2.beta2
- kipi-plugins-0.1.4-beta2

* Tue Jun 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.4-0.1.beta1
- kipi-plugins-0.1.4-beta1

* Mon May 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.3-5
- respin against libkexiv2-0.1.5

* Tue May 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.3-4
- --with-libgpod (with patch)

* Mon Apr 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.3-3
- respin against exiv2-0.14

* Wed Jan 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.3-2
- drop --with-libgpod, still busted

* Wed Jan 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.3-1
- kipi-plugins-0.1.3
- --with-libgpod 

* Wed Dec 27 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1.3-0.2.rc1
- kipi-plugins-0.1.3-rc1

* Mon Dec 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.3-0.1.beta1
- kipi-plugins-0.1.3-beta1

* Wed Oct 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.2-2
- rebuild against new(er) imlib2

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.2-1
- kipi-plugins-0.1.2

* Thu Jun 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.1-1
- kipi-plugins-0.1.1

* Sun Jun 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-1
- kipi-plugins-0.1.0 (final)

* Fri Jun 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.11
- 0.1.0 (final rc candidate)

* Wed May 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.10.rc2
- --with-opengl, BR: libGLU-devel
  to ensure build/inclusion of slideshow plugin (#193676)

* Wed May 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.9.rc2
- Requires(hint): dcraw

* Mon May 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.8.rc2
- 0.1.0-rc2
- BR: ImageMagick-c++-devel, libtiff-devel, libxslt-devel

* Tue Apr 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.7.rc1
- fc5: drop gphoto2 workaround (#183262)
- cleanup filelist

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.6.rc1
- BR: libGL-devel
- fc5: gcc/glibc respin
- fc5: workaround gphoto2 bug (#183367)

* Thu Nov 10 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.5.rc1
- fix symlinks
- simplify configure

* Fri Nov 04 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.4.rc1
- drop redundant %%doc
- simplify BR's

* Sun Oct 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.3.rc1
- drop BR: libacl-devel
- drop reference(s) to external repos (legalities)

* Sat Oct 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-0.2.rc1
- BR: libacl-devel (at least until kdelibs bug #170602 is fixed)
- drop all optional Req's, mention in %%description
- Release < 1, since it's not final
- %%description: format < 80 columns
- drop goofy install-strip conditional

* Mon Sep 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.1.0-1.rc1
- 0.1.0-rc1

* Tue Feb 08 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.1-0.fdr.0.4.beta2
- 0.1.0-beta2

* Mon Jan 03 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.1-0.fdr.0.3.beta1
- rawconverter: Req: dcraw
- Req: mjpegtools
- Req: ImageMagick 

* Mon Dec 21 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.1-0.fdr.0.2.beta1
- rebuild against libkexif-0.2

* Mon Oct 25 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1-0.fdr.0.1.beta1
- Initial RPM release.
