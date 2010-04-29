struct scope1 {
    int c;
};

struct scope2 {
    struct scope1 *parent;
    int a;
    int b;
};

int f(struct scope1 *parent, int a, int b)
{
    struct scope2 *scope;
    int local_var1;

    /* Reservar memoria para la estructura scope. */

    scope->parent = parent;
    scope->a = a;
    scope->b = b;
    local_var1 = scope->a + scope->b;

    return local_var1;
}

int main()
{
    struct scope1 *scope;

    /* Reservar memoria para la estructura scope. */

    scope->c =  0;
    scope->c = f(scope, 5, 10);
}
