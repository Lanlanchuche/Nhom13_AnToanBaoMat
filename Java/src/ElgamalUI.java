import javax.swing.*;
import javax.swing.border.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Random;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

public class ElgamalUI extends JFrame {

    // ── Fields ──────────────────────────────────────────────────────────────
    // Auto-tab
    private JTextField txtP_a, txtG_a, txtX_a, txtY_a, txtK_a;
    // Manual-tab
    private JTextField txtP_m, txtG_m, txtX_m, txtY_m, txtK_m;

    private JTextArea txtPlain, txtC1, txtC2, txtCipher, txtDecrypt, txtCipherIn;

    private JButton btnGenAuto, btnGenManual;
    private JButton btnEncrypt, btnDecrypt, btnClear, btnExit;
    private JButton btnSaveKey, btnSavePlain, btnSaveCipher, btnSaveDecrypt;
    private JButton btnLoadPlain, btnLoadCipher;

    private JTabbedPane keyTabs;
    private String originalPlainText, originalCipherText;

    // ── Constructor ──────────────────────────────────────────────────────────
    public ElgamalUI() {
        setTitle("Mã hóa ElGamal");
        setSize(1260, 680);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        UIManager.put("Panel.background", new Color(0xF0F0F0));
        initUI();
    }

    // ── Build UI ─────────────────────────────────────────────────────────────
    private void initUI() {
        JTabbedPane mainTab = new JTabbedPane();
        mainTab.addTab("Mã hóa ElGamal", buildMainPanel());
        add(mainTab);
    }

    private JPanel buildMainPanel() {
        JPanel root = new JPanel(new BorderLayout(8, 8));
        root.setBorder(new EmptyBorder(8, 8, 8, 8));

        // TOP: 3-column layout
        JPanel top = new JPanel(new GridLayout(1, 3, 8, 0));
        top.add(buildKeyPanel());
        top.add(buildEncryptPanel());
        top.add(buildDecryptPanel());
        root.add(top, BorderLayout.CENTER);

        // BOTTOM: intermediate values + action buttons
        JPanel bottom = new JPanel(new BorderLayout(0, 4));
        bottom.add(buildIntermediatePanel(), BorderLayout.CENTER);
        bottom.add(buildButtonBar(), BorderLayout.SOUTH);
        root.add(bottom, BorderLayout.SOUTH);

        return root;
    }

