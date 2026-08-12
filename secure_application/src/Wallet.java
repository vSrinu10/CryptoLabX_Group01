import java.util.ArrayList;
import java.util.List;

public class Wallet {
    private String walletId;
    private String ownerName;
    private String password;
    private double balance;
    private List<Transaction> transactions;

    public Wallet(String walletId, String ownerName, String password) {
        this.walletId = walletId;
        this.ownerName = ownerName;
        this.password = password;
        this.balance = 1000.0;
        this.transactions = new ArrayList<>();
    }

    public String getWalletId() {
        return walletId;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public String getPassword() {
        return password;
    }

    public double getBalance() {
        return balance;
    }

    public List<Transaction> getTransactions() {
        return transactions;
    }

    public void addBalance(double amount) {
        balance += amount;
    }

    public void subtractBalance(double amount) {
        balance -= amount;
    }

    public void addTransaction(Transaction transaction) {
        transactions.add(transaction);
    }

    public void displayWallet() {
        System.out.println("\n========== WALLET DETAILS ==========");
        System.out.println("Wallet ID : " + walletId);
        System.out.println("Owner     : " + ownerName);
        System.out.println("Balance   : " + balance + " CR");
        System.out.println("====================================");
    }
}
