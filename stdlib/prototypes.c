
/* Tiger standard library functions. */

void tiger_print(void *scope, struct tiger_string *s);

void tiger_printi(void *scope, int64_t n);

void tiger_flush(void *scope);

struct tiger_string *tiger_getchar(void *scope);

int64_t tiger_ord(void *scope, struct tiger_string *s);

struct tiger_string *tiger_chr(void *scope, int64_t i);

int64_t tiger_size(void *scope, struct tiger_string *s);

struct tiger_string *tiger_substring(void *scope, struct tiger_string *s, int64_t f, int64_t n);

struct tiger_string *tiger_concat(void *scope, struct tiger_string *s1, struct tiger_string *s2);

int64_t tiger_not(void *scope, int64_t i);

int64_t tiger_exit(void *scope, int64_t i);

/* Internal functions used by PyTiger2C. */

void pytiger2c_error(char *msg);

void *pytiger2c_malloc(size_t size);

int64_t pytiger2c_strcmp(struct tiger_string *a, struct tiger_string *b);

/* Functions defined in the program. */

