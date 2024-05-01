#
# Conditional build:
%bcond_with	goa	# online accounts dialog (deprecated)

%define	translations_version	6.0.2
%define	cinnamon_desktop_ver	4.6.0
%define	csd_ver			4.4.0
%define	cinnamon_menus_ver	4.4.0

Summary:	Utilities to configure the Cinnamon desktop
Summary(pl.UTF-8):	Narzędzia do konfiguracji środowiska Cinnamon
Name:		cinnamon-control-center
Version:	6.0.1
Release:	2
License:	GPL v2+
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/cinnamon-control-center/releases
Source0:	https://github.com/linuxmint/cinnamon-control-center/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ee3379a326a5603c474a5de02a1d42fa
#Source1Download: https://github.com/linuxmint/cinnamon-translations/releases
Source1:	https://github.com/linuxmint/cinnamon-translations/archive/%{translations_version}/cinnamon-translations-%{translations_version}.tar.gz
# Source1-md5:	36552df46587be4e32ac311b8d7084e4
URL:		https://github.com/linuxmint/cinnamon-control-center
BuildRequires:	ModemManager-devel >= 0.7
BuildRequires:	NetworkManager-devel >= 2:1.8.0
BuildRequires:	NetworkManager-gtk-lib-devel >= 1.8.0
BuildRequires:	cinnamon-desktop-devel >= %{cinnamon_desktop_ver}
BuildRequires:	cinnamon-menus-devel >= %{cinnamon_menus_ver}
BuildRequires:	cinnamon-settings-daemon-devel >= %{csd_ver}
BuildRequires:	colord-devel >= 0.1.14
BuildRequires:	fontconfig-devel
BuildRequires:	gdk-pixbuf2-devel >= 2.23.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.44.0
%if %{with goa}
BuildRequires:	gnome-online-accounts-devel >= 3.21.5
BuildRequires:	gnome-online-accounts-devel < 3.50
%endif
BuildRequires:	gtk+3-devel >= 3.16.0
BuildRequires:	iso-codes
BuildRequires:	libgnomekbd-devel >= 3.28
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libnotify-devel >= 0.7.3
BuildRequires:	libwacom-devel >= 0.27
BuildRequires:	libxklavier-devel >= 5.1
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	polkit-devel >= 0.103
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	upower-devel >= 0.99.8
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel >= 1.2
Requires(post,postun):	glib2-devel >= 1:2.44.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	NetworkManager >= 2:1.8.0
# nm-connection-editor for the network panel
Requires:	NetworkManager-applet >= 1.8.0
Requires:	cinnamon-desktop >= %{cinnamon_desktop_ver}
Requires:	cinnamon-menus >= %{cinnamon_menus_ver}
Requires:	cinnamon-settings-daemon >= %{csd_ver}
Requires:	colord >= 0.1.14
Requires:	dbus-x11
Requires:	gdk-pixbuf2 >= 2.23.0
# For the colour panel
Requires:	gnome-color-manager
Requires:	hicolor-icon-theme
Requires:	iso-codes
Requires:	libgnomekbd >= 3.28
Requires:	libgudev >= 232
Requires:	libnotify >= 0.7.3
Requires:	libwacom >= 0.27
Requires:	libxklavier >= 5.1
Requires:	polkit >= 0.103
Requires:	upower >= 0.99.8
Requires:	xorg-lib-libXi >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains configuration utilities for the Cinnamon
desktop, which allow to configure accessibility options, desktop
fonts, keyboard and mouse properties, sound setup, desktop theme and
background, user interface properties, screen resolution, and other
settings.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia konfiguracyjne dla środowiska graficznego
Cinnamon, pozwalające konfigurować opcje dostępności, fonty,
właściwości klawiatury i myszy, dźwięki, motywy pulpitu i tła,
ustawienia interfejsu użytkownika, rozdzielczość ekranu i inne.

%package libs
Summary:	Cinnamon control center shared library
Summary(pl.UTF-8):	Pakiet programistyczny Cinnamon control center
Group:		Libraries
Requires:	glib2 >= 1:2.44.0
Requires:	gtk+3 >= 3.16.0

%description libs
Cinnamon control center shared library.

%description libs -l pl.UTF-8
Pakiet programistyczny Cinnamon control center.

%package devel
Summary:	Development package for Cinnamon control center
Summary(pl.UTF-8):	Pakiet programistyczny Cinnamon control center
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0
Requires:	gtk+3-devel >= 3.16.0

%description devel
Header files for Cinnamon control center.

%description devel -l pl.UTF-8
Pliki nagłówkowe Cinnamon control center.

%prep
%setup -q -a1

%build
%meson build \
	%{!?with_goa:-Donlineaccounts=false}

%ninja_build -C build

%{__make} -C cinnamon-translations-%{translations_version}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

cd cinnamon-translations-%{translations_version}
for f in usr/share/locale/*/LC_MESSAGES/%{name}.mo ; do
	install -D "$f" "$RPM_BUILD_ROOT/$f"
done
cd ..

# not supported by glibc 2.39
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ie,frp,rue}

# cinnamon-control-center (from translations) and cinnamon-control-center-timezones domains
%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README README.md debian/changelog
%attr(755,root,root) %{_bindir}/cinnamon-control-center
%dir %{_libdir}/cinnamon-control-center-1
%dir %{_libdir}/cinnamon-control-center-1/panels
%{_libdir}/cinnamon-control-center-1/panels/libcolor.so
%{_libdir}/cinnamon-control-center-1/panels/libdisplay.so
%{_libdir}/cinnamon-control-center-1/panels/libnetwork.so
%if %{with goa}
%{_libdir}/cinnamon-control-center-1/panels/libonline-accounts.so
%endif
%{_libdir}/cinnamon-control-center-1/panels/libregion.so
%{_libdir}/cinnamon-control-center-1/panels/libwacom-properties.so
%dir %{_datadir}/cinnamon-control-center
%{_datadir}/cinnamon-control-center/panels
%{_datadir}/cinnamon-control-center/ui
%{_datadir}/glib-2.0/schemas/org.cinnamon.control-center.display.gschema.xml
%{_desktopdir}/cinnamon-color-panel.desktop
%{_desktopdir}/cinnamon-display-panel.desktop
%{_desktopdir}/cinnamon-network-panel.desktop
%{_desktopdir}/cinnamon-wacom-panel.desktop
%{_iconsdir}/hicolor/*x*/apps/cinnamon-preferences-*.png
%{_iconsdir}/hicolor/scalable/apps/cinnamon-preferences-*.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcinnamon-control-center.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinnamon-control-center.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcinnamon-control-center.so
%{_includedir}/cinnamon-control-center-1
%{_pkgconfigdir}/libcinnamon-control-center.pc
