int a;
int b, c;
int d;
float e;
float f;

function int test_t62(int a) {
  b = 1;
  c = 10;
  e = 5.0;
  f = e * c;
  if (c > b)
  {
    d = 5;
    c = c + -b
  }
  else
  {
    while (b < 5) {
        c = -d * b;
	b = b + 1
    }
  };
  print c;
  return c
}

main () {
   int retval;
   retval = test_t62(3);
   print (retval)
}
