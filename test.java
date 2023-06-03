import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpHeaders;
import java.io.IOException;

public class test {
    public static void main(String[] args) {
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest httpRequest = HttpRequest.newBuilder()
                .uri(URI.create("http://results.skcet.ac.in:607"))
                .build();

        try {
            HttpResponse<String> response = httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofString());

            int statusCode = response.statusCode();
            HttpHeaders headers = response.headers();
            String responseBody = response.body();

            System.out.println("Status Code: " + statusCode);
            System.out.println("Headers: " + headers);
            System.out.println("Response: " + responseBody);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
