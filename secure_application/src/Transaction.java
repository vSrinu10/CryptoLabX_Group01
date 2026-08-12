public class Transaction {
    private String transactionId;
    private String senderId;
    private String receiverId;
    private double amount;

    public Transaction(String transactionId, String senderId,
                       String receiverId, double amount) {
        this.transactionId = transactionId;
        this.senderId = senderId;
        this.receiverId = receiverId;
        this.amount = amount;
    }

    public void displayTransaction() {
        System.out.println("------------------------------------");
        System.out.println("Transaction ID : " + transactionId);
        System.out.println("From           : " + senderId);
        System.out.println("To             : " + receiverId);
        System.out.println("Amount         : " + amount + " CR");
        System.out.println("------------------------------------");
    }
}

