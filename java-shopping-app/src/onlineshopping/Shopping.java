package onlineshopping;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;

import java.io.*;
import java.net.URL;
import java.nio.file.Files;
import java.util.*;

public class Shopping extends Application {
    private Stage primaryStage;
    private Scene roleSelectionScene, loginScene, registrationScene, productScene, cartScene, checkoutScene,
            productDetailScene, adminHomeScene, viewCustomersScene, viewPurchasesScene, summaryTableScene;
    private final Map<String, List<String[]>> categorizedProducts = new LinkedHashMap<>();
    private final List<String[]> shoppingCart = new ArrayList<>();
    private final Map<String, String> userCredentials = new HashMap<>();
    private final Map<String, String> adminCredentials = new HashMap<>();
    private String currentUser = null;
    private boolean isAdmin = false;

    private final File customerFile = new File("customers.txt");
    private final File adminFile = new File("admins.txt");

    @Override
    public void start(Stage primaryStage) {
        this.primaryStage = primaryStage;
        primaryStage.setTitle("Shopping App");
        loadUsersFromFile();
        loadAdminsFromFile();
        loadProducts();
        createRoleSelectionScene();
        createProductScene();
        createCartScene();
        createCheckoutScene();
        primaryStage.setScene(roleSelectionScene);
        primaryStage.show();
    }

    private void createRoleSelectionScene() {
        VBox root = new VBox(20);
        styleScene(root);
        root.setAlignment(Pos.CENTER);
        Label label = new Label("Continue as:");
        label.setFont(new Font("Arial", 22));
        Button customerBtn = new Button("Customer");
        Button adminBtn = new Button("Admin");

        customerBtn.setOnAction(e -> {
            isAdmin = false;
            createLoginScene(null);
            createRegistrationScene();
            primaryStage.setScene(loginScene);
        });

        adminBtn.setOnAction(e -> {
            isAdmin = true;
            createLoginScene(null);
            createRegistrationScene();
            primaryStage.setScene(loginScene);
        });

        root.getChildren().addAll(label, customerBtn, adminBtn);
        roleSelectionScene = new Scene(root, 400, 300);
    }

    private void loadProducts() {
        categorizedProducts.put("Dairy", Arrays.asList(
                new String[] { "1", "Milk", "180", "/images/milk.png" },
                new String[] { "2", "Cheese", "500", "/images/cheese.png" },
                new String[] { "3", "Yogurt", "100", "/images/yogurt.png" },
                new String[] { "4", "Butter", "350", "/images/butter.png" },
                new String[] { "5", "Cream", "300", "/images/cream.png" }));

        categorizedProducts.put("Frozen Foods", Arrays.asList(
                new String[] { "6", "Frozen Peas", "200", "/images/frozen_peas.png" },
                new String[] { "7", "Frozen Chicken", "800", "/images/frozen_chicken.png" },
                new String[] { "8", "Frozen Pizza", "450", "/images/frozen_pizza.png" },
                new String[] { "9", "Ice Cream", "250", "/images/ice_cream.png" },
                new String[] { "10", "Frozen Fries", "300", "/images/frozen_fries.png" }));

        categorizedProducts.put("Snacks", Arrays.asList(
                new String[] { "11", "Chips", "50", "/images/chips.png" },
                new String[] { "12", "Chocolate", "120", "/images/chocolate.png" },
                new String[] { "13", "Cookies", "150", "/images/cookies.png" },
                new String[] { "14", "Nimko", "100", "/images/nimko.png" },
                new String[] { "15", "Popcorn", "80", "/images/popcorn.png" }));
    }

