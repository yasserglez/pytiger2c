struct main_scope
{
    int64_t c;
};

struct f_scope
{
    struct main_scope* parent;
    int64_t v;
};

struct g_scope
{
    struct f_scope* parent;
    int64_t h;
};

int64_t f(struct main_scope* parent, int64_t v);
int64_t g(struct f_scope* parent, int64_t h);

int64_t f(struct main_scope* parent, int64_t v)
{
    struct f_scope* scope;
    int64_t local_var;
    int64_t local_var1;

    /* Reservar memoria para la estructura scope */

    scope->parent = parent;
    scope->v = v;

    local_var = g(scope, 5);
    local_var1=(local_var);

    /* Liberar memoria de la estructura scope */

    return local_var1;
}

int64_t g(struct f_scope* parent, int64_t h)
{
    struct g_scope* scope;
    int64_t local_var;

    /* Reservar memoria para la estructura scope */

    scope->parent = parent;
    scope->h = h;
    local_var = scope->parent->v + scope->h;

    /* Liberar memoria de la estructura scope */

    return local_var;
}

int main()
{
    struct main_scope* scope;
    int64_t local_var;

    /* Reservar memoria para la estructura scope */

    scope->c = 0;
    local_var = f(scope, 10);
    scope->c = local_var;

    /* Liberar memoria de la estructura scope */

}
