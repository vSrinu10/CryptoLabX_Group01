#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <cctype>
#include <sstream>

using namespace std;

// ------------------------------------------------------------
// Global constants
// ------------------------------------------------------------

const string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Secret monoalphabetic substitution key.
// Plaintext letter -> Ciphertext letter
// This key is NOT displayed during normal execution.
const string ENCRYPTION_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM";

// ------------------------------------------------------------
// Utility function
// ------------------------------------------------------------

string cleanWord(const string& word)
{
    string result;

    for (char c : word)
    {
        if (isalpha(static_cast<unsigned char>(c)))
            result += toupper(static_cast<unsigned char>(c));
    }

    return result;
}

// ------------------------------------------------------------
// Encrypt plaintext
// ------------------------------------------------------------

string encryptText(const string& plaintext)
{
    string ciphertext = plaintext;

    for (size_t i = 0; i < plaintext.length(); i++)
    {
        char c = plaintext[i];

        if (isalpha(static_cast<unsigned char>(c)))
        {
            bool lowercase = islower(static_cast<unsigned char>(c));
            char upper = toupper(static_cast<unsigned char>(c));

            int index = upper - 'A';
            char encrypted = ENCRYPTION_KEY[index];

            ciphertext[i] = lowercase ? tolower(encrypted) : encrypted;
        }
        else
        {
            ciphertext[i] = c;
        }
    }

    return ciphertext;
}

// ------------------------------------------------------------
// Read complete file
// ------------------------------------------------------------

string readFile(const string& filename)
{
    ifstream file(filename);

    if (!file)
    {
        cerr << "Error: Cannot open " << filename << endl;
        return "";
    }

    stringstream buffer;
    buffer << file.rdbuf();

    return buffer.str();
}

// ------------------------------------------------------------
// Write complete file
// ------------------------------------------------------------

void writeFile(const string& filename, const string& content)
{
    ofstream file(filename);

    if (!file)
    {
        cerr << "Error: Cannot write " << filename << endl;
        return;
    }

    file << content;
}

// ------------------------------------------------------------
// 1. frequency_analysis()
// ------------------------------------------------------------

void frequency_analysis(const string& ciphertext)
{
    vector<int> frequency(26, 0);

    int totalLetters = 0;

    for (char c : ciphertext)
    {
        if (isalpha(static_cast<unsigned char>(c)))
        {
            char upper = toupper(static_cast<unsigned char>(c));
            frequency[upper - 'A']++;
            totalLetters++;
        }
    }

    vector<pair<char, int>> results;

    for (int i = 0; i < 26; i++)
    {
        results.push_back({char('A' + i), frequency[i]});
    }

    sort(results.begin(), results.end(),
         [](const pair<char, int>& a, const pair<char, int>& b)
         {
             return a.second > b.second;
         });

    cout << "\n============================================\n";
    cout << "        LETTER FREQUENCY ANALYSIS\n";
    cout << "============================================\n";

    cout << left << setw(10) << "Letter"
         << setw(10) << "Count"
         << setw(15) << "Percentage" << endl;

    cout << "--------------------------------------------\n";

    for (auto& item : results)
    {
        double percentage = 0.0;

        if (totalLetters > 0)
            percentage = (item.second * 100.0) / totalLetters;

        cout << left << setw(10) << item.first
             << setw(10) << item.second
             << fixed << setprecision(2)
             << percentage << "%" << endl;
    }

    cout << "\nMost frequent ciphertext letters:\n";

    for (int i = 0; i < 5; i++)
    {
        cout << results[i].first
             << " (" << results[i].second << " occurrences)\n";
    }
}

// ------------------------------------------------------------
// 2. word_frequency_analysis()
// ------------------------------------------------------------

