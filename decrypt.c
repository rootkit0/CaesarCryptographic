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

char desencriptar_char(int clau, char c) {
    char desencriptat;
    if(isalpha(c)) {
        if(isupper(c)) {
            desencriptat = ((((c - 65) + clau)%23) + 65);
            desencriptat = toupper(desencriptat);
        }
        if(islower(c)) {
            desencriptat = ((((c - 65) + clau)%23) + 65);
            desencriptat = tolower(desencriptat);
        }
        if(desencriptat == 'J' || desencriptat == 'j' || desencriptat == 'K' || desencriptat == 'k' || desencriptat == 'W' || desencriptat == 'w') {
            desencriptat -= 1;
        }
        return desencriptat;
    }
    else {
        return c;
    }
}

void desencriptar_arxiu(int clau, FILE *file1, FILE *file2) {
    char actual, desencriptat;
    while((actual=fgetc(file1))!=EOF){
        desencriptat = desencriptar_char(key_algorithm(clau), actual);
        fputc(desencriptat, file2);
    }
}

int main (int argc, char *argv[]) {
    //Cas de llegir per stdin
    if(argc == 2) {
        char c = getc(stdin), desencriptat;
        while(c != '\n' && c != EOF) {
            desencriptat = desencriptar_char(atoi(argv[1]), c);
            printf("%c", desencriptat);
            c = getc(stdin);
        }
    }
    //Cas de llegir per fitxers
    else if(argc > 2) {
        int clau = atoi(argv[1]);
        FILE *coded_file;
        coded_file = fopen(argv[2], "r");
        FILE *decoded_file;
        decoded_file = fopen(argv[3], "w");
        desencriptar_arxiu(clau, coded_file, decoded_file);
        fclose(decoded_file);
        fclose(coded_file);
    }
    //L'usuari no ha proporcionat cap clau
    else {
        printf("Us: ./decrypt clau [fitxer codificat] [fitxer en clar]\n");
    }
}