/* Tiger standard library functions. */

/* Print the string on the standard output. */
void tiger_print(struct tiger_string *s)
{
	if (s->length > 0) {
		fwrite(s->data, s->length, 1, stdout);
	}
}

/* Print the integer on the standard output. */
void tiger_printi(int n)
{
	fprintf(stdout, "%i", n);
}

/* Flush the standard output buffer. */
void tiger_flush()
{
	fflush(stdout);
}

/* Read and return a character from the standard input, return an empty string
 * if the end of the file is found. */
struct tiger_string *tiger_getchar()
{
	int c;
	struct tiger_string *dest;

	dest = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
	c = fgetc(stdin);
	if (c == EOF) {
		dest->data = NULL;
		dest->length = 0;
	} else {
		dest->data = (char *) pytiger2c_malloc(sizeof(char));
		dest->data[0] = (char) (c % 256);
		dest->length = 1;
	}

	return dest;
}

/* Return the ASCII value of the first character of s, or -1 if s is empty. */
int tiger_ord(struct tiger_string *s)
{
	if (s->length == 0) {
		return -1;
	} else {
		return s->data[0];
	}
}

/* Return a single-character string for the integer ASCII value i. The program
 * will terminate if the argument i is out of range. */
struct tiger_string *tiger_chr(int i)
{
	struct tiger_string *dest;

	if (i < 0 || i > 255) {
		pytiger2c_error("chr() function invoked with an invalid ASCII value.");
	}
	dest = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
	dest->data = (char *) pytiger2c_malloc(sizeof(char));
	dest->data[0] = (char) (i % 256);
	dest->length = 1;

	return dest;
}

/* Return the number of characters in s. */
int tiger_size(struct tiger_string *s)
{
	return (int) s->length;
}

/* Return the substring of s starting at the character f (first character is
 * numbered zero) and going for n characters. */
struct tiger_string *tiger_substring(struct tiger_string *s, int f, int n)
{
	struct tiger_string *sub;

	if (f < 0 || f + n > s->length)
	{
		pytiger2c_error("substring() invoked with indexes out of range.");
	}
	sub = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
	sub->data = (char *) pytiger2c_malloc(n * sizeof(char));
	sub->length = (size_t) n;
    memcpy(sub->data, s->data + f, n);

    return sub;
}

/* Return a new string consisting of s1 followed by s2. */
struct tiger_string *tiger_concat(struct tiger_string *s1, struct tiger_string *s2)
{
	struct tiger_string *conc;
	size_t conc_len;

	conc_len = s1->length + s2->length;
    conc = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
    conc->data = (char *) pytiger2c_malloc(conc_len * sizeof(char));
    conc->length = conc_len;
    memcpy(conc->data, s1->data, s1->length);
    memcpy(conc->data + s1->length, s2->data, s2->length);

    return conc;
}

/* Return 1 if i is zero, 0 otherwise. */
int tiger_not(int i)
{
	return (i == 0) ? 1 : 0;
}

/* Terminate execution of the program with code i. */
int tiger_exit(int i)
{
	exit(i);
}

/* Internal functions used by PyTiger2C. */

/* Print the given runtime error message to the standard output error and exit
 * the program with error status. */
void pytiger2c_error(char *msg)
{
	fprintf(stderr, "Runtime Error: %s\n", msg);
	exit(EXIT_FAILURE);
}

/* Wrapper to print a runtime error if could not allocate memory. */
void *pytiger2c_malloc(size_t size)
{
	void *mem;

	mem = GC_MALLOC(size);
	if (mem == NULL)
	{
		pytiger2c_error("Could not allocate memory.");
	}
	memset(mem, 0, size);

	return mem;
}

/* Auxiliar function used to compare two Tiger strings. */
int pytiger2c_strcmp(struct tiger_string *a, struct tiger_string *b)
{
    size_t a_length = a->length;
    size_t b_length = b->length;
    int result;

    result = memcmp(a->data, b->data, (a_length < b_length) ? a_length : b_length);
    if (result == 0) {
        result = a_length - b_length;
    }

    return result;
}

/* Auxiliar function used to check the array indexes. */
void pytiger2c_validate_index(size_t length, int index)
{
	if (index < 0 || index >= length) {
		pytiger2c_error("Array index is out of range.");
	}
}

/* Functions defined in the program. */

