#
# spec file for package udjat-branding-upstream
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (C) <2008> <Banco do Brasil S.A.>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# References:
#	https://en.opensuse.org/openSUSE:Packaging_Branding

%define product_name %(pkg-config --variable=product_name libudjat)
%define httproot /srv/www/htdocs/%{product_name}

Summary:		Branding for %{product_name} 
Name:			%{product_name}-branding-upstream
Version:		1.0
Release:		0
License:		LGPL-3.0
Source:			%{name}-%{version}.tar.xz

URL:			https://github.com/PerryWerneck/udjat-branding

Group:			Development/Libraries/C and C++
BuildRoot:		/var/tmp/%{name}-%{version}
BuildArch:		noarch

BuildRequires:  gdk-pixbuf-loader-rsvg
BuildRequires:  gtk3-tools >= 3.24.2

# To make sure the icon theme cache gets generated
Requires(post):	(gtk3-tools if libgtk-3-0)
Requires(post):	(gtk4-tools if libgtk-4-1)

Enhances:		%{product_name}	
Supplements:	packageand(%{product_name}:branding-upstream)
Provides:		%{product_name}-branding = %{version}
Conflicts:		otherproviders(%{product_name}-branding)

BuildRequires:  pkgconfig(libudjat)
BuildRequires:	fdupes
BuildRequires:	sed

# Python scour & pre-reqs
BuildRequires:	python3-setuptools
BuildRequires:	python-xml
BuildRequires:	python-scour
BuildRequires:	python3-css-html-js-minify

%description
Upstream branding for libudjat applications.

%package -n %{product_name}-branding-http-upstream
Summary:		HTTP branding for %{product_name}

Enhances:		%{product_name}-module-http	
Supplements:	packageand(%{product_name}-module-http:branding-upstream)
Provides:		%{product_name}-branding-http = %{version}
Conflicts:		otherproviders(%{product_name}-branding-http)

%description -n %{product_name}-branding-http-upstream
Upstream branding for %{product_name} http server modules.

#---[ Build & Install ]-----------------------------------------------------------------------------------------------

%prep
%setup

%build

%install

mkdir -p %{buildroot}%{_datadir}/icons
mkdir -p %{buildroot}%{_datadir}/icons/%{product_name}
mkdir -p %{buildroot}%{httproot}/icons
mkdir -p %{buildroot}%{httproot}/icons/%{product_name}

mkdir -p "%{buildroot}%{_datadir}/icons/%{product_name}"
install --mode=644 "icons/index.theme" "%{buildroot}%{_datadir}/icons/%{product_name}"

cd icons
for SVG in $(find . -iname *.svg)
do
	mkdir -p $(dirname "%{buildroot}%{httproot}/${SVG}")
	scour -i "${SVG}" -o "%{buildroot}%{httproot}/icons/${SVG}"
	chmod 644 "%{buildroot}%{httproot}/icons/${SVG}"
	mkdir -p $(dirname "%{buildroot}%{_datadir}/icons/%{product_name}/${SVG}")
	install --mode=644 "%{buildroot}%{httproot}/icons/${SVG}" "%{buildroot}%{_datadir}/icons/%{product_name}/${SVG}"
done
cd ..

find %{buildroot}
exit -1

mkdir -p %{buildroot}%{httproot}/images
for SVG in images/*.svg
do
	scour -i "${SVG}" -o "%{buildroot}%{httproot}/images/$(basename ${SVG})"
	chmod 644 "%{buildroot}%{httproot}/images/$(basename ${SVG})"
done
ln %{buildroot}%{httproot}/images/logo.svg %{buildroot}%{httproot}/images/%{product_name}.svg

mkdir -p %{buildroot}%{httproot}/css
for CSS in css/*.css
do
	css-html-js-minify "${CSS}"
	install --mode=644 "css/$(basename --suffix=.css ${CSS}).min.css" "%{buildroot}%{httproot}/${CSS}"
done

mkdir -p %{buildroot}%{_sysconfdir}/%{product_name}.conf.d

install "conf.d/50-branding.conf.in" "%{buildroot}%{_sysconfdir}/%{product_name}.conf.d/50-branding.conf"

sed -i -e \
	"s|@PRODUCT_NAME@|%{product_name}|g" \
	"%{buildroot}%{_sysconfdir}/%{product_name}.conf.d/50-branding.conf"
	
chmod 644 "%{buildroot}%{_sysconfdir}/%{product_name}.conf.d/50-branding.conf"
	
%{icon_theme_cache_create_ghost %{product_name}}	
%fdupes %{buildroot}/%{httproot}
%fdupes %{buildroot}/%{_datadir}
%fdupes %{buildroot}/%{_sysconfdir}

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/%{product_name}.conf.d
%config(noreplace) %{_sysconfdir}/%{product_name}.conf.d/*.conf

%ghost %{_datadir}/icons/%{product_name}/icon-theme.cache

%dir %{_datadir}/*/%{product_name}
%dir %{_datadir}/*/%{product_name}/*

%dir %{_datadir}/icons/%{product_name}/*/*
%{_datadir}/icons/%{product_name}/*/*/*.svg
%{_datadir}/icons/%{product_name}/index.theme

%files -n %{product_name}-branding-http-upstream
%defattr(-,root,root)
%dir %{httproot}
%dir %{httproot}/*
%dir %{httproot}/icons/*
%{httproot}/*/*.css
%{httproot}/*/*/*.svg
%{httproot}/*/*.svg

%changelog

