/* Tiger standard library functions. */

/* Print the string on the standard output. */
void tiger_print(struct string *s)
{
}

/* Print the integer on the standard output. */
void tiger_printi(int64_t n)
{
}

/* Flush the standard output buffer. */
void tiger_flush()
{
}

/* Read and return a character from standard input; 
 * return an empty string at end-of-file. */
struct string *tiger_getchar()
{
}

/* Return the ASCII value of the first character of s,
 * or -1 if s is empty. */
int64_t tiger_ord(struct string *s)
{
}

/* Return a single-character string for ASCII value i.
 * Terminate program if i is out of range. */
struct string *tiger_chr(int64_t i)
{
}

/* Return the number of characters in s. */
int64_t tiger_size(struct string *s)
{
}

/* Return the substring of s starting at the character f (first
 * character is numbered zero) and going for n characters. */
struct string *tiger_substring(struct string *s, int64_t f, int64_t n)
{
}

/* Return a new string consisting of s1 followed by s2. */
struct string *tiger_concat(struct string *s1, struct string *s2)
{
}

/* Return 1 if i is zero, 0 otherwise. */
int64_t tiger_not(int64_t i)
{
}

/* Terminate execution of the program with code i. */
int64_t tiger_exit(int64_t i)
{
}

/* Internal functions used by PyTiger2C. */
