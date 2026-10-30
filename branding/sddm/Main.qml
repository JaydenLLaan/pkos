import QtQuick 2.15
import QtQuick.Controls 2.15
Rectangle {
    width: 1920
    height: 1080
    color: "#10151b"
    Image {
        anchors.fill: parent
        source: "/usr/share/wallpapers/pkos-slate/contents/images/2560x1440.png"
        fillMode: Image.PreserveAspectCrop
    }
    Rectangle {
        width: 380
        height: 430
        radius: 16
        color: "#111921"
        anchors.centerIn: parent
        Column {
            anchors.centerIn: parent
            spacing: 20
            width: 300
            Image {
                source: "wordmark.png"
                width: 225
                height: 68
                fillMode: Image.PreserveAspectFit
            }
            TextField {
                id: username
                width: parent.width
                placeholderText: "Username"
                text: userModel.lastUser
                font.family: "Inter"
                font.pixelSize: 16
                color: "#edf2f7"
                background: Rectangle {
                    color: "#1f2b36"
                    radius: 6
                }
                padding: 12
                KeyNavigation.tab: password
            }
            TextField {
                id: password
                width: parent.width
                placeholderText: "Password"
                echoMode: TextInput.Password
                focus: true
                font.pixelSize: 16
                color: "#edf2f7"
                background: Rectangle {
                    color: "#1f2b36"
                    radius: 6
                }
                padding: 12
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

