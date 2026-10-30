import QtQuick 2.0
import calamares.slideshow 1.0
Presentation {
    id: presentation
    Timer { interval: 12000; repeat: true; running: true; onTriggered: presentation.goToNextSlide() }
    Slide {
        Rectangle { anchors.fill: parent; color: "#10151b" }
        Column {
            anchors.centerIn: parent; width: parent.width * 0.8; spacing: 24
            Text { text: "A quiet place to build."; color: "#edf2f7"; font.pixelSize: 28; font.family: "Inter" }
            Text { text: "Plasma 6 · Wayland · Intel + NVIDIA"; color: "#9baab9"; font.pixelSize: 17 }
        }
    }
    Slide {
        Rectangle { anchors.fill: parent; color: "#10151b" }
        Column {
            anchors.centerIn: parent; width: parent.width * 0.8; spacing: 24
            Text { text: "Your tools. Ready."; color: "#edf2f7"; font.pixelSize: 28; font.family: "Inter" }
            Text { text: "Python · Node · Go · containers · Git"; color: "#9baab9"; font.pixelSize: 17 }
        }
    }
    Slide {
        Rectangle { anchors.fill: parent; color: "#10151b" }
        Column {
            anchors.centerIn: parent; width: parent.width * 0.8; spacing: 24
            Text { text: "Make it yours."; color: "#edf2f7"; font.pixelSize: 28; font.family: "Inter" }
            Text { text: "Run pk-setup for AI tools, Rust and local models."; color: "#9baab9"; font.pixelSize: 17 }
        }
    }
}

