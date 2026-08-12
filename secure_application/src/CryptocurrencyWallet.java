import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class CryptocurrencyWallet {

    private static Map<String, Wallet> wallets = new HashMap<>();
    private static Scanner scanner = new Scanner(System.in);

    private static Wallet loggedInWallet = null;

    // VULNERABILITY 1: Hardcoded Secret
    private static final String ADMIN_SECRET = "Admin@123";

    private static int walletCounter = 1001;
    private static int transactionCounter = 5001;

    public static void main(String[] args) {

        while (true) {

            System.out.println("\n========================================");
            System.out.println("       CRYPTOCURRENCY WALLET");
            System.out.println("========================================");
            System.out.println("1. Create Wallet");
            System.out.println("2. Login");
            System.out.println("3. Check Balance");
            System.out.println("4. Send Cryptocurrency");
            System.out.println("5. Transaction History");
            System.out.println("6. View Wallet");
            System.out.println("7. Logout");
            System.out.println("8. Exit");
            System.out.println("========================================");

            System.out.print("Enter choice: ");

            String choice = scanner.nextLine();

            switch (choice) {

                case "1":
                    createWallet();
                    break;

                case "2":
                    login();
                    break;

                case "3":
                    checkBalance();
                    break;

                case "4":
                    sendCryptocurrency();
                    break;

                case "5":
                    transactionHistory();
                    break;

                case "6":
                    viewWallet();
                    break;

                case "7":
                    logout();
                    break;

                case "8":
                    System.out.println("Thank you for using Cryptocurrency Wallet.");
                    scanner.close();
                    return;

                default:
                    System.out.println("Invalid menu choice.");
            }
        }
    }

    private static void createWallet() {

        System.out.println("\n========== CREATE WALLET ==========");

        System.out.print("Enter owner name: ");
        String ownerName = scanner.nextLine();

        System.out.print("Enter password: ");
        String password = scanner.nextLine();

        String walletId = "W" + walletCounter++;

        Wallet wallet = new Wallet(walletId, ownerName, password);

        wallets.put(walletId, wallet);

        System.out.println("\nWallet created successfully!");
        System.out.println("Wallet ID: " + walletId);
        System.out.println("Initial Balance: 1000.0 CR");
    }

    private static void login() {

        System.out.println("\n========== LOGIN ==========");

        System.out.print("Enter Wallet ID: ");
        String walletId = scanner.nextLine();

        System.out.print("Enter Password: ");
        String password = scanner.nextLine();

        Wallet wallet = wallets.get(walletId);

        if (wallet != null && wallet.getPassword().equals(password)) {

            loggedInWallet = wallet;

            System.out.println("\nLogin successful!");
            System.out.println("Welcome, " + wallet.getOwnerName());

        } else {

            System.out.println("\nInvalid Wallet ID or Password.");
        }
    }

    private static void checkBalance() {

        if (loggedInWallet == null) {
            System.out.println("\nPlease login first.");
            return;
        }

        System.out.println("\n========== BALANCE ==========");
        System.out.println("Wallet ID : " + loggedInWallet.getWalletId());
        System.out.println("Balance   : " + loggedInWallet.getBalance() + " CR");
    }

    private static void sendCryptocurrency() {

        if (loggedInWallet == null) {
            System.out.println("\nPlease login first.");
            return;
        }

        System.out.println("\n========== SEND CRYPTOCURRENCY ==========");

        System.out.print("Enter recipient wallet ID: ");
        String receiverId = scanner.nextLine();

        Wallet receiver = wallets.get(receiverId);

        if (receiver == null) {
            System.out.println("Recipient wallet not found.");
            return;
        }

        System.out.print("Enter amount: ");
        double amount;

        try {
            amount = Double.parseDouble(scanner.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("Invalid amount.");
            return;
        }

        // VULNERABILITY 2: Improper Input Validation
        // Negative values are not properly rejected.
        if (amount > loggedInWallet.getBalance()) {
            System.out.println("Insufficient balance.");
            return;
        }

        loggedInWallet.subtractBalance(amount);
        receiver.addBalance(amount);

        String transactionId = "TX" + transactionCounter++;

        Transaction transaction = new Transaction(
                transactionId,
                loggedInWallet.getWalletId(),
                receiverId,
                amount
        );

        loggedInWallet.addTransaction(transaction);
        receiver.addTransaction(transaction);

        System.out.println("\nTransaction successful!");
        System.out.println("Transaction ID: " + transactionId);
        System.out.println("Amount: " + amount + " CR");
    }

    private static void transactionHistory() {

        if (loggedInWallet == null) {
            System.out.println("\nPlease login first.");
            return;
        }

        System.out.println("\n========== TRANSACTION HISTORY ==========");

        List<Transaction> transactions =
                loggedInWallet.getTransactions();

        if (transactions.isEmpty()) {
            System.out.println("No transactions found.");
            return;
        }

        for (Transaction transaction : transactions) {
            transaction.displayTransaction();
        }
    }

    private static void viewWallet() {

        if (loggedInWallet == null) {
            System.out.println("\nPlease login first.");
            return;
        }

        System.out.print("\nEnter Wallet ID to view: ");
        String requestedWalletId = scanner.nextLine();

        // VULNERABILITY 3: Broken Access Control / IDOR
        // The application does not verify that the requested wallet
        // belongs to the currently logged-in user.

        Wallet requestedWallet = wallets.get(requestedWalletId);

        if (requestedWallet == null) {
            System.out.println("Wallet not found.");
            return;
        }

        requestedWallet.displayWallet();
    }

    private static void logout() {

        if (loggedInWallet == null) {
            System.out.println("\nNo user is currently logged in.");
            return;
        }

        System.out.println("\nLogged out successfully.");

        loggedInWallet = null;
    }
}
