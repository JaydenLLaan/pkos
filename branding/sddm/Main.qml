import QtQuick 2.15
import QtQuick.Controls 2.15
Pane {
    width: 1920
    height: 1080
    padding: 0
    font.family: "Inter"
    font.pixelSize: 14
    palette.window: "#10151b"
    palette.windowText: "#edf2f7"
    palette.base: "#17212b"
    palette.text: "#edf2f7"
    palette.button: "#17212b"
    palette.buttonText: "#edf2f7"
    palette.highlight: "#8babc0"
    palette.highlightedText: "#edf2f7"
    background: Rectangle {
        color: "#10151b"
    }
    Image {
        anchors.fill: parent
        source: "/usr/share/wallpapers/pkos-slate/contents/images/2560x1440.png"
        fillMode: Image.PreserveAspectCrop
    }
    Rectangle {
        width: 384
        height: 432
        radius: 12
        color: "#17212b"
        border.width: 1
        border.color: "#33434f"
        anchors.centerIn: parent
        Column {
            anchors.centerIn: parent
            spacing: 16
            width: 320
            Image {
                source: "wordmark.png"
                width: 224
                height: 72
                fillMode: Image.PreserveAspectFit
            }
            TextField {
                id: username
                width: parent.width
                placeholderText: "Username"
                placeholderTextColor: "#8babc0"
                text: userModel.lastUser
                font.family: "Inter"
                font.pixelSize: 16
                color: "#edf2f7"
                background: Rectangle {
                    color: "#10151b"
                    radius: 8
                    border.color: "#33434f"
                    border.width: 1
                }
                padding: 16
                KeyNavigation.tab: password
            }
            TextField {
                id: password
                width: parent.width
                placeholderText: "Password"
                placeholderTextColor: "#8babc0"
                echoMode: TextInput.Password
                focus: true
                font.pixelSize: 16
                color: "#edf2f7"
                background: Rectangle {
                    color: "#10151b"
                    radius: 8
                    border.color: "#33434f"
                    border.width: 1
                }
                padding: 16
                onAccepted: sddm.login(username.text, password.text, session.currentIndex)
            }
            ComboBox {
                id: session
                width: parent.width
                model: sessionModel
                textRole: "name"
                currentIndex: sessionModel.lastIndex
            }
            Button {
                width: parent.width
                text: "Sign in"
                onClicked: sddm.login(username.text, password.text, session.currentIndex)
            }
            Text {
                id: status
                color: "#d8b99a"
                font.pixelSize: 13
                text: ""
            }
        }
    }
    Row {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 32
        spacing: 16
        Button {
            text: "Restart"
            onClicked: sddm.reboot()
        }
        Button {
            text: "Power off"
            onClicked: sddm.powerOff()
        }
    }
    Connections {
        target: sddm
        function onLoginFailed() {
            status.text = "Could not sign in. Please try again."
            password.text = ""
        }
    }
}

