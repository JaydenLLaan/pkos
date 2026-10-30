// Two independent panels; no application-menu widget is used.
var top = new Panel;
top.location = "top";
top.height = 28;
top.floating = false;
top.lengthMode = "fill";
top.hiding = "none";
top.opacity = "translucent";
top.addWidget("org.pkos.wordmark");
var spacer = top.addWidget("org.kde.plasma.panelspacer");
spacer.currentConfigGroup = ["General"];
spacer.writeConfig("expanding", true);
top.addWidget("org.kde.plasma.systemtray");
var clock = top.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", false);
clock.writeConfig("showSeconds", 0);
clock.writeConfig("use24hFormat", 2);
clock.writeConfig("fontFamily", "Inter");
clock.writeConfig("fontSize", 10);

var dock = new Panel;
dock.location = "bottom";
dock.height = 56;
dock.floating = true;
dock.alignment = "center";
dock.lengthMode = "fit";
dock.hiding = "none";
dock.opacity = "opaque";
var tasks = dock.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", ["applications:org.kde.dolphin.desktop", "applications:kitty.desktop", "applications:codium.desktop", "applications:firefox-esr.desktop", "applications:systemsettings.desktop"]);
tasks.writeConfig("fill", false);
tasks.writeConfig("iconSpacing", 1);
tasks.writeConfig("taskHoverEffect", true);
tasks.writeConfig("highlightWindows", false);
tasks.writeConfig("showOnlyCurrentDesktop", true);
for (var i = 0; i < screenCount; i++) {
    var desktop = desktopForScreen(i);
    desktop.wallpaperPlugin = "org.kde.image";
    desktop.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    desktop.writeConfig("Image", "file:///usr/share/wallpapers/pkos-slate/contents/images/2560x1440.png");
    // Folder View is deliberately empty on installed boots. The live launcher
    // is the only file placed in Desktop, and Calamares removes it from skel.
    desktop.currentConfigGroup = ["General"];
    desktop.writeConfig("showToolbox", false);
}

