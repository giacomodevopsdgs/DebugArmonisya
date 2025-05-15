Name:       armonisya
Version:    RH_VERSION
Release:    RH_RELEASE
Summary:    Armonisya, a DevSecOps Identity Security helper

License:    Copyrighted
Source0:    RPM_SOURCE

Requires:   python3.11, python3.11-pip, git

BuildArch:  noarch

%description
Armonisya, a DevSecOps Identity Security helper

%include %{_topdir}/SPECS/preinst.spec
%include %{_topdir}/SPECS/postinst.spec
%include %{_topdir}/SPECS/prerm.spec
%include %{_topdir}/SPECS/postrm.spec

%prep
%setup  -q #unpack tarball

%install
cp -rfa * %{buildroot}

%include %{_topdir}/SPECS/files.spec
