%global __python3 /usr/bin/python3.12
%global python3_pkgversion 3.12

Name:           python%{python3_pkgversion}-lxml
Version:        4.9.3
Release:        2%{?dist}
Summary:        XML processing library combining libxml2/libxslt with the ElementTree API

# The lxml project is licensed under BSD-3-Clause
# Some code is derived from ElementTree and cElementTree
# thus using the MIT-CMU elementtree license
# .xsl schematron files are under the MIT license
License:        BSD and MIT
URL:            https://github.com/lxml/lxml

# We use the get-lxml-source.sh script to generate the tarball
# without the isoschematron RNG validation file under a problematic license.
# See: https://gitlab.com/fedora/legal/fedora-license-data/-/issues/154
Source0:         lxml-%{version}-no-isoschematron-rng.tar.gz
Source1:         get-lxml-source.sh

# Make the validation of ISO-Schematron files optional in lxml,
# depending on the availability of the RNG validation file
# Rebased from https://github.com/lxml/lxml/commit/4bfab2c821961fb4c5ed8a04e329778c9b09a1df
# Will be included in lxml 5.0
Patch1:         Make-the-validation-of-ISO-Schematron-files-optional.patch
# Skip test_isoschematron.test_schematron_invalid_schema_empty without the RNG file
Patch2:         https://github.com/lxml/lxml/pull/380.patch

# Upstream issue: https://bugs.launchpad.net/lxml/+bug/2016939
Patch3:         Skip-failing-test-test_html_prefix_nsmap.patch

# Cython 3 support backported from future lxml 5.0
Patch4:         https://github.com/lxml/lxml/commit/dcbc0cc1cb0cedf8019184aaca805d2a649cd8de.patch
Patch5:         https://github.com/lxml/lxml/commit/a03a4b3c6b906d33c5ef1a15f3d5ca5fff600c76.patch

BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-Cython

%global _description \
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It\
provides safe and convenient access to these libraries using the ElementTree It\
extends the ElementTree API significantly to offer support for XPath, RelaxNG,\
XML Schema, XSLT, C14N and much more.

%description %{_description}

%prep
%autosetup -n lxml-%{version} -p1
# Don't run html5lib tests, the [html5] extra is not built in RHEL
rm src/lxml/html/tests/test_html5parser.py

# Remove pregenerated Cython C sources
find -type f -name '*.c' -print -delete >&2

%build
export WITH_CYTHON=true
%py3_build

%install
%py3_install

%check
# The tests assume inplace build, so we copy the built library to source-dir.
# If not done that, Python can either import the tests or the extension modules, but not both.
cp -a build/lib.%{python3_platform}-*/* src/
# The options are: verbose, unit, functional
%{python3} test.py -vuf

%files -n python%{python3_pkgversion}-lxml
%license LICENSE.txt LICENSES.txt
%license doc/licenses/BSD.txt doc/licenses/elementtree.txt
%doc README.rst
%{python3_sitearch}/lxml/
%{python3_sitearch}/lxml-*.egg-info/

%changelog
* Tue Jan 23 2024 Miro Hrončok <mhroncok@redhat.com> - 4.9.3-2
- Rebuilt for timestamp .pyc invalidation mode

* Tue Oct 17 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 4.9.3-1
- Initial package
- Fedora contributions by:
      Alexander Todorov <atodorov@redhat.com>
      Bill Nottingham <notting@fedoraproject.org>
      Charalampos Stratakis <cstratak@redhat.com>
      Dan Horák <dan@danny.cz>
      David Malcolm <dmalcolm@redhat.com>
      Dennis Gilmore <dennis@ausil.us>
      Fabio Alessandro Locati <me@fale.io>
      Igor Gnatenko <ignatenkobrain@fedoraproject.org>
      Jason ティビツ <tibbs@fedoraproject.org>
      Jeffrey C. Ollie <jeff@ocjtech.us>
      Jesse Keating <jkeating@fedoraproject.org>
      Kevin Fenzi <kevin@scrye.com>
      Lumir Balhar <lbalhar@redhat.com>
      Mikolaj Izdebski <mizdebsk@redhat.com>
      Miro Hrončok <miro@hroncok.cz>
      Peter Robinson <pbrobinson@gmail.com>
      Robert Kuska <rkuska@redhat.com>
      Shahms King <shahms@fedoraproject.org>
      Slavek Kabrda <bkabrda@redhat.com>
      Tomáš Hrnčiar <thrnciar@redhat.com>
      tomspur <tomspur@fedoraproject.org>
      Ville Skyttä <scop@fedoraproject.org>
      Yaakov Selkowitz <yselkowi@redhat.com>