    private void loadUsersFromFile() {
        if (customerFile.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(customerFile))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("USER:")) {
                        String[] parts = line.substring(5).split(",");
                        if (parts.length == 2)
                            userCredentials.put(parts[0], parts[1]);
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void loadAdminsFromFile() {
        if (adminFile.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(adminFile))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("ADMIN:")) {
                        String[] parts = line.substring(6).split(",");
                        if (parts.length == 2)
                            adminCredentials.put(parts[0], parts[1]);
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void saveUserToFile(String username, String password) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(customerFile, true))) {
            writer.write("USER:" + username + "," + password);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void saveAdminToFile(String username, String password) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(adminFile, true))) {
            writer.write("ADMIN:" + username + "," + password);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void savePurchaseToFile(List<String[]> purchases) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(customerFile, true))) {
            writer.write("PURCHASE:" + currentUser);
            writer.newLine();
            for (String[] product : purchases) {
                writer.write(product[1] + "," + product[2]);
                writer.newLine();
            }
            writer.write("END_PURCHASE");
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void createLoginScene(String optionalMessage) {
        GridPane grid = new GridPane();
        styleScene(grid);
        grid.setAlignment(Pos.CENTER);
        grid.setPadding(new Insets(20));
        grid.setHgap(10);
        grid.setVgap(10);

        Label title = new Label("Login");
        title.setFont(new Font("Arial", 20));
        grid.add(title, 0, 0, 2, 1);

        TextField usernameField = new TextField();
        PasswordField passwordField = new PasswordField();
        grid.add(new Label("Username:"), 0, 1);
        grid.add(usernameField, 1, 1);
        grid.add(new Label("Password:"), 0, 2);
        grid.add(passwordField, 1, 2);

        Label message = new Label(optionalMessage != null ? optionalMessage : "");
        message.setTextFill(optionalMessage != null ? Color.GREEN : Color.RED);
        grid.add(message, 1, 3);

        Button loginButton = new Button("Login");
        loginButton.setOnAction(e -> {
            String username = usernameField.getText();
            String password = passwordField.getText();
            if (isAdmin) {
                if (adminCredentials.containsKey(username) && adminCredentials.get(username).equals(password)) {
                    currentUser = username;
                    createAdminHomeScene();
                    primaryStage.setScene(adminHomeScene);
                } else {
                    message.setText("Invalid admin credentials.");
                }
            } else {
                if (userCredentials.containsKey(username) && userCredentials.get(username).equals(password)) {
                    currentUser = username;
                    primaryStage.setScene(productScene);
                } else {
                    message.setText("Invalid user credentials.");
                }
            }
        });

        Button registerButton = new Button("Register");
        registerButton.setOnAction(e -> {
            createRegistrationScene();
            primaryStage.setScene(registrationScene);
        });

        Button backButton = new Button("Back");
        backButton.setOnAction(e -> primaryStage.setScene(roleSelectionScene));

        HBox buttons = new HBox(10, loginButton, registerButton, backButton);
        grid.add(buttons, 1, 4);

        loginScene = new Scene(grid, 450, 300);
    }

    private void createRegistrationScene() {
        GridPane grid = new GridPane();
        styleScene(grid);
        grid.setAlignment(Pos.CENTER);
        grid.setPadding(new Insets(20));
        grid.setHgap(10);
        grid.setVgap(10);

        Label title = new Label("Register");
        title.setFont(new Font("Arial", 20));
        grid.add(title, 0, 0, 2, 1);

        TextField usernameField = new TextField();
        PasswordField passwordField = new PasswordField();
        grid.add(new Label("Username:"), 0, 1);
        grid.add(usernameField, 1, 1);
        grid.add(new Label("Password:"), 0, 2);
        grid.add(passwordField, 1, 2);

        Button registerButton = new Button("Register");
        registerButton.setOnAction(e -> {
            String user = usernameField.getText();
            String pass = passwordField.getText();
            if (!user.isEmpty() && !pass.isEmpty()) {
                if (isAdmin) {
                    adminCredentials.put(user, pass);
                    saveAdminToFile(user, pass);
                } else {
                    userCredentials.put(user, pass);
                    saveUserToFile(user, pass);
                }
                createLoginScene("Registration successful. Please login.");
                primaryStage.setScene(loginScene);
            }
        });

        Button backButton = new Button("Back");
        backButton.setOnAction(e -> primaryStage.setScene(loginScene));

        grid.add(registerButton, 1, 4);
        grid.add(backButton, 0, 4);

        registrationScene = new Scene(grid, 400, 300);
    }

    private void createAdminHomeScene() {
        VBox root = new VBox(20);
        styleScene(root);
        root.setAlignment(Pos.CENTER);

        Label title = new Label("Admin Dashboard");
        title.setFont(new Font("Arial", 22));

        Button viewCustomers = new Button("View Customer Accounts");
        viewCustomers.setOnAction(e -> viewCustomerAccounts());

        Button viewPurchases = new Button("View Purchase Records");
        viewPurchases.setOnAction(e -> viewPurchaseRecords());

        Button logout = new Button("Logout");
        logout.setOnAction(e -> primaryStage.setScene(roleSelectionScene));

        root.getChildren().addAll(title, viewCustomers, viewPurchases, logout);
        adminHomeScene = new Scene(root, 500, 400);
    }

    private void viewCustomerAccounts() {
        VBox root = new VBox(10);
        styleScene(root);
        root.setPadding(new Insets(10));
        root.setAlignment(Pos.TOP_CENTER);

        Label title = new Label("Customer Accounts");
        title.setFont(new Font("Arial", 20));
        root.getChildren().add(title);

        try (BufferedReader reader = new BufferedReader(new FileReader(customerFile))) {
            String line;
            VBox list = new VBox(5);
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("USER:")) {
                    String[] parts = line.substring(5).split(",");
                    if (parts.length == 2) {
                        String username = parts[0];
                        String password = parts[1];

                        Button viewBtn = new Button(username);
                        viewBtn.setOnAction(e -> showCustomerDetails(username, password));

                        Button deleteBtn = new Button("Delete");
                        deleteBtn.setOnAction(e -> deleteCustomer(username));

                        HBox row = new HBox(10, viewBtn, deleteBtn);
                        list.getChildren().add(row);
                    }
                }
            }
            root.getChildren().add(list);
        } catch (IOException e) {
            e.printStackTrace();
        }

        Button back = new Button("Back");
        back.setOnAction(e -> primaryStage.setScene(adminHomeScene));
        root.getChildren().add(back);

        viewCustomersScene = new Scene(root, 500, 500);
        primaryStage.setScene(viewCustomersScene);
    }

    private void showCustomerDetails(String username, String password) {
        VBox root = new VBox(10);
        styleScene(root);
        root.setPadding(new Insets(10));
        root.setAlignment(Pos.TOP_LEFT);

        Label userLabel = new Label("Username: " + username);
        Label passLabel = new Label("Password: " + password);
        Label purchasesLabel = new Label("Purchases:");

        VBox purchaseList = new VBox(5);
        try (BufferedReader reader = new BufferedReader(new FileReader(customerFile))) {
            String line;
            boolean found = false;
            while ((line = reader.readLine()) != null) {
                if (line.equals("PURCHASE:" + username)) {
                    found = true;
                    continue;
                }
                if (found && line.equals("END_PURCHASE")) {
                    break;
                }
                if (found) {
                    purchaseList.getChildren().add(new Label(line));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        Button back = new Button("Back");
        back.setOnAction(e -> viewCustomerAccounts());

        root.getChildren().addAll(userLabel, passLabel, purchasesLabel, purchaseList, back);

        primaryStage.setScene(new Scene(root, 500, 500));
    }

    private void deleteCustomer(String username) {
        Alert confirm = new Alert(Alert.AlertType.CONFIRMATION, "Are you sure you want to delete this user?",
                ButtonType.YES, ButtonType.NO);
        confirm.showAndWait().ifPresent(type -> {
            if (type == ButtonType.YES) {
                try {
                    List<String> lines = Files.readAllLines(customerFile.toPath());
                    List<String> updated = new ArrayList<>();
                    boolean skip = false;
                    for (String line : lines) {
                        if (line.startsWith("USER:" + username)) {
                            skip = true;
                            continue;
                        }
                        if (line.equals("PURCHASE:" + username)) {
                            skip = true;
                            continue;
                        }
                        if (skip && line.equals("END_PURCHASE")) {
                            skip = false;
                            continue;
                        }
                        if (!skip)
                            updated.add(line);
                    }
                    Files.write(customerFile.toPath(), updated);
                    viewCustomerAccounts();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void viewPurchaseRecords() {
        VBox root = new VBox(10);
        styleScene(root);
        root.setPadding(new Insets(10));
        root.setAlignment(Pos.TOP_LEFT);

        Label title = new Label("Purchase Records");
        title.setFont(new Font("Arial", 20));
        root.getChildren().add(title);

        VBox purchases = new VBox(5);
        try (BufferedReader reader = new BufferedReader(new FileReader(customerFile))) {
            String line;
            boolean show = false;
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("PURCHASE:")) {
                    purchases.getChildren().add(new Label(line));
                    show = true;
                    continue;
                }
                if (show && line.equals("END_PURCHASE")) {
                    show = false;
                    continue;
                }
                if (show) {
                    purchases.getChildren().add(new Label("    " + line));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        Button summaryBtn = new Button("View Summary Table");
        summaryBtn.setOnAction(e -> showSummaryTable());

        Button back = new Button("Back");
        back.setOnAction(e -> primaryStage.setScene(adminHomeScene));

        root.getChildren().addAll(purchases, summaryBtn, back);
        viewPurchasesScene = new Scene(root, 600, 500);
        primaryStage.setScene(viewPurchasesScene);
    }

    private void showSummaryTable() {
        VBox root = new VBox(10);
        styleScene(root);
        root.setPadding(new Insets(10));

        Label title = new Label("Summary Table");
        title.setFont(new Font("Arial", 20));
        root.getChildren().add(title);

        Map<String, int[]> summary = new LinkedHashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(customerFile))) {
            String line;
            boolean show = false;
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("PURCHASE:")) {
                    show = true;
                    continue;
                }
                if (show && line.equals("END_PURCHASE")) {
                    show = false;
                    continue;
                }
                if (show) {
                    String[] parts = line.split(",");
                    if (parts.length == 2) {
                        String name = parts[0];
                        int price = Integer.parseInt(parts[1]);
                        summary.putIfAbsent(name, new int[] { price, 0 });
                        summary.get(name)[1] += 1;
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.addRow(0, new Label("Product"), new Label("Price"), new Label("Quantity"), new Label("Total"));

        int row = 1;
        for (Map.Entry<String, int[]> entry : summary.entrySet()) {
            int total = entry.getValue()[0] * entry.getValue()[1];
            grid.addRow(row++, new Label(entry.getKey()), new Label("Rs. " + entry.getValue()[0]),
                    new Label(String.valueOf(entry.getValue()[1])), new Label("Rs. " + total));
        }

        Button downloadBtn = new Button("Download as CSV");
        downloadBtn.setOnAction(e -> downloadSummaryCSV(summary));

        Button back = new Button("Back");
        back.setOnAction(e -> primaryStage.setScene(viewPurchasesScene));

        root.getChildren().addAll(grid, downloadBtn, back);
        summaryTableScene = new Scene(root, 600, 400);
        primaryStage.setScene(summaryTableScene);
    }

    private void downloadSummaryCSV(Map<String, int[]> summary) {
        File file = new File("summary.csv");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
            writer.write("Product,Price,Quantity,Total\n");
            for (Map.Entry<String, int[]> entry : summary.entrySet()) {
                int total = entry.getValue()[0] * entry.getValue()[1];
                writer.write(String.format("%s,%d,%d,%d\n", entry.getKey(), entry.getValue()[0], entry.getValue()[1],
                        total));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void createProductScene() {
        VBox root = new VBox(20);
        styleScene(root);
        root.setPadding(new Insets(20));
        root.setAlignment(Pos.TOP_CENTER);

        Label title = new Label("Available Products");
        title.setFont(new Font("Arial", 22));
        root.getChildren().add(title);

        HBox categoryRow = new HBox(30);
        categoryRow.setAlignment(Pos.CENTER);

        for (Map.Entry<String, List<String[]>> entry : categorizedProducts.entrySet()) {
            VBox box = new VBox(10);
            box.setAlignment(Pos.TOP_CENTER);

            Label label = new Label(entry.getKey());
            label.setFont(new Font("Arial", 16));

            ComboBox<String> dropdown = new ComboBox<>();
            Map<String, String[]> map = new HashMap<>();
            for (String[] p : entry.getValue()) {
                dropdown.getItems().add(p[1]);
                map.put(p[1], p);
            }

            dropdown.setOnAction(e -> {
                String selected = dropdown.getValue();
                if (map.containsKey(selected)) {
                    createProductDetailScene(map.get(selected));
                    primaryStage.setScene(productDetailScene);
                }
            });

            box.getChildren().addAll(label, dropdown);
            categoryRow.getChildren().add(box);
        }

        root.getChildren().add(categoryRow);
        productScene = new Scene(root, 700, 500);
    }

    private void createProductDetailScene(String[] product) {
        VBox root = new VBox(15);
        styleScene(root);
        root.setPadding(new Insets(20));
        root.setAlignment(Pos.CENTER);

        Label name = new Label(product[1]);
        name.setFont(new Font("Arial", 22));
        root.getChildren().add(name);

        URL url = getClass().getResource(product[3]);
        if (url != null) {
            ImageView img = new ImageView(new Image(url.toExternalForm(), 100, 100, true, true));
            root.getChildren().add(img);
        }

        Label price = new Label("Rs. " + product[2]);
        price.setFont(new Font("Arial", 18));
        root.getChildren().add(price);

        HBox qtyBox = new HBox(10);
        qtyBox.setAlignment(Pos.CENTER);
        Label qtyLabel = new Label("Quantity: 1");
        int[] qty = { 1 };

        Button minus = new Button("-");
        Button plus = new Button("+");

        minus.setOnAction(e -> {
            if (qty[0] > 1)
                qty[0]--;
            qtyLabel.setText("Quantity: " + qty[0]);
        });

        plus.setOnAction(e -> {
            qty[0]++;
            qtyLabel.setText("Quantity: " + qty[0]);
        });

        qtyBox.getChildren().addAll(minus, qtyLabel, plus);
        root.getChildren().add(qtyBox);

        Button addToCart = new Button("Add to Cart");
        addToCart.setOnAction(e -> {
            for (int i = 0; i < qty[0]; i++)
                shoppingCart.add(product);
            createCartScene();
            primaryStage.setScene(cartScene);
        });

        Button back = new Button("Back to Products");
        HBox nav = new HBox(10, back, addToCart);
        nav.setAlignment(Pos.CENTER);

        back.setOnAction(e -> primaryStage.setScene(productScene));
        root.getChildren().add(nav);

        productDetailScene = new Scene(root, 500, 500);
    }

    private void createCartScene() {
        VBox root = new VBox(15);
        styleScene(root);
        root.setPadding(new Insets(15));

        Label title = new Label("Your Cart");
        title.setFont(new Font("Arial", 20));
        root.getChildren().add(title);

        Map<String, Integer> count = new LinkedHashMap<>();
        Map<String, String[]> map = new HashMap<>();
        int total = 0;

        for (String[] p : shoppingCart) {
            String key = p[0];
            count.put(key, count.getOrDefault(key, 0) + 1);
            map.put(key, p);
        }

        for (Map.Entry<String, Integer> e : count.entrySet()) {
            String[] p = map.get(e.getKey());
            int q = e.getValue();
            int price = Integer.parseInt(p[2]);
            total += q * price;

            HBox box = new HBox(10);
            Label label = new Label(p[1] + " x" + q + " - Rs. " + (q * price));

            Button dec = new Button("-");
            dec.setOnAction(a -> {
                shoppingCart.remove(p);
                createCartScene();
                primaryStage.setScene(cartScene);
            });

            Button inc = new Button("+");
            inc.setOnAction(a -> {
                shoppingCart.add(p);
                createCartScene();
                primaryStage.setScene(cartScene);
            });

            Button del = new Button("Remove");
            del.setOnAction(a -> {
                shoppingCart.removeIf(i -> i[0].equals(p[0]));
                createCartScene();
                primaryStage.setScene(cartScene);
            });

            box.getChildren().addAll(label, dec, inc, del);
            root.getChildren().add(box);
        }

        Label totalLabel = new Label("Total: Rs. " + total);
        totalLabel.setFont(Font.font("Arial", 16));
        root.getChildren().add(totalLabel);

        Button back = new Button("Add More Products");
        back.setOnAction(e -> primaryStage.setScene(productScene));

        Button checkout = new Button("Checkout");
        checkout.setOnAction(e -> {
            createCheckoutScene();
            primaryStage.setScene(checkoutScene);
        });

        root.getChildren().add(new HBox(10, back, checkout));
        cartScene = new Scene(root, 550, 500);
    }

    private void createCheckoutScene() {
        VBox root = new VBox(10);
        styleScene(root);
        root.setPadding(new Insets(10));
        root.setAlignment(Pos.CENTER);

        Label title = new Label("Checkout Summary");
        title.setFont(new Font("Arial", 20));
        root.getChildren().add(title);

        int total = 0;
        for (String[] p : shoppingCart) {
            root.getChildren().add(new Label(p[1] + " - Rs. " + p[2]));
            total += Integer.parseInt(p[2]);
        }

        Label totalLabel = new Label("Total: Rs. " + total);
        totalLabel.setFont(Font.font("Arial", 16));
        root.getChildren().add(totalLabel);

        Button confirm = new Button("Confirm Purchase");
        confirm.setOnAction(e -> {
            savePurchaseToFile(shoppingCart);
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("Order Confirmed");
            alert.setContentText("Thank you for your purchase!");
            alert.showAndWait();
            shoppingCart.clear();
            createProductScene();
            primaryStage.setScene(productScene);
        });

        Button back = new Button("Back to Cart");
        back.setOnAction(e -> {
            createCartScene();
            primaryStage.setScene(cartScene);
        });

        root.getChildren().addAll(confirm, back);
        checkoutScene = new Scene(root, 500, 400);
    }

    private void styleScene(Region root) {
        root.setStyle("-fx-background-color: linear-gradient(to bottom right, #f0faff, #d0e8ff);");
    }

    public static void main(String[] args) {
        launch(args);
    }
}
