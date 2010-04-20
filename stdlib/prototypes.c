
/* Tiger standard library functions. */

void tiger_print(struct tiger_string *s);

void tiger_printi(int n);

void tiger_flush(void *scope);

struct tiger_string *tiger_getchar(void *scope);

int tiger_ord(struct tiger_string *s);

struct tiger_string *tiger_chr(int i);

int tiger_size(struct tiger_string *s);

struct tiger_string *tiger_substring(struct tiger_string *s, int f, int n);

struct tiger_string *tiger_concat(struct tiger_string *s1, struct tiger_string *s2);

int tiger_not(int i);

int tiger_exit(int i);

/* Internal functions used by PyTiger2C. */

void pytiger2c_error(char *msg);

void *pytiger2c_malloc(size_t size);

int pytiger2c_strcmp(struct tiger_string *a, struct tiger_string *b);

/* Functions defined in the program. */

