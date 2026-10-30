import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import org.kde.plasma.plasmoid

PlasmoidItem {
    preferredRepresentation: fullRepresentation
    fullRepresentation: Item {
        Layout.minimumWidth: 64
        Layout.preferredWidth: 64
        Layout.minimumHeight: 16
        ToolTip.visible: hover.hovered
        ToolTip.text: "pkOS — Alt+Space for applications"
        HoverHandler { id: hover }
        Text {
            anchors.centerIn: parent
            text: "pkOS"
            color: "#edf2f7"
            font.family: "Inter"
            font.pixelSize: 13
            font.letterSpacing: 0.5
            renderType: Text.QtRendering
        }
    }
}
