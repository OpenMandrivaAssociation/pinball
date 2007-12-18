%define	name	pinball
%define	version	0.3.1
%define	release	%mkrel 9
%define	Summary	Emilia 3d Pinball

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/pinball/%{name}-%{version}.tar.bz2
Source11:	pinball-16x16.png
Source12:	pinball-32x32.png
Source13:	pinball-48x48.png
License:	GPL
Group:		Games/Arcade
URL:		http://pinball.sourceforge.net/
BuildRequires:	mesaglu-devel mesa-common-devel SDL-devel >= 1.2 
Buildrequires:	png-devel SDL_image-devel SDL_mixer-devel oggvorbis-devel smpeg-devel
Buildrequires:	jpeg-devel tiff-devel

%description
The Emilia Pinball projects is an open source pinball simulator for linux
and other unix systems. The current release is a stable and mature alpha.
There is only two levels to play with but it is however very addictive.

%prep
%setup -q

%build
%configure2_5x	--datadir=%{_gamesdatadir} \
		--bindir=%{_gamesbindir} \
		--with-pic \
		--with-gnu-ld
# 0.2.0: parallel make is broken.
make CXXFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std EM_HIGHSCORE_DIR=%{_localstatedir}/games/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Pinball
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# Remove development files untill someone wants them.
rm -rf $RPM_BUILD_ROOT%{_includedir}/%{name} \
    $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a
rm -f  $RPM_BUILD_ROOT%{_gamesbindir}/%{name}-config

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README ChangeLog 
%{_gamesbindir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/*.la
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%dir %{_localstatedir}/games/%{name}
%{_localstatedir}/games/%{name}/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png


