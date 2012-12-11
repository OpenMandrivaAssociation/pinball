# pinball actually uses libltdl to load its plugins
%define dont_remove_libtool_files 1

Summary:	Emilia 3d Pinball
Name:		pinball
Version:	0.3.1
Release:	13
Source0:	http://prdownloads.sourceforge.net/pinball/%{name}-%{version}.tar.bz2
Source11:	pinball-16x16.png
Source12:	pinball-32x32.png
Source13:	pinball-48x48.png
Patch0:         pinball-0.3.1-sys-ltdl.patch
Patch1:         pinball-0.3.1-hiscore.patch
Patch2:		pinball-0.3.1-strictproto.patch
Patch3:		pinball-0.3.1-compile.patch
License:	GPL+
Group:		Games/Arcade
URL:		http://pinball.sourceforge.net/
BuildRequires:	mesaglu-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel SDL_mixer-devel
BuildRequires:	libtool-devel

%description
The Emilia Pinball projects is an open source pinball simulator for linux
and other unix systems. The current release is a stable and mature alpha.
There is only two levels to play with but it is however very addictive.

%prep
%setup -q
%patch0 -p1 -b .sys-ltdl~
%patch1 -p1 -b .hiscore~
%patch2 -p0
%patch3 -p1 -b .compile~
rm -fr libltdl
libtoolize --force
aclocal
autoheader
automake -a
autoconf
# cleanup a bit
chmod -x ChangeLog */*.h */*.cpp data/*/Module*.cpp

%build
%configure2_5x	--datadir=%{_gamesdatadir} \
		--bindir=%{_gamesbindir} \
		--with-pic \
		--with-gnu-ld
# 0.2.0: parallel make is broken.
make CXXFLAGS="%{optflags}"

%install
rm -fr %buildroot
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Pinball
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# Remove development files untill someone wants them.
rm -rf $RPM_BUILD_ROOT%{_includedir}/%{name} \
    $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a \
    $RPM_BUILD_ROOT%{_libdir}/%{name}/*.so \
    $RPM_BUILD_ROOT%{_libdir}/%{name}/libModuleTest.*
rm -f  $RPM_BUILD_ROOT%{_gamesbindir}/%{name}-config

# remove unused global higescorefiles:
rm -fr $RPM_BUILD_ROOT%{_localstatedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README ChangeLog 
%{_gamesbindir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/*.la
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png




%changelog
* Mon Jun 08 2009 Funda Wang <fundawang@mandriva.org> 0.3.1-12mdv2010.0
+ Revision: 383818
- sync fedora patch to fix hiscore record problem

* Tue May 19 2009 Jérôme Brenier <incubusss@mandriva.org> 0.3.1-11mdv2010.0
+ Revision: 377416
- fix perm on ChangeLog
- fix license
- trivial fix to the desktop file

* Fri Aug 08 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.3.1-10mdv2009.0
+ Revision: 268985
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.3.1-9mdv2009.0
+ Revision: 140731
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill X-mdv category
    - drop doble menu

* Tue Dec 18 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.3.1-9mdv2008.1
+ Revision: 132313
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Fri Jun 08 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.3.1-9mdv2008.0
+ Revision: 37528
- Rebuild with libslang2.

* Sat May 26 2007 Funda Wang <fundawang@mandriva.org> 0.3.1-8mdv2008.0
+ Revision: 31417
- Rebuild for directfb 1.0


* Wed Feb 28 2007 Lenny Cartier <lenny@mandriva.com> 0.3.1-7mdv2007.0
+ Revision: 127216
- Rebuild for dependencies

* Mon Nov 20 2006 Emmanuel Andry <eandry@mandriva.org> 0.3.1-6mdv2007.1
+ Revision: 85698
- xdg menu
- %%mkrel
  fix buildrequires
- Import pinball

* Thu Feb 17 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.3.1-5mdk
- fix typo in description (from Eskild again;)

* Tue Feb 15 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.3.1-4mdk
- fix description (from Eskild Hustvedt)

* Tue Feb 15 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.3.1-3mdk
- use %%configure macro
- move hiscore file to %%{_localstatedir}/games/%%{name}
- do not bzip2 icons in src.rpm

* Thu Jun 17 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.3.1-2mdk
- rebuild

