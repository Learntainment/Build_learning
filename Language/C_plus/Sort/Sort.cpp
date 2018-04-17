#include <iostream>
#include <time.h>
#include <random>
#include <cstring>

using namespace std;

void Swap1(int &a, int &b) {
    if (a != b) {
        a = a^b;
        b = a^b;
        a = a^b;
    }
}

void Swap2(int *p, int *q) {
    *p = *p+*q;
    *q = *p-*q;
    *p = *p-*q;
}

void Quick_Sort(int array[], int low, int high) {
    int i = low;
    int j = high;
    int x = array[i];
    if (i<j) {
        while (i<j) {
            while (i<j && array[j]>=x) {
                j--;
            }
            if (i<j) {
                array[i] = array[j];
                i++;
            }

            while (i<j && array[i]<=x) {
                i++;
            }
            if (i<j) {
                array[j] = array[i];
                j--;
            }
        }
        array[i] = x;
        Quick_Sort(array, low, i-1);
        Quick_Sort(array, i+1, high);
    }
}

void Bubble1_Sort(int array[], int low, int high) {
    int i = low;
    int boundary = high;
    int tmp = 0;
    for (i; i <= boundary; i++) {
        for (int j = low; j <= boundary-1; j++) {
            if (array[j] > array[j+1]) {
                tmp = array[j];
                array[j] = array[j+1];
                array[j+1] = tmp;
            }
        }
    }
}

void Bubble2_Sort(int array[], int low, int high) {
    int i = low;
    int boundary = high;
    int tmp = 0;
    for (i; i <= boundary; i++) {
        for (int j = 1; j <= boundary-i; j++) {
            if (array[j-1] > array[j]) {
                tmp = array[j-1];
                array[j-1] = array[j];
                array[j] = tmp;
            }
        }
    }
}

void Bubble3_Sort(int array[], int low, int high) {
    int j, k, tmp;
    bool flag;

    k = high-low+1;
    flag = true;
    while (flag) {
    	flag = false;
        for (j = 1; j < k; j++)
        	if (array[j - 1] > array[j]) {
            	tmp = array[j-1];
			    array[j-1] = array[j];
				array[j] = tmp;
                flag = true;
            }
       	k--;
    }
}

void Bubble4_Sort(int array[], int low, int high) {
	int j, k, tmp;
    int flag;

    flag = high-low+1;
    while (flag > 0) {
        k = flag;
        flag = 0;
        for (j = 1; j < k; j++)
            if (array[j - 1] > array[j]) {
                tmp = array[j-1];
                array[j-1] = array[j];
                array[j] = tmp;
                flag = j;
            }
    }
}

void Insert1_Sort(int array[], int low, int high) {
    // 每一次比较就是把i和j+1的位置置换
    int i, j, k;
    int n = high-low+1;
    int count = 0;
    for (i = 1; i < n; i++) {
        for (j = i - 1; j >= 0; j--)
            if (array[j] < array[i])
                break;
        if (j != i - 1) {
            int temp = array[i];
            for (k = i - 1; k > j; k--)
                array[k + 1] = array[k];
            array[j + 1] = temp;
        }
    }
}

void Insert2_Sort(int array[], int low, int high) {
    int count = high-low+1;
    int i,j;
    for (i=1; i<count; i++) {
        if (array[i] < array[i-1]) {
            int temp = array[i];
            for (j=i-1; j>=0&&array[j]>temp; j--) {
                array[j+1] = array[j];
            }
            array[j+1] = temp;
        }
    }
}

void Insert3_Sort(int array[], int low, int high) {
    int count = high-low+1;
    int i,j;
    for (i=1; i<count; i++) {
        for (j=i-1; j>=0&&array[j+1]<array[j]; j--) {
            int temp = array[j];
            array[j] = array[j+1];
            array[j+1] = temp;
        }
    }
}

void Select_Sort(int array[], int low, int high) {
    int count = high-low+1;
    int i, j, min_n;
    for (i = 0; i < count; i++) {
        min_n = i;
        for (j = i+1; j < count; j++) {
            if (array[j] < array[min_n]) {
                min_n = j;
            }
        }
        Swap1(array[i], array[min_n]);
    }
}

void Find_Once () {
    const int MAXN = 15;
    int a[MAXN] = {1, 347, 6, 9, 13, 65, 889, 712, 889, 347, 1, 9, 65, 13, 712};
    int lostNum = 0;
    for (int i = 0; i < MAXN; i++) {
        lostNum ^= a[i];
        cout << "lostNum: " << lostNum << endl;;
    }
    cout << "lost one is: " << lostNum << endl;
}

void Func_timer(void func(int*, int, int), int array[], int low, int high) {
    clock_t startTime,endTime;
    startTime = clock();
    func(array, low, high);
    endTime = clock();
    cout << "Totle Time : " << (double)(endTime - startTime) / CLOCKS_PER_SEC << "s" << endl;
}


void Random_seed(int array[], int count) {
    int n = count;
    default_random_engine random_e;
    uniform_int_distribution<int> uniform_d(0, 100);
    for (int i=0; i<n; i++) {
        array[i] = uniform_d(random_e);
    }
}

void Output(int array[], int low, int high) {
    for (int a = low; a <= high; a ++) {
        cout << "sort array: " << array[a] << endl;
    }
}

int main() {
    int array[30] = {72, 6, 57, 88, 60, 42, 83, 73, 48, 85, 1, 3, 9, 4, 6, 43, 44, 57, 89, 100, 38, 40, 29, 21, 45, 65, 88, 56, 89, 90};
    //int b1_array[30] = {72, 6, 57, 88, 60, 42, 83, 73, 48, 85, 1, 3, 9, 4, 6, 43, 44, 57, 89, 100, 38, 40, 29, 21, 45, 65, 88, 56, 89, 90};
    //int b2_array[30] = {72, 6, 57, 88, 60, 42, 83, 73, 48, 85, 1, 3, 9, 4, 6, 43, 44, 57, 89, 100, 38, 40, 29, 21, 45, 65, 88, 56, 89, 90};
    //int short_array[10] = {72, 6, 57, 88, 60, 42, 83, 73, 48, 85};

    int count = 100;
    int *new_array = new int[count];
    Random_seed(new_array, count);
    int *rd_array = new int[count];
    memcpy(rd_array, new_array, 100);
    int *rd_array1 = new int[count];
    memcpy(rd_array1, new_array, 100);

    //Func_timer(Quick_Sort, array, 0, 29);
    //Func_timer(Bubble1_Sort, b1_array, 0, 29);
    //Func_timer(Bubble2_Sort, b2_array, 0, 29);
    //Func_timer(Bubble3_Sort, b1_array, 0, 29);
    //Func_timer(Bubble4_Sort, b2_array, 0, 29);
    //Func_timer(Insert1_Sort, short_array, 0, 9);
    //Func_timer(Insert1_Sort, b2_array, 0, 29);
    //Func_timer(Quick_Sort, new_array, 0, 99);
    //Func_timer(Bubble2_Sort, rd_array1, 0, 99);
    //Func_timer(Insert2_Sort, rd_array, 0, 99);
    //Func_timer(Select_Sort, rd_array, 0, 99);

    //Output(array, 0, 29);
    //Output(b1_array, 0, 29);
    //Output(b2_array, 0, 29);
    //Output(short_array, 0, 9);
    //Output(rd_array, 0, 99);
    Find_Once();

}
