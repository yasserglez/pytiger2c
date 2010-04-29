struct scope1 {
    int a;
    int b;
    int c;
};

int main()
{
    struct scope1* scope;
    
    /* Reservar memoria para la estructura scope. */

    scope->a = 5;
    scope->b = 10;
    scope->c = 0;
    scope->c = scope->a + scope->b;
}
