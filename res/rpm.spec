Name:       xldesk
Version:    1.4.3
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://xldesk.com
Vendor:     xldesk <info@xldesk.com>
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/xldesk/
mkdir -p %{buildroot}/usr/share/xldesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -Dm 755 $HBB/target/release/xldesk %{buildroot}/usr/bin/xldesk
install -Dm 644 $HBB/libsciter-gtk.so %{buildroot}/usr/share/xldesk/libsciter-gtk.so
install -Dm 644 $HBB/res/xldesk.service -t "%{buildroot}/usr/share/xldesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/xldesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/xldesk.svg"
install -Dm 644 $HBB/res/xldesk.desktop -t "%{buildroot}/usr/share/xldesk/files"
install -Dm 644 $HBB/res/xldesk-link.desktop -t "%{buildroot}/usr/share/xldesk/files"

%files
/usr/bin/xldesk
/usr/share/xldesk/libsciter-gtk.so
/usr/share/xldesk/files/xldesk.service
/usr/share/icons/hicolor/256x256/apps/xldesk.png
/usr/share/icons/hicolor/scalable/apps/xldesk.svg
/usr/share/xldesk/files/xldesk.desktop
/usr/share/xldesk/files/xldesk-link.desktop
/usr/share/xldesk/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop xldesk || true
  ;;
esac

%post
cp /usr/share/xldesk/files/xldesk.service /etc/systemd/system/xldesk.service
cp /usr/share/xldesk/files/xldesk.desktop /usr/share/applications/xldesk.desktop
cp /usr/share/xldesk/files/xldesk-link.desktop /usr/share/applications/xldesk-link.desktop
systemctl daemon-reload
systemctl enable xldesk
systemctl start xldesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop xldesk || true
    systemctl disable xldesk || true
    rm /etc/systemd/system/xldesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/xldesk.desktop || true
    rm /usr/share/applications/xldesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
