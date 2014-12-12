%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Summary: A graphical interface for configuring kernel crash dumping
Name: system-config-kdump
Version: 2.0.5
Release: 15%{?dist}%{?ns_dist}.06
URL: http://fedorahosted.org/system-config-kdump/
License: GPLv2+
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source0: http://fedorahosted.org/released/system-config-kdump/%{name}-%{version}-rhel6.tar.bz2
BuildRequires: desktop-file-utils
BuildRequires: intltool, gettext, gnome-doc-utils, docbook-dtds, rarian-compat, scrollkeeper
Requires: pygtk2 >= 2.8.6
Requires: pygtk2-libglade
Requires: usermode >= 1.36
Requires: kexec-tools
Requires: yelp
Requires: python-slip-dbus
Requires(pre): gtk2 >= 2.8.20
Requires(pre): hicolor-icon-theme

# 626787
Patch1: 0001-Hint-message-where-the-dump-file-will-be-copied.patch
Patch3: 0003-Remove-filechooser-button.patch

# 642751
Patch2: 0002-Check-the-core_collector-in-kdump.conf.patch

# 740155
Patch4: 0004-Change-window-type-from-error-message-to-info-messag.patch

# 754059
Patch5: 0005-Correctly-set-nfs-target.patch
Patch12: 0011-Consider-all-changes-when-clicking-apply.patch

# 653450
Patch6: 0006-Fix-some-typos.patch

# 676777
Patch7: 0007-Handle-Extended-crashkernel-syntax.patch
Patch8: 0008-another-patch-for-extended-syntax.patch

# 632999
Patch9: 0009-Regenerated-pot-file-and-po-file-for-translations.patch

# 796308
Patch10: system-config-kdump-2.0.5-s390x.patch

# 622870
Patch11: 0010-Show-error-message-when-D-Bus-isn-t-running.patch

# 816009, threshold for auto lowered
Patch13: 0001-Update-thresh-values-for-auto-2GB-on-x86-4GB-on-ppc-.patch

# 813337, manage zipl.conf
Patch14: 0001-Learn-backend-about-zipl-for-s390x.patch
Patch15: 0002-Call-zipl-binary-when-configuring-zipl.patch

# 740155, Change failed to unable
Patch16: system-config-kdump-2.0.5-change_failed.patch

# 821410, Fixed typo
Patch17: system-config-kdump-2.0.5-typo.patch
Patch18: system-config-kdump-2.0.5-typo2.patch

# 819814, translations
Patch19: system-config-kdump-2.0.5-translations1.patch
Patch20: system-config-kdump-2.0.5-translations2.patch

# 811104, zipl on s390x stores full kernel path and not relative
Patch21: system-config-kdump-2.0.5-s390x_kernel_path.patch

# 829386, Use last value and don't traceback on auto value
Patch22: system-config-kdump-2.0.5-multiple_values.patch

# 852766, firmware assisted dump
Patch23: system-config-kdump-2.0.5-fadump.patch

# 858280, timeout on dbus calls
# and don't (re)start service when setting auto option
Patch24: system-config-kdump-2.0.5-timeout.patch

#neokylin add begin
Patch50: system-config-kdump-2.0.5-neokylin-pathEntry.patch
Patch51: system-config-kdump-nfstips.patch
Patch52: system-config-kdump-warning.patch
Patch53: system-config-kdump-2.0.5-neokylin-zh_CN.po
Patch54: system-config-kdump-2.0.5-neokylin-bug31165.patch
Patch55: system-config-kdump-2.0.5-neokylin-bug30123.patch
Patch56: system-config-kdump-2.0.5-neokylin-bug31754.patch
Patch57: system-config-kdump-2.0.5-neokylin-bug34861.patch
Patch58: system-config-kdump-2.0.5-neokylin-bug34870.patch
Patch59: system-config-kdump-2.0.5-neokylin-bug35588.patch
#neokylin end

%description
system-config-kdump is a graphical tool for configuring kernel crash
dumping via kdump and kexec.

