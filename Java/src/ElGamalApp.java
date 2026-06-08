import javax.swing.*;
import javax.swing.border.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class ElGamalApp extends JFrame {

    // ===== BẢNG MÀU MODERN DARK =====
    static final Color BG_MAIN     = new Color(11, 15, 25);     // #0b0f19
    static final Color BG_PANEL    = new Color(21, 31, 50);     // #151f32
    static final Color BG_INPUT    = new Color(29, 41, 62);     // #1d293e
    static final Color ACCENT      = new Color(56, 189, 248);   // #38bdf8
    static final Color ACCENT_DARK = new Color(14, 165, 233);   // #0ea5e9
    static final Color SUCCESS     = new Color(34, 197, 94);    // #22c55e
    static final Color WARNING     = new Color(234, 179, 8);    // #eab308
    static final Color DANGER      = new Color(239, 68, 68);    // #ef4444
    static final Color TEXT_MAIN   = new Color(248, 250, 252);  // #f8fafc
    static final Color TEXT_DIM    = new Color(148, 163, 184);  // #94a3b8
    static final Color BORDER_CLR  = new Color(51, 65, 85);     // #334155
    static final Color BUTTON_SEC  = new Color(39, 55, 81);     // #273751
    static final Color BUTTON_SEC_HOVER = new Color(51, 71, 102); // #334766

    // SHARED STATE
    private int sharedP = 0, sharedG = 0, sharedX = 0, sharedY = 0;

    // LƯU TRỮ CHUỖI GỐC ĐỂ SO SÁNH CHÍNH XÁC (LOGIC THAY ĐỔI)
    private String originalCipher = "";
    private String originalP = "";
    private String originalX = "";

    public ElGamalApp() {
        setTitle("Mã hóa - Giải mã Elgamal");
        setSize(920, 740);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        getContentPane().setBackground(BG_MAIN);
        setLayout(new BorderLayout());

        UIManager.put("TabbedPane.selected",           BG_PANEL);
        UIManager.put("TabbedPane.background",         BG_MAIN);
        UIManager.put("TabbedPane.foreground",         TEXT_DIM);
        UIManager.put("TabbedPane.selectedForeground", ACCENT);
        UIManager.put("TabbedPane.contentAreaColor",   BG_MAIN);
        UIManager.put("TabbedPane.borderHighlightColor", BORDER_CLR);

//        JPanel header = buildHeader();
//        add(header, BorderLayout.NORTH);

        JTabbedPane tabs = new JTabbedPane();
        tabs.setBackground(BG_MAIN);
        tabs.setForeground(TEXT_MAIN);
        tabs.setFont(new Font("Segoe UI", Font.BOLD, 14));
        tabs.setBorder(BorderFactory.createEmptyBorder(10, 16, 16, 16));

        tabs.addTab("🔑  Sinh Khóa",   buildKeyTab());
        tabs.addTab("🔒  Mã Hóa",      buildEncryptTab());
        tabs.addTab("🔓  Giải Mã",     buildDecryptTab());

        add(tabs, BorderLayout.CENTER);
        setVisible(true);
    }

//    private JPanel buildHeader() {
//        JPanel p = new JPanel(new BorderLayout());
//        p.setBackground(BG_PANEL);
//        p.setBorder(BorderFactory.createEmptyBorder(16, 24, 16, 24));
//
//        JLabel title = new JLabel("ElGamal Cryptosystem");
//        title.setFont(new Font("Segoe UI", Font.BOLD, 22));
//        title.setForeground(TEXT_MAIN);
//
//        JLabel sub = new JLabel("Public-Key Encryption Demo  •  Java Swing Modern UI");
//        sub.setFont(new Font("Segoe UI", Font.PLAIN, 12));
//        sub.setForeground(TEXT_DIM);
//
//        JPanel left = new JPanel(new GridLayout(2, 1, 0, 4));
//        left.setOpaque(false);
//        left.add(title);
//        left.add(sub);
//        p.add(left, BorderLayout.WEST);
//
//        JPanel line = new JPanel();
//        line.setBackground(ACCENT);
//        line.setPreferredSize(new Dimension(0, 3));
//        p.add(line, BorderLayout.SOUTH);
//        return p;
//    }

    // =====================================================================
    //  TAB 1 – SINH KHÓA
    // =====================================================================
    private JPanel buildKeyTab() {
        JPanel root = darkPanel(new BorderLayout(0, 12));
        root.setBorder(BorderFactory.createEmptyBorder(16, 0, 0, 0));

        // Sử dụng GridLayout(1, 2) cho thân máy giúp tự động co dãn đều hai bên khi FullScreen
        JPanel bodyGrid = darkPanel(new GridLayout(1, 2, 20, 0));

        // --- CỘT TRÁI ---
        JPanel leftColumn = darkPanel(new GridLayout(2, 1, 0, 16));

        JPanel autoCard = card("Sinh Tự Động");
        autoCard.setLayout(new BorderLayout(0, 12));
        JLabel autoDesc = dimLabel("Tự động sinh số nguyên tố p, phần tử sinh g,<br>khóa bí mật x và khóa công khai y ngẫu nhiên.");
        autoCard.add(autoDesc, BorderLayout.CENTER);
        JButton btnAuto = accentButton("  Sinh Khóa Ngẫu Nhiên");
        autoCard.add(btnAuto, BorderLayout.SOUTH);
        leftColumn.add(autoCard);

        JPanel manCard = card("Nhập Thủ Công");
        manCard.setLayout(new GridBagLayout());
        GridBagConstraints gc = gbc();
        JTextField tfP = inputField("Số nguyên tố p");
        JTextField tfG = inputField("Phần tử sinh g");
        JTextField tfX = inputField("Khóa bí mật x");
        JTextField tfY = inputField("Khóa công khai y  (tự tính nếu để trống)");
        addRow(manCard, gc, "p :", tfP, 0);
        addRow(manCard, gc, "g :", tfG, 1);
        addRow(manCard, gc, "x :", tfX, 2);
        addRow(manCard, gc, "y :", tfY, 3);
        JButton btnManual = accentButton("  Xác Nhận Khóa");
        gc.gridx = 0; gc.gridy = 4; gc.gridwidth = 2; gc.insets = new Insets(14, 0, 0, 0);
        manCard.add(btnManual, gc);
        leftColumn.add(manCard);

        // --- CỘT PHẢI ---
        JPanel rightColumn = darkPanel(new BorderLayout(0, 16));

        JPanel dispCard = card("Khóa Hiện Tại Hệ Thống");
        dispCard.setLayout(new GridLayout(5, 1, 0, 8));
        JLabel lblP = keyLabel("p", "—");
        JLabel lblG = keyLabel("g", "—");
        JLabel lblX = keyLabel("x  (bí mật)", "—");
        JLabel lblY = keyLabel("y  (công khai)", "—");
        JLabel lblStatus = new JLabel("   Chưa có khóa hợp lệ");
        lblStatus.setForeground(DANGER);
        lblStatus.setFont(new Font("Segoe UI", Font.ITALIC | Font.BOLD, 12));
        dispCard.add(lblP); dispCard.add(lblG); dispCard.add(lblX); dispCard.add(lblY); dispCard.add(lblStatus);

        JPanel saveCard = card("Lưu Khóa Ra File");
        saveCard.setLayout(new GridLayout(2, 1, 0, 8));
        JButton btnSavePub  = secondaryButton("  Lưu Khóa Công Khai  (p, g, y)");
        JButton btnSavePriv = secondaryButton("  Lưu Khóa Bí Mật  (p, g, x, y)");
        saveCard.add(btnSavePub); saveCard.add(btnSavePriv);
        rightColumn.add(dispCard, BorderLayout.CENTER);
        rightColumn.add(saveCard, BorderLayout.SOUTH);

        // Thêm cột trái và phải vào lưới đồng bộ
        bodyGrid.add(leftColumn);
        bodyGrid.add(rightColumn);
        root.add(bodyGrid, BorderLayout.CENTER);

        JLabel statusBar = statusLabel("Sẵn sàng");
        root.add(statusBar, BorderLayout.SOUTH);

        Runnable refreshDisplay = () -> {
            if (sharedP == 0) {
                setText(lblP, "p", "—"); setText(lblG, "g", "—");
                setText(lblX, "x (bí mật)", "—"); setText(lblY, "y (công khai)", "—");
                lblStatus.setText("   Chưa có khóa hợp lệ"); lblStatus.setForeground(DANGER);
            } else {
                setText(lblP, "p", String.valueOf(sharedP));
                setText(lblG, "g", String.valueOf(sharedG));
                setText(lblX, "x (bí mật)", String.valueOf(sharedX));
                setText(lblY, "y (công khai)", String.valueOf(sharedY));
                lblStatus.setText("   Khóa hoạt động hợp lệ"); lblStatus.setForeground(SUCCESS);
            }
        };

        btnAuto.addActionListener(e -> {
            int[] keys = ElGamal.generateKey();
            sharedP = keys[0]; sharedG = keys[1]; sharedX = keys[2]; sharedY = keys[3];
            refreshDisplay.run();
            statusBar.setText("Đã sinh khóa ngẫu nhiên thành công."); statusBar.setForeground(SUCCESS);
        });

        btnManual.addActionListener(e -> {
            try {
                int p = Integer.parseInt(tfP.getText().trim());
                int g = Integer.parseInt(tfG.getText().trim());
                int x = Integer.parseInt(tfX.getText().trim());
                if (!ElGamal.isPrime(p)) throw new Exception("p không phải số nguyên tố!");
                if (!ElGamal.isGenerator(g, p)) throw new Exception("g không phải phần tử sinh của p!");
                if (x < 2 || x >= p - 1) throw new Exception("x phải nằm trong khoảng [2, p-2]!");
                int y = tfY.getText().trim().isEmpty() ? (int) ElGamal.modPow(g, x, p) : Integer.parseInt(tfY.getText().trim());
                if (y != (int) ElGamal.modPow(g, x, p)) throw new Exception("y không khớp với g^x mod p!");
                sharedP = p; sharedG = g; sharedX = x; sharedY = y;
                refreshDisplay.run();
                statusBar.setText("Khóa thủ công cấu hình thành công "); statusBar.setForeground(SUCCESS);
            } catch (Exception ex) {
                statusBar.setText("Lỗi: " + ex.getMessage()); statusBar.setForeground(DANGER);
                JOptionPane.showMessageDialog(root, ex.getMessage(), "Lỗi cấu hình khóa", JOptionPane.ERROR_MESSAGE);
            }
        });

        btnSavePub.addActionListener(e -> saveKeyFile(root, false, statusBar));
        btnSavePriv.addActionListener(e -> saveKeyFile(root, true, statusBar));

        return root;
    }

    private void saveKeyFile(JComponent parent, boolean includePrivate, JLabel status) {
        if (sharedP == 0) {
            JOptionPane.showMessageDialog(parent, "Chưa có khóa hoạt động để xuất file!", "Thông báo", JOptionPane.WARNING_MESSAGE);
            return;
        }
        JFileChooser fc = fileChooser(includePrivate ? "private_key.txt" : "public_key.txt");
        if (fc.showSaveDialog(parent) != JFileChooser.APPROVE_OPTION) return;
        try (PrintWriter pw = new PrintWriter(fc.getSelectedFile())) {
            pw.println("# ElGamal Key File");
            pw.println("p=" + sharedP); pw.println("g=" + sharedG); pw.println("y=" + sharedY);
            if (includePrivate) pw.println("x=" + sharedX);
            status.setText("Đã lưu tệp: " + fc.getSelectedFile().getName()); status.setForeground(SUCCESS);
        } catch (IOException ex) {
            status.setText("Lỗi ghi tập tin!"); status.setForeground(DANGER);
        }
    }

    // =====================================================================
    //  TAB 2 – MÃ HÓA
    // =====================================================================
    private JPanel buildEncryptTab() {
        JPanel root = darkPanel(new BorderLayout(0, 12));
        root.setBorder(BorderFactory.createEmptyBorder(10, 0, 0, 0));

        JPanel keyInfo = card("Cấu Hình Khóa Công Khai Để Mã Hóa");
        keyInfo.setLayout(new GridBagLayout());
        GridBagConstraints kgc = gbc();
        JTextField encP = inputField("Nhập p");
        JTextField encG = inputField("Nhập g");
        JTextField encY = inputField("Nhập y");
        JTextField encK = inputField("Số k (để trống nếu muốn tự động sinh ngẫu nhiên)");

        kgc.weightx = 0.2; kgc.gridy = 0;
//        kgc.gridx = 0; keyInfo.add(new JLabel("  p:"), kgc); kgc.gridx = 1; keyInfo.add(encP, kgc);
//        kgc.gridx = 2; keyInfo.add(new JLabel("  g:"), kgc); kgc.gridx = 3; keyInfo.add(encG, kgc);
//        kgc.gridx = 4; keyInfo.add(new JLabel("  y:"), kgc); kgc.gridx = 5; keyInfo.add(encY, kgc);
//        kgc.gridx = 6; keyInfo.add(new JLabel("  k:"), kgc); kgc.gridx = 7; keyInfo.add(encK, kgc);
        kgc.gridx = 0; keyInfo.add(whiteLabel("  p:"), kgc);  kgc.gridx = 1; keyInfo.add(encP, kgc);
        kgc.gridx = 2; keyInfo.add(whiteLabel("  g:"), kgc);  kgc.gridx = 3; keyInfo.add(encG, kgc);
        kgc.gridx = 4; keyInfo.add(whiteLabel("  y:"), kgc);  kgc.gridx = 5; keyInfo.add(encY, kgc);
        kgc.gridx = 6; keyInfo.add(whiteLabel("  k:"), kgc);  kgc.gridx = 7; keyInfo.add(encK, kgc);

        JPanel keyActionPanel = darkPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        JButton btnLoadEncKey = secondaryButton("  Nạp Khóa Từ File");
        JButton btnUseSharedKey = secondaryButton("  Dùng Khóa Vừa Sinh Ở Tab 1");
        keyActionPanel.add(btnLoadEncKey); keyActionPanel.add(btnUseSharedKey);
        kgc.gridx = 0; kgc.gridy = 1; kgc.gridwidth = 8; kgc.insets = new Insets(10, 0, 0, 0);
        keyInfo.add(keyActionPanel, kgc);
        root.add(keyInfo, BorderLayout.NORTH);

        JPanel center = darkPanel(new GridLayout(1, 2, 16, 0));
        JPanel inCard = card("Văn Bản Gốc (Plaintext)");
        inCard.setLayout(new BorderLayout(0, 8));
        JTextArea taPlain = textArea();
        inCard.add(scrollWrap(taPlain), BorderLayout.CENTER);

        JPanel inBtns = darkPanel(new GridLayout(1, 2, 8, 0));
        JButton btnLoadText = secondaryButton("  Mở Tệp Văn Bản");
        JButton btnSaveText = secondaryButton("  Lưu Văn Bản Gốc");
        inBtns.add(btnLoadText); inBtns.add(btnSaveText);
        inCard.add(inBtns, BorderLayout.SOUTH);

        JPanel outCard = card("Văn Văn Bản Sau Mã Hóa (Ciphertext)");
        outCard.setLayout(new BorderLayout(0, 8));
        JTextArea taCipher = textArea(); taCipher.setEditable(false);
        outCard.add(scrollWrap(taCipher), BorderLayout.CENTER);
        JButton btnSaveCipher = secondaryButton("  Lưu Tệp Bản Mã (.txt)");
        outCard.add(btnSaveCipher, BorderLayout.SOUTH);

        center.add(inCard); center.add(outCard);
        root.add(center, BorderLayout.CENTER);

        JPanel bottom = darkPanel(new BorderLayout(12, 0));
        JButton btnEncrypt = accentButton("  Thực Hiện Mã Hóa");
        btnEncrypt.setPreferredSize(new Dimension(180, 42));
        JLabel statusBar = statusLabel("Sẵn sàng hành động");
        bottom.add(btnEncrypt, BorderLayout.WEST);
        bottom.add(statusBar, BorderLayout.CENTER);
        root.add(bottom, BorderLayout.SOUTH);

        btnUseSharedKey.addActionListener(e -> {
            if (sharedP == 0) {
                JOptionPane.showMessageDialog(root, "Tab 1 chưa có cấu hình khóa nào!", "Thông báo", JOptionPane.WARNING_MESSAGE);
                return;
            }
            encP.setText(String.valueOf(sharedP)); encG.setText(String.valueOf(sharedG)); encY.setText(String.valueOf(sharedY));
            statusBar.setText("Đã đồng bộ bộ khóa từ Tab 1."); statusBar.setForeground(SUCCESS);
        });

        btnLoadEncKey.addActionListener(e -> {
            JFileChooser fc = fileChooser(null);
            if (fc.showOpenDialog(root) != JFileChooser.APPROVE_OPTION) return;
            try {
                Map<String, String> map = readKeyFromFile(fc.getSelectedFile());
                if (map.containsKey("p")) encP.setText(map.get("p"));
                if (map.containsKey("g")) encG.setText(map.get("g"));
                if (map.containsKey("y")) encY.setText(map.get("y"));
                statusBar.setText("Đã nạp thành công thông số khóa từ file: " + fc.getSelectedFile().getName());
                statusBar.setForeground(SUCCESS);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(root, "File khóa không đúng định dạng!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        });

        btnLoadText.addActionListener(e -> {
            JFileChooser fc = fileChooser(null);
            if (fc.showOpenDialog(root) != JFileChooser.APPROVE_OPTION) return;
            try {
                taPlain.setText(Files.readString(fc.getSelectedFile().toPath()));
                statusBar.setText("Đã nạp file gốc: " + fc.getSelectedFile().getName()); statusBar.setForeground(SUCCESS);
            } catch (IOException ex) {
                statusBar.setText("Lỗi đọc file dữ liệu!"); statusBar.setForeground(DANGER);
            }
        });

        btnSaveText.addActionListener(e -> saveText(root, taPlain.getText(), "plaintext.txt", statusBar));

        btnEncrypt.addActionListener(e -> {
            try {
                int p = Integer.parseInt(encP.getText().trim());
                int g = Integer.parseInt(encG.getText().trim());
                int y = Integer.parseInt(encY.getText().trim());
                String plain = taPlain.getText();

                if (plain.isEmpty()) throw new Exception("Văn bản gốc đang trống!");

                int k;
                if (encK.getText().trim().isEmpty()) {
                    k = new Random().nextInt(p - 3) + 2;
                    encK.setText(String.valueOf(k));
                } else {
                    k = Integer.parseInt(encK.getText().trim());
                }

                StringBuilder sb = new StringBuilder();
                for (char c : plain.toCharArray()) {
                    int[] pair = ElGamal.encryptChar(c, p, g, y, k);
                    sb.append(pair[0]).append(",").append(pair[1]).append("\n");
                }
                taCipher.setText(sb.toString().trim());
                statusBar.setText("Mã hóa hoàn tất! Số ký tự: " + plain.length() + " (k=" + k + ")");
                statusBar.setForeground(SUCCESS);
            } catch (Exception ex) {
                statusBar.setText("Thất bại: " + ex.getMessage()); statusBar.setForeground(DANGER);
                JOptionPane.showMessageDialog(root, ex.getMessage(), "Lỗi mã hóa", JOptionPane.ERROR_MESSAGE);
            }
        });

        btnSaveCipher.addActionListener(e -> saveText(root, taCipher.getText(), "ciphertext.txt", statusBar));

        return root;
    }

    // =====================================================================
    //  TAB 3 – GIẢI MÃ (ĐÃ ĐỔI SANG LOGIC SO SÁNH CHUỖI GỐC CHUẨN XÁC)
    // =====================================================================
    private JPanel buildDecryptTab() {
        JPanel root = darkPanel(new BorderLayout(0, 12));
        root.setBorder(BorderFactory.createEmptyBorder(10, 0, 0, 0));

        JPanel topRow = darkPanel(new GridBagLayout());
        GridBagConstraints tgc = gbc();

        JPanel keyCard = card("Thông Số Bộ Khóa Giải Mã");
        keyCard.setLayout(new GridBagLayout());
        GridBagConstraints kgc = gbc();
        JTextField decP = inputField("Nhập p");
        JTextField decX = inputField("Nhập x (bí mật)");
//        kgc.weightx = 0.1; kgc.gridx = 0; keyCard.add(new JLabel("p:"), kgc);
//        kgc.weightx = 0.4; kgc.gridx = 1; keyCard.add(decP, kgc);
//        kgc.weightx = 0.1; kgc.gridx = 2; keyCard.add(new JLabel("x:"), kgc);
//        kgc.weightx = 0.4; kgc.gridx = 3; keyCard.add(decX, kgc);
        kgc.weightx = 0.1; kgc.gridx = 0; keyCard.add(whiteLabel("p:"), kgc);
        kgc.weightx = 0.4; kgc.gridx = 1; keyCard.add(decP, kgc);
        kgc.weightx = 0.1; kgc.gridx = 2; keyCard.add(whiteLabel("x:"), kgc);
        kgc.weightx = 0.4; kgc.gridx = 3; keyCard.add(decX, kgc);

        JButton btnLoadKeyFile = secondaryButton("  Nạp Khóa Từ File");
        kgc.gridx = 0; kgc.gridy = 1; kgc.gridwidth = 4; kgc.insets = new Insets(8, 0, 0, 0);
        keyCard.add(btnLoadKeyFile, kgc);

        tgc.weightx = 0.5; tgc.gridx = 0; tgc.gridy = 0; topRow.add(keyCard, tgc);

        JPanel cipherCtrlCard = card("Quản Lý File Bản Mã");
        cipherCtrlCard.setLayout(new BorderLayout(0, 12));
        JLabel lblCipherFile = dimLabel("Chưa chọn tệp mã hóa đầu vào nào");
        JButton btnLoadCipher = accentButton("  Chọn & Đọc File Bản Mã");
        cipherCtrlCard.add(lblCipherFile, BorderLayout.CENTER);
        cipherCtrlCard.add(btnLoadCipher, BorderLayout.SOUTH);

        tgc.gridx = 1; topRow.add(cipherCtrlCard, tgc);
        root.add(topRow, BorderLayout.NORTH);

        JPanel center = darkPanel(new GridLayout(1, 2, 16, 0));

        JPanel previewCard = card("Nội Dung Bản Mã Thiết Lập (Có thể chỉnh sửa trực tiếp)");
        previewCard.setLayout(new BorderLayout());
        JTextArea taCipher = textArea(); taCipher.setEditable(true);
        previewCard.add(scrollWrap(taCipher), BorderLayout.CENTER);

        JPanel plainCard = card("Văn Bản Gốc Sau Giải Mã");
        plainCard.setLayout(new BorderLayout(0, 8));
        JTextArea taPlain = textArea(); taPlain.setEditable(false);
        plainCard.add(scrollWrap(taPlain), BorderLayout.CENTER);
        JButton btnSavePlain = secondaryButton("  Xuất Kết Quả Giải Mã Ra File");
        plainCard.add(btnSavePlain, BorderLayout.SOUTH);

        center.add(previewCard); center.add(plainCard);
        root.add(center, BorderLayout.CENTER);

        JPanel bottom = darkPanel(new BorderLayout(12, 0));
        JButton btnDecrypt = accentButton("  Bắt Đầu Giải Mã");
        btnDecrypt.setPreferredSize(new Dimension(180, 42));
        JLabel statusBar = statusLabel("Đang chờ dữ liệu đầu vào");
        bottom.add(btnDecrypt, BorderLayout.WEST);
        bottom.add(statusBar, BorderLayout.CENTER);
        root.add(bottom, BorderLayout.SOUTH);

        // BỘ LẮNG NGHE KIỂM TRA ĐỘNG ĐỂ ĐỔI MÀU STATUS BAR NHANH (XEM TRỰC QUAN)
        Runnable checkRealtimeChanges = () -> {
            String currentCipher = taCipher.getText();
            String currentP = decP.getText().trim();
            String currentX = decX.getText().trim();

            boolean cipherDiff = !currentCipher.equals(originalCipher);
            boolean keyDiff = !currentP.equals(originalP) || !currentX.equals(originalX);

            if (cipherDiff && keyDiff) {
                statusBar.setText("⚠️ Khóa và Bản mã đã bị thay đổi so với file gốc!");
                statusBar.setForeground(WARNING);
            } else if (cipherDiff) {
                statusBar.setText("⚠️ Bản mã đã bị thay đổi so với file gốc!");
                statusBar.setForeground(WARNING);
            } else if (keyDiff) {
                statusBar.setText("⚠️ Cấu hình khóa đã bị thay đổi so với file gốc!");
                statusBar.setForeground(WARNING);
            } else {
                statusBar.setText(" Dữ liệu hiện tại khớp hoàn toàn với file gốc.");
                statusBar.setForeground(SUCCESS);
            }
        };

        DocumentListener dynamicListener = new DocumentListener() {
            public void insertUpdate(DocumentEvent e) { checkRealtimeChanges.run(); }
            public void removeUpdate(DocumentEvent e) { checkRealtimeChanges.run(); }
            public void changedUpdate(DocumentEvent e) { checkRealtimeChanges.run(); }
        };

        taCipher.getDocument().addDocumentListener(dynamicListener);
        decP.getDocument().addDocumentListener(dynamicListener);
        decX.getDocument().addDocumentListener(dynamicListener);

        btnLoadCipher.addActionListener(e -> {
            taCipher.getDocument().removeDocumentListener(dynamicListener);
            JFileChooser fc = fileChooser(null);
            if (fc.showOpenDialog(root) != JFileChooser.APPROVE_OPTION) {
                taCipher.getDocument().addDocumentListener(dynamicListener);
                return;
            }
            try {
                String content = Files.readString(fc.getSelectedFile().toPath());
                taCipher.setText(content);
                originalCipher = content; // Cập nhật chuỗi gốc mốc so sánh

                lblCipherFile.setText("  " + fc.getSelectedFile().getName());
                lblCipherFile.setForeground(SUCCESS);
                checkRealtimeChanges.run();
            } catch (IOException ex) {
                statusBar.setText("Lỗi đọc file bản mã!"); statusBar.setForeground(DANGER);
            }
            taCipher.getDocument().addDocumentListener(dynamicListener);
        });

        btnLoadKeyFile.addActionListener(e -> {
            decP.getDocument().removeDocumentListener(dynamicListener);
            decX.getDocument().removeDocumentListener(dynamicListener);
            JFileChooser fc = fileChooser(null);
            if (fc.showOpenDialog(root) != JFileChooser.APPROVE_OPTION) {
                decP.getDocument().addDocumentListener(dynamicListener);
                decX.getDocument().addDocumentListener(dynamicListener);
                return;
            }
            try {
                Map<String, String> map = readKeyFromFile(fc.getSelectedFile());
                if (!map.containsKey("x")) throw new Exception("File không chứa khóa bí mật x để giải mã!");

                if (map.containsKey("p")) {
                    decP.setText(map.get("p"));
                    originalP = map.get("p").trim(); // Ghi nhận mốc so sánh gốc
                }
                if (map.containsKey("x")) {
                    decX.setText(map.get("x"));
                    originalX = map.get("x").trim(); // Ghi nhận mốc so sánh gốc
                }
                checkRealtimeChanges.run();
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(root, ex.getMessage(), "Lỗi file khóa", JOptionPane.ERROR_MESSAGE);
            }
            decP.getDocument().addDocumentListener(dynamicListener);
            decX.getDocument().addDocumentListener(dynamicListener);
        });

        btnDecrypt.addActionListener(e -> {
            // =================================================================
            // LOGIC SO SÁNH GIÁ TRỊ THỰC TẾ ĐỂ BẬT CỬA SỔ DIALOG (XỬ LÝ CHÍNH)
            // =================================================================
            String currentCipher = taCipher.getText();
            String currentP = decP.getText().trim();
            String currentX = decX.getText().trim();

            boolean cipherDiff = !currentCipher.equals(originalCipher);
            boolean keyDiff = !currentP.equals(originalP) || !currentX.equals(originalX);

            if (cipherDiff && keyDiff) {
                JOptionPane.showMessageDialog(root,
                        "Khóa và bản mã đã bị thay đổi!\nHệ thống sẽ từ chối thực hiện giải mã.",
                        "Cảnh Báo Thay Đổi", JOptionPane.WARNING_MESSAGE);
                return;
            } else if (cipherDiff) {
                JOptionPane.showMessageDialog(root,
                        "Bản mã đã bị thay đổi!\nHệ thống sẽ từ chối thực hiện giải mã.",
                        "Cảnh Báo Thay Đổi", JOptionPane.WARNING_MESSAGE);
                return;
            } else if (keyDiff) {
                JOptionPane.showMessageDialog(root,
                        "Khóa đã bị thay đổi!\nHệ thống sẽ từ chối thực hiện giải mã.",
                        "Cảnh Báo Thay Đổi", JOptionPane.WARNING_MESSAGE);
                return;
            }

            if (currentCipher.trim().isEmpty()) {
                JOptionPane.showMessageDialog(root, "Nội dung bản mã trống!", "Thiếu dữ liệu", JOptionPane.WARNING_MESSAGE);
                return;
            }
            try {
                int p = Integer.parseInt(currentP);
                int x = Integer.parseInt(currentX);

                java.util.List<String[]> pairs = new ArrayList<>();
                for (String line : currentCipher.split("\n")) {
                    line = line.trim();
                    if (line.isEmpty() || line.startsWith("#")) continue;
                    String[] parts = line.split(",");
                    if (parts.length == 2) pairs.add(parts);
                }

                if (pairs.isEmpty()) throw new Exception("Không tìm thấy dữ liệu cặp tọa độ mã hóa hợp lệ (dạng c1,c2)!");

                StringBuilder sb = new StringBuilder();
                for (String[] pair : pairs) {
                    int c1 = Integer.parseInt(pair[0].trim());
                    int c2 = Integer.parseInt(pair[1].trim());
                    int m = ElGamal.decryptChar(c1, c2, p, x);
                    sb.append((char) m);
                }

                taPlain.setText(sb.toString());
                statusBar.setText("Giải mã dữ liệu hoàn tất thành công! ");
                statusBar.setForeground(SUCCESS);
            } catch (Exception ex) {
                statusBar.setText("Giải mã thất bại: " + ex.getMessage()); statusBar.setForeground(DANGER);
                JOptionPane.showMessageDialog(root, "Lỗi dữ liệu hoặc sai thông số khóa!\nChi tiết: " + ex.getMessage(), "Lỗi Giải Mã", JOptionPane.ERROR_MESSAGE);
            }
        });

        btnSavePlain.addActionListener(e -> saveText(root, taPlain.getText(), "plaintext_decrypted.txt", statusBar));

        return root;
    }

    private Map<String, String> readKeyFromFile(File file) throws IOException {
        Map<String, String> map = new HashMap<>();
        for (String line : Files.readAllLines(file.toPath())) {
            line = line.trim();
            if (line.startsWith("#") || !line.contains("=")) continue;
            String[] kv = line.split("=", 2);
            map.put(kv[0].trim(), kv[1].trim());
        }
        return map;
    }

    private void saveText(JComponent parent, String text, String defaultName, JLabel status) {
        if (text == null || text.trim().isEmpty()) {
            JOptionPane.showMessageDialog(parent, "Không tìm thấy nội dung để xuất file!", "Thông báo", JOptionPane.WARNING_MESSAGE);
            return;
        }
        JFileChooser fc = fileChooser(defaultName);
        if (fc.showSaveDialog(parent) != JFileChooser.APPROVE_OPTION) return;
        try {
            Files.writeString(fc.getSelectedFile().toPath(), text);
            status.setText("Xuất file thành công: " + fc.getSelectedFile().getName()); status.setForeground(SUCCESS);
        } catch (IOException ex) {
            status.setText("Xảy ra lỗi khi lưu tệp!"); status.setForeground(DANGER);
        }
    }

    private JFileChooser fileChooser(String defaultName) {
        JFileChooser fc = new JFileChooser();
        fc.setFileFilter(new FileNameExtensionFilter("Text files (*.txt)", "txt"));
        if (defaultName != null) fc.setSelectedFile(new File(defaultName));
        return fc;
    }

    private JPanel darkPanel(LayoutManager lm) {
        JPanel p = new JPanel(lm); p.setBackground(BG_MAIN); p.setOpaque(true); return p;
    }

    private JPanel card(String title) {
        JPanel p = new JPanel(); p.setBackground(BG_PANEL);
        p.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(BORDER_CLR, 1, true),
                BorderFactory.createTitledBorder(BorderFactory.createEmptyBorder(8, 12, 12, 12),
                        "  " + title, TitledBorder.LEFT, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 13), ACCENT)
        ));
        return p;
    }

    private JButton accentButton(String txt) {
        JButton b = new JButton(txt); b.setBackground(ACCENT); b.setForeground(BG_MAIN);
        b.setFont(new Font("Segoe UI", Font.BOLD, 13)); b.setFocusPainted(false);
        b.setContentAreaFilled(false); b.setOpaque(true);
        b.setBorder(BorderFactory.createEmptyBorder(10, 16, 10, 16));
        b.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        b.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) { b.setBackground(ACCENT_DARK); b.setForeground(Color.WHITE); }
            public void mouseExited(MouseEvent e)  { b.setBackground(ACCENT); b.setForeground(BG_MAIN); }
        });
        return b;
    }

    private JButton secondaryButton(String txt) {
        JButton b = new JButton(txt); b.setBackground(BUTTON_SEC); b.setForeground(TEXT_MAIN);
        b.setFont(new Font("Segoe UI", Font.PLAIN, 12)); b.setFocusPainted(false);
        b.setContentAreaFilled(false); b.setOpaque(true);
        b.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLineBorder(BORDER_CLR), BorderFactory.createEmptyBorder(8, 12, 8, 12)));
        b.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        b.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) { b.setBackground(BUTTON_SEC_HOVER); }
            public void mouseExited(MouseEvent e)  { b.setBackground(BUTTON_SEC); }
        });
        return b;
    }

    private JTextField inputField(String placeholder) {
        JTextField tf = new JTextField(); tf.setBackground(BG_INPUT); tf.setForeground(TEXT_MAIN);
        tf.setCaretColor(TEXT_MAIN); tf.setFont(new Font("Segoe UI Mono", Font.BOLD, 14));
        tf.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLineBorder(BORDER_CLR), BorderFactory.createEmptyBorder(6, 10, 6, 10)));
        tf.setToolTipText(placeholder); return tf;
    }

    private JTextArea textArea() {
        JTextArea ta = new JTextArea(); ta.setBackground(BG_INPUT); ta.setForeground(TEXT_MAIN);
        ta.setCaretColor(TEXT_MAIN); ta.setFont(new Font("Segoe UI Mono", Font.PLAIN, 13));
        ta.setLineWrap(true); ta.setWrapStyleWord(true);
        ta.setBorder(BorderFactory.createEmptyBorder(8, 10, 8, 10)); return ta;
    }

    private JScrollPane scrollWrap(JComponent c) {
        JScrollPane sp = new JScrollPane(c); sp.setBorder(BorderFactory.createLineBorder(BORDER_CLR));
        sp.getViewport().setBackground(BG_INPUT); return sp;
    }

    private JLabel dimLabel(String txt) {
        JLabel l = new JLabel("<html>" + txt.replace("\n", "<br>") + "</html>");
        l.setForeground(TEXT_DIM); l.setFont(new Font("Segoe UI", Font.PLAIN, 12)); return l;
    }

    private JLabel keyLabel(String k, String v) {
        JLabel l = new JLabel(); setText(l, k, v);
        l.setFont(new Font("Segoe UI Mono", Font.PLAIN, 14));
        l.setBorder(BorderFactory.createEmptyBorder(2, 4, 2, 4)); return l;
    }

