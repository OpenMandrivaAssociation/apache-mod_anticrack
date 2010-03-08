#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_anticrack
%define mod_conf B21_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_AntiCrack module for Apache 2.x
Name:		apache-%{mod_name}
Version:	0.3
Release:	%mkrel 9
Group:		System/Servers
License:	GPL
URL:		http://www.uglyboxindustries.com/
Source0:	http://www.uglyboxindustries.com/%{mod_name}-%{version}.tar.gz
Source1:	http://www.uglyboxindustries.com/mod_anticrack.html
Source2:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	mysql-devel
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The mod_anticrack module is designed to thwart attempts at cracking into
password protected paths of your web site. The module uses a MySQL server
database to store invalid login attempts from IP addresses. After a cracker
exceeds the configured threshold, they are given 403 HTTP codes no matter what
they enter. This effectively blocks their access and stops the possibility of
them gaining access to your password protected sites.

This modules is best employed in scenarios where you have paying content locked
behind a password protected area, and you are prone to cracking attempts.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} mod_anticrack.html
cp %{SOURCE2} %{mod_conf}

mv ipSearch.php ipsearch.php
dos2unix ipsearch.php mod_anticrack.html

%build

%{_sbindir}/apxs -c -I%{_includedir}/mysql -L%{_libdir} -lmysqlclient mod_anticrack.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc mod_anticrack.html ipsearch.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

