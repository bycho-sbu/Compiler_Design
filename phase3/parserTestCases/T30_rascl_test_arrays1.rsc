int a[5], b;
float c, d[4];

function int test_t30 () {
  a[2] = 5;
  b = a[2] * 2;
  print b;
  return b
}

main() {
   int retval;
   retval = test_t30()
}
