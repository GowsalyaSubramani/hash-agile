#include <stdio.h>

// Function to find the length of a string manually
int stringLength(const char *s) {
    int length = 0;
    while (s[length] != '\0') {
        length++;
    }
    return length;
}

// Function to check if a given substring is a palindrome
int isPalindrome(const char *s, int start, int end) {
    while (start < end) {
        if (s[start] != s[end]) {
            return 0; // Not a palindrome
        }
        start++;
        end--;
    }
    return 1; // It is a palindrome
}

// Function to find the longest palindrome substring
void longestPalSubstr(const char *s, char *result) {
    int n = stringLength(s);
    int maxLen = 1; // Length of the longest palindrome
    int start = 0;  // Starting index of the longest palindrome

    // Check all substrings
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            // Check if the substring s[i...j] is a palindrome
            if (isPalindrome(s, i, j)) {
                int currLen = j - i + 1;
                if (currLen > maxLen) {
                    start = i;
                    maxLen = currLen;
                }
            }
        }
    }

    // Copy the longest palindrome substring into result manually
    for (int i = 0; i < maxLen; i++) {
        result[i] = s[start + i];
    }
    result[maxLen] = '\0'; // Null-terminate the result
}

// Driver Code
int main() {
    char s[100];        // Array to store the input string
    char result[100];   // Array to store the result

    // Get input from the user
    printf("Enter a string: ");
    scanf("%s", s);     // Read the input string

    // Call the function to find the longest palindrome substring
    longestPalSubstr(s, result);

    // Print the result
    printf("Longest Palindromic Substring: %s\n", result);
    return 0;
}
