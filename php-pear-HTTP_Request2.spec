%define		_class		HTTP
%define		_subclass	Request2
%define		upstream_name	%{_class}_%{_subclass}

%define		_requires_exceptions pear(PHPUnit

Summary:	Provides an easy way to perform HTTP requests
Name:		php-pear-%{upstream_name}
Version:	2.0.0
Release:	%mkrel 2
License:	BSD
Group:		Development/PHP
URL:		http://pear.php.net/package/HTTP_Request2/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tgz
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHP5 rewrite of HTTP_Request package (with parts of HTTP_Client). Provides
cleaner API and pluggable Adapters:
* Socket adapter, based on old HTTP_Request code,
* Curl adapter, wraps around PHP's cURL extension,
* Mock adapter, to use for testing packages dependent on HTTP_Request2.
Supports POST requests with data and file uploads, basic and digest
authentication, cookies, managing cookies across requests, proxies, gzip and
deflate encodings, redirects, monitoring the request progress with Observers...

%prep

%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
%{_datadir}/pear/data/%{upstream_name}

