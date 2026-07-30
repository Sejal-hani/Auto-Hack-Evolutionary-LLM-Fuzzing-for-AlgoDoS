// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 16
// [N_CONSTRAINT]: 50
// [INPUT_FORMAT]: T; per case: N, then string S of length N. 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int main(){
   int test;
   scanf("%d", &test);
   // test = 1;
   char s[51];
   char ans[51];
   while(test--){
       int n;
       scanf("%d", &n);
       scanf("\n");
       scanf("%s", s);
       scanf("\n");
       int len = 0;
       for(int i = n - 1; i >= 0; i--){
           if(s[i] == '0'){
               int temp = s[i - 1] - '0' + (s[i - 2] - '0')*10 - 1;
               ans[len] = 'a' + temp;
               len++;
               i -= 2;
           }else{
               ans[len] = 'a' + (s[i] - '0') - 1;
               len++;
           }
       }
       for(int i = len - 1; i >= 0; i--){
           printf("%c", ans[i]);
       }
       printf("\n");
   }
   return 0;
}