%prep
%setup -q
%patch1 -p1 -b .0001
%patch2 -p1 -b .0002
%patch3 -p1 -b .0003
%patch4 -p1 -b .0004
%patch5 -p1 -b .0005
%patch6 -p1 -b .0006
%patch7 -p1 -b .0007
%patch8 -p1 -b .0008
%patch9 -p1 -b .0009
%patch10 -p1 -b .s390x
%patch11 -p1 -b .0010
%patch12 -p1 -b .0012
%patch13 -p1 -b .threshold
%patch14 -p1 -b .zipl_conf
%patch15 -p1 -b .zipl_call
%patch16 -p1 -b .change_failed
%patch17 -p1 -b .typo
%patch18 -p1 -b .typo2
%patch19 -p1 -b .translations1
%patch20 -p1 -b .translations2
%patch21 -p1 -b .s390x_kernel_path
%patch22 -p1 -b .multiple_values
%patch23 -p1 -b .fadump
%patch24 -p1 -b .timeout

%patch50 -p1
#%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
 
%build
make

%install
rm -rf $RPM_BUILD_ROOT
make INSTROOT=$RPM_BUILD_ROOT install
desktop-file-install --vendor system --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --remove-category Application                             \
  --remove-category SystemSetup                             \
  --remove-category GTK                                     \
  --add-category Settings                                   \
  $RPM_BUILD_ROOT%{_datadir}/applications/system-config-kdump.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
%{_bindir}/scrollkeeper-update -q || :


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
%{_bindir}/scrollkeeper-update -q || :



