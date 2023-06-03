#include<iostream>
#include<curl/curl.h>

using namespace std;

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t total_size = size * nmemb;
    response->append((char*)contents, total_size);
    return total_size;
}

int main() {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string response;
        curl_easy_setopt(curl, CURLOPT_URL, "results.skcet.ac.in:607");
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        
        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Failed to make request: " << curl_easy_strerror(res) << std::endl;
        }
        else {
            std::cout << "Response: " << response << std::endl;
        }

        curl_easy_cleanup(curl);
    }
    else {
        std::cerr << "Failed to initialize cURL" << std::endl;
    }

    return 0;
}
