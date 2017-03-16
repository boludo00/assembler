#include "stdio.h"

int getHammDist(int, int);
int getMaxHamming(int [], int);

int getMaxHamming(int arr[], int len) {
	int maxHamming = 0;

	for(int i = 0; i < len; ++i) {

		int curr_val = arr[i];


		for(int j = i + 1; j < len; ++j) {
			int nextElement = arr[j];
			int ham = getHammDist(curr_val, nextElement);
			if(ham > maxHamming) {
				maxHamming = ham;
			}
		}
	}
	return maxHamming;
}

int getHammDist(int a, int b) {

	int count = 0;

	for(int i = 0; i < sizeof(int); ++i) {
		if((a&1) != (b&1)) {
			count++;
		}
		a = a >> 1;
		b = b >> 1;
	}

	return count;


}


int main(int argc, char* argv[]) {

	int arr[4] = {0, 0, 0, 15};
	int len = sizeof(arr)/sizeof(arr[0]);


	fprintf(stderr, "getMaxHamming()=> %d\n", getMaxHamming(arr, len));


	return 0;
}
