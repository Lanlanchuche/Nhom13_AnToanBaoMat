import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.util.Random;

public class ElGamalFrame extends JFrame {

    private JTextField txtP;
    private JTextField txtG;
    private JTextField txtX;
    private JTextField txtY;
    private JTextField txtK;

    private JTextArea txtPlain;
    private JTextArea txtC1;
    private JTextArea txtC2;
    private JTextArea txtCipher;
    private JTextArea txtDecrypt;

    private JButton btnGenerate;
    private JButton btnEncrypt;
    private JButton btnDecrypt;
    private JButton btnClear;
    private JButton btnExit;

    private JRadioButton rdAuto;
    private JRadioButton rdManual;

    public ElGamalFrame() {

        setTitle("Mã hóa ElGamal");
        setSize(1300, 700);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        initUI();
    }

    private void initUI() {

        setLayout(new BorderLayout());

        // PANEL KHÓA
        JPanel keyPanel = new JPanel();
        keyPanel.setBorder(BorderFactory.createTitledBorder("Tạo khóa"));
        keyPanel.setLayout(new GridLayout(7, 2, 5, 5));

        rdAuto = new JRadioButton("Tự sinh khóa", true);
        rdManual = new JRadioButton("Nhập khóa");

        ButtonGroup group = new ButtonGroup();
        group.add(rdAuto);
        group.add(rdManual);

        txtP = new JTextField();
        txtG = new JTextField();
        txtX = new JTextField();
        txtY = new JTextField();
        txtK = new JTextField();

        txtY.setEditable(false);

        keyPanel.add(rdAuto);
        keyPanel.add(rdManual);

        keyPanel.add(new JLabel("p (số nguyên tố)"));
        keyPanel.add(txtP);

        keyPanel.add(new JLabel("a (phần tử sinh)"));
        keyPanel.add(txtG);

        keyPanel.add(new JLabel("x (khóa bí mật)"));
        keyPanel.add(txtX);

        keyPanel.add(new JLabel("d = g^x mod p"));
        keyPanel.add(txtY);

        keyPanel.add(new JLabel("k"));
        keyPanel.add(txtK);

        btnGenerate = new JButton("Tạo khóa");

        keyPanel.add(btnGenerate);


        // CENTER PANEL
        JPanel centerPanel = new JPanel(new GridLayout(1, 5, 5, 5));

        txtPlain = new JTextArea();
        txtC1 = new JTextArea();
        txtC2 = new JTextArea();
        txtCipher = new JTextArea();
        txtDecrypt = new JTextArea();

        centerPanel.add(createAreaPanel("Bản rõ", txtPlain));

        centerPanel.add(createAreaPanel("C1 = a^k mod p", txtC1));

        centerPanel.add(createAreaPanel("C2 = M × d^k mod p", txtC2));

        centerPanel.add(createAreaPanel("Bản mã", txtCipher));

        centerPanel.add(createAreaPanel("Giải mã", txtDecrypt));


        // BUTTON PANEL
        JPanel buttonPanel = new JPanel();

        btnEncrypt = new JButton("Mã hóa");
        btnDecrypt = new JButton("Giải mã");
        btnClear = new JButton("Xóa");
        btnExit = new JButton("Thoát");

        buttonPanel.add(btnEncrypt);
        buttonPanel.add(btnDecrypt);
        buttonPanel.add(btnClear);
        buttonPanel.add(btnExit);

        add(keyPanel, BorderLayout.NORTH);
        add(centerPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);

        initEvent();

        rdAuto.doClick();
    }

    private JPanel createAreaPanel(String title, JTextArea area) {

        JPanel panel = new JPanel(new BorderLayout());

        panel.setBorder(BorderFactory.createTitledBorder(title));

        panel.add(new JScrollPane(area));

        return panel;
    }

