#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int key_algorithm(int clau) {
    int actual = clau, suma_digits = 0;
    while(actual != 0) {
        suma_digits += actual%10;
        actual /= 10;
    }
    suma_digits *= 7;
    suma_digits %= 23;
    return suma_digits;
}

char encriptar_char(int clau, char c) {
    char encriptat;
    if(isalpha(c)) {
        if(isupper(c)) {
            encriptat = ((((c - 65) + clau)%23) + 65);
            encriptat = toupper(encriptat);
        }
        if(islower(c)) {
            encriptat = ((((c - 65) + clau)%23) + 65);
            encriptat = tolower(encriptat);
        }
        if(encriptat == 'J' || encriptat == 'j' || encriptat == 'K' || encriptat == 'k' || encriptat == 'W' || encriptat == 'w') {
            encriptat += 1;
        }
        return encriptat;
    }
    else {
        return c;
    }
}

void encriptar_arxiu(int clau, FILE *file1, FILE *file2) {
    char actual, encriptat;
    while((actual=fgetc(file1))!=EOF){
        encriptat = encriptar_char(key_algorithm(clau), actual);
        fputc(encriptat, file2);
    }
}

int main (int argc, char *argv[]) {
    //Cas de llegir per stdin
    if(argc == 2) {
        char c = getc(stdin), encriptat;
        while(c != '\n' && c != EOF) {
            encriptat = encriptar_char(atoi(argv[1]), c);
            printf("%c", encriptat);
            c = getc(stdin);
        }
    }
    //Cas de llegir per fitxers
    else if(argc > 2) {
        int clau = atoi(argv[1]);
        FILE *decoded_file;
        decoded_file = fopen(argv[2], "r");
        FILE *coded_file;
        coded_file = fopen(argv[3], "w");
        encriptar_arxiu(clau, decoded_file, coded_file);
        fclose(decoded_file);
        fclose(coded_file);
    }
    //L'usuari no ha proporcionat cap clau
    else {
        printf("Us: ./encrypt clau [fitxer en clar] [fitxer codificat]\n");
    }
}