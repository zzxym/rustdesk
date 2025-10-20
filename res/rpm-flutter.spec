Name:       xldesk
Version:    1.4.3
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://xldesk.com
Vendor:     xldesk <info@xldesk.com>
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/xldesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/xldesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/xldesk.service -t "%{buildroot}/usr/share/xldesk/files"
install -Dm 644 $HBB/res/xldesk.desktop -t "%{buildroot}/usr/share/xldesk/files"
install -Dm 644 $HBB/res/xldesk-link.desktop -t "%{buildroot}/usr/share/xldesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/xldesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/xldesk.svg"

%files
/usr/share/xldesk/*
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
ln -sf /usr/share/xldesk/xldesk /usr/bin/xldesk
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
    rm /usr/bin/xldesk || true
    rmdir /usr/lib/xldesk || true
    rmdir /usr/local/xldesk || true
    rmdir /usr/share/xldesk || true
    rm /usr/share/applications/xldesk.desktop || true
    rm /usr/share/applications/xldesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/xldesk || true
    rmdir /usr/local/xldesk || true
  ;;
esac
