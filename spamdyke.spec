Name:      spamdyke
Summary:   connection-time spam filter for qmail
Version:   4.3.1
Release:   0%{?dist}
License:   GPL (version 2 only)
Group:     System Environment/Libraries
Vendor:    QmailToaster
Packager:  Eric Shubert <qmt-build@datamatters.us>
URL:       http://www.spamdyke.org/
Source0:   http://www.spamdyke.org/releases/%{name}-%{version}.tgz
Source1:   spamdyke.conf
Source2:   blacklist_keywords
Source3:   whitelist_ip
Source4:   sd-prune-graylist
BuildRequires: openssl-devel
BuildRoot: %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define debug_package %{nil}
%define BASE_DIR      /opt/%{name}
%define BIN_DIR       %{BASE_DIR}/bin
%define CONF_DIR      %{BASE_DIR}/etc
%define VAR_DIR       %{BASE_DIR}/var
%define BIN_LINK      %{_bindir}
%define CONF_LINK     %{_sysconfdir}/%{name}
%define VAR_LINK      %{_localstatedir}/%{name}

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
spamdyke is a filter for monitoring and intercepting SMTP connections
between a remote host and a qmail server.
Spam is blocked while the remote server (spammer) is still connected;
no additional processing or storage is needed.

spamdyke also includes a number of features to enhance qmail.

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------
%setup -q

#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------
cd %{name}
./configure
make

#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
%{__rm} -rf  %{buildroot}
%{__mkdir_p} %{buildroot}%{BASE_DIR} \
             %{buildroot}%{BIN_DIR} \
             %{buildroot}%{CONF_DIR} \
             %{buildroot}%{VAR_DIR}/graylist \
             %{buildroot}%{BIN_LINK} \
             %{buildroot}%{_sysconfdir} \
             %{buildroot}%{_localstatedir}
%{__ln_s}  ..%{CONF_DIR}  %{buildroot}%{CONF_LINK}
%{__ln_s}  ..%{VAR_DIR}   %{buildroot}%{VAR_LINK}

touch %{buildroot}%{CONF_DIR}/blacklist_ip \
      %{buildroot}%{CONF_DIR}/blacklist_rdns \
      %{buildroot}%{CONF_DIR}/blacklist_recipients \
      %{buildroot}%{CONF_DIR}/blacklist_senders \
      %{buildroot}%{CONF_DIR}/whitelist_keywords \
      %{buildroot}%{CONF_DIR}/whitelist_rdns \
      %{buildroot}%{CONF_DIR}/whitelist_recipients \
      %{buildroot}%{CONF_DIR}/whitelist_senders

%{__install} -p %{SOURCE1}        %{buildroot}%{CONF_DIR}/.
%{__install} -p %{SOURCE2}        %{buildroot}%{CONF_DIR}/.
%{__install} -p %{SOURCE3}        %{buildroot}%{CONF_DIR}/.

%{__install} -p %{SOURCE4}        %{buildroot}%{BIN_DIR}/.
%{__install} -p %{name}/%{name}   %{buildroot}%{BIN_DIR}/.

%{__ln_s}  ../..%{BIN_DIR}/sd-prune-graylist  %{buildroot}%{BIN_LINK}/.
%{__ln_s}  ../..%{BIN_DIR}/%{name}            %{buildroot}%{BIN_LINK}/.

#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------
%defattr(0644,root,root,0755)

%dir %{BASE_DIR}
%dir %{BIN_DIR}
%dir %{CONF_DIR}
%dir %{VAR_DIR}
%dir %{VAR_DIR}/graylist

%attr(0755,root,root) %{BIN_DIR}/*
%config(noreplace)    %{CONF_DIR}/*

%{BIN_LINK}/%{name}
%{BIN_LINK}/sd-prune-graylist
%{CONF_LINK}
%{VAR_LINK}

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
rm -rf %{_builddir}/%{name}-%{version}
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Nov 23 2013 Eric Shubert <eric@datamatters.us> 4.3.1-0.qt
- Added sd-prune-graylist script to package
* Mon Oct 21 2013 Eric Shubert <eric@datamatters.us> 4.3.1-0
- Initial package, much of which taken from qtp-install-spamdyke script
