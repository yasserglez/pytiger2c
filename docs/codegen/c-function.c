struct main_scope
{
    int64_t c;
};

struct f_scope
{
    struct main_scope* parent;
    int64_t a;
    int64_t b;
};

int64_t f(struct main_scope* parent, int64_t a, int64_t b);

int64_t f(struct main_scope* parent, int64_t a, int64_t b)
{
    struct f_scope* scope;
    int64_t local_var;

    /* Reservar memoria para la estructura scope */

    scope->parent = parent;
    scope->a = a;
    scope->b = b;
    local_var= scope->a + scope->b;

    /* Liberar memoria de la estructura scope */

    return local_var;
}

int main()
{
    struct main_scope* scope;
    int64_t local_var;

    /* Reservar memoria para la estructura scope */

    scope->c =  0;
    local_var = f(scope, 5, 10);
    scope->c = local_var;

    /* Liberar memoria de la estructura scope */

}
