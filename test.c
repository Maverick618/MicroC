/*
just a test comment
*/

int num;

int factorial(int num){
    // num must be positive
    if(num == 1){
        return 1;
    }else{
        return num * factorial(num - 1);
    }
}
// I'm a test comment
int main(){
    num = 1;
    int res;
    char N;
    N = input();
    while(num <= N){
        res = factorial(num);
        print(res);
        num = num + 1;
    }
    return N << 1;
}