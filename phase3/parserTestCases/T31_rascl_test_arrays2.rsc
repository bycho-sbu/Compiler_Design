int a[5];
int i;

function void test_t31 () {
  i = 0;
  while (i < 5) {
    a[i] = i*i;
    i = i + 1
  };
  i = 0;
  while (i < 5) {
    print a[i];
    i = i + 1
  }
}

main() {
   call test_t31()
}
