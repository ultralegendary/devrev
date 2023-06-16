import java.net.*;
import java.io.*;
public class console {
    Scanner scanner = new Scanner(System.in);
    public static void main(String[] args) {

        while (true) {
            System.out.println("Flight Booking System");
            System.out.println("1. User Login");
            System.out.println("2. User Sign Up");
            System.out.println("3. Admin Login");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume the newline character

            switch (choice) {
                case 1:
                    userLogin();
                    break;
                case 2:
                    userSignUp();
                    break;
                case 3:
                    adminLogin();
                    break;
                case 4:
                    System.out.println("Thank you for using the Flight Booking System!");
                    System.exit(0);
                default:
                    System.out.println("Invalid choice. Please try again.");
                    break;
            }
        }
    }

    public static void userLogin() {
        System.out.print("Enter your email id: ");
        String username=scanner.next();
        System.out.print("Enter your password: ");
        String password=scanner.next();
        try {
            URL url = new URL("localhost:5000/userlogin");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            
            // Set request parameters
            String params = "email=" + URLEncoder.encode(username, "UTF-8") +
                    "&password=" + URLEncoder.encode(password, "UTF-8");
            
            // Send request
            OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
            writer.write(params);
            writer.flush();
            
            // Process response
            if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                
            } else {
                // Failed login
                // Process the error response
            }
            
            conn.disconnect();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public static void userSignUp() {
        // Implement user sign up functionality
        // You can call the signUp() function provided in the previous code
    }

    public static void adminLogin() {
        // Implement admin login functionality
        // You can call the login() function provided in the previous code
    }

    // Add more functions for each use case as per your requirement
}
