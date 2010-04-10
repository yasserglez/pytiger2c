/* Tiger standard library functions. */

void tiger_print(struct tiger_string *s);

void tiger_printi(int64_t n);

void tiger_flush();

struct tiger_string *tiger_getchar();

int64_t tiger_ord(struct tiger_string *s);

struct tiger_string *tiger_chr(int64_t i);

int64_t tiger_size(struct tiger_string *s);

struct tiger_string *tiger_substring(struct tiger_string *s, int64_t f, int64_t n);

struct tiger_string *tiger_concat(struct tiger_string *s1, struct tiger_string *s2);

int64_t tiger_not(int64_t i);

int64_t tiger_exit(int64_t i);

/* Internal functions used by PyTiger2C. */

void pytiger2c_error(char *msg);

void *pytiger2c_malloc(size_t size);
