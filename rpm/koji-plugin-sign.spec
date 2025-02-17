Name:           koji-plugin-sign
Version:        1.4.0
Release:        12%{?dist}
Summary:        GPG signing plugin for koji-hub

Group:          Applications/System
License:        Apache 2.0
URL:            https://github.com/osg-htc/koji-plugin-sign
Source:         %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  koji-hub
Requires:       koji-hub
%if 0%{?el7}
BuildRequires:  pexpect
Requires:       pexpect
%else
BuildRequires:  python3-pexpect
Requires:       python3-pexpect
%endif
Requires:       /usr/bin/rpmsign

%description
GPG signing plugin for koji-hub

%prep
%autosetup -p1

%build
exit 0


%install
mkdir -p $RPM_BUILD_ROOT
install -D sign.conf -m 0600 $RPM_BUILD_ROOT/etc/koji-hub/plugins/sign.conf
install -D sign.py -m 0755 $RPM_BUILD_ROOT/usr/lib/koji-hub-plugins/sign.py


%files
%config(noreplace) %attr(0600,apache,apache) /etc/koji-hub/plugins/sign.conf
%attr(0755,root,root) /usr/lib/koji-hub-plugins/sign.py*



%changelog
* Fri Oct 13 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-12
- First build from GitHub sources

* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-10
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Wed Dec 28 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-9
- Patch to add gpg_digest_algo option (SOFTWARE-5425)
- Patches to improve error detection (SOFTWARE-5410)
- Patch for Python 3 compat

* Wed Apr 22 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-8
- Add /usr/bin/rpmsign dependency

* Thu Oct 17 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-7
- Rebuild with dist tag

* Thu Sep 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-6
- fixed disabling not working with previous patch

* Thu Sep 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-5
- added patch to allow enabling/disabling signing for a tag (or by default)

* Thu Sep 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-4
- added pexpect dependency

* Thu Sep 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-3
- Set package to be noarch
- sign.py moved to /usr/lib/koji-hub-plugins to match what the package koji-hub-plugins is doing

* Fri Aug 5 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-1
- Created