void word_frequency_analysis(const string& ciphertext)
{
    map<string, int> wordFrequency;

    string currentWord;

    for (char c : ciphertext)
    {
        if (isalpha(static_cast<unsigned char>(c)))
        {
            currentWord += toupper(static_cast<unsigned char>(c));
        }
        else
        {
            if (!currentWord.empty())
            {
                wordFrequency[currentWord]++;
                currentWord.clear();
            }
        }
    }

    if (!currentWord.empty())
        wordFrequency[currentWord]++;

    cout << "\n============================================\n";
    cout << "          WORD FREQUENCY ANALYSIS\n";
    cout << "============================================\n";

    cout << "\nONE-LETTER WORDS:\n";

    for (auto& item : wordFrequency)
    {
        if (item.first.length() == 1)
            cout << item.first << " -> "
                 << item.second << " times\n";
    }

    cout << "\nTWO-LETTER WORDS:\n";

    for (auto& item : wordFrequency)
    {
        if (item.first.length() == 2)
            cout << item.first << " -> "
                 << item.second << " times\n";
    }

    cout << "\nTHREE-LETTER WORDS:\n";

    for (auto& item : wordFrequency)
    {
        if (item.first.length() == 3)
            cout << item.first << " -> "
                 << item.second << " times\n";
    }

    cout << "\nREPEATED WORDS:\n";

    for (auto& item : wordFrequency)
    {
        if (item.second > 1)
        {
            cout << item.first << " -> "
                 << item.second << " times\n";
        }
    }
}

// ------------------------------------------------------------
// Generate repeated-letter pattern
// ------------------------------------------------------------

string generatePattern(const string& word)
{
    map<char, int> mapping;

    string pattern;
    int nextNumber = 0;

    for (char c : word)
    {
        if (mapping.find(c) == mapping.end())
        {
            mapping[c] = nextNumber++;
        }

        pattern += to_string(mapping[c]);
    }

    return pattern;
}

// ------------------------------------------------------------
// 3. pattern_analysis()
// ------------------------------------------------------------

void pattern_analysis(const string& ciphertext)
{
    map<string, int> patternFrequency;

    string currentWord;

    for (char c : ciphertext)
    {
        if (isalpha(static_cast<unsigned char>(c)))
        {
            currentWord += toupper(static_cast<unsigned char>(c));
        }
        else
        {
            if (!currentWord.empty())
            {
                string pattern = generatePattern(currentWord);

                patternFrequency[pattern]++;

                currentWord.clear();
            }
        }
    }

    if (!currentWord.empty())
    {
        string pattern = generatePattern(currentWord);
        patternFrequency[pattern]++;
    }

    cout << "\n============================================\n";
    cout << "             PATTERN ANALYSIS\n";
    cout << "============================================\n";

    currentWord.clear();

    stringstream ss(ciphertext);
    string word;

    map<string, bool> displayed;

    while (ss >> word)
    {
        string cleaned = cleanWord(word);

        if (!cleaned.empty() && !displayed[cleaned])
        {
            displayed[cleaned] = true;

            cout << left << setw(20)
                 << cleaned
                 << " Pattern: "
                 << generatePattern(cleaned)
                 << endl;
        }
    }

    cout << "\nPattern frequency:\n";

    for (auto& item : patternFrequency)
    {
        cout << item.first << " -> "
             << item.second << " occurrence(s)\n";
    }
}

// ------------------------------------------------------------
// 4. apply_substitution()
// ------------------------------------------------------------

// mapping[ciphertext letter - 'A'] = guessed plaintext letter
string apply_substitution(const string& ciphertext,
                          const string& mapping)
{
    string result = ciphertext;

    for (size_t i = 0; i < ciphertext.length(); i++)
    {
        char c = ciphertext[i];

        if (isalpha(static_cast<unsigned char>(c)))
        {
            bool lowercase = islower(static_cast<unsigned char>(c));
            char upper = toupper(static_cast<unsigned char>(c));

            int index = upper - 'A';

            if (index >= 0 && index < 26 &&
                mapping[index] != '?')
            {
                char replacement = mapping[index];

                result[i] = lowercase
                    ? tolower(replacement)
                    : replacement;
            }
            else
            {
                result[i] = '?';
            }
        }
    }

    return result;
}

// ------------------------------------------------------------
// 5. display_partial_plaintext()
// ------------------------------------------------------------

