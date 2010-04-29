struct scope1 {
    int c;
};

struct scope2 {
    struct scope1 *parent;
    int v;
};

struct scope3 {
    struct scope2 *parent;
    int h;
};

int f(struct scope1 *parent, int v)
{
    struct scope2 *scope;
    int local_var1;

    /* Reservar memoria para la estructura scope. */

    scope->parent = parent;
    scope->v = v;
    local_var1 = g(scope, 5);

    return local_var1;
}

int g(struct scope2 *parent, int h)
{
    struct scope3 *scope;
    int local_var1;

    /* Reservar memoria para la estructura scope. */

    scope->parent = parent;
    scope->h = h;
    local_var1 = scope->parent->v + scope->h;

    return local_var1;
}

int main()
{
    struct scope1 *scope;

    /* Reservar memoria para la estructura scope. */

    scope->c = 0;
    scope->c = f(scope, 10);
}
