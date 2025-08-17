int a;
int b;
int theSum;
int bignum;

function dude(int a, int b)
{
    theSum = a * a + b * b;
    return theSum;
}

{
  a = 5;
  b = 10;

  bignum = dude(a, b);
  print bignum
}
