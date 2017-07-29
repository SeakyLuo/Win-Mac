#include <iostream>
#include <string>

struct p{
   string a;
   string b;
   string c;
};

int main(){
   p p1 = { a="1", b="2", c="3"};
   std::cout << p1.a << " " << p1.b << " " << p1.c << std::endl;
}
