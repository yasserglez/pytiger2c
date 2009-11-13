struct main_scope
{
    int64_t a;
    int64_t b;
    int64_t c;
};


int main()
{
    struct main_scope* scope;
    
    /* Reservar memoria para la estructura scope */

    scope->a = 5;
    scope->b = 10;
    scope->c = 0;
    scope->c = scope->a + scope->b;

    /* Liberar memoria de la estructura scope */
}