void display_partial_plaintext(const string& ciphertext,
                               const string& mapping)
{
    cout << "\n============================================\n";
    cout << "           PARTIAL PLAINTEXT\n";
    cout << "============================================\n\n";

    cout << apply_substitution(ciphertext, mapping) << endl;

    cout << "\nCurrent substitutions:\n";

    for (int i = 0; i < 26; i++)
    {
        if (mapping[i] != '?')
        {
            cout << char('A' + i)
                 << " -> "
                 << mapping[i] << endl;
        }
    }
}

// ------------------------------------------------------------
// Create encryption key from recovered decryption mapping
// ------------------------------------------------------------

string createEncryptionKey(const string& decryptionMapping)
{
    string encryptionKey(26, '?');

    for (int cipherIndex = 0; cipherIndex < 26; cipherIndex++)
    {
        char plaintextLetter = decryptionMapping[cipherIndex];

        if (plaintextLetter != '?')
        {
            int plainIndex = plaintextLetter - 'A';

            if (plainIndex >= 0 && plainIndex < 26)
            {
                encryptionKey[plainIndex] =
                    char('A' + cipherIndex);
            }
        }
    }

    return encryptionKey;
}

// ------------------------------------------------------------
// Encrypt using a recovered key
// ------------------------------------------------------------

string encryptWithKey(const string& plaintext,
                      const string& encryptionKey)
{
    string ciphertext = plaintext;

    for (size_t i = 0; i < plaintext.length(); i++)
    {
        char c = plaintext[i];

        if (isalpha(static_cast<unsigned char>(c)))
        {
            bool lowercase =
                islower(static_cast<unsigned char>(c));

            char upper =
                toupper(static_cast<unsigned char>(c));

            int index = upper - 'A';

            char encrypted = encryptionKey[index];

            ciphertext[i] =
                lowercase ? tolower(encrypted) : encrypted;
        }
    }

    return ciphertext;
}

// ------------------------------------------------------------
// 6. verify_solution()
// ------------------------------------------------------------

void verify_solution(const string& ciphertext,
                     const string& recoveredMapping)
{
    for (char c : recoveredMapping)
    {
        if (c != '?' && !isalpha(static_cast<unsigned char>(c)))
        {
            cout << "\nInvalid key.\n";
            return;
        }
    }

    string plaintext =
        apply_substitution(ciphertext, recoveredMapping);

    cout << "\n============================================\n";
    cout << "           RECOVERED PLAINTEXT\n";
    cout << "============================================\n\n";

    cout << plaintext << endl;

    string encryptionKey =
        createEncryptionKey(recoveredMapping);

    for (char c : encryptionKey)
    {
        if (c == '?')
        {
            cout << "\nVerification cannot be completed.\n";
            cout << "The recovered key is incomplete.\n";
            return;
        }
    }

    string reEncrypted =
        encryptWithKey(plaintext, encryptionKey);

    if (reEncrypted == ciphertext)
    {
        cout << "\n============================================\n";
        cout << "          VERIFICATION SUCCESS\n";
        cout << "============================================\n";

        cout << "\nRecovered Key:\n";
        cout << "Cipher : " << ALPHABET << endl;
        cout << "Plain  : " << recoveredMapping << endl;

        cout << "\nRe-encryption matches original ciphertext.\n";
        cout << "The recovered substitution key is CORRECT.\n";
    }
    else
    {
        cout << "\n============================================\n";
        cout << "          VERIFICATION FAILED\n";
        cout << "============================================\n";

        cout << "\nThe recovered substitutions are not completely correct.\n";
        cout << "Continue cryptanalysis.\n";
    }
}

// ------------------------------------------------------------
// Update substitution mapping
// ------------------------------------------------------------

void addSubstitution(string& mapping)
{
    char cipher;
    char plain;

    cout << "\nEnter ciphertext letter: ";
    cin >> cipher;

    cout << "Enter suspected plaintext letter: ";
    cin >> plain;

    cipher = toupper(static_cast<unsigned char>(cipher));
    plain = toupper(static_cast<unsigned char>(plain));

    if (cipher < 'A' || cipher > 'Z' ||
        plain < 'A' || plain > 'Z')
    {
        cout << "Invalid letters.\n";
        return;
    }

    mapping[cipher - 'A'] = plain;

    cout << "\nSubstitution added: "
         << cipher << " -> " << plain << endl;
}

