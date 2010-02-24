/* Tiger standard library functions. */

void tiger_print(struct string *s);

void tiger_printi(int64_t n);

void tiger_flush();

struct string *tiger_getchar();

int64_t tiger_ord(struct string *s);

struct string *tiger_chr(int64_t i);

int64_t tiger_size(struct string *s);

struct string *tiger_substring(struct string *s, int64_t f, int64_t n);

struct string *tiger_concat(struct string *s1, struct string *s2);

int64_t tiger_not(int64_t i);

int64_t tiger_exit(int64_t i);

/* Internal functions used by PyTiger2C. */
