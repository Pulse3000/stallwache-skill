const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, WidthType, BorderStyle, HeadingLevel, PageBreak,
        ShadingType, LevelFormat } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const headerBg = "2E75B6";
const headerBorder = { style: BorderStyle.SINGLE, size: 6, color: headerBg, space: 1 };

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 },
        paragraph: { spacing: { line: 360, lineRule: "auto" } }
      }
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 32, bold: true, font: "Arial", color: "FFFFFF" },
        paragraph: {
          spacing: { before: 240, after: 120 },
          outlineLevel: 0,
          border: { bottom: headerBorder }
        }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 }
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 24, bold: true, font: "Arial", color: "404040" },
        paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 2 }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      },
      {
        reference: "numbers",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Title
      new Paragraph({ children: [new TextRun("")], spacing: { before: 800 } }),
      new Paragraph({
        children: [new TextRun({ text: "STALLWACHE", bold: true, size: 56, color: "2E75B6" })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Hardware-Setup-Guide", size: 40, color: "2E75B6" })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Rollei Safetycam HD 20 Integration", size: 32, bold: true })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "KI-basiertes Kalberkennungs- und Stallüberwachungssystem", italic: true, size: 24 })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 1200 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Version 1.0 | Mai 2026", size: 22, color: "666666" })],
        alignment: AlignmentType.CENTER
      }),

      new PageBreak(),

      // Section 1
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("1. Systemübersicht")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),
      new Paragraph({ children: [new TextRun("Das Stallwache-System besteht aus drei Hauptkomponenten:")] }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Rollei Safetycam HD 20", bold: true }), new TextRun(" – Netzwerk-Überwachungskamera")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Edge-Server (lokaler PC/Laptop)", bold: true }), new TextRun(" – KI-Inferenz und Alert-Verarbeitung")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Rollei Cloud & Messenger", bold: true }), new TextRun(" – Backup-Speicher und Benachrichtigungen")]
      }),

      new PageBreak(),

      // Section 2
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("2. Rollei Safetycam HD 20 – Spezifikationen")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.1 Hardware-Specs")]
      }),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2340, 7020],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 2340, type: WidthType.DXA },
                shading: { fill: headerBg, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Parameter", bold: true, color: "FFFFFF" })] })]
              }),
              new TableCell({
                borders, width: { size: 7020, type: WidthType.DXA },
                shading: { fill: headerBg, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Wert", bold: true, color: "FFFFFF" })] })]
              })
            ]
          }),
          ...createSpecRows([
            ["Auflösung", "1920×1080 Pixel (Full HD)"],
            ["Framerate", "30 fps bei Full HD"],
            ["Sensor", "1/3″ CMOS"],
            ["Blickwinkel", "160° diagonal"],
            ["Nachtsicht", "Infrarot-LEDs (bis 15m)"],
            ["Stromversorgung", "12V DC / PoE"],
            ["Wasserschutz", "IP66"],
            ["Betriebstemp.", "-10°C bis +50°C"],
            ["Gewicht", "ca. 280g"],
            ["Abmessungen", "180×108×86 mm"]
          ])
        ]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { after: 200 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.2 Netzwerk-Features")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "RTSP-Stream:", bold: true }), new TextRun(" rtsp://[CAMERA_IP]:554/stream")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "ONVIF-Support:", bold: true }), new TextRun(" Standardisierte Geräte-Integration")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "HTTP-API:", bold: true }), new TextRun(" Web-Interface für Konfiguration")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "WiFi 802.11ac:", bold: true }), new TextRun(" 5GHz/2.4GHz oder Gigabit Ethernet")]
      }),

      new PageBreak(),

      // Section 3
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("3. Netzwerk-Konfiguration")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.1 Kamera-Initialisierung")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Stromversorgung anschließen (12V DC oder PoE-Switch)")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("30 Sekunden warten auf Boot")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("LED sollte blau/grün blinken (Verbindung wird hergestellt)")]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { after: 200 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.2 IP-Adresse ermitteln")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Methode A: Rollei Setup-App")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Laden Sie die \"Rollei SafetyCam\" App herunter")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("App scannt lokales Netzwerk nach Kamera")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Notieren Sie die IP-Adresse (z.B. 192.168.1.100)")]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { after: 200 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.3 Statische IP zuweisen")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Öffnen Sie das Web-Interface: http://[CAMERA_IP]")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Standard-Login: admin / 12345")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Navigieren Sie zu Einstellungen → Netzwerk")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Wählen Sie \"Statische IP\" statt DHCP")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "Empfehlung:", bold: true }), new TextRun(" 192.168.1.200")]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { after: 200 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.4 RTSP-Stream testen")]
      }),

      new Paragraph({ children: [new TextRun("Öffnen Sie VLC Media Player:")] }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Datei → Stream öffnen")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("URL eingeben:")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "rtsp://admin:12345@192.168.1.200:554/stream", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Video startet ✓ – RTSP funktioniert")]
      }),

      new PageBreak(),

      // Section 4
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("4. Platzierung im Stall")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("4.1 Optimale Positionierung")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Höhe:", bold: true }), new TextRun(" 2–3m")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Winkel:", bold: true }), new TextRun(" 45° nach unten gerichtet")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Entfernung:", bold: true }), new TextRun(" 2–5m zum Kalb-Abkalbe-Bereich")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Vermeiden Sie:", bold: true }), new TextRun(" Gegenlicht, Reflektionen")]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { after: 200 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("4.2 Stromversorgung")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Separates 12V-Netzteil oder PoE-Injektor")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Kabelführung: entlang Stallwand")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Netzwerk-Kabel: Cat5e/Cat6, mind. 10m")]
      }),

      new PageBreak(),

      // Section 5
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("5. Edge-Server Anforderungen")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.1 Mindestanforderungen")]
      }),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2340, 7020],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 2340, type: WidthType.DXA },
                shading: { fill: headerBg, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Komponente", bold: true, color: "FFFFFF" })] })]
              }),
              new TableCell({
                borders, width: { size: 7020, type: WidthType.DXA },
                shading: { fill: headerBg, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Anforderung", bold: true, color: "FFFFFF" })] })]
              })
            ]
          }),
          ...createSpecRows([
            ["CPU", "Intel i5/i7 oder AMD Ryzen 5/7 (4+ Cores)"],
            ["RAM", "8 GB (16 GB empfohlen)"],
            ["GPU", "Optional: NVIDIA RTX 3060+"],
            ["Speicher", "250 GB SSD"],
            ["OS", "Windows 10/11, Linux, macOS"],
            ["Netzwerk", "Gigabit Ethernet oder 5GHz WiFi"],
            ["RAM-Nutzung", "~2–4 GB während Inferenz"],
            ["CPU-Last", "~30–60% bei 30fps 1080p"]
          ])
        ]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { after: 200 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.2 Software-Setup")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "Python 3.10+", bold: true }), new TextRun(" installieren")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Dependencies:")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("opencv-python")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("ultralytics (YOLOv8)")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("python-telegram-bot")]
      }),

      new PageBreak(),

      // Section 6
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("6. Sicherheit & Datenschutz")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Standard-Passwort ändern!:", bold: true }), new TextRun(" admin → sicheres Passwort")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Firewall-Regel:", bold: true }), new TextRun(" Kamera nur im lokalen Netzwerk")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Firmware aktuell:", bold: true }), new TextRun(" Regelmäßig prüfen")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Video-Speicherung:", bold: true }), new TextRun(" Lokal 7 Tage, Cloud 30 Tage")]
      }),

      new PageBreak(),

      // Section 7
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("7. Troubleshooting")],
        shading: { fill: headerBg, type: ShadingType.CLEAR }
      }),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2700, 6660],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 2700, type: WidthType.DXA },
                shading: { fill: headerBg, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Problem", bold: true, color: "FFFFFF" })] })]
              }),
              new TableCell({
                borders, width: { size: 6660, type: WidthType.DXA },
                shading: { fill: headerBg, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Lösung", bold: true, color: "FFFFFF" })] })]
              })
            ]
          }),
          ...createTSRows([
            ["Kamera antwortet nicht", "1) Stromversorgung prüfen\n2) Router neu starten\n3) Kamera neu booten"],
            ["RTSP-Stream fehlt", "1) Netzwerk-Stabilität überprüfen\n2) WiFi → Ethernet wechseln\n3) Firewall-Regeln prüfen"],
            ["Niedriges FPS", "1) CPU/RAM überprüfen\n2) Streaming-Qualität reduzieren\n3) GPU aktivieren"],
            ["Cloud-Upload fehlt", "1) Rollei-Cloud-Login prüfen\n2) Internet-Verbindung testen\n3) Speicherplatz überprüfen"]
          ])
        ]
      }),

      new PageBreak(),

      // Final Section
      new Paragraph({
        children: [new TextRun({ text: "Nächste Schritte", bold: true, size: 32, color: "2E75B6" })],
        spacing: { after: 200 }
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Konsultieren Sie den Python-Code-Guide")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Docker-Container aufsetzen")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("KI-Modelle mit Testvideos prüfen")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Alert-Schwellenwerte tunen")]
      }),

      new Paragraph({ children: [new TextRun("")], spacing: { before: 400 } }),
      new Paragraph({
        children: [new TextRun({ text: "Fragen? Kontaktieren Sie: stallwache123@gmail.com", italic: true })],
        spacing: { before: 200 }
      })
    ]
  }]
});

function createSpecRows(specs) {
  return specs.map(([param, value]) =>
    new TableRow({
      children: [
        new TableCell({
          borders, width: { size: 2340, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun(param)] })]
        }),
        new TableCell({
          borders, width: { size: 7020, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun(value)] })]
        })
      ]
    })
  );
}

function createTSRows(issues) {
  return issues.map(([problem, solution]) =>
    new TableRow({
      children: [
        new TableCell({
          borders, width: { size: 2700, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun({ text: problem, bold: true })] })]
        }),
        new TableCell({
          borders, width: { size: 6660, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun(solution)] })]
        })
      ]
    })
  );
}

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("C:\\Users\\axe2k\\Desktop\\Projekt Stall\\stallwache\\Stallwache\\Rollei_HD20_Hardware_Setup_Guide.docx", buffer);
  console.log("✓ Document created successfully!");
});