%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/system-config-kdump
%{_datadir}/system-config-kdump
%{_datadir}/applications/*
%{python_sitelib}/*egg*
%{python_sitelib}/sckdump/

%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-kdump
%config(noreplace) %{_sysconfdir}/pam.d/system-config-kdump

%{_sysconfdir}/dbus-1/system.d/org.fedoraproject.systemconfig.kdump.mechanism.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.systemconfig.kdump.mechanism.service
%{_datadir}/polkit-1/actions/org.fedoraproject.systemconfig.kdump.policy

%{_datadir}/icons/hicolor/48x48/apps/system-config-kdump.png

%doc ChangeLog COPYING
%doc %{_datadir}/gnome/help/system-config-kdump
%doc %{_datadir}/omf/system-config-kdump

%changelog
* Thu May 09 2014 Zhang Hao <hao.zhang@cs2c.com.cn> -2.0.5-16.ns6.06
- Patch57: Resolve bz#34861 get wrong vmlinuz patch
- Patch58: Resolve bz#34870
- Patch59: Resolve bz#35588 do not load crashkernel config

* Wed Jul 03 2013 Zhang Hao <hao.zhang@cs2c.com.cn> -2.0.5-15.ns6.04
- Remove patch51
- Resolve bz#30123

* Tue Apr 02 2013 Zhang Hao <hao.zhang@cs2c.com.cn> - 2.0.5-15.ns6.01
- check host name of nfs
- can't change the directiory of nfs
- remove the warning while start
 
* Thu Sep 20 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-15
- Set timout for dbus calls to 5 minutes
- Don't (re)start service when setting auto option
  Resolves: #858280

* Wed Sep 12 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-14
- support firmware assisted dump
  Resolves: #852766

* Wed Aug 22 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-13
- Use last value when multiple values are mentioned
- Don't traceback when value is auto
  Resolves: #829386

* Wed Aug 22 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-12
- zipl on s390x machines stores full path of kernel
  Resolves: #811104.patch

* Tue May 29 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-11
- Translations
  Resolves: #819814

* Wed May 16 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-10
- Fix for #821410 wasn't complete. Now it is.
  Resolves: #821410

* Wed May 16 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-9
- I didn't apply the previous patch, so applying now
  Resolves: #821410

* Wed May 16 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-8
- Fixed typo
  Resolves: #821410

* Mon May 14 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-7
- Change `Failed' to `Unable'
  Resolves: #740155

* Wed May 02 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-6
- Configure zipl.conf and properly call zipl on s390x
  Resolves: #813337

* Mon Apr 30 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-5
- Lower threshold for auto option
  Resolves: #816009

* Fri Mar 16 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-4
- Show proper error message when D-Bus isn't running
- Consider-all-changes-when-clicking-apply
  Resolves: #622870, #754059

* Fri Feb 24 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-3
- Enable on s390x
  Resolves: #796308

* Tue Feb 14 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-2
- Support for extended crash kernel syntax
- Don't show misleading filechooser
- Correctly set nfs target
- Change window type from error message to info message
- Check the core_collector in kdump.conf
- Fix some typos
- Pot files update
  Resolves: #676777, #626787, #754059, #740155, #642751, #653450, #629483,
  Resolves: #632999

* Thu Feb 09 2012 Roman Rakus <rrakus@redhat.com> - 2.0.5-1
- Rebase to 2.0.5
  Resolves: #622870, #609487, #590057

* Tue Aug 10 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.2-2
- Add fallback to get total mem from /proc/meminfo
  Resolves: #622868

* Tue Aug 10 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.2-1
- Bump to 2.0.2.2
- New traslations
  Resolves: #610471

* Wed Jun 30 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-19
- Added poweroff default action
- Added missing check
  Resolves: #603801

* Wed Jun 30 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-18
- Added support for ext4
- check the return code of the service handling
- show error message when cathed dbus exception
  Resolves: #608020

* Mon Jun 07 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-17
- Calculate total memory from /proc/iomem rather than read it
  from /proc/meminfo.
  Resolves: #581422

* Tue May 25 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-16
- Properly deal with unsupported bootloader
  Resolves: #590380

* Tue May 25 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-15
- Make the apply button sensitive if the application makes a change and
  not only if the user make a change
  Resolves: #581433

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-14
- Additional checks for valid crashkernel value
  Resolves: #591019

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-13
- Show the help in the right place in yelp
  Resolves: #588576

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-12
- Added translations
  Resolves: #575679

* Mon Apr 26 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-11
- Added new translations

* Thu Apr 22 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-10
- Use better policy
- Better calculation of total memory on system
  Resolves: #581422

* Thu Apr 15 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-9
- Removed deprecated text
  Resolves: #581446

* Thu Apr 15 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-8
- Do not depend on bitmap-fonts
  Resolves: #581916

* Thu Apr 08 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-7
- Use icon for main window and better name in gnome menu
  Resolves: #567680

* Thu Mar 11 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-6
- Fixed typo
  Resolves: #572219

* Wed Mar 10 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-5
- Use `auto' as default and allow to manually set size
  Resolves: #556866

* Tue Feb 09 2010 Roman Rakus <rrakus@redhat.com> 2.0.2-4
- Get a rid of rhpl
  Resolves: #563143

* Thu Jan 21 2010 Roman Rakus rrakus@redhat.com 2.0.2-3
- Inform user that he doesn't have enough memory for auto crashkernel
- Allow him to set everything but memory for kdump
  Resvoles: #556866

* Wed Jan 20 2010 Roman Rakus <rrakus@redhat.com> 2.0.2-2
- Use only auto value for crashkernel kernel argument
  Resolves: #528714
- Since auto is only valid, don't try to integerize it
  Resolves: #556866

* Mon Dec 07 2009 Roman Rakus <rrakus@redhat.com> - 2.0.2-1
- Don't be interested in non linux entries in bootloaders conf.
  Resolves: #538850

* Fri Oct 02 2009 Roman Rakus <rrakus@redhat.com> - 2.0.1-1
- Update to version 2.0.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Roman Rakus <rrakus@redhat.com> - 2.0.0-2
- Added missing requires python-slip-dbus

* Tue May 05 2009 Roman Rakus <rrakus@redhat.com> - 2.0.0-1
- Changed to satisfy system config tools clenaup

* Mon Apr 13 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0.14-6
- Improve error handling when applying settings

* Mon Mar 23 2009 Roman Rakus <rrakus@redhat.com> - 1.0.14-5
- Fix off by one error in kernel command line parsing
  Resolves #334269

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.14-3
- Rebuild for Python 2.6

* Thu Sep 11 2008 Roman Rakus <rrakus@redhat.com> 1.0.14-2
- Don't specify any offset in cmdline argument
  Resolves: #461602

* Tue Sep 09 2008 Roman Rakus <rrakus@redhat.com> 1.0.14-1
- Bump to version 1.0.14

* Fri Feb 01 2008 Dave Lehman <dlehman@redhat.com> 1.0.13-2%{?dist}
- replace desktop file category "SystemSetup" with "Settings"

* Fri Jan 18 2008 Dave Lehman <dlehman@redhat.com> 1.0.13-1%{?dist}
- handle kdump service start/stop
  Resolves: rhbz#239324
- only suggest reboot if memory reservation altered
  Related: rhbz#239324
- preserve unknown config options
  Resolves: rhbz#253603
- add 'halt' default action
  Related: rhbz#253603

* Tue Oct 23 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-5%{?dist}
- fix license tag again

* Tue Oct 23 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-4%{?dist}
- fix desktop file in spec to avoid patching

* Mon Oct 22 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-3%{?dist}
- fix desktop file categories
- remove redhat-artwork requires

* Fri Oct 19 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-2%{?dist}
- change License to GPL2+

* Tue Sep 11 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-1%{?dist}
- prompt user for a PAE kernel for 32-bit xen with >4G memory (Jarod Wilson)
  Resolves: rhbz#284851

* Wed Aug 29 2007 Dave Lehman <dlehman@redhat.com> 1.0.11-1%{?dist}
- add support for xen (patch from Jarod Wilson)
  Resolves: #243191

* Tue Jan 16 2007 Dave Lehman <dlehman@redhat.com> 1.0.10-1%{?dist}
- handle ia64 bootloader correctly
  Resolves: #220231
- align memory requirements with documented system limits
  Resolves: #228711

* Wed Dec 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-3%{?dist}
- only present ext2 and ext3 as filesystem type choices (#220223)

* Wed Dec 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-2%{?dist}
- make "Edit Location" button translatable (#216596, again)

* Mon Dec 18 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-1%{?dist}
- more translations
- use file: URIs instead of local: (#218878)

* Tue Dec  5 2006 Dave Lehman <dlehman@redhat.com> 1.0.8-1%{?dist}
- more translations (#216596)

* Wed Nov 29 2006 Dave Lehman <dlehman@redhat.com> 1.0.7-1%{?dist}
- rework memory constraints for increased flexibility (#215990)
- improve consistency WRT freezing/thawing of widgets (#215991)
- update translations (#216596)

* Fri Oct 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.6-1%{?dist}
- add ChangeLog and COPYING as docs

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-3%{?dist}
- use %%{_sysconfdir} instead of /etc in specfile

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-2%{?dist}
- remove #!/usr/bin/python from system-config-kdump.py (for rpmlint)

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-1%{?dist}
- fix install make target to specify modes where needed
- remove unnecessary %%preun
- various specfile fixes to appease rpmlint

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.4-2
- fix path to icon in glade file

* Tue Oct 24 2006 Dave Lehman <dlehman@redhat.com> 1.0.4-1
- all location types now in combo box (no text entry for type)
- preserve comment lines from kdump.conf instead of writing config header
- add hicolor icon from Diana Fong

* Thu Oct 19 2006 Dave Lehman <dlehman@redhat.com> 1.0.3-1
- rework UI to only allow one location
- minor spec file cleanup

* Wed Oct 18 2006 Dave Lehman <dlehman@redhat.com> 1.0.2-1
- add support for "core_collector" and "path" handlers
- give choices of "ssh" and "nfs" instead of "net"
- validate results of edit location dialog
- add choice of "none" to default actions
- remove "ifc" support since it's gone from kexec-tools
- update kdump config file header
- fix a couple of strings that weren't getting translated

* Mon Oct 16 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-3
- Fix parsing of "crashkernel=..." string from /proc/cmdline

* Fri Oct 13 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-2
- convert crashkernel values to ints when parsing

* Tue Oct 10 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-1
- Fix bugs in writeDumpConfig and writeBootloaderConfig
- Fix handling of pre-existing "ifc" and "default" directives
- Always leave network interface checkbutton sensitive
- Various minor fixes

* Fri Oct 06 2006 Dave Lehman <dlehman@redhat.com> 1.0.0-1
- Initial build

