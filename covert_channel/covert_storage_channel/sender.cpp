#include <iostream>
#include <stdio.h>
#include <time.h>
#include <windows.h>
#include <string>
#include <sstream>
#include <algorithm>
#include <bitset>

using namespace std;
// Define the default path using any desired path and folder name

#define PATH "H:\\PycharmProjects\\Security\\covert_channel\\covert_storage_channel\\import"
#define STOP "H:\\PycharmProjects\\Security\\covert_channel\\covert_storage_channel\\export"		// used by receiver to signal the sender to stop

bool dirExists(const string & dirName_in){
	DWORD ftyp = GetFileAttributesA(dirName_in.c_str());
	if (ftyp == INVALID_FILE_ATTRIBUTES){
		return false;	// Something wrong with your path
	}

	if (ftyp & FILE_ATTRIBUTE_DIRECTORY){
		return true;	// This is a directory
	}

	return false;	// This is not a directory
}


void CreateFolder(const char * path){
	if (!CreateDirectory(path, NULL)){	// Create path(directory) fail: 0, success: 1
		return;	
	}
}

void DeleteFolder(const char * path){
	if (!RemoveDirectory(path)){		// Remove path(directory) fail: 0, success: 1
		return;
	}
}

void sendBitMessage(char input){
	int code = int(input);
	cout << "Sending: " << input << "(";
	string temp = bitset<8>(code).to_string();
	while (temp.length() < 8)
		temp = "0" + temp;
	string code_p = temp;
	reverse(temp.begin(), temp.end());	// reverse the input to send	01101 -> 10110 => 1 0 1 1 0
	// code = stoi(temp)
	cout << code_p << ")" << endl;		// print input in bit string
	bool zeroFlag = false;
	for (int i = 0; i < 8; i++){
		if (dirExists(STOP))
			break;
		Sleep(1000);			// in order to sync both sender and receiver
		if (temp.back() == '1'){	// if bit is 1, create
			CreateFolder(PATH);
		}else {
			DeleteFolder(PATH);
		}
		// code = code / 10;
		temp = temp.substr(0, temp.size() - 1);
	}
}

int main(){
	DeleteFolder(STOP);
	DeleteFolder(PATH);

	string message;
	cout << "Write a message to send:\n";
	getline(cin, message);
	message.erase(remove_if(message.begin(), message.end(), isspace), message.end());	// Trimming the message
	int messageLen = message.length();
	while (!dirExists(STOP)){
		cout << "Signaling...\n";
		sendBitMessage('%');
		sendBitMessage('$');
		for (int i = 0; i < messageLen; i++){
			sendBitMessage(message.at(i));
			if (dirExists(STOP))
				break;
		}
		sendBitMessage('$');
		sendBitMessage('%');
	}
	return 0;
}
