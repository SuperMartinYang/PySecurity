#include <iostream>
#include <stdio.h>
#include <time.h>
#include <windows.h>
#include <string.h>
#include <sstream>
#include <algorithm>
#include <iomanip>

using namespace std;

#define PATH "H:\\PycharmProjects\\Security\\covert_channel\\covert_storage_channel\\import"
#define STOP "H:\\PycharmProjects\\Security\\covert_channel\\covert_storage_channel\\export"		// used by receiver to signal the sender to stop

void resetArray(int arr[]){
	for (int i = 0; i < 8; i++){
		arr[i] = 0;
	}
}

int binaryToDecimal(int input){		// Converting a binary integer to the relevant decimal value
	int in = input;
	int multiplier = 1;
	int temp = 0;
	for (int i = 0; i < 8; i++){
		temp = (in % 10) * multiplier + temp;
		multiplier *= 2;
		in = in / 10;
	}
	return temp;
}


void shiftAndAppend(int arr[], int element){
	for (int i = 1; i < 8; i++){
		arr[i - 1] = arr[i];
	}
	arr[7] = element;
}

/**
 * TO-DO
 */
int arrToChar(int arr[]){
	int temp = 0;
	int multiplier = 1;
	for (int i = 0; i < 8; i++){
		temp = (arr[i] * multiplier) + temp;
		multiplier *= 10;
	}
	temp = binaryToDecimal(temp);
	return char(temp);
}

bool dirExists(const string & dirName_in){
	DWORD ftyp = GetFileAttributesA(dirName_in.c_str);
	if (ftyp == INVALID_FILE_ATTRIBUTES)
		return false;
	if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
		return true;
	return false;
}

bool CreateFolder(const char * path){
	if (!CreateDirectory(path, NULL))
		return;
}

void DeleteFolder(const char * path){
	if (!DeleteDirectory(path))
		return;
}

int recBitMessage(){
	Sleep(1000);
	if (!dirExists(PATH)){
		return 0;
	}else {
		return 1;
	}
}

/**
 * TO-DO
 * */
char readMessage(){
	int msgChar = 0;
	int multiplier = 1;
	for (int i = 0; i < 8; i++){
		msgChar = msgChar * multiplier + recBitMessage();
		mulitplier *= 10;
	}
}



int main(){
	int count = 0;
	char restart;
	int msgArray[8] = {0, 0, 0, 0, 0, 0, 0, 0};
	char msgChar;
	bool firstSign = false;
	bool secondSign = false;

	bool firstOff = false;
	bool secondOff = false;

	int cnt = 0;
	bool exit = true;

	cout << "Waiting to capture...\n";

	while (exit){
		if (!firstSign && !secondSign){
			shiftAndAppend(msgArray, recBitMessage());
			msgChar = arrToChar(msgArray);
			cnt++;
			if (msgChar == '%'){
				cout << "Probable signaling...\n";
				resetArray(msgArray);
				cnt = 0;
				firstSign = true;
			}
		}

		if (firstSign && !secondSign){
			shiftAndAppend(msgArray, recBitMessage());
			msgChar = arrToChar(msgArrar);
			cnt++;
			if (cnt == 8){
				resetArray(msgArray);
				cnt = 0;
				cout << endl << "Message started:\n";
				if (msgChar == '$'){
					secondSign = true;
				}
			}
		}

		if (firstSign && secondSign){
			shiftAndAppend(msgArray, recBitMessage());
			msgChar = arrToChar(msgArray);
			cnt++;
			if (cnt == 8){
				resetArray(msgArray);
				cnt = 0;
				cout << "Received:" << msgChar << endl;
				if (msgChar == '$'){		// probably end
					firstOff = true;
					firstSign = false;
				}
			}
		}

		if (firstOff && !secondOff){
			shiftAndAppend(msgArray, recBitMessage());
			msgChar = arrToChar(msgArray);
			cnt++;
			if (cnt == 8){
				resetArray(msgArray);
				cnt = 0;
				cout << msgChar << endl;

				if (msgChar == '%'){
					secondOff = true;
				}
			}
		}

		if (firstOff && secondOff){
			resetArray(msgArray);
			cout << "Message fully received!\n";
			cout << "Quiting...\n";
			CreateFolder(STOP);
			Sleep(5000);
			DeleteFolder(STOP);
			DeleteFolder(PATH);

			exit = false;
		}
	}
	return 0;
}