    private void initEvent() {

        rdAuto.addActionListener(e -> {

            txtP.setEditable(false);
            txtG.setEditable(false);
            txtX.setEditable(false);

        });

        rdManual.addActionListener(e -> {

            txtP.setEditable(true);
            txtG.setEditable(true);
            txtX.setEditable(true);

        });


        // TẠO KHÓA
        btnGenerate.addActionListener(e -> {

            try {

                if (rdAuto.isSelected()) {

                    int[] key = ElGamal.generateKey();

                    txtP.setText(String.valueOf(key[0]));

                    txtG.setText(String.valueOf(key[1]));

                    txtX.setText(String.valueOf(key[2]));

                    txtY.setText(String.valueOf(key[3]));

                    Random rd = new Random();

                    int p = key[0];

                    int k;

                    do {
                        k = rd.nextInt(p - 3) + 2;
                    }
                    while (!ElGamal.gcdEqualsOne(k, p - 1));

                    txtK.setText(String.valueOf(k));

                } else {

                    int p = Integer.parseInt(txtP.getText());

                    int g = Integer.parseInt(txtG.getText());

                    int x = Integer.parseInt(txtX.getText());

                    if (!ElGamal.isPrime(p)) {

                        JOptionPane.showMessageDialog(this, "p phải là số nguyên tố");

                        return;
                    }

                    if (!ElGamal.isGenerator(g, p)) {

                        JOptionPane.showMessageDialog(this, "a không phải phần tử sinh của Zp*");

                        return;
                    }

                    int y = (int) ElGamal.modPow(g, x, p);

                    txtY.setText(String.valueOf(y));
                }

            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi tạo khóa");
            }
        });


        // MÃ HÓA
        btnEncrypt.addActionListener(e -> {

            try {

                int p = Integer.parseInt(txtP.getText());

                int g = Integer.parseInt(txtG.getText());

                int y = Integer.parseInt(txtY.getText());

                int k = Integer.parseInt(txtK.getText());

                if (k <= 1 || k >= p - 1) {

                    JOptionPane.showMessageDialog(this, "k phải thỏa 1 < k < p - 1");

                    return;
                }

                if (!ElGamal.gcdEqualsOne(k, p - 1)) {

                    JOptionPane.showMessageDialog(this, "k phải nguyên tố cùng nhau với p - 1");

                    return;
                }

                String plain = txtPlain.getText();

                StringBuilder c1Text = new StringBuilder();

                StringBuilder c2Text = new StringBuilder();

                StringBuilder cipher = new StringBuilder();

                byte[] bytes = plain.getBytes(StandardCharsets.UTF_8);

                for (byte b : bytes) {

                    int m = b & 0xFF;

                    int[] pair = ElGamal.encryptChar(m, p, g, y, k);

                    int c1 = pair[0];
                    int c2 = pair[1];

                    c1Text.append(c1).append("\n");

                    c2Text.append(c2).append("\n");

                    cipher.append("(").append(c1).append(", ").append(c2).append(")\n");
                }

                txtC1.setText(c1Text.toString());

                txtC2.setText(c2Text.toString());

                txtCipher.setText(cipher.toString());

            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi mã hóa");
            }
        });

        // GIẢI MÃ
        btnDecrypt.addActionListener(e -> {

            try {

                int p = Integer.parseInt(txtP.getText());

                int x = Integer.parseInt(txtX.getText());

                java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();

                String[] lines = txtCipher.getText().split("\n");

                for (String line : lines) {

                    if (line.trim().isEmpty())
                        continue;

                    line = line.replace("(", "");

                    line = line.replace(")", "");

                    String[] pair = line.split(",");

                    int c1 = Integer.parseInt(pair[0].trim());

                    int c2 = Integer.parseInt(pair[1].trim());

                    int m = ElGamal.decryptChar(c1, c2, p, x);

                    baos.write(m);
                }

                String result = new String(baos.toByteArray(), StandardCharsets.UTF_8);

                txtDecrypt.setText(result);

            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi giải mã");
            }
        });

        btnClear.addActionListener(e -> {

            txtPlain.setText("");
            txtC1.setText("");
            txtC2.setText("");
            txtCipher.setText("");
            txtDecrypt.setText("");

        });

        btnExit.addActionListener(e -> System.exit(0));
    }
}