//    private void setText(JLabel l, String k, String v) {
//        l.setText(String.format("<html><span style='color:#94a3b8'>%s:</span> &nbsp; <b style='color:#38bdf8'>%s</b></html>", k, v));
//    }

    private void setText(JLabel l, String k, String v) {
        l.setText(String.format("<html><span style='color:#ffffff'>%s:</span> &nbsp; <b style='color:#ffffff'>%s</b></html>", k, v));
    }

    // THÊM MỚI: Hàm helper giúp tạo nhãn chữ màu trắng sáng đồng bộ cho Tab 2 và Tab 3
    private JLabel whiteLabel(String txt) {
        JLabel l = new JLabel(txt);
        l.setForeground(TEXT_MAIN);
        l.setFont(new Font("Segoe UI", Font.BOLD, 13));
        return l;
    }

    private JLabel statusLabel(String txt) {
        JLabel l = new JLabel("  " + txt); l.setFont(new Font("Segoe UI", Font.BOLD, 12));
        l.setForeground(TEXT_DIM); l.setBorder(BorderFactory.createEmptyBorder(8, 0, 0, 0)); return l;
    }

    private GridBagConstraints gbc() {
        GridBagConstraints gc = new GridBagConstraints(); gc.fill = GridBagConstraints.HORIZONTAL; gc.insets = new Insets(6, 4, 6, 4); return gc;
    }

    private void addRow(JPanel p, GridBagConstraints gc, String label, JTextField field, int row) {
        JLabel lbl = new JLabel(label); lbl.setForeground(TEXT_MAIN); lbl.setFont(new Font("Segoe UI", Font.BOLD, 13));
        gc.gridx = 0; gc.gridy = row; gc.weightx = 0.2; gc.gridwidth = 1; p.add(lbl, gc);
        gc.gridx = 1; gc.weightx = 0.8; p.add(field, gc);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(ElGamalApp::new);
    }
}