// ------------------------------------------------------------
// Display original encryption key
// Used only when the user explicitly chooses the option.
// Useful for understanding/testing the implementation.
// ------------------------------------------------------------

void displayOriginalKey()
{
    cout << "\nOriginal Encryption Key:\n";
    cout << "Plain : " << ALPHABET << endl;
    cout << "Cipher: " << ENCRYPTION_KEY << endl;
}

// ------------------------------------------------------------
// Main
// ------------------------------------------------------------

int main()
{
    string plaintext;
    string ciphertext;

    string recoveredMapping(26, '?');

    int choice;

    cout << "============================================\n";
    cout << "   MONOALPHABETIC SUBSTITUTION CIPHER\n";
    cout << "          AND CRYPTANALYSIS\n";
    cout << "============================================\n";

    while (true)
    {
        cout << "\n\n========== MENU ==========\n";
        cout << "1. Encrypt plaintext\n";
        cout << "2. Frequency Analysis\n";
        cout << "3. Word Frequency Analysis\n";
        cout << "4. Pattern Analysis\n";
        cout << "5. Apply Substitution\n";
        cout << "6. Display Partial Plaintext\n";
        cout << "7. Verify Solution\n";
        cout << "8. Display Original Key\n";
        cout << "9. Exit\n";
        cout << "==========================\n";

        cout << "Enter choice: ";
        cin >> choice;

        if (choice == 1)
        {
            plaintext = readFile("plaintext.txt");

            if (plaintext.empty())
            {
                cout << "Plaintext file is empty or could not be read.\n";
                continue;
            }

            ciphertext = encryptText(plaintext);

            writeFile("ciphertext.txt", ciphertext);

            cout << "\nEncryption completed successfully.\n";
            cout << "Ciphertext saved to ciphertext.txt\n";
        }

        else if (choice == 2)
        {
            if (ciphertext.empty())
                ciphertext = readFile("ciphertext.txt");

            if (ciphertext.empty())
            {
                cout << "No ciphertext available.\n";
                continue;
            }

            frequency_analysis(ciphertext);
        }

        else if (choice == 3)
        {
            if (ciphertext.empty())
                ciphertext = readFile("ciphertext.txt");

            if (ciphertext.empty())
            {
                cout << "No ciphertext available.\n";
                continue;
            }

            word_frequency_analysis(ciphertext);
        }

        else if (choice == 4)
        {
            if (ciphertext.empty())
                ciphertext = readFile("ciphertext.txt");

            if (ciphertext.empty())
            {
                cout << "No ciphertext available.\n";
                continue;
            }

            pattern_analysis(ciphertext);
        }

        else if (choice == 5)
        {
            if (ciphertext.empty())
                ciphertext = readFile("ciphertext.txt");

            if (ciphertext.empty())
            {
                cout << "No ciphertext available.\n";
                continue;
            }

            addSubstitution(recoveredMapping);
        }

        else if (choice == 6)
        {
            if (ciphertext.empty())
                ciphertext = readFile("ciphertext.txt");

            if (ciphertext.empty())
            {
                cout << "No ciphertext available.\n";
                continue;
            }

            display_partial_plaintext(ciphertext,
                                      recoveredMapping);
        }

        else if (choice == 7)
        {
            if (ciphertext.empty())
                ciphertext = readFile("ciphertext.txt");

            if (ciphertext.empty())
            {
                cout << "No ciphertext available.\n";
                continue;
            }

            verify_solution(ciphertext,
                            recoveredMapping);
        }

        else if (choice == 8)
        {
            displayOriginalKey();
        }

        else if (choice == 9)
        {
            cout << "\nExiting program...\n";
            break;
        }

        else
        {
            cout << "\nInvalid choice. Try again.\n";
        }
    }

    return 0;
}