    // ── LEFT: Key panel ───────────────────────────────────────────────────────
    private JPanel buildKeyPanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 4));
        panel.setBorder(titledBorder("Tạo khóa"));

        keyTabs = new JTabbedPane(JTabbedPane.TOP);
        keyTabs.addTab("Tự động", buildAutoTab());
        keyTabs.addTab("Tùy chọn", buildManualTab());
        panel.add(keyTabs, BorderLayout.CENTER);

        return panel;
    }

    private JPanel buildAutoTab() {
        JPanel p = new JPanel(new GridBagLayout());
        p.setBorder(new EmptyBorder(8, 6, 6, 6));
        GridBagConstraints gc = new GridBagConstraints();
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.insets = new Insets(3, 2, 3, 2);

        txtP_a = readonlyField(); txtG_a = readonlyField();
        txtX_a = readonlyField(); txtY_a = readonlyField(); txtK_a = readonlyField();

        JLabel note = new JLabel("<html><i style='color:#666'>Hệ thống tự sinh các tham số hợp lệ.</i></html>");
        addRow(p, gc, 0, "Số nguyên tố  p =", txtP_a);
        addRow(p, gc, 1, "Phần tử sinh  a =", txtG_a);
        addRow(p, gc, 2, "Khóa bí mật   x =", txtX_a);
        addRow(p, gc, 3, "d = a^x mod p  d =", txtY_a);
        addRow(p, gc, 4, "Số ngẫu nhiên k =", txtK_a);

        gc.gridx=0; gc.gridy=5; gc.gridwidth=2;
        gc.insets = new Insets(2,2,2,2);
        p.add(note, gc);

        gc.gridy=6;
        btnGenAuto = makeButton("Tạo khóa ngẫu nhiên mới", new Color(0x2980B9), Color.WHITE);
        btnGenAuto.setFont(new Font("Segoe UI", Font.BOLD, 12));
        p.add(btnGenAuto, gc);

        // filler
        gc.gridy=7; gc.weighty=1;
        p.add(new JLabel(), gc);

        return p;
    }

    private JPanel buildManualTab() {
        JPanel p = new JPanel(new GridBagLayout());
        p.setBorder(new EmptyBorder(8, 6, 6, 6));
        GridBagConstraints gc = new GridBagConstraints();
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.insets = new Insets(3, 2, 3, 2);

        txtP_m = editField(); txtG_m = editField();
        txtX_m = editField(); txtY_m = readonlyField(); txtK_m = editField();

        addRow(p, gc, 0, "Số nguyên tố  p =", txtP_m);
        addRow(p, gc, 1, "Phần tử sinh  a =", txtG_m);
        addRow(p, gc, 2, "Khóa bí mật   x =", txtX_m);
        addRow(p, gc, 3, "d = a^x mod p  d =", txtY_m);
        addRow(p, gc, 4, "Số ngẫu nhiên k =", txtK_m);

        gc.gridx=0; gc.gridy=5; gc.gridwidth=2;
        gc.insets = new Insets(4,2,2,2);
        btnGenManual = makeButton("Tính d từ tham số", new Color(0x27AE60), Color.WHITE);
        btnGenManual.setFont(new Font("Segoe UI", Font.BOLD, 12));
        p.add(btnGenManual, gc);

        gc.gridy=6; gc.weighty=1;
        p.add(new JLabel(), gc);

        return p;
    }

    private void addRow(JPanel p, GridBagConstraints gc, int row, String label, JTextField field) {
        gc.gridwidth=1; gc.weightx=0; gc.gridx=0; gc.gridy=row;
        JLabel lbl = new JLabel(label);
        lbl.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        p.add(lbl, gc);
        gc.gridx=1; gc.weightx=1;
        p.add(field, gc);
    }

    // ── CENTER: Encrypt panel ─────────────────────────────────────────────────
    private JPanel buildEncryptPanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 6));
        panel.setBorder(titledBorder("Mã hóa"));

        JPanel top = new JPanel(new BorderLayout(0, 4));

        JLabel lbl = new JLabel("Bản rõ");
        lbl.setFont(labelFont());
        top.add(lbl, BorderLayout.NORTH);
        txtPlain = makeTextArea();
        top.add(new JScrollPane(txtPlain), BorderLayout.CENTER);

        JPanel kRow = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 0));
        JLabel klbl = new JLabel("Số ngẫu nhiên k =");
        klbl.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        kRow.add(klbl);
        // k field is read from tab, no separate display needed

        JPanel btnRow = new JPanel(new GridLayout(1, 2, 6, 0));
        btnLoadPlain = makeButton("Mở file bản rõ", new Color(0x7F8C8D), Color.WHITE);
        btnEncrypt   = makeButton("Thực hiện mã hóa", new Color(0x2980B9), Color.WHITE);
        btnRow.add(btnLoadPlain);
        btnRow.add(btnEncrypt);

        panel.add(top, BorderLayout.CENTER);
        panel.add(btnRow, BorderLayout.SOUTH);
        return panel;
    }

    // ── RIGHT: Decrypt panel ──────────────────────────────────────────────────
    private JPanel buildDecryptPanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 6));
        panel.setBorder(titledBorder("Giải mã"));

        JPanel top = new JPanel(new BorderLayout(0, 4));
        JLabel lbl = new JLabel("Bản mã hóa nhận được:");
        lbl.setFont(labelFont());
        top.add(lbl, BorderLayout.NORTH);
        txtCipherIn = makeTextArea();
        top.add(new JScrollPane(txtCipherIn), BorderLayout.CENTER);

        JPanel btnRow = new JPanel(new GridLayout(1, 2, 6, 0));
        btnLoadCipher = makeButton("Mở file", new Color(0x7F8C8D), Color.WHITE);
        btnDecrypt    = makeButton("Thực hiện giải mã", new Color(0x8E44AD), Color.WHITE);
        btnRow.add(btnLoadCipher);
        btnRow.add(btnDecrypt);

        panel.add(top, BorderLayout.CENTER);
        panel.add(btnRow, BorderLayout.SOUTH);
        return panel;
    }

    // ── BOTTOM: C1, C2, Cipher, Decrypt ──────────────────────────────────────
    private JPanel buildIntermediatePanel() {
        JPanel panel = new JPanel(new GridLayout(1, 4, 8, 0));
        panel.setPreferredSize(new Dimension(0, 180));

        txtC1      = makeTextArea();
        txtC2      = makeTextArea();
        txtCipher  = makeTextArea();
        txtDecrypt = makeTextArea();
        txtDecrypt.setEditable(false);

        panel.add(labeledScroll("(C1 = a^k mod p)  C1 =", txtC1));
        panel.add(labeledScroll("(C2 = M×d^k mod p)  C2 =", txtC2));
        panel.add(labeledScroll("Bản mã:", txtCipher));
        panel.add(labeledScroll("Giải mã bản mã hóa nhận được bản rõ", txtDecrypt));

        return panel;
    }

    private JPanel labeledScroll(String title, JTextArea area) {
        JPanel p = new JPanel(new BorderLayout(0, 3));
        JLabel lbl = new JLabel(title);
        lbl.setFont(new Font("Segoe UI", Font.BOLD, 11));
        lbl.setForeground(new Color(0x34495E));
        p.add(lbl, BorderLayout.NORTH);
        JScrollPane sp = new JScrollPane(area);
        sp.setBorder(BorderFactory.createLineBorder(new Color(0xBBBBBB)));
        p.add(sp, BorderLayout.CENTER);
        return p;
    }

    // ── Bottom button bar ─────────────────────────────────────────────────────
    private JPanel buildButtonBar() {
        JPanel bar = new JPanel(new GridLayout(1, 5, 6, 0));
        bar.setPreferredSize(new Dimension(0, 36));

        btnSavePlain  = makeButton("Lưu file mã hóa", new Color(0x27AE60), Color.WHITE);
        btnSaveCipher = makeButton("Chuyển →", new Color(0x2980B9), Color.WHITE);
        btnSaveKey    = makeButton("Lưu khóa", new Color(0xE67E22), Color.WHITE);
        btnClear      = makeButton("Làm mới", new Color(0x7F8C8D), Color.WHITE);
        btnExit       = makeButton("Thoát", new Color(0xC0392B), Color.WHITE);

        bar.add(btnSavePlain);
        bar.add(btnSaveCipher);
        bar.add(btnSaveKey);
        bar.add(btnClear);
        bar.add(btnExit);
        return bar;
    }

    // ── Component helpers ─────────────────────────────────────────────────────
    private Border titledBorder(String title) {
        TitledBorder tb = BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(0xAAAAAA), 1), title,
            TitledBorder.LEFT, TitledBorder.TOP,
            new Font("Segoe UI", Font.BOLD, 13), new Color(0x2C3E50));
        return BorderFactory.createCompoundBorder(tb, new EmptyBorder(2, 4, 4, 4));
    }

    private Font labelFont() { return new Font("Segoe UI", Font.BOLD, 12); }

    private JTextField editField() {
        JTextField f = new JTextField(10);
        f.setFont(new Font("Consolas", Font.PLAIN, 13));
        return f;
    }

    private JTextField readonlyField() {
        JTextField f = editField();
        f.setEditable(false);
        f.setBackground(new Color(0xEEEEEE));
        f.setForeground(new Color(0x555555));
        return f;
    }

    private JTextArea makeTextArea() {
        JTextArea a = new JTextArea();
        a.setFont(new Font("Consolas", Font.PLAIN, 12));
        a.setLineWrap(true);
        a.setMargin(new Insets(4, 4, 4, 4));
        return a;
    }

    private JButton makeButton(String text, Color bg, Color fg) {
        JButton btn = new JButton(text);
        btn.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        btn.setFocusPainted(false);
        btn.setBorderPainted(true);
        btn.setOpaque(false);
        btn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        return btn;
    }

    // ── Helper accessors (active tab) ─────────────────────────────────────────
    private boolean isAuto() { return keyTabs.getSelectedIndex() == 0; }
    private int getP()  { return parse(isAuto() ? txtP_a : txtP_m); }
    private int getA()  { return parse(isAuto() ? txtG_a : txtG_m); }
    private int getPrivateKey()  { return parse(isAuto() ? txtX_a : txtX_m); }
    private int getPublickey()  { return parse(isAuto() ? txtY_a : txtY_m); }
    private int getK()  { return parse(isAuto() ? txtK_a : txtK_m); }
    private int parse(JTextField f) {
    try {
        return Integer.parseInt(f.getText().trim());
    } catch (NumberFormatException e) {
        throw new IllegalArgumentException("Vui lòng nhập số hợp lệ");
    }
}

    // ── Events ────────────────────────────────────────────────────────────────
    private void initEvents() {

        // Auto generate
        btnGenAuto.addActionListener(e -> {
            try {
                int[] key = ElGamal.generateKey();
                txtP_a.setText(String.valueOf(key[0]));
                txtG_a.setText(String.valueOf(key[1]));
                txtX_a.setText(String.valueOf(key[2]));
                txtY_a.setText(String.valueOf(key[3]));
                Random rd = new Random();
                int p = key[0], k;
                do { k = rd.nextInt(p - 3) + 2; } while (!ElGamal.gcdEqualsOne(k, p - 1));
                txtK_a.setText(String.valueOf(k));
            } catch (Exception ex) { err("Lỗi tạo khóa tự động"); }
        });

        // Manual compute d
        btnGenManual.addActionListener(e -> {
            try {
                int p = parse(txtP_m), g = parse(txtG_m), x = parse(txtX_m);
                if (!ElGamal.isPrime(p))        { err("p phải là số nguyên tố"); return; }
                if (!ElGamal.isGenerator(g, p)) { err("a không phải phần tử sinh của Zp*"); return; }
                txtY_m.setText(String.valueOf((int) ElGamal.modPow(g, x, p)));
            } catch (Exception ex) { err("Lỗi tính khóa thủ công"); }
        });

        // Encrypt
        btnEncrypt.addActionListener(e -> {
            try {
                int p = getP(), g = getA(), y = getPublickey(), k = getK();
                if (p <= 255) {
    err("p phải lớn hơn 255 để mã hóa ký tự UTF-8");
    return;
}
                if (k <= 1 || k >= p - 1)             { err("k phải thỏa 1 < k < p-1"); return; }
                if (!ElGamal.gcdEqualsOne(k, p - 1))  { err("k phải nguyên tố cùng nhau với p-1"); return; }
                StringBuilder sb1 = new StringBuilder(), sb2 = new StringBuilder(), sb3 = new StringBuilder();
                for (byte b : txtPlain.getText().getBytes(StandardCharsets.UTF_8)) {
                    int m = b & 0xFF;
                    int[] pair = ElGamal.encryptChar(m, p, g, y, k);
                    sb1.append(pair[0]).append("\n");
                    sb2.append(pair[1]).append("\n");
                    sb3.append("(").append(pair[0]).append(", ").append(pair[1]).append(")\n");
                }
                txtC1.setText(sb1.toString());
                txtC2.setText(sb2.toString());
                txtCipher.setText(sb3.toString());
                originalPlainText  = txtPlain.getText();
                originalCipherText = txtCipher.getText();
            } catch (Exception ex) { err("Lỗi mã hóa dữ liệu."); }
        });

        // Decrypt — uses txtCipherIn (top-right) first, falls back to txtCipher
        btnDecrypt.addActionListener(e -> {
            try {
                int p = getP(), x = getPrivateKey();
                String src = txtCipherIn.getText().trim().isEmpty() ? txtCipher.getText() : txtCipherIn.getText();
               txtDecrypt.setText(decryptText(src, p, x));

boolean mod = isCurrentCipherModified();

boolean bad = false;
if (originalPlainText != null) {
    bad = !originalPlainText.trim()
            .equals(txtDecrypt.getText().trim());
}

if (bad || mod) {
    err((bad ? "Khóa sai" : "") +
        (bad && mod ? " và " : "") +
        (mod ? "bản mã đã bị chỉnh sửa" : ""));
}
            } catch (Exception ex) { err("Lỗi giải mã dữ liệu."); }
        });

        // "Chuyển →" copies cipher to cipherIn
        btnSaveCipher.addActionListener(e -> txtCipherIn.setText(txtCipher.getText()));

        btnSavePlain.addActionListener(e -> {
            String t = txtPlain.getText();
            if (t.isEmpty()) { err("Chưa có bản gốc."); return; }
            saveFile(t, "original");
        });

        btnSaveKey.addActionListener(e -> {
            String t = keyText();
            if (t.isEmpty()) { err("Chưa có khóa."); return; }
            saveFile(t, "key");
        });

        btnLoadPlain.addActionListener(e -> {
            String c = loadFile(); if (c != null) txtPlain.setText(c);
        });

        btnLoadCipher.addActionListener(e -> {
            String c = loadFile(); if (c != null) txtCipherIn.setText(c);
        });

        btnClear.addActionListener(e -> {
            txtPlain.setText(""); txtC1.setText(""); txtC2.setText("");
            txtCipher.setText(""); txtCipherIn.setText(""); txtDecrypt.setText("");
            originalPlainText = originalCipherText = null;
        });

        btnExit.addActionListener(e -> System.exit(0));
    }

    private String keyText() {
        try {
            return "p = "+getP()+"\na = "+getA()+"\nx = "+getPrivateKey()+"\nd = "+getPublickey()+"\nk = "+getK()+"\n";
        } catch (Exception e) { return ""; }
    }

    private void err(String msg) {
        JOptionPane.showMessageDialog(this, msg, "Thông báo", JOptionPane.WARNING_MESSAGE);
    }

    // ── File I/O ──────────────────────────────────────────────────────────────
    private void saveFile(String text, String base) {
        JFileChooser fc = new JFileChooser();
        fc.addChoosableFileFilter(new FileNameExtensionFilter("Text (*.txt)", "txt"));
        fc.addChoosableFileFilter(new FileNameExtensionFilter("Word (*.docx)", "docx"));
        fc.addChoosableFileFilter(new FileNameExtensionFilter("PDF (*.pdf)", "pdf"));
        fc.setSelectedFile(new File(base + ".txt"));
        fc.setAcceptAllFileFilterUsed(false);
        if (fc.showSaveDialog(this) != JFileChooser.APPROVE_OPTION) return;
        File f = fc.getSelectedFile();
        String name = f.getName().toLowerCase();
        if (!name.contains(".")) {
            String ext = "txt";
            if (fc.getFileFilter() instanceof FileNameExtensionFilter)
                ext = ((FileNameExtensionFilter)fc.getFileFilter()).getExtensions()[0];
            f = new File(f.getParent(), f.getName() + "." + ext);
            name = f.getName().toLowerCase();
        }
        try {
            if (name.endsWith(".docx"))      writeDocx(f, text);
            else if (name.endsWith(".pdf"))  writePdf(f, text);
            else { try(Writer w=new OutputStreamWriter(new FileOutputStream(f),StandardCharsets.UTF_8)){w.write(text);} }
            JOptionPane.showMessageDialog(this, "Đã lưu: " + f.getAbsolutePath());
        } catch (Exception ex) { err("Không thể lưu file."); }
    }

    private String loadFile() {
        JFileChooser fc = new JFileChooser();
        fc.addChoosableFileFilter(new FileNameExtensionFilter("Text (*.txt)", "txt"));
        fc.addChoosableFileFilter(new FileNameExtensionFilter("Word (*.docx)", "docx"));
        if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) return null;
        File f = fc.getSelectedFile();
        try {
            if (f.getName().toLowerCase().endsWith(".docx")) return readDocx(f);
            try (BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(f), StandardCharsets.UTF_8))) {
                StringBuilder sb = new StringBuilder(); String line;
                while ((line = r.readLine()) != null) sb.append(line).append("\n");
                return sb.toString();
            }
        }catch (Exception ex) { err("Không thể đọc file."); return null ; }
}

    // ── Crypto helpers ────────────────────────────────────────────────────────
    private String decryptText(String cipherText, int p, int x) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        for (String line : cipherText.split("\n")) {
            line = line.trim();
            if (line.isEmpty()) continue;
            line = line.replace("(","").replace(")","");
            String[] parts = line.split(",");
            baos.write(ElGamal.decryptChar(Integer.parseInt(parts[0].trim()), Integer.parseInt(parts[1].trim()), p, x));
        }
        return new String(baos.toByteArray(), StandardCharsets.UTF_8);
    }

    private boolean isCurrentCipherModified() {
        return originalCipherText != null && !originalCipherText.equals(txtCipher.getText());
    }

    private boolean isCurrentKeyWrong() {
    if (originalPlainText == null || originalCipherText == null) {
        return false;
    }

    try {
        String decrypted = decryptText(
                originalCipherText,
                getP(),
                getPrivateKey());

        return !originalPlainText.trim()
                .equals(decrypted.trim());

    } catch (Exception e) {
        return true;
    }
}

    // ── DOCX writer ───────────────────────────────────────────────────────────
    private void writeDocx(File file, String text) throws IOException {
        try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(file))) {
            putEntry(zos, "[Content_Types].xml",
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
                "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">" +
                "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>" +
                "<Default Extension=\"xml\" ContentType=\"application/xml\"/>" +
                "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>" +
                "</Types>");
            putEntry(zos, "_rels/.rels",
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
                "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">" +
                "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>" +
                "</Relationships>");
            putEntry(zos, "word/_rels/document.xml.rels",
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
                "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"/>");
            StringBuilder doc = new StringBuilder(
                "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
                "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:body>");
            for (String line : text.split("\r?\n"))
                doc.append("<w:p><w:r><w:t>").append(xmlEsc(line)).append("</w:t></w:r></w:p>");
            doc.append("</w:body></w:document>");
            putEntry(zos, "word/document.xml", doc.toString());
        }
    }

    private void putEntry(ZipOutputStream zos, String name, String content) throws IOException {
        zos.putNextEntry(new ZipEntry(name));
        zos.write(content.getBytes(StandardCharsets.UTF_8));
        zos.closeEntry();
    }

    // ── PDF writer ────────────────────────────────────────────────────────────
    private void writePdf(File file, String text) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        baos.write("%PDF-1.4\n".getBytes(StandardCharsets.US_ASCII));
        int o1=baos.size(); baos.write("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n".getBytes(StandardCharsets.US_ASCII));
        int o2=baos.size(); baos.write("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n".getBytes(StandardCharsets.US_ASCII));
        int o3=baos.size(); baos.write("3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 5 0 R /Resources << /Font << /F1 4 0 R >> >> >>\nendobj\n".getBytes(StandardCharsets.US_ASCII));
        int o4=baos.size(); baos.write("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n".getBytes(StandardCharsets.US_ASCII));
        StringBuilder cb = new StringBuilder("BT\n/F1 12 Tf\n50 800 Td\n");
        String[] lines = text.split("\r?\n");
        for (int i=0;i<lines.length;i++){cb.append('(').append(pdfEsc(lines[i])).append(") Tj\n");if(i<lines.length-1)cb.append("0 -14 Td\n");}
        cb.append("ET\n");
        byte[] cb2=cb.toString().getBytes(StandardCharsets.US_ASCII);
        int o5=baos.size(); baos.write(("5 0 obj\n<< /Length "+cb2.length+" >>\nstream\n").getBytes(StandardCharsets.US_ASCII));
        baos.write(cb2); baos.write("endstream\nendobj\n".getBytes(StandardCharsets.US_ASCII));
        int xref=baos.size();
        StringBuilder xb=new StringBuilder("xref\n0 6\n0000000000 65535 f \n");
        for (int o:new int[]{o1,o2,o3,o4,o5}) xb.append(String.format("%010d 00000 n \n",o));
        baos.write(xb.toString().getBytes(StandardCharsets.US_ASCII));
        baos.write(("trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n"+xref+"\n%%EOF\n").getBytes(StandardCharsets.US_ASCII));
        try(OutputStream out=new FileOutputStream(file)){baos.writeTo(out);}
    }

    private String readDocx(File file) throws IOException {
        try (java.util.zip.ZipFile zip = new java.util.zip.ZipFile(file)) {
            java.util.zip.ZipEntry entry = zip.getEntry("word/document.xml");
            if (entry == null) return "";
            try (BufferedReader r = new BufferedReader(new InputStreamReader(zip.getInputStream(entry), StandardCharsets.UTF_8))) {
                StringBuilder sb = new StringBuilder(); String line;
                while ((line = r.readLine()) != null) sb.append(line).append("\n");
                return sb.toString().replaceAll("<.*?>","").replaceAll("&amp;","&").replaceAll("&lt;","<").replaceAll("&gt;",">").replaceAll("&quot;","\"").replaceAll("&apos;","'");
            }
        }
    }

    private String xmlEsc(String v){return v.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\"","&quot;").replace("'","&apos;");}
    private String pdfEsc(String s){StringBuilder b=new StringBuilder();for(char c:s.toCharArray()){if(c=='('||c==')'||c=='\\')b.append('\\').append(c);else if(c<32||c>126)b.append(String.format("\\%03o",(int)c));else b.append(c);}return b.toString();}

    // ── Entry point ───────────────────────────────────────────────────────────
    public static void main(String[] args) {
        try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); } catch (Exception ignored) {}
        SwingUtilities.invokeLater(() -> {
            ElgamalUI frame = new ElgamalUI();
            frame.initEvents();
            frame.setVisible(true);
        });
    }
}