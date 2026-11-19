import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class SmartWellDashboard extends JFrame {

    // COLORS
    Color bg = new Color(16, 24, 39);
    Color card = new Color(30, 41, 59);
    Color blue = new Color(56, 189, 248);
    Color green = new Color(34, 197, 94);
    Color red = new Color(239, 68, 68);
    Color yellow = new Color(250, 204, 21);
    Color white = Color.WHITE;

    // SENSOR INPUTS
    JTextField waterInput;
    JTextField distanceInput;
    JTextField tempInput;
    JTextField minutesInput;

    // SENSOR VALUES
    JLabel waterValue;
    JLabel distanceValue;
    JLabel tempValue;

    // STATUS LABELS
    JLabel safetyStatus;
    JLabel buzzerStatus;
    JLabel timerDisplay;

    // DETECTION COUNTS
    JLabel personCount;
    JLabel animalCount;
    JLabel birdCount;
    JLabel totalCount;

    // DROPDOWNS
    JComboBox<String> wellChoice;
    JComboBox<String> objectChoice;

    // HISTORY
    DefaultListModel<String> historyModel;
    JList<String> historyList;

    // COUNTERS
    int person = 0;
    int animal = 0;
    int bird = 0;

    int seconds = 0;

    // TIMERS
    Timer bathingTimer;
    Timer buzzerTimer;

    // FLAGS
    boolean distanceAlarm = false;
    boolean buzzerOn = false;

    // CONSTRUCTOR
    public SmartWellDashboard() {

        setTitle("Smart Well Safety Dashboard");
        setSize(1200, 850);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel main = new JPanel();
        main.setBackground(bg);
        main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));
        main.setBorder(new EmptyBorder(18, 18, 18, 18));

        // HEADER
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(bg);
        header.setMaximumSize(new Dimension(1150, 85));

        JLabel title = new JLabel(
                "SMART WELL SAFETY DASHBOARD",
                JLabel.CENTER
        );

        title.setFont(new Font("Arial", Font.BOLD, 27));
        title.setForeground(blue);

        JLabel subtitle = new JLabel(
                "Real-Time Well Monitoring and Safety Alert System",
                JLabel.CENTER
        );

        subtitle.setFont(new Font("Arial", Font.PLAIN, 14));
        subtitle.setForeground(white);

        JPanel titlePanel = new JPanel(new GridLayout(2, 1));
        titlePanel.setBackground(bg);
        titlePanel.add(title);
        titlePanel.add(subtitle);

        header.add(titlePanel, BorderLayout.CENTER);

        main.add(header);
        main.add(Box.createVerticalStrut(18));

        // WELL SELECTION
        JPanel wellPanel = createPanel("WELL SELECTION");

        wellChoice = new JComboBox<>(new String[]{
                "North Field Well",
                "Village Well",
                "Farm Well"
        });

        styleCombo(wellChoice);

        addRow(wellPanel, "Select Well:", wellChoice);

        main.add(wellPanel);
        main.add(Box.createVerticalStrut(18));

        // DETECTION COUNT CARDS
        JPanel countPanel = new JPanel(
                new GridLayout(1, 4, 12, 0)
        );

        countPanel.setBackground(bg);
        countPanel.setMaximumSize(new Dimension(1150, 115));

        personCount = createValue("0");
        animalCount = createValue("0");
        birdCount = createValue("0");
        totalCount = createValue("0");

        countPanel.add(createCountCard("PERSON COUNT", personCount));
        countPanel.add(createCountCard("ANIMAL COUNT", animalCount));
        countPanel.add(createCountCard("BIRD COUNT", birdCount));
        countPanel.add(createCountCard("TOTAL COUNT", totalCount));

        main.add(countPanel);
        main.add(Box.createVerticalStrut(18));

        // MAIN CONTENT
        JPanel content = new JPanel(
                new GridLayout(2, 2, 15, 15)
        );

        content.setBackground(bg);
        content.setMaximumSize(new Dimension(1150, 460));

        // SENSOR PANEL
        JPanel sensorPanel = createPanel("SENSOR MONITORING");

        waterInput = createInput("65");
        distanceInput = createInput("150");
        tempInput = createInput("28");

        waterValue = createValue("65 cm");
        distanceValue = createValue("150 cm");
        tempValue = createValue("28 °C");

        addSensorRow(
                sensorPanel,
                "Water Level (cm):",
                waterInput,
                waterValue
        );

        addSensorRow(
                sensorPanel,
                "Distance (cm):",
                distanceInput,
                distanceValue
        );

        addSensorRow(
                sensorPanel,
                "Temperature (°C):",
                tempInput,
                tempValue
        );

        safetyStatus = new JLabel("SAFE");
        safetyStatus.setFont(new Font("Arial", Font.BOLD, 20));
        safetyStatus.setForeground(green);

        addRow(sensorPanel, "Safety Status:", safetyStatus);

        JButton updateButton = createButton("UPDATE SENSOR");

        updateButton.addActionListener(e -> updateSensor());

        sensorPanel.add(updateButton);

        // OBJECT DETECTION PANEL
        JPanel detectionPanel = createPanel("OBJECT DETECTION");

        objectChoice = new JComboBox<>(new String[]{
                "Person",
                "Animal",
                "Bird"
        });

        styleCombo(objectChoice);

        addRow(detectionPanel, "Select Object:", objectChoice);

        JButton detectButton = createButton("DETECT OBJECT");

        detectButton.addActionListener(e -> detectObject());

        detectionPanel.add(detectButton);

        // BUZZER PANEL
        JPanel buzzerPanel = createPanel("BUZZER CONTROL");

        buzzerStatus = new JLabel("BUZZER OFF");

        buzzerStatus.setFont(new Font("Arial", Font.BOLD, 22));
        buzzerStatus.setForeground(green);

        addRow(buzzerPanel, "Buzzer Status:", buzzerStatus);

        JButton stopBuzzerButton = createButton("STOP BUZZER");

        stopBuzzerButton.addActionListener(e -> {
            stopBuzzer();
            addHistory("Buzzer stopped manually");
        });

        buzzerPanel.add(stopBuzzerButton);

        // BATHING TIMER PANEL
        JPanel timerPanel = createPanel("BATHING TIME MONITOR");

        minutesInput = createInput("5");

        timerDisplay = new JLabel("05:00");

        timerDisplay.setFont(new Font("Arial", Font.BOLD, 28));
        timerDisplay.setForeground(yellow);

        addRow(timerPanel, "Bathing Time (Minutes):", minutesInput);
        addRow(timerPanel, "Remaining Time:", timerDisplay);

        JButton startButton = createButton("START");
        JButton stopButton = createButton("STOP");
        JButton resetButton = createButton("RESET");

        startButton.addActionListener(e -> startTimer());
        stopButton.addActionListener(e -> stopTimer());
        resetButton.addActionListener(e -> resetTimer());

        JPanel timerButtons = new JPanel(
                new FlowLayout(FlowLayout.CENTER)
        );

        timerButtons.setBackground(card);

        timerButtons.add(startButton);
        timerButtons.add(stopButton);
        timerButtons.add(resetButton);

        timerPanel.add(timerButtons);

        content.add(sensorPanel);
        content.add(detectionPanel);
        content.add(buzzerPanel);
        content.add(timerPanel);

        main.add(content);
        main.add(Box.createVerticalStrut(18));

        // HISTORY PANEL
        JPanel historyPanel = createPanel("ACTIVITY HISTORY");

        historyModel = new DefaultListModel<>();

        historyList = new JList<>(historyModel);
        historyList.setBackground(card);
        historyList.setForeground(white);
        historyList.setFont(new Font("Arial", Font.PLAIN, 14));
        historyList.setVisibleRowCount(6);

        JScrollPane historyScroll = new JScrollPane(historyList);

        historyScroll.setPreferredSize(new Dimension(1100, 140));

        historyPanel.add(historyScroll);

        JButton clearButton = createButton("CLEAR HISTORY");

        clearButton.addActionListener(e -> historyModel.clear());

        historyPanel.add(clearButton);

        main.add(historyPanel);

        JScrollPane scrollPane = new JScrollPane(main);
        scrollPane.setBorder(null);
        scrollPane.getVerticalScrollBar().setUnitIncrement(15);

        add(scrollPane);

        addHistory("Smart Well Dashboard Started");

        setVisible(true);
    }

    // CREATE PANEL
    JPanel createPanel(String heading) {

        JPanel panel = new JPanel();

        panel.setLayout(
                new BoxLayout(panel, BoxLayout.Y_AXIS)
        );

        panel.setBackground(card);

        panel.setBorder(
                BorderFactory.createTitledBorder(
                        BorderFactory.createLineBorder(blue),
                        heading,
                        TitledBorder.LEFT,
                        TitledBorder.TOP,
                        new Font("Arial", Font.BOLD, 15),
                        blue
                )
        );

        return panel;
    }

    // COUNT CARD
    JPanel createCountCard(String heading, JLabel value) {

        JPanel panel = new JPanel(
                new GridLayout(2, 1, 5, 5)
        );

        panel.setBackground(card);

        panel.setBorder(
                BorderFactory.createLineBorder(blue)
        );

        JLabel title = new JLabel(heading, JLabel.CENTER);

        title.setForeground(white);
        title.setFont(new Font("Arial", Font.BOLD, 13));

        value.setHorizontalAlignment(JLabel.CENTER);
        value.setFont(new Font("Arial", Font.BOLD, 25));

        panel.add(title);
        panel.add(value);

        return panel;
    }

    // INPUT FIELD
    JTextField createInput(String text) {

        JTextField field = new JTextField(text, 10);

        field.setFont(new Font("Arial", Font.PLAIN, 15));

        return field;
    }

    // VALUE LABEL
    JLabel createValue(String text) {

        JLabel label = new JLabel(text);

        label.setForeground(blue);
        label.setFont(new Font("Arial", Font.BOLD, 18));

        return label;
    }

    // BUTTON
    JButton createButton(String text) {

        JButton button = new JButton(text);

        button.setFont(new Font("Arial", Font.BOLD, 13));
        button.setBackground(blue);
        button.setForeground(Color.BLACK);
        button.setFocusPainted(false);

        return button;
    }

    // COMBO BOX STYLE
    void styleCombo(JComboBox<String> combo) {

        combo.setFont(new Font("Arial", Font.PLAIN, 14));
        combo.setBackground(white);
        combo.setForeground(Color.BLACK);
    }

    // ADD ROW
    void addRow(
            JPanel panel,
            String text,
            Component component
    ) {

        JPanel row = new JPanel(
                new FlowLayout(FlowLayout.LEFT, 10, 5)
        );

        row.setBackground(card);

        JLabel label = new JLabel(text);

        label.setForeground(white);
        label.setFont(new Font("Arial", Font.PLAIN, 14));

        row.add(label);
        row.add(component);

        panel.add(row);
    }

    // SENSOR ROW
    void addSensorRow(
            JPanel panel,
            String text,
            JTextField input,
            JLabel value
    ) {

        JPanel row = new JPanel(
                new FlowLayout(FlowLayout.LEFT, 8, 5)
        );

        row.setBackground(card);

        JLabel label = new JLabel(text);

        label.setForeground(white);
        label.setFont(new Font("Arial", Font.PLAIN, 13));

        row.add(label);
        row.add(input);
        row.add(value);

        panel.add(row);
    }

    // UPDATE SENSOR
    void updateSensor() {

        try {

            int water = Integer.parseInt(waterInput.getText());
            int distance = Integer.parseInt(distanceInput.getText());
            int temperature = Integer.parseInt(tempInput.getText());

            if (water < 0 || distance < 0 || temperature < 0) {

                JOptionPane.showMessageDialog(
                        this,
                        "Sensor values cannot be negative!"
                );

                return;
            }

            waterValue.setText(water + " cm");
            distanceValue.setText(distance + " cm");
            tempValue.setText(temperature + " °C");

            if (distance < 200) {

                safetyStatus.setText("UNSAFE");
                safetyStatus.setForeground(red);

                if (!distanceAlarm) {

                    distanceAlarm = true;

                    startBuzzer(true);

                    addHistory(
                            "UNSAFE: Object is near the well"
                    );
                }

            } else {

                safetyStatus.setText("SAFE");
                safetyStatus.setForeground(green);

                if (distanceAlarm) {

                    distanceAlarm = false;

                    stopBuzzer();

                    addHistory(
                            "SAFE: Distance is normal"
                    );
                }
            }

            addHistory("Water Level: " + water + " cm");
            addHistory("Distance: " + distance + " cm");
            addHistory("Temperature: " + temperature + " °C");

        } catch (NumberFormatException ex) {

            JOptionPane.showMessageDialog(
                    this,
                    "Please enter valid sensor values!"
            );
        }
    }

    // OBJECT DETECTION
    void detectObject() {

        String selected =
                (String) objectChoice.getSelectedItem();

        if (selected == null) {
            return;
        }

        if (selected.equals("Person")) {

            person++;

            addHistory("Person Detected");

            updateCounts();

            if (!distanceAlarm) {
                startBuzzer(false);
            }

        } else if (selected.equals("Animal")) {

            animal++;

            addHistory("Animal Detected");

            updateCounts();

            if (!distanceAlarm) {
                startBuzzer(false);
            }

        } else if (selected.equals("Bird")) {

            bird++;

            addHistory("Bird Detected - IGNORED");

            updateCounts();

            // BIRD DETECTION:
            // Count மட்டும் அதிகரிக்கும்.
            // Safety Status மாற்றப்படாது.
            // Buzzer ON ஆகாது.
        }
    }

    // UPDATE COUNTS
    void updateCounts() {

        personCount.setText(String.valueOf(person));

        animalCount.setText(String.valueOf(animal));

        birdCount.setText(String.valueOf(bird));

        totalCount.setText(
                String.valueOf(person + animal + bird)
        );
    }

    // START BUZZER
    void startBuzzer(boolean continuous) {

        if (buzzerTimer != null) {
            buzzerTimer.stop();
        }

        buzzerOn = true;

        buzzerStatus.setText("BUZZER ON");
        buzzerStatus.setForeground(red);

        Toolkit.getDefaultToolkit().beep();

        if (continuous) {

            buzzerTimer = new Timer(1000, e -> {
                Toolkit.getDefaultToolkit().beep();
            });

            buzzerTimer.start();

        } else {

            buzzerTimer = new Timer(3000, e -> {
                stopBuzzer();
            });

            buzzerTimer.setRepeats(false);

            buzzerTimer.start();
        }
    }

    // STOP BUZZER
    void stopBuzzer() {

        buzzerOn = false;

        if (buzzerTimer != null) {
            buzzerTimer.stop();
            buzzerTimer = null;
        }

        buzzerStatus.setText("BUZZER OFF");
        buzzerStatus.setForeground(green);
    }

    // START BATHING TIMER
    void startTimer() {

        try {

            int minutes = Integer.parseInt(
                    minutesInput.getText()
            );

            if (minutes < 1 || minutes > 180) {

                JOptionPane.showMessageDialog(
                        this,
                        "Enter time between 1 and 180 minutes"
                );

                return;
            }

            if (bathingTimer != null) {
                bathingTimer.stop();
            }

            seconds = minutes * 60;

            updateTimerDisplay();

            addHistory("Bathing Timer Started");

            bathingTimer = new Timer(1000, e -> {

                seconds--;

                updateTimerDisplay();

                if (seconds <= 0) {

                    bathingTimer.stop();

                    timerDisplay.setText("COMPLETED");
                    timerDisplay.setForeground(green);

                    addHistory(
                            "Bathing Time Completed"
                    );

                    if (!distanceAlarm) {
                        startBuzzer(false);
                    }
                }
            });

            bathingTimer.start();

        } catch (NumberFormatException ex) {

            JOptionPane.showMessageDialog(
                    this,
                    "Please enter valid bathing time!"
            );
        }
    }

    // UPDATE TIMER DISPLAY
    void updateTimerDisplay() {

        int minutes = seconds / 60;
        int secs = seconds % 60;

        timerDisplay.setText(
                String.format("%02d:%02d", minutes, secs)
        );

        timerDisplay.setForeground(yellow);
    }

    // STOP TIMER
    void stopTimer() {

        if (bathingTimer != null) {

            bathingTimer.stop();

            addHistory("Bathing Timer Stopped");
        }
    }

    // RESET TIMER
    void resetTimer() {

        if (bathingTimer != null) {
            bathingTimer.stop();
        }

        seconds = 0;

        timerDisplay.setText("00:00");
        timerDisplay.setForeground(yellow);

        addHistory("Bathing Timer Reset");
    }

    // ADD HISTORY
    void addHistory(String message) {

        String time = new SimpleDateFormat(
                "HH:mm:ss"
        ).format(new Date());

        historyModel.addElement(
                "[" + time + "] " + message
        );

        historyList.ensureIndexIsVisible(
                historyModel.size() - 1
        );
    }

    // MAIN METHOD
    public static void main(String[] args) {

        SwingUtilities.invokeLater(() -> {
            new SmartWellDashboard();
        });
    }
}