Name:       xldesk
Version:    1.1.9
Release:    0
Summary:    Remote desktop software
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
Remote desktop software. Works out of the box, no configuration required.

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
install -m 755 $HBB/target/release/xldesk %{buildroot}/usr/bin/xldesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/xldesk/libsciter-gtk.so
install $HBB/res/rustdesk.service %{buildroot}/usr/share/xldesk/files/xldesk.service
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/xldesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/xldesk.svg
install $HBB/res/rustdesk.desktop %{buildroot}/usr/share/xldesk/files/xldesk.desktop
install $HBB/res/rustdesk-link.desktop %{buildroot}/usr/share/xldesk/files/xldesk-link.desktop

%files
/usr/bin/xldesk
/usr/share/xldesk/libsciter-gtk.so
/usr/share/xldesk/files/xldesk.service
/usr/share/icons/hicolor/256x256/apps/xldesk.png
/usr/share/icons/hicolor/scalable/apps/xldesk.svg
/usr/share/xldesk/files/xldesk.desktop
/usr/share/xldesk/files/xldesk-link.desktop

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
cp /usr/share/xldesk/files/xldesk.desktop /usr/share/applications/
cp /usr/share/xldesk/files/xldesk-link.desktop /usr/share/applications/
